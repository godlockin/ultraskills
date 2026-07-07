#!/usr/bin/env bash
# install-hook.sh — Install RTK PreToolUse hook into ~/.claude/hooks/
#
# Idempotent. Safe to run multiple times.
# Source: devops/rtk-bridge/references/hook-source.md (pinned v3)
# Mirrors what `rtk init -g` does, but tracks the hook in our repo.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# SCRIPT_DIR = devops/rtk-bridge/scripts → up 3 levels reaches repo root
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
HOOK_SRC="$REPO_ROOT/devops/rtk-bridge/references/hook-source.md"
HOOK_DST_DIR="$HOME/.claude/hooks"
HOOK_DST="$HOOK_DST_DIR/rtk-rewrite.sh"
SETTINGS_FILE="$HOME/.claude/settings.json"

# ── 1. Prereq checks ────────────────────────────────────────────────────────
if ! command -v rtk >/dev/null 2>&1; then
  echo "✗ rtk not in PATH"
  echo "  Install: brew install rtk-ai/tap/rtk"
  echo "  Or:      https://github.com/rtk-ai/rtk#installation"
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  echo "✗ jq not in PATH"
  echo "  Install: brew install jq"
  exit 1
fi

RTK_VERSION=$(rtk --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
RTK_MAJOR=$(echo "$RTK_VERSION" | cut -d. -f1)
RTK_MINOR=$(echo "$RTK_VERSION" | cut -d. -f2)
if [ "${RTK_MAJOR:-0}" -lt 1 ] && [ "${RTK_MINOR:-0}" -lt 23 ]; then
  echo "✗ rtk $RTK_VERSION too old (need >= 0.23.0 for `rtk rewrite`)"
  exit 1
fi

# ── 2. Extract hook source from pinned reference ───────────────────────────
if [ ! -f "$HOOK_SRC" ]; then
  echo "✗ Hook source not found: $HOOK_SRC"
  exit 1
fi

# Extract bash code block from markdown reference
HOOK_CONTENT=$(awk '/^```bash$/{flag=1;next}/^```$/{flag=0}flag' "$HOOK_SRC")
if [ -z "$HOOK_CONTENT" ]; then
  echo "✗ Could not extract bash from $HOOK_SRC"
  exit 1
fi

# ── 3. Write hook to ~/.claude/hooks/ ──────────────────────────────────────
mkdir -p "$HOOK_DST_DIR"

# Backup if existing hook differs
if [ -f "$HOOK_DST" ] && ! diff -q <(echo "$HOOK_CONTENT") "$HOOK_DST" >/dev/null 2>&1; then
  cp "$HOOK_DST" "$HOOK_DST.bak.$(date +%s)"
  echo "  ↻ Backed up existing hook to $HOOK_DST.bak.<ts>"
fi

echo "$HOOK_CONTENT" > "$HOOK_DST"
chmod +x "$HOOK_DST"
echo "✓ Hook written: $HOOK_DST"

# ── 4. Register hook in settings.json (idempotent) ────────────────────────
if [ ! -f "$SETTINGS_FILE" ]; then
  echo "  ⚠️  $SETTINGS_FILE not found, skipping registration"
  echo "     Create the file and rerun install-hook.sh"
  exit 0
fi

python3 - "$SETTINGS_FILE" "$HOOK_DST" << 'PY'
import json, sys
from pathlib import Path

settings_path = Path(sys.argv[1])
hook_path = sys.argv[2]

with settings_path.open() as f:
    cfg = json.load(f)

hooks = cfg.setdefault("hooks", {})
pre_list = hooks.setdefault("PreToolUse", [])

# Check if our hook is already registered
already = False
for entry in pre_list:
    if entry.get("matcher") == "Bash":
        for h in entry.get("hooks", []):
            if h.get("command") == hook_path:
                already = True
                break

if already:
    print("  ✓ Hook already registered in settings.json")
else:
    # Append, don't clobber
    pre_list.append({
        "matcher": "Bash",
        "hooks": [{"type": "command", "command": hook_path}]
    })
    with settings_path.open("w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("  ✓ Registered hook in PreToolUse (matcher: Bash)")

PY

echo ""
echo "✓ Done. Restart Claude Code to activate."
echo "  Verify: bash devops/rtk-bridge/scripts/check-status.sh"
