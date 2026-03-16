#!/usr/bin/env python3
"""
Agent Reach Wrapper - Provides CLI interface for Agent Reach tool

Usage:
    python wrapper.py install [--safe] [--dry-run]
    python wrapper.py doctor
    python wrapper.py configure <key> <value>
    python wrapper.py uninstall [--keep-config]
"""

import subprocess
import sys
import os


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if check and result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
    return result


def install(safe_mode: bool = False, dry_run: bool = False):
    """Install Agent Reach."""
    # Install the package
    run_command(["pip", "install", "https://github.com/Panniantong/agent-reach/archive/main.zip"])

    # Build install command
    install_cmd = ["agent-reach", "install", "--env=auto"]
    if safe_mode:
        install_cmd.append("--safe")
    if dry_run:
        install_cmd.append("--dry-run")

    run_command(install_cmd, check=False)


def doctor():
    """Run health check."""
    run_command(["agent-reach", "doctor"], check=False)


def configure(key: str, value: str):
    """Configure Agent Reach settings."""
    run_command(["agent-reach", "configure", key, value], check=False)


def uninstall(keep_config: bool = False):
    """Uninstall Agent Reach."""
    cmd = ["agent-reach", "uninstall"]
    if keep_config:
        cmd.append("--keep-config")
    run_command(cmd, check=False)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1]

    if action == "install":
        safe_mode = "--safe" in sys.argv
        dry_run = "--dry-run" in sys.argv
        install(safe_mode=safe_mode, dry_run=dry_run)
    elif action == "doctor":
        doctor()
    elif action == "configure":
        if len(sys.argv) < 4:
            print("Usage: wrapper.py configure <key> <value>")
            sys.exit(1)
        configure(sys.argv[2], sys.argv[3])
    elif action == "uninstall":
        keep_config = "--keep-config" in sys.argv
        uninstall(keep_config=keep_config)
    else:
        print(f"Unknown action: {action}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()