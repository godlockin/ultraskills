#!/usr/bin/env bash
# install-global-mcp.sh — register cua-mcp-server in ~/.claude/mcp.json
#
# Appends (not overwrites!) — preserves other MCP servers like skills-discovery.
# Fixes the clobber bug in devops/skill-loader/install-global-mcp.sh.

set -euo pipefail

MCP_CONFIG="$HOME/.claude/mcp.json"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WRAPPER="$SCRIPT_DIR/scripts/run_cua_driver.sh"

# Ensure wrapper is executable
chmod +x "$WRAPPER"

mkdir -p "$(dirname "$MCP_CONFIG")"
[ -f "$MCP_CONFIG" ] || echo '{}' > "$MCP_CONFIG"

# Use Python for safe JSON merge (preserves existing keys)
python3 <<PYEOF
import json
from pathlib import Path

p = Path("$MCP_CONFIG")
try:
    data = json.loads(p.read_text()) if p.stat().st_size else {}
except json.JSONDecodeError:
    print(f"WARN: $MCP_CONFIG is corrupted, backing up and starting fresh")
    p.rename(p.with_suffix('.json.bak'))
    data = {}

data.setdefault("mcpServers", {})

# Resolve absolute wrapper path
wrapper = Path("$WRAPPER").resolve()

data["mcpServers"]["cua-mcp-server"] = {
    "type": "stdio",
    "command": str(wrapper),
    "args": [],
    "env": {}
}

p.write_text(json.dumps(data, indent=2))
print(f"✅ Registered cua-mcp-server in {p}")
print(f"   wrapper: {wrapper}")
print(f"   total servers: {list(data['mcpServers'].keys())}")
PYEOF

echo ""
echo "Next steps:"
echo "  1. Restart Claude Code (or run /mcp to refresh)"
echo "  2. Verify: cat $MCP_CONFIG | python3 -m json.tool"
echo "  3. Sanity test: $SCRIPT_DIR/scripts/check_install.py"
