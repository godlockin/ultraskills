#!/usr/bin/env python3
"""
hub 搜索准确率回归测试.

跑 ground_truth.json 里的 30 条查询,记录:
  - top1 命中率 (`must_top1` 项)
  - top3 覆盖率 (`expected_top` 至少有一个在 top3)
  - 未命中/命中详情

用法:
    python3 devops/ultraskills-hub/tests/regression.py                # 全跑
    python3 devops/ultraskills-hub/tests/regression.py --verbose      # 逐条打印
    python3 devops/ultraskills-hub/tests/regression.py --save NAME    # 保存快照,后续可对比
    python3 devops/ultraskills-hub/tests/regression.py --diff A B     # 对比两次快照

输出退出码:
    0 = 全部通过(top3 覆盖率 100%)
    1 = 有降级
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GT_FILE = Path(__file__).parent / "ground_truth.json"
SEARCH = ROOT / "devops" / "ultraskills-hub" / "scripts" / "search.py"
SNAPSHOTS = Path(__file__).parent / "snapshots"


def run_search(query: str) -> list[dict]:
    out = subprocess.run(
        ["python3", str(SEARCH), query],
        capture_output=True, text=True, cwd=str(ROOT),
    )
    if out.returncode != 0:
        return []
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        return []


def evaluate(cases: list[dict]) -> dict:
    total = len(cases)
    top1_target = 0
    top1_hit = 0
    top3_hit = 0
    details: list[dict] = []

    for case in cases:
        q = case["query"]
        expected = set(case["expected_top"])
        must_top1 = case.get("must_top1")
        results = run_search(q)
        top_ids = [r["id"] for r in results[:3]]

        top3_ok = bool(expected & set(top_ids))
        if top3_ok:
            top3_hit += 1

        top1_ok = None
        if must_top1:
            top1_target += 1
            top1_ok = top_ids and top_ids[0] == must_top1
            if top1_ok:
                top1_hit += 1

        details.append({
            "query": q,
            "expected": list(expected),
            "must_top1": must_top1,
            "top_ids": top_ids,
            "top1_ok": top1_ok,
            "top3_ok": top3_ok,
        })

    return {
        "total": total,
        "top1_target": top1_target,
        "top1_hit": top1_hit,
        "top1_rate": top1_hit / top1_target if top1_target else 0.0,
        "top3_hit": top3_hit,
        "top3_rate": top3_hit / total,
        "details": details,
    }


def print_report(result: dict, verbose: bool = False) -> None:
    r = result
    print(f"total cases:       {r['total']}")
    print(f"top1 (strict):     {r['top1_hit']}/{r['top1_target']}  ({r['top1_rate']*100:.1f}%)")
    print(f"top3 (any hit):    {r['top3_hit']}/{r['total']}  ({r['top3_rate']*100:.1f}%)")

    if verbose:
        print()
        for d in r["details"]:
            mark = "✅" if d["top3_ok"] else "❌"
            top1_note = ""
            if d["must_top1"] is not None:
                top1_note = " top1✓" if d["top1_ok"] else f" top1✗(want:{d['must_top1']})"
            print(f"  {mark} [{d['query']}]{top1_note}")
            print(f"     top3: {d['top_ids']}")
            print(f"     expected: {d['expected']}")


def save_snapshot(result: dict, name: str) -> Path:
    SNAPSHOTS.mkdir(exist_ok=True)
    p = SNAPSHOTS / f"{name}.json"
    p.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    return p


def diff_snapshots(a_name: str, b_name: str) -> None:
    a = json.loads((SNAPSHOTS / f"{a_name}.json").read_text())
    b = json.loads((SNAPSHOTS / f"{b_name}.json").read_text())
    print(f"=== 对比: {a_name} → {b_name} ===")
    print(f"top1: {a['top1_hit']}/{a['top1_target']}  →  {b['top1_hit']}/{b['top1_target']}"
          f"  (Δ = {b['top1_hit']-a['top1_hit']:+d})")
    print(f"top3: {a['top3_hit']}/{a['total']}  →  {b['top3_hit']}/{b['total']}"
          f"  (Δ = {b['top3_hit']-a['top3_hit']:+d})")

    # 逐条 diff
    a_by_q = {d["query"]: d for d in a["details"]}
    b_by_q = {d["query"]: d for d in b["details"]}
    print("\n--- 变化项 ---")
    for q, bd in b_by_q.items():
        ad = a_by_q.get(q, {})
        if ad.get("top3_ok") != bd["top3_ok"] or ad.get("top1_ok") != bd["top1_ok"]:
            arrow = "🔺" if (bd["top3_ok"] and not ad.get("top3_ok")) or (bd["top1_ok"] and not ad.get("top1_ok")) else "🔻"
            print(f"  {arrow} [{q}]")
            print(f"     前: top3={ad.get('top_ids', [])}  top1_ok={ad.get('top1_ok')}")
            print(f"     后: top3={bd['top_ids']}  top1_ok={bd['top1_ok']}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--save", metavar="NAME", help="保存本次结果快照")
    ap.add_argument("--diff", nargs=2, metavar=("A", "B"), help="对比两个快照")
    args = ap.parse_args()

    if args.diff:
        diff_snapshots(*args.diff)
        return 0

    cases = json.loads(GT_FILE.read_text())["cases"]
    result = evaluate(cases)
    print_report(result, verbose=args.verbose)

    if args.save:
        p = save_snapshot(result, args.save)
        print(f"\nsaved: {p}")

    return 0 if result["top3_rate"] == 1.0 else 1


if __name__ == "__main__":
    sys.exit(main())
