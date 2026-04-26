#!/usr/bin/env python3
"""
ultraskills search — find relevant skills by keyword/intent.

Usage:
  search.py <query terms...>
  search.py --tag <tag>
  search.py --list-tags
  search.py --id <skill-id>        # exact lookup, returns path
  search.py --winners              # list arena winners only

Output: JSON array of matches with id, path, description, score, tags
"""

import sys
import json
import os
import re

# Auto-detect repo root relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))
INDEX_FILE = os.path.join(REPO_ROOT, "index.json")


def load_index():
    if not os.path.exists(INDEX_FILE):
        print(json.dumps({"error": f"index.json not found at {INDEX_FILE}"}))
        sys.exit(1)
    with open(INDEX_FILE, encoding="utf-8") as f:
        return json.load(f)


def skill_path(s):
    """Absolute path to skill directory. Guards against path traversal."""
    # os.path.normpath resolves any ../.. sequences
    raw = os.path.join(REPO_ROOT, s["path"].lstrip("./"))
    resolved = os.path.normpath(raw)
    # Reject if resolved path escapes repo root
    if not resolved.startswith(REPO_ROOT + os.sep) and resolved != REPO_ROOT:
        return None  # poisoned index entry
    return resolved


def search(idx, query_terms, limit=8, winners_only=False, tag_filter=None):
    skills = idx["skills"]
    kw = [t.lower() for t in query_terms]

    results = []
    for s in skills:
        if winners_only and not s.get("arena", {}).get("is_winner"):
            continue
        if tag_filter and tag_filter not in s.get("tags", []):
            continue

        path = skill_path(s)
        if path is None:
            continue  # poisoned index entry, skip

        # Scoring: exact id match > tags > description keyword hits
        score = 0
        sid = s["id"].lower()
        desc = s.get("description", "").lower()
        tags = [t.lower() for t in s.get("tags", [])]
        rec = [r.lower() for r in s.get("recommended_for", [])]

        for kw_item in kw:
            if kw_item == sid:
                score += 20
            elif kw_item in sid:
                score += 5  # reduced from 10: prevent id-substring from beating winners
            if any(kw_item in t for t in tags):
                score += 6
            if any(kw_item in r for r in rec):
                score += 5
            # Count description hits
            score += desc.count(kw_item) * 2

        # Arena bonus — heavily weighted, not just tiebreak
        arena = s.get("arena", {})
        arena_score = arena.get("score", 0)
        is_winner = arena.get("is_winner", False)
        arena_rank = arena.get("rank", 999)
        arena_cat = arena.get("category", "")
        a_scores = arena.get("scores", {})

        # Arena bonus — only applied when keyword relevance already established
        # (score > 0 = has keyword match; prevents winner bonus from firing on unrelated skills)
        if score > 0:
            # Winner bonus: only if skill has meaningful keyword relevance (>= 10pts)
            # Prevents unrelated winners from outranking relevant non-winners
            if is_winner and score >= 10:
                score += 15
            elif is_winner:
                score += 5  # small boost for marginal matches
            # Arena score bonus: 0-100 → 0-10 pts
            score += arena_score * 0.10
            # Quality dimension bonus
            score += a_scores.get("quality", 0) * 0.15
            score += a_scores.get("maintainability", 0) * 0.10
            # Category match bonus
            if any(kw_item in arena_cat for kw_item in kw):
                score += 4

        # Browse modes (--winners, --tag): no query terms → seed score from arena data
        no_query = not kw
        if no_query:
            score = arena_score * 0.10
            if is_winner:
                score += 15
            score += a_scores.get("quality", 0) * 0.15

        # Emit result if relevant (keyword hit) or browsing (no query)
        if score > 0:
            results.append({
                "id": s["id"],
                "path": path,
                "description": s.get("description", ""),
                "tags": s.get("tags", []),
                "arena_score": arena_score,
                "arena_rank": arena_rank,
                "arena_category": arena_cat,
                "quality_score": a_scores.get("quality", 0),
                "is_winner": is_winner,
                "match_score": round(score, 2),
            })

    results.sort(key=lambda x: -x["match_score"])
    return results[:limit]


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    idx = load_index()

    if args[0] == "--list-tags":
        tags = set()
        for s in idx["skills"]:
            tags.update(s.get("tags", []))
        print(json.dumps(sorted(tags), ensure_ascii=False, indent=2))
        return

    if args[0] == "--winners":
        results = search(idx, [], limit=50, winners_only=True)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    if args[0] == "--tag" and len(args) >= 2:
        results = search(idx, [], limit=30, tag_filter=args[1])
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    if args[0] == "--id" and len(args) >= 2:
        target = args[1].lower()
        skills = idx["skills"]
        match = next((s for s in skills if s["id"].lower() == target), None)
        if not match:
            # partial
            matches = [s for s in skills if target in s["id"].lower()]
            if len(matches) == 1:
                match = matches[0]
            elif matches:
                print(json.dumps([{"id": m["id"], "path": skill_path(m)} for m in matches[:5]]))
                return
        if match:
            print(json.dumps({"id": match["id"], "path": skill_path(match)}, ensure_ascii=False))
        else:
            print(json.dumps({"error": f"skill not found: {args[1]}"}))
        return

    # Default: keyword search
    results = search(idx, args)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
