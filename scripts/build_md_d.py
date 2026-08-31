#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_md_d.py — 流水线第 3 阶段：raw_md.d/ → md.d/（Hugo 直接消费，page bundle 结构）

把阶段②处理好的 raw_md.d（md 内图片引用可能是 /assets/xxx.webp 或原图床 URL）迁移成
Hugo page bundle 内容目录：
  - raw_md.d/*.md → md.d/posts/<md文件名去.md>/index.md
    （frontmatter 规整：去 source；黑名单注入 draft）
  - download_images.py 下载的图片池（md.d/assets/，由该脚本先写入）被"分拣"进各文章
    bundle 目录并改名为 img1/img2/...（弃用全局 <日期>-<序号>-img<序号> 命名），
    引用统一改写为相对路径（与文章同目录），随后删除图片池（已不再需要）
  - 未被 download 处理的引用（原图床 URL / 本地相对）原样保留

frontmatter 规则（同旧版）：
  - 保留 title / date / tags（如有）；去掉 source 字段（内部溯源，不发布）
  - 无 tags 的文章不加空数组
  - 黑名单中的文件注入 draft: true（不发布）

行为契约：
  1. 只读 raw_md.d，绝不改动（那是中间产物 + 可重跑的输入）
  2. md.d 每次全量重建（先清空再写入），保证与 raw_md.d 同步
  3. 幂等：重复运行结果一致；--dry-run 只预览
  4. --limit N：只重建最后 N 篇（输入按文件名排序取尾 N 个），其它 bundle 不动；
     配合 --revert 把非窗口文章恢复为 git HEAD 版本（默认关闭），
     方便日常增量发布时把"窗口外"的已发布文章还原到与 HEAD 一致

用法：
    python3 scripts/build_md_d.py             # 重建 md.d/（bundle 结构）
    python3 scripts/build_md_d.py --limit 5   # 只重建最后 5 篇
    python3 scripts/build_md_d.py --limit 5 --revert  # 只重建最后5篇，其余恢复为 git HEAD
    python3 scripts/build_md_d.py --dry-run   # 预览（不写入）
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("缺少 PyYAML 库：python3.11 -m pip install pyyaml")

BASE = Path(__file__).resolve().parent.parent
RAW_DIR = BASE / "raw_md.d"      # 输入：阶段②产物
MD_DIR = BASE / "md.d"           # 输出：Hugo contentDir
POOL_DIR = MD_DIR / "assets"     # download_images.py 下载的临时图片池（build 后清除）

POOL_REF = re.compile(r'!\[([^\]]*)\]\(/assets/([^)\s]+)\)')
# 裸相对引用的本地图（如 nasm-two-num-sum-N.png）：引用处同级找源文件
LOCAL_REF = re.compile(r'!\[([^\]]*)\]\(([^)\s/][^)\s]*\.(?:png|jpe?g|webp|gif|bmp|svg))\)', re.I)
# 池引用改写后产生的 imgN.ext 不应被 LOCAL_REF 二次匹配
NEW_IMG = re.compile(r'^img\d+\.(?:png|jpe?g|webp|gif|bmp|svg)$', re.I)

# 本地图源：raw_md.d/ 下与文章同级的 md/图文件（download_images 未本地化的遗留）
LOCAL_SRC_DIRS = (RAW_DIR,)

FRONT_KEYS = ("title", "date", "tags", "draft")  # 只保留这些；去 source

# 黑名单：filename.md → description（不发布的文章）
BLACKLIST_PATH = BASE / "config.d" / "blacklist.yaml"


def log(msg: str) -> None:
    print(msg, flush=True)


def parse_front(content: str) -> tuple[dict, str]:
    """取 YAML frontmatter + body（兼容无 frontmatter）。"""
    if content.startswith("---\n"):
        end = content.find("\n---", 4)
        if end != -1:
            fm = yaml.safe_load(content[4:end]) or {}
            return (fm if isinstance(fm, dict) else {}), content[end + 4:]
    return {}, content


def dump_front(fm: dict) -> str:
    body = yaml.safe_dump(
        {k: fm[k] for k in FRONT_KEYS if k in fm and fm[k]},
        allow_unicode=True, sort_keys=False, default_flow_style=False,
    )
    return "---\n" + body + "---\n\n"


def load_blacklist() -> set[str]:
    """加载黑名单，返回文件名集合（不含目录路径）。"""
    if not BLACKLIST_PATH.is_file():
        return set()
    data = yaml.safe_load(BLACKLIST_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return set()
    meta = {"generated", "updated"}
    return {k for k in data if isinstance(k, str) and k not in meta}


def git_restore_bundle(stem: str) -> bool:
    """把 md.d/posts/<stem>/ 整个 bundle 恢复为 git HEAD 版本。

    仅用于 --limit 模式下处理"窗口外"文章：它们不是本次要重建的对象，
    若工作区里已被改动/删除，恢复为 HEAD 即可保持与已发布版本一致。
    """
    dest = MD_DIR / "posts" / stem
    try:
        import subprocess
        r = subprocess.run(
            ["git", "checkout", "HEAD", "--", str(dest)],
            capture_output=True, text=True,
        )
        return r.returncode == 0
    except Exception:
        return False


def distribute_images(bundle: Path, content: str) -> tuple[str, dict]:
    """把内容里的 /assets/xxx.ext 引用改写为 bundle 目录内的相对引用 imgN.ext。

    用正则逐处 sub（不重建字符串，避免 alt 含特殊字符/空串时 replace 失配），
    从 POOL_DIR 拷贝对应文件进 bundle；共享图片每篇各复制一份（解耦）。
    返回 (改写后 content, {assets名: bundle内文件名, ...})。
    """
    pool_map: dict[str, str] = {}

    def _sub(m: re.Match) -> str:
        alt, fname = m.group(1), m.group(2)
        if fname not in pool_map:
            seq = len(pool_map) + 1
            ext = Path(fname).suffix if Path(fname).suffix else ".webp"
            pool_map[fname] = f"img{seq}{ext}"
            src = POOL_DIR / fname
            if src.is_file():
                shutil.copy2(src, bundle / pool_map[fname])
        return f"![{alt}]({pool_map[fname]})"

    content = POOL_REF.sub(_sub, content)
    return content, pool_map


def main() -> int:
    ap = argparse.ArgumentParser(description="raw_md.d → md.d (Hugo bundle 内容目录)")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不写入")
    ap.add_argument("--limit", type=int, default=0, metavar="N",
                    help="只处理最后 N 篇（按文件名排序取尾 N 个）；默认全部")
    ap.add_argument("--revert", action="store_true",
                    help="limit 模式：把窗口外的 bundle 恢复为 git HEAD 版本（默认关闭）")
    args = ap.parse_args()

    blacklist = load_blacklist()
    log(f"黑名单：{len(blacklist)} 个文件" if blacklist else "黑名单：空")

    mds = sorted(RAW_DIR.glob("*.md"))
    if not mds:
        log(f"[ERROR] {RAW_DIR} 没有 md")
        return 1
    window = mds[-args.limit:] if args.limit > 0 else mds
    if args.limit > 0:
        log(f"limit={args.limit}：窗口 {len(window)} 篇，另有 {len(mds) - len(window)} 篇不动"
            + ("（--revert 恢复为 git HEAD）" if args.revert else ""))

    posts_dir = MD_DIR / "posts"
    if not args.dry_run:
        # 全量：清空 md.d/posts（保留 static/）
        if args.limit == 0:
            if posts_dir.exists():
                shutil.rmtree(posts_dir)
        elif args.revert:
            for md in mds:
                if md.name in (w.name for w in window):
                    continue
                if git_restore_bundle(md.stem):
                    log(f"  [REVERT   ] {md.stem} ← git HEAD")
                else:
                    log(f"  [SKIP     ] {md.stem}（git 恢复失败，保持现状）")
        posts_dir.mkdir(parents=True, exist_ok=True)

    moved = 0
    draft_count = 0
    img_copied = 0
    pool = {p.name: p for p in POOL_DIR.iterdir()} if POOL_DIR.is_dir() else {}
    log(f"图片池：{len(pool)} 个文件（{POOL_DIR}）" if pool else "图片池：空/不存在（引用保持原样）")

    for md in window:
        content = md.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_front(content)
        bundle = posts_dir / md.stem
        if args.dry_run:
            n_img = len(POOL_REF.findall(content))
            log(f"  [PLAN] {md.stem}  (tags={fm.get('tags')}, 池图{n_img})")
            moved += 1
            continue
        if md.name in blacklist:
            fm["draft"] = True
            draft_count += 1
        bundle.mkdir(parents=True, exist_ok=True)
        # 在 body 上做图片相对化（frontmatter 由 fm 重新 dump，不参与引用改写）
        new_body, _map = distribute_images(bundle, body)
        img_copied += len(_map)
        # 裸相对本地图：从源查找并拷入（缺失则忽略）
        for alt, fname in dict.fromkeys(LOCAL_REF.findall(new_body)):
            if fname in _map.values() or NEW_IMG.match(fname):
                continue
            src = next((d / fname for d in LOCAL_SRC_DIRS if (d / fname).is_file()), None)
            if src:
                shutil.copy2(src, bundle / fname)
                img_copied += 1
        (bundle / "index.md").write_text(dump_front(fm) + new_body.lstrip("\n"), encoding="utf-8")
        moved += 1

    if not args.dry_run and args.limit == 0 and pool:
        # 图片已全部分拣进 bundle，删除临时池（download 阶段可再生成）
        shutil.rmtree(POOL_DIR, ignore_errors=True)
        log(f"图片池已消费并删除：{POOL_DIR}")

    log(f"完成：{moved} 篇 md → {MD_DIR}/posts/（{draft_count} 篇 draft，"
        f"分拣图片 {img_copied} 个）" if not args.dry_run
        else f"dry-run：{moved} 篇将写入 {MD_DIR}/posts/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
