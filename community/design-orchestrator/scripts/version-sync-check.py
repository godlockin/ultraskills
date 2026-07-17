#!/usr/bin/env python3
"""
design-orchestrator version sync check.

Detects upstream drift in referenced skills (hallmark, ui-ux-pro-max, etc).
Reads SKILL.md frontmatter `version` for each referenced skill, compares
to cached last-known-good in `.design-orch-version-cache.json`. Outputs
warnings and exits 1 if any upstream bumped.

Usage:
  python3 scripts/version-sync-check.py           # full check (cached)
  python3 scripts/version-sync-check.py --refresh  # re-scan all 22 design skills
  python3 scripts/version-sync-check.py --target hallmark  # check one skill

Exit codes:
  0 = all aligned
  1 = at least one upstream moved (warnings)
  2 = error (missing SKILL.md, parse failure)
"""

import json
import os
import re
import sys
from pathlib import Path


# Skills referenced by orchestrator (canonical 22 minus non-design product ops)
REFERENCED_SKILLS = [
    ("hallmark",                    "community/hallmark/SKILL.md"),
    ("ui-ux-pro-max-skill",         "community/ui-ux-pro-max-skill/SKILL.md"),
    ("awesome-design-md",           "community/awesome-design-md/SKILL.md"),
    ("design-consultation",         "community/gstack/design-consultation/SKILL.md"),
    ("design-review",               "community/gstack/design-review/SKILL.md"),
    ("design-shotgun",              "community/gstack/design-shotgun/SKILL.md"),
    ("plan-design-review",          "community/gstack/plan-design-review/SKILL.md"),
    ("design-html",                 "community/gstack/design-html/SKILL.md"),
    ("design-tokens",               "community/design-tokens/SKILL.md"),
    ("figma-to-code",               "community/figma-to-code/SKILL.md"),
    ("icon-system",                 "community/icon-system/SKILL.md"),
    ("motion-design",               "community/motion-design/SKILL.md"),
    ("design-an-interface",         "community/design-an-interface/SKILL.md"),
    ("awwwards-design-intelligence","community/awwwards-design-intelligence/SKILL.md"),
    ("color-expert",                "external/color-expert/SKILL.md"),
    ("design-system",               "external/knowledge-work-plugins/design/skills/design-system/SKILL.md"),
    ("ux-copy",                     "external/knowledge-work-plugins/design/skills/ux-copy/SKILL.md"),
    ("design-critique",             "external/knowledge-work-plugins/design/skills/design-critique/SKILL.md"),
    ("design-handoff",              "external/knowledge-work-plugins/design/skills/design-handoff/SKILL.md"),
    ("accessibility-review",        "external/knowledge-work-plugins/design/skills/accessibility-review/SKILL.md"),
    ("write-spec",                  "external/knowledge-work-plugins/product-management/skills/write-spec/SKILL.md"),
    ("metrics-review",              "external/knowledge-work-plugins/product-management/skills/metrics-review/SKILL.md"),
    ("stakeholder-update",          "external/knowledge-work-plugins/product-management/skills/stakeholder-update/SKILL.md"),
    ("sprint-planning",             "external/knowledge-work-plugins/product-management/skills/sprint-planning/SKILL.md"),
    ("ikea-designer-pro",           "community/ikea-designer/SKILL.md"),
]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
VERSION_RE = re.compile(r"^version:\s*(\S+)", re.MULTILINE)
NAME_RE = re.compile(r"^name:\s*(\S+)", re.MULTILINE)

CACHE_FILE = ".design-orch-version-cache.json"


def get_repo_root():
    """Resolve repo root from script path. ../../.. walks up from scripts/."""
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # scripts → design-orchestrator → community → repo_root
    return os.path.abspath(os.path.join(script_dir, "..", "..", ".."))


def read_skill_version(repo_root, rel_path):
    """Read version + name from SKILL.md frontmatter.

    Returns:
        (name, version) — both present
        ("name", None)  — version missing (skill has no frontmatter version)
        None            — file missing or unparseable frontmatter
    """
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
        return (name, None)  # skill exists but no version declared
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
            print(f"Available: {[n for n, _ in REFERENCED_SKILLS]}")
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
            print(f"[NOVR]   {actual_name:35s} (no frontmatter version — known upstream convention)")
            continue

        new_cache[actual_name] = version

        cached_version = cache.get(actual_name)
        if cached_version is None:
            # First time we see this — no comparison possible
            print(f"[NEW]    {actual_name:35s} v{version}")
        elif cached_version != version:
            warnings.append(
                f"[DRIFT]  {actual_name:35s} v{cached_version} → v{version}  "
                f"(orchestrator may reference stale anti-slop rules)"
            )
        else:
            print(f"[OK]     {actual_name:35s} v{version}")

    # Save cache
    save_cache(repo_root, new_cache)

    # Summary
    print()
    print(f"Checked:   {len(skills_to_check)}")
    print(f"Errors:    {len(errors)}")
    print(f"No-Version:{len(no_version)} (skills without frontmatter version)")
    print(f"Drift:     {len(warnings)}")
    print(f"Cache:     {CACHE_FILE} (next to repo root)")

    if errors:
        print()
        for e in errors:
            print(f"  {e}")

    if warnings:
        print()
        print("WARNINGS:")
        for w in warnings:
            print(f"  {w}")
        print()
        print("Action: review affected reference files in design-orchestrator/")
        print("  - references/routing-table.md")
        print("  - references/orchestration-patterns.md")
        print("  - references/anti-slop-index.md")
        sys.exit(1)

    if errors:
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
