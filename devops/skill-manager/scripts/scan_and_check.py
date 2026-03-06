#!/usr/bin/env python3
"""
scan_and_check.py - 扫描并检查 Skills 更新状态

扫描本地 skills 目录，识别 GitHub 封装的 skills，
并发检查远程 commit hash 以检测更新。
"""

import os
import sys
import yaml
import json
import subprocess
import concurrent.futures
from typing import List, Dict, Optional


def get_remote_hash(url: str) -> Optional[str]:
    """获取远程仓库的最新 commit hash。"""
    try:
        result = subprocess.run(
            ['git', 'ls-remote', url, 'HEAD'], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode != 0:
            return None
        parts = result.stdout.split()
        return parts[0] if parts else None
    except (subprocess.TimeoutExpired, Exception):
        return None


def parse_frontmatter(content: str) -> Optional[Dict]:
    """解析 YAML frontmatter。"""
    parts = content.split('---')
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError:
        return None


def scan_skills(skills_root: str) -> List[Dict]:
    """扫描所有子目录，提取带 github_url 的 skills 元数据。"""
    skill_list = []
    
    if not os.path.exists(skills_root):
        print(f"Skills root not found: {skills_root}", file=sys.stderr)
        return []

    for item in os.listdir(skills_root):
        skill_dir = os.path.join(skills_root, item)
        if not os.path.isdir(skill_dir):
            continue
            
        skill_md = os.path.join(skill_dir, "SKILL.md")
        if not os.path.exists(skill_md):
            continue
            
        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
                
            frontmatter = parse_frontmatter(content)
            if not frontmatter:
                continue
                
            # 只处理 GitHub 封装的 skills
            if 'github_url' in frontmatter:
                skill_list.append({
                    "name": frontmatter.get('name', item),
                    "dir": skill_dir,
                    "github_url": frontmatter['github_url'],
                    "local_hash": frontmatter.get('github_hash', 'unknown'),
                    "local_version": frontmatter.get('version', '0.0.0')
                })
        except Exception:
            pass
            
    return skill_list


def check_updates(skills: List[Dict]) -> List[Dict]:
    """并发检查所有 skills 的更新状态。"""
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_skill = {
            executor.submit(get_remote_hash, skill['github_url']): skill 
            for skill in skills
        }
        
        for future in concurrent.futures.as_completed(future_to_skill):
            skill = future_to_skill[future]
            try:
                remote_hash = future.result()
                skill['remote_hash'] = remote_hash
                
                if not remote_hash:
                    skill['status'] = 'error'
                    skill['message'] = 'Could not reach remote'
                elif remote_hash != skill['local_hash']:
                    skill['status'] = 'outdated'
                    skill['message'] = 'New commits available'
                else:
                    skill['status'] = 'current'
                    skill['message'] = 'Up to date'
                    
                results.append(skill)
            except Exception as e:
                skill['status'] = 'error'
                skill['message'] = str(e)
                results.append(skill)
                
    return results


def main():
    if len(sys.argv) < 2:
        # 默认路径
        default_paths = [
            os.path.expanduser("~/.claude/skills"),
            os.path.expanduser("~/.trae/skills"),
        ]
        target_dir = None
        for path in default_paths:
            if os.path.exists(path):
                target_dir = path
                break
        
        if not target_dir:
            print("Usage: python scan_and_check.py <skills_dir>")
            print("\nExample:")
            print("  python scan_and_check.py ~/.claude/skills/")
            sys.exit(1)
    else:
        target_dir = sys.argv[1]

    print(f"Scanning: {target_dir}", file=sys.stderr)
    skills = scan_skills(target_dir)
    print(f"Found {len(skills)} GitHub-based skills", file=sys.stderr)
    
    updates = check_updates(skills)
    print(json.dumps(updates, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
