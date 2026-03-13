#!/usr/bin/env python3
"""
Test Skill Loader
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from skill_cache import get_skill_cache
from skill_router import SkillRouter

# 项目根目录
project_root = Path(__file__).parent.parent.parent

print("=" * 60)
print("Skill Loader 测试")
print("=" * 60)

# 测试缓存
print("\n1️⃣  测试缓存系统...")
cache = get_skill_cache(project_root, auto_watch=False)
stats = cache.get_index_stats()
print(f"   技能总数：{stats['total_skills']}")
print(f"   缓存大小：{stats['cache_file_size']:,} bytes")

# 测试搜索
print("\n2️⃣  测试搜索功能...")
query = "code review"
results = cache.search(query, top_n=5)
print(f"   查询：{query}")
print(f"   结果数：{len(results)}")
for r in results:
    print(f"     - [{r['score']}分] {r['name']}")

# 测试路由
print("\n3️⃣  测试路由功能...")
router = SkillRouter()
router.initialize()

test_queries = [
    "fix the bug in login",
    "add a new feature for user management",
    "refactor the database layer",
]

for q in test_queries:
    result = router.route(q, top_n=3)
    print(f"\n   查询：{q}")
    print(f"   复杂度：{result['complexity']}")
    if result['primary_skill']:
        m = result['primary_skill']
        print(f"   推荐：{m.skill_name} ({m.score:.1f}分)")
        print(f"   理由：{m.recommended_reason[:60]}...")

print("\n" + "=" * 60)
print("测试完成!")
print("=" * 60)
