#!/bin/bash
# BFG Repo-Cleaner 自动化清理脚本
# 用法：./cleanup_repo.sh <repo.git 路径> <操作>

set -e

REPO_PATH="${1:-.}"
ACTION="${2:-clean}"

case "$ACTION" in
    clean)
        echo "🧹 清理 Git 仓库：$REPO_PATH"
        echo "⚠️  此操作将重写 Git 历史，请确保已备份！"
        read -p "确认继续？(y/N): " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            echo "已取消"
            exit 1
        fi

        cd "$REPO_PATH"

        echo "📦 运行 git gc..."
        git reflog expire --expire=now --all
        git gc --prune=now --aggressive

        echo "✅ 清理完成！"
        echo "📊 当前仓库大小：$(du -sh . | cut -f1)"
        ;;

    size)
        echo "📊 检查仓库大小..."
        cd "$REPO_PATH"
        du -sh .

        echo ""
        echo "📦 最大的对象："
        git verify-pack -v .git/objects/pack/*.idx | \
            sort -k 3 -n -r | head -10
        ;;

    *)
        echo "用法：$0 <repo.git 路径> <操作>"
        echo ""
        echo "操作:"
        echo "  clean  - 执行垃圾回收"
        echo "  size   - 显示仓库大小"
        exit 1
        ;;
esac
