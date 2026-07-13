#!/usr/bin/env bash
# setup.sh — Install + maintain ultraskills into ~/.claude/skills/
#
# Two-phase model:
#
#   PHASE 1 — First-time install (zero dependencies):
#     ./setup.sh                            # hub-only on Claude Code (recommended)
#     ./setup.sh --top                      # hub + 33 curated skills pre-loaded
#     ./setup.sh --all                      # hub + ALL skills (floods system-reminder)
#     ./setup.sh --platform <name>          # deploy to specific AI tool (claude-code | cursor | windsurf | codex | gemini | cline | trae | all)
#     ./setup.sh --platform list            # show supported platforms
#     ./setup.sh --mode symlink|copy|both   # link strategy (default symlink)
#     ./setup.sh --remove                   # uninstall — remove all ultraskills symlinks + MCP entry
#
#     These run WITHOUT touching submodules or arena index. Just installs the
#     client-side hub so Claude can search/load skills on demand.
#
#   PHASE 2 — Maintain (after git pull / when adding new skills):
#     ./setup.sh --update-submodules   # git submodule update --init --remote
#     ./setup.sh --update-arena        # rebuild index.json (scan + cluster + build)
#     ./setup.sh --update              # both of the above
#
# Use cases:
#   - Fresh checkout:    ./setup.sh                          # Claude Code only
#   - Multi-tool user:   ./setup.sh --platform all           # all detected AI tools
#   - Forked skill:      ./setup.sh --platform claude-code --mode copy
#   - Repo dev workflow: ./setup.sh --update                 # after pull / before commit
#   - Restore baseline:  ./setup.sh --remove && ./setup.sh
#
# Why split: fresh install shouldn't fail on upstream-submodule 404s (13 of
# ours are gone). Maintain step is explicit so the user knows when network
# fetches happen.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"
INSTALL_MODE="${1:-}"

# Multi-flag support: scan all args, allow --flag VALUE pairs
PLATFORM="claude-code"
LINK_MODE="symlink"
declare -a REMAINING_ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --platform=*) PLATFORM="${1#--platform=}"; shift ;;
    --mode=*)     LINK_MODE="${1#--mode=}"; shift ;;
    --platform)   shift; PLATFORM="${1:-claude-code}"; shift ;;
    --mode)       shift; LINK_MODE="${1:-symlink}"; shift ;;
    *)            REMAINING_ARGS+=("$1"); shift ;;
  esac
done
# Restore positional for downstream (handle empty array safely under set -u)
if [ ${#REMAINING_ARGS[@]} -gt 0 ]; then
  set -- "${REMAINING_ARGS[@]}"
else
  set --
fi

# Curated top skills: arena winners + community picks
TOP_SKILLS=(
  "receiving-code-review|community/receiving-code-review"
  "ab-test-setup|external/marketingskills/skills/ab-test-setup"
  "site-architecture|external/marketingskills/skills/site-architecture"
  "launch-strategy|external/marketingskills/skills/launch-strategy"
  "schema-markup|external/marketingskills/skills/schema-markup"
  "autoresearch|engineering/autoresearch"
  "page-cro|external/marketingskills/skills/page-cro"
  "onboarding-cro|external/marketingskills/skills/onboarding-cro"
  "copywriting|external/marketingskills/skills/copywriting"
  "content-strategy|external/marketingskills/skills/content-strategy"
  "social-content|external/marketingskills/skills/social-content"
  "product-analytics|external/claude-skills/product-team/product-analytics"
  "ad-creative|external/marketingskills/skills/ad-creative"
  "free-tool-strategy|external/marketingskills/skills/free-tool-strategy"
  "advanced-evaluation|community/advanced-evaluation"
  "context-engineering-collection|external/context-engineering-skills"
  "git-commit-master|community/git-commit-master"
  "fastapi-expert|external/fullstack-dev-skills/skills/fastapi-expert"
  "bdi-mental-states|community/bdi-mental-states"
  "rag-architect|external/fullstack-dev-skills/skills/rag-architect"
  "media-downloader|external/media-downloader"
  "cold-email|external/marketingskills/skills/cold-email"
  "revops|external/marketingskills/skills/revops"
  "pricing-strategy|external/marketingskills/skills/pricing-strategy"
  "karpathy-guidelines|community/karpathy-guidelines"
  "grill-me|community/grill-me"
  "design-an-interface|community/design-an-interface"
  "git-guardrails-claude-code|community/git-guardrails-claude-code"
  "to-prd|community/to-prd"
  "to-issues|community/to-issues"
  "improve-codebase-architecture|community/improve-codebase-architecture"
  "ubiquitous-language|community/ubiquitous-language"
  "triage-issue|community/triage-issue"
)

mkdir -p "$SKILLS_DIR"

symlink_skill() {
  local id="$1"
  local rel_path="$2"
  local src="$REPO_DIR/$rel_path"
  local dst="$SKILLS_DIR/$id"

  if [ ! -d "$src" ]; then
    echo "  ⚠️  skip $id (not found)"
    return
  fi
  [ -L "$dst" ] && rm "$dst"
  if [ -d "$dst" ]; then
    echo "  ⚠️  skip $id (real dir exists)"
    return
  fi
  ln -sf "$src" "$dst"
  echo "  ✓ $id"
}

install_hub() {
  local hub_src="$REPO_DIR/devops/ultraskills-hub"
  local hub_dst="$SKILLS_DIR/ultraskills-hub"
  # Snapshot any locally-edited skills BEFORE we touch anything
  python3 "$REPO_DIR/scripts/snapshot.py" 2>&1 | sed 's/^/    /' || true
  [ -L "$hub_dst" ] && rm "$hub_dst"
  ln -sf "$hub_src" "$hub_dst"
  echo "  ✓ ultraskills-hub (search engine for all 555 skills)"
}

# Register ultraskills-hub MCP server in ~/.claude/settings.json so Claude Code
# can call search_skills/get_skill/list_winners without copying SKILL.md frontmatter
# into context. Idempotent — replaces existing entry on re-run.
register_mcp_server() {
  local settings_dir="$HOME/.claude"
  local settings="$settings_dir/settings.json"
  local hub_py="$REPO_DIR/devops/ultraskills-hub/mcp_server.py"

  [ -f "$hub_py" ] || { echo "  ⚠️  mcp_server.py not found, skipping MCP registration"; return 0; }

  # Create $HOME/.claude + settings.json if missing (fresh install scenario)
  if [ ! -f "$settings" ]; then
    mkdir -p "$settings_dir"
    echo '{}' > "$settings"
    echo "  ✓ created $settings"
  fi

  python3 - "$settings" "$hub_py" "$REPO_DIR/devops/ultraskills-hub" <<'PYEOF'
import json, sys
settings_path, hub_py, hub_cwd = sys.argv[1], sys.argv[2], sys.argv[3]
with open(settings_path, encoding="utf-8") as f:
    s = json.load(f)
mcp = s.setdefault("mcpServers", {})
mcp["ultraskills-hub"] = {
    "command": "python3",
    "args": [hub_py],
    "cwd": hub_cwd,
}
with open(settings_path, "w", encoding="utf-8") as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
print(f"  ✓ registered ultraskills-hub MCP server")
PYEOF
}

remove_ultraskills() {
  echo "Removing ultraskills symlinks from $SKILLS_DIR..."
  local count=0
  for link in "$SKILLS_DIR"/*/; do
    link="${link%/}"
    if [ -L "$link" ]; then
      target="$(readlink "$link")"
      if [[ "$target" == "$REPO_DIR"* ]]; then
        rm "$link"
        echo "  removed: $(basename "$link")"
        ((count++)) || true
      fi
    fi
  done
  echo "Done. Removed $count symlinks."

  # Also remove MCP server registration
  local settings="$HOME/.claude/settings.json"
  if [ -f "$settings" ]; then
    python3 - "$settings" <<'PYEOF'
import json, sys
with open(sys.argv[1], encoding="utf-8") as f:
    s = json.load(f)
mcp = s.get("mcpServers", {})
if "ultraskills-hub" in mcp:
    del mcp["ultraskills-hub"]
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        json.dump(s, f, indent=2, ensure_ascii=False)
    print(f"  ✓ removed ultraskills-hub MCP server entry")
PYEOF
  fi
  exit 0
}

# ── Claude Code hooks injection ───────────────────────────────────────────────
setup_hooks() {
  local settings="$REPO_DIR/.claude/settings.local.json"
  local hook_post="$REPO_DIR/devops/hooks/post-skill-write.sh"
  local hook_stop="$REPO_DIR/devops/hooks/stop-arena-rebuild.sh"

  if [ ! -f "$settings" ]; then
    echo "  ⚠️  .claude/settings.local.json not found, skipping hooks injection"
    return
  fi

  chmod +x "$hook_post" "$hook_stop"

  # Inject PostToolUse + Stop hooks via Python (idempotent)
  python3 - "$settings" "$hook_post" "$hook_stop" << 'PY'
import json, sys

settings_path, hook_post, hook_stop = sys.argv[1], sys.argv[2], sys.argv[3]
with open(settings_path) as f:
    cfg = json.load(f)

hooks = cfg.setdefault("hooks", {})

def has_hook(hook_list, cmd):
    for entry in hook_list:
        for h in entry.get("hooks", []):
            if h.get("command") == cmd:
                return True
    return False

# PostToolUse: validate on Write/Edit to SKILL.md or index.json
post_list = hooks.setdefault("PostToolUse", [])
if not has_hook(post_list, hook_post):
    post_list.append({
        "matcher": "Write|Edit",
        "hooks": [{"type": "command", "command": hook_post}]
    })
    print(f"  ✓ PostToolUse hook added: post-skill-write.sh")
else:
    print(f"  ✓ PostToolUse hook already present")

# Stop: arena pipeline rebuild if SKILL.md was written this session
stop_list = hooks.setdefault("Stop", [])
if not has_hook(stop_list, hook_stop):
    stop_list.append({
        "matcher": "",
        "hooks": [{"type": "command", "command": hook_stop}]
    })
    print(f"  ✓ Stop hook added: stop-arena-rebuild.sh")
else:
    print(f"  ✓ Stop hook already present")

with open(settings_path, "w") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)
    f.write("\n")
PY
}


# ── RTK hook setup (PreToolUse Bash rewriter for token savings) ─────────────
setup_rtk_hook() {
  if [[ "${INSTALL_MODE}" == "--no-rtk" ]]; then
    return 0
  fi

  if [ ! -x "$REPO_DIR/devops/rtk-bridge/scripts/install-hook.sh" ]; then
    return 0
  fi

  # Quick check: rtk + jq must exist
  if ! command -v rtk >/dev/null 2>&1 || ! command -v jq >/dev/null 2>&1; then
    echo "  ⚠️  rtk or jq not in PATH — skipping RTK hook install"
    echo "     Install: brew install rtk-ai/tap/rtk jq"
    return 0
  fi

  bash "$REPO_DIR/devops/rtk-bridge/scripts/install-hook.sh" || \
    echo "  ⚠️  RTK hook install failed (run devops/rtk-bridge/scripts/install-hook.sh manually)"
}


# ── Python venv setup (skillspector, cua — created on first run) ──────────────
setup_python_venvs() {
  if [[ "${INSTALL_MODE}" == "--no-venvs" ]]; then
    return 0
  fi

  if [ -x "$REPO_DIR/scripts/setup_cua.sh" ]; then
    bash "$REPO_DIR/scripts/setup_cua.sh" || echo "  ⚠️  cua venv setup failed (run scripts/setup_cua.sh manually)"
  fi
  if [ -x "$REPO_DIR/devops/skill-security-scan/scripts/setup_skillspector.sh" ]; then
    bash "$REPO_DIR/devops/skill-security-scan/scripts/setup_skillspector.sh" || \
      echo "  ⚠️  skillspector venv setup failed (run manually if needed)"
  fi
}


# ── Phase 2: Maintain submodules + arena index ──────────────────────────────
# Implementation lives in scripts/ (Python) so it can be unit-tested and
# invoked directly without bash. setup.sh just dispatches.

update_submodules() {
  python3 "$REPO_DIR/scripts/sync_submodules.py"
}

update_arena_index() {
  python3 "$REPO_DIR/scripts/build_arena_index.py"
}

# ── Dispatch ──────────────────────────────────────────────────────────────────

# Phase 2 dispatch (maintain) — handled FIRST so --update flags exit before
# install runs (avoids touching ~/.claude/skills/ during a maintain session).
case "$INSTALL_MODE" in
  --update)
    echo "=== Phase 2: full maintain ==="
    echo ""
    update_submodules
    echo ""
    update_arena_index
    exit 0
    ;;
  --update-submodules)
    echo "=== Phase 2: submodule sync ==="
    echo ""
    update_submodules
    exit 0
    ;;
  --update-arena)
    echo "=== Phase 2: arena rebuild ==="
    echo ""
    update_arena_index
    exit 0
    ;;
  --restore)
    echo "=== Restore snapshot ==="
    shift
    python3 "$REPO_DIR/scripts/snapshot.py" --restore "$@"
    exit $?
    ;;
  --snapshot)
    python3 "$REPO_DIR/scripts/snapshot.py"
    exit $?
    ;;
esac

if [ "$INSTALL_MODE" = "--remove" ]; then
  remove_ultraskills
  # Also remove from all platforms
  python3 "$REPO_DIR/scripts/distribute.py" --remove --platform all
  exit 0
fi

# All install modes now delegate to distribute.py for skill deployment.
# Claude-Code-specific concerns (hooks, RTK, MCP register) still happen here.

if [ "$INSTALL_MODE" = "--all" ]; then
  echo "Installing hub + ALL skills → all detected platforms (mode=$LINK_MODE)"
  echo "⚠️  945 skills will appear in system-reminder. Expect token overhead."
  echo ""
  install_hub
  python3 "$REPO_DIR/scripts/distribute.py" --platform all --mode "$LINK_MODE"
  setup_hooks
  setup_rtk_hook
  register_mcp_server
  exit 0
fi

if [ "$INSTALL_MODE" = "--top" ]; then
  echo "Installing hub + top 33 curated skills → $PLATFORM (mode=$LINK_MODE)"
  echo ""
  install_hub
  # Deploy only the curated top skills (not the whole index) — overlay a
  # filtered distribute. Implemented via filter: distribute reads index.json
  # and creates links for ALL. For --top we create only TOP_SKILLS symlinks
  # using the legacy per-skill symlink_skill function, scoped to PLATFORM.
  if [ "$PLATFORM" = "claude-code" ]; then
    for entry in "${TOP_SKILLS[@]}"; do
      symlink_skill "${entry%%|*}" "${entry##*|}"
    done
  else
    # For other platforms we still deploy everything (--top only meaningful
    # for Claude Code where system-reminder cost matters)
    python3 "$REPO_DIR/scripts/distribute.py" --platform "$PLATFORM" --mode "$LINK_MODE"
  fi
  echo ""
  echo "Installed hub + ${#TOP_SKILLS[@]} top skills"
  setup_hooks
  setup_rtk_hook
  register_mcp_server
  exit 0
fi

# Default: hub only on Claude Code (unless --platform specified)
if [ "$PLATFORM" != "claude-code" ] || [ "$LINK_MODE" != "symlink" ]; then
  # User asked for non-default platform or mode → deploy via distribute
  echo "Deploying to $PLATFORM (mode=$LINK_MODE, hub-only otherwise)..."
  install_hub
  python3 "$REPO_DIR/scripts/distribute.py" --platform "$PLATFORM" --mode "$LINK_MODE"
  setup_hooks
  setup_rtk_hook
  register_mcp_server
  echo ""
  echo "Done. Deployed to $PLATFORM with hub + MCP."
  exit 0
fi

# Pure default: hub only
echo "Installing ultraskills-hub → $SKILLS_DIR"
echo ""
install_hub
setup_hooks
setup_rtk_hook
register_mcp_server
echo ""
echo "Done. Claude can now search all ultraskills on demand."
echo "  In session: Skill('ultraskills-hub') → search → load specific skill"
echo "  MCP server 'ultraskills-hub' exposes search_skills/get_skill/list_winners/etc."
echo ""
echo "Phase 1 (install) options:"
echo "  ./setup.sh --top                                  # also pre-load 33 curated skills"
echo "  ./setup.sh --all                                  # pre-load all skills (high token overhead)"
echo "  ./setup.sh --platform <name>                      # deploy to specific AI tool (claude-code | cursor | windsurf | codex | gemini | cline | trae | all)"
echo "  ./setup.sh --mode symlink|copy                    # link strategy (default symlink)"
echo "  ./setup.sh --remove                               # uninstall everything"
echo ""
echo "Phase 2 (maintain — run after git pull / when adding skills):"
echo "  ./setup.sh --update-submodules   # fetch latest submodule commits"
echo "  ./setup.sh --update-arena        # rebuild index.json from current SKILL.md"
echo "  ./setup.sh --update              # both of the above"
