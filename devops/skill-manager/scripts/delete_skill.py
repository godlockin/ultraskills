#!/usr/bin/env python3
"""
delete_skill.py - 删除指定的 Skill

永久删除一个 skill 目录。请谨慎使用。
"""

import os
import sys
import shutil


def delete_skill(skills_root: str, skill_name: str) -> bool:
    """
    删除指定的 skill。
    
    Args:
        skills_root: skills 根目录
        skill_name: 要删除的 skill 名称
        
    Returns:
        是否删除成功
    """
    skill_dir = os.path.join(skills_root, skill_name)
    
    if not os.path.exists(skill_dir):
        print(f"❌ Error: Skill '{skill_name}' not found at {skill_dir}")
        return False
        
    try:
        shutil.rmtree(skill_dir)
        print(f"✅ Successfully deleted skill: {skill_name}")
        return True
    except Exception as e:
        print(f"❌ Error deleting skill '{skill_name}': {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python delete_skill.py <skill_name> [skills_root]")
        print("\nExample:")
        print("  python delete_skill.py yt-dlp ~/.claude/skills/")
        sys.exit(1)
        
    skill_name = sys.argv[1]
    
    if len(sys.argv) > 2:
        skills_root = sys.argv[2]
    else:
        # 尝试默认路径
        default_paths = [
            os.path.expanduser("~/.claude/skills"),
            os.path.expanduser("~/.trae/skills"),
        ]
        skills_root = None
        for path in default_paths:
            if os.path.exists(path):
                skills_root = path
                break
        
        if not skills_root:
            print("Error: Could not find default skills directory")
            print("Please specify the skills root directory")
            sys.exit(1)
    
    # 确认删除
    skill_path = os.path.join(skills_root, skill_name)
    print(f"⚠️  About to delete: {skill_path}")
    
    success = delete_skill(skills_root, skill_name)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
