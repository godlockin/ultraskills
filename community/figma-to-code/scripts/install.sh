#!/usr/bin/env bash
# figma-to-code installer
set -euo pipefail

echo "==> figma-to-code install"

if ! command -v node >/dev/null; then
  echo "WARN: node not found (needed for MCP servers)"
  command -v brew >/dev/null && brew install node
fi

if ! command -v jq >/dev/null; then
  command -v brew >/dev/null && brew install jq || true
fi

cat <<EOF

Done. Next:
  1) Get FIGMA_ACCESS_TOKEN:
     https://www.figma.com/developers/api#access-tokens
     export FIGMA_ACCESS_TOKEN="figd_xxx"

  2) (Recommended) install Framelink MCP:
     npx -y figma-developer-mcp --version
     Then add to ~/.claude.json mcpServers (see SKILL.md)

  3) Or use Figma Dev Mode MCP (Pro acct, Figma desktop only):
     Figma → Preferences → Enable Dev Mode MCP Server
     Add http://127.0.0.1:3845/mcp to mcp.json (sse transport)
EOF
