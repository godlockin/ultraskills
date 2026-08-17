#!/usr/bin/env python3
"""
sync_submodules.py — update every configured submodule in .gitmodules.

Per-path loop so one failure doesn't stop the rest. Reads .gitmodules.deny
to silently skip submodules whose upstream is known-unreachable.

Exit code: 0 always (failures are reported, not fatal — submodule debt
is repo state, not a script bug).

Usage:
  python3 scripts/sync_submodules.py            # update all non-denied
  python3 scripts/sync_submodules.py --dry-run  # list what would be updated
  python3 scripts/sync_submodules.py --list     # show deny list + status
"""

import argparse
import configparser
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
GITMODULES = REPO_ROOT / ".gitmodules"
DENY_FILE = REPO_ROOT / ".gitmodules.deny"


def read_submodule_paths() -> list[str]:
    """Return paths from .gitmodules. Empty list if file missing."""
    if not GITMODULES.exists():
        return []
    cfg = configparser.ConfigParser()
    cfg.read(GITMODULES, encoding="utf-8")
    return [
        cfg.get(s, "path", fallback="")
        for s in cfg.sections()
        if cfg.has_option(s, "path")
    ]


def read_deny_list() -> set[str]:
    """Read .gitmodules.deny → set of paths to skip silently."""
    if not DENY_FILE.exists():
        return set()
    denied = set()
    for line in DENY_FILE.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        # Allow inline comments: "path  # reason" → keep only path
        s = s.split("#", 1)[0].strip()
        if s:
            denied.add(s)
    return denied


def shield_reverse_skill(path: str) -> tuple[bool, str]:
    """Shield reverse-skill after a successful update; never leave it unshielded."""
    if path != "external/reverse-skill":
        return True, "ok"
    target = REPO_ROOT / path
    rules_file = target / "RULES.md"
    if not rules_file.is_file():
        return False, f"shield target missing: {rules_file}"
    script = REPO_ROOT / "scripts" / "shield-reverse-skill.sh"
    result = subprocess.run(
        ["bash", str(script), str(target)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return True, "ok"
    error = (result.stderr or result.stdout or "shield failed").strip().splitlines()
    return False, f"shield: {error[-1] if error else 'shield failed'}"


def update_one(path: str) -> tuple[bool, str]:
    """Update one submodule and shield reverse-skill before reporting success."""
    r = subprocess.run(
        ["git", "submodule", "update", "--init", "--remote", "--recursive", path],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        # Last non-empty error line
        err = ""
        for line in (r.stderr or "").splitlines():
            line = line.strip()
            if line and ("fatal" in line or "error" in line):
                err = line
        return False, err or f"exit {r.returncode}"
    return shield_reverse_skill(path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="list updates that would run")
    ap.add_argument("--list", action="store_true", help="show status table and exit")
    args = ap.parse_args()

    all_paths = read_submodule_paths()
    denied = read_deny_list()
    targets = [p for p in all_paths if p and p not in denied]

    if args.list:
        print(f"{'PATH':<48} {'STATUS'}")
        for p in all_paths:
            status = "DENY" if p in denied else "OK"
            print(f"  {p:<46} {status}")
        print(f"\nTotal: {len(all_paths)} configured, {len(denied)} denied, {len(targets)} active")
        return 0

    if args.dry_run:
        print(f"Would update {len(targets)} submodule(s):")
        for p in targets:
            print(f"  {p}")
        if denied:
            print(f"\nSkipping {len(denied)} denied submodule(s):")
            for p in sorted(denied):
                print(f"  {p}")
        return 0

    print(f"Updating {len(targets)} submodule(s)...")
    ok = 0
    failed: list[tuple[str, str]] = []
    shield_failed = False
    for path in targets:
        print(f"  {path:<48} ", end="", flush=True)
        success, msg = update_one(path)
        if success:
            print("✓")
            ok += 1
        else:
            print(f"✗ {msg[:60]}")
            failed.append((path, msg))
            if path == "external/reverse-skill" and msg.startswith("shield"):
                shield_failed = True

    print()
    print(f"Done: {ok} updated, {len(failed)} failed")
    if denied:
        print(f"Skipped {len(denied)} (see .gitmodules.deny)")
    if failed:
        print("\nFailures (upstream debt, not blockers):")
        for p, msg in failed:
            print(f"  {p}: {msg[:80]}")
    return 1 if shield_failed else 0  # shield failure must not leave injection active


if __name__ == "__main__":
    sys.exit(main())
