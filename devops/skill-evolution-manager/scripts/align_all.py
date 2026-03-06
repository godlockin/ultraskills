#!/usr/bin/env python3
"""
align_all.py - 全量对齐工具

遍历所有 skills，将存在的 evolution.json 重新缝合回对应的 SKILL.md。
通常在 skill-manager 批量更新后运行。
"""

import os
import sys
import subprocess


def align_all(skills_root: str) -> int:
    """
    对齐所有 skills 的经验数据。
    
    Args:
        skills_root: skills 根目录
        
    Returns:
        对齐的 skills 数量
    """
    if not os.path.exists(skills_root):
        print(f"❌ Error: {skills_root} not found")
        return 0

    # 获取 smart_stitch.py 的路径
    stitch_script = os.path.join(os.path.dirname(__file__), "smart_stitch.py")
    
    if not os.path.exists(stitch_script):
        print(f"❌ Error: smart_stitch.py not found at {stitch_script}")
        return 0
    
    count = 0
    for item in sorted(os.listdir(skills_root)):
        skill_dir = os.path.join(skills_root, item)
        if not os.path.isdir(skill_dir):
            continue
            
        evolution_json = os.path.join(skill_dir, "evolution.json")
        if os.path.exists(evolution_json):
            print(f"🔄 Aligning {item}...")
            try:
                subprocess.run(
                    [sys.executable, stitch_script, skill_dir],
                    check=True,
                    capture_output=True,
                    text=True
                )
                count += 1
            except subprocess.CalledProcessError as e:
                print(f"   ⚠️  Warning: Failed to align {item}: {e.stderr}")
            
    return count


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
            print("Usage: python align_all.py <skills_dir>")
            print("\nExample:")
            print("  python align_all.py ~/.claude/skills/")
            sys.exit(1)
    
    print(f"📂 Scanning: {skills_path}")
    count = align_all(skills_path)
    print(f"\n✅ Finished. Aligned {count} skills.")


if __name__ == "__main__":
    main()
