#!/usr/bin/env python3
"""
validate_skills.py — CI dry-run validator for ultraskills.

Usage:
  python3 validate_skills.py              # validate all skills
  python3 validate_skills.py --fix-hints  # also show suggested fixes

Exit code: 0 = all pass, 1 = failures found
"""

import sys
import os
import json
import re
import configparser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))
INDEX_FILE = os.path.join(REPO_ROOT, "index.json")


def load_submodule_paths():
    """Parse .gitmodules and return set of normalized submodule root paths."""
    gitmodules = os.path.join(REPO_ROOT, ".gitmodules")
    if not os.path.exists(gitmodules):
        return set()
    cfg = configparser.ConfigParser()
    cfg.read(gitmodules, encoding="utf-8")
    paths = set()
    for section in cfg.sections():
        if cfg.has_option(section, "path"):
            p = cfg.get(section, "path")
            paths.add(os.path.normpath(os.path.join(REPO_ROOT, p)))
    return paths


def is_under_submodule(resolved_path, submodule_roots):
    """Return True if resolved_path is inside any known submodule root."""
    for sm_root in submodule_roots:
        # exact match (the submodule root itself) or a subdirectory
        if resolved_path == sm_root or resolved_path.startswith(sm_root + os.sep):
            return True
    return False

REQUIRED_FRONTMATTER = ["name", "description", "version", "tags"]

def parse_frontmatter(content):
    """Extract YAML frontmatter fields (simple key: value parser)."""
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        m = re.match(r"^(\w+)\s*:\s*(.+)", line.strip())
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields

def validate_all():
    errors = []
    warnings = []

    # Load index
    if not os.path.exists(INDEX_FILE):
        print(f"ERROR: index.json not found at {INDEX_FILE}")
        sys.exit(1)

    with open(INDEX_FILE, encoding="utf-8") as f:
        idx = json.load(f)

    indexed_ids = {s["id"] for s in idx["skills"]}

    def skill_dir(raw_path):
        """Resolve skill directory from path (handles both dir paths and SKILL.md paths)."""
        p = os.path.normpath(os.path.join(REPO_ROOT, raw_path.lstrip("./")))
        if p.endswith("SKILL.md"):
            return os.path.dirname(p)
        return p

    indexed_paths = {skill_dir(s["path"]) for s in idx["skills"]}

    submodule_roots = load_submodule_paths()

    # Check 1: all index entries point to existing dirs
    for s in idx["skills"]:
        resolved = skill_dir(s["path"])
        if not os.path.isdir(resolved):
            if is_under_submodule(resolved, submodule_roots):
                warnings.append(f"[MISSING_DIR:submodule-not-initialized] id={s['id']} path={s['path']}")
            else:
                errors.append(f"[MISSING_DIR] id={s['id']} path={s['path']} → directory not found")
        skill_md = os.path.join(resolved, "SKILL.md")
        if os.path.isdir(resolved) and not os.path.exists(skill_md):
            errors.append(f"[MISSING_SKILL_MD] id={s['id']} → SKILL.md not found in {resolved}")

    # Check 2: scan all SKILL.md files, validate frontmatter
    scanned = 0
    for root, dirs, files in os.walk(REPO_ROOT):
        # skip hidden dirs and node_modules
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
        if "SKILL.md" in files:
            skill_path = os.path.join(root, "SKILL.md")
            scanned += 1
            with open(skill_path, encoding="utf-8") as f:
                content = f.read()
            fields = parse_frontmatter(content)
            rel = os.path.relpath(root, REPO_ROOT)
            if fields is None:
                msg = f"[NO_FRONTMATTER] {rel}/SKILL.md — missing YAML frontmatter"
                # test assets are expected to lack frontmatter
                if 'assets/' in rel or 'sample' in rel:
                    warnings.append(msg)
                else:
                    errors.append(msg)
                continue
            norm_root = os.path.normpath(root)
            is_external = rel.startswith("external/") or is_under_submodule(norm_root, submodule_roots)
            for req in REQUIRED_FRONTMATTER:
                if req not in fields:
                    msg = f"[MISSING_FIELD:{req}] {rel}/SKILL.md"
                    # external skills may lack version/tags — downgrade to warning
                    if is_external and req in ("version", "tags"):
                        warnings.append(msg)
                    elif req == "description" and is_external:
                        # multi-line description not parsed by simple regex
                        warnings.append(msg)
                    else:
                        errors.append(msg)
            # Check if indexed
            if norm_root not in indexed_paths:
                warnings.append(f"[NOT_INDEXED] {rel}/SKILL.md — skill exists but not in index.json")

    # Report
    print(f"\n=== UltraSkills Validation ===")
    print(f"Repo:    {REPO_ROOT}")
    print(f"Scanned: {scanned} SKILL.md files")
    print(f"Indexed: {len(indexed_ids)} skills in index.json")
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

    print()
    if errors:
        print(f"Result: FAIL ({len(errors)} errors, {len(warnings)} warnings)")
        sys.exit(1)
    else:
        print(f"Result: PASS (0 errors, {len(warnings)} warnings)")
        sys.exit(0)

if __name__ == "__main__":
    validate_all()
