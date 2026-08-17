#!/usr/bin/env python3
"""Generate human-readable SKILLS_INDEX.md from index.json."""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
index = json.loads((ROOT / "index.json").read_text(encoding="utf-8"))
meta = index.get("meta", {})
clusters = defaultdict(list)
for skill in index.get("skills", []):
    arena = skill.get("arena", {})
    clusters[(arena.get("cluster", "misc"), arena.get("cluster_name", "misc"))].append(skill)

lines = [
    "# UltraSkills Index (Auto-generated)",
    f"**Total Skills**: {meta.get('total_skills', len(index.get('skills', [])))}",
    f"**Total Clusters**: {meta.get('total_clusters', len(clusters))}",
    f"**Average Score**: {meta.get('avg_arena_score', 0):.2f}/10",
    f"**Last Updated**: {meta.get('updated_at', '')}",
    "", "---", "",
]
for (_, name), skills in sorted(clusters.items(), key=lambda item: item[0][1]):
    skills.sort(key=lambda skill: skill.get("arena", {}).get("rank", 0))
    lines.extend([f"## {name} ({len(skills)} skills)", "", "| Rank | Skill | Score | Path |", "|------|-------|-------|------|"])
    for skill in skills:
        arena = skill.get("arena", {})
        lines.append(f"| {arena.get('rank', '')} | {skill['id']} | {arena.get('score', 0):.1f} | `{skill['path']}` |")
    lines.append("")
(ROOT / "SKILLS_INDEX.md").write_text("\n".join(lines), encoding="utf-8")
print(f"Generated SKILLS_INDEX.md: {len(index.get('skills', []))} skills, {len(clusters)} clusters")
