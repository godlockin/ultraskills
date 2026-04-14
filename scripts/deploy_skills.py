#!/usr/bin/env python3
"""
deploy_skills.py - Skills 部署脚本

两组 skills:
  1. external/  - GitHub 开源 submodule（只读，git submodule update 更新）
  2. 其他目录   - 自研 skills（community/, engineering/, creative/, productivity/, devops/）

功能:
  scan    扫描所有 skills，更新 index.json
  deploy  软链接部署到 ~/.claude/skills, ~/.cursor/skills 等
  clean   清理失效软链接
  status  显示部署状态

用法:
  python3 deploy_skills.py scan
  python3 deploy_skills.py deploy
  python3 deploy_skills.py deploy --dry-run
  python3 deploy_skills.py status
  python3 deploy_skills.py clean
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml

# ─── 配置 ────────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent.parent
INDEX_PATH = PROJECT_ROOT / "index.json"

# 自研 skill 目录（全文件保存在项目里）
OWNED_DIRS = [
    "community",
    "engineering",
    "creative",
    "productivity",
    "devops",
]

# 外部 submodule 目录（只读）
EXTERNAL_DIR = PROJECT_ROOT / "external"

# 部署目标
DEPLOY_TARGETS = [
    Path.home() / ".claude" / "skills",
    Path.home() / ".cursor" / "skills",
    Path.home() / ".windsurf" / "skills",
    Path.home() / ".codex" / "skills",
]

# 扫描时跳过的目录/文件名
SKIP_NAMES = {".git", ".cache", "__pycache__", "node_modules", ".DS_Store",
              "templates", "examples", "resources", "scripts", "reports",
              "test-suites", "plans", "plugins", ".codex", ".gemini", ".cursor"}

# ─── 工具函数 ─────────────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> Optional[Dict]:
    """解析 YAML frontmatter。"""
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        return None


def find_skill_dirs(base: Path, max_depth: int = 4) -> List[Path]:
    """
    递归找所有包含 SKILL.md 的目录。
    跳过 SKIP_NAMES 中的目录。
    """
    results = []
    if not base.exists():
        return results

    def _walk(path: Path, depth: int):
        if depth > max_depth:
            return
        if path.name in SKIP_NAMES:
            return
        if (path / ".no-skill").exists():
            return  # 显式标记为非 skill 目录（如 devops 工具实现目录）
        if (path / "SKILL.md").exists():
            results.append(path)
            return  # 不再深入（子目录可能是子 skill）
        if path.is_dir():
            for child in sorted(path.iterdir()):
                if child.is_dir() and not child.name.startswith("."):
                    _walk(child, depth + 1)

    _walk(base, 0)
    return results


def scan_skill(skill_dir: Path, source_type: str) -> Optional[Dict]:
    """读取 skill 元数据。"""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None

    text = skill_md.read_text(encoding="utf-8", errors="ignore")
    fm = parse_frontmatter(text) or {}

    name = fm.get("name", "").strip('"').strip("'") or skill_dir.name
    skill_id = re.sub(r'[^\w\-]', '-', name.lower()).strip('-')

    rel_path = "./" + str(skill_dir.relative_to(PROJECT_ROOT))

    return {
        "id": skill_id,
        "name": name,
        "description": (fm.get("description") or "").strip(),
        "version": str(fm.get("version", "1.0.0")),
        "tags": fm.get("tags") or [],
        "path": rel_path,
        "source": source_type,  # "owned" | "external"
        "source_dir": skill_dir.parts[len(PROJECT_ROOT.parts)],  # top-level dir
    }


# ─── scan ────────────────────────────────────────────────────────────────────

def cmd_scan(args):
    """扫描所有 skills，写入 index.json。"""
    print("🔍 Scanning skills...")

    skills: List[Dict] = []
    seen_ids: Dict[str, str] = {}  # id -> path (for dedup warning)

    # 1. 自研 skills
    for dir_name in OWNED_DIRS:
        base = PROJECT_ROOT / dir_name
        for skill_dir in find_skill_dirs(base):
            skill = scan_skill(skill_dir, "owned")
            if not skill:
                continue
            sid = skill["id"]
            if sid in seen_ids:
                print(f"  ⚠️  Duplicate id '{sid}': {skill['path']} vs {seen_ids[sid]}")
            else:
                seen_ids[sid] = skill["path"]
                skills.append(skill)

    owned_count = len(skills)
    print(f"  Owned skills: {owned_count}")

    # 2. External submodule skills
    ext_count = 0
    if EXTERNAL_DIR.exists():
        for submodule_dir in sorted(EXTERNAL_DIR.iterdir()):
            if not submodule_dir.is_dir() or submodule_dir.name.startswith("."):
                continue
            for skill_dir in find_skill_dirs(submodule_dir):
                skill = scan_skill(skill_dir, "external")
                if not skill:
                    continue
                sid = skill["id"]
                if sid in seen_ids:
                    # External 重复 owned → 跳过（owned 优先）
                    continue
                seen_ids[sid] = skill["path"]
                skills.append(skill)
                ext_count += 1

    print(f"  External skills: {ext_count}")
    print(f"  Total: {len(skills)}")

    # 横向分析：按 tag 聚合
    tag_index: Dict[str, List[str]] = {}
    for s in skills:
        for tag in s.get("tags") or []:
            tag_index.setdefault(tag, []).append(s["id"])

    # 纵向分析：按 source_dir 聚合
    dir_index: Dict[str, List[str]] = {}
    for s in skills:
        dir_index.setdefault(s["source_dir"], []).append(s["id"])

    # 读取现有 arena 数据（保留）
    existing_arena: Dict[str, Dict] = {}
    if INDEX_PATH.exists():
        try:
            old = json.loads(INDEX_PATH.read_text())
            for s in old.get("skills", []):
                if "arena" in s:
                    existing_arena[s["id"]] = s["arena"]
        except Exception:
            pass

    # 合并 arena 数据
    for s in skills:
        if s["id"] in existing_arena:
            s["arena"] = existing_arena[s["id"]]

    index = {
        "version": "1.0.0",
        "generated_at": datetime.now().strftime("%Y-%m-%d"),
        "stats": {
            "total": len(skills),
            "owned": owned_count,
            "external": ext_count,
        },
        "tag_index": tag_index,
        "dir_index": dir_index,
        "skills": skills,
    }

    INDEX_PATH.write_text(json.dumps(index, indent=2, ensure_ascii=False))
    print(f"\n✅ index.json updated ({len(skills)} skills)")


# ─── deploy ──────────────────────────────────────────────────────────────────

def _ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def cmd_deploy(args):
    """把所有 skills 软链接到各 IDE 的 skills 目录。"""
    dry = getattr(args, "dry_run", False)
    mode = "DRY RUN" if dry else "DEPLOY"
    print(f"🔗 {mode}: deploying skills to IDE dirs...")

    if not INDEX_PATH.exists():
        print("❌ index.json not found. Run 'scan' first.")
        sys.exit(1)

    index = json.loads(INDEX_PATH.read_text())
    skills = index["skills"]

    stats = {"created": 0, "updated": 0, "skipped": 0, "error": 0}

    for target_base in DEPLOY_TARGETS:
        if not dry:
            _ensure_dir(target_base)
        print(f"\n  → {target_base}")

        for skill in skills:
            skill_id = skill["id"]
            skill_path = (PROJECT_ROOT / skill["path"].lstrip("./")).resolve()

            if not skill_path.exists():
                print(f"    ⚠️  Missing: {skill['path']}")
                stats["error"] += 1
                continue

            link = target_base / skill_id

            # Already correct symlink
            if link.is_symlink() and link.resolve() == skill_path:
                stats["skipped"] += 1
                continue

            if dry:
                action = "UPDATE" if link.exists() else "CREATE"
                print(f"    [{action}] {skill_id} -> {skill_path}")
                stats["created"] += 1
                continue

            # Remove stale link/dir
            if link.is_symlink() or link.exists():
                if link.is_symlink():
                    link.unlink()
                else:
                    import shutil
                    shutil.rmtree(link)
                stats["updated"] += 1
            else:
                stats["created"] += 1

            link.symlink_to(skill_path)

    print(f"\n✅ Done: {stats['created']} created, {stats['updated']} updated, "
          f"{stats['skipped']} skipped, {stats['error']} errors")


# ─── clean ───────────────────────────────────────────────────────────────────

def cmd_clean(args):
    """清理各 IDE skills 目录中失效的软链接。"""
    print("🧹 Cleaning broken symlinks...")
    total = 0
    for target_base in DEPLOY_TARGETS:
        if not target_base.exists():
            continue
        for link in sorted(target_base.iterdir()):
            if link.is_symlink() and not link.exists():
                print(f"  rm {link}")
                link.unlink()
                total += 1
    print(f"✅ Removed {total} broken symlinks")


# ─── status ──────────────────────────────────────────────────────────────────

def cmd_status(args):
    """显示部署状态。"""
    if not INDEX_PATH.exists():
        print("❌ index.json not found. Run 'scan' first.")
        return

    index = json.loads(INDEX_PATH.read_text())
    skills = {s["id"] for s in index["skills"]}
    stats = index.get("stats", {})

    print(f"📊 Index: {stats.get('total', len(skills))} skills "
          f"(owned: {stats.get('owned', '?')}, external: {stats.get('external', '?')})")
    print(f"   Generated: {index.get('generated_at', '?')}")

    for target_base in DEPLOY_TARGETS:
        if not target_base.exists():
            print(f"\n  {target_base}: NOT DEPLOYED")
            continue

        deployed = {p.name for p in target_base.iterdir() if p.is_symlink()}
        broken   = {p.name for p in target_base.iterdir() if p.is_symlink() and not p.exists()}
        missing  = skills - deployed
        extra    = deployed - skills

        print(f"\n  {target_base}")
        print(f"    deployed: {len(deployed)}  broken: {len(broken)}  "
              f"missing: {len(missing)}  extra (not in index): {len(extra)}")
        if broken:
            for b in sorted(broken)[:5]:
                print(f"    ⚠️  BROKEN: {b}")
        if missing:
            for m in sorted(missing)[:5]:
                print(f"    ❌ MISSING: {m}")


# ─── main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="UltraSkills deploy tool")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("scan",   help="Scan all skills and update index.json")

    dp = sub.add_parser("deploy", help="Symlink skills to IDE dirs")
    dp.add_argument("--dry-run", action="store_true", help="Preview without changes")

    sub.add_parser("clean",  help="Remove broken symlinks from IDE dirs")
    sub.add_parser("status", help="Show deployment status")

    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(1)

    {"scan": cmd_scan, "deploy": cmd_deploy,
     "clean": cmd_clean, "status": cmd_status}[args.cmd](args)


if __name__ == "__main__":
    main()
