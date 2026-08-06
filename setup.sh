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
  "git-guardrails-claude-code|community/git-guardrails-claude-code"
  "to-prd|community/to-prd"
  "to-issues|community/to-issues"
  "improve-codebase-architecture|community/improve-codebase-architecture"
  "ubiquitous-language|community/ubiquitous-language"
  "triage-issue|community/triage-issue"
)

# ── Environment doctor — print a one-shot health report at startup ─────────
# Detects: python3 / uv / pip / git / jq / rtk / mcp SDK / network / disk
# Skipped silently under --quiet or --no-doctor.
doctor() {
  if [[ "${INSTALL_MODE}" == "--no-doctor" ]] || [[ "${INSTALL_MODE}" == "--quiet" ]]; then
    return 0
  fi

  local ok="✓" warn="⚠" fail="✗"
  local out=()

  out+=("=== Environment doctor ===")

  # Required
  command -v git >/dev/null 2>&1 \
    && out+=("  $ok git      : $(git --version | head -1)") \
    || out+=("  $fail git      : not found (required)")

  command -v python3 >/dev/null 2>&1 \
    && out+=("  $ok python3  : $(python3 --version | head -1) @ $(command -v python3)") \
    || out+=("  $fail python3  : not found (required for setup_hub_venv / snapshot / distribute)")

  command -v jq >/dev/null 2>&1 \
    && out+=("  $ok jq       : $(jq --version)") \
    || out+=("  $warn jq       : not found (RTK hook will be skipped)")

  # Recommended
  command -v rtk >/dev/null 2>&1 \
    && out+=("  $ok rtk      : $(rtk --version | head -1) @ $(command -v rtk)") \
    || out+=("  $warn rtk      : not found (Bash hook rewrite disabled — install: brew install rtk-ai/tap/rtk)")

  command -v uv >/dev/null 2>&1 \
    && out+=("  $ok uv       : $(uv --version | head -1)") \
    || out+=("  $warn uv       : not found (will fall back to pip — slower)")

  # Optional — only if already on PATH
  command -v brew >/dev/null 2>&1 && out+=("  $ok brew     : $(brew --version | head -1)")
  command -v node  >/dev/null 2>&1 && out+=("  $ok node     : $(node --version | head -1)")

  # mcp SDK — only relevant if hub is being installed
  local mcp_ok=0
  if [ -x "$REPO_DIR/devops/ultraskills-hub/.venv/bin/python" ]; then
    if "$REPO_DIR/devops/ultraskills-hub/.venv/bin/python" -c "import mcp" 2>/dev/null; then
      out+=("  $ok mcp SDK  : installed in hub venv")
      mcp_ok=1
    fi
  fi
  if [ $mcp_ok -eq 0 ] && [ -d "$REPO_DIR/devops/ultraskills-hub" ]; then
    out+=("  $warn mcp SDK  : not installed (will be created by setup_hub_venv if Python 3.11+ available)")
  fi

  # Network — short probe, non-fatal
  if command -v curl >/dev/null 2>&1; then
    if curl -sS --max-time 3 -o /dev/null -w '%{http_code}' https://api.github.com 2>/dev/null | grep -qE '^(200|301|302)$'; then
      out+=("  $ok network  : github.com reachable")
    else
      out+=("  $warn network  : github.com probe failed (submodule update may stall)")
    fi
  fi

  # Disk
  local free_mb
  free_mb=$(df -m "$REPO_DIR" 2>/dev/null | awk 'NR==2 {print $4}')
  if [ -n "$free_mb" ]; then
    if [ "$free_mb" -lt 200 ]; then
      out+=("  $fail disk     : ${free_mb}MB free in $REPO_DIR (need ≥200MB for venvs + cache)")
    else
      out+=("  $ok disk     : ${free_mb}MB free")
    fi
  fi

  # Submodule count + drift
  local sm_total sm_dirty
  sm_total=$(git -C "$REPO_DIR" submodule status 2>/dev/null | wc -l | tr -d ' ')
  sm_dirty=$(git -C "$REPO_DIR" submodule status 2>/dev/null | grep -cE '^[+-]' || true)
  if [ "$sm_total" -gt 0 ]; then
    if [ "$sm_dirty" -gt 0 ]; then
      out+=("  $warn submod  : $sm_total registered, $sm_dirty drift (run ./setup.sh --update-submodules)")
    else
      out+=("  $ok submod  : $sm_total initialized, clean")
    fi
  fi

  echo ""
  printf '%s\n' "${out[@]}"
  echo ""
}

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
  local hub_venv_py="$REPO_DIR/devops/ultraskills-hub/.venv/bin/python"

  [ -f "$hub_py" ] || { echo "  ⚠️  mcp_server.py not found, skipping MCP registration"; return 0; }

  # Create $HOME/.claude + settings.json if missing (fresh install scenario)
  if [ ! -f "$settings" ]; then
    mkdir -p "$settings_dir"
    echo '{}' > "$settings"
    echo "  ✓ created $settings"
  fi

  # Prefer hub venv python (has mcp SDK); fall back to system python3
  local py_bin="python3"
  if [ -x "$hub_venv_py" ] && "$hub_venv_py" -c "import mcp" 2>/dev/null; then
    py_bin="$hub_venv_py"
    echo "  → using hub venv python: $py_bin"
  else
    echo "  ⚠️  hub venv missing — run scripts/setup_hub_venv.sh first"
  fi

  python3 - "$settings" "$hub_py" "$REPO_DIR/devops/ultraskills-hub" "$py_bin" <<'PYEOF'
import json, sys
settings_path, hub_py, hub_cwd, py_bin = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
with open(settings_path, encoding="utf-8") as f:
    s = json.load(f)
mcp = s.setdefault("mcpServers", {})
mcp["ultraskills-hub"] = {
    "command": py_bin,
    "args": [hub_py],
    "cwd": hub_cwd,
}
with open(settings_path, "w", encoding="utf-8") as f:
    json.dump(s, f, indent=2, ensure_ascii=False)
print(f"  ✓ registered ultraskills-hub MCP server (python: {py_bin})")
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
# ── Hub Python venv setup (mcp SDK for ultraskills-hub MCP server) ──────────
setup_hub_venv() {
  if [[ "${INSTALL_MODE}" == "--no-venvs" ]]; then
    return 0
  fi

  if [ -x "$REPO_DIR/scripts/setup_hub_venv.sh" ]; then
    bash "$REPO_DIR/scripts/setup_hub_venv.sh" || \
      echo "  ⚠️  hub venv setup failed (run scripts/setup_hub_venv.sh manually)"
  fi
}


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
  doctor  # still report even when removing — captures pre-removal state
  remove_ultraskills
  # Also remove from all platforms
  python3 "$REPO_DIR/scripts/distribute.py" --remove --platform all
  exit 0
fi

# Print environment doctor report (skipped under --no-doctor / --quiet)
doctor

# Shield reverse-skill whenever an install path is used. A missing submodule is
# safe to skip (there is no RULES.md to inject); an existing target must shield
# successfully or setup stops without claiming a safe install.
shield_reverse_skill_if_present() {
  local target="$REPO_DIR/external/reverse-skill"
  if [ ! -d "$target" ]; then
    echo "  ⚠️  reverse-skill target missing — no RULES.md to shield; continuing safely"
    return 0
  fi
  bash "$REPO_DIR/scripts/shield-reverse-skill.sh" "$target"
}

shield_reverse_skill_if_present

# All install modes now delegate to distribute.py for skill deployment.
# Claude-Code-specific concerns (hooks, RTK, MCP register) still happen here.

if [ "$INSTALL_MODE" = "--all" ]; then
  echo "Installing hub + ALL skills → all detected platforms (mode=$LINK_MODE)"
  echo "⚠️  945 skills will appear in system-reminder. Expect token overhead."
  echo ""
  install_hub
  python3 "$REPO_DIR/scripts/distribute.py" --platform all --mode "$LINK_MODE"
  setup_hooks
  setup_hub_venv
  setup_rtk_hook
  register_mcp_server
  exit 0
fi

if [ "$INSTALL_MODE" = "--top" ]; then
  echo "Installing hub + top 32 curated skills → $PLATFORM (mode=$LINK_MODE)"
  echo ""
  install_hub
  if [ "$PLATFORM" = "claude-code" ]; then
    top_args=()
    for entry in "${TOP_SKILLS[@]}"; do
      top_args+=(--only "${entry%%|*}")
    done
    if ! python3 "$REPO_DIR/scripts/distribute.py" --platform "$PLATFORM" --mode "$LINK_MODE" "${top_args[@]}"; then
      echo "✗ --top aborted: one or more curated skills are unavailable" >&2
      exit 1
    fi
  else
    # For other platforms we still deploy everything (--top only meaningful
    # for Claude Code where system-reminder cost matters)
    python3 "$REPO_DIR/scripts/distribute.py" --platform "$PLATFORM" --mode "$LINK_MODE"
  fi
  echo ""
  echo "Installed hub + ${#TOP_SKILLS[@]} top skills"
  setup_hooks
  setup_hub_venv
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
  setup_hub_venv
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
setup_hub_venv
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
