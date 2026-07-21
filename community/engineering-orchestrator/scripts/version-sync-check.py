#!/usr/bin/env python3
"""
engineering-orchestrator version sync check.

Detects upstream drift in engineering cluster skills. Mirrors design/business
orchestrator scripts.

Usage:
  python3 scripts/version-sync-check.py
  python3 scripts/version-sync-check.py --refresh
  python3 scripts/version-sync-check.py --target qa

Exit codes: 0=aligned, 1=drift, 2=error.
"""

import json
import os
import re
import sys

# Engineering cluster references
REFERENCED_SKILLS = [
    # Code quality
    ("receiving-code-review",       "community/receiving-code-review/SKILL.md"),
    ("changelog-generator",         "community/changelog-generator/SKILL.md"),
    ("improve-codebase-architecture","community/improve-codebase-architecture/SKILL.md"),
    ("code-documenter",             "external/fullstack-dev-skills/skills/code-documenter/SKILL.md"),
    # Architecture
    ("information-architecture",    "community/information-architecture/SKILL.md"),
    ("api-designer",                "external/fullstack-dev-skills/skills/api-designer/SKILL.md"),
    ("design-an-interface",         "community/design-an-interface/SKILL.md"),
    ("ubiquitous-language",         "community/ubiquitous-language/SKILL.md"),
    # DevOps / Deploy
    ("setup-deploy",                "community/gstack/setup-deploy/SKILL.md"),
    ("land-and-deploy",             "community/gstack/land-and-deploy/SKILL.md"),
    ("canary",                      "community/gstack/canary/SKILL.md"),
    # QA / Testing
    ("qa",                          "community/gstack/qa/SKILL.md"),
    ("devex-review",                "community/gstack/devex-review/SKILL.md"),
    ("test-case-templates",         "devops/skill-arena/templates/test-case-templates/SKILL.md"),
    ("triage-issue",                "community/triage-issue/SKILL.md"),
    # Debugging
    ("systematic-debugging",        "community/systematic-debugging/SKILL.md"),
    ("investigate",                 "community/gstack/investigate/SKILL.md"),
    # Security
    ("pre-mortem",                  "external/phuryn-pm-skills/pm-execution/skills/pre-mortem/SKILL.md"),
    ("cso",                         "community/gstack/cso/SKILL.md"),
    ("strategy-red-team",           "external/phuryn-pm-skills/pm-execution/skills/strategy-red-team/SKILL.md"),
    # Git
    ("using-git-worktrees",         "community/using-git-worktrees/SKILL.md"),
    ("finishing-a-development-branch","community/finishing-a-development-branch/SKILL.md"),
    # Dev tools
    ("codex",                       "community/gstack/codex/SKILL.md"),
    ("codegraph-booster",           "devops/codegraph-booster/SKILL.md"),
    ("skills-audit",                "devops/skills-audit/SKILL.md"),
    ("git-guardrails",              "community/git-guardrails-claude-code/SKILL.md"),
    # Framework/language specialists (single-skill)
    ("django-expert",               "external/fullstack-dev-skills/skills/django-expert/SKILL.md"),
    ("fastapi-expert",              "external/fullstack-dev-skills/skills/fastapi-expert/SKILL.md"),
    ("laravel-specialist",          "external/fullstack-dev-skills/skills/laravel-specialist/SKILL.md"),
    ("rust-engineer",               "external/fullstack-dev-skills/skills/rust-engineer/SKILL.md"),
    # Frontend
    ("design-html",                 "community/gstack/design-html/SKILL.md"),
    ("frontend-design",             "community/frontend-design/SKILL.md"),
]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
VERSION_RE = re.compile(r"^version:\s*(\S+)", re.MULTILINE)
NAME_RE = re.compile(r"^name:\s*(\S+)", re.MULTILINE)

CACHE_FILE = ".engineering-orch-version-cache.json"


def get_repo_root():
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
        print("WARNINGS:")
        for w in warnings:
            print(f"  {w}")
        sys.exit(1)

    if errors:
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
