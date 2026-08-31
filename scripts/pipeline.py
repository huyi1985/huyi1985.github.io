#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pipeline.py — 一键流水线：tmp/ → raw_md.d/ → md.d/ → hugo → public/ → git push

把三个阶段脚本 + Hugo 构建 + 发布串成一条命令：
  ① collect_posts.py    提取 tmp/ 文章 → raw_md.d/（幂等，已存在则跳过）
  ② download_images.py  图床图本地化 → md.d/assets/，转 WebP，改写引用
  ③ build_md_d.py       raw_md.d → md.d/（frontmatter 规整 + 黑名单 draft）
  ④ hugo --minify        构建 public/
  ⑤ git commit + push   发布到 GitHub Pages（push main 触发 Actions）

默认运行【增量】：只处理 tmp/ 里"新出现的文章"（raw_md.d 目标已存在则跳过），
已发布的文章不动；适合日常加一篇就发布一篇。
--full 则【全量】：强制重新提取/重下/重建，全部文章重出一遍后再发布。
--limit N 则【窗口】：只跑最后 N 篇文章（download 与 build 均传 --limit；
  窗口外 md 在 build 里保持现状/git HEAD），并自动跳过 git push（仅构建预览）。

行为契约：
  1. 只调用 scripts/ 现有脚本与 hugo/git，不复制它们的逻辑
  2. 默认增量：collect_posts 不带 --force；--full 传 --force 且 hugo 前清 public/
  3. --skip-push：构建但不提交/不推送（本地预览用）
  4. --dry-run：只打印将执行的命令，不运行、不 push
  5. 失败即停（返回码非 0 中止），每阶段打印标记便于定位
  6. push 前 git add -A；提交信息含日期与本次新增文章数
  7. 一律用 Path 拼接命令数组（subprocess 列表形式），不用裸 shell glob
     ——tmp/ 目录名含空格（如 "已发布/20260102 看《疯狂动物城2》…"），必须避免字符串拼接

用法：
    python3.11 scripts/pipeline.py                 # 增量：处理新增文章并发布
    python3.11 scripts/pipeline.py --full          # 全量：全部重出并发布
    python3.11 scripts/pipeline.py --limit 5       # 只处理最后 5 篇文章（不 push）
    python3.11 scripts/pipeline.py --skip-push     # 只构建，不提交不推送
    python3.11 scripts/pipeline.py --dry-run       # 预览将执行的命令
    python3.11 scripts/pipeline.py --full --skip-push --dry-run
"""

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SCRIPTS = BASE / "scripts"
PY = sys.executable  # 用当前解释器（调用方以 python3.11 运行）
HUGO = None  # 在 main() 里探测

# 各阶段子命令（列表形式，无 shell）
STAGES = {
    "collect": [PY, str(SCRIPTS / "collect_posts.py")],
    "images": [PY, str(SCRIPTS / "download_images.py")],
    "build": [PY, str(SCRIPTS / "build_md_d.py")],
}


def log(msg: str) -> None:
    print(f"[pipeline] {msg}", flush=True)


def run(cmd: list[str], dry_run: bool) -> int:
    """执行命令；dry_run 时只打印。返回退出码。"""
    shown = " ".join(f'"{c}"' if " " in c else c for c in cmd)
    log(f"$ {shown}")
    if dry_run:
        return 0
    r = subprocess.run(cmd)
    if r.returncode != 0:
        log(f"✗ 命令失败（exit {r.returncode}）：{shown}")
    return r.returncode


def detect_hugo() -> tuple[bool, str]:
    """探测 hugo 可执行文件；返回 (是否存在, 命令)。"""
    import shutil
    exe = shutil.which("hugo")
    return (exe is not None, exe or "hugo")


def count_new(collect_out: str) -> int:
    """从 collect_posts 输出统计新增文章数（[COPY md  ] 行数）。"""
    return sum(1 for line in collect_out.splitlines() if "[COPY md" in line)


def main() -> int:
    global HUGO
    ap = argparse.ArgumentParser(
        description="一键流水线：tmp→raw_md.d→md.d→hugo→git push（默认增量，--full 全量）"
    )
    ap.add_argument("--full", action="store_true",
                    help="全量：collect 带 --force，hugo 前清 public/")
    ap.add_argument("--limit", type=int, default=0, metavar="N",
                    help="只处理最后 N 篇文章（不 push，仅构建预览）")
    ap.add_argument("--skip-push", action="store_true",
                    help="只构建，不 git commit / push")
    ap.add_argument("--dry-run", action="store_true",
                    help="只打印命令，不执行不 push")
    args = ap.parse_args()

    if args.full and args.limit:
        log("✗ --full 与 --limit 互斥（全量=全部，窗口=部分），请二选一")
        return 2

    HUGO_OK, HUGO = detect_hugo()
    if not HUGO_OK:
        log("✗ 未找到 hugo（PATH 里没有）；请先安装或加入 PATH")
        return 1

    mode = "全量" if args.full else ("窗口" if args.limit else "增量")
    log(f"模式：{mode}" + (f"（limit={args.limit}）" if args.limit else "")
        + f" | skip-push={args.skip_push} | dry-run={args.dry_run}")

    # ── 阶段① 提取 ──
    cmd = list(STAGES["collect"])
    if args.full:
        cmd.append("--force")
    log("$ " + " ".join(f'"{c}"' if " " in c else c for c in cmd))
    if args.dry_run:
        new_n = 0
    else:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            log(f"✗ 阶段① collect_posts 失败（exit {r.returncode}）")
            print(r.stderr[-2000:] if r.stderr else r.stdout[-2000:])
            return r.returncode
        new_n = count_new(r.stdout)

    # ── 阶段② 图片本地化（--limit 传给 download_images）──
    cmd = list(STAGES["images"])
    if args.full:
        cmd.append("--force")
    if args.limit:
        cmd += ["--limit", str(args.limit)]
    rc = run(cmd, args.dry_run)
    if rc:
        return rc

    # ── 阶段③ 构建 md.d（--limit 传给 build_md_d）──
    cmd = list(STAGES["build"])
    if args.limit:
        cmd += ["--limit", str(args.limit)]
    rc = run(cmd, args.dry_run)
    if rc:
        return rc

    # ── 阶段④ Hugo 构建 ──
    if args.full:
        import shutil
        public = BASE / "public"
        if public.is_dir():
            shutil.rmtree(public)
    rc = run([HUGO, "--minify"], args.dry_run)
    if rc:
        return rc

    # ── 阶段⑤ 提交 + 推送 ──
    if args.limit or args.skip_push or args.dry_run:
        log("limit / skip-push / dry-run：不提交不推送；构建完成 ✓")
        return 0

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    msg = f"pipeline: {today} {mode}发布 {new_n} 篇文章" if new_n else (
        f"pipeline: {today} {mode}发布（无新增文章，构建/模板更新）"
    )
    for cmd in (["git", "add", "-A"],
                ["git", "commit", "-m", f"{msg}\n\nCo-Authored-By: Claude Code <noreply@anthropic.com>"],
                ["git", "push", "origin", "main"]):
        rc = run(cmd, False)
        if rc:
            log(f"✗ git 阶段失败：{' '.join(cmd[:2])}（exit {rc}）")
            return rc
    log("✓ 已推送 main，GitHub Actions 将自动部署")
    return 0


if __name__ == "__main__":
    sys.exit(main())
