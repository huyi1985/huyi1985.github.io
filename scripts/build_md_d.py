#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_md_d.py — 流水线第 3 阶段：raw_md.d/ → md.d/（Hugo 直接消费）

把阶段②处理好的 raw_md.d（md 内图片引用已是 /assets/xxx.webp）迁移成 Hugo 内容目录：
  - raw_md.d/*.md      → md.d/*.md       （文件名不变，frontmatter 规整：去 source）
  - raw_md.d/assets/   → md.d/assets/    （图片本地资源，Hugo 以静态挂载 /assets/）
  - md 内 /assets/ 引用原样保留（绝对路径，与静态挂载一致）

frontmatter 规则：
  - 保留 title / date / tags（如有）；去掉 source 字段（内部溯源，不发布）
  - 无 tags 的文章不加空数组（Hugo 列表页无标签时不显示标签行）
  - 用 PyYAML 序列化，与 collect_posts.py 一致的转义保证

行为契约：
  1. 只读 raw_md.d，绝不改动（那是中间产物 + 可重跑的输入）
  2. md.d 每次全量重建（先清空再写入），保证与 raw_md.d 同步
  3. 幂等：重复运行结果一致；--dry-run 只预览

用法：
    python3 scripts/build_md_d.py             # 重建 md.d/
    python3 scripts/build_md_d.py --dry-run   # 预览（不写入）
    python3 scripts/build_md_d.py --no-assets # 不拷贝 assets（调试 md 结构）
"""

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("缺少 PyYAML 库：python3.11 -m pip install pyyaml")

BASE = Path(__file__).resolve().parent.parent
RAW_DIR = BASE / "raw_md.d"      # 输入：阶段②产物
MD_DIR = BASE / "md.d"           # 输出：Hugo contentDir
ASSETS_SRC = RAW_DIR / "assets"
ASSETS_DST = MD_DIR / "assets"

FRONT_KEYS = ("title", "date", "tags")  # 只保留这 3 个；去 source


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


def main() -> int:
    ap = argparse.ArgumentParser(description="raw_md.d → md.d (Hugo 内容目录)")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不写入")
    ap.add_argument("--no-assets", action="store_true",
                    help="不拷贝 assets（仅调试 md 结构）")
    args = ap.parse_args()

    mds = sorted(RAW_DIR.glob("*.md"))
    if not mds:
        log(f"[ERROR] {RAW_DIR} 没有 md")
        return 1

    if not args.dry_run:
        # 全量重建：清空 md.d 内容（不含 assets 之外的东西）
        for p in MD_DIR.glob("*"):
            import shutil

            shutil.rmtree(p) if p.is_dir() else p.unlink()
        MD_DIR.mkdir(parents=True, exist_ok=True)

    moved = 0
    skipped = 0
    for md in mds:
        content = md.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_front(content)
        dest = MD_DIR / md.name
        if args.dry_run:
            log(f"  [PLAN] {md.name}  (tags={fm.get('tags')}) ")
            moved += 1
            continue
        dest.write_text(dump_front(fm) + body.lstrip("\n"), encoding="utf-8")
        moved += 1
    if not args.dry_run:
        # 拷贝 assets（增量：只拷贝新增/变更的，避免覆盖已有手调）
        import shutil

        if args.no_assets:
            log("  跳过 assets 拷贝（--no-assets）")
        elif ASSETS_SRC.is_dir():
            ASSETS_DST.mkdir(parents=True, exist_ok=True)
            copied = 0
            for src_f in ASSETS_SRC.iterdir():
                if not src_f.is_file():
                    continue
                dst_f = ASSETS_DST / src_f.name
                if not dst_f.exists() or dst_f.stat().st_size != src_f.stat().st_size:
                    shutil.copy2(src_f, dst_f)
                    copied += 1
            log(f"  assets 拷贝：{copied} 个（{len(list(ASSETS_SRC.iterdir()))} 总数）")

    log(f"完成：{moved} 篇 md → {MD_DIR}" if not args.dry_run
        else f"dry-run：{moved} 篇将写入 {MD_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
