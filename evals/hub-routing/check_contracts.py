#!/usr/bin/env python3
"""Mechanical grader for hub-routing eval fixtures.

Screens each fixture against its case's expectations in cases.json:
primary-skill hit, no forbidden skill chosen as primary, required output-
contract sections present, composition shape (when applicable). Stop-marker
presence is only a WARNING — final judgment on whether the executor stayed in
the router's lane is human (see rubric.md).

Usage:
    python3 evals/hub-routing/check_contracts.py            # grade all fixtures
    python3 evals/hub-routing/check_contracts.py --json     # machine output
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CASES_FILE = os.path.join(HERE, "cases.json")
FIXTURES_DIR = os.path.join(HERE, "fixtures")

PRIMARY_LINE_RE = re.compile(r"推荐|主 ?[Ss]kill|主[：=]|入口|编排结论|调用|进入|使用")
# Stricter shape for forbidding a designation: weak verbs like 进入/调用 appear in
# fallback branches ("没结果切到 x", "提到 x 属冗余") and must not count.
FORBIDDEN_LINE_RE = re.compile(r"推荐|主 ?[Ss]kill|主[：=]|入口[：=]|选定|首选")
STOP_RE = re.compile(r"编排到此|本轮不代替|等你调用|到此结束|准备好就|开始分析即可|立即停止")
SECTIONS = [
    ("更像/判断", r"更像|当前判断|判读|当前 read|current read|这题大概率|大概率是|标准形状"),
    ("为什么", r"为什么|why this"),
    ("下一步", r"先做|下一步|next 1-3"),
    ("每步解释", r"每步|what each step"),
    ("没结果分支", r"没结果|切到|if it fails|怎么办"),
    ("术语解释", r"术语|glossary"),
]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def primary_hits(lines, skill_stem):
    """Lines that look like a primary-skill designation naming this skill."""
    hits = []
    for line in lines:
        if PRIMARY_LINE_RE.search(line) and skill_stem in line:
            hits.append(line.strip()[:120])
    return hits


def forbidden_hits(lines, skill_stem):
    """Designation-shaped lines naming a forbidden skill (fallback branches excluded)."""
    return [line.strip()[:120] for line in lines
            if FORBIDDEN_LINE_RE.search(line) and skill_stem in line]


def grade_case(case, reply):
    problems, warnings, evidence = [], [], []

    # 1. Primary skill must be designated from the expected set.
    primary_evidence = []
    for cand in case["expect"]["primary_any_of"]:
        primary_evidence += primary_hits(reply.splitlines(), cand)
    if primary_evidence:
        evidence.append(f"primary: {primary_evidence[0]}")
    else:
        problems.append(f"no primary designation found for {case['expect']['primary_any_of']}")

    # 2. Forbidden skills must not be designated as primary.
    for forb in case["expect"].get("forbidden_primary", []):
        if forbidden_hits(reply.splitlines(), forb):
            problems.append(f"forbidden skill designated as primary: {forb}")

    # 3. Composition shape.
    comp = case["expect"].get("composition")
    if comp:
        if not primary_hits(reply.splitlines(), comp["main"]):
            problems.append(f"composition main `{comp['main']}` not designated")
        for group in comp.get("aux_any_of", []):
            if not any(cand in reply for cand in group):
                problems.append(f"composition missing aux from {group}")

    # 4. Output-contract sections.
    low = reply.lower()
    missing = [label for label, pat in SECTIONS if not re.search(pat, low)]
    if missing:
        problems.append(f"output contract sections missing: {', '.join(missing)}")

    # 5. Stop marker (warning only — human confirms no downstream execution).
    if not STOP_RE.search(reply):
        warnings.append("no explicit stop marker; confirm the reply did not execute downstream work")

    return problems, warnings, evidence


def main():
    cases = {c["id"]: c for c in json.load(open(CASES_FILE, encoding="utf-8"))["cases"]}
    fixtures = sorted(f for f in os.listdir(FIXTURES_DIR) if f.endswith(".md"))
    if not fixtures:
        print("no fixtures found; run a blinded executor per executor-prompt.md first")
        return 1

    as_json = "--json" in sys.argv
    failures = 0
    report = []
    for fx in fixtures:
        case_id = os.path.splitext(fx)[0]
        if case_id not in cases:
            print(f"? {case_id}: no matching case in cases.json")
            continue
        problems, warnings, evidence = grade_case(cases[case_id], load(os.path.join(FIXTURES_DIR, fx)))
        failures += bool(problems)
        report.append({"case": case_id, "status": "FAIL" if problems else "PASS",
                       "problems": problems, "warnings": warnings, "evidence": evidence})
        if not as_json:
            mark = "✗" if problems else "✓"
            print(f"{mark} {case_id} — {cases[case_id]['title']}")
            for p in problems:
                print(f"    FAIL: {p}")
            for w in warnings:
                print(f"    warn: {w}")

    if as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"\n{len(report)} graded, {failures} failed (mechanical screen only; "
              "human-review stop behaviour per rubric.md)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
