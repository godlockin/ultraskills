#!/usr/bin/env python3
"""
lessons-lookup — Search ~/.claude/lessons/ for relevant past lessons.

Usage:
  lessons-lookup <keyword> [keyword2 ...]
  lessons-lookup --list
  lessons-lookup --skill <skill-id>

Examples:
  lessons-lookup python injection
  lessons-lookup --skill skill-evolution-manager
  lessons-lookup --list
"""

import sys
import json
import os
import re

LESSONS_DIR = os.path.expanduser("~/.claude/lessons")
INDEX_FILE = os.path.join(LESSONS_DIR, "index.json")


def load_index():
    if not os.path.exists(INDEX_FILE):
        print("No lessons index found. Run consolidate-evolutions.sh first.")
        sys.exit(0)
    with open(INDEX_FILE, encoding='utf-8') as f:
        return json.load(f)


def cmd_list(idx):
    lessons = idx.get('lessons', [])
    if not lessons:
        print("No lessons recorded yet.")
        return
    print(f"{'SKILL':<40} {'UPDATED':<25} KEYWORDS")
    print("-" * 90)
    for l in sorted(lessons, key=lambda x: x.get('updated', ''), reverse=True):
        kws = ', '.join(l.get('keywords', [])[:6])
        print(f"{l['id']:<40} {l.get('updated','?'):<25} {kws}")


def cmd_skill(idx, skill_id):
    lessons = idx.get('lessons', [])
    match = next((l for l in lessons if l['id'] == skill_id), None)
    if not match:
        # Try partial match
        matches = [l for l in lessons if skill_id.lower() in l['id'].lower()]
        if not matches:
            print(f"No lessons found for: {skill_id}")
            return
        if len(matches) == 1:
            match = matches[0]
        else:
            print(f"Multiple matches: {', '.join(m['id'] for m in matches)}")
            return
    path = match['path']
    if os.path.exists(path):
        print(open(path, encoding='utf-8').read())
    else:
        print(f"Lessons file not found: {path}")


def cmd_search(idx, keywords):
    lessons = idx.get('lessons', [])
    kw_lower = [k.lower() for k in keywords]

    results = []
    for l in lessons:
        index_kws = [k.lower() for k in l.get('keywords', [])]
        skill_id_lower = l['id'].lower()

        # Score: how many keywords match
        score = sum(
            1 for kw in kw_lower
            if kw in skill_id_lower or any(kw in ik for ik in index_kws)
        )
        if score > 0:
            results.append((score, l))

    if not results:
        print(f"No lessons found for: {' '.join(keywords)}")
        return

    results.sort(key=lambda x: -x[0])
    for score, l in results[:5]:
        print(f"\n{'='*60}")
        print(f"  {l['id']}  (score: {score}, updated: {l.get('updated','?')[:10]})")
        print(f"  keywords: {', '.join(l.get('keywords',[])[:8])}")
        path = l['path']
        if os.path.exists(path):
            content = open(path, encoding='utf-8').read()
            # Show first 40 lines
            lines = content.split('\n')[:40]
            print('\n'.join(lines))
            if len(content.split('\n')) > 40:
                print(f"  ... ({len(content.split(chr(10)))-40} more lines, use --skill {l['id']} for full)")
        else:
            print(f"  (file missing: {path})")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    idx = load_index()

    if args[0] == '--list':
        cmd_list(idx)
    elif args[0] == '--skill' and len(args) >= 2:
        cmd_skill(idx, args[1])
    else:
        cmd_search(idx, args)


if __name__ == '__main__':
    main()
