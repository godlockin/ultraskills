#!/usr/bin/env python3
"""Wrapper for awesome-android-ui reference catalog.

Subcommands:
    list                   — print the full mirrored README
    search <term> [...]    — grep catalog (case-insensitive) for term(s)
"""
import sys
import re
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "references" / "upstream-readme.md"


def cmd_list() -> int:
    if not CATALOG.exists():
        print(f"Catalog missing: {CATALOG}", file=sys.stderr)
        return 1
    sys.stdout.write(CATALOG.read_text(encoding="utf-8"))
    return 0


def cmd_search(terms):
    if not CATALOG.exists():
        print(f"Catalog missing: {CATALOG}", file=sys.stderr)
        return 1
    text = CATALOG.read_text(encoding="utf-8")
    pattern = re.compile("|".join(re.escape(t) for t in terms), re.IGNORECASE)
    hits = [line for line in text.splitlines() if pattern.search(line)]
    if not hits:
        print(f"(no matches for: {' '.join(terms)})", file=sys.stderr)
        return 1
    for line in hits:
        print(line)
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    sub = sys.argv[1]
    if sub == "list":
        return cmd_list()
    if sub == "search" and len(sys.argv) >= 3:
        return cmd_search(sys.argv[2:])
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
