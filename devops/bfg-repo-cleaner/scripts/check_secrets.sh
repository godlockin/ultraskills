#!/bin/bash
# 检查仓库中是否包含常见敏感数据模式
# 用法：./check_secrets.sh <repo 路径>

set -e

REPO_PATH="${1:-.}"

echo "🔍 扫描敏感数据：$REPO_PATH"
echo "================================"

cd "$REPO_PATH"

# 定义敏感模式
declare -a PATTERNS=(
    "AWS 访问密钥：AKIA[0-9A-Z]{16}"
    "AWS 秘密密钥：[A-Za-z0-9/+=]{40}"
    "GitHub Token:ghp_[0-9a-zA-Z]{36}"
    "私钥头部:-----BEGIN.*PRIVATE KEY-----"
    "密码文件：password|passwd|pwd"
    "API 密钥：api[_-]?key|apikey"
)

FOUND_ISSUES=0

for pattern_desc in "${PATTERNS[@]}"; do
    IFS='：' read -r name pattern <<< "$pattern_desc"

    # 搜索 git 历史
    if git log -S "$pattern" --all --oneline 2>/dev/null | head -1; then
        echo "⚠️  发现：$name"
        FOUND_ISSUES=$((FOUND_ISSUES + 1))
    fi
done

echo "================================"
if [ $FOUND_ISSUES -gt 0 ]; then
    echo "❌ 发现 $FOUND_ISSUES 类潜在敏感数据"
    echo ""
    echo "建议操作:"
    echo "1. 使用 BFG 清理：bfg --replace-text banned.txt repo.git"
    echo "2. 或手动移除并提交"
    exit 1
else
    echo "✅ 未发现已知敏感数据模式"
fi
