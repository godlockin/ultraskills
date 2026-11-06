#!/usr/bin/env python3
"""
validate_skills.py — UltraSkills CI dry-run validator (v2.0)

v2.0 修复了旧版四类根因：
  1. 逐行正则 frontmatter 解析 → 多行描述 / 嵌套 metadata.version / 块列表误报
  2. 递归 os.walk() 与有限 glob 口径漂移 → 统一由 skill_contract.iter_skill_dirs() 提供
  3. 静态 index.json 快照过期 → 明确「全量登记 / 精选登记」两种职责边界
  4. external 第三方 skill 缺 version/tags 被当成 warning → 归入可选元数据 INFO

契约不再靠「降级告警」掩盖问题：自有 skill 缺字段、应登记未登记一律升为 ERROR。
上游skill 的可选元数据缺口不丢弃，可用 --coverage-report 导出完整明细。

Usage:
  python3 validate_skills.py
  python3 validate_skills.py --fix-hints
  python3 validate_skills.py --coverage-report devops/skill-arena/reports/skill-coverage.json

Exit code: 0 = pass, 1 = errors found
"""

import argparse
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skill_contract as sc

REPO_ROOT = sc.REPO_ROOT
INDEX_FILE = os.path.join(REPO_ROOT, "index.json")


def skill_dir(raw_path):
    """Resolve skill directory from an index.json path."""
    p = os.path.normpath(os.path.join(REPO_ROOT, raw_path.lstrip("./")))
    return os.path.dirname(p) if p.endswith("SKILL.md") else p


def validate_all(show_fix_hints=False, coverage_path=None):
    errors, warnings = [], []

    if not os.path.exists(INDEX_FILE):
        print(f"ERROR: index.json not found at {INDEX_FILE}")
        sys.exit(1)

    with open(INDEX_FILE, encoding="utf-8") as f:
        idx = json.load(f)

    indexed_paths = {skill_dir(s["path"]) for s in idx["skills"]}
    submodule_roots = sc.load_submodule_roots()

    # ---- Check A: 索引条目必须指向真实存在、且在统一扫描范围内的 skill ----
    scan_set = {norm for norm, _, _ in sc.iter_skill_dirs()}
    for s in idx["skills"]:
        resolved = skill_dir(s["path"])
        if not os.path.isdir(resolved):
            msg = f"[MISSING_DIR] id={s['id']} path={s['path']} → directory not found"
            (warnings if sc.is_under_submodule(resolved, submodule_roots) else errors).append(msg)
            continue
        if not os.path.exists(os.path.join(resolved, "SKILL.md")):
            errors.append(f"[MISSING_SKILL_MD] id={s['id']} → SKILL.md not found in {resolved}")
        if resolved not in scan_set:
            warnings.append(
                f"[STALE_INDEX_ENTRY] id={s['id']} path={s['path']} "
                f"→ 不在统一扫描范围内（模板/测试夹具？）"
            )

    # ---- Check B: 统一口径遍历所有 skill ----
    coverage = {
        "upstream_missing_version": [],
        "upstream_missing_tags": [],
        "selective_not_indexed": [],
    }
    scanned = full_scope = 0

    for norm_root, rel, skill_md in sc.iter_skill_dirs():
        scanned += 1
        rel_posix = rel.replace(os.sep, "/")
        with open(skill_md, encoding="utf-8", errors="replace") as f:
            fields = sc.parse_frontmatter(f.read())

        if fields is None:
            errors.append(f"[NO_FRONTMATTER] {rel_posix}/SKILL.md — 缺少 YAML frontmatter")
            continue

        upstream = sc.is_upstream(rel, norm_root, submodule_roots)
        required = sc.UPSTREAM_REQUIRED_FIELDS if upstream else sc.OWNED_REQUIRED_FIELDS
        for field in required:
            if field not in fields:
                errors.append(
                    f"[MISSING_FIELD:{field}] {rel_posix}/SKILL.md "
                    f"({'上游' if upstream else '自有'} skill 必需字段)"
                )

        if upstream:
            if "version" not in fields:
                coverage["upstream_missing_version"].append(rel_posix)
            if "tags" not in fields:
                coverage["upstream_missing_tags"].append(rel_posix)

        if sc.in_full_index_scope(rel):
            full_scope += 1
            if norm_root not in indexed_paths:
                errors.append(
                    f"[NOT_REGISTERED] {rel_posix}/SKILL.md — 自有 skill 未登记进 index.json "
                    f"（运行 sync_skill_index.py --apply）"
                )
        elif norm_root not in indexed_paths:
            coverage["selective_not_indexed"].append(rel_posix)

    # ---- 报告 ----
    print("\n=== UltraSkills Validation ===")
    print(f"Repo:     {REPO_ROOT}")
    print(f"Contract: skill_contract {sc.CONTRACT_VERSION}")
    print(f"Scanned:  {scanned} SKILL.md files (统一口径)")
    print(f"Indexed:  {len(idx['skills'])} skills in index.json")
    print(f"Scope:    全量登记 {full_scope} / 精选登记 {scanned - full_scope}")
    print()

    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("ERRORS: none ✓")

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
        print("WARNINGS: none ✓")

    n_ver = len(coverage["upstream_missing_version"])
    n_tag = len(coverage["upstream_missing_tags"])
    n_sel = len(coverage["selective_not_indexed"])
    print("\nCOVERAGE (上游可选元数据，按契约不阻断):")
    print(f"  external / submodule 缺 version:  {n_ver}")
    print(f"  external / submodule 缺 tags:     {n_tag}")
    print(f"  external 精选范围未入选索引:      {n_sel}")
    if coverage_path:
        print(f"  明细 → {coverage_path}")
    else:
        print("  明细 → --coverage-report <path>")

    if show_fix_hints and errors:
        print("\nFIX HINTS:")
        print("  MISSING_FIELD / NO_FRONTMATTER → 补齐该 SKILL.md 的 frontmatter")
        print("  NOT_REGISTERED / STALE_INDEX_ENTRY → python3 sync_skill_index.py --apply --prune-stale")
        print("  MISSING_DIR 且属 submodule → git submodule update --init --recursive")

    if coverage_path:
        out = os.path.join(REPO_ROOT, coverage_path) if not os.path.isabs(coverage_path) else coverage_path
        os.makedirs(os.path.dirname(out), exist_ok=True)
        payload = {
            "contract_version": sc.CONTRACT_VERSION,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "repo": REPO_ROOT,
            "scanned": scanned,
            "indexed": len(idx["skills"]),
            "full_index_scope": full_scope,
            "counts": {
                "upstream_missing_version": n_ver,
                "upstream_missing_tags": n_tag,
                "selective_not_indexed": n_sel,
            },
            "errors": errors,
            "warnings": warnings,
            **coverage,
        }
        with open(out, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    print()
    if errors:
        print(f"Result: FAIL ({len(errors)} errors, {len(warnings)} warnings)")
        sys.exit(1)
    print(f"Result: PASS (0 errors, {len(warnings)} warnings)")
    sys.exit(0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="UltraSkills skill validator")
    ap.add_argument("--fix-hints", action="store_true", help="show suggested fixes")
    ap.add_argument("--coverage-report", metavar="PATH", help="write full coverage JSON")
    args = ap.parse_args()
    validate_all(show_fix_hints=args.fix_hints, coverage_path=args.coverage_report)
