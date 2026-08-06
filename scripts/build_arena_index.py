#!/usr/bin/env python3
"""
build_arena_index.py — run the 3-stage arena pipeline as a single command.

Stage 1: arena_scan.py         → skill-arena/skills_inventory.json
Stage 2: arena_cluster_score.py → clusters + scores + winners
Stage 3: arena_build_index.py  → index.json (the public search index)

Each stage is a separate script kept in scripts/ for granular usage.
This wrapper is the single entry point for `--update-arena`.

Usage:
  python3 scripts/build_arena_index.py             # full rebuild
  python3 scripts/build_arena_index.py --stage 1   # scan only
  python3 scripts/build_arena_index.py --stage 1,2 # scan + cluster
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"

STAGES = [
    (1, "arena_scan.py", "scan SKILL.md tree"),
    (2, "arena_cluster_score.py", "cluster + score + winners"),
    (3, "arena_build_index.py", "merge to index.json"),
]


def run(stage_num: int) -> int:
    script_name, desc = STAGES[stage_num - 1][1], STAGES[stage_num - 1][2]
    script = SCRIPTS_DIR / script_name
    print(f"  [stage {stage_num}] {script_name} — {desc}")
    env = os.environ.copy()
    env["ULTRASKILLS_PIPELINE_LOCK_HELD"] = "1"
    r = subprocess.run([sys.executable, str(script)], cwd=REPO_ROOT, env=env)
    return r.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--stage",
        default="1,2,3",
        help="comma-separated stage numbers (default: 1,2,3)",
    )
    args = ap.parse_args()

    try:
        stages = sorted({int(s.strip()) for s in args.stage.split(",") if s.strip()})
    except ValueError:
        print("Invalid --stage value: must be comma-separated integers 1-3", file=sys.stderr)
        return 2

    if not all(1 <= s <= 3 for s in stages):
        print("--stage must be in range 1-3", file=sys.stderr)
        return 2

    from pipeline_lock import PipelineLock
    with PipelineLock("arena_build"):
        for s in stages:
            rc = run(s)
            if rc != 0:
                print(f"Stage {s} failed (exit {rc})", file=sys.stderr)
                return rc
    return 0


if __name__ == "__main__":
    sys.exit(main())
