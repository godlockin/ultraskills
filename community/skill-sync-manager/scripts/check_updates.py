#!/usr/bin/env python3
"""
Check for submodule updates without actually updating.
"""

import subprocess
import json
import sys


def run_cmd(cmd):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def get_submodule_status():
    """Get submodule status with update info."""
    rc, stdout, stderr = run_cmd("git submodule status")

    if rc != 0:
        print(f"Error getting submodules: {stderr}")
        return []

    submodules = []
    for line in stdout.strip().split("\n"):
        if line:
            # Format: <hash> <path> (<branch/tag>)
            # Leading + means there's an update available
            # Leading  means up to date
            # Leading - means the submodule is not initialized

            line = line.strip()
            if line.startswith("-"):
                # Not initialized
                parts = line.split()
                submodules.append({
                    "path": parts[1],
                    "status": "not_initialized",
                    "hash": parts[0][1:],
                    "branch": parts[2] if len(parts) > 2 else "unknown"
                })
            elif line.startswith("+"):
                # Has update
                parts = line.split()
                submodules.append({
                    "path": parts[1],
                    "status": "outdated",
                    "local_hash": parts[0][1:],
                    "branch": parts[2] if len(parts) > 2 else "unknown"
                })
            else:
                # Up to date
                parts = line.split()
                submodules.append({
                    "path": parts[1],
                    "status": "current",
                    "hash": parts[0],
                    "branch": parts[2] if len(parts) > 2 else "unknown"
                })

    return submodules


def main():
    print("=== Skill Update Checker ===\n")

    # Check if we're in a git repo
    rc, _, _ = run_cmd("git rev-parse --git-dir")
    if rc != 0:
        print("Error: Not in a git repository")
        sys.exit(1)

    submodules = get_submodule_status()

    if not submodules:
        print("No submodules found")
        sys.exit(0)

    # Categorize
    outdated = [s for s in submodules if s["status"] == "outdated"]
    current = [s for s in submodules if s["status"] == "current"]
    not_init = [s for s in submodules if s["status"] == "not_initialized"]

    print(f"Total: {len(submodules)} submodules\n")

    if outdated:
        print("=== Outdated (updates available) ===")
        for sm in outdated:
            print(f"  ⚠️  {sm['path']} ({sm['branch']})")
        print()

    if current:
        print("=== Current (up to date) ===")
        for sm in current:
            print(f"  ✓  {sm['path']} ({sm['branch']})")
        print()

    if not_init:
        print("=== Not Initialized ===")
        for sm in not_init:
            print(f"  ?  {sm['path']}")
        print()

    # Summary
    print("=== Summary ===")
    print(f"Outdated: {len(outdated)}")
    print(f"Current: {len(current)}")
    print(f"Not Initialized: {len(not_init)}")

    if outdated:
        print("\nTo update, run:")
        print("  git submodule update --remote --merge")
        print("or:")
        print("  python scripts/sync_submodules.py")

    # JSON output for automation
    print("\n--- JSON Output ---")
    print(json.dumps(submodules, indent=2))


if __name__ == "__main__":
    main()