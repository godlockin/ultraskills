#!/usr/bin/env python3
"""
arena_scan.py - 扫描所有 SKILL.md，提取元数据，输出完整 skill 清单。

排除:
  - hidden dirs (.git, .gemini, .cursor, .codex, etc.)
  - _template_skill
  - autoresearch (无标准 SKILL.md)
  - 重复 skill id（同名取 community/ > devops/ > engineering/ > external/ 优先级）

输出: skill-arena/skills_inventory.json
"""

import os
import re
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent

# 排除目录前缀（相对于 ROOT）
EXCLUDE_PREFIXES = [
    "_template_skill",
    "external/autoresearch",
    "external/anthropic-quickstarts",
    # html-anything 内部模板 (低分，不适合作为独立 skill)
    "external/html-anything/next/src/lib/templates/skills",
]

# 排除特定低价值 skills (保持 external/ 完整性，但从索引剔除)
EXCLUDE_SKILL_IDS = [
    "runbook-generator",  # 与 sop-writer 重叠，质量低
    '"runbook-generator"',  # 带引号版本
    "template-skill",     # 空模板，无价值
    # === Low-quality videocut skills ===
    "videocut:安装",      # 环境安装说明，非 skill
    "videocut:自进化",    # 自我迭代说明，非 skill
    # === External duplicates (quoted versions from claude-skills) ===
    # Marketing skills: keep marketingskills/ (bare), exclude claude-skills/marketing-skill/ (quoted)
    '"ab-test-setup"', '"ad-creative"', '"copy-editing"', '"onboarding-cro"',
    '"paid-ads"', '"pricing-strategy"', '"programmatic-seo"', '"referral-program"',
    '"competitor-alternatives"', '"free-tool-strategy"', '"marketing-ideas"',
    '"marketing-psychology"', '"page-cro"', '"social-content"', '"copywriting"',
    '"email-sequence"', '"paywall-upgrade-cro"',
    '"ai-seo"', '"analytics-tracking"', '"churn-prevention"', '"cold-email"',
    '"content-strategy"', '"form-cro"', '"launch-strategy"', '"schema-markup"',
    '"seo-audit"', '"signup-flow-cro"', '"site-architecture"', '"popup-cro"',
    # Brand guidelines: EXCEPTION - keep quoted (8.8), exclude bare (7.3)
    'brand-guidelines',
    # Engineering skills: keep fullstack-dev-skills/ (bare), exclude claude-skills/engineering/ (quoted)
    '"code-reviewer"', '"rag-architect"',
    # Changelog: keep community (9.0), exclude claude-skills (4.5)
    '"changelog-generator"',
    # Prompt engineer: keep fullstack-dev-skills (7.8), exclude community (6.8)
    '"prompt-engineer"',
    # Media downloader: keep external/media-downloader (bare), exclude community copy
    '"media-downloader"',
]

# 配套/辅助 skills (标记为 auxiliary，不参与竞技场评分但保留索引)
# 注: caveman 子 skills 已证明有价值，移除 auxiliary 标记
AUXILIARY_SKILL_PATTERNS = [
    'caveman-stats',     # Token stats (hook-driven, 纯统计)
    'cavecrew',          # Subagent dispatch (内部用)
]

# 排除路径中包含 hidden 目录（任意层级以 . 开头的目录）
def has_hidden_component(path: Path) -> bool:
    for part in path.parts:
        if part.startswith(".") and part != ".":
            return True
    return False


def parse_frontmatter(text: str) -> dict:
    """提取 YAML frontmatter（简单解析，支持多行字符串）。"""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm_text = text[3:end].strip()
    result = {}
    lines = fm_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()

            # YAML 多行字符串: > (folded) 或 | (literal)
            if val in (">", "|", ">-", "|-"):
                # 收集后续缩进行
                multiline_parts = []
                i += 1
                while i < len(lines):
                    next_line = lines[i]
                    # 缩进行属于多行内容
                    if next_line.startswith("  ") or next_line.startswith("\t"):
                        multiline_parts.append(next_line.strip())
                        i += 1
                    elif next_line.strip() == "":
                        # 空行也属于多行内容
                        i += 1
                    else:
                        # 遇到非缩进行，结束多行
                        break
                # folded (>) 用空格连接，literal (|) 用换行
                if val.startswith(">"):
                    val = " ".join(multiline_parts)
                else:
                    val = "\n".join(multiline_parts)
                result[key] = val
                continue  # 不要 i += 1，已在 while 中处理

            # 处理 tags: [a, b] 或 tags:\n  - a
            elif val.startswith("[") and val.endswith("]"):
                val = [t.strip().strip('"\'') for t in val[1:-1].split(",") if t.strip()]
            elif val == "":
                # 可能是多行 list (tags:\n  - a\n  - b)
                list_items = []
                i += 1
                while i < len(lines):
                    next_line = lines[i]
                    if next_line.strip().startswith("- "):
                        list_items.append(next_line.strip()[2:].strip().strip('"\''))
                        i += 1
                    elif next_line.startswith("  ") or next_line.startswith("\t"):
                        i += 1
                    else:
                        break
                val = list_items if list_items else []
                result[key] = val
                continue
            result[key] = val
        i += 1
    return result


def extract_description_from_body(text: str, skill_id: str) -> str:
    """从 SKILL.md body 提取第一段非空描述（作为 fallback）。"""
    # 跳过 frontmatter
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            body = text[end + 4:]

    # 找第一个 # 标题后的描述段落
    lines = body.splitlines()
    in_section = False
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            in_section = True
            continue
        if in_section and line and not line.startswith("#") and not line.startswith(">"):
            # 清理 markdown
            clean = re.sub(r"\*\*|__|\*|_|`", "", line)
            clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean)
            if len(clean) > 20:
                return clean[:200]
    return f"{skill_id} skill"


def infer_tags_from_path(rel_path: str) -> list:
    """从路径推断 tags。"""
    tags = []
    parts = rel_path.split("/")
    # 顶层目录
    top = parts[0] if parts else ""
    if top in ("community", "devops", "engineering"):
        tags.append(top)
    elif top == "external":
        if len(parts) > 1:
            tags.append(parts[1].replace("-skills", "").replace("-skill", ""))
    return tags


def skill_priority(rel_path: str) -> int:
    """数字越小优先级越高。"""
    if rel_path.startswith("community/"):
        return 0
    if rel_path.startswith("devops/"):
        return 1
    if rel_path.startswith("engineering/"):
        return 2
    if rel_path.startswith("external/"):
        return 3
    return 9


def scan_all_skills() -> list:
    skills = {}  # id -> dict
    seen_real_paths = set()  # canonical paths to detect symlink/submodule duplicates

    skill_mds = sorted(ROOT.rglob("SKILL.md"))

    for skill_md in skill_mds:
        # Deduplicate by real (resolved) path — catches symlinks and submodule overlaps
        real_path = skill_md.resolve()
        if real_path in seen_real_paths:
            continue
        seen_real_paths.add(real_path)

        rel = skill_md.relative_to(ROOT)
        # Normalize: strip leading './' so EXCLUDE_PREFIXES checks work correctly
        rel_str = str(rel).lstrip("./") if str(rel).startswith("./") else str(rel)

        # 排除 hidden 目录
        if has_hidden_component(rel):
            continue

        # 排除特定前缀
        if any(rel_str.startswith(p) for p in EXCLUDE_PREFIXES):
            continue

        # 排除含 .no-skill marker 的目录（marker 存在即跳过整棵树，包括其下所有子目录）
        # 与 scripts/deploy_skills.py:102 行为对齐
        skill_dir = skill_md.parent
        if (skill_dir / ".no-skill").exists():
            continue

        # skill 目录 = SKILL.md 的父目录
        skill_dir_rel = str(skill_dir.relative_to(ROOT))

        text = skill_md.read_text(encoding="utf-8", errors="ignore")
        fm = parse_frontmatter(text)

        # skill id: frontmatter name > 目录名
        skill_id = fm.get("name", "").strip() or skill_dir.name
        # 规范化：小写，去空格
        skill_id = skill_id.lower().replace(" ", "-")

        # 排除特定低价值 skills (保持 external/ 完整性)
        if skill_id in EXCLUDE_SKILL_IDS:
            continue

        description = fm.get("description", "") or ""
        if isinstance(description, list):
            description = " ".join(str(x) for x in description)
        description = str(description).strip()
        if not description:
            description = extract_description_from_body(text, skill_id)

        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [t.strip() for t in tags.split(",")]
        # 补充从路径推断的 tags
        inferred = infer_tags_from_path(skill_dir_rel)
        for t in inferred:
            if t and t not in tags:
                tags.append(t)

        version = fm.get("version", "")
        github_url = fm.get("github_url", "")

        # 标记配套 skills (不参与竞技场评分)
        is_auxiliary = any(pattern in skill_id for pattern in AUXILIARY_SKILL_PATTERNS)

        entry = {
            "id": skill_id,
            "path": f"./{skill_dir_rel}/SKILL.md",
            "description": description,
            "tags": tags if isinstance(tags, list) else [],
            "version": str(version) if version else "",
            "github_url": str(github_url) if github_url else "",
            "auxiliary": is_auxiliary,  # 配套 skill 标记
            "_priority": skill_priority(skill_dir_rel),
            "_rel_path": skill_dir_rel,
        }

        # 去重：同 id 取优先级高的
        if skill_id not in skills:
            skills[skill_id] = entry
        else:
            existing = skills[skill_id]
            if entry["_priority"] < existing["_priority"]:
                skills[skill_id] = entry

    result = sorted(skills.values(), key=lambda x: (x["_rel_path"]))
    # 清理内部字段
    for s in result:
        s.pop("_priority", None)
        s.pop("_rel_path", None)

    return result


if __name__ == "__main__":
    from pipeline_lock import PipelineLock
    with PipelineLock("arena_scan"):

        out_dir = ROOT / "skill-arena"
        out_dir.mkdir(exist_ok=True)

        skills = scan_all_skills()
        print(f"Scanned: {len(skills)} unique skills")

        # 统计 path 分布
        dist = {}
        for s in skills:
            top = s["path"].split("/")[1]
            dist[top] = dist.get(top, 0) + 1
        print("Distribution:", json.dumps(dist, ensure_ascii=False))

        out_file = out_dir / "skills_inventory.json"
        out_file.write_text(json.dumps(skills, ensure_ascii=False, indent=2))
        print(f"Written: {out_file}")
