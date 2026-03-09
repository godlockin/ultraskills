#!/usr/bin/env python3
"""
Scoring and Ranking Module

Calculates weighted scores and generates rankings.
"""

from typing import Dict, Any, List


def score_and_rank(results: List[Dict]) -> Dict:
    """
    Score all skills and generate rankings.

    Scoring formula:
    Total = (Speed × 0.30) + (Quality × 0.50) + (Maintainability × 0.20)
    """
    rankings = {
        "categories": [],
        "overall": []
    }

    # Group results by cluster
    clusters = {}
    for result in results:
        cluster_name = result["cluster_name"]
        if cluster_name not in clusters:
            clusters[cluster_name] = []
        clusters[cluster_name].append(result)

    # Score each cluster
    for cluster_name, cluster_results in clusters.items():
        scored_skills = []

        for result in cluster_results:
            scores = calculate_scores(result)
            scored_skills.append({
                "skill_id": result["skill_id"],
                "skill_name": result["skill_name"],
                "scores": scores,
                "total_score": scores["total"]
            })

        # Sort by total score
        scored_skills.sort(key=lambda x: x["total_score"], reverse=True)

        rankings["categories"].append({
            "category": cluster_name,
            "skills": scored_skills,
            "winner": scored_skills[0] if scored_skills else None
        })

        # Add to overall
        for skill in scored_skills:
            rankings["overall"].append({
                **skill,
                "category": cluster_name
            })

    # Sort overall
    rankings["overall"].sort(key=lambda x: x["total_score"], reverse=True)

    return rankings


def calculate_scores(result: Dict) -> Dict[str, float]:
    """
    Calculate weighted scores for a skill.

    Returns:
    {
        "speed": 0-30,
        "quality": 0-50,
        "maintainability": 0-20,
        "total": 0-100
    }
    """
    test_results = result.get("test_results", [])

    if not test_results:
        return {"speed": 0, "quality": 0, "maintainability": 0, "total": 0}

    # Calculate speed score (30 points max)
    avg_response_time = sum(r.get("response_time_s", 10) for r in test_results) / len(test_results)
    speed_score = max(0, 30 - (avg_response_time * 2))  # Faster = higher score

    # Calculate quality score (50 points max)
    avg_quality = sum(r.get("quality_score", 5) for r in test_results) / len(test_results)
    quality_score = (avg_quality / 10) * 50  # Normalize to 50

    # Calculate maintainability score (20 points max)
    # In production, analyze code structure, documentation, etc.
    maintainability_score = 15  # Default placeholder

    total = speed_score + quality_score + maintainability_score

    return {
        "speed": round(speed_score, 2),
        "quality": round(quality_score, 2),
        "maintainability": round(maintainability_score, 2),
        "total": round(total, 2)
    }
