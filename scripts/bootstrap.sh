#!/usr/bin/env bash
set -euo pipefail

UPGRADE=false
GUIDED=false
DRY_RUN=false
TARGET_DIR="$HOME/.claude/skills"

for arg in "$@"; do
  case $arg in
    --upgrade)  UPGRADE=true ;;
    --guided)   GUIDED=true ;;
    --dry-run)  DRY_RUN=true ;;
    --target=*) TARGET_DIR="${arg#*=}" ;;
    --help)
      echo "Usage: bash scripts/bootstrap.sh [--upgrade] [--guided] [--dry-run] [--target=DIR]"
      exit 0 ;;
  esac
done

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'; BOLD='\033[1m'
ok()   { echo -e "${GREEN}✓ $1${NC}"; }
info() { echo -e "${CYAN}  $1${NC}"; }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }
err()  { echo -e "${RED}✗ $1${NC}"; }
step() { echo -e "\n${BOLD}${YELLOW}→ $1${NC}"; }

# 自动检测 ultraskills 仓库根目录（支持 OneDrive 软链接）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd -P)"
info "仓库路径: $REPO_ROOT"

SKILL_CATEGORIES=("community" "engineering" "creative" "devops" "productivity")
NEW=0; EXISTS=0; FAIL=0

do_symlink() {
  local src="$1" name="$2"
  local dst="$TARGET_DIR/$name"
  if [ -L "$dst" ] && [ -e "$dst" ]; then
    info "已存在: $name"
    EXISTS=$((EXISTS + 1))
  elif $DRY_RUN; then
    info "[DRY-RUN] ln -s $src $dst"
    NEW=$((NEW + 1))
  else
    mkdir -p "$TARGET_DIR"
    ln -sf "$src" "$dst" && ok "链接: $name" && NEW=$((NEW + 1)) \
      || { err "失败: $name"; FAIL=$((FAIL + 1)); }
  fi
}

if ! $GUIDED && ! $UPGRADE; then
  step "安装所有 skills → $TARGET_DIR"
  for cat in "${SKILL_CATEGORIES[@]}"; do
    cat_dir="$REPO_ROOT/$cat"
    [ -d "$cat_dir" ] || continue
    for skill_dir in "$cat_dir"/*/; do
      [ -d "$skill_dir" ] || continue
      skill_name="$(basename "$skill_dir")"
      do_symlink "$skill_dir" "$skill_name"
    done
  done
  echo ""
  echo -e "${BOLD}完成: 新建 ${GREEN}$NEW${NC} / 已存在 ${CYAN}$EXISTS${NC} / 失败 ${RED}$FAIL${NC}"
fi
