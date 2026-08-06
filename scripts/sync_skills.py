#!/usr/bin/env python3
"""
sync_skills.py - 自动扫描并同步所有 Skills

功能:
1. 遍历本项目的 skill 目录
2. 从外部目录导入 skills（~/.claude/skills, ~/.trae/skills）
3. 从 GitHub 仓库拉取开源 skills
4. 更新 index.json
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlparse

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent

# Skill 分类目录
SKILL_CATEGORIES = ["engineering", "productivity", "devops", "creative"]

# 外部 Skills 目录（Claude 官方 / Trae 等）
EXTERNAL_SKILL_DIRS = [
    Path.home() / ".claude" / "skills",
    Path.home() / ".trae" / "skills",
]

# GitHub Skills 仓库配置
GITHUB_SKILL_REPOS = [
    {
        "url": "https://github.com/anthropics/skills",
        "branch": "main",
        "skills_path": "skills",  # 仓库内的 skills 目录
        "name": "anthropic-skills"
    },
    {
        "url": "https://github.com/KKKKhazix/Khazix-Skills",
        "branch": "main", 
        "skills_path": ".",  # 根目录就是 skills
        "name": "khazix-skills"
    },
    {
        "url": "https://github.com/obra/superpowers",
        "branch": "main",
        "skills_path": "skills",  # skills 目录
        "name": "superpowers"
    },
    {
        "url": "https://github.com/Ceeon/videocut-skills",
        "branch": "main",
        "skills_path": ".",  # 根目录就是 skill
        "name": "videocut-skills"
    },
    {
        "url": "https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering",
        "branch": "main",
        "skills_path": "skills",  # skills 目录
        "name": "context-engineering-skills"
    }
]

# 导入目标目录
IMPORT_TARGET_DIR = PROJECT_ROOT / "community"

ALLOWED_GITHUB_HOST = "github.com"


def canonical_repo_url(repo_url: str) -> str:
    parsed = urlparse(repo_url)
    path = parsed.path.rstrip("/")
    if (
        parsed.scheme != "https"
        or parsed.hostname != ALLOWED_GITHUB_HOST
        or parsed.username is not None
        or parsed.password is not None
        or parsed.port is not None
        or parsed.query
        or parsed.fragment
        or path.count("/") != 2
    ):
        raise ValueError(f"blocked repository URL (allowlist requires https://github.com/OWNER/REPO): {repo_url}")
    owner, repo = path.lstrip("/").split("/")
    if not owner or not repo or repo.endswith("/"):
        raise ValueError(f"blocked repository URL: {repo_url}")
    repo = repo.removesuffix(".git")
    if not repo:
        raise ValueError(f"blocked repository URL: {repo_url}")
    return f"https://github.com/{owner}/{repo}"


def validate_repo_url(repo_url: str) -> None:
    canonical_repo_url(repo_url)


def verify_cached_repo(repo_cache: Path, repo_url: str) -> str:
    expected = canonical_repo_url(repo_url)
    remote = subprocess.run(
        ["git", "-C", str(repo_cache), "remote", "get-url", "origin"],
        check=True, capture_output=True, text=True, timeout=10,
    ).stdout.strip()
    if canonical_repo_url(remote) != expected:
        raise ValueError(f"cached remote mismatch for {repo_cache.name}: {remote}")
    return subprocess.run(
        ["git", "-C", str(repo_cache), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True, timeout=10,
    ).stdout.strip()

def parse_frontmatter(content: str) -> Optional[Dict]:
    """Parse the small scalar/list subset used by skill frontmatter."""
    if not content.startswith("---"):
        return None
    end = content.find("\n---", 3)
    if end < 0:
        return None
    result: Dict[str, object] = {}
    for line in content[3:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip(" \\\"'")
        if value.startswith("[") and value.endswith("]"):
            value = [item.strip().strip(" \\\"'") for item in value[1:-1].split(",") if item.strip()]
        result[key.strip()] = value
    return result

def scan_skill(skill_dir: Path, base_path: Path = None) -> Optional[Dict]:
    """扫描单个 skill 目录。"""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None
    
    try:
        content = skill_md.read_text(encoding="utf-8")
        meta = parse_frontmatter(content)
        if not meta:
            return None
        
        base = base_path or PROJECT_ROOT
        try:
            rel_path = skill_md.relative_to(base)
        except ValueError:
            rel_path = skill_md
        
        return {
            "id": skill_dir.name,
            "name": meta.get("name", skill_dir.name),
            "path": f"./{rel_path}",
            "description": meta.get("description", "No description"),
            "tags": meta.get("tags", []),
            "source": "local"
        }
    except Exception as e:
        print(f"  ❌ {skill_dir.name}: {e}")
        return None


def scan_local_skills() -> List[Dict]:
    """扫描本项目的 skills。"""
    skills = []
    
    for category in SKILL_CATEGORIES:
        category_dir = PROJECT_ROOT / category
        if not category_dir.exists():
            continue
        
        print(f"\n📂 Scanning {category}/")
        for item in sorted(category_dir.iterdir()):
            if item.is_dir() and not item.name.startswith("_"):
                skill = scan_skill(item)
                if skill:
                    skill["source"] = f"local/{category}"
                    skills.append(skill)
                    print(f"  ✅ {item.name}")
    
    # 扫描 community 目录
    community_dir = PROJECT_ROOT / "community"
    if community_dir.exists():
        print(f"\n📂 Scanning community/")
        for item in sorted(community_dir.iterdir()):
            if item.is_dir() and not item.name.startswith("_"):
                skill = scan_skill(item)
                if skill:
                    skill["source"] = "community"
                    skills.append(skill)
                    print(f"  ✅ {item.name}")
    
    return skills


def import_external_skills(dry_run: bool = False) -> List[str]:
    """从外部目录导入 skills。"""
    imported = []
    
    for ext_dir in EXTERNAL_SKILL_DIRS:
        if not ext_dir.exists():
            continue
        
        print(f"\n📥 Checking external: {ext_dir}")
        
        for item in ext_dir.iterdir():
            if not item.is_dir():
                continue
            skill_md = item / "SKILL.md"
            if not skill_md.exists():
                continue
            
            # 检查是否已存在
            target = IMPORT_TARGET_DIR / item.name
            if target.exists():
                print(f"  ⏭️  {item.name} (already exists)")
                continue
            
            if dry_run:
                print(f"  📋 {item.name} (would import)")
            else:
                IMPORT_TARGET_DIR.mkdir(exist_ok=True)
                shutil.copytree(item, target)
                print(f"  ✅ {item.name} (imported)")
                imported.append(item.name)
    
    return imported


def fetch_github_skills(dry_run: bool = False) -> List[str]:
    """从 GitHub 仓库拉取 skills。"""
    fetched = []
    cache_dir = PROJECT_ROOT / ".cache" / "github"
    
    for repo in GITHUB_SKILL_REPOS:
        repo_name = repo["name"]
        repo_url = repo["url"]
        branch = repo.get("branch", "main")
        skills_path = repo.get("skills_path", ".")
        
        print(f"\n🌐 Fetching from GitHub: {repo_name}")
        
        repo_cache = cache_dir / repo_name
        
        try:
            validate_repo_url(repo_url)
            if repo_cache.exists():
                if not dry_run:
                    commit = verify_cached_repo(repo_cache, repo_url)
                    print(f"  ✓ Using allowlisted cached commit {commit}")
                else:
                    print(f"  📋 Would verify cached origin for {repo_name} (no network refresh)")
            else:
                print(f"  📦 Cloning allowlisted repository {repo_name}...")
                if not dry_run:
                    cache_dir.mkdir(parents=True, exist_ok=True)
                    subprocess.run(
                        ["git", "clone", "--depth", "1", "--branch", branch, repo_url, str(repo_cache)],
                        check=True, capture_output=True, text=True, timeout=60,
                    )
                    commit = verify_cached_repo(repo_cache, repo_url)
                    print(f"  ✓ Verified origin; cached commit {commit}")
            if dry_run:
                print(f"  📋 Would scan {repo_name} (no network refresh)")
                continue
            
            # 扫描并导入
            skills_dir = repo_cache / skills_path
            if not skills_dir.exists():
                print(f"  ⚠️  Skills path not found: {skills_path}")
                continue
            
            for item in skills_dir.iterdir():
                if not item.is_dir() or item.name.startswith("."):
                    continue
                skill_md = item / "SKILL.md"
                if not skill_md.exists():
                    continue
                
                target = IMPORT_TARGET_DIR / item.name
                if target.exists():
                    print(f"  ⏭️  {item.name} (exists)")
                    continue
                
                IMPORT_TARGET_DIR.mkdir(exist_ok=True)
                shutil.copytree(item, target)
                print(f"  ✅ {item.name} (imported)")
                fetched.append(item.name)
                
        except subprocess.TimeoutExpired as exc:
            print(f"  ❌ Timeout fetching {repo_name}", file=sys.stderr)
            raise RuntimeError(f"timeout fetching {repo_name}") from exc
        except Exception as exc:
            print(f"  ❌ Error: {exc}", file=sys.stderr)
            raise
    
    return fetched


def sync_global_links(skills: List[Dict], dry_run: bool = False) -> dict:
    """校验并创建到全局 skills 目录的软链接。"""
    global_dirs = [
        Path.home() / ".trae" / "skills",
        Path.home() / ".claude" / "skills",
        Path.home() / ".codex" / "skills",
        Path.home() / ".antigravity" / "skills",
        Path.home() / ".gemini" / "skills",
        Path.home() / ".windsurf" / "skills",
        Path.home() / ".cursor" / "skills",
    ]
    
    results = {"created": [], "exists": [], "broken": [], "missing_dir": []}
    
    print("\n🔗 Syncing global symlinks...")
    
    for global_dir in global_dirs:
        if not global_dir.exists():
            if dry_run:
                print(f"  📋 Would create: {global_dir}")
            else:
                global_dir.mkdir(parents=True, exist_ok=True)
                print(f"  📁 Created: {global_dir}")
    
    for skill in skills:
        skill_path = skill.get("path", "")
        if not skill_path:
            continue
        
        # 解析实际路径
        skill_full_path = PROJECT_ROOT / skill_path.lstrip("./")
        skill_dir = skill_full_path.parent
        skill_name = skill_dir.name
        
        if not skill_dir.exists():
            continue
        
        for global_dir in global_dirs:
            link_path = global_dir / skill_name
            
            if link_path.is_symlink():
                # 检查链接是否有效
                if link_path.resolve() == skill_dir.resolve():
                    if global_dir.name == "skills" and global_dir.parent.name == ".trae":
                        results["exists"].append(skill_name)
                else:
                    results["broken"].append(skill_name)
                    if not dry_run:
                        link_path.unlink()
                        link_path.symlink_to(skill_dir)
                        print(f"  🔧 Fixed: {skill_name}")
            elif link_path.exists():
                # 是一个真实目录，跳过
                pass
            else:
                # 创建新链接
                if dry_run:
                    if skill_name not in [r for r in results["created"]]:
                        results["created"].append(skill_name)
                        print(f"  📋 Would link: {skill_name}")
                else:
                    link_path.symlink_to(skill_dir)
                    if skill_name not in results["created"]:
                        results["created"].append(skill_name)
                        print(f"  ✅ Linked: {skill_name}")
    
    # 只显示一次的汇总
    if results["exists"]:
        print(f"\n  ⏭️  Already linked: {len(results['exists'])} skills")
    if results["broken"]:
        print(f"  🔧 Fixed broken: {len(results['broken'])} skills")
    
    return results


def update_index(skills: List[Dict]):
    """Rebuild the canonical index through the full Arena pipeline."""
    script = PROJECT_ROOT / "scripts" / "build_arena_index.py"
    env = os.environ.copy()
    env["ULTRASKILLS_PIPELINE_LOCK_HELD"] = "1"
    result = subprocess.run([sys.executable, str(script)], cwd=PROJECT_ROOT, env=env)
    if result.returncode != 0:
        raise RuntimeError(f"Arena pipeline failed with exit {result.returncode}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Sync UltraSkils library")
    parser.add_argument("--import-external", action="store_true", help="Import from ~/.claude/skills etc.")
    parser.add_argument("--fetch-github", action="store_true", help="Fetch from GitHub repositories")
    parser.add_argument("--link", action="store_true", help="Sync symlinks to ~/.trae/skills and ~/.claude/skills")
    parser.add_argument("--all", action="store_true", help="Do everything: scan, import, fetch, link")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    args = parser.parse_args()
    
    print("🔄 Syncing UltraSkils...")
    
    # 1. 扫描本地
    skills = scan_local_skills()
    
    # 2. 导入外部
    if args.import_external or args.all:
        imported = import_external_skills(dry_run=args.dry_run)
        if imported:
            # 重新扫描以包含新导入的
            skills = scan_local_skills()
    
    # 3. 从 GitHub 获取
    if args.fetch_github or args.all:
        fetched = fetch_github_skills(dry_run=args.dry_run)
        if fetched:
            skills = scan_local_skills()
    
    if not skills:
        print("\n⚠️  No skills found!")
        return 1
    
    if not args.dry_run:
        update_index(skills)
    
    # 4. 同步全局软链接
    if args.link or args.all:
        sync_global_links(skills, dry_run=args.dry_run)
    
    print("\n✨ Sync complete!")
    
    # 显示来源统计
    sources = {}
    for s in skills:
        src = s.get("source", "unknown")
        sources[src] = sources.get(src, 0) + 1
    
    print("\n📊 Skills by source:")
    for src, count in sorted(sources.items()):
        print(f"   {src}: {count}")
    
    return 0


if __name__ == "__main__":
    from pipeline_lock import PipelineLock
    with PipelineLock("sync_skills"):
        sys.exit(main())

