#!/usr/bin/env python3
"""
Sync all git submodules to their latest remote version.
"""

import subprocess
import sys
import os


def run_cmd(cmd, cwd=None):
    """Run a shell command and return output."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def get_submodules():
    """Get list of submodules."""
    rc, stdout, stderr = run_cmd("git submodule status")
    if rc != 0:
        print(f"Error getting submodules: {stderr}")
        print("  Fix: Ensure you're in the repo root. Try: git submodule init")
        return []

    submodules = []
    for line in stdout.strip().split("\n"):
        if line:
            parts = line.split()
            if len(parts) >= 2:
                submodules.append(parts[1])
    return submodules


def update_submodule(submodule_path):
    """Update a single submodule to latest remote."""
    print(f"Updating {submodule_path}...")

    # First, fetch latest
    rc, stdout, stderr = run_cmd(
        f"git submodule update --remote --merge {submodule_path}"
    )

    if rc != 0:
        print(f"  Warning: {stderr}")
        print(f"  Fix: Try manually: cd {submodule_path} && git fetch && git pull")
        return False

    print(f"  Updated {submodule_path}")
    return True


def main():
    print("=== Skill Sync Manager ===\n")

    # Check if we're in a git repo
    rc, _, _ = run_cmd("git rev-parse --git-dir")
    if rc != 0:
        print("Error: Not in a git repository")
        print("  Fix: cd to ultraskills repo root first")
        sys.exit(1)

    # Get submodules
    submodules = get_submodules()

    if not submodules:
        print("No submodules found")
        sys.exit(0)

    print(f"Found {len(submodules)} submodules:\n")
    for sm in submodules:
        print(f"  - {sm}")

    print("\n--- Updating all submodules ---\n")

    updated = []
    failed = []

    for sm in submodules:
        if update_submodule(sm):
            updated.append(sm)
        else:
            failed.append(sm)

    print("\n=== Summary ===")
    print(f"Updated: {len(updated)}")
    print(f"Failed: {len(failed)}")

    if updated:
        print("\nUpdated submodules:")
        for sm in updated:
            print(f"  - {sm}")

    if failed:
        print("\nFailed submodules:")
        for sm in failed:
            print(f"  - {sm}")
        print(f"\n  Fix: Retry failed only: git submodule update --remote --merge {' '.join(failed)}")
        sys.exit(1)

    # Check for changes
    print("\n--- Checking for changes ---")
    rc, stdout, _ = run_cmd("git diff --submodule --quiet")
    if rc == 0:
        print("No changes to commit")
    else:
        print("Changes detected! Run 'git diff --submodule' to view")
        print("Then run: git add external/ && git commit -m 'chore: update submodules'")


if __name__ == "__main__":
    main()