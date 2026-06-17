#!/usr/bin/env bash
# uninstall-hook.sh — Remove RTK PreToolUse hook

set -euo pipefail

HOOK_DST="$HOME/.claude/hooks/rtk-rewrite.sh"
SETTINGS_FILE="$HOME/.claude/settings.json"

# ── 1. Remove hook script ─────────────────────────────────────────────────
if [ -f "$HOOK_DST" ] || [ -L "$HOOK_DST" ]; then
  rm "$HOOK_DST"
  echo "✓ Removed: $HOOK_DST"
else
  echo "  (hook not present at $HOOK_DST)"
fi

# ── 2. Unregister from settings.json ─────────────────────────────────────
if [ -f "$SETTINGS_FILE" ]; then
  python3 - "$SETTINGS_FILE" "$HOOK_DST" << 'PY'
import json, sys
from pathlib import Path

settings_path = Path(sys.argv[1])
hook_path = sys.argv[2]

with settings_path.open() as f:
    cfg = json.load(f)

hooks = cfg.get("hooks", {})
pre_list = hooks.get("PreToolUse", [])

# Remove entries pointing to our hook
new_pre = []
removed = 0
for entry in pre_list:
    if entry.get("matcher") == "Bash":
        filtered = [h for h in entry.get("hooks", []) if h.get("command") != hook_path]
        if len(filtered) < len(entry.get("hooks", [])):
            removed += 1
        if filtered:
            entry["hooks"] = filtered
            new_pre.append(entry)
    else:
        new_pre.append(entry)

cfg["hooks"]["PreToolUse"] = new_pre
with settings_path.open("w") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"  ✓ Removed {removed} hook entry from settings.json")

PY
else
  echo "  (settings.json not present)"
fi

echo ""
echo "✓ Done. Restart Claude Code."
