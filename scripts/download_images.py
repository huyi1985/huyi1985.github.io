#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
download_images.py — 流水线第 2 阶段：图床图片本地化 + WebP 压缩 → raw_md.d/assets/

流水线设计（用户已确认）：
  1) collect_posts.py    提取文章 md → raw_md.d/（扁平，纯 md）
  2) [本脚本] 解析 raw_md.d 里 md 的图片引用（![..](https://图床/..)），
       下载图片 → raw_md.d/assets/，转 WebP 压缩，
       并把 md 里的引用改写为绝对路径 /assets/xxx.webp
  3) [未来脚本] 生成 Hugo 可消费的 md.d/（规范 slug、frontmatter；md.d 已含改写后的引用）

行为契约：
  1. 只读 raw_md.d，绝不动源目录；产物集中在 raw_md.d/assets/
  2. 只处理"图片链接"：正则匹配 ![alt](target)，target 为 URL 或相对路径
  3. 远程图（http/https）统一下载到 assets/；文件名用原 URL 最后一段（sanitize）
  4. 转换 WebP：优先 cwebp/sips 命令，缺失用 Pillow 兜底；转换失败保持原格式
  5. 重复 URL 只下载一次（md 内多处引用 → 同一个 assets 文件）
  6. 幂等：assets 文件已存在则跳过；--force 强制重下
  7. md 内的引用被改写为 /assets/<name>.webp（本地路径引用保留不下载）
  8. 失败/跳过不误改 md；改写是"整块"的——全部图就绪才替换，保证 md 原子一致

用法：
    python3 scripts/download_images.py            # 下载 + 转换 + 改写（幂等）
    python3 scripts/download_images.py --force    # 强制重下已存在的图片
    python3 scripts/download_images.py --dry-run  # 只预览（不下载/不改写）
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    sys.exit("缺少 requests 库，请先安装：python3.11 -m pip install requests")

# ── 可配置清单 ──────────────────────────────────────────────
# 待处理的 md 根目录（raw_md.d/，纯 md 提取物）
CONTENT_DIR = Path(__file__).resolve().parent.parent / "raw_md.d"
# 下载后的图片集中存放目录（与 md 同根的 assets/，Hugo 挂 /assets/）
ASSETS_DIR = CONTENT_DIR / "assets"

# 图片扩展名（决定哪些链接算"图片"，需要本地化）
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".avif"}

# 下载超时 / UA（部分图床按 UA 判断；带 UA 更稳）
TIMEOUT = 60
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

# 匹配 md 图片语法：![alt](target)。target 可能带标题（"url \"title\""），取 url 段。
IMG_RE = re.compile(r"!\[([^\]]*)\]\(([^)]*)\)")


def log(msg: str) -> None:
    print(msg, flush=True)


def is_remote_url(url: str) -> bool:
    return urlparse(url).scheme in ("http", "https")


def parse_target(raw: str) -> str:
    """从 ![alt](TARGET) 的 TARGET 里剥离可选标题，返回纯 url。

    Markdown 允许 `(url "title")`；这里按空白切分取第一段，兼容带标题的写法。
    """
    return raw.split()[0].strip()


def pick_filename(url: str) -> str:
    """由 URL 决定落盘文件名（原始文件名段，去掉 query 参数，做安全化）。

    图床形如 p.ipic.vip/elpjzf.png 可直接用尾段；
    带 query（如 mmbiz.qpic.cn/.../640?wx_fmt=png）需剥掉 ? 后的部分。
    """
    path = urlparse(url).path
    name = path.rsplit("/", 1)[-1] if "/" in path else path
    if not name:  # URL 没有文件名段（罕见），用 md5 兜底
        import hashlib

        name = hashlib.md5(url.encode()).hexdigest()[:12] + ".img"
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-")
    return name


def ext_from_url(url: str) -> str:
    """推断 URL 的图片扩展名（含 query 形式 mmbiz.qpic.cn/.../640?wx_fmt=png）。"""
    path = urlparse(url).path
    lower = path.lower()
    for e in sorted(IMAGE_EXTS, key=len, reverse=True):
        if lower.endswith(e):
            return e
    # 无扩展名：看 query（wx_fmt=png）
    q = urlparse(url).query
    fm = re.search(r"(?:wx_fmt|format)=([a-z0-9]+)", q, re.I)
    if fm:
        cand = fm.group(1).lower()
        if "." + cand in IMAGE_EXTS:
            return "." + cand
    return ".png"  # 兜底：内容探测会在下载后修正


def safe_ext(data: bytes) -> str:
    """按文件头魔数探测真实格式；探测不到返回原 ext 兜底。

    cwebp/sips 需要正确的输入格式才能转换，魔数优先于 URL 扩展名。
    """
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return ".gif"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return ".webp"
    if data.startswith(b"<svg") or b"<svg" in data[:256]:
        return ".svg"
    if data.startswith(b"BM"):
        return ".bmp"
    return ""  # 无法识别


def webp_bin() -> str | None:
    return shutil.which("cwebp")


def to_webp(src: Path, dest: Path) -> bool:
    """把 src 转成 WebP 存到 dest。优先 cwebp，其次 sips（macOS 自带），最后 Pillow。

    返回是否成功；全失败则返回 False，调用方保持原格式。
    注：WebP 不支持 alpha，透明 PNG 若转 WebP 会丢透明 → 转换器会失败或出黑底，
    故透明 png 保持 .png 不转（detect 阶段由调用方判断）。
    """
    # 透明 PNG 不转 WebP（WebP 会丢 alpha → 黑底）
    if src.suffix.lower() == ".png":
        try:
            import struct

            with open(src, "rb") as f:
                head = f.read(48)
            # PNG IHDR 第 25 字节：0=灰度 2=RGB 3=索引 4=灰度+alpha 6=RGBA
            color_type = head[25]
            if color_type in (4, 6):
                return False
        except Exception:
            pass

    # 1) cwebp（Google 官方，质量最高）
    exe = webp_bin()
    if exe:
        cmd = [exe, "-quiet", "-q", "80", str(src), "-o", str(dest)]
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=120)
            if r.returncode == 0 and dest.exists() and dest.stat().st_size > 0:
                return True
        except Exception:
            pass
    # 2) sips（macOS 自带，能读 webp 输出）
    elif sys.platform == "darwin" and shutil.which("sips"):
        tmp = src.with_suffix(".webp.tmp")
        try:
            r = subprocess.run(
                ["sips", "-s", "format", "webp", str(src), "--out", str(tmp)],
                capture_output=True, timeout=180,
            )
            if r.returncode == 0 and tmp.exists():
                tmp.replace(dest)
                return True
        except Exception:
            pass
    # 3) Pillow 兜底
    try:
        from PIL import Image

        im = Image.open(src)
        im.convert("RGB").save(dest, "WEBP", quality=80)
        return True
    except Exception:
        return False
    return False


def download_one(url: str, session: requests.Session) -> bytes:
    """下载图片。优先 requests；遇到被反爬/拒绝（400/403 等），
    或 requests 无法处理的 URL（如未编码的括号），回退到 curl。

    requests 与 curl 对部分图床（wikimedia 的 (1974) 括号、sstatic 的反爬）
    行为不一致：requests 直接 400/403，curl 却 200。这里做两层兜底。
    """
    from urllib.parse import quote

    urls = [url]
    # 对 path 部分做百分号编码（保留已编码的 %xx；未编码的括号/空格等转正）：
    # wikimedia 的 "(1974)" 只有 curl 能拉，requests 会 400。
    parsed = urlparse(url)
    if any(c in parsed.path for c in "() ") and not any(
        c in parsed.path for c in ["%28", "%29", "%20"]
    ):
        qpath = quote(parsed.path, safe="/%:-_.~")
        urls.insert(0, parsed._replace(path=qpath).geturl())

    last_exc: Exception | None = None
    for cand in urls:
        try:
            r = session.get(cand, headers=HEADERS, timeout=TIMEOUT)
            if r.status_code == 200:
                return r.content
            last_exc = RuntimeError(f"HTTP {r.status_code}")
        except Exception as e:
            last_exc = e
    # requests 全家失败 → 用 curl 兜底（图床反爬常见，curl 默认 UA 更不易被拦）
    exe = shutil.which("curl")
    if exe:
        import subprocess

        try:
            r = subprocess.run(
                [exe, "-sSL", "-A", HEADERS["User-Agent"], "--max-time", str(TIMEOUT), url],
                capture_output=True, timeout=TIMEOUT + 10,
            )
            if r.returncode == 0 and r.stdout:
                return r.stdout
            last_exc = RuntimeError(f"curl exit {r.returncode}")
        except Exception as e:
            last_exc = e
    raise last_exc or RuntimeError("download failed")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="流水线第 2 阶段：把图床图片下载到 raw_md.d/assets/，转 WebP，改写 md 引用"
    )
    parser.add_argument("--force", "-f", action="store_true",
                        help="强制重新下载已存在的图片（默认：存在则跳过）")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不下载/不改写")
    args = parser.parse_args()

    mds = sorted(CONTENT_DIR.glob("*.md"))
    if not mds:
        log(f"  [ERROR    ] {CONTENT_DIR} 下没有 md 文件")
        return 1

    session = requests.Session()
    plan: list[dict] = []
    stats = {"found": 0, "local": 0, "remote": 0, "downloaded": 0,
             "converted": 0, "kept": 0, "skipped": 0, "failed": 0}

    # 预扫描每个 md，收集 (md, refs) 列表；refs = [(原文本, url, 目标assets名, 是否远程)]
    tasks = []
    for md in mds:
        text = md.read_text(encoding="utf-8", errors="replace")
        refs = []
        for m in IMG_RE.finditer(text):
            url = parse_target(m.group(2))
            if not url or not url.strip():
                continue
            if not (is_remote_url(url) or url.startswith("/")):
                continue  # 跳过非链接引用
            stats["found"] += 1
            if url.startswith("/"):  # 已是本地绝对路径（前序产物可能已改写）
                stats["local"] += 1
                continue
            name = pick_filename(url)
            if name.lower().endswith(tuple(IMAGE_EXTS)):
                fname = name
            else:
                # 无扩展名 URL：先按内容探测（下载后修正 ext）
                fname = name + ext_from_url(url)
            refs.append((m.group(0), url, fname, is_remote_url(url)))
            stats["remote"] += 1
        if refs:
            tasks.append((md, text, refs))

    if args.dry_run:
        for md, _, refs in tasks:
            log(f"== {md.relative_to(CONTENT_DIR)}")
            for _orig, url, fname, remote in refs:
                log(f"  [PLAN     ] {url} → {fname} ({'remote' if remote else 'local'})")
        log(f"dry-run：{len(mds)} 篇 md，{len(tasks)} 篇含图，"
            f"{stats['remote']} 个远程引用，{stats['local']} 个已是本地引用")
        return 0

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # ── 第一遍：下载 + 转换（不读写 md，保证 md 原子性）──
    # 记录 URL → 最终 assets 文件名（含修正后的 ext）；转换失败则保持原 ext 原文件
    url_to_assets: dict[str, str] = {}
    for md, _t, refs in tasks:
        for _orig, url, fname, remote in refs:
            if not remote or url in url_to_assets:
                continue
            if not is_remote_url(url):
                continue
            ext = Path(fname).suffix.lower()
            stem = Path(fname).stem

            # 幂等跳过（assets 已存在且 --force 未开）
            existing = [
                p for p in ASSETS_DIR.glob(f"{stem}*") if p.is_file()
            ]
            if existing and not args.force:
                url_to_assets[url] = existing[0].name
                stats["skipped"] += 1
                continue

            # 下载
            try:
                data = download_one(url, session)
            except Exception as e:
                log(f"  [FAIL     ] {url} → {e}")
                stats["failed"] += 1
                continue

            # 修正真实扩展名（魔数优先）
            sniff = safe_ext(data)
            if sniff:
                ext_used = sniff
            else:
                ext_used = ext if ext in IMAGE_EXTS else ".png"
            raw_name = f"{stem}{ext_used}"
            raw_path = ASSETS_DIR / raw_name
            raw_path.write_bytes(data)
            stats["downloaded"] += 1
            url_to_assets[url] = raw_name  # 先用原格式名，md 引用待转换后统一修正

            # 转 WebP（png/jpg/gif/webp 都尝试；透明 png/svg/失败 → 保持原格式）
            if ext_used in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
                webp_path = ASSETS_DIR / f"{stem}.webp"
                if to_webp(raw_path, webp_path):
                    raw_path.unlink(missing_ok=True)  # 只保留 webp
                    url_to_assets[url] = f"{stem}.webp"
                    stats["converted"] += 1
                else:
                    stats["kept"] += 1
            else:
                stats["kept"] += 1
            log(f"  [OK       ] {raw_name if url_to_assets[url].endswith(raw_name) else url_to_assets[url]}  ← {url}")

    # ── 第二遍：改写 md（全部引用解析完毕，统一替换，未下载成功的引用保持原样）──
    for md, text, refs in tasks:
        new_text = text
        changed = False
        for orig, url, _fname, remote in refs:
            if not remote:
                continue
            assets_name = url_to_assets.get(url)
            if not assets_name:
                continue  # 该 URL 下载失败 → md 里保留原图床引用，不误改
            new_ref = f"![{re.match(IMG_RE, orig).group(1)}](/assets/{assets_name})"
            if orig != new_ref:
                new_text = new_text.replace(orig, new_ref)
                changed = True
        if changed:
            md.write_text(new_text, encoding="utf-8")
            log(f"  [REWRITE  ] {md.relative_to(CONTENT_DIR)}")

    log(f"完成：{len(mds)} 篇 md / {stats['remote']} 远程引用 → "
        f"下载 {stats['downloaded']}（新下 {stats['downloaded']}，复用 {stats['skipped']}，"
        f"失败 {stats['failed']}）| 转 WebP {stats['converted']}，保持原格式 {stats['kept']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
