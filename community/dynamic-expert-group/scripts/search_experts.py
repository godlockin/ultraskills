#!/usr/bin/env python3
"""
搜索专家脚本

根据任务描述搜索匹配的专家。
"""

import json
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).parent.parent
INDEX_FILE = SKILL_ROOT / "references" / "experts" / "all_experts.json"


def load_experts() -> dict:
    """加载专家索引"""
    if not INDEX_FILE.exists():
        print("Error: Run init_expert_lib.py first")
        sys.exit(1)
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def search_experts(query: str, top_k: int = 5) -> list[dict]:
    """搜索匹配的专家"""
    data = load_experts()
    experts = data.get('experts', [])
    by_keyword = data.get('by_keyword', {})

    # 分词查询
    query_lower = query.lower()
    query_words = query_lower.split()

    # 统计每个专家的匹配分数
    scores = {}

    for expert in experts:
        score = 0
        expert_keywords = [k.lower() for k in expert.get('trigger_keywords', [])]

        for word in query_words:
            # 精确匹配 +1
            if word in expert_keywords:
                score += 3
            # 领域匹配
            if word in expert.get('domain', '').lower():
                score += 2
            # 子领域匹配
            if word in expert.get('subdomain', '').lower():
                score += 2
            # 名字匹配
            if word in expert.get('name', '').lower():
                score += 2
            if word in expert.get('name_cn', '').lower():
                score += 2

        if score > 0:
            scores[expert['id']] = score

    # 排序
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_experts = []

    for expert_id, score in ranked[:top_k]:
        for e in experts:
            if e['id'] == expert_id:
                top_experts.append(e)
                break

    return top_experts


def main():
    if len(sys.argv) < 2:
        print("Usage: python search_experts.py <query>")
        sys.exit(1)

    query = sys.argv[1]
    experts = search_experts(query)

    print(f"🔍 Searching for: {query}")
    print(f"📋 Found {len(experts)} matching experts:\n")

    for i, e in enumerate(experts, 1):
        print(f"{i}. {e['name']} ({e['name_cn']}) - {e.get('domain', '')}")
        print(f"   {e.get('avatar', '')}")
        print()


if __name__ == "__main__":
    main()