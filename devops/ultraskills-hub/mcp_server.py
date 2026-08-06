#!/usr/bin/env python3
"""
ultraskills-hub MCP Server — unified skill discovery + on-demand loading.

Consumes the canonical index.json (944 skills, rebuilt via arena pipeline).
Exposes tools:
  - search_skills(query, top_n) → ranked matches with id, path, score, tags
  - get_skill(skill_id, include_content) → metadata + optional full SKILL.md
  - list_categories() → cluster hierarchy
  - list_winners(top_n) → arena top performers
  - refresh_index() → trigger arena rebuild (subprocess)

Loading semantics:
  - Metadata (frontmatter) loaded from index.json (~immediate).
  - Full SKILL.md content read on demand via get_skill(include_content=true).
  This avoids auto-loading 944 frontmatter blocks into context.
"""

import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

SERVER_NAME = "ultraskills-hub"
SERVER_VERSION = "2.0.0"

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
INDEX_FILE = REPO_ROOT / "index.json"

server = Server(SERVER_NAME)
_index_cache: dict[str, Any] | None = None

_REFRESH_INDEX_RUNNER = """
import subprocess
import sys

for script in sys.argv[2:]:
    subprocess.run([sys.executable, script], check=True)
"""


def _load_index() -> dict[str, Any]:
    global _index_cache
    if _index_cache is not None:
        return _index_cache
    if not INDEX_FILE.exists():
        raise FileNotFoundError(f"index.json not found at {INDEX_FILE}")
    with INDEX_FILE.open(encoding="utf-8") as f:
        _index_cache = json.load(f)
    return _index_cache


def _invalidate() -> None:
    global _index_cache
    _index_cache = None


def _arena(skill: dict) -> dict:
    return skill.get("arena") or {}


def _search_skills(query: str, top_n: int = 10) -> list[dict]:
    idx = _load_index()
    q = query.lower().strip()
    terms = [t for t in q.split() if t]
    if not terms:
        return []

    scored: list[tuple[float, dict]] = []
    for s in idx.get("skills", []):
        score = 0.0
        sid = (s.get("id") or "").lower()
        desc = (s.get("description") or "").lower()
        tags = [t.lower() for t in (s.get("tags") or [])]
        arena_score = _arena(s).get("score") or 0

        for t in terms:
            if t == sid or t in sid:
                score += 20
            elif t in desc:
                score += 2
            elif any(t in tag for tag in tags):
                score += 6
        score += min(arena_score, 10) * 0.5
        if score > 0:
            scored.append((score, s))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [
        {
            "id": s.get("id"),
            "path": s.get("path"),
            "description": (s.get("description") or "")[:200],
            "tags": s.get("tags", []),
            "arena_score": _arena(s).get("score"),
            "arena_rank": _arena(s).get("rank"),
            "is_winner": _arena(s).get("is_winner"),
            "match_score": round(score, 2),
        }
        for score, s in scored[:top_n]
    ]


def _get_skill(skill_id: str, include_content: bool = False) -> dict:
    idx = _load_index()
    skill = next(
        (s for s in idx.get("skills", []) if s.get("id") == skill_id),
        None,
    )
    if skill is None:
        return {"error": f"Skill not found: {skill_id}"}

    arena = _arena(skill)
    result = {
        "id": skill.get("id"),
        "name": skill.get("name"),
        "path": skill.get("path"),
        "description": skill.get("description"),
        "tags": skill.get("tags", []),
        "arena_score": arena.get("score"),
        "arena_rank": arena.get("rank"),
        "is_winner": arena.get("is_winner"),
        "arena_cluster": arena.get("cluster_name"),
    }

    if include_content:
        skill_path = REPO_ROOT / skill.get("path", "")
        if skill_path.exists():
            result["content"] = skill_path.read_text(encoding="utf-8")
        else:
            result["content_error"] = f"Path not found: {skill_path}"

    return result


def _list_categories() -> list[dict]:
    idx = _load_index()
    return idx.get("clusters", [])


def _list_winners(top_n: int = 20) -> list[dict]:
    idx = _load_index()
    winners = [s for s in idx.get("skills", []) if _arena(s).get("is_winner")]
    winners.sort(key=lambda s: _arena(s).get("score", 0), reverse=True)
    return [
        {
            "id": w.get("id"),
            "path": w.get("path"),
            "arena_score": _arena(w).get("score"),
            "arena_rank": _arena(w).get("rank"),
            "arena_cluster": _arena(w).get("cluster_name"),
        }
        for w in winners[:top_n]
    ]


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_skills",
            description="Search UltraSkills (944 skills) by keyword/intent. Returns ranked matches with id, path, arena_score, tags. Use this before Skill tool to discover skills.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query or task description"},
                    "top_n": {"type": "integer", "default": 10, "description": "Max results"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_skill",
            description="Get full SKILL.md content for a specific skill by id. Use after search_skills to load the actual skill body before invoking it.",
            inputSchema={
                "type": "object",
                "properties": {
                    "skill_id": {"type": "string"},
                    "include_content": {"type": "boolean", "default": False},
                },
                "required": ["skill_id"],
            },
        ),
        Tool(
            name="list_categories",
            description="List all skill clusters/categories from arena pipeline.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="list_winners",
            description="List top arena winners (best skill per cluster).",
            inputSchema={
                "type": "object",
                "properties": {
                    "top_n": {"type": "integer", "default": 20},
                },
            },
        ),
        Tool(
            name="refresh_index",
            description="Trigger arena pipeline rebuild (subprocess: arena_scan.py + arena_cluster_score.py + arena_build_index.py). Use after adding/updating skills.",
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    try:
        if name == "search_skills":
            data = _search_skills(
                arguments.get("query", ""),
                arguments.get("top_n", 10),
            )
        elif name == "get_skill":
            data = _get_skill(
                arguments.get("skill_id", ""),
                arguments.get("include_content", False),
            )
        elif name == "list_categories":
            data = _list_categories()
        elif name == "list_winners":
            data = _list_winners(arguments.get("top_n", 20))
        elif name == "refresh_index":
            scripts_dir = REPO_ROOT / "scripts"
            log_path = Path("/tmp/claude-tasks/ultraskills-hub-rebuild.log")
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log = log_path.open("w")
            proc = subprocess.Popen(
                [
                    sys.executable,
                    "-c",
                    _REFRESH_INDEX_RUNNER,
                    "--",
                    *[
                        str(scripts_dir / script_name)
                        for script_name in (
                            "arena_scan.py",
                            "arena_cluster_score.py",
                            "arena_build_index.py",
                        )
                    ],
                ],
                cwd=REPO_ROOT,
                stdout=log,
                stderr=log,
                shell=False,
            )
            _invalidate()
            data = {
                "status": "started",
                "pid": proc.pid,
                "log": str(log_path),
                "message": "Rebuild launched in background. Index invalidated — next call will reload.",
            }
        else:
            data = {"error": f"Unknown tool: {name}"}

    except Exception as e:
        data = {"error": str(e)}

    return [TextContent(type="text", text=json.dumps(data, ensure_ascii=False, indent=2))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())