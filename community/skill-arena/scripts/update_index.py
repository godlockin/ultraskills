#!/usr/bin/env python3
"""
Index Updater Module

Updates index.json with arena data (rankings, scores, recommended_for tags).
"""

import json
from pathlib import Path
from typing import Dict, Any


def update_index_with_arena_data(index_path: Path, winners_data: Dict, rankings: Dict):
    """
    Update index.json with arena benchmark data.

    Adds to each skill:
    - arena.rank: Ranking in category
    - arena.score: Total score
    - arena.scores: Breakdown by dimension
    - arena.is_winner: Whether this skill is the category winner
    - recommended_for: List of use cases this skill is best suited for
    - priority: Priority level (1=highest, based on ranking)
    """
    with open(index_path, 'r', encoding='utf-8') as f:
        index_data = json.load(f)

    # Build lookup maps
    winner_map = {}  # skill_id -> winner info
    for winner in winners_data.get("winners", []):
        winner_map[winner["skill_id"]] = winner

    skill_rank_map = {}  # skill_id -> rank info
    for category in rankings.get("categories", []):
        for rank, skill in enumerate(category.get("skills", []), 1):
            skill_rank_map[skill["skill_id"]] = {
                "rank": rank,
                "category": category["category"],
                "scores": skill.get("scores", {}),
                "total_score": skill.get("total_score", 0)
            }

    # Update skills
    for skill in index_data.get("skills", []):
        skill_id = skill.get("id", "")

        # Add arena data if skill was tested
        if skill_id in skill_rank_map:
            rank_info = skill_rank_map[skill_id]
            is_winner = skill_id in winner_map

            skill["arena"] = {
                "rank": rank_info["rank"],
                "category": rank_info["category"],
                "score": rank_info["total_score"],
                "scores": rank_info["scores"],
                "is_winner": is_winner,
                "test_date": "2026-03-09",
                "test_version": "1.0.0"
            }

            # Add priority based on ranking
            if rank_info["rank"] == 1:
                skill["priority"] = 1  # Highest priority
            elif rank_info["rank"] <= 3:
                skill["priority"] = 2  # High priority
            else:
                skill["priority"] = 3  # Standard priority

            # Add recommended_for based on category
            skill["recommended_for"] = generate_recommended_for(
                skill_id, rank_info["category"], is_winner
            )

        # Ensure tags include arena info if winner
        if skill_id in winner_map:
            if "tags" not in skill:
                skill["tags"] = []
            if "arena-winner" not in skill["tags"]:
                skill["tags"].append("arena-winner")

    # Update metadata
    index_data["meta"]["arena_version"] = "1.0.0"
    index_data["meta"]["arena_updated_at"] = "2026-03-09"

    # Write back
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)


def generate_recommended_for(skill_id: str, category: str, is_winner: bool) -> list:
    """Generate recommended use cases based on category."""

    templates = {
        "cro": ["landing-page-review", "conversion-audit", "cro-consultation"],
        "seo": ["seo-audit", "content-optimization", "technical-seo-review"],
        "content": ["content-creation", "copy-review", "content-strategy"],
        "marketing": ["marketing-strategy", "campaign-planning", "ad-creative-review"],
        "engineering": ["code-review", "architecture-review", "debugging-help"],
        "product": ["product-strategy", "ux-review", "feature-planning"],
        "devops": ["deployment-help", "ci-cd-setup", "infrastructure-review"],
    }

    base_recommendations = templates.get(category, [f"{category}-related-tasks"])

    if is_winner:
        # Winners get broader recommendations
        return [f"best-{category}-skill"] + base_recommendations
    return base_recommendations
