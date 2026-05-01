#!/usr/bin/env python3
"""
arena_build_index.py - 重建 index.json（全量 skills + arena scores）

输入:  skill-arena/skills_inventory.json, scores.json, clusters.json
输出: index.json (覆盖写入)
"""

import json
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
ARENA_DIR = ROOT / "skill-arena"


def main():
    inventory  = json.loads((ARENA_DIR / "skills_inventory.json").read_text())
    scores_raw = json.loads((ARENA_DIR / "scores.json").read_text())
    clusters   = json.loads((ARENA_DIR / "clusters.json").read_text())

    # id -> score entry
    score_map = {s["id"]: s for s in scores_raw}

    # cluster_id -> cluster entry
    cluster_map = {c["id"]: c for c in clusters}

    # 构建 skills 列表（按 cluster 分组，cluster 内按分数降序）
    skills_out = []
    for s in inventory:
        sid = s["id"]
        sc  = score_map.get(sid, {})
        cid = sc.get("cluster", "misc")
        c   = cluster_map.get(cid, {})

        entry = {
            "id":          sid,
            "name":        sid,
            "path":        s["path"],
            "description": s["description"],
            "tags":        s.get("tags") or [],
            "arena": {
                "cluster":          cid,
                "cluster_name":     c.get("name", cid),
                "score":            sc.get("total", 0),
                "doc_quality":      sc.get("doc_quality", 0),
                "func_clarity":     sc.get("func_clarity", 0),
                "maintainability":  sc.get("maintainability", 0),
                "is_winner":        sc.get("is_winner", False),
                "rank":             0,          # 填充下面
                "test_date":        str(date.today()),
                "test_version":     "1.0.0",
            },
        }
        if s.get("version"):
            entry["version"] = s["version"]
        if s.get("github_url"):
            entry["github_url"] = s["github_url"]

        skills_out.append(entry)

    # 在每个 cluster 内部设置 rank（1 = winner）
    from collections import defaultdict
    cluster_members = defaultdict(list)
    for e in skills_out:
        cluster_members[e["arena"]["cluster"]].append(e)

    for cid, members in cluster_members.items():
        members.sort(key=lambda x: x["arena"]["score"], reverse=True)
        for i, m in enumerate(members):
            m["arena"]["rank"] = i + 1

    # 全局按 (cluster, rank) 排序，保证输出有序
    skills_out.sort(key=lambda x: (x["arena"]["cluster"], x["arena"]["rank"]))

    # 统计
    winners     = [s for s in skills_out if s["arena"]["is_winner"]]
    avg_score   = sum(s["arena"]["score"] for s in skills_out) / len(skills_out)
    cluster_cnt = len(cluster_map)

    # 构建 index.json
    index = {
        "meta": {
            "version":           "2.0.0",
            "updated_at":        str(date.today()),
            "arena_version":     "1.0.0",
            "arena_updated_at":  str(date.today()),
            "total_skills":      len(skills_out),
            "total_clusters":    cluster_cnt,
            "avg_arena_score":   round(avg_score, 2),
            "total_winners":     len(winners),
        },
        "skills": skills_out,
    }

    out_path = ROOT / "index.json"
    out_path.write_text(json.dumps(index, ensure_ascii=False, indent=2))

    print(f"✅ index.json written: {len(skills_out)} skills, {cluster_cnt} clusters")
    print(f"   avg score: {avg_score:.2f} | winners: {len(winners)}")
    print(f"\nTop winners by cluster:")
    winners_sorted = sorted(winners, key=lambda x: x["arena"]["score"], reverse=True)
    for w in winners_sorted[:20]:
        print(f"  {w['arena']['score']:4.1f}  {w['id']:<45} [{w['arena']['cluster_name']}]")


if __name__ == "__main__":
    from pipeline_lock import PipelineLock
    with PipelineLock("arena_build_index"):
        main()
