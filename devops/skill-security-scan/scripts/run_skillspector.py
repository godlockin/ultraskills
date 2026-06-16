#!/usr/bin/env python3
"""
SkillSpector wrapper — runs the NVIDIA SkillSpector CLI on a skill path.

Usage:
  run_skillspector.py <skill-path> [--no-llm] [--format json|terminal] [--output FILE]

Defaults: --no-llm (CI-safe, no API key), --format json (machine-readable).

Exits 0 on SAFE/CAUTION, 2 on DO-NOT-INSTALL, 1 on error.
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def find_skillspector():
    """Locate the skillspector CLI. Prefer system PATH, fall back to submodule venv."""
    binary = shutil.which("skillspector")
    if binary:
        return binary
    # Fallback: try the submodule's installed entry point
    candidate = REPO_ROOT / "external" / "skillspector" / ".venv" / "bin" / "skillspector"
    if candidate.exists():
        return str(candidate)
    return None


def parse_args():
    p = argparse.ArgumentParser(description="Run SkillSpector on a skill path")
    p.add_argument("skill_path", help="Path to skill directory or SKILL.md file")
    p.add_argument("--no-llm", action="store_true", default=True,
                   help="Skip LLM semantic filter (CI-safe, no API key needed)")
    p.add_argument("--with-llm", dest="no_llm", action="store_false",
                   help="Enable LLM semantic filter (requires API key)")
    p.add_argument("--format", choices=["json", "terminal", "markdown", "sarif"],
                   default="json", help="Output format (default: json)")
    p.add_argument("--output", help="Write output to file instead of stdout")
    p.add_argument("--timeout", type=int, default=120, help="Timeout in seconds")
    return p.parse_args()


def run(args, binary):
    cmd = [
        binary, "scan", args.skill_path,
        "--format", args.format,
    ]
    if args.no_llm:
        cmd.append("--no-llm")
    if args.output:
        cmd.extend(["--output", args.output])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=args.timeout,
    )
    return result


def main():
    args = parse_args()

    binary = find_skillspector()
    if not binary:
        print(
            "ERROR: skillspector CLI not found in PATH and no submodule venv.\n"
            "       Install with: pip install -e external/skillspector/\n"
            "       (requires Python 3.12+)",
            file=sys.stderr,
        )
        sys.exit(1)

    skill_path = Path(args.skill_path)
    if not skill_path.exists():
        print(f"ERROR: skill path does not exist: {args.skill_path}", file=sys.stderr)
        sys.exit(1)

    try:
        result = run(args, binary)
    except subprocess.TimeoutExpired:
        print(f"ERROR: skillspector timed out after {args.timeout}s", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        # Skillspector already wrote the file; just confirm
        print(f"Report written to: {args.output}")
        sys.exit(result.returncode)

    # Stream output
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)

    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
