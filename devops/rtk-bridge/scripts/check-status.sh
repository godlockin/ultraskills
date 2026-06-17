#!/usr/bin/env bash
# check-status.sh — Report RTK hook install state

set -uo pipefail

HOOK_DST="$HOME/.claude/hooks/rtk-rewrite.sh"
SETTINGS_FILE="$HOME/.claude/settings.json"

echo "=== RTK Hook Status ==="
echo ""

# 1. RTK in PATH
if command -v rtk >/dev/null 2>&1; then
  RTK_VERSION=$(rtk --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
  echo "✓ rtk installed: $RTK_VERSION ($(which rtk))"
else
  echo "✗ rtk NOT in PATH"
fi

# 2. jq in PATH
if command -v jq >/dev/null 2>&1; then
  echo "✓ jq installed: $(which jq)"
else
  echo "✗ jq NOT in PATH"
fi

# 3. Hook file
if [ -f "$HOOK_DST" ]; then
  HOOK_VERSION=$(grep -oE 'rtk-hook-version: [0-9]+' "$HOOK_DST" | head -1 | awk '{print $2}')
  echo "✓ hook installed: $HOOK_DST (v$HOOK_VERSION)"
else
  echo "✗ hook NOT installed: $HOOK_DST"
fi

# 4. Settings registration
if [ -f "$SETTINGS_FILE" ]; then
  REGISTERED=$(python3 -c "
import json
with open('$SETTINGS_FILE') as f: cfg = json.load(f)
hooks = cfg.get('hooks', {}).get('PreToolUse', [])
for entry in hooks:
    if entry.get('matcher') == 'Bash':
        for h in entry.get('hooks', []):
            if 'rtk-rewrite.sh' in h.get('command',''):
                print('yes')
                exit()
print('no')
")
  if [ "$REGISTERED" = "yes" ]; then
    echo "✓ hook registered in $SETTINGS_FILE (PreToolUse / Bash)"
  else
    echo "✗ hook NOT registered in $SETTINGS_FILE"
  fi
else
  echo "✗ $SETTINGS_FILE not found"
fi

echo ""
echo "=== Fix ==="
echo "  Install:   bash devops/rtk-bridge/scripts/install-hook.sh"
echo "  Remove:    bash devops/rtk-bridge/scripts/uninstall-hook.sh"
