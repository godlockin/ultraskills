#!/usr/bin/env bash
# commit.sh — Conventional Commits 格式校验 + 执行
# 用法: MESSAGE="feat: add feature" bash scripts/commit.sh [--dry-run]
set -euo pipefail

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

# 1. 检查有无 staged 内容
if ! git diff --cached --name-only | grep -q .; then
  echo "❌ 没有 staged 的内容，请先 git add"; exit 1
fi

# 2. 获取 MESSAGE（环境变量或 stdin）
if [ -z "${MESSAGE:-}" ]; then
  echo "请输入 commit message (Ctrl+D 结束):"
  MESSAGE=$(cat)
fi

# 3. 校验 Conventional Commits 格式
# 格式: type(scope): description  或  type: description
CC_PATTERN='^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?: .+'
if ! echo "$MESSAGE" | grep -qE "$CC_PATTERN"; then
  echo "❌ 不符合 Conventional Commits 格式"
  echo "   期望: type(scope): description"
  echo "   类型: feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert"
  echo "   收到: $MESSAGE"
  exit 1
fi

# 4. 执行（或 dry-run）
if $DRY_RUN; then
  echo "[DRY-RUN] git commit -m \"$MESSAGE\""
else
  git commit -m "$MESSAGE"
  echo "✅ 已提交: $MESSAGE"
fi
