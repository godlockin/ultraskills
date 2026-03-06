#!/usr/bin/env python3
"""
search.py - 根据关键词搜索 Skills

从 index.json 中查找最匹配的 Skills，基于关键词加权算法计分。
"""

import json
import os
import sys
from typing import List, Dict, Any


def load_index(index_path: str = "index.json") -> Dict[str, Any]:
    """加载 skills 索引"""
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_score(query: str, skill: Dict[str, Any]) -> int:
    """
    计算查询与 skill 的匹配得分

    评分规则：
    - name 完全匹配 = 10 分
    - name 包含查询 = 5 分
    - description 包含查询 = 3 分
    - tags 匹配 = 2 分/个
    """
    query_lower = query.lower()
    score = 0

    name = skill.get("name", "").lower()
    description = skill.get("description", "").lower()
    tags = skill.get("tags", [])

    # name 完全匹配
    if name == query_lower:
        score += 10
    # name 包含查询
    elif query_lower in name:
        score += 5

    # description 包含查询
    if query_lower in description:
        score += 3

    # tags 匹配
    for tag in tags:
        if query_lower in tag.lower():
            score += 2

    return score


def search_skills(query: str, index_path: str = "index.json", top_n: int = 5) -> List[Dict[str, Any]]:
    """
    根据关键词搜索 Skills

    Args:
        query: 搜索关键词/任务描述
        index_path: index.json 路径
        top_n: 返回前 N 个结果

    Returns:
        按得分排序的匹配结果列表
    """
    index_data = load_index(index_path)
    skills = index_data.get("skills", [])

    # 计算每个 skill 的得分
    results = []
    for skill in skills:
        score = calculate_score(query, skill)
        if score > 0:
            results.append({
                **skill,
                "score": score
            })

    # 按得分排序
    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_n]


def print_results(results: List[Dict[str, Any]]) -> None:
    """打印搜索结果"""
    if not results:
        print("❌ 没有找到匹配的 Skills")
        print("\n💡 可以选择「生成新 Skill」来创建一个")
        return

    print(f"找到 {len(results)} 个匹配的 Skills:\n")
    print("=" * 60)

    for i, skill in enumerate(results, 1):
        print(f"\n#{i} [{skill['score']}分] {skill['name']}")
        print(f"   描述: {skill['description']}")
        if skill.get("tags"):
            print(f"   标签: {', '.join(skill['tags'])}")
        print(f"   路径: {skill['path']}")

    print("\n" + "=" * 60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python search.py <query>")
        print("Example: python search.py 视频处理")
        sys.exit(1)

    query = sys.argv[1]
    results = search_skills(query)
    print_results(results)


if __name__ == "__main__":
    main()