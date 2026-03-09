#!/usr/bin/env python3
"""
Skill Arena - Main Entry Point

Usage:
    python skill-arena.py scan       # Scan all skills and cluster
    python skill-arena.py test       # Run PK tests
    python skill-arena.py report     # Generate benchmark report
    python skill-arena.py update     # Update index.json with ratings
    python skill-arena.py full       # Full pipeline
    python skill-arena.py backtrack  # Re-test all with new test cases
"""

import argparse
import json
import sys
from pathlib import Path

# Import sub-modules
from cluster_skills import scan_skills, analyze_skills, cluster_skills
from design_tests import design_test_cases
from run_benchmarks import run_benchmarks
from score_results import score_and_rank
from generate_report import generate_report
from update_index import update_index_with_arena_data


# Project root is 3 levels up from this script (scripts -> skill-arena -> devops -> project root)
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
INDEX_JSON_PATH = PROJECT_ROOT / "index.json"
CLUSTERS_JSON_PATH = PROJECT_ROOT / "devops" / "skill-arena" / "clusters.json"
WINNERS_JSON_PATH = PROJECT_ROOT / "devops" / "skill-arena" / "winners.json"
REPORTS_DIR = PROJECT_ROOT / "devops" / "skill-arena" / "reports"
TEST_SUITES_DIR = PROJECT_ROOT / "devops" / "skill-arena" / "test-suites"


def cmd_scan(args):
    """Scan all skills and perform clustering."""
    print("🔍 Scanning project for skills...")
    skills = scan_skills(PROJECT_ROOT)
    print(f"   Found {len(skills)} skills")

    print("\n🧠 Analyzing skill semantics...")
    analyzed = analyze_skills(skills, PROJECT_ROOT)

    print("\n📊 Clustering similar skills...")
    clusters = cluster_skills(analyzed)
    print(f"   Created {len(clusters)} clusters")

    # Save clusters
    clusters_data = {
        "version": "1.0.0",
        "updated_at": "2026-03-09",
        "clusters": [
            {
                "id": c["id"],
                "name": c["name"],
                "description": c["description"],
                "skills": [s["id"] for s in c["skills"]],
                "skill_count": len(c["skills"])
            }
            for c in clusters
        ]
    }

    with open(CLUSTERS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(clusters_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Clusters saved to {CLUSTERS_JSON_PATH}")
    return clusters


def cmd_test(args):
    """Run PK tests for clusters."""
    print("🏆 Running PK tests...")

    # Load clusters
    with open(CLUSTERS_JSON_PATH, 'r', encoding='utf-8') as f:
        clusters_data = json.load(f)

    parallel = not getattr(args, 'no_parallel', False)
    max_workers = getattr(args, 'workers', 4)

    results = []
    for cluster in clusters_data["clusters"]:
        print(f"\n📦 Testing cluster: {cluster['name']} ({cluster['id']})")

        # Design test cases if not exists
        test_suite_path = TEST_SUITES_DIR / cluster["name"] / "tests.yaml"
        if not test_suite_path.exists():
            print(f"   🧠 Designing test cases with expert panel...")
            design_test_cases(cluster, TEST_SUITES_DIR)

        # Run benchmarks
        print(f"   ⚡ Running benchmarks (parallel={parallel}, workers={max_workers})...")
        cluster_results = run_benchmarks(cluster, TEST_SUITES_DIR, parallel=parallel, max_workers=max_workers)
        results.extend(cluster_results)

    # Save raw results
    results_path = REPORTS_DIR / "raw-results.json"
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump({"results": results}, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Test results saved to {results_path}")
    return results


def cmd_score(args):
    """Score and rank skills."""
    print("📊 Scoring and ranking...")

    # Load raw results
    results_path = REPORTS_DIR / "raw-results.json"
    with open(results_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    rankings = score_and_rank(data["results"])

    # Save rankings
    rankings_path = REPORTS_DIR / "rankings.json"
    with open(rankings_path, 'w', encoding='utf-8') as f:
        json.dump(rankings, f, indent=2, ensure_ascii=False)

    # Update winners
    winners = {
        "version": "1.0.0",
        "updated_at": "2026-03-09",
        "winners": [
            {
                "category": cat["category"],
                "skill_id": cat["winner"]["skill_id"],
                "score": cat["winner"]["total_score"],
                "scores": cat["winner"]["scores"],
                "defeated": [s["skill_id"] for s in cat["skills"][1:]]
            }
            for cat in rankings["categories"]
        ]
    }

    with open(WINNERS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(winners, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Winners saved to {WINNERS_JSON_PATH}")
    return rankings


def cmd_report(args):
    """Generate benchmark report."""
    print("📝 Generating benchmark report...")

    # Load rankings
    rankings_path = REPORTS_DIR / "rankings.json"
    with open(rankings_path, 'r', encoding='utf-8') as f:
        rankings = json.load(f)

    report_path = generate_report(rankings, REPORTS_DIR)
    print(f"\n✅ Report generated: {report_path}")
    return report_path


def cmd_update(args):
    """Update index.json with arena data."""
    print("🔄 Updating index.json...")

    # Load winners
    with open(WINNERS_JSON_PATH, 'r', encoding='utf-8') as f:
        winners_data = json.load(f)

    # Load rankings
    rankings_path = REPORTS_DIR / "rankings.json"
    with open(rankings_path, 'r', encoding='utf-8') as f:
        rankings = json.load(f)

    update_index_with_arena_data(INDEX_JSON_PATH, winners_data, rankings)
    print(f"\n✅ index.json updated")


def cmd_full(args):
    """Run full pipeline."""
    cmd_scan(args)
    cmd_test(args)
    cmd_score(args)
    cmd_report(args)
    cmd_update(args)
    print("\n🎉 Full pipeline completed!")


def cmd_backtrack(args):
    """Re-test all skills with updated test cases."""
    print("🔄 Backtracking: Re-testing all skills with new test cases...")
    # For now, just run full pipeline
    # In production, this would load new test cases and re-run
    cmd_full(args)


def main():
    parser = argparse.ArgumentParser(
        description="Skill Arena - Benchmark and rank AI skills"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan and cluster skills")
    scan_parser.set_defaults(func=cmd_scan)

    # Test command
    test_parser = subparsers.add_parser("test", help="Run PK tests")
    test_parser.add_argument("--no-parallel", action="store_true", help="Disable parallel execution")
    test_parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers")
    test_parser.set_defaults(func=cmd_test)

    # Score command
    score_parser = subparsers.add_parser("score", help="Score and rank skills")
    score_parser.set_defaults(func=cmd_score)

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate benchmark report")
    report_parser.set_defaults(func=cmd_report)

    # Update command
    update_parser = subparsers.add_parser("update", help="Update index.json")
    update_parser.set_defaults(func=cmd_update)

    # Full command
    full_parser = subparsers.add_parser("full", help="Run full pipeline")
    full_parser.set_defaults(func=cmd_full)

    # Backtrack command
    backtrack_parser = subparsers.add_parser("backtrack", help="Re-test all with new test cases")
    backtrack_parser.set_defaults(func=cmd_backtrack)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    # Ensure directories exist
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    TEST_SUITES_DIR.mkdir(parents=True, exist_ok=True)

    args.func(args)


if __name__ == "__main__":
    main()
