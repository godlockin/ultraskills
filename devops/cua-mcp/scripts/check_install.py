#!/usr/bin/env python3
"""
cua-mcp install check — verify cua-mcp-server is reachable.

Mirrors devops/skill-security-scan/scripts/run_skillspector.py:23-32.
Tries system PATH first, falls back to the submodule venv.

Exits 0 on success, 1 if not installed (with clear next-step message).
"""

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SUBMODULE_VENV = REPO_ROOT / "external" / "cua" / ".venv" / "bin" / "cua-mcp-server"
REQUIRED_PYTHON = "3.12"


def find_binary():
    """Locate cua-mcp-server. Prefer system PATH, fall back to submodule venv."""
    binary = shutil.which("cua-mcp-server")
    if binary:
        return binary
    if SUBMODULE_VENV.exists():
        return str(SUBMODULE_VENV)
    return None


def main():
    print("=== cua-mcp install check ===\n")

    binary = find_binary()
    if not binary:
        print("❌ cua-mcp-server not found in PATH and no submodule venv.\n")
        print("Install with:")
        print("  uv venv --python 3.12 external/cua/.venv")
        print("  external/cua/.venv/bin/pip install \\")
        print("      external/cua/libs/python/cua \\")
        print("      external/cua/libs/python/mcp-server")
        print("\nOr globally:")
        print("  pip install cua cua-mcp-server")
        print("\nNOTE: do NOT install cua-agent[omni] (AGPL-3.0 contamination risk).")
        sys.exit(1)

    print(f"✅ Found: {binary}")

    # Try a --version or --help to verify it actually runs
    try:
        result = subprocess.run(
            [binary, "--help"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            print(f"✅ Executable (--help exit 0)")
        else:
            print(f"⚠️  Executable but --help returned {result.returncode}")
            if result.stderr:
                print(f"   stderr: {result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        print("⚠️  Binary found but --help timed out")
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        sys.exit(1)

    # Check if MCP registration exists
    mcp_config = Path.home() / ".claude" / "mcp.json"
    if mcp_config.exists():
        try:
            import json
            data = json.loads(mcp_config.read_text())
            servers = data.get("mcpServers", {})
            if "cua-mcp-server" in servers:
                print(f"✅ MCP registered in {mcp_config}")
            else:
                print(f"⚠️  MCP not registered. Run: bash devops/cua-mcp/install-global-mcp.sh")
        except Exception:
            print(f"⚠️  Could not parse {mcp_config}")
    else:
        print(f"ℹ️  No {mcp_config} yet — run: bash devops/cua-mcp/install-global-mcp.sh")

    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
