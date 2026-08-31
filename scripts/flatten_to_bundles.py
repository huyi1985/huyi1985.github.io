#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
flatten_to_bundles.py — 一次性迁移：md.d/ 扁平结构 → Hugo page bundle 结构

现状：md.d/*.md 平铺 + md.d/assets/ 全局图片池 + md.d/static/（footer 二维码）
目标：md.d.new/posts/<md文件名去.md>/index.md + 图片同目录（相对引用）

迁移规则：
  1. 目录名 = md 文件名去掉 .md（如 2024-07-30-XXX.md → posts/2024-07-30-XXX/）
  2. index.md = 原文（frontmatter 原样保留，含 draft）
  3. 图片：
     - /assets/xxx 且池中有文件 → 拷入该文章目录，命名 img1/img2/...（保持原扩展名），
       引用改写为相对 imgN.ext
     - /assets/xxx 但池中无文件（失效引用）→ 引用同样改写为 imgN.ext（保持现状：无文件不显示）
     - 裸文件名引用（4 处 nasm-*.png）→ 本地文件随文拷入，引用不变（已是相对）
     - 共享图片（多篇文章引用同一 assets 文件）→ 每篇各自复制一份，彻底解耦
  4. static/ 原样拷到 md.d.new/static/
  5. 输出到 md.d.new/（只读输入，绝不改 md.d/），验证通过后再手动替换

用法：
    python3 scripts/flatten_to_bundles.py          # 迁移到 md.d.new/
    python3 scripts/flatten_to_bundles.py --dry-run # 只预览
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "md.d"          # 输入：扁平结构
DST = BASE / "md.d.new"      # 输出：page bundle 结构
ASSETS = SRC / "assets"
STATIC = SRC / "static"

IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".svg")

# 图片引用两种形态：
#  1) ![](/assets/FILE.EXT)            → 全局池，池里有文件
#  2) ![](local-file.png)（裸文件名）   → 本地文件（nasm-*.png 那类）
POOL_REF = re.compile(r'!\[([^\]]*)\]\(/assets/([^)\s]+)\)')
LOCAL_REF = re.compile(r'!\[([^\]]*)\]\(([^)\s/][^)\s]*\.(?:png|jpe?g|webp|gif|bmp|svg))\)', re.I)
# 注意 LOCAL_REF 要求路径不以 http 或 / 开头（排除远程图与 /assets/，避免重复匹配）。
# 池引用改写后产生的 imgN.ext 不应再被 LOCAL_REF 当作"本地裸文件"二次匹配
NEW_IMG_REF = re.compile(r'!\[[^\]]*\]\(img\d+\.(?:png|jpe?g|webp|gif|bmp|svg)\)', re.I)


def log(msg: str) -> None:
    print(msg, flush=True)


def pick_new_name(n: int, ext_with_dot: str) -> str:
    """目录内图片命名：img1.ext, img2.ext…（弃用全局 <日期>-<序号>-img<序号> 模式）。"""
    return f"img{n}{ext_with_dot}"


def main() -> int:
    ap = argparse.ArgumentParser(description="md.d 扁平 → page bundle 一次性迁移")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不写入")
    args = ap.parse_args()

    src_ok = SRC.is_dir() and (ASSETS.is_dir() or STATIC.is_dir())
    if not src_ok:
        log(f"[ERROR] 找不到输入结构：{SRC}")
        return 1
    if DST.exists():
        log(f"[ERROR] 输出目录已存在，先移走/删除：{DST}")
        return 1

    mds = sorted(SRC.glob("*.md"))
    log(f"待迁移 {len(mds)} 篇 md；assets 池 {len(list(ASSETS.glob('*')))} 个文件")

    # 预扫：assets 池文件集合 + 每篇引用
    pool_files = {p.name: p for p in ASSETS.glob("*") if p.is_file()}
    # 本地文件（裸文件名引用的源）：md.d/<md名> 旁的同名文件
    local_files = {p.name: p for p in SRC.glob("*") if p.is_file() and p.suffix.lower() in IMG_EXT}
    log(f"md.d 根下随 md 并存的本地图片文件：{len(local_files)} 个")

    shared_report: dict[str, set[str]] = {}
    missing_report: list[tuple[str, str]] = []  # (md, assets名)
    total_imgs = 0
    total_copied = 0

    for md in mds:
        content = md.read_text(encoding="utf-8", errors="replace")
        bundle = DST / "posts" / md.stem
        if args.dry_run:
            n_pool = len(POOL_REF.findall(content))
            n_local = len(LOCAL_REF.findall(content))
            log(f"  [PLAN] {md.stem}  (池图{n_pool} 本地图{n_local})")
            continue

        bundle.mkdir(parents=True, exist_ok=True)
        # index.md 先拷原文；随后做引用改写并回写
        index = bundle / "index.md"
        index.write_text(content, encoding="utf-8")

        # 1) 池引用 → 拷贝 + 改相对
        pool_map: dict[str, str] = {}   # assets名 → 新文件名
        seq = 0
        for alt, fname in POOL_REF.findall(content):
            src = pool_files.get(fname)
            if fname not in pool_map:
                seq += 1
                ext = Path(fname).suffix if Path(fname).suffix else ".webp"
                new_name = pick_new_name(seq, ext)
                pool_map[fname] = new_name
                shared_report.setdefault(fname, set()).add(md.name)
                if src:
                    shutil.copy2(src, bundle / new_name)
                    total_copied += 1
                else:
                    missing_report.append((md.name, fname))
                    log(f"  [缺图] {md.name} → /assets/{fname}（无池文件，仅改引用）")
            content = content.replace(
                f"![{alt}](/assets/{fname})", f"![{alt}]({pool_map[fname]})"
            )
        total_imgs += len(pool_map)

        # 2) 裸文件名本地引用：文件随文拷入，引用不变（排除已改写的 imgN.ext）
        for alt, fname in dict.fromkeys(LOCAL_REF.findall(content)):
            if fname in pool_map:
                continue
            if NEW_IMG_REF.search(f"![x]({fname})"):
                continue
            src = local_files.get(fname) or (SRC / fname)
            if src and src.is_file():
                shutil.copy2(src, bundle / fname)
                total_copied += 1
            else:
                log(f"  [缺图] {md.name} → {fname}（本地无文件）")

        index.write_text(content, encoding="utf-8")

    # 3) static/ 拷贝
    if STATIC.is_dir() and not args.dry_run:
        shutil.copytree(STATIC, DST / "static")
        log(f"static/ 拷贝完成（{', '.join(p.name for p in STATIC.iterdir()) if STATIC.iterdir() else '空'}）")

    # 报告
    shared = {k: v for k, v in shared_report.items() if len(v) > 1}
    log(f"\n=== 迁移完成 ===")
    log(f"文章 {len(mds)} 篇 → {DST}/posts/<名>/")
    log(f"拷贝图片 {total_copied} 个文件；文章内图片引用 {total_imgs} 处")
    if shared:
        log(f"共享图片 {len(shared)} 组（每篇各复制一份）：")
        for k, v in sorted(shared.items()):
            log(f"    {k} ← {len(sorted(v))} 篇：{sorted(v)}")
    if missing_report:
        log(f"失效引用（引用池外文件）{len(missing_report)} 处：")
        for md, f in missing_report:
            log(f"    {md} → /assets/{f}")
    else:
        log("无失效引用")
    return 0


if __name__ == "__main__":
    sys.exit(main())
