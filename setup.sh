#!/usr/bin/env bash
# setup.sh — Install ultraskills into ~/.claude/skills/
#
# Usage:
#   ./setup.sh           # Symlink top skills (arena winners + community picks)
#   ./setup.sh --all     # Symlink ALL 555 skills (slower discovery)
#   ./setup.sh --remove  # Remove all ultraskills symlinks from ~/.claude/skills/
#
# What this does:
#   Creates symlinks: ~/.claude/skills/{skill-id} → /path/to/ultraskills/{skill-dir}
#   Skills become discoverable by Claude Code, equivalent to default ~/.claude/skills/.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$HOME/.claude/skills"
INSTALL_MODE="${1:-}"

# Top skills: arena winners (24 found in index) + curated community/karpathy picks
TOP_SKILLS=(
  # Arena winners
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
  # Curated community picks (karpathy + mattpocock)
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

install_skill() {
  local id="$1"
  local rel_path="$2"
  local src="$REPO_DIR/$rel_path"
  local dst="$SKILLS_DIR/$id"

  if [ ! -d "$src" ]; then
    echo "  ⚠️  skip $id (dir not found: $src)"
    return
  fi

  if [ -L "$dst" ]; then
    rm "$dst"
  elif [ -d "$dst" ]; then
    echo "  ⚠️  skip $id (real dir exists at $dst, not overwriting)"
    return
  fi

  ln -sf "$src" "$dst"
  echo "  ✓ $id"
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

if [ "$INSTALL_MODE" = "--remove" ]; then
  remove_ultraskills
fi

if [ "$INSTALL_MODE" = "--all" ]; then
  echo "Installing ALL skills from $REPO_DIR → $SKILLS_DIR"
  echo "⚠️  555 skills will be registered. Session start may be slower."
  echo ""
  # Use index.json to enumerate all skills
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
        print(f"  ⚠️  skip {sid}")
        continue
    if os.path.islink(dst):
        os.remove(dst)
    elif os.path.isdir(dst):
        print(f"  ⚠️  skip {sid} (real dir exists)")
        continue
    os.symlink(src, dst)
    count += 1
print(f"\nInstalled {count} skills → {skills_dir}")
PY
else
  echo "Installing top skills (arena winners + curated picks) → $SKILLS_DIR"
  echo ""
  for entry in "${TOP_SKILLS[@]}"; do
    id="${entry%%|*}"
    path="${entry##*|}"
    install_skill "$id" "$path"
  done
  echo ""
  echo "Installed ${#TOP_SKILLS[@]} skills → $SKILLS_DIR"
  echo ""
  echo "To install all 555 skills: ./setup.sh --all"
  echo "To remove:                 ./setup.sh --remove"
fi
