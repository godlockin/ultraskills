#!/usr/bin/env python3
"""
MCP Server for Skills Discovery

提供基于 MCP 协议的技能发现、搜索和检索服务。
"""

import json
import sys
import os
from pathlib import Path
from typing import Any

# 添加父目录到路径以导入 skill_cache
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    ResourceTemplate,
)
from skill_cache import SkillIndexCache, get_skill_cache

# 服务器配置
SERVER_NAME = "skills-discovery"
SERVER_VERSION = "1.0.0"

# 初始化服务器
server = Server(SERVER_NAME)

# 全局缓存实例
_skill_cache: SkillIndexCache = None


def get_cache() -> SkillIndexCache:
    """获取或创建技能缓存实例"""
    global _skill_cache
    if _skill_cache is None:
        project_root = Path(__file__).parent.parent.parent.parent
        _skill_cache = get_skill_cache(project_root, auto_watch=True)
    return _skill_cache


@server.list_tools()
async def list_tools() -> list[Tool]:
    """列出可用的工具"""
    return [
        Tool(
            name="list_skills",
            description="List all available skills with optional filtering by category",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filter by category (engineering, productivity, devops, creative, community)"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of skills to return",
                        "default": 50
                    },
                    "include_external": {
                        "type": "boolean",
                        "description": "Include skills from external directories",
                        "default": True
                    }
                }
            }
        ),
        Tool(
            name="search_skills",
            description="Search for skills by keyword or task description",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query or task description"
                    },
                    "top_n": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_skill",
            description="Get detailed information about a specific skill",
            inputSchema={
                "type": "object",
                "properties": {
                    "skill_id": {
                        "type": "string",
                        "description": "The skill ID or name"
                    },
                    "include_content": {
                        "type": "boolean",
                        "description": "Include full skill content",
                        "default": False
                    }
                },
                "required": ["skill_id"]
            }
        ),
        Tool(
            name="get_stats",
            description="Get statistics about the skill library",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="rebuild_index",
            description="Rebuild the skill index cache (requires admin)",
            inputSchema={
                "type": "object",
                "properties": {
                    "force": {
                        "type": "boolean",
                        "description": "Force rebuild even if cache is valid",
                        "default": False
                    }
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """处理工具调用"""
    cache = get_cache()

    try:
        if name == "list_skills":
            return await handle_list_skills(cache, arguments)

        elif name == "search_skills":
            return await handle_search_skills(cache, arguments)

        elif name == "get_skill":
            return await handle_get_skill(cache, arguments)

        elif name == "get_stats":
            return await handle_get_stats(cache)

        elif name == "rebuild_index":
            return await handle_rebuild_index(cache, arguments)

        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}"}, indent=2)
            )]

    except Exception as e:
        return [TextContent(
            type="text",
            text=json.dumps({"error": str(e)}, indent=2, ensure_ascii=False)
        )]


async def handle_list_skills(cache: SkillIndexCache, arguments: dict) -> list[TextContent]:
    """处理 list_skills 请求"""
    category = arguments.get("category")
    limit = arguments.get("limit", 50)
    include_external = arguments.get("include_external", True)

    all_skills = cache.get_all_skills()
    filtered = []

    for skill_id, skill in all_skills.items():
        # 按分类过滤
        if category:
            if category.lower() not in skill.path.lower():
                continue

        # 过滤外部技能
        if not include_external and "external" in skill.path:
            continue

        filtered.append({
            "id": skill.id,
            "name": skill.name,
            "path": skill.path,
            "description": skill.description,
            "tags": skill.tags,
            "content_length": skill.content_length,
            "section_count": skill.section_count
        })

        if len(filtered) >= limit:
            break

    result = {
        "skills": filtered,
        "total": len(filtered),
        "category": category
    }

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2, ensure_ascii=False)
    )]


async def handle_search_skills(cache: SkillIndexCache, arguments: dict) -> list[TextContent]:
    """处理 search_skills 请求"""
    query = arguments.get("query", "")
    top_n = arguments.get("top_n", 10)

    if not query:
        return [TextContent(
            type="text",
            text=json.dumps({"error": "Query is required"}, indent=2)
        )]

    results = cache.search(query, top_n=top_n)

    return [TextContent(
        type="text",
        text=json.dumps({
            "query": query,
            "results": results,
            "count": len(results)
        }, indent=2, ensure_ascii=False)
    )]


async def handle_get_skill(cache: SkillIndexCache, arguments: dict) -> list[TextContent]:
    """处理 get_skill 请求"""
    skill_id = arguments.get("skill_id")
    include_content = arguments.get("include_content", False)

    if not skill_id:
        return [TextContent(
            type="text",
            text=json.dumps({"error": "skill_id is required"}, indent=2)
        )]

    skill = cache.get_skill(skill_id)

    if not skill:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Skill not found: {skill_id}"}, indent=2)
        )]

    result = {
        "id": skill.id,
        "name": skill.name,
        "path": skill.path,
        "description": skill.description,
        "tags": skill.tags,
        "content_length": skill.content_length,
        "section_count": skill.section_count,
        "last_scanned": skill.last_scanned
    }

    # 如果需要完整内容，读取文件
    if include_content:
        project_root = Path(__file__).parent.parent.parent.parent
        skill_path = project_root / skill.path
        if skill_path.exists():
            result["content"] = skill_path.read_text(encoding='utf-8')

    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2, ensure_ascii=False)
    )]


async def handle_get_stats(cache: SkillIndexCache) -> list[TextContent]:
    """处理 get_stats 请求"""
    stats = cache.get_index_stats()

    return [TextContent(
        type="text",
        text=json.dumps(stats, indent=2, ensure_ascii=False)
    )]


async def handle_rebuild_index(cache: SkillIndexCache, arguments: dict) -> list[TextContent]:
    """处理 rebuild_index 请求"""
    force = arguments.get("force", False)

    if not force and cache.get_index_stats().get("total_skills", 0) > 0:
        return [TextContent(
            type="text",
            text=json.dumps({
                "status": "skipped",
                "message": "Cache already exists. Use force=true to rebuild."
            }, indent=2)
        )]

    skills = cache.rebuild_index()

    return [TextContent(
        type="text",
        text=json.dumps({
            "status": "success",
            "total_skills": len(skills),
            "message": "Index rebuilt successfully"
        }, indent=2)
    )]


@server.list_resources()
async def list_resources() -> list[Resource]:
    """列出可用资源"""
    cache = get_cache()
    skills = cache.get_all_skills()

    resources = []
    for skill_id, skill in skills.items():
        resources.append(Resource(
            uri=f"skill://{skill_id}",
            name=skill.name,
            description=skill.description,
            mimeType="text/markdown"
        ))

    return resources


@server.read_resource()
async def read_resource(uri: str) -> str:
    """读取资源内容"""
    if uri.startswith("skill://"):
        skill_id = uri.replace("skill://", "")
        cache = get_cache()
        skill = cache.get_skill(skill_id)

        if not skill:
            raise ValueError(f"Skill not found: {skill_id}")

        # 读取技能文件内容
        project_root = Path(__file__).parent.parent.parent.parent
        skill_path = project_root / skill.path
        return skill_path.read_text(encoding='utf-8')

    raise ValueError(f"Unknown resource URI: {uri}")


async def main():
    """主入口"""
    # 初始化缓存
    get_cache()

    # 启动 MCP 服务器
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
