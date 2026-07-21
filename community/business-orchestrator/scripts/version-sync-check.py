#!/usr/bin/env python3
"""
business-orchestrator version sync check.

Detects upstream drift in business cluster skills (comps-analysis, dcf-model,
lbo-model, pitch-deck, initiating-coverage, etc). Reads SKILL.md frontmatter
`version` for each referenced skill, compares to cache. Outputs warnings.

Usage:
  python3 scripts/version-sync-check.py           # full check (cached)
  python3 scripts/version-sync-check.py --refresh # re-scan
  python3 scripts/version-sync-check.py --target dcf-model  # one skill

Exit codes:
  0 = aligned
  1 = drift
  2 = error (missing/unparseable)
"""

import json
import os
import re
import sys


# Skills referenced by business-orchestrator (canonical business cluster)
REFERENCED_SKILLS = [
    # Anthropic financial services — core analytic skills
    ("initiating-coverage",  "external/anthropic-financial-services/initiating-coverage/SKILL.md"),
    ("comps-analysis",       "external/anthropic-financial-services/comps-analysis/SKILL.md"),
    ("dcf-model",            "external/anthropic-financial-services/dcf-model/SKILL.md"),
    ("earnings-analysis",    "external/anthropic-financial-services/earnings-analysis/SKILL.md"),
    ("datapack-builder",     "external/anthropic-financial-services/datapack-builder/SKILL.md"),
    ("3-statement-model",    "external/anthropic-financial-services/3-statement-model/SKILL.md"),
    ("lbo-model",            "external/anthropic-financial-services/lbo-model/SKILL.md"),
    ("pitch-deck",           "external/anthropic-financial-services/pitch-deck/SKILL.md"),
    ("deck-refresh",         "external/anthropic-financial-services/deck-refresh/SKILL.md"),
    ("ai-readiness",         "external/anthropic-financial-services/ai-readiness/SKILL.md"),
    ("audit-xls",            "external/anthropic-financial-services/audit-xls/SKILL.md"),
    ("competitive-analysis", "external/anthropic-financial-services/competitive-analysis/SKILL.md"),
    ("deal-sourcing",        "external/anthropic-financial-services/deal-sourcing/SKILL.md"),
    # SMB operations
    ("smb-onboard",              "external/knowledge-work-plugins/small-business/skills/smb-onboard/SKILL.md"),
    ("canva-creator",            "external/knowledge-work-plugins/small-business/skills/canva-creator/SKILL.md"),
    ("cash-flow-snapshot",       "external/knowledge-work-plugins/small-business/skills/cash-flow-snapshot/SKILL.md"),
    ("invoice-chase",            "external/knowledge-work-plugins/small-business/skills/invoice-chase/SKILL.md"),
    ("customer-pulse",           "external/knowledge-work-plugins/small-business/skills/customer-pulse/SKILL.md"),
    ("lead-triage",              "external/knowledge-work-plugins/small-business/skills/lead-triage/SKILL.md"),
    # Customer support / ops
    ("customer-escalation",      "external/knowledge-work-plugins/customer-support/skills/customer-escalation/SKILL.md"),
    ("draft-response",           "external/knowledge-work-plugins/customer-support/skills/draft-response/SKILL.md"),
    ("kb-article",               "external/knowledge-work-plugins/customer-support/skills/kb-article/SKILL.md"),
    ("sop-writer",               "community/sop-writer/SKILL.md"),
    ("crisis-comms-playbook",    "community/crisis-comms-playbook/SKILL.md"),
    # C-level / CEO / product
    ("digital-brain",            "external/context-engineering-skills/examples/digital-brain-skill/SKILL.md"),
    ("data-viz",                 "community/data-viz/SKILL.md"),
    ("plan-ceo-review",          "community/gstack/plan-ceo-review/SKILL.md"),
    ("office-hours",             "community/gstack/office-hours/SKILL.md"),
    ("unit-economics",           "community/unit-economics-calculator/SKILL.md"),
    # Accounting / finance
    ("variance-analysis",        "external/knowledge-work-plugins/finance/skills/variance-analysis/SKILL.md"),
    ("journal-entry",            "external/knowledge-work-plugins/finance/skills/journal-entry/SKILL.md"),
    ("close-management",         "external/knowledge-work-plugins/finance/skills/close-management/SKILL.md"),
    ("audit-support",            "external/knowledge-work-plugins/finance/skills/audit-support/SKILL.md"),
    # Legal (mandatory in B2)
    ("review-contract",          "external/knowledge-work-plugins/legal/skills/review-contract/SKILL.md"),
    ("triage-nda",               "external/knowledge-work-plugins/legal/skills/triage-nda/SKILL.md"),
    ("vendor-check",             "external/knowledge-work-plugins/legal/skills/vendor-check/SKILL.md"),
    ("meeting-briefing",         "external/knowledge-work-plugins/legal/skills/meeting-briefing/SKILL.md"),
    ("compliance-check",         "external/knowledge-work-plugins/legal/skills/compliance-check/SKILL.md"),
    ("legal-risk-assessment",    "external/knowledge-work-plugins/legal/skills/legal-risk-assessment/SKILL.md"),
    ("contract-risk-highlighter","community/contract-risk-highlighter/SKILL.md"),
    ("legal-response",           "external/knowledge-work-plugins/legal/skills/legal-response/SKILL.md"),
    # Sales
    ("objection-handler",        "community/objection-handler/SKILL.md"),
    ("okr-alignment",            "community/okr-alignment-checker/SKILL.md"),
    ("pitch-deck-critic",        "community/pitch-deck-critic/SKILL.md"),
    ("create-an-asset",          "external/knowledge-work-plugins/sales/skills/create-an-asset/SKILL.md"),
    ("draft-outreach",           "external/knowledge-work-plugins/sales/skills/draft-outreach/SKILL.md"),
    # PM / retro
    ("learn-from-loss",          "community/learn-from-loss/SKILL.md"),
    ("to-issues",                "community/to-issues/SKILL.md"),
    ("retro",                    "community/gstack/retro/SKILL.md"),
    ("grill-me",                 "community/grill-me/SKILL.md"),
    # Strategy
    ("competitive-intelligence", "external/knowledge-work-plugins/sales/skills/competitive-intelligence/SKILL.md"),
    # HR
    ("performance-review",       "external/knowledge-work-plugins/human-resources/skills/performance-review/SKILL.md"),
    ("draft-offer",              "external/knowledge-work-plugins/human-resources/skills/draft-offer/SKILL.md"),
    ("comp-analysis",            "external/knowledge-work-plugins/human-resources/skills/comp-analysis/SKILL.md"),
]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
VERSION_RE = re.compile(r"^version:\s*(\S+)", re.MULTILINE)
NAME_RE = re.compile(r"^name:\s*(\S+)", re.MULTILINE)

CACHE_FILE = ".business-orch-version-cache.json"


def get_repo_root():
    """scripts → business-orchestrator → community → repo_root."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(os.path.join(script_dir, "..", "..", ".."))


def read_skill_version(repo_root, rel_path):
    full_path = os.path.join(repo_root, rel_path)
    if not os.path.exists(full_path):
        return None
    try:
        with open(full_path, encoding="utf-8") as f:
            content = f.read(65536)
    except OSError:
        return None
    m = FRONTMATTER_RE.match(content)
    if not m:
        return None
    fm = m.group(1)
    name_m = NAME_RE.search(fm)
    version_m = VERSION_RE.search(fm)
    name = name_m.group(1) if name_m else "?"
    if not version_m:
        return (name, None)
    return (name, version_m.group(1))


def load_cache(repo_root):
    cache_path = os.path.join(repo_root, CACHE_FILE)
    if not os.path.exists(cache_path):
        return {}
    try:
        with open(cache_path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(repo_root, cache):
    cache_path = os.path.join(repo_root, CACHE_FILE)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2, ensure_ascii=False, sort_keys=True)


def main():
    args = sys.argv[1:]
    refresh = "--refresh" in args
    target = None
    for i, a in enumerate(args):
        if a == "--target" and i + 1 < len(args):
            target = args[i + 1]
            break

    repo_root = get_repo_root()
    cache = load_cache(repo_root)
    if refresh:
        cache = {}

    skills_to_check = REFERENCED_SKILLS
    if target:
        skills_to_check = [(n, p) for n, p in REFERENCED_SKILLS if n == target]
        if not skills_to_check:
            print(f"Unknown skill: {target}")
            sys.exit(2)

    new_cache = {}
    warnings = []
    errors = []
    no_version = []

    for name, rel_path in skills_to_check:
        result = read_skill_version(repo_root, rel_path)
        if result is None:
            errors.append(f"MISSING: {name} → {rel_path}")
            continue
        actual_name, version = result
        if version is None:
            no_version.append(actual_name)
            print(f"[NOVR]   {actual_name:35s} (no frontmatter version)")
            continue

        new_cache[actual_name] = version
        cached_version = cache.get(actual_name)
        if cached_version is None:
            print(f"[NEW]    {actual_name:35s} v{version}")
        elif cached_version != version:
            warnings.append(
                f"[DRIFT]  {actual_name:35s} v{cached_version} → v{version} "
                f"(orchestrator may reference stale method)"
            )
        else:
            print(f"[OK]     {actual_name:35s} v{version}")

    save_cache(repo_root, new_cache)

    print()
    print(f"Checked:   {len(skills_to_check)}")
    print(f"Errors:    {len(errors)}")
    print(f"No-Version:{len(no_version)}")
    print(f"Drift:     {len(warnings)}")
    print(f"Cache:     {CACHE_FILE}")

    if errors:
        print()
        for e in errors:
            print(f"  {e}")

    if warnings:
        print()
        print("WARNINGS (review references for broken methodology):")
        for w in warnings:
            print(f"  {w}")
        sys.exit(1)

    if errors:
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
