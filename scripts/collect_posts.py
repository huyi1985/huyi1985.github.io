#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
collect_posts.py — 流水线第 1 阶段：从源目录"提取"文章 md → raw_md.d/

流水线设计（用户已确认）：
  1) [本脚本] collect_posts.py
       从源目录递归提取文章 md：只收 md，不收目录结构、不收图片
       → 输出到 raw_md.d/（扁平，一篇文章一个 md）
  2) [未来脚本] 解析 raw_md.d 里 md 的图床引用（![..](https://...)），
       下载图片到本地并改写引用
  3) [未来脚本] 生成 Hugo 可消费的 md.d/（规范 slug、frontmatter、图片路径）

  所以本脚本只负责"提取"，raw_md.d 是中间产物，不直接喂给 Hugo。

行为契约：
  1. 只 COPY/读取源，绝不 write 回源目录（纯读源）
  2. 目录列表驱动：只处理 SOURCE_DIRS 里列出的源目录
  3. 递归提取：源目录下（含子目录）的每个 md 都视为候选文章
  4. 排除清单 + 隐藏/备份目录 不提取
  5. 输出 raw_md.d/<date>-<title>.md，扁平，不建子目录
  6. 幂等：目标 md 已存在则跳过；--force 强制覆盖

用法：
    python3 scripts/collect_posts.py                 # 提取（目标已存在则跳过）
    python3 scripts/collect_posts.py --force         # 强制覆盖已存在的目标
    python3 scripts/collect_posts.py --dry-run       # 只预览将做什么
"""

import argparse
import json
import re
import sys
from functools import lru_cache
from datetime import datetime, timezone
from pathlib import Path

# ── 可配置清单 ──────────────────────────────────────────────
# 源目录（绝对路径，避免 cwd 歧义）。每个目录会被递归扫描。
SOURCE_DIRS = [
    Path(__file__).resolve().parent.parent / "tmp",
]

# 目标根目录：raw_md.d/（纯 md 提取物，中间产物）
TARGET_DIR = Path(__file__).resolve().parent.parent / "raw_md.d"

# 跳过这些（任意级别的）目录名：备份/临时/工具目录，里面的 md 不是文章。
SKIP_DIRS = {
    "_bak",
    "scripts",
    "output",
    "docs",      # 若某源把说明文档也收进去可能误伤，可按源调整
}

# 明确排除的 md（按文件名去扩展名匹配）：README/报告/研究索引等
EXCLUDED_FILENAMES = {
    
}

@lru_cache(maxsize=1)
def get_yaml() -> object:
    """延迟导入 yaml（PyYAML）库；缺则提示安装。

    用于 frontmatter 的 YAML 转义（标题可能含引号/换行，如
    '从 "BUGS none possible" 到 systemd'，手工拼字符串会破坏解析）。
    Hugo 的 frontmatter 默认按 YAML（key: value）解析，
    '=' 形式的 TOML frontmatter 在新版 Hugo 中默认不识别。
    """
    try:
        import yaml
    except ImportError:
        sys.exit(
            "缺少 PyYAML 库，请先安装：python3.11 -m pip install pyyaml\n"
            "（用于 frontmatter 的 YAML 转义，避免标题含引号等字符破坏解析）"
        )
    return yaml


def log(msg: str) -> None:
    print(msg, flush=True)


def infer_date(path: Path) -> str:
    """用文件 mtime 作为默认发布日（用户已确认），返回 YYYY-MM-DD。"""
    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return mtime.strftime("%Y-%m-%d")


def make_frontmatter(
    title: str, date_str: str, src_abs: str
) -> str:
    """生成 YAML frontmatter。

    用 PyYAML 序列化，保证标题/路径里的引号、换行等字符被正确转义
    （Hugo 解析 YAML frontmatter 时会正确还原）。source 便于溯源/回写，
    站点侧可忽略。
    """
    fm = {
        "title": title,
        "date": date_str,
        "source": src_abs,
    }
    body = get_yaml().safe_dump(
        fm, allow_unicode=True, sort_keys=False, default_flow_style=False
    )
    return "---\n" + body + "---\n\n"


def sanitize_filename(text: str) -> str:
    """把标题/任意文本变成文件系统安全的文件名。

    保留中文与字母数字、`-`、`_`、`.`；把其余字符（空格、冒号、引号、斜杠等）
    统一替换成 `-`。连续替换符合并为一个，两端去除，避免文件名以奇怪字符开头/结尾。
    """
    out = re.sub(r'[^\w一-鿿.-]+', '-', text.strip(), flags=re.UNICODE)
    out = re.sub(r'-{2,}', '-', out).strip('-')
    return out


def collect_from_dir(src: Path, dry_run: bool, force: bool = False) -> list[dict]:
    """从源目录递归提取文章 md → raw_md.d/（扁平，一篇文章一个 md）。

    force=True 时覆盖已存在的目标文件；否则目标已存在则跳过（纯 COPY 语义）。
    图片：不在此阶段处理（后续脚本从图床下载）。
    """
    if not dry_run:
        TARGET_DIR.mkdir(parents=True, exist_ok=True)  # 目标目录只建一次，移到循环外
    out: list[dict] = []
    for md in sorted(src.rglob("*.md")):
        # 跳过隐藏目录 / 备份与工具目录（任意层级命中即排除）
        rel_parts = md.relative_to(src).parts[:-1]
        if any(p.startswith(".") or p in SKIP_DIRS for p in rel_parts):
            log(f"  [SKIP md ] {md.relative_to(src)} (目录被排除)")
            continue
        stem = md.stem
        if stem in EXCLUDED_FILENAMES:
            log(f"  [SKIP md ] {stem} (排除清单)")
            continue

        title = infer_title(md)
        date_str = infer_date(md)

        # 文件名 = date + '-' + 标题（标题做文件系统安全化）；不用 aliases
        fname = sanitize_filename(f"{date_str}-{title}")
        dest_md = TARGET_DIR / f"{fname}.md"  # 扁平：raw_md.d/<date>-<title>.md
        entry = {
            "src_md": str(md),
            "title": title,
            "date": date_str,
            "dest_md": str(dest_md.relative_to(TARGET_DIR)),
        }
        out.append(entry)

        if dry_run:
            log(f"  [PLAN md ] {md.relative_to(src)} → {dest_md.relative_to(TARGET_DIR)}")
            continue

        # 幂等式复制：目标已存在则跳过，只有 --force 才覆盖。
        # （纯 COPY 工具不做内容比对——"存在即视为最新"，绝不隐式改写已发布的产物。）
        if dest_md.exists() and not force:
            log(f"  [SKIP md   ] {stem} (目标已存在，--force 可覆盖)")
            continue

        dest_md.write_text(
            make_frontmatter(title, date_str, str(md))
            + md.read_text(encoding="utf-8", errors="replace"),
            encoding="utf-8",
        )
        log(f"  [COPY md   ] {fname} " + ("(force)" if force and dest_md.exists() else ""))
    return out


def infer_title(md: Path) -> str:
    """从 md 首个 '#' 标题推断文章名，无标题则用文件名。"""
    try:
        for line in md.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
    except OSError:
        pass
    return md.stem


def write_manifest(entries: list[dict], path: Path, dry_run: bool) -> None:
    """写入 manifest.json：供后续脚本消费的提取清单。"""
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "stage": "raw_md.d",
        "source_dirs": [str(s) for s in SOURCE_DIRS],
        "articles": entries,
    }
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    log(f"  [WRITE    ] {path.relative_to(TARGET_DIR)} ({len(entries)} 篇)")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="提取源目录里的文章 md 到 raw_md.d/（纯 md，不含目录结构/图片）"
    )
    parser.add_argument("--force", "-f", action="store_true",
                        help="强制覆盖已存在的目标文件（默认：目标已存在则跳过）")
    parser.add_argument("--dry-run", action="store_true", help="只预览，不写入")
    args = parser.parse_args()

    all_entries: list[dict] = []
    for src in SOURCE_DIRS:
        src_path = Path(src)
        if not src_path.is_dir():
            log(f"  [ERROR    ] 源目录不存在: {src}")
            continue
        log(f"== 处理源目录: {src}")
        all_entries.extend(
            collect_from_dir(src_path, args.dry_run, force=args.force)
        )

    if args.dry_run:
        for e in all_entries:
            log(f"  [PLAN     ] {e['title']} | {e['date']}")
        log("dry-run 完成（未写入任何文件）")
    else:
        all_entries.sort(key=lambda e: e["date"], reverse=True)
        write_manifest(all_entries, TARGET_DIR / "manifest.json", dry_run=False)
        log("完成：源目录未改动，raw_md.d/ 已就绪（仅 md；图片待后续脚本从图床下载）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
