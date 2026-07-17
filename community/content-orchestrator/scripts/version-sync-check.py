#!/usr/bin/env python3
"""
content-orchestrator version sync check.

Detects upstream drift in content cluster skills (baoyu-*, doc-coauthoring,
remotion, ai-seo, etc).

Usage:
  python3 scripts/version-sync-check.py
  python3 scripts/version-sync-check.py --refresh
  python3 scripts/version-sync-check.py --target ai-seo

Exit codes: 0=aligned, 1=drift, 2=error.
"""

import json
import os
import re
import sys


REFERENCED_SKILLS = [
    # Writing
    ("doc-coauthoring",            "community/doc-coauthoring/SKILL.md"),
    ("markdown-mermaid-writing",   "external/claude-scientific-skills/scientific-skills/markdown-mermaid-writing/SKILL.md"),
    ("document-release",           "community/gstack/document-release/SKILL.md"),
    ("support-ticket-triage",      "community/support-ticket-triage/SKILL.md"),
    ("youtube-script-optimizer",   "community/youtube-script-optimizer/SKILL.md"),
    ("meeting-notes-and-actions",  "community/meeting-notes-and-actions/SKILL.md"),
    # Doc / slide decks
    ("baoyu-markdown-to-html",     "community/baoyu-skills/baoyu-markdown-to-html/SKILL.md"),
    ("baoyu-slide-deck",           "community/baoyu-skills/baoyu-slide-deck/SKILL.md"),
    ("baoyu-format-markdown",      "community/baoyu-skills/baoyu-format-markdown/SKILL.md"),
    ("baoyu-translate",            "community/baoyu-skills/baoyu-translate/SKILL.md"),
    ("baoyu-danger-x-to-markdown", "community/baoyu-skills/baoyu-danger-x-to-markdown/SKILL.md"),
    ("baoyu-post-to-wechat",       "community/baoyu-skills/baoyu-post-to-wechat/SKILL.md"),
    ("baoyu-imagine",              "community/baoyu-skills/baoyu-imagine/SKILL.md"),
    ("baoyu-article-illustrator",  "community/baoyu-skills/baoyu-article-illustrator/SKILL.md"),
    ("baoyu-cover-image",          "community/baoyu-skills/baoyu-cover-image/SKILL.md"),
    ("baoyu-image-cards",          "community/baoyu-skills/baoyu-image-cards/SKILL.md"),
    ("baoyu-comic",                "community/baoyu-skills/baoyu-comic/SKILL.md"),
    ("baoyu-diagram",              "community/baoyu-skills/baoyu-diagram/SKILL.md"),
    # Presentation / design
    ("magazine-web-ppt",           "community/magazine-web-ppt/SKILL.md"),
    ("visual-forge",               "community/visual-forge/SKILL.md"),
    ("deck-that-wins",             "community/deck-that-wins/SKILL.md"),
    ("awesome-design-md",          "community/awesome-design-md/SKILL.md"),
    ("zero-debt-lint",             "community/zero-debt-lint/SKILL.md"),
    ("spreadsheet-formula-helper", "community/spreadsheet-formula-helper/SKILL.md"),
    ("to-prd",                     "community/to-prd/SKILL.md"),
    # Video
    ("remotion",                   "community/remotion/SKILL.md"),
    ("video-content-analyzer",     "external/video-content-analyzer/SKILL.md"),
    ("video-analyzer",             "community/video-analyzer/SKILL.md"),
    ("video-frame-extractor",      "community/video-frame-extractor/SKILL.md"),
    # Video production
    ("faceless-explainer",         "external/hyperframes/skills/faceless-explainer/SKILL.md"),
    ("talking-head-recut",         "external/hyperframes/skills/talking-head-recut/SKILL.md"),
    ("motion-graphics",            "external/hyperframes/skills/motion-graphics/SKILL.md"),
    ("embedded-captions",          "external/hyperframes/skills/embedded-captions/SKILL.md"),
    ("hyperframes-cli",            "external/hyperframes/skills/hyperframes-cli/SKILL.md"),
    # SEO
    ("ai-seo",                     "external/marketingskills/skills/ai-seo/SKILL.md"),
    ("programmatic-seo",           "external/claude-skills/marketing-skill/programmatic-seo/SKILL.md"),
    ("schema-markup",              "external/marketingskills/skills/schema-markup/SKILL.md"),
    ("seo-audit",                  "external/marketingskills/skills/seo-audit/SKILL.md"),
    # 小红书 / CN-specific
    ("xhs-publish",                "external/xiaohongshu-skills/skills/xhs-publish/SKILL.md"),
    ("xiaohongshu-skills",         "external/xiaohongshu-skills/SKILL.md"),
    ("xhs-content-ops",            "external/xiaohongshu-skills/skills/xhs-content-ops/SKILL.md"),
    ("xhs-auth",                   "external/xiaohongshu-skills/skills/xhs-auth/SKILL.md"),
    ("xhs-explore",                "external/xiaohongshu-skills/skills/xhs-explore/SKILL.md"),
]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
VERSION_RE = re.compile(r"^version:\s*(\S+)", re.MULTILINE)
NAME_RE = re.compile(r"^name:\s*(\S+)", re.MULTILINE)

CACHE_FILE = ".content-orch-version-cache.json"


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
                f"(orchestrator may reference stale content method)"
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
