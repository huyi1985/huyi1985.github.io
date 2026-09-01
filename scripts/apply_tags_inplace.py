#!/usr/bin/env python3
"""就地给 md.d/posts/*/index.md 补 tags（关键词打 tag）。

为何就地、不全量重建：全量 build_md_d.py 会清空 posts/ 再从 raw_md.d 重建，
此时若图片池（md.d/assets/）不存在会丢全部图。本脚本只改 index.md 的 frontmatter，
正文与图片原样不动，安全。

复用 build_md_d.py 的 parse_front / dump_front / load_keywords / match_keywords，
保证匹配逻辑与 build 完全一致。

用法：
    python3.11 scripts/apply_tags_inplace.py            # 实写
    python3.11 scripts/apply_tags_inplace.py --dry-run  # 预演，只报告不改文件
"""
import argparse
import sys
from pathlib import Path

# 复用 build_md_d.py 的函数
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_md_d as bmd  # noqa: E402

POSTS_DIR = bmd.BASE / "md.d" / "posts"


def main() -> int:
    ap = argparse.ArgumentParser(description="就地补 tags")
    ap.add_argument("--dry-run", action="store_true", help="只报告，不写文件")
    args = ap.parse_args()

    keywords = bmd.load_keywords()
    if not keywords:
        print("⚠ 关键词词典为空（config.d/keywords.yaml 缺失或无 keywords 字段），退出。")
        return 1
    print(f"关键词词典：{len(keywords)} 个")

    if not POSTS_DIR.is_dir():
        print(f"⚠ {POSTS_DIR} 不存在，退出。")
        return 1

    bundles = sorted(d for d in POSTS_DIR.iterdir() if d.is_dir())
    tagged = 0
    skipped_has_tags = 0
    skipped_no_match = 0
    total_tags = 0
    for bundle in bundles:
        idx = bundle / "index.md"
        if not idx.is_file():
            continue
        content = idx.read_text(encoding="utf-8", errors="replace")
        fm, body = bmd.parse_front(content)
        if fm.get("tags"):
            # 已有 tags，不覆盖
            skipped_has_tags += 1
            continue
        matched = bmd.match_keywords(body, keywords)
        if not matched:
            skipped_no_match += 1
            if args.dry_run:
                print(f"  [SKIP] {bundle.name}  (无命中)")
            continue
        fm["tags"] = matched
        new_content = bmd.dump_front(fm) + body.lstrip("\n")
        tag_count = len(matched)
        if args.dry_run:
            print(f"  [PLAN] {bundle.name}  +tags[{tag_count}] = {matched}")
        else:
            idx.write_text(new_content, encoding="utf-8")
            print(f"  [ OK ] {bundle.name}  +tags[{tag_count}]")
        tagged += 1
        total_tags += tag_count

    mode = "dry-run" if args.dry_run else "完成"
    print(
        f"\n{mode}：{len(bundles)} 个 bundle，"
        f"打 tag {tagged} 篇（共 {total_tags} 个 tag），"
        f"已有 tags 跳过 {skipped_has_tags}，无命中跳过 {skipped_no_match}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
