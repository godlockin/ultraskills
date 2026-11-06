#!/usr/bin/env python3
"""
skill_contract.py — UltraSkills 的扫描 / frontmatter / 契约「单一真源」

此前 validate_skills.py 用递归 os.walk()、cluster_skills.py 用有限 glob，
两者口径不一致，加上 index.json 是静态快照，产生了大量 NOT_INDEXED 告警。
本模块把三件事收拢到一处：

  1. iter_skill_dirs()      —— 唯一的 skill 目录扫描口径（含非 skill 目录排除）
  2. parse_frontmatter()    —— 零依赖 YAML frontmatter 解析（多行 / 嵌套 / 列表）
  3. 契约分级               —— 自有 skill 强制四字段 + 全量登记；
                              上游 skill（external/ 与 submodule）字段由上游维护，
                              version/tags 记为可选元数据，不进告警。

契约版本: 2.0.0  (2026-11-06)
"""

from __future__ import annotations

import configparser
import os
import re

CONTRACT_VERSION = "2.0.0"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../.."))

# ---------------------------------------------------------------- 扫描口径

# 这些目录里的 SKILL.md 是模板 / 测试夹具 / 依赖，不是可登记的 skill
EXCLUDED_DIR_NAMES = {
    "node_modules", "testdata", "assets", "_template_skill",
    "__pycache__", "venv", ".venv", "dist", "build", "vendor",
}
EXCLUDED_PATH_PARTS = {"testdata", "assets"}

# index.json 登记策略：
#   external/ 为「精选登记制」——上游镜像由 .gitmodules 管理，未入选不是错误
#   其余顶层为「全量登记制」——凡是扫描到的 skill 都必须登记，缺失即 ERROR
SELECTIVE_INDEX_TOP_LEVEL = "external"

OWNED_REQUIRED_FIELDS = ("name", "description", "version", "tags")
UPSTREAM_REQUIRED_FIELDS = ("name", "description")
UPSTREAM_OPTIONAL_FIELDS = ("version", "tags")
ALL_TRACKED_FIELDS = OWNED_REQUIRED_FIELDS


def load_submodule_roots(repo_root: str = REPO_ROOT) -> set[str]:
    """从 .gitmodules 读取所有 submodule 根路径（规范化绝对路径）。"""
    gitmodules = os.path.join(repo_root, ".gitmodules")
    if not os.path.exists(gitmodules):
        return set()
    cfg = configparser.ConfigParser()
    cfg.read(gitmodules, encoding="utf-8")
    return {
        os.path.normpath(os.path.join(repo_root, cfg.get(sec, "path")))
        for sec in cfg.sections()
        if cfg.has_option(sec, "path")
    }


def is_under_submodule(resolved_path: str, submodule_roots: set[str]) -> bool:
    return any(
        resolved_path == root or resolved_path.startswith(root + os.sep)
        for root in submodule_roots
    )


def is_upstream(rel: str, norm_root: str, submodule_roots: set[str]) -> bool:
    """上游维护的 skill：external/ 顶层，或位于任意 submodule 内。"""
    return (
        rel.split(os.sep)[0] == SELECTIVE_INDEX_TOP_LEVEL
        or is_under_submodule(norm_root, submodule_roots)
    )


def in_full_index_scope(rel: str) -> bool:
    """是否需要强制登记进 index.json。external/ 为精选登记制，不强制。"""
    top = rel.split(os.sep)[0]
    return top != SELECTIVE_INDEX_TOP_LEVEL and not top.startswith("_")


def iter_skill_dirs(repo_root: str = REPO_ROOT):
    """统一扫描口径。产出 (norm_root, rel, skill_md_path)。

    校验器、聚类器、索引同步器都必须调用它，避免再次出现口径漂移。
    """
    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [
            d for d in dirs
            if not d.startswith(".") and d not in EXCLUDED_DIR_NAMES
        ]
        if "SKILL.md" not in files:
            continue
        rel = os.path.relpath(root, repo_root)
        parts = rel.split(os.sep)
        if any(p in EXCLUDED_PATH_PARTS for p in parts):
            continue
        yield os.path.normpath(root), rel, os.path.join(root, "SKILL.md")


# ------------------------------------------------------- frontmatter 解析

_FM = re.compile(r"^---\s*\r?\n(.*?)\r?\n---(?:\s*\r?\n|$)", re.DOTALL)
_KEY = re.compile(r"^([A-Za-z_][\w.-]*)\s*:\s*(.*)$")
_BLOCK_SCALARS = {">", "|", ">-", "|-", ">+", "|+"}


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _strip_comment(value: str) -> str:
    """去掉未被引号包裹的行内 # 注释。"""
    out, quote = [], None
    for ch in value:
        if quote:
            out.append(ch)
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
            out.append(ch)
        elif ch == "#" and (not out or out[-1].isspace()):
            break
        else:
            out.append(ch)
    return "".join(out).strip()


def _unquote(value: str) -> str:
    v = value.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1].strip()
    return v


def _collect_block(lines, start: int, parent_indent: int):
    """收集缩进大于 parent_indent 的连续行，返回 (拼接文本, 下一行索引)。"""
    buf, j = [], start
    while j < len(lines):
        ln = lines[j]
        if ln.strip() and _indent(ln) <= parent_indent:
            break
        if ln.strip():
            buf.append(ln.strip())
        j += 1
    return " ".join(buf), j


def parse_frontmatter(content: str):
    """零依赖解析 YAML frontmatter，返回字段 dict；无 frontmatter 返回 None。

    覆盖社区 skill 里真实存在的写法：
      key: value
      key: >  /  key: |          多行块标量
      key:                       后跟缩进正文（隐式块标量，如 web-access）
      key:                       后跟缩进 mapping（如 metadata.version）
      key:                       后跟 - item 块列表（如 tags）
      key: [a, b]                内联列表
    嵌套字段中的受追踪字段会提升为顶层（metadata.version -> version）。
    """
    m = _FM.match(content)
    if not m:
        return None
    lines = m.group(1).splitlines()
    top: dict[str, str] = {}
    nested: dict[str, str] = {}
    stack: list[tuple[int, str]] = []
    i = 0
    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("- "):
            i += 1
            continue
        ind = _indent(raw)
        km = _KEY.match(stripped)
        if not km:
            i += 1
            continue
        key, val = km.group(1), _strip_comment(km.group(2))
        while stack and stack[-1][0] >= ind:
            stack.pop()
        full = ".".join([p[1] for p in stack] + [key])
        target = nested if stack else top

        if val in _BLOCK_SCALARS:
            target[full], i = _collect_block(lines, i + 1, ind)
            continue

        if val == "":
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and _indent(lines[j]) > ind:
                nxt = lines[j].strip()
                if nxt.startswith("- "):
                    # 块列表：tags:\n  - a\n  - b
                    buf, k = [], i + 1
                    while k < len(lines):
                        ln = lines[k]
                        if ln.strip() and _indent(ln) <= ind:
                            break
                        if ln.strip().startswith("- "):
                            buf.append(ln.strip()[2:].strip())
                        k += 1
                    target[full] = ", ".join(buf)
                    i = k
                    continue
                if _KEY.match(nxt):
                    # 嵌套 mapping
                    stack.append((ind, key))
                    i += 1
                    continue
                # 隐式块标量：description: 后直接跟缩进正文
                target[full], i = _collect_block(lines, i + 1, ind)
                continue
            i += 1
            continue

        target[full] = _unquote(val)
        i += 1

    # 把嵌套在 metadata / 其它容器下的受追踪字段提升为顶层
    for full, value in nested.items():
        if not isinstance(value, str) or not value.strip():
            continue
        leaf = full.rsplit(".", 1)[-1]
        if leaf in ALL_TRACKED_FIELDS and leaf not in top:
            top[leaf] = value

    return {k: v for k, v in top.items() if isinstance(v, str) and v.strip()}
