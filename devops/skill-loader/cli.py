#!/usr/bin/env python3
"""
Skill Loader - CLI 入口脚本
"""

import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# 直接导入 skill_cache 模块
from skill_cache import get_skill_cache

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Skill Loader CLI")
    parser.add_argument('command', choices=['rebuild', 'stats'], help='命令')
    args = parser.parse_args()

    # 项目根目录是 skill-loader 的父目录的父目录的父目录
    project_root = Path(__file__).parent.parent.parent
    cache = get_skill_cache(project_root, auto_watch=False)

    if args.command == 'rebuild':
        cache.rebuild_index()
        stats = cache.get_index_stats()
        print(f"\n✅ 索引重建完成")
        print(f"   技能总数：{stats['total_skills']}")
    elif args.command == 'stats':
        stats = cache.get_index_stats()
        print(f"\n📊 索引统计:")
        print(f"   技能总数：{stats['total_skills']}")
        print(f"   缓存版本：{stats['cache_version']}")
        print(f"   更新时间：{stats['updated_at']}")

if __name__ == "__main__":
    main()
