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
from pathlib import Path
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


##############################################################################
# Health Check Functions
##############################################################################

import re

# Project root (ultraskills repo root)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def _load_known_tags() -> set:
    """Load all known tags from index.json."""
    index_path = os.path.join(_PROJECT_ROOT, "index.json")
    if not os.path.exists(index_path):
        return set()
    try:
        with open(index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        tags = set()
        skills = data if isinstance(data, list) else data.get("skills", [])
        for skill in skills:
            for tag in skill.get("tags", []):
                tags.add(tag)
        return tags
    except Exception:
        return set()


def _find_skill_dirs(target_dir: str) -> List[str]:
    """Find all skill directories (contain SKILL.md) under target_dir."""
    skill_dirs = []
    # If target_dir itself has SKILL.md, it's a single skill
    if os.path.isfile(os.path.join(target_dir, "SKILL.md")):
        skill_dirs.append(target_dir)
    else:
        # Walk subdirectories (one level deep for category dirs)
        for item in os.listdir(target_dir):
            sub = os.path.join(target_dir, item)
            if os.path.isdir(sub) and os.path.isfile(os.path.join(sub, "SKILL.md")):
                skill_dirs.append(sub)
    return skill_dirs


def check_script_references(skill_dir: str, content: str) -> List[str]:
    """Check that scripts/ references in SKILL.md actually exist."""
    warnings = []
    # Match patterns like scripts/xxx.py, scripts/foo.sh etc.
    refs = re.findall(r'scripts/[\w\-\.]+', content)
    for ref in set(refs):
        ref_path = os.path.join(skill_dir, ref)
        if not os.path.exists(ref_path):
            warnings.append(f"WARNING: [{os.path.basename(skill_dir)}] referenced '{ref}' not found")
    return warnings


def check_examples_nonempty(skill_dir: str) -> List[str]:
    """Check that examples/ dir has at least one non-empty file."""
    warnings = []
    examples_dir = os.path.join(skill_dir, "examples")
    if os.path.isdir(examples_dir):
        has_content = False
        for f in os.listdir(examples_dir):
            fp = os.path.join(examples_dir, f)
            if os.path.isfile(fp) and os.path.getsize(fp) > 0:
                has_content = True
                break
        if not has_content:
            warnings.append(f"WARNING: [{os.path.basename(skill_dir)}] examples/ is empty or has no non-empty files")
    return warnings


def check_tags_standard(skill_dir: str, frontmatter: Dict, known_tags: set) -> List[str]:
    """Check if tags are in the known tags set."""
    infos = []
    if not known_tags:
        return infos
    tags = frontmatter.get("tags", [])
    if isinstance(tags, list):
        for tag in tags:
            if tag and tag not in known_tags:
                infos.append(f"INFO: [{os.path.basename(skill_dir)}] tag '{tag}' not in known tags set (new or typo?)")
    return infos


def check_security_scan(skill_dir: str) -> List[str]:
    """
    Stage 2.5 security gate. Delegates to the SkillSpector wrapper at
    devops/skill-security-scan/scripts/health_gate.py.

    Scans community/ and external/ skills for prompt injection, MCP tool
    poisoning, data exfiltration, supply-chain CVEs, etc. Returns 0+ warnings.
    Never raises — graceful fallback if SkillSpector is not installed.
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "skill-security-scan" / "scripts"))
        from health_gate import check_security_scan as _gate
        return _gate(skill_dir)
    except Exception as e:
        return [f"WARN: [{os.path.basename(skill_dir)}] security gate error: {e}"]


def run_health_check(target_dir: str):
    """Run full health check on all skills under target_dir."""
    skill_dirs = _find_skill_dirs(target_dir)
    known_tags = _load_known_tags()

    warnings = []
    infos = []
    checked = 0

    for skill_dir in skill_dirs:
        skill_md = os.path.join(skill_dir, "SKILL.md")
        try:
            with open(skill_md, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue

        checked += 1
        frontmatter = parse_frontmatter(content) or {}

        # 1. Script reference check
        warnings.extend(check_script_references(skill_dir, content))

        # 2. Examples non-empty check
        warnings.extend(check_examples_nonempty(skill_dir))

        # 2.5 Security scan (skillspector) — community/external skills only
        if "community" in skill_dir or "/external/" in skill_dir or skill_dir.startswith("external/"):
            warnings.extend(check_security_scan(skill_dir))

        # 3. Tags standardization check
        infos.extend(check_tags_standard(skill_dir, frontmatter, known_tags))

    # Print issues
    for w in warnings:
        print(w, file=sys.stderr)
    for i in infos:
        print(i, file=sys.stderr)

    # Summary
    print(f"\nHealth Report: {checked} skills checked, {len(warnings)} warnings, {len(infos)} info",
          file=sys.stderr)


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
            print("  python scan_and_check.py community/")
            print("  python scan_and_check.py --health community/")
            sys.exit(1)
    else:
        target_dir = sys.argv[-1]

    # Health check mode
    if "--health" in sys.argv:
        print(f"Running health check on: {target_dir}", file=sys.stderr)
        run_health_check(target_dir)
        return

    print(f"Scanning: {target_dir}", file=sys.stderr)
    skills = scan_skills(target_dir)
    print(f"Found {len(skills)} GitHub-based skills", file=sys.stderr)

    updates = check_updates(skills)
    print(json.dumps(updates, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
