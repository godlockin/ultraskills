#!/usr/bin/env python3
"""Wrapper for ui-ux-pro-max-skill.

Lazily clones https://github.com/nextlevelbuilder/ui-ux-pro-max-skill into
~/.cache/ui-ux-pro-max/ on first run, then dispatches the user's brief
to the upstream design-system generator.

Usage:
    python wrapper.py "<design brief>"
"""
import os
import sys
import subprocess
from pathlib import Path

REPO_URL = "https://github.com/nextlevelbuilder/ui-ux-pro-max-skill"
PINNED_HASH = "b7e3af80f6e331f6fb456667b82b12cade7c9d35"
CACHE_DIR = Path.home() / ".cache" / "ui-ux-pro-max"


def ensure_repo() -> Path:
    if not CACHE_DIR.exists():
        CACHE_DIR.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["git", "clone", "--depth", "50", REPO_URL, str(CACHE_DIR)],
            check=True,
        )
        subprocess.run(["git", "checkout", PINNED_HASH], cwd=CACHE_DIR, check=False)
    return CACHE_DIR


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: python wrapper.py "<design brief>"', file=sys.stderr)
        return 2

    brief = " ".join(sys.argv[1:])
    repo = ensure_repo()

    # Try common upstream entry points in order.
    candidates = [
        ["python3", "main.py", brief],
        ["python3", "cli.py", brief],
        ["python3", "-m", "uipro", brief],
        ["npx", "uipro-cli", "design", brief],
    ]

    for cmd in candidates:
        exe = cmd[0]
        if exe.startswith("python") and len(cmd) > 1 and not (repo / cmd[1]).exists():
            continue
        try:
            return subprocess.run(cmd, cwd=repo).returncode
        except FileNotFoundError:
            continue

    print(
        f"No upstream entry point found. Inspect the cloned repo at:\n  {repo}\n"
        "and update wrapper.py with the correct invocation.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
