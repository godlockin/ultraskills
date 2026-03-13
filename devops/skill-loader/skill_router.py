#!/usr/bin/env python3
"""
Skill Router - 技能路由和语义匹配引擎

功能:
1. 基于语义的技能匹配（关键词 + 向量相似度）
2. 智能路由（根据任务类型推荐技能）
3. 技能组合推荐（多技能协作场景）
"""

import json
import math
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import Counter

# 导入缓存模块
from skill_cache import SkillIndexCache, SkillMetadata, get_skill_cache


@dataclass
class MatchResult:
    """匹配结果"""
    skill_id: str
    skill_name: str
    score: float
    match_type: str  # exact, keyword, semantic
    matched_fields: List[str]
    recommended_reason: str


class KeywordMatcher:
    """关键词匹配器"""

    # 预定义的技能类别关键词
    CATEGORY_KEYWORDS = {
        "engineering": ["code", "git", "test", "refactor", "debug", "review", "api", "database"],
        "productivity": ["automation", "script", "download", "convert", "process", "batch"],
        "devops": ["deploy", "docker", "kubernetes", "ci/cd", "pipeline", "infrastructure"],
        "creative": ["design", "image", "video", "art", "generate", "create"],
        "agent": ["agent", "multi-agent", "workflow", "orchestration", "autonomous"],
    }

    # 任务类型到技能的映射
    TASK_TYPE_MAPPING = {
        "bug_fix": ["debugging", "systematic-debugging", "security-reviewer"],
        "feature": ["test-driven-development", "writing-plans", "frontend-design"],
        "refactor": ["code-simplifier", "security-reviewer", "receiving-code-review"],
        "review": ["requesting-code-review", "verification-before-completion"],
        "research": ["brainstorming", "agent-reach"],
        "deploy": ["finishing-a-development-branch", "commit-commands"],
    }

    def __init__(self):
        # 构建倒排索引
        self.tag_index: Dict[str, List[str]] = {}
        self.name_index: Dict[str, List[str]] = {}
        self.desc_index: Dict[str, List[str]] = {}

    def build_index(self, skills: Dict[str, SkillMetadata]):
        """构建倒排索引"""
        for skill_id, skill in skills.items():
            # 索引 tags
            for tag in skill.tags:
                tag_lower = tag.lower()
                if tag_lower not in self.tag_index:
                    self.tag_index[tag_lower] = []
                self.tag_index[tag_lower].append(skill_id)

            # 索引 name (分词)
            name_words = self._tokenize(skill.name)
            for word in name_words:
                if word not in self.name_index:
                    self.name_index[word] = []
                self.name_index[word].append(skill_id)

            # 索引 description (分词)
            desc_words = self._tokenize(skill.description)
            for word in desc_words:
                if word not in self.desc_index:
                    self.desc_index[word] = []
                self.desc_index[word].append(skill_id)

    def _tokenize(self, text: str) -> List[str]:
        """文本分词"""
        # 转小写，拆分连字符和空格
        text = text.lower()
        # 保留字母数字和连字符
        text = re.sub(r'[^\w\s-]', ' ', text)
        # 拆分
        words = text.split()
        # 过滤短词
        return [w for w in words if len(w) > 2]

    def match(self, query: str, skills: Dict[str, SkillMetadata]) -> List[MatchResult]:
        """匹配查询"""
        query_lower = query.lower()
        query_words = self._tokenize(query)
        results = []

        for skill_id, skill in skills.items():
            score = 0.0
            matched_fields = []
            match_type = "none"

            # 1. 完全匹配 name
            if skill.name.lower() == query_lower:
                score += 100.0
                matched_fields.append("name_exact")
                match_type = "exact"

            # 2. name 包含查询
            elif query_lower in skill.name.lower():
                score += 50.0
                matched_fields.append("name_contains")
                if match_type != "exact":
                    match_type = "keyword"

            # 3. name 单词匹配
            name_words = self._tokenize(skill.name)
            for word in query_words:
                if word in name_words:
                    score += 20.0
                    matched_fields.append(f"name_word:{word}")
                    if match_type == "none":
                        match_type = "keyword"

            # 4. tag 匹配
            for tag in skill.tags:
                tag_lower = tag.lower()
                if query_lower == tag_lower:
                    score += 30.0
                    matched_fields.append(f"tag_exact:{tag}")
                elif query_lower in tag_lower or tag_lower in query_lower:
                    score += 15.0
                    matched_fields.append(f"tag_partial:{tag}")

                # 标签单词匹配
                tag_words = self._tokenize(tag)
                for word in query_words:
                    if word in tag_words:
                        score += 10.0
                        matched_fields.append(f"tag_word:{word}")

            # 5. description 匹配
            desc_words = self._tokenize(skill.description)
            for word in query_words:
                if word in desc_words:
                    score += 5.0
                    matched_fields.append(f"desc_word:{word}")

            # 6. 类别关键词匹配
            for category, keywords in self.CATEGORY_KEYWORDS.items():
                if category in skill.path.lower():
                    for kw in keywords:
                        if kw in query_words:
                            score += 8.0
                            matched_fields.append(f"category:{category}")

            # 7. 任务类型识别
            task_type = self._detect_task_type(query)
            if task_type and skill_id in self.TASK_TYPE_MAPPING.get(task_type, []):
                score += 40.0
                matched_fields.append(f"task_type:{task_type}")

            if score > 0:
                results.append(MatchResult(
                    skill_id=skill_id,
                    skill_name=skill.name,
                    score=score,
                    match_type=match_type,
                    matched_fields=matched_fields,
                    recommended_reason=self._generate_reason(matched_fields, skill)
                ))

        # 按分数排序
        results.sort(key=lambda x: x.score, reverse=True)
        return results

    def _detect_task_type(self, query: str) -> Optional[str]:
        """检测任务类型"""
        query_lower = query.lower()

        if any(w in query_lower for w in ["bug", "fix", "error", "fail", "broken", "issue"]):
            return "bug_fix"
        elif any(w in query_lower for w in ["add", "new", "feature", "implement", "create"]):
            return "feature"
        elif any(w in query_lower for w in ["refactor", "clean", "simplify", "improve"]):
            return "refactor"
        elif any(w in query_lower for w in ["review", "check", "audit", "verify"]):
            return "review"
        elif any(w in query_lower for w in ["research", "explore", "investigate", "find"]):
            return "research"
        elif any(w in query_lower for w in ["deploy", "release", "ship", "merge", "push"]):
            return "deploy"

        return None

    def _generate_reason(self, matched_fields: List[str], skill: SkillMetadata) -> str:
        """生成推荐理由"""
        reasons = []

        for field in matched_fields:
            if field.startswith("name_exact"):
                reasons.append(f"名称完全匹配")
            elif field.startswith("name_contains"):
                reasons.append(f"名称包含关键词")
            elif field.startswith("name_word"):
                reasons.append(f"名称匹配：{field.split(':')[1]}")
            elif field.startswith("tag_exact"):
                reasons.append(f"标签匹配：{field.split(':')[1]}")
            elif field.startswith("tag_partial"):
                reasons.append(f"标签部分匹配：{field.split(':')[1]}")
            elif field.startswith("category"):
                reasons.append(f"属于相关类别：{field.split(':')[1]}")
            elif field.startswith("task_type"):
                reasons.append(f"适用于：{field.split(':')[1]}场景")

        if not reasons:
            reasons.append(f"描述中包含相关关键词")

        return "；".join(reasons) + f" - {skill.description[:50]}..."


class SkillRouter:
    """技能路由引擎"""

    def __init__(self, cache: SkillIndexCache = None):
        self.cache = cache or get_skill_cache(auto_watch=False)
        self.keyword_matcher = KeywordMatcher()
        self._initialized = False

    def initialize(self):
        """初始化（加载索引）"""
        skills = self.cache.get_all_skills()
        self.keyword_matcher.build_index(skills)
        self._initialized = True

    def route(self, query: str, top_n: int = 5) -> Dict:
        """
        路由查询到最匹配的技能

        Args:
            query: 用户查询或任务描述
            top_n: 返回结果数量

        Returns:
            包含匹配结果和推荐的信息
        """
        if not self._initialized:
            self.initialize()

        skills = self.cache.get_all_skills()
        matches = self.keyword_matcher.match(query, skills)

        # 检测任务复杂度
        complexity = self._analyze_complexity(query)

        # 是否需要多技能组合
        needs_composition = self._needs_composition(query)
        composition = []
        if needs_composition:
            composition = self._recommend_composition(query, matches[:top_n])

        return {
            "query": query,
            "complexity": complexity,
            "primary_skill": matches[0] if matches else None,
            "matches": [self._to_dict(m) for m in matches[:top_n]],
            "composition": composition if needs_composition else None,
            "suggested_workflow": self._suggest_workflow(query, matches[:top_n])
        }

    def _to_dict(self, match: MatchResult) -> dict:
        """转换为字典"""
        return {
            "skill_id": match.skill_id,
            "skill_name": match.skill_name,
            "score": match.score,
            "match_type": match.match_type,
            "matched_fields": match.matched_fields,
            "recommended_reason": match.recommended_reason
        }

    def _analyze_complexity(self, query: str) -> str:
        """分析任务复杂度"""
        query_lower = query.lower()

        # 简单任务关键词
        simple_indicators = ["simple", "quick", "just", "small", "minor", "fix typo"]
        if any(w in query_lower for w in simple_indicators):
            return "simple"

        # 复杂任务关键词
        complex_indicators = ["implement", "build", "create", "design", "architecture", "system"]
        if any(w in query_lower for w in complex_indicators):
            return "complex"

        # 多步骤任务
        multi_step_indicators = ["refactor", "migrate", "integrate", "end-to-end"]
        if any(w in query_lower for w in multi_step_indicators):
            return "multi-step"

        return "medium"

    def _needs_composition(self, query: str) -> bool:
        """判断是否需要多技能组合"""
        query_lower = query.lower()

        # 明确需要多技能的场景
        composition_indicators = [
            "full", "complete", "end-to-end", "from scratch",
            "implement and test", "build and deploy",
            "design and implement"
        ]

        return any(w in query_lower for w in composition_indicators)

    def _recommend_composition(self, query: str, matches: List[MatchResult]) -> List[Dict]:
        """推荐技能组合"""
        composition = []

        # 1. 规划技能
        planning_skills = ["writing-plans", "brainstorming"]
        for skill_id in planning_skills:
            if self.cache.get_skill(skill_id):
                composition.append({
                    "skill_id": skill_id,
                    "phase": "planning",
                    "reason": "制定实施计划"
                })

        # 2. 主要实现技能
        if matches:
            composition.append({
                "skill_id": matches[0].skill_id,
                "phase": "implementation",
                "reason": matches[0].recommended_reason
            })

        # 3. 验证技能
        verification_skills = ["verification-before-completion", "requesting-code-review"]
        for skill_id in verification_skills:
            if self.cache.get_skill(skill_id):
                composition.append({
                    "skill_id": skill_id,
                    "phase": "verification",
                    "reason": "验证完成质量"
                })

        return composition

    def _suggest_workflow(self, query: str, matches: List[MatchResult]) -> str:
        """建议工作流程"""
        complexity = self._analyze_complexity(query)

        if complexity == "simple":
            return "直接调用最匹配的技能完成任务"

        elif complexity == "complex":
            workflow = ["1. 使用 brainstorming 技能进行需求分析"]
            workflow.append("2. 使用 writing-plans 技能创建实施计划")
            if matches:
                workflow.append(f"3. 使用 {matches[0].skill_name} 技能实施")
            workflow.append("4. 使用 verification-before-completion 验证")
            workflow.append("5. 使用 requesting-code-review 进行代码审查")
            return "\n".join(workflow)

        else:
            workflow = ["1. 分析任务需求"]
            if matches:
                workflow.append(f"2. 调用 {matches[0].skill_name} 技能")
            workflow.append("3. 验证结果")
            return "\n".join(workflow)


# CLI 入口
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Skill Router CLI")
    parser.add_argument('command', choices=['route', 'match', 'analyze'],
                       help='命令')
    parser.add_argument('--query', '-q', required=True, help='查询/任务描述')
    parser.add_argument('--top-n', '-n', type=int, default=5, help='返回结果数量')
    args = parser.parse_args()

    router = SkillRouter()

    if args.command == 'route':
        result = router.route(args.query, top_n=args.top_n)

        print(f"\n📍 路由结果")
        print(f"查询：{result['query']}")
        print(f"复杂度：{result['complexity']}")
        print()

        if result['primary_skill']:
            print(f"🎯 主推荐技能：{result['primary_skill'].skill_name}")
            print(f"   分数：{result['primary_skill'].score}")
            print(f"   匹配类型：{result['primary_skill'].match_type}")
            print(f"   理由：{result['primary_skill'].recommended_reason}")
            print()

        if result['matches']:
            print(f"📋 匹配列表 (Top {len(result['matches'])}):")
            for i, m in enumerate(result['matches'], 1):
                print(f"  {i}. {m['skill_name']} (分数：{m['score']:.1f})")
                print(f"     {m['recommended_reason']}")
            print()

        if result['composition']:
            print(f"🔗 推荐技能组合:")
            for comp in result['composition']:
                print(f"  [{comp['phase']}] {comp['skill_id']}: {comp['reason']}")
            print()

        if result['suggested_workflow']:
            print(f"📝 建议工作流程:")
            print(result['suggested_workflow'])

    elif args.command == 'match':
        skills = router.cache.get_all_skills()
        matches = router.keyword_matcher.match(args.query, skills)

        print(f"\n🔍 匹配结果 (查询：{args.query}):\n")
        for m in matches[:args.top_n]:
            print(f"  [{m.match_type}] {m.skill_name} - {m.score:.1f}分")
            print(f"     匹配字段：{', '.join(m.matched_fields[:5])}")
            print(f"     理由：{m.recommended_reason}")
            print()


if __name__ == "__main__":
    main()
