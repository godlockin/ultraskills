#!/usr/bin/env bash
# cua-mcp-server wrapper — ensures the venv exists, then exec's the MCP server.
# Used by install-global-mcp.sh to register the MCP entry point.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENV_PY="$REPO_ROOT/external/cua/.venv/bin/python"
VENV_BIN="$REPO_ROOT/external/cua/.venv/bin/cua-mcp-server"

# Prefer the submodule venv if it exists
if [ -x "$VENV_BIN" ]; then
    exec "$VENV_BIN" "$@"
fi

# Fallback: system PATH
if command -v cua-mcp-server >/dev/null 2>&1; then
    exec cua-mcp-server "$@"
fi

echo "ERROR: cua-mcp-server not found." >&2
echo "Run the install steps from devops/cua-mcp/SKILL.md first." >&2
exit 1
