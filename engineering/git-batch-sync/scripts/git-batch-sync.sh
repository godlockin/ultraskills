#!/usr/bin/env bash
# git-batch-sync.sh — 批量同步 + fork upstream 同步 + 启发式修冲突
# Usage: git-batch-sync.sh [ROOT_DIR] [--no-fetch] [--dry-run] [--summary]
#                       [--stats] [--bench] [--sync-upstream] [--push]
#                       [--max-depth=N] [--skiplist=FILE] [--allowlist=FILE]
#                       [--install-deps] [--migrate-tools] [--help]
# 注: macOS 默认 bash 3.2 不兼容 `set -u` + 空数组 `${ARR[@]}`,
#     故不开 -u, 仅用 pipefail 抓命令失败。
set -o pipefail

SCRIPT_PATH="${BASH_SOURCE[0]:-$0}"
# ROOT 解析: 优先 --root=, 再用第一个非 flag positional arg, 最后默认值
ROOT_DEFAULT="$HOME/working/sourcecode"
NO_FETCH=0
DRY_RUN=0
SUMMARY_ONLY=0
STATS=0
BENCH=0
SYNC_UPSTREAM=0
PUSH=0
MAX_DEPTH=8
SKIPLIST=""
ALLOWLIST=""
MODE_RUN=1
MODE_INSTALL=0
MODE_MIGRATE=0
MODE_HELP=0
ROOT="$ROOT_DEFAULT"
for arg in "$@"; do
  case "$arg" in
    --no-fetch)      NO_FETCH=1 ;;
    --dry-run)       DRY_RUN=1 ;;
    --summary)       SUMMARY_ONLY=1 ;;
    --stats)         STATS=1 ;;
    --bench)         BENCH=1 ;;
    --sync-upstream) SYNC_UPSTREAM=1 ;;
    --push)          PUSH=1 ;;
    --install-deps)  MODE_RUN=0; MODE_INSTALL=1 ;;
    --migrate-tools) MODE_RUN=0; MODE_MIGRATE=1 ;;
    --help|-h)       MODE_RUN=0; MODE_HELP=1 ;;
    --max-depth=*)   MAX_DEPTH="${arg#--max-depth=}" ;;
    --skiplist=*)    SKIPLIST="${arg#--skiplist=}" ;;
    --allowlist=*)   ALLOWLIST="${arg#--allowlist=}" ;;
    --root=*)        ROOT="${arg#--root=}" ;;
    -*)              ;;
    *)               ROOT="$arg" ;;
  esac
done

have() { command -v "$1" >/dev/null 2>&1; }
HAVE_FD=$(have fd && echo 1 || echo 0)
HAVE_RG=$(have rg && echo 1 || echo 0)
HAVE_EZA=$(have eza && echo 1 || echo 0)
HAVE_BAT=$(have bat && echo 1 || echo 0)
HAVE_DELTA=$(have delta && echo 1 || echo 0)
HAVE_DUST=$(have dust && echo 1 || echo 0)
HAVE_TOKEI=$(have tokei && echo 1 || echo 0)
HAVE_HF=$(have hyperfine && echo 1 || echo 0)
HAVE_JUST=$(have just && echo 1 || echo 0)

if [ -t 1 ]; then
  C_RED=$'\033[31m'; C_GRN=$'\033[32m'; C_YEL=$'\033[33m'
  C_BLU=$'\033[34m'; C_MAG=$'\033[35m'; C_DIM=$'\033[2m'
  C_BLD=$'\033[1m'; C_OFF=$'\033[0m'
else
  C_RED=; C_GRN=; C_YEL=; C_BLU=; C_MAG=; C_DIM=; C_BLD=; C_OFF=
fi
ok()   { echo "${C_GRN}✓${C_OFF} $*"; }
warn() { echo "${C_YEL}⚠${C_OFF} $*"; }
err()  { echo "${C_RED}✗${C_OFF} $*"; }
info() { echo "${C_BLU}▶${C_OFF} $*"; }
dim()  { echo "${C_DIM}$*${C_OFF}"; }

mkdir -p /tmp/claude-tasks
LOG="/tmp/claude-tasks/git-batch-sync-$(date +%Y%m%d-%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

# ---- alt-mode dispatch (skip main flow) ------------------------------------
print_help() {
  cat <<'EOF'
git-batch-sync — 批量同步 + fork upstream + 冲突自动解决

Usage:
  git-batch-sync.sh [ROOT_DIR] [OPTIONS]

Main run:
  --summary            仅扫描, 列出每个 repo 状态 (read-only)
  --dry-run             显示会做什么, 不真跑
  --no-fetch            跳过 fetch, 用缓存 refs
  --sync-upstream       fork 项目同步 upstream 后再 pull origin
  --push                更新后 git push origin <branch>

Filters:
  --skiplist=<file>     黑名单: 跳过这些路径 (一行一个, 支持 prefix/*)
  --allowlist=<file>    白名单: 只跑这些路径 (其他全跳过)

Tools & diagnostics:
  --install-deps        一键安装 fd/ripgrep/eza/bat/delta/dust/tokei/hyperfine/just
  --migrate-tools       输出 PATH 中低效能工具 vs rust 替代品对照
  --stats               tokei LOC 统计
  --bench               hyperfine fd-vs-find 真实 benchmark

Other:
  --max-depth=N         fd/find 扫描深度 (default 8)
  --root=PATH           扫描根目录
  -h, --help            显示此帮助

Conflict policy:
  lockfiles / deps / generated / tooling → 自动 --theirs
  其他代码冲突 → rebase abort + 列出文件给人工

Exit codes:
  0 = OK / all updated
  1 = errors or unresolved conflicts
  2 = no repos found after filters

Examples:
  git-batch-sync.sh ~/code --summary
  git-batch-sync.sh ~/code --skiplist=~/.gbs-skiplist
  git-batch-sync.sh ~/code --allowlist=~/work-repos.txt --sync-upstream --push
  git-batch-sync.sh --install-deps
  git-batch-sync.sh --migrate-tools
EOF
}

install_deps() {
  echo "${C_BLD}── install dependencies ──${C_OFF}"
  if ! command -v brew >/dev/null 2>&1; then
    err "Homebrew 缺失"
    echo "  安装: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    return 1
  fi
  local CORE=(fd ripgrep)
  local OPTIONAL=(eza bat delta dust procs hyperfine tokei just)
  echo "  [CORE]"
  for t in "${CORE[@]}"; do
    if command -v "$t" >/dev/null 2>&1; then
      echo "    ${C_GRN}✓${C_OFF} $t ($(command -v $t))"
    else
      info "    brew install $t"
      brew install "$t" 2>&1 | tail -2 | sed "s/^/      /"
    fi
  done
  echo "  [OPTIONAL]"
  for t in "${OPTIONAL[@]}"; do
    if command -v "$t" >/dev/null 2>&1; then
      echo "    ${C_GRN}✓${C_OFF} $t"
    else
      info "    brew install $t"
      brew install "$t" 2>&1 | tail -2 | sed "s/^/      /"
    fi
  done
}

migrate_tools() {
  echo "${C_BLD}── tool migration ──${C_OFF}"
  echo
  printf "  ${C_DIM}%-15s %-15s %s${C_OFF}\n" "POSIX/GNU" "Rust alt" "Status"
  printf "  ${C_DIM}%-15s %-15s %s${C_OFF}\n" "---------------" "---------------" "------"

  declare -a PAIRS=(
    "find:fd"
    "grep:rg"
    "cat:bat"
    "ls:eza"
    "diff:delta"
    "du:dust"
    "ps:procs"
    "top:btop"
    "time:hyperfine"
    "wc:tokei"
    "make:just"
    "sed:sd"
    "curl:xh"
  )

  for pair in "${PAIRS[@]}"; do
    legacy="${pair%:*}"
    modern="${pair#*:}"
    legacy_status="MISSING"
    modern_status="MISSING"
    command -v "$legacy" >/dev/null 2>&1 && legacy_status="${C_GRN}installed${C_OFF}"
    command -v "$modern" >/dev/null 2>&1 && modern_status="${C_GRN}installed${C_OFF}" || modern_status="${C_YEL}missing${C_OFF}"
    printf "  %-15s %-15s legacy=%s modern=%s\n" "$legacy" "$modern" "$legacy_status" "$modern_status"
  done

  echo
  echo "  安装缺失的 rust 替代: git-batch-sync.sh --install-deps"
  echo "  详细对照: \$SKILL_DIR/references/tools-mapping.md"
}

# Dispatch (skip main loop)
if [ $MODE_HELP -eq 1 ]; then
  print_help
  exit 0
fi
if [ $MODE_INSTALL -eq 1 ]; then
  install_deps
  exit 0
fi
if [ $MODE_MIGRATE -eq 1 ]; then
  migrate_tools
  exit 0
fi

echo "${C_BLD}=== git-batch-sync ===${C_OFF}"
echo "ROOT          : $ROOT"
echo "FETCH         : $([ $NO_FETCH -eq 1 ] && echo 'skip' || echo 'on')"
echo "DRY_RUN       : $([ $DRY_RUN -eq 1 ] && echo 'yes' || echo 'no')"
echo "SUMMARY       : $([ $SUMMARY_ONLY -eq 1 ] && echo 'yes' || echo 'no')"
echo "SYNC_UPSTREAM : $([ $SYNC_UPSTREAM -eq 1 ] && echo 'yes' || echo 'no')"
echo "PUSH          : $([ $PUSH -eq 1 ] && echo 'yes' || echo 'no')"
echo "MAX_DEPTH     : $MAX_DEPTH"
echo "SKIPLIST      : ${SKIPLIST:-none}"
echo "ALLOWLIST     : ${ALLOWLIST:-none}"
echo "TOOLS         : fd=$HAVE_FD rg=$HAVE_RG eza=$HAVE_EZA bat=$HAVE_BAT delta=$HAVE_DELTA dust=$HAVE_DUST tokei=$HAVE_TOKEI hyperfine=$HAVE_HF just=$HAVE_JUST"
echo "LOG           : $LOG"
echo "TIME          : $(date)"
echo "----------------------------------------"

# ---- scan ------------------------------------------------------------------
# bash 3.2 兼容: 用 while-read 替代 mapfile (macOS /bin/bash 是 3.2)
REPOS=()
if [ "$HAVE_FD" = "1" ]; then
  while IFS= read -r line; do
    REPOS+=("$line")
  done < <(fd --type=dir --hidden --no-ignore --max-depth="$MAX_DEPTH" \
            --glob '.git' "$ROOT" 2>/dev/null | sort)
else
  dim "[fallback] fd missing → using find"
  while IFS= read -r line; do
    REPOS+=("$line")
  done < <(find "$ROOT" -maxdepth "$MAX_DEPTH" -type d -name '.git' \
            -not -path '*/node_modules/*' -not -path '*/.venv/*' \
            -not -path '*/vendor/*' -not -path '*/target/*' \
            -not -path '*/.gradle/*' -not -path '*/__pycache__/*' \
            2>/dev/null | sort)
fi

# ---- apply allowlist + skiplist --------------------------------------------
ALLOWLIST_MATCHED=()
SKIPPED_BY_LIST=()
SKIPPED_BY_ALLOWLIST=()

# 1. allowlist 优先: 只保留匹配路径
if [ -n "$ALLOWLIST" ] && [ -f "$ALLOWLIST" ]; then
  declare -a ALLOW_PATTERNS=()
  while IFS= read -r line; do
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "${line// }" ]] && continue
    ALLOW_PATTERNS+=("${line#"${line%%[![:space:]]*}"}")
  done < "$ALLOWLIST"

  if [ ${#ALLOW_PATTERNS[@]} -gt 0 ]; then
    FILTERED=()
    for r in "${REPOS[@]}"; do
      rel=$(dirname "$r")              # 兼容 fd trailing slash
      rel="${rel#$ROOT/}"
      match=0
      for p in "${ALLOW_PATTERNS[@]}"; do
        case "$rel" in
          "$p"|"$p"/*) match=1; break ;;
        esac
      done
      if [ "$match" -eq 1 ]; then
        FILTERED+=("$r")
        ALLOWLIST_MATCHED+=("$rel")
      else
        SKIPPED_BY_ALLOWLIST+=("$rel")
      fi
    done
    REPOS=("${FILTERED[@]}")
  fi
fi

# 2. skiplist 二次过滤
if [ -n "$SKIPLIST" ] && [ -f "$SKIPLIST" ]; then
  declare -a SKIP_PATTERNS=()
  while IFS= read -r line; do
    [[ "$line" =~ ^[[:space:]]*# ]] && continue
    [[ -z "${line// }" ]] && continue
    SKIP_PATTERNS+=("${line#"${line%%[![:space:]]*}"}")
  done < "$SKIPLIST"

  if [ ${#SKIP_PATTERNS[@]} -gt 0 ]; then
    FILTERED=()
    for r in "${REPOS[@]}"; do
      rel=$(dirname "$r")              # 兼容 fd trailing slash
      rel="${rel#$ROOT/}"
      skip=0
      for p in "${SKIP_PATTERNS[@]}"; do
        case "$rel" in
          "$p"|"$p"/*) skip=1; break ;;
        esac
      done
      if [ "$skip" -eq 1 ]; then
        SKIPPED_BY_LIST+=("$rel")
      else
        FILTERED+=("$r")
      fi
    done
    REPOS=("${FILTERED[@]}")
  fi
fi

TOTAL=${#REPOS[@]}
[ "$TOTAL" -eq 0 ] && { err "no git repos under $ROOT (after filters)"; exit 2; }
info "Repos found: $TOTAL (allowlist matched: ${#ALLOWLIST_MATCHED[@]}, skiplist excluded: ${#SKIPPED_BY_LIST[@]})"
echo "----------------------------------------"

# ---- optional: hyperfine ----------------------------------------------------
if [ "$BENCH" -eq 1 ]; then
  echo
  echo "${C_BLD}── hyperfine: fd vs find ──${C_OFF}"
  if [ "$HAVE_HF" = "1" ]; then
    hyperfine --warmup 1 --shell=bash \
      "fd --type=dir --hidden --no-ignore --max-depth=$MAX_DEPTH --glob '.git' $ROOT >/dev/null" \
      "find $ROOT -maxdepth $MAX_DEPTH -type d -name .git >/dev/null" \
      2>&1
  else
    warn "hyperfine missing → brew install hyperfine"
  fi
  echo
fi

# ---- optional: tokei stats --------------------------------------------------
if [ "$STATS" -eq 1 ]; then
  echo
  echo "${C_BLD}── tokei: language stats ──${C_OFF}"
  if [ "$HAVE_TOKEI" = "1" ]; then
    tokei "$ROOT" --exclude '*.min.js' --exclude 'dist' --exclude 'build' \
      --exclude 'node_modules' --exclude '.venv' --exclude 'vendor' \
      --exclude 'target' --exclude '.gradle' --exclude '__pycache__' \
      2>/dev/null | head -40
  else
    warn "tokei missing → brew install tokei"
  fi
  echo
fi

# ---- autoresolve patterns --------------------------------------------------
AUTORESOLVE_PATTERNS=(
  'package-lock.json' 'yarn.lock' 'pnpm-lock.yaml' 'Cargo.lock'
  'poetry.lock' 'composer.lock' 'Gemfile.lock' 'go.sum'
  '.DS_Store' '*.min.js' '*.min.css' 'dist/*' 'build/*'
  '.idea/*' '.vscode/*'
)

grep_q() {
  if [ "$HAVE_RG" = "1" ]; then
    rg -q --no-heading --no-line-number "$1"
  else
    grep -qiE "$1" /dev/stdin
  fi
}

# ---- counters --------------------------------------------------------------
OK=0; UPDATED=0; DIRTY=0; CONFLICT=0; ERROR=0; SKIPPED=0
FORK_TOTAL=0; FORK_SYNCED=0; PUSHED=0
FETCH_FAILED=()
RETRY_OK=0; RETRY_FAILED=()
START=$(date +%s)
i=0
for gitdir in "${REPOS[@]}"; do
  i=$((i+1))
  repo=$(dirname "$gitdir")     # 兼容 fd 带 trailing slash (e.g. /path/.git/)
  rel="${repo#$ROOT/}"
  echo
  echo "${C_BLD}[$i/$TOTAL]${C_OFF} ${C_BLU}$rel${C_OFF}"

  cd "$repo" || { err "cd failed"; ERROR=$((ERROR+1)); continue; }

  # ---- fork detection ------------------------------------------------------
  is_fork=0
  upstream_url=$(git config --get remote.upstream.url 2>/dev/null)
  if [ -n "$upstream_url" ]; then
    is_fork=1
    FORK_TOTAL=$((FORK_TOTAL+1))
    echo "  ${C_MAG}⊟ fork${C_OFF} upstream: $upstream_url"
  fi

  # ---- dirty ---------------------------------------------------------------
  dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  [ "$dirty" -gt 0 ] && { warn "dirty: $dirty files"; DIRTY=$((DIRTY+1)); }

  # ---- fetch origin --------------------------------------------------------
  if [ $NO_FETCH -eq 0 ]; then
    if [ $DRY_RUN -eq 0 ]; then
      fetch_out=$(git fetch origin --prune --tags 2>&1)
      echo "$fetch_out" | sed "s/^/  ${C_DIM}/; s/\$/${C_OFF}/"
      if echo "$fetch_out" | grep_q 'Connection closed|Could not read from remote|fatal: unable to access|Could not resolve host|Connection reset|Connection timed out'; then
        FETCH_FAILED+=("$rel")
        warn "fetch failed → retry queue"
      fi
    else
      dim "  [dry-run] fetch origin"
    fi
  fi

  # ---- fork: fetch upstream + failure detection ----------------------------
  if [ "$is_fork" = "1" ] && [ "$SYNC_UPSTREAM" = "1" ] && [ $DRY_RUN -eq 0 ]; then
    ups_out=$(git fetch upstream --prune --tags 2>&1)
    echo "$ups_out" | sed "s/^/    ${C_DIM}/; s/\$/${C_OFF}/"
    if echo "$ups_out" | grep_q 'Connection closed|Could not read from remote|fatal: unable to access|Could not resolve host|Connection reset|Connection timed out'; then
      [[ ! " ${FETCH_FAILED[@]} " =~ " $rel " ]] && FETCH_FAILED+=("$rel")
      warn "upstream fetch failed → retry queue"
    fi
  fi

  # ---- branch + upstream (origin side) ------------------------------------
  branch=$(git symbolic-ref --short HEAD 2>/dev/null)
  if [ -z "$branch" ]; then
    dim "  — detached HEAD, skip"; SKIPPED=$((SKIPPED+1)); continue
  fi
  origin_upstream=$(git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>/dev/null)
  if [ -z "$origin_upstream" ]; then
    dim "  — no upstream on $branch, skip"; SKIPPED=$((SKIPPED+1)); continue
  fi
  ahead=$(git rev-list --count "$origin_upstream..HEAD" 2>/dev/null)
  behind=$(git rev-list --count "HEAD..$origin_upstream" 2>/dev/null)
  echo "  branch=${C_BLD}$branch${C_OFF} ahead=$ahead behind=$behind"

  # ---- FORK: sync upstream first ------------------------------------------
  fork_synced=0
  fork_conflict_files=()

  if [ "$is_fork" = "1" ] && [ "$SYNC_UPSTREAM" = "1" ]; then
    if [ $DRY_RUN -eq 0 ]; then
      git fetch upstream --prune --tags 2>&1 | sed "s/^/    ${C_DIM}/; s/\$/${C_OFF}/" || true
      if git rev-parse --verify "upstream/$branch" >/dev/null 2>&1; then
        upstream_ahead=$(git rev-list --count "HEAD..upstream/$branch" 2>/dev/null)
        echo "  upstream/$branch ahead by $upstream_ahead"
        if [ "$upstream_ahead" -gt 0 ]; then
          # stash if dirty
          stashed=0
          if [ "$dirty" -gt 0 ]; then
            git stash push -u -m "gbs-upstream-$(date +%s)" >/dev/null 2>&1 && stashed=1
          fi
          out=$(git rebase "upstream/$branch" 2>&1)
          echo "$out" | sed "s/^/    /"
          if echo "$out" | grep_q 'CONFLICT|cannot (reapply|apply)|conflict'; then
            warn "  upstream rebase CONFLICT"
            conflicts=$(git diff --name-only --diff-filter=U 2>/dev/null)
            auto_ok=0; auto_fail=0
            for f in $conflicts; do
              match=0
              for pat in "${AUTORESOLVE_PATTERNS[@]}"; do
                [[ "$f" == $pat ]] && match=1 && break
              done
              if [ "$match" -eq 1 ]; then
                dim "    ↪ theirs: $f"
                git checkout --theirs -- "$f" 2>/dev/null && git add "$f"
                auto_ok=$((auto_ok+1))
              else
                err "    ✗ manual: $f"
                fork_conflict_files+=("$f")
                auto_fail=$((auto_fail+1))
              fi
            done
            if [ "$auto_fail" -eq 0 ]; then
              GIT_EDITOR=true git rebase --continue 2>&1 | sed "s/^/    /"
              ok "  upstream rebase auto-resolved ($auto_ok)"
              fork_synced=1; FORK_SYNCED=$((FORK_SYNCED+1))
            else
              git rebase --abort 2>&1 | sed "s/^/    /" || true
              err "  upstream rebase aborted, manual fix needed"
              CONFLICT=$((CONFLICT+1))
            fi
          else
            ok "  upstream rebased"
            fork_synced=1; FORK_SYNCED=$((FORK_SYNCED+1))
          fi
          [ "$stashed" -eq 1 ] && git stash pop >/dev/null 2>&1 || true
        else
          dim "  upstream/$branch: already in sync"
        fi
      else
        dim "  no upstream/$branch"
      fi
    else
      dim "  [dry-run] fetch upstream + rebase upstream/$branch"
    fi
  fi

  # ---- refresh ahead/behind after upstream sync ---------------------------
  if [ "$fork_synced" = "1" ]; then
    ahead=$(git rev-list --count "$origin_upstream..HEAD" 2>/dev/null)
    behind=$(git rev-list --count "HEAD..$origin_upstream" 2>/dev/null)
    echo "  post-upstream: ahead=$ahead behind=$behind"
  fi

  # ---- summary mode -------------------------------------------------------
  if [ "$behind" -eq 0 ] && [ "$ahead" -eq 0 ]; then
    ok "up-to-date"; OK=$((OK+1))
    # still try push if requested and ahead>0 was reset; check if push needed
    if [ "$PUSH" = "1" ] && [ "$is_fork" = "1" ]; then
      if [ $DRY_RUN -eq 1 ]; then
        dim "  [dry-run] git push origin $branch"
      else
        git push origin "$branch" 2>&1 | sed "s/^/    /"
        PUSHED=$((PUSHED+1))
      fi
    fi
    continue
  fi

  if [ $SUMMARY_ONLY -eq 1 ]; then
    warn "needs update (behind=$behind)"
    continue
  fi

  # ---- main pull: ff-only → rebase --autostash ----------------------------
  stashed=0
  if [ "$dirty" -gt 0 ] && [ $DRY_RUN -eq 0 ]; then
    git stash push -u -m "gbs-origin-$(date +%s)" >/dev/null 2>&1 && stashed=1
  fi

  if [ $DRY_RUN -eq 1 ]; then
    dim "  [dry-run] git pull --ff-only"
    continue
  fi

  if git pull --ff-only 2>&1 | sed "s/^/  /"; then
    ok "fast-forwarded"; UPDATED=$((UPDATED+1))
    [ "$stashed" -eq 1 ] && git stash pop >/dev/null 2>&1 || true
  else
    warn "ff-only failed → rebase --autostash"
    pull_out=$(git pull --rebase --autostash 2>&1)
    echo "$pull_out" | sed "s/^/  /"
    if echo "$pull_out" | grep_q 'CONFLICT|cannot (reapply|apply)|conflict'; then
      warn "CONFLICT, attempting autoresolve..."
      conflicts=$(git diff --name-only --diff-filter=U 2>/dev/null)
      auto_ok=0; auto_fail=0; fails=()
      for f in $conflicts; do
        match=0
        for pat in "${AUTORESOLVE_PATTERNS[@]}"; do
          [[ "$f" == $pat ]] && match=1 && break
        done
        if [ "$match" -eq 1 ]; then
          dim "    ↪ theirs: $f"
          git checkout --theirs -- "$f" 2>/dev/null && git add "$f"
          auto_ok=$((auto_ok+1))
        else
          err "    ✗ manual: $f"
          fails+=("$f"); auto_fail=$((auto_fail+1))
        fi
      done
      if [ "$auto_fail" -eq 0 ]; then
        GIT_EDITOR=true git rebase --continue 2>&1 | sed "s/^/    /"
        ok "auto-resolved ($auto_ok files)"
        UPDATED=$((UPDATED+1))
      else
        git rebase --abort 2>&1 | sed "s/^/    /" || true
        err "unresolved: ${#fails[@]} → $(IFS=,; echo "${fails[*]}")"
        CONFLICT=$((CONFLICT+1))
      fi
    else
      ok "rebased"; UPDATED=$((UPDATED+1))
    fi
    [ "$stashed" -eq 1 ] && { git stash pop >/dev/null 2>&1 || warn "stash pop conflict (run: git stash list)"; }
  fi

  # ---- push back to origin if requested -----------------------------------
  if [ "$PUSH" = "1" ] && [ $DRY_RUN -eq 0 ]; then
    if git push origin "$branch" 2>&1 | sed "s/^/  /"; then
      ok "pushed → origin/$branch"; PUSHED=$((PUSHED+1))
    else
      err "push failed (rejected?)"
    fi
  elif [ "$PUSH" = "1" ] && [ $DRY_RUN -eq 1 ]; then
    dim "  [dry-run] git push origin $branch"
  fi
done

# ---- retry pass: re-fetch failed repos (proxy/transient errors) ----------
if [ ${#FETCH_FAILED[@]} -gt 0 ]; then
  echo
  echo "${C_BLD}========================================${C_OFF}"
  echo "${C_BLD}Retry pass: ${#FETCH_FAILED[@]} repos (proxy/transient)${C_OFF}"
  echo "${C_BLD}========================================${C_OFF}"
  for rel in "${FETCH_FAILED[@]}"; do
    repo=$(dirname "$gitdir")
    [ -d "$repo" ] || continue
    cd "$repo" || continue
    sleep 1
    echo
    info "retry: $rel"
    retry_out=$(git fetch origin --prune --tags 2>&1)
    rc=$?
    if [ $rc -ne 0 ] || echo "$retry_out" | grep_q 'Connection closed|Could not read|fatal: unable|Could not resolve|Connection reset|Connection timed out'; then
      RETRY_FAILED+=("$rel")
      err "still failing"
      echo "$retry_out" | sed "s/^/    /"
    else
      echo "$retry_out" | sed "s/^/    ${C_DIM}/; s/\$/${C_OFF}/"
      # Try ff-only pull now that fetch succeeded
      branch=$(git symbolic-ref --short HEAD 2>/dev/null)
      upstream=$(git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>/dev/null)
      if [ -n "$branch" ] && [ -n "$upstream" ]; then
        behind=$(git rev-list --count "HEAD..$upstream" 2>/dev/null)
        if [ "${behind:-0}" -gt 0 ]; then
          if git pull --ff-only 2>&1 | sed "s/^/    /"; then
            ok "retry: ff-only pulled"
            RETRY_OK=$((RETRY_OK+1)); UPDATED=$((UPDATED+1))
          else
            RETRY_FAILED+=("$rel")
            err "retry: ff-only failed"
          fi
        else
          ok "retry: already up-to-date"
          RETRY_OK=$((RETRY_OK+1))
        fi
      fi
    fi
  done
fi

ELAPSED=$(( $(date +%s) - START ))

# ---- summary ---------------------------------------------------------------
echo
echo "${C_BLD}========================================${C_OFF}"
echo "${C_BLD}Summary${C_OFF}"
echo "${C_BLD}========================================${C_OFF}"
printf "Total          : %d\n" "$TOTAL"
printf "${C_MAG}Forks          : %d (synced=%d)${C_OFF}\n" "$FORK_TOTAL" "$FORK_SYNCED"
printf "${C_GRN}Up-to-date     : %d${C_OFF}\n" "$OK"
printf "${C_BLU}Updated        : %d${C_OFF}\n" "$UPDATED"
printf "${C_BLU}Pushed         : %d${C_OFF}\n" "$PUSHED"
printf "${C_YEL}Dirty          : %d${C_OFF}\n" "$DIRTY"
printf "${C_RED}Conflicts      : %d${C_OFF}\n" "$CONFLICT"
printf "${C_YEL}FetchFailed    : %d (retry_ok=%d retry_failed=%d)${C_OFF}\n" "${#FETCH_FAILED[@]}" "$RETRY_OK" "${#RETRY_FAILED[@]}"
printf "Skipped        : %d\n" "$SKIPPED"
printf "Errors         : %d\n" "$ERROR"
printf "Skiplist       : %d repos excluded\n" "${#SKIPPED_BY_LIST[@]}"
if [ -n "$ALLOWLIST" ] && [ -f "$ALLOWLIST" ]; then
  printf "Allowlist      : %d matched, %d skipped\n" "${#ALLOWLIST_MATCHED[@]}" "${#SKIPPED_BY_ALLOWLIST[@]}"
fi
printf "Elapsed        : %ds\n" "$ELAPSED"
printf "Log            : %s\n" "$LOG"

# ---- write failed list for later inspection / manual retry ----------------
if [ ${#RETRY_FAILED[@]} -gt 0 ]; then
  FAIL_FILE="/tmp/claude-tasks/git-batch-sync-failed-$(date +%Y%m%d-%H%M%S).txt"
  printf '%s\n' "${RETRY_FAILED[@]}" > "$FAIL_FILE"
  echo
  err "retry still failing: ${#RETRY_FAILED[@]} repos"
  err "list saved: $FAIL_FILE"
  echo "  manual retry: bash $SCRIPT_PATH <root> --no-fetch"
  printf '  %s\n' "${RETRY_FAILED[@]}" | sed "s/^/  - /"
fi

if [ "$HAVE_DUST" = "1" ] && [ -d "$ROOT" ]; then
  echo
  dim "── dust top-level ──"
  dust -d 1 "$ROOT" 2>/dev/null | head -15
fi
