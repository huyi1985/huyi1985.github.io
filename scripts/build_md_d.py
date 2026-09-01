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
# 冻结名单：条目 = md.d/posts 子目录名（= raw_md.d 的 md.stem）；
# 命中即跳过图片相对化、末尾 --- 过滤、裸相对图拷贝，正文原样保留（只规整 frontmatter + 注 draft）
FREEZE_PATH = BASE / "config.d" / "freeze.yaml"
# 关键词词典：正文纯子串匹配命中即作为该篇 tag（打 tag + SEO keywords meta 用）
KEYWORDS_PATH = BASE / "config.d" / "keywords.yaml"


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


def _load_name_list(path: Path) -> set[str]:
    """加载名单 yaml，返回 stem 集合（key 即 stem，不含 .md）。

    通用：blacklist/freeze 同格式（dict，key=子目录名，value=描述）。
    忽略 generated/updated 等元字段。
    """
    if not path.is_file():
        return set()
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return set()
    meta = {"generated", "updated"}
    return {k for k in data if isinstance(k, str) and k not in meta}


def load_blacklist() -> set[str]:
    """黑名单：命中注入 draft: true（不发布）。返回 stem 集合。"""
    return _load_name_list(BLACKLIST_PATH)


def load_freeze() -> set[str]:
    """冻结名单：命中则流水线不改写正文（只规整 frontmatter + 注 draft）。返回 stem 集合。"""
    return _load_name_list(FREEZE_PATH)


def load_keywords() -> list[str]:
    """关键词词典：正文纯子串匹配命中即作为 tag。返回有序词列表（顺序即 tag 优先级）。"""
    if not KEYWORDS_PATH.is_file():
        return []
    data = yaml.safe_load(KEYWORDS_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        return []
    kws = data.get("keywords") or []
    if not isinstance(kws, list):
        return []
    # 元素可能是 "词" 或 "词: 别名"，取冒号前
    # 大小写不敏感去重：仅大小写不同的词条只保留首次出现者（= 用户词典里的规范写法）
    out = []
    seen_lower = set()
    for k in kws:
        if not isinstance(k, str):
            continue
        word = k.split(":", 1)[0].strip().strip('"').strip("'")
        if not word:
            continue
        low = word.lower()
        if low in seen_lower:
            continue
        seen_lower.add(low)
        out.append(word)
    return out


def match_keywords(body: str, keywords: list[str]) -> list[str]:
    """正文纯子串匹配词典（大小写不敏感），返回命中的 tag 列表（按词典顺序，去重）。

    返回的 tag 用词典里的规范写法（首现者）。匹配基于 body 的小写形式。
    """
    if not keywords:
        return []
    body_low = body.lower()
    tags = []
    seen = set()
    for kw in keywords:
        if kw in seen:
            continue
        if kw.lower() in body_low:
            tags.append(kw)
            seen.add(kw)
    return tags


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


def restore_pool_from_bundles(window: list[Path], freeze: set[str]) -> int:
    """从现有 md.d/posts/<stem>/ 的 imgN.ext 还原图片池到 md.d/assets/。

    全量重建时若图片池（md.d/assets/）缺失，直接清空 md.d/posts 再从 raw 重建
    会丢光所有图片——因为 distribute_images 从池里拷贝图片进 bundle。
    本函数在清空前先把每个 bundle 已有的图片还原回池（imgN.ext → 原 assets 名），
    使全量重建可安全进行，无需先跑 download_images.py 重下远程图。

    映射推导：distribute_images 对 raw body 的 POOL_REF 按出现顺序给每个唯一
    assets 名分配 img{seq}.ext（seq = 已见 assets 数 +1）。此处复刻同一逻辑得到
    assets→imgN 映射，再把 bundle/imgN.ext 拷回 POOL_DIR/assetsname。

    返回还原的图片文件数。
    """
    restored = 0
    POOL_DIR.mkdir(parents=True, exist_ok=True)
    for md in window:
        stem = md.stem
        if stem in freeze:
            continue  # freeze 文章正文原样，其 bundle 图引用未相对化，跳过
        bundle = MD_DIR / "posts" / stem
        body = parse_front(md.read_text(encoding="utf-8", errors="replace"))[1]
        # 复刻 distribute_images 的 assets→imgN 顺序映射
        pool_map: dict[str, str] = {}
        for m in POOL_REF.finditer(body):
            fname = m.group(2)
            if fname not in pool_map:
                pool_map[fname] = f"img{len(pool_map) + 1}{(Path(fname).suffix or '.webp')}"
        # 从 bundle 拷回池（池里已存在则跳过，避免覆盖较新的下载版）
        for assets_name, bundle_name in pool_map.items():
            src = bundle / bundle_name
            if not src.is_file():
                continue  # bundle 里没有这张图（可能下载失败/冻结改动）→ 无法还原
            dst = POOL_DIR / assets_name
            if dst.is_file():
                continue
            shutil.copy2(src, dst)
            restored += 1
    return restored


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


# 独占一行的 ---（正文里的分隔线；frontmatter 已剥离，不会误伤 frontmatter 闭合符）
TRAILING_SEP = re.compile(r"(?ms)^---[ \t]*\r?\n(?:(?!^---[ \t]*\r?$).)*\Z")


def trim_trailing_sep(body: str) -> tuple[str, int]:
    """切掉正文最后一个独占一行的 --- 及其后的所有内容。

    用户要求：删末尾 --- 及之后所有（含译文/附录，即便实质内容也删）。
    从 body 末尾反向找最后一个 ^--- 行，从该行起截断。
    返回 (新 body, 删掉的字符数)。找不到 --- 返回原样 (body, 0)。
    """
    # 找所有独占一行的 --- 的位置，取最后一个
    matches = list(re.finditer(r"(?m)^---[ \t]*\r?$", body))
    if not matches:
        return body, 0
    last = matches[-1]
    # 截断点 = 最后一个 --- 行的起始；其后（含该行）全删
    trimmed = body[:last.start()].rstrip("\n") + "\n"
    return trimmed, len(body) - len(trimmed)


def main() -> int:
    ap = argparse.ArgumentParser(description="raw_md.d → md.d (Hugo bundle 内容目录)")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不写入")
    ap.add_argument("--limit", type=int, default=0, metavar="N",
                    help="只处理最后 N 篇（按文件名排序取尾 N 个）；默认全部")
    ap.add_argument("--revert", action="store_true",
                    help="limit 模式：把窗口外的 bundle 恢复为 git HEAD 版本（默认关闭）")
    args = ap.parse_args()

    blacklist = load_blacklist()
    freeze = load_freeze()
    keywords = load_keywords()
    log(f"黑名单：{len(blacklist)} 个" if blacklist else "黑名单：空")
    log(f"冻结名单：{len(freeze)} 个" if freeze else "冻结名单：空")
    log(f"关键词词典：{len(keywords)} 个" if keywords else "关键词词典：空")

    mds = sorted(RAW_DIR.glob("*.md"))
    if not mds:
        log(f"[ERROR] {RAW_DIR} 没有 md")
        return 1
    window = mds[-args.limit:] if args.limit > 0 else mds
    if args.limit > 0:
        log(f"limit={args.limit}：窗口 {len(window)} 篇，另有 {len(mds) - len(window)} 篇不动"
            + ("（--revert 恢复为 git HEAD）" if args.revert else ""))

    # ── 全量重建图片保护：池缺失则从现有 bundle 还原，避免清空 posts_dir 后丢图 ──
    # 全量(不带 --limit)会清空 md.d/posts 再从 raw 重建，图片依赖 md.d/assets/ 池；
    # 池在每次 build 后被删除、由 download_images.py 重建。若池不在而 raw 有 /assets/
    # 引用，直接清空 = 静默丢光所有图片。此处先从现有 bundle 的 imgN.ext 还原池，
    # 使全量重建可安全进行。仅当无任何 bundle 可还原（首次构建）才中止。
    if not args.dry_run and args.limit == 0:
        pool_exists = POOL_DIR.is_dir() and any(POOL_DIR.iterdir())
        if not pool_exists:
            n = restore_pool_from_bundles(window, freeze)
            if n > 0:
                log(f"图片池缺失：从现有 bundle 还原 {n} 个图片到 {POOL_DIR}")
            else:
                # 无 bundle 可还原：raw 里有 /assets/ 引用但池空且 bundle 也没图
                pool_refs = sum(
                    len(POOL_REF.findall(md.read_text(encoding="utf-8", errors="replace")))
                    for md in window if md.stem not in freeze
                )
                if pool_refs > 0:
                    log(f"[ERROR] 全量重建需要图片池（raw 有 {pool_refs} 处 /assets/ 引用），"
                        f"但 {POOL_DIR} 空且现有 bundle 无图可还原。")
                    log("        请先跑： python3.11 scripts/download_images.py   重建图片池，")
                    log("        或改用增量： python3.11 scripts/build_md_d.py --limit N   只重建末尾 N 篇（不清空）。")
                    return 1

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
    freeze_count = 0
    img_copied = 0
    trim_total = 0
    kw_count = 0
    trim_count = 0
    pool = {p.name: p for p in POOL_DIR.iterdir()} if POOL_DIR.is_dir() else {}
    log(f"图片池：{len(pool)} 个文件（{POOL_DIR}）" if pool else "图片池：空/不存在（引用保持原样）")

    for md in window:
        content = md.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_front(content)
        stem = md.stem
        bundle = posts_dir / stem
        is_freeze = stem in freeze
        is_draft = stem in blacklist
        # 末尾 --- 过滤（freeze 跳过；先切末尾再分拣图片，避免附录里的图被分拣）
        if not is_freeze:
            body, trimmed = trim_trailing_sep(body)
            if trimmed:
                trim_total += trimmed
                trim_count += 1
        if args.dry_run:
            n_img = len(POOL_REF.findall(body))
            tag = []
            if is_draft: tag.append("draft")
            if is_freeze: tag.append("FREEZE")
            if not is_freeze and trimmed: tag.append(f"trim-{trimmed}")
            if not is_freeze and keywords:
                kw_hit = len(match_keywords(body, keywords))
                if kw_hit:
                    tag.append(f"kw{kw_hit}")
            log(f"  [PLAN] {stem}  (tags={fm.get('tags')}, 池图{n_img}{' ['+' '.join(tag)+']' if tag else ''})")
            moved += 1
            continue
        if is_draft:
            fm["draft"] = True
            draft_count += 1
        if is_freeze:
            freeze_count += 1
        bundle.mkdir(parents=True, exist_ok=True)
        if is_freeze:
            # 冻结：正文原样保留，仅规整 frontmatter（不相对化图片、不分拣）
            new_body, _map = body, {}
        else:
            # 关键词打 tag：正文纯子串匹配（大小写不敏感）。已有 tags 则不覆盖。
            if not fm.get("tags") and keywords:
                matched = match_keywords(body, keywords)
                if matched:
                    fm["tags"] = matched
                    kw_count += len(matched)
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
        f"{freeze_count} 篇 freeze，分拣图片 {img_copied} 个，"
        f"末尾---过滤 {trim_count} 篇共 {trim_total} 字，关键词打 tag {kw_count} 个）" if not args.dry_run
        else f"dry-run：{moved} 篇将写入 {MD_DIR}/posts/（{freeze_count} freeze，"
        f"{trim_count} 篇将被 trim 共 {trim_total} 字，关键词打 tag {kw_count} 个）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
