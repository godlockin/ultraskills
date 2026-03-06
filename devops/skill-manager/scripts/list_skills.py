#!/usr/bin/env python3
"""
list_skills.py - 列出所有已安装的 Skills

以表格形式展示所有 skills 的名称、类型、描述和版本。
"""

import os
import sys
import yaml
import io

# 强制 UTF-8 编码以处理中文字符
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')


def parse_frontmatter(content: str) -> dict:
    """解析 YAML frontmatter。"""
    parts = content.split("---")
    if len(parts) >= 3:
        try:
            return yaml.safe_load(parts[1]) or {}
        except yaml.YAMLError:
            pass
    return {}


def list_skills(skills_root: str):
    """列出所有 skills。"""
    if not os.path.exists(skills_root):
        print(f"Error: {skills_root} not found")
        return

    # 表头
    header = f"{'Skill Name':<25} | {'Type':<10} | {'Description':<40} | {'Ver':<8}"
    print(header)
    print("-" * len(header))

    for item in sorted(os.listdir(skills_root)):
        skill_dir = os.path.join(skills_root, item)
        if not os.path.isdir(skill_dir):
            continue
            
        skill_md = os.path.join(skill_dir, "SKILL.md")
        skill_type = "Standard"
        version = "0.1.0"
        description = "No description"
        
        if os.path.exists(skill_md):
            try:
                with open(skill_md, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                meta = parse_frontmatter(content)
                if meta:
                    if "github_url" in meta:
                        skill_type = "GitHub"
                    version = str(meta.get("version", "0.1.0"))
                    desc = meta.get("description", "No description")
                    description = desc.replace('\n', ' ').strip()
            except Exception:
                pass
        
        # 截断过长的描述
        if len(description) > 37:
            display_desc = description[:37] + "..."
        else:
            display_desc = description
            
        print(f"{item:<25} | {skill_type:<10} | {display_desc:<40} | {version:<8}")


def main():
    if len(sys.argv) > 1:
        skills_path = sys.argv[1]
    else:
        # 尝试默认路径
        default_paths = [
            os.path.expanduser("~/.claude/skills"),
            os.path.expanduser("~/.trae/skills"),
        ]
        skills_path = None
        for path in default_paths:
            if os.path.exists(path):
                skills_path = path
                break
        
        if not skills_path:
            print("Usage: python list_skills.py <skills_dir>")
            print("\nExample:")
            print("  python list_skills.py ~/.claude/skills/")
            sys.exit(1)
    
    print(f"Skills in: {skills_path}\n")
    list_skills(skills_path)


if __name__ == "__main__":
    main()
