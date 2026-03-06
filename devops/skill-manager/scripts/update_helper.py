#!/usr/bin/env python3
"""
update_helper.py - Skill 更新辅助工具

在更新 skill 之前备份 SKILL.md。
"""

import shutil
import os
import sys
import datetime


def backup_skill(skill_path: str) -> tuple[bool, str]:
    """
    备份 SKILL.md 文件。
    
    Args:
        skill_path: skill 目录路径
        
    Returns:
        (success, message) 元组
    """
    if not os.path.exists(skill_path):
        return False, "Skill path does not exist"
        
    skill_md = os.path.join(skill_path, "SKILL.md")
    if not os.path.exists(skill_md):
        return False, "SKILL.md not found"
        
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"SKILL.md.bak.{timestamp}"
    backup_path = os.path.join(skill_path, backup_name)
    
    try:
        shutil.copy2(skill_md, backup_path)
        return True, backup_path
    except Exception as e:
        return False, str(e)


def main():
    if len(sys.argv) < 2:
        print("Usage: python update_helper.py <skill_dir>")
        print("\nExample:")
        print("  python update_helper.py ~/.claude/skills/yt-dlp/")
        sys.exit(1)
        
    skill_dir = sys.argv[1]
    success, msg = backup_skill(skill_dir)
    
    if success:
        print(f"✅ Backup created: {msg}")
    else:
        print(f"❌ Backup failed: {msg}")
        sys.exit(1)


if __name__ == "__main__":
    main()
