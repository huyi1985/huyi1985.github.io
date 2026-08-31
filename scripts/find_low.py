#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
find_low.py — 检测 md.d/（或 raw_md.d/）中"可能重复的文章"与"混入的草稿"

两种可疑文章：
  1. 重复（duplicate）：同一内容/同一标题出现多次
     - 本地启发式初筛：标题归一化（去标点/空格/大小写）+ 正文相似度
       （minhashes + jaccard；无依赖，纯标准库）
     - 高置信（标题归一化相同，或正文 jaccard 极高）→ 直接标记
     - 低置信候选 → 用 OpenAI（config.d/openai.yaml 的 key）做 LLM 判定
  2. 草稿（draft）：混进内容目录的未完成稿
     - 标题/正文含 草稿/未写完/待发布/draft/TODO/占位 等标记
     - 无 date、无内容、异常短、以日期+标题但文件名带 -huyi-MacBook-home 等机器痕迹

输出：按可疑度排序的清单（含原因，重复的对会标出与谁重复）。

用法（用 config.d/openai.yaml 里的 api_key；只读，不改动任何 md）：
    python3 scripts/find_low.py                    # 扫描 md.d/
    python3 scripts/find_low.py --dir raw_md.d     # 扫别的目录
    python3 scripts/find_low.py --no-llm           # 只用本地启发式，不调 OpenAI
    python3 scripts/find_low.py --limit N          # 最多调 N 次 LLM（0=不限）
"""

import argparse
import json
import math
import re
import sys
import urllib.request
from pathlib import Path

# ── OpenAI 配置 ──────────────────────────────────────────────
# 从 config.d/openai.yaml 读取（key / model 用户已配置）。可用环境变量覆盖：
#   OPENAI_API_KEY / OPENAI_MODEL
CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.d" / "openai.yaml"


def load_openai_cfg() -> dict:
    key = cfg = None
    try:
        import yaml
        cfg = yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8")) or {}
    except Exception as e:
        print(f"  [WARN] 读取 {CONFIG_FILE} 失败：{e}（将只用本地启发式）")
    key = cfg.get("api_key") or cfg.get("old_api_key")
    model = cfg.get("model", "gpt-4o-mini")
    key = key.strip() if key else None
    # 环境变量优先
    key = __import__("os").environ.get("OPENAI_API_KEY", key)
    model = __import__("os").environ.get("OPENAI_MODEL", model)
    return {"key": key, "model": model}


def llm_judge_pair(a: dict, b: dict, cfg: dict) -> bool | None:
    """调 OpenAI 判定 a/b 是否为重复文章。返回 True/False；失败返回 None。

    判定原则：只看"是否同一篇文章"（同内容/同标题/同正文主题），
    "不同文章但相似"（如系列文、转载改标题）不算重复。
    """
    if not cfg.get("key"):
        print("  [WARN] 无 OpenAI key，跳过 LLM 判定")
        return None
    trunc = 400
    prompt = f"""你是内容审核助手。判断下面两篇中文技术文章是否属于"同一篇文章的重复"。
判定标准：标题相同或高度近似，且正文内容、主题、结构基本一致 → 重复。
不同主题、或仅是主题相近的不同文章（如同一系列的上下篇、改标题的独立文章）→ 不重复。
只回答 JSON：{{"duplicate": true/false, "reason": "一句话"}}

文章A 标题：{a['title']}
文章A 正文（前 {trunc} 字）：{a['body'][:trunc]}

文章B 标题：{b['title']}
文章B 正文（前 {trunc} 字）：{b['body'][:trunc]}"""
    body = json.dumps({
        "model": cfg["model"],
        "messages": [{"role": "user", "content": prompt}],
        "max_completion_tokens": 120,
        "response_format": {"type": "json_object"},
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {cfg['key']}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
        content = data["choices"][0]["message"]["content"]
        j = json.loads(content)
        return bool(j.get("duplicate"))
    except Exception as e:
        print(f"  [WARN] LLM 判定失败：{e}")
        return None


# ── 本地启发式：正文相似度（minhash + jaccard，无第三方依赖）──

def shingles(text: str, k: int = 4) -> set[str]:
    t = re.sub(r"\s+", " ", text)
    return {t[i:i + k] for i in range(len(t) - k + 1)} if len(t) >= k else {t}


def jaccard_approx(a: str, b: str, n: int = 128) -> float:
    """用 minhash 签名估计 jaccard（0~1）。"""
    import hashlib
    hashes = []
    for text in (a, b):
        hset = set()
        for sh in shingles(text):
            h = int(hashlib.md5(sh.encode()).hexdigest()[:8], 16) & 0xFFFFFFFF
            hset.add(h)
        hashes.append(hset)
    inter = len(hashes[0] & hashes[1])
    union = len(hashes[0] | hashes[1])
    return inter / union if union else 0.0


def normalize_title(t: str) -> str:
    t = re.sub(r"[^\w一-鿿]+", "", t.lower())
    t = re.sub(r"-\s*huyi-macbook-home\s*$", "", t)
    return t


def strip_front(txt: str) -> tuple[dict, str]:
    if not txt.startswith("---\n"):
        return {}, txt
    end = txt.find("\n---", 4)
    if end == -1:
        return {}, txt
    fm, body = txt[4:end], txt[end + 4:]
    try:
        import yaml
        d = yaml.safe_load(fm) or {}
    except Exception:
        d = {}
    return (d if isinstance(d, dict) else {}), body


# ── 草稿 / 问题标记（启发式，全本地）──

DRAFT_MARKERS = [
    "草稿", "未写完", "尚未完成", "待补充", "待发布", "占位", "TODO", "待更新",
    "draft", "wip", "placeholder", "未定稿", "初稿", "测试稿", "试验稿",
]
MACHINE_TRAIL = re.compile(r"-huyi-macbook-home\s*$", re.I)
NO_DATE_BUT_TITLE = re.compile(r"^\s*(未命名|untitled|无标题|draft|草稿)", re.I)


def draft_flags(fname: str, fm: dict, body: str) -> list[str]:
    flags = []
    title = str(fm.get("title", "")).strip()
    if MACHINE_TRAIL.search(fname) or MACHINE_TRAIL.search(title):
        flags.append("文件名/标题带机器痕迹 -huyi-MacBook-home")
    if not fm.get("date"):
        flags.append("无 date（frontmatter 缺日期）")
    if title and (title in ("未命名", "untitled") or NO_DATE_BUT_TITLE.match(title)):
        flags.append("标题像占位/未命名")
    body_text = re.sub(r"\s+", " ", body).strip()
    if len(body_text) == 0:
        flags.append("正文为空（纯 frontmatter 空壳）")
    elif len(body_text) < 30:
        flags.append(f"正文过短（{len(body_text)} 字）")
    # 参考/链接整理稿：标题像 "Ref" 或无正文叙述、内容多为链接/标签 → 不是正经文章
    if re.match(r"^\s*(ref|reference|参考|链接|收藏|bookmarks?)\s*$", title, re.I):
        flags.append("标题为 Ref/参考 等整理类标记")
    # 正文以多个链接/标签开头（无叙述），且标题又短 → 疑似链接收藏稿
    heads = [l.strip() for l in body.strip().splitlines()[:3] if l.strip()]
    linky = sum(1 for l in heads[:3] if l.startswith(("http", "#", "!", "[")) or re.match(r"^https?://", l))
    if len(heads) >= 2 and linky >= 2 and len(title) <= 12:
        flags.append(f"正文开头多为链接/标签（{linky}/{len(heads[:3])}），疑似收藏/整理稿")
    low = (title + " " + body_text[:800]).lower()
    for marker in DRAFT_MARKERS:
        if marker.lower() in low:
            flags.append(f"含草稿标记“{marker}”")
            break
    return flags


# ── 主流程 ──────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="检测 md.d/ 里的重复文章与混入草稿")
    ap.add_argument("--dir", default="md.d", help="扫描目录（默认 md.d/）")
    ap.add_argument("--no-llm", action="store_true", help="只用本地启发式，不调 OpenAI")
    ap.add_argument("--limit", type=int, default=0,
                    help="最多调 N 次 LLM 判定（0=不限）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    base = Path(args.dir)
    if not base.is_dir():
        print(f"[ERROR] 目录不存在：{base}")
        return 1

    cfg = load_openai_cfg() if not args.no_llm else {"key": None, "model": None}
    if not cfg.get("key"):
        print("  [WARN] 未配置/未找到 OpenAI key → 仅本地启发式")
    print(f"模型：{cfg.get('model')}")

    # 读入全部文章
    arts = []
    for f in sorted(base.glob("*.md")):
        txt = f.read_text(encoding="utf-8", errors="replace")
        fm, body = strip_front(txt)
        body_clean = re.sub(r"\s+", " ", body).strip()
        arts.append({
            "file": f.name, "title": str(fm.get("title", "")).strip(),
            "date": str(fm.get("date", "")).strip(), "body": body_clean,
            "len": len(body_clean), "fm": fm,
        })
    print(f"共 {len(arts)} 篇文章")

    # ── A. 草稿 / 问题文章 ──
    drafts = []
    for a in arts:
        fl = draft_flags(a["file"], a["fm"], a["body"])
        if fl:
            drafts.append({**a, "flags": fl})

    # ── B. 重复候选（本地启发式）──
    # 先用标题归一化分组（同标题必查），再用正文 jaccard 找"标题不同但内容相同"
    by_t = {}
    for a in arts:
        by_t.setdefault(normalize_title(a["title"]), []).append(a)

    dup_by_title = []
    for t, group in by_t.items():
        if not t or len(group) < 2:
            continue
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                dup_by_title.append((group[i], group[j], "标题归一化相同"))

    # 标题组里的对也给出相似度（供展示），并标记"标题相同"
    title_pairs = [(a, b, jaccard_approx(a["body"], b["body"]), tag)
                   for a, b, tag in dup_by_title]
    titled_keys = {frozenset((a["file"], b["file"])) for a, b, _, _ in title_pairs}

    # 正文相似：对不在标题组的剩余两两做 jaccard（O(n²)，n=140 可接受）
    # 空壳文章（无正文）不参与正文相似判定——空 vs 空 不算"重复"
    body_cand = []
    nonempty = [a for a in arts if a["len"] > 0]
    for i in range(len(nonempty)):
        for j in range(i + 1, len(nonempty)):
            a, b = nonempty[i], nonempty[j]
            key = frozenset((a["file"], b["file"]))
            if key in titled_keys:
                continue
            jac = jaccard_approx(a["body"], b["body"])
            if jac >= 0.60:
                body_cand.append((a, b, jac))
    # 只保留高置信正文重复（≥0.85），0.6~0.85 交给 LLM
    body_cand = [c for c in body_cand if c[2] >= 0.85]

    # ── C. LLM 复核低置信候选 ──
    llm_res = {}
    # 需要 LLM 的候选，全部来自上面已算出的对（jaccard 已给出）
    needs_llm = []
    for a, b, jac, tag in title_pairs:
        if jac < 0.6:
            needs_llm.append((a, b))
    for a, b, jac in body_cand:
        if jac < 0.85:
            needs_llm.append((a, b))
    llm_calls = 0
    for a, b in needs_llm:
        if args.limit and llm_calls >= args.limit:
            break
        print(f"  [LLM] 判定是否重复：{a['file']} ⟷ {b['file']}")
        res = llm_judge_pair(a, b, cfg)
        if res is not None:
            llm_res[frozenset((a["file"], b["file"]))] = res
            llm_calls += 1

    # ── 汇总输出 ──
    findings = []  # (severity, kind, articleA, articleB, reason)
    for a, b, jac, tag in title_pairs:
        key = frozenset((a["file"], b["file"]))
        judged = llm_res.get(key)
        if judged is False:
            continue  # LLM 明确说不重复
        sev = "HIGH" if (jac >= 0.6 or judged is True) else "MED"
        findings.append((sev, "重复(标题相同)", a, b,
                         f"jaccard={jac:.2f} {tag}"
                         + ("，LLM 判定重复" if judged else (
                             "，LLM 判定不重复" if judged is False else ""))))
    for a, b, jac in body_cand:
        key = frozenset((a["file"], b["file"]))
        judged = llm_res.get(key)
        sev = "MED" if jac < 0.85 else "HIGH"
        if judged is False:
            continue
        findings.append((sev, "重复(正文相似)", a, b,
                         f"jaccard={jac:.2f}"
                         + ("，LLM 判定重复" if judged else "")))
    for d in drafts:
        findings.append(("MED-HIGH" if "过短" in d["flags"] else "LOW",
                         "草稿/问题", d, None,
                         "；".join(d["flags"])))

    order = {"HIGH": 0, "MED-HIGH": 1, "MED": 2, "LOW": 3}
    findings.sort(key=lambda x: order.get(x[0], 4))

    if args.json:
        out = []
        for sev, kind, a, b, reason in findings:
            out.append({
                "severity": sev, "kind": kind, "reason": reason,
                "a": {"file": a["file"], "title": a["title"], "date": a["date"]},
                "b": {"file": b["file"], "title": b["title"], "date": b["date"]} if b else None,
            })
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        if not findings:
            print("未发现可疑文章 ✓")
            return 0
        print(f"\n发现 {len(findings)} 条可疑：\n")
        for sev, kind, a, b, reason in findings:
            line = f"[{sev}] {kind}"
            if b:
                line += f"\n    A  {a['date']}  {a['title']}  ({a['file']})"
                line += f"\n    B  {b['date']}  {b['title']}  ({b['file']})"
            else:
                line += f"\n    {a['date']}  {a['title']}  ({a['file']})"
            line += f"\n    → {reason}"
            print(line + "\n")
    print(f"\nLLM 调用次数：{llm_calls}   （重复对 {len([x for x in findings if '重复' in x[1]])}，"
          f"草稿/问题 {len([x for x in findings if '草稿' in x[1]])}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
