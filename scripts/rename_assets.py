#!/usr/bin/env python3
"""
Rename image assets in md.d/assets/ and update references in md.d/*.md files.

Naming rule: {YYYY-mm-dd}-{article_idx}-{image_idx}.{ext}
"""

import os
import re
from pathlib import Path
from collections import defaultdict

MD_DIR = Path("/Users/huyi/Projects/_niuniu_yiyi/md.d")
ASSETS_DIR = MD_DIR / "assets"

DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")
IMG_RE = re.compile(r"!\[([^\]]*)\]\((/assets/[^)]+)\)")


def main():
    # 0. 先扫描所有 md，统计每个引用的 basename 出现次数
    #    —— 跨文章共享 / 一文内重复引用的图片，保持原文件名，不参与重命名，
    #    （避免单映射覆盖导致引用断裂；共享图通常无后缀规律，原名即可辨识）
    md_files = sorted(MD_DIR.glob("*.md"))
    ref_count = defaultdict(int)
    for md_path in md_files:
        content = md_path.read_text(encoding="utf-8")
        for match in IMG_RE.finditer(content):
            ref_count[os.path.basename(match.group(2))] += 1

    # 1. Collect all md files and group by date
    date_groups = defaultdict(list)

    for md_path in md_files:
        m = DATE_RE.match(md_path.name)
        if m:
            date_groups[m.group(1)].append(md_path)
        else:
            print(f"SKIP (no date): {md_path.name}")

    # 2. For each article, find image references and build rename mappings
    rename_map = {}       # { old_basename: new_basename }
    updates = {}          # { md_path: [(old_ref, new_ref), ...] }

    total_articles = 0
    total_images = 0
    skipped = 0

    for date_str in sorted(date_groups):
        articles = date_groups[date_str]
        for article_idx, md_path in enumerate(articles, 1):
            total_articles += 1
            content = md_path.read_text(encoding="utf-8")

            img_matches = list(IMG_RE.finditer(content))
            if not img_matches:
                continue

            # Track images seen in this article: old_basename -> new_basename
            article_seen = {}
            # Image index only increments for new (non-duplicate) images
            article_img_idx = 0

            md_updates = []
            for match in img_matches:
                asset_path = match.group(2)
                asset_basename = os.path.basename(asset_path)
                ext = os.path.splitext(asset_basename)[1]

                # 共享/重复引用的图 → 保持原名，不重命名
                if ref_count[asset_basename] > 1:
                    if asset_basename not in article_seen:
                        print(f"KEEP (shared ref x{ref_count[asset_basename]}): {asset_basename}")
                    article_seen[asset_basename] = asset_basename
                elif asset_basename not in article_seen:
                    article_img_idx += 1
                    new_name = f"{date_str}-{article_idx}-{article_img_idx}{ext}"

                    src = ASSETS_DIR / asset_basename
                    if not src.exists():
                        print(f"SKIP (no asset): {asset_basename} in {md_path.name}")
                        skipped += 1
                        continue

                    dst = ASSETS_DIR / new_name
                    if dst.exists() and dst != src:
                        print(f"SKIP (conflict): {new_name} already exists, skipping {asset_basename}")
                        skipped += 1
                        continue

                    rename_map[asset_basename] = new_name
                    article_seen[asset_basename] = new_name
                    total_images += 1

                new_ref = f"/assets/{article_seen[asset_basename]}"
                md_updates.append((asset_path, new_ref))

            if md_updates:
                updates[md_path] = md_updates

    # 3. Perform all renames
    for old_name, new_name in rename_map.items():
        src = ASSETS_DIR / old_name
        dst = ASSETS_DIR / new_name
        src.rename(dst)

    # 4. Update md file references
    for md_path, replacements in updates.items():
        content = md_path.read_text(encoding="utf-8")
        for old_ref, new_ref in replacements:
            content = content.replace(old_ref, new_ref)
        md_path.write_text(content, encoding="utf-8")

    # 5. Summary
    print(f"\n{'='*50}")
    print(f"Summary:")
    print(f"  Total articles processed: {total_articles}")
    print(f"  Total images renamed: {total_images}")
    print(f"  Skipped: {skipped}")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
