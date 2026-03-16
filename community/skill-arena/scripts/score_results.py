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

    # Aggregate scores from all test results
    total_speed = 0
    total_quality = 0
    total_maintainability = 0

    for test_result in test_results:
        # Use scoring_breakdown if available (from test execution)
        scoring = test_result.get("scoring_breakdown", {})

        speed = scoring.get("speed", 0)
        quality = scoring.get("quality", 0)
        maintainability = scoring.get("maintainability", 0)

        # Fallback: calculate from raw metrics if scoring_breakdown not available
        if speed == 0 and quality == 0 and maintainability == 0:
            # Calculate speed from response time
            response_time = test_result.get("response_time_s", 10)
            speed = max(0, 30 - (response_time * 2))

            # Calculate quality from quality_score (0-10 scale)
            quality_score = test_result.get("quality_score", 5)
            quality = (quality_score / 10) * 50

            # Default maintainability
            maintainability = 15

        total_speed += speed
        total_quality += quality
        total_maintainability += maintainability

    # Average across all tests
    num_tests = len(test_results)
    avg_speed = total_speed / num_tests
    avg_quality = total_quality / num_tests
    avg_maintainability = total_maintainability / num_tests

    total = avg_speed + avg_quality + avg_maintainability

    return {
        "speed": round(avg_speed, 2),
        "quality": round(avg_quality, 2),
        "maintainability": round(avg_maintainability, 2),
        "total": round(total, 2)
    }
