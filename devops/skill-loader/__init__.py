#!/usr/bin/env python3
"""
Skill Loader - 高效的 Skills 动态加载系统

统一入口模块，提供:
1. 索引缓存 (SkillIndexCache)
2. MCP Server 发现接口
3. 语义路由和匹配 (SkillRouter)
"""

__version__ = "1.0.0"
__author__ = "UltraSkills Team"

# 使用绝对导入
from skill_cache import (
    SkillIndexCache,
    SkillMetadata,
    CacheMetadata,
    get_skill_cache,
    compute_file_hash,
    parse_frontmatter,
)

from skill_router import (
    SkillRouter,
    KeywordMatcher,
    MatchResult,
)

__all__ = [
    # Cache
    "SkillIndexCache",
    "SkillMetadata",
    "CacheMetadata",
    "get_skill_cache",
    "compute_file_hash",
    "parse_frontmatter",
    # Router
    "SkillRouter",
    "KeywordMatcher",
    "MatchResult",
]


def get_router() -> SkillRouter:
    """获取路由引擎实例"""
    return SkillRouter()


def get_cache() -> SkillIndexCache:
    """获取缓存实例"""
    return get_skill_cache()
