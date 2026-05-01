#!/usr/bin/env bash
# setup.sh — Install ultraskills into ~/.claude/skills/
#
# Usage:
#   ./setup.sh           # Hub-only (recommended): 1 entry point + search engine
#   ./setup.sh --top     # Hub + 33 top/curated skills pre-loaded
#   ./setup.sh --all     # Hub + ALL 555 skills (floods system-reminder)
#   ./setup.sh --remove  # Remove all ultraskills symlinks from ~/.claude/skills/
#
# Recommended: hub-only
#   - Only "ultraskills-hub" skill appears in system-reminder (1 entry)
#   - Claude searches index on demand → loads specific SKILL.md when needed
#   - Zero bloat, full access to all 555 skills

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"
INSTALL_MODE="${1:-}"

# ── Submodule check ───────────────────────────────────────────────────────────
check_submodules() {
  # Detect uninitialized submodules: registered in .gitmodules but empty dirs
  local uninitialized=()
  while IFS= read -r path; do
    local full="$REPO_DIR/$path"
    if [ -d "$full" ] && [ -z "$(ls -A "$full" 2>/dev/null)" ]; then
      uninitialized+=("$path")
    elif [ ! -d "$full" ]; then
      uninitialized+=("$path")
    fi
  done < <(git -C "$REPO_DIR" config --file .gitmodules --get-regexp 'submodule\..*\.path' | awk '{print $2}')

  if [ ${#uninitialized[@]} -eq 0 ]; then
    return 0
  fi

  echo ""
  echo "⚠️  Uninitialized submodules detected (${#uninitialized[@]}):"
  for p in "${uninitialized[@]}"; do
    echo "    - $p"
  done
  echo ""

  # Auto-init by default; skip only if --no-submodules passed
  if [[ "${INSTALL_MODE}" == "--no-submodules" ]]; then
    echo "Skipping submodule init (--no-submodules). Some skills may be unavailable."
    return 0
  fi

  echo "Initializing submodules... (pass --no-submodules to skip)"
  git -C "$REPO_DIR" submodule update --init --recursive
  echo "✓ Submodules initialized"
}

check_submodules

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
  [ -L "$hub_dst" ] && rm "$hub_dst"
  ln -sf "$hub_src" "$hub_dst"
  echo "  ✓ ultraskills-hub (search engine for all 555 skills)"
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


# ── Dispatch ──────────────────────────────────────────────────────────────────

if [ "$INSTALL_MODE" = "--remove" ]; then
  remove_ultraskills
fi

if [ "$INSTALL_MODE" = "--all" ]; then
  echo "Installing hub + ALL skills → $SKILLS_DIR"
  echo "⚠️  555 skills will appear in system-reminder. Expect token overhead."
  echo ""
  install_hub
  python3 - "$REPO_DIR" "$SKILLS_DIR" << 'PY'
import json, os, sys
repo_dir, skills_dir = sys.argv[1], sys.argv[2]
idx = json.load(open(os.path.join(repo_dir, "index.json")))
count = 0
for s in idx["skills"]:
    sid = s["id"]
    src = os.path.join(repo_dir, s["path"].lstrip("./"))
    dst = os.path.join(skills_dir, sid)
    if not os.path.isdir(src):
        continue
    if os.path.islink(dst):
        os.remove(dst)
    elif os.path.isdir(dst):
        continue
    os.symlink(src, dst)
    count += 1
print(f"  + {count} individual skills")
PY
  setup_hooks
  exit 0
fi

if [ "$INSTALL_MODE" = "--top" ]; then
  echo "Installing hub + top 33 curated skills → $SKILLS_DIR"
  echo ""
  install_hub
  for entry in "${TOP_SKILLS[@]}"; do
    symlink_skill "${entry%%|*}" "${entry##*|}"
  done
  echo ""
  echo "Installed hub + ${#TOP_SKILLS[@]} top skills"
  setup_hooks
  exit 0
fi

# Default: hub only
echo "Installing ultraskills-hub → $SKILLS_DIR"
echo ""
install_hub
setup_hooks
echo ""
echo "Done. Claude can now search all 555 ultraskills on demand."
echo "  In session: Skill('ultraskills-hub') → search → load specific skill"
echo ""
echo "Other modes:"
echo "  ./setup.sh --top     # also pre-load 33 curated skills"
echo "  ./setup.sh --all     # pre-load all 555 (high token overhead)"
echo "  ./setup.sh --remove  # uninstall everything"
