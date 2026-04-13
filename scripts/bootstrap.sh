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
[[ -n "$TARGET_DIR" ]] || { echo "✗ --target value cannot be empty" >&2; exit 1; }

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
    EXISTS=$((EXISTS + 1)) || true
  elif $DRY_RUN; then
    info "[DRY-RUN] ln -s $src $dst"
    NEW=$((NEW + 1)) || true
  else
    mkdir -p "$TARGET_DIR"
    if ln -sf "$src" "$dst"; then
      ok "链接: $name"; NEW=$((NEW + 1)) || true
    else
      err "失败: $name"; FAIL=$((FAIL + 1)) || true
    fi
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
  if [[ $NEW -eq 0 && $EXISTS -eq 0 && $FAIL -eq 0 ]]; then
    warn "未找到任何 skill，请检查仓库结构或 --target 路径"
  fi
fi

if $UPGRADE; then
  step "更新仓库..."
  $DRY_RUN && info "[DRY-RUN] git pull" || git -C "$REPO_ROOT" pull
  $DRY_RUN && info "[DRY-RUN] git submodule update --remote" \
    || git -C "$REPO_ROOT" submodule update --remote --quiet

  step "修复断链..."
  FIXED=0
  for link in "$TARGET_DIR"/*; do
    [ -L "$link" ] || continue
    if [ ! -e "$link" ]; then
      warn "断链: $(basename "$link")"
      $DRY_RUN && info "[DRY-RUN] rm $link" || { rm "$link"; FIXED=$((FIXED + 1)) || true; }
    fi
  done
  info "修复断链: $FIXED 个"
  exit 0
fi
