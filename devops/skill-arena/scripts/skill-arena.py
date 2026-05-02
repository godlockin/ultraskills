#!/usr/bin/env python3
"""
Skill Arena - Main Entry Point

Usage:
    python skill-arena.py scan       # Scan all skills and cluster
    python skill-arena.py test       # Run PK tests (auto-detects changed clusters)
    python skill-arena.py report     # Generate benchmark report
    python skill-arena.py update     # Update index.json with ratings
    python skill-arena.py full       # Full pipeline
    python skill-arena.py backtrack  # Re-test all with new test cases
    python skill-arena.py diff       # Show which skills changed and affected clusters
"""

import argparse
import hashlib
import json
import sys
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables before anything else
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")  # Load from root only

# Import sub-modules
from cluster_skills import scan_skills, analyze_skills, cluster_skills
from design_tests import design_test_cases
from run_benchmarks import run_benchmarks
from score_results import score_and_rank
from generate_report import generate_report
from update_index import update_index_with_arena_data


# Project root is 4 levels up from this script (scripts -> skill-arena -> devops -> project root)
INDEX_JSON_PATH = PROJECT_ROOT / "index.json"
CLUSTERS_JSON_PATH = PROJECT_ROOT / "devops" / "skill-arena" / "clusters.json"
WINNERS_JSON_PATH = PROJECT_ROOT / "devops" / "skill-arena" / "winners.json"
REPORTS_DIR = PROJECT_ROOT / "devops" / "skill-arena" / "reports"
TEST_SUITES_DIR = PROJECT_ROOT / "devops" / "skill-arena" / "test-suites"
SKILL_SNAPSHOTS_PATH = PROJECT_ROOT / "devops" / "skill-arena" / "skill-snapshots.json"


# ─────────────────────────────────────────────
# Snapshot / diff helpers
# ─────────────────────────────────────────────

def _hash_skill(skill_path: Path) -> str:
    """SHA-1 of SKILL.md content (fast, good enough for change detection)."""
    try:
        content = skill_path.read_bytes()
        return hashlib.sha1(content).hexdigest()
    except Exception:
        return ""


def load_snapshots() -> dict:
    """Load saved skill hashes. Returns {skill_id: hash}."""
    if SKILL_SNAPSHOTS_PATH.exists():
        return json.loads(SKILL_SNAPSHOTS_PATH.read_text(encoding="utf-8"))
    return {}


def save_snapshots(snapshots: dict):
    SKILL_SNAPSHOTS_PATH.write_text(
        json.dumps(snapshots, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def build_current_snapshots() -> dict:
    """Walk clusters.json, compute hash for each skill's SKILL.md.

    NOTE: External/submodule skills (external/, community/ submodules) are
    hashed read-only — their source files are NEVER modified by this pipeline.
    Change detection here only triggers re-testing, never content edits.
    """
    if not CLUSTERS_JSON_PATH.exists():
        return {}
    clusters_data = json.loads(CLUSTERS_JSON_PATH.read_text(encoding="utf-8"))
    snapshots = {}
    for cluster in clusters_data.get("clusters", []):
        for skill in cluster.get("skills", []):
            sid = skill.get("id") if isinstance(skill, dict) else skill
            path_hint = skill.get("path", "") if isinstance(skill, dict) else ""
            skill_md = _find_skill_md(sid, path_hint)
            if skill_md:
                snapshots[sid] = _hash_skill(skill_md)
    return snapshots


def _find_skill_md(skill_id: str, path_hint: str = "") -> Path | None:
    """Resolve SKILL.md path for a skill."""
    # Try path hint first
    if path_hint:
        candidate = PROJECT_ROOT / path_hint.lstrip("./")
        if candidate.exists():
            return candidate
        # path_hint might point to directory
        candidate2 = candidate.parent / "SKILL.md" if candidate.name != "SKILL.md" else candidate
        if candidate2.exists():
            return candidate2
    # Fallback: search common locations
    for base in ["community", "engineering", "productivity", "creative", "devops", "external", "meta"]:
        for p in (PROJECT_ROOT / base).glob(f"**/{skill_id}/SKILL.md"):
            return p
    return None


def detect_changes(old_snapshots: dict, new_snapshots: dict) -> dict:
    """
    Compare old vs new snapshots.
    Returns:
        {
          "added":   [skill_id, ...],
          "changed": [skill_id, ...],
          "removed": [skill_id, ...],
        }
    """
    old_ids = set(old_snapshots)
    new_ids = set(new_snapshots)
    added   = sorted(new_ids - old_ids)
    removed = sorted(old_ids - new_ids)
    changed = sorted(
        sid for sid in old_ids & new_ids
        if old_snapshots[sid] != new_snapshots[sid]
    )
    return {"added": added, "changed": changed, "removed": removed}


def map_skills_to_clusters(skill_ids: list[str]) -> dict:
    """
    Returns {cluster_id: cluster_dict} for every cluster that contains
    at least one of the given skill_ids.
    """
    if not CLUSTERS_JSON_PATH.exists():
        return {}
    clusters_data = json.loads(CLUSTERS_JSON_PATH.read_text(encoding="utf-8"))
    affected = {}
    target = set(skill_ids)
    for cluster in clusters_data.get("clusters", []):
        cid = cluster["id"]
        for skill in cluster.get("skills", []):
            sid = skill.get("id") if isinstance(skill, dict) else skill
            if sid in target:
                affected[cid] = cluster
                break
    return affected


def get_affected_clusters(force_all: bool = False) -> tuple[list, bool]:
    """
    Determine which clusters need re-testing.

    Returns:
        (clusters_list, is_full_run)
        clusters_list: list of cluster dicts to test
        is_full_run:   True if running all 52, False if incremental
    """
    clusters_data = json.loads(CLUSTERS_JSON_PATH.read_text(encoding="utf-8"))
    all_clusters = clusters_data.get("clusters", [])

    if force_all:
        return all_clusters, True

    old_snapshots = load_snapshots()

    # No snapshot yet → full run
    if not old_snapshots:
        print("   📸 No snapshot found — running full test suite")
        return all_clusters, True

    new_snapshots = build_current_snapshots()
    changes = detect_changes(old_snapshots, new_snapshots)

    all_changed = changes["added"] + changes["changed"] + changes["removed"]
    if not all_changed:
        print("   ✅ No skill changes detected since last run")
        return [], False

    affected = map_skills_to_clusters(all_changed)
    if not affected:
        print("   ℹ️  Changed skills not found in any cluster — nothing to test")
        return [], False

    return list(affected.values()), False


# ─────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────

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

    # Save clusters with full skill data
    clusters_data = {
        "version": "1.0.0",
        "updated_at": "2026-03-09",
        "clusters": [
            {
                "id": c["id"],
                "name": c["name"],
                "description": c["description"],
                "skills": c["skills"],  # Keep full skill dicts, not just IDs
                "skill_count": len(c["skills"])
            }
            for c in clusters
        ]
    }

    with open(CLUSTERS_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(clusters_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Clusters saved to {CLUSTERS_JSON_PATH}")
    return clusters


def cmd_diff(args):
    """Show which skills changed and which clusters are affected."""
    print("🔍 Detecting skill changes...\n")

    old_snapshots = load_snapshots()
    if not old_snapshots:
        print("   ⚠️  No snapshot found. Run 'test' first to establish a baseline.")
        return

    new_snapshots = build_current_snapshots()
    changes = detect_changes(old_snapshots, new_snapshots)

    total = len(changes["added"]) + len(changes["changed"]) + len(changes["removed"])
    if total == 0:
        print("   ✅ No changes since last snapshot")
        return

    if changes["added"]:
        print(f"➕ Added ({len(changes['added'])}):")
        for s in changes["added"]:
            print(f"   {s}")
    if changes["changed"]:
        print(f"\n✏️  Changed ({len(changes['changed'])}):")
        for s in changes["changed"]:
            print(f"   {s}")
    if changes["removed"]:
        print(f"\n➖ Removed ({len(changes['removed'])}):")
        for s in changes["removed"]:
            print(f"   {s}")

    all_changed = changes["added"] + changes["changed"] + changes["removed"]
    affected = map_skills_to_clusters(all_changed)
    print(f"\n📦 Affected clusters ({len(affected)}):")
    for cid, cluster in affected.items():
        print(f"   {cluster['name']} ({cid})")


def cmd_test(args):
    """Run PK tests — incremental by default, full if --all."""
    force_all = getattr(args, 'all', False)
    parallel = not getattr(args, 'no_parallel', False)
    max_workers = getattr(args, 'workers', 4)
    use_llm = getattr(args, 'use_llm', False)
    llm_provider = getattr(args, 'provider', 'anthropic')

    # ── Determine which clusters to test ──
    print("🔍 Checking for skill changes...")
    clusters_to_test, is_full = get_affected_clusters(force_all=force_all)

    if not clusters_to_test:
        print("   Nothing to test.")
        return []

    if is_full:
        print(f"🏆 Full run: testing all {len(clusters_to_test)} clusters")
    else:
        # Show what changed
        old_snapshots = load_snapshots()
        new_snapshots = build_current_snapshots()
        changes = detect_changes(old_snapshots, new_snapshots)
        all_changed = changes["added"] + changes["changed"] + changes["removed"]
        print(f"   Skills changed: {len(all_changed)}")
        for label, lst in [("added", changes["added"]), ("changed", changes["changed"]), ("removed", changes["removed"])]:
            if lst:
                print(f"   {'➕' if label=='added' else '✏️ ' if label=='changed' else '➖'} {label}: {', '.join(lst)}")
        print(f"\n🏆 Incremental run: testing {len(clusters_to_test)} affected cluster(s)")
        for c in clusters_to_test:
            print(f"   📦 {c['name']} ({c['id']})")

    print()

    # ── Load existing raw results (to merge incremental) ──
    results_path = REPORTS_DIR / "raw-results.json"
    existing_results = []
    if results_path.exists() and not is_full:
        try:
            existing_data = json.loads(results_path.read_text(encoding="utf-8"))
            existing_results = existing_data.get("results", [])
            # Remove stale results for clusters we're about to re-test
            retesting_cluster_ids = {c["id"] for c in clusters_to_test}
            existing_results = [
                r for r in existing_results
                if r.get("cluster_id") not in retesting_cluster_ids
            ]
            print(f"   ♻️  Kept {len(existing_results)} existing results from other clusters\n")
        except Exception:
            existing_results = []

    # ── Run tests ──
    new_results = []
    for cluster in clusters_to_test:
        print(f"📦 Testing cluster: {cluster['name']} ({cluster['id']})")

        # Design test cases if not exists
        test_suite_path = TEST_SUITES_DIR / cluster["name"] / "tests.yaml"
        if not test_suite_path.exists():
            print(f"   🧠 Designing test cases with expert panel...")
            design_test_cases(cluster, TEST_SUITES_DIR)

        # Run benchmarks
        print(f"   ⚡ Running benchmarks (parallel={parallel}, workers={max_workers}, llm={use_llm})...")
        cluster_results = run_benchmarks(
            cluster, TEST_SUITES_DIR,
            parallel=parallel, max_workers=max_workers,
            use_llm=use_llm, llm_provider=llm_provider
        )
        # Tag results with cluster_id for future incremental merging
        for r in cluster_results:
            r["cluster_id"] = cluster["id"]
        new_results.extend(cluster_results)

    # ── Merge + save ──
    all_results = existing_results + new_results
    results_path.write_text(
        json.dumps({"results": all_results}, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"\n✅ Test results saved to {results_path}")
    print(f"   Total: {len(all_results)} results ({len(new_results)} new, {len(existing_results)} retained)")

    # ── Update snapshot after successful test ──
    new_snapshots = build_current_snapshots()
    save_snapshots(new_snapshots)
    print(f"   📸 Snapshot updated ({len(new_snapshots)} skills)")

    return all_results


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
        "updated_at": datetime.now().strftime("%Y-%m-%d"),
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
    args.all = True  # Force full test
    cmd_scan(args)
    cmd_test(args)
    cmd_score(args)
    cmd_report(args)
    cmd_update(args)
    print("\n🎉 Full pipeline completed!")


def cmd_backtrack(args):
    """Re-test all skills with updated test cases."""
    print("🔄 Backtracking: Re-testing all skills with new test cases...")
    # Delete all test suites to force regeneration
    import shutil
    if TEST_SUITES_DIR.exists():
        for suite in TEST_SUITES_DIR.iterdir():
            if suite.is_dir():
                shutil.rmtree(suite)
        print(f"   🗑️  Cleared all test suites in {TEST_SUITES_DIR}")
    # Force full run
    args.all = True
    cmd_test(args)
    cmd_score(args)
    cmd_report(args)
    cmd_update(args)
    print("\n🎉 Backtrack completed!")


def main():
    parser = argparse.ArgumentParser(
        description="Skill Arena - Benchmark and rank AI skills"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Scan command
    scan_parser = subparsers.add_parser("scan", help="Scan and cluster skills")
    scan_parser.set_defaults(func=cmd_scan)

    # Diff command
    diff_parser = subparsers.add_parser("diff", help="Show changed skills and affected clusters")
    diff_parser.set_defaults(func=cmd_diff)

    # Test command
    test_parser = subparsers.add_parser("test", help="Run PK tests (incremental by default)")
    test_parser.add_argument("--all", action="store_true", help="Force full run (ignore change detection)")
    test_parser.add_argument("--no-parallel", action="store_true", help="Disable parallel execution")
    test_parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers")
    test_parser.add_argument("--use-llm", action="store_true", help="Use actual LLM invocation (requires API key)")
    test_parser.add_argument("--provider", type=str, default="anthropic", help="LLM provider (anthropic, openai, google)")
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
    full_parser.add_argument("--no-parallel", action="store_true", help="Disable parallel execution")
    full_parser.add_argument("--workers", type=int, default=4, help="Number of parallel workers")
    full_parser.add_argument("--use-llm", dest="use_llm", action="store_true", help="Use actual LLM invocation")
    full_parser.add_argument("--provider", type=str, default="anthropic", help="LLM provider")
    full_parser.set_defaults(func=cmd_full)

    # Backtrack command
    backtrack_parser = subparsers.add_parser("backtrack", help="Re-test all with new test cases")
    backtrack_parser.add_argument("--no-parallel", action="store_true")
    backtrack_parser.add_argument("--workers", type=int, default=4)
    backtrack_parser.add_argument("--use-llm", dest="use_llm", action="store_true")
    backtrack_parser.add_argument("--provider", type=str, default="anthropic")
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
