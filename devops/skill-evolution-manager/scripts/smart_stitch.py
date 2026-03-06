#!/usr/bin/env python3
"""
smart_stitch.py - 智能缝合文档

读取 evolution.json 并将内容缝合到 SKILL.md 的专用章节中。
"""

import os
import sys
import json
import re


def stitch_skill(skill_dir: str) -> bool:
    """
    将 evolution.json 缝合到 SKILL.md。
    
    Args:
        skill_dir: skill 目录路径
        
    Returns:
        是否成功
    """
    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    evolution_json_path = os.path.join(skill_dir, "evolution.json")

    # 1. 检查文件存在
    if not os.path.exists(skill_md_path):
        print(f"❌ Error: SKILL.md not found in {skill_dir}", file=sys.stderr)
        return False
        
    if not os.path.exists(evolution_json_path):
        print(f"ℹ️  No evolution.json found in {skill_dir}. Nothing to stitch.", file=sys.stderr)
        return True

    # 2. 读取 evolution.json
    try:
        with open(evolution_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"❌ Error parsing evolution.json: {e}", file=sys.stderr)
        return False

    # 3. 构建 Markdown 内容块
    evolution_section = []
    evolution_section.append("\n\n## User-Learned Best Practices & Constraints")
    evolution_section.append("\n> **Auto-Generated Section**: This section is maintained by `skill-evolution-manager`. Do not edit manually.")
    
    if data.get("last_updated"):
        evolution_section.append(f"\n> Last updated: {data['last_updated']}")
    
    if data.get("preferences"):
        evolution_section.append("\n### User Preferences")
        for item in data["preferences"]:
            evolution_section.append(f"- {item}")
            
    if data.get("fixes"):
        evolution_section.append("\n### Known Fixes & Workarounds")
        for item in data["fixes"]:
            evolution_section.append(f"- {item}")
            
    if data.get("custom_prompts"):
        evolution_section.append("\n### Custom Instruction Injection")
        evolution_section.append(f"\n{data['custom_prompts']}")
        
    evolution_block = "\n".join(evolution_section)

    # 4. 读取原始 SKILL.md
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 5. 使用正则查找并替换或追加
    # 匹配 "## User-Learned Best Practices" 到文件末尾
    pattern = r"(\n+## User-Learned Best Practices & Constraints.*$)"
    
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        # 替换现有章节
        print("ℹ️  Updating existing evolution section...", file=sys.stderr)
        new_content = content[:match.start()] + evolution_block
    else:
        # 追加到末尾
        print("ℹ️  Appending new evolution section...", file=sys.stderr)
        new_content = content + evolution_block

    # 6. 写回文件
    try:
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Successfully stitched evolution data into {skill_md_path}")
        return True
    except Exception as e:
        print(f"❌ Error writing SKILL.md: {e}", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python smart_stitch.py <skill_dir>")
        print("\nExample:")
        print("  python smart_stitch.py ~/.claude/skills/yt-dlp/")
        sys.exit(1)
        
    target_dir = sys.argv[1]
    success = stitch_skill(target_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
