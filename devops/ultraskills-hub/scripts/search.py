#!/usr/bin/env python3
"""
ultraskills search — find relevant skills by keyword/intent.

Usage:
  search.py <query terms...>
  search.py --tag <tag>
  search.py --list-tags
  search.py --id <skill-id>        # exact lookup, returns path
  search.py --winners              # list arena winners only
  search.py --compare <skill-id-a> <skill-id-b>  # side-by-side comparison
  search.py --cluster <cluster-id> # list skills in a cluster
  search.py --clusters             # list all clusters with metadata
  search.py --hierarchy            # show category tree
  search.py --related <cluster-id> # show related clusters

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


def levenshtein(a, b):
    """Pure-Python Levenshtein edit distance."""
    if len(a) < len(b):
        return levenshtein(b, a)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (ca != cb)))
        prev = curr
    return prev[-1]


def chinese_bigrams(text):
    """Split Chinese text into character bigrams for matching."""
    chars = [c for c in text if '一' <= c <= '鿿']
    if len(chars) < 2:
        return []
    return [chars[i] + chars[i + 1] for i in range(len(chars) - 1)]


def has_chinese(text):
    return bool(re.search(r'[一-鿿]', text))


def expand_query_terms(query_terms):
    """Expand query terms with Chinese bigrams where applicable."""
    expanded = []
    for t in query_terms:
        expanded.append(t.lower())
        if has_chinese(t):
            expanded.extend(chinese_bigrams(t))
    return expanded


def fuzzy_suggest(idx, query_terms, top_n=3):
    """Return top-N closest skill ids by edit distance for 'did you mean' suggestions."""
    query = " ".join(query_terms).lower()
    scored = []
    for s in idx["skills"]:
        sid = s["id"].lower()
        dist = levenshtein(query, sid)
        scored.append((dist, s["id"]))
    scored.sort(key=lambda x: x[0])
    return scored[:top_n]


_REPAIR_CMD = (
    "python3 scripts/arena_scan.py && "
    "python3 scripts/arena_cluster_score.py && "
    "python3 scripts/arena_build_index.py"
)


def _validate_index(data):
    """Validate index.json structure. Exits on failure."""
    errors = []
    if not isinstance(data, dict):
        errors.append("top-level value is not an object")
    else:
        if "version" not in data and "meta" not in data:
            errors.append("missing required key 'version' or 'meta'")
        if "skills" not in data:
            errors.append("missing required key 'skills'")
        elif not isinstance(data["skills"], list) or len(data["skills"]) == 0:
            errors.append("'skills' must be a non-empty list")
    if errors:
        print(f"❌ index.json is corrupted or incomplete ({'; '.join(errors)}). Run:")
        print(f"   {_REPAIR_CMD}")
        sys.exit(1)


def load_index():
    if not os.path.exists(INDEX_FILE):
        print(json.dumps({"error": f"index.json not found at {INDEX_FILE}"}))
        sys.exit(1)
    with open(INDEX_FILE, encoding="utf-8") as f:
        try:
            data = json.load(f)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"❌ index.json is corrupted or incomplete (invalid JSON: {e}). Run:")
            print(f"   {_REPAIR_CMD}")
            sys.exit(1)
    _validate_index(data)
    return data


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
    kw = []
    for t in query_terms:
        kw.extend(t.lower().split())
        # Chinese bigram expansion
        if has_chinese(t):
            kw.extend(chinese_bigrams(t))

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

        # Fuzzy match on skill id: only when no exact/partial match found
        if score == 0 and kw:
            for kw_item in kw:
                if levenshtein(kw_item, sid) <= 2:
                    score += 8
                    break

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
            if is_winner and arena_cat:
                rank_label = f"#{arena_rank} in {arena_cat} category" if arena_rank and arena_rank < 999 else f"winner in {arena_cat} category"
                winner_reason = f"{rank_label}, arena score {arena_score}"
            else:
                winner_reason = None

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
                "winner_reason": winner_reason,
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

    if args[0] == "--clusters":
        cmd_clusters(idx)
        return

    if args[0] == "--cluster" and len(args) >= 2:
        cmd_cluster_skills(idx, args[1])
        return

    if args[0] == "--hierarchy":
        cmd_hierarchy(idx)
        return

    if args[0] == "--related" and len(args) >= 2:
        cmd_related(idx, args[1])
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

    if args[0] == "--compare" and len(args) >= 3:
        def get_skill_by_id(idx, target):
            skills = idx["skills"]
            target = target.lower()
            match = next((s for s in skills if s["id"].lower() == target), None)
            if not match:
                matches = [s for s in skills if target in s["id"].lower()]
                if len(matches) == 1:
                    match = matches[0]
            return match

        sa = get_skill_by_id(idx, args[1])
        sb = get_skill_by_id(idx, args[2])
        if not sa:
            print(json.dumps({"error": f"skill not found: {args[1]}"}))
            return
        if not sb:
            print(json.dumps({"error": f"skill not found: {args[2]}"}))
            return

        def arena_scores(s):
            a = s.get("arena", {})
            scores = a.get("scores", {})
            return {
                "total": a.get("score", 0),
                "speed": scores.get("speed", 0),
                "quality": scores.get("quality", 0),
                "maintainability": scores.get("maintainability", 0),
                "is_winner": a.get("is_winner", False),
                "rank": a.get("rank", 999),
                "category": a.get("category", ""),
            }

        aa = arena_scores(sa)
        ab = arena_scores(sb)

        dims = ["speed", "quality", "maintainability", "total"]
        winner_id = sa["id"] if aa["total"] >= ab["total"] else sb["id"]

        comparison = {
            "skill_a": {"id": sa["id"], "description": sa.get("description", ""), "path": skill_path(sa), **aa},
            "skill_b": {"id": sb["id"], "description": sb.get("description", ""), "path": skill_path(sb), **ab},
            "winner": winner_id,
            "dimension_winners": {
                dim: (sa["id"] if aa[dim] >= ab[dim] else sb["id"]) for dim in dims
            },
            "score_delta": round(aa["total"] - ab["total"], 2),
        }
        print(json.dumps(comparison, ensure_ascii=False, indent=2))
        return

    # Default: keyword search
    results = search(idx, args)
    if not results:
        suggestions = fuzzy_suggest(idx, args, top_n=3)
        output = {
            "results": [],
            "did_you_mean": [s[1] for s in suggestions]
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))


def cmd_clusters(idx):
    """List all clusters with metadata (sorted by skill_count desc)."""
    clusters = idx.get("clusters", [])
    if not clusters:
        print(json.dumps({"error": "no clusters in index (v2.1.0+ required)"}))
        return
    # 简化输出，移除空字段
    out = []
    for c in clusters:
        entry = {
            "id": c["id"],
            "name": c["name"],
            "skill_count": c["skill_count"],
            "winner": c.get("winner"),
        }
        if c.get("description"):
            entry["description"] = c["description"]
        if c.get("triggers"):
            entry["triggers"] = c["triggers"][:5]  # 前5个触发词
        if c.get("parent"):
            entry["parent"] = c["parent"]
        out.append(entry)
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_cluster_skills(idx, cluster_id):
    """List skills in a specific cluster."""
    skills = idx["skills"]
    cluster_id = cluster_id.lower()
    matches = [s for s in skills if s.get("arena", {}).get("cluster", "").lower() == cluster_id]
    if not matches:
        # fuzzy match cluster name
        clusters = idx.get("clusters", [])
        possible = [c for c in clusters if cluster_id in c["id"].lower() or cluster_id in c.get("name", "").lower()]
        if possible:
            print(json.dumps({"error": f"cluster '{cluster_id}' not found", "did_you_mean": [c["id"] for c in possible[:5]]}))
        else:
            print(json.dumps({"error": f"cluster '{cluster_id}' not found"}))
        return

    matches.sort(key=lambda x: x.get("arena", {}).get("rank", 999))
    out = []
    for s in matches:
        arena = s.get("arena", {})
        out.append({
            "id": s["id"],
            "description": s.get("description", "")[:100],
            "arena_score": arena.get("score", 0),
            "rank": arena.get("rank", 999),
            "is_winner": arena.get("is_winner", False),
        })
    print(json.dumps(out, ensure_ascii=False, indent=2))


def cmd_hierarchy(idx):
    """Show category hierarchy tree."""
    hierarchy = idx.get("hierarchy", {})
    if not hierarchy:
        print(json.dumps({"error": "no hierarchy in index (v2.1.0+ required)"}))
        return

    clusters = {c["id"]: c for c in idx.get("clusters", [])}

    # 层级只有两层：root -> clusters，不需要递归
    tree = []
    for root_id in hierarchy.get("root", []):
        child_ids = hierarchy.get(root_id, [])
        children = []
        for child_id in child_ids:
            c = clusters.get(child_id, {})
            children.append({
                "id": child_id,
                "name": c.get("name", child_id),
                "skill_count": c.get("skill_count", 0),
                "winner": c.get("winner"),
            })
        # 按 skill_count 降序
        children.sort(key=lambda x: x["skill_count"], reverse=True)
        total = sum(ch["skill_count"] for ch in children)
        tree.append({
            "id": root_id,
            "name": root_id.title(),
            "total_skills": total,
            "cluster_count": len(children),
            "children": children,
        })
    # 按 total_skills 降序
    tree.sort(key=lambda x: x["total_skills"], reverse=True)
    print(json.dumps(tree, ensure_ascii=False, indent=2))


def cmd_related(idx, cluster_id):
    """Show related clusters for a given cluster."""
    clusters = {c["id"]: c for c in idx.get("clusters", [])}
    cluster_id = cluster_id.lower()
    c = clusters.get(cluster_id)
    if not c:
        possible = [cid for cid in clusters if cluster_id in cid.lower()]
        if possible:
            print(json.dumps({"error": f"cluster '{cluster_id}' not found", "did_you_mean": possible[:5]}))
        else:
            print(json.dumps({"error": f"cluster '{cluster_id}' not found"}))
        return

    related_ids = c.get("related", [])
    parent_id = c.get("parent")

    out = {
        "cluster": {"id": c["id"], "name": c["name"], "description": c.get("description", "")},
        "parent": clusters.get(parent_id, {"id": parent_id}) if parent_id else None,
        "related": [{"id": rid, "name": clusters.get(rid, {}).get("name", rid), "skill_count": clusters.get(rid, {}).get("skill_count", 0)} for rid in related_ids if rid in clusters],
        "suitable_for": c.get("suitable_for", []),
        "not_suitable_for": c.get("not_suitable_for", []),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
