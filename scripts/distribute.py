#!/usr/bin/env python3
"""
distribute.py — deploy UltraSkills skills to multiple AI tool platforms.

Each platform has its own convention directory. This script:
  1. Reads the platform table (PLATFORMS)
  2. Creates symlinks (or copies) from each skill in index.json to the
     platform's skills directory
  3. Registers MCP server entry in the platform's settings.json if supported

Usage:
  python3 scripts/distribute.py --platform claude-code        # default
  python3 scripts/distribute.py --platform cursor
  python3 scripts/distribute.py --platform all
  python3 scripts/distribute.py --platform list
  python3 scripts/distribute.py --platform claude-code --mode copy
  python3 scripts/distribute.py --remove --platform cursor
"""

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
INDEX_FILE = REPO_ROOT / "index.json"
SAFE_SKILL_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def safe_skill_id(value: object) -> str:
    if not isinstance(value, str) or not SAFE_SKILL_ID.fullmatch(value) or value in {".", ".."}:
        raise ValueError(f"unsafe skill id: {value!r}")
    return value


def resolve_within(root: Path, *parts: str) -> Path:
    root_resolved = root.resolve()
    candidate = root_resolved.joinpath(*parts).resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"path escapes root: {candidate}") from exc
    return candidate


def index_source_path(raw_path: object) -> Path:
    if not isinstance(raw_path, str) or not raw_path:
        raise ValueError("missing source path")
    relative = raw_path[2:] if raw_path.startswith("./") else raw_path
    return resolve_within(REPO_ROOT, relative)

# Platform table — known AI tool conventions.
# Add new platforms by appending; tests should cover each.
#   skill_dir: where symlinks land (relative to platform_root or absolute)
#   mcp_settings: settings file path for MCP server registration (None = skip)
#   mcp_servers_key: top-level key in settings.json (usually "mcpServers")
PLATFORMS = {
    "claude-code": {
        "label": "Claude Code",
        "root": Path.home() / ".claude",
        "skill_dir": "skills",
        "mcp_settings": Path.home() / ".claude" / "settings.json",
        "mcp_servers_key": "mcpServers",
        "hub_command": "python3",
        "hub_args": [str(REPO_ROOT / "devops" / "ultraskills-hub" / "mcp_server.py")],
        "hub_cwd": str(REPO_ROOT / "devops" / "ultraskills-hub"),
    },
    "cursor": {
        "label": "Cursor",
        "root": Path.home() / ".cursor",
        "skill_dir": "skills",
        "mcp_settings": Path.home() / ".cursor" / "mcp.json",
        "mcp_servers_key": "mcpServers",
        "hub_command": "python3",
        "hub_args": [str(REPO_ROOT / "devops" / "ultraskills-hub" / "mcp_server.py")],
        "hub_cwd": str(REPO_ROOT / "devops" / "ultraskills-hub"),
    },
    "windsurf": {
        "label": "Windsurf (Codeium)",
        "root": Path.home() / ".codeium" / "windsurf",
        "skill_dir": "skills",
        "mcp_settings": Path.home() / ".codeium" / "windsurf" / "mcp_config.json",
        "mcp_servers_key": "mcpServers",
        "hub_command": "python3",
        "hub_args": [str(REPO_ROOT / "devops" / "ultraskills-hub" / "mcp_server.py")],
        "hub_cwd": str(REPO_ROOT / "devops" / "ultraskills-hub"),
    },
    "codex": {
        "label": "OpenAI Codex CLI",
        "root": Path.home() / ".codex",
        "skill_dir": "skills",
        # Codex CLI does not have an MCP config convention in 2026-07; skip.
        "mcp_settings": None,
    },
    "gemini": {
        "label": "Gemini CLI",
        "root": Path.home() / ".gemini",
        "skill_dir": "skills",
        "mcp_settings": Path.home() / ".gemini" / "settings.json",
        "mcp_servers_key": "mcpServers",
        "hub_command": "python3",
        "hub_args": [str(REPO_ROOT / "devops" / "ultraskills-hub" / "mcp_server.py")],
        "hub_cwd": str(REPO_ROOT / "devops" / "ultraskills-hub"),
    },
    "cline": {
        "label": "Cline",
        "root": Path.home() / ".cline",
        "skill_dir": "skills",
        "mcp_settings": Path.home() / ".cline" / "data" / "settings" / "cline_mcp_settings.json",
        "mcp_servers_key": "mcpServers",
        "hub_command": "python3",
        "hub_args": [str(REPO_ROOT / "devops" / "ultraskills-hub" / "mcp_server.py")],
        "hub_cwd": str(REPO_ROOT / "devops" / "ultraskills-hub"),
    },
    "trae": {
        "label": "Trae IDE",
        "root": Path.home() / ".trae",
        "skill_dir": "skills",
        "mcp_settings": None,  # Trae uses a different config format
    },
}


def list_platforms() -> None:
    print(f"{'NAME':<14} {'LABEL':<24} {'SKILL DIR':<32} {'MCP':<6}")
    for name, cfg in PLATFORMS.items():
        skill_full = Path(cfg["root"]) / cfg["skill_dir"]
        mcp = "yes" if cfg.get("mcp_settings") else "—"
        print(f"  {name:<12} {cfg['label']:<24} {str(skill_full):<32} {mcp:<6}")


def load_skills_from_index() -> list[dict]:
    """Return all skills from index.json. Each entry has `id`, `src` (the
    directory containing SKILL.md — parent of path), and `dst_name` (id)."""
    if not INDEX_FILE.exists():
        print(f"  ✗ index.json not found at {INDEX_FILE}", file=sys.stderr)
        sys.exit(1)
    with INDEX_FILE.open(encoding="utf-8") as f:
        idx = json.load(f)
    out = []
    for s in idx.get("skills", []):
        try:
            skill_id = safe_skill_id(s.get("id"))
            src_file = index_source_path(s.get("path"))
        except (TypeError, ValueError) as exc:
            print(f"  ✗ skipping unsafe index entry: {exc}", file=sys.stderr)
            continue
        if not src_file.exists():
            continue
        # index.json path points to SKILL.md file — use parent as the skill root
        src_dir = src_file if src_file.is_dir() else src_file.parent
        out.append({"id": skill_id, "src": src_dir, "dst_name": skill_id})
    return out


def deploy_symlink(skills: list[dict], dst_root: Path) -> tuple[int, int]:
    """Create one symlink per skill (link → skill dir). Skip if dst is real dir.
    Skill IDs may contain `/` (e.g. `zoom-mcp/whiteboard`) — preserve as nested dir."""
    dst_root.mkdir(parents=True, exist_ok=True)
    ok = skip = 0
    for s in skills:
        try:
            dst = resolve_within(dst_root, safe_skill_id(s["dst_name"]))
        except (TypeError, ValueError) as exc:
            print(f"    ✗ skip unsafe destination {s.get('id')}: {exc}")
            skip += 1
            continue
        if dst.is_symlink():
            dst.unlink()
        elif dst.exists():
            print(f"    ⚠ skip {s['id']} (real dir exists)")
            skip += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.symlink_to(s["src"])
        ok += 1
    return ok, skip


def deploy_copy(skills: list[dict], dst_root: Path) -> tuple[int, int]:
    """Copy each skill tree to dst. Skip if exists."""
    dst_root.mkdir(parents=True, exist_ok=True)
    ok = skip = 0
    for s in skills:
        try:
            dst = resolve_within(dst_root, safe_skill_id(s["dst_name"]))
        except (TypeError, ValueError) as exc:
            print(f"    ✗ skip unsafe destination {s.get('id')}: {exc}")
            skip += 1
            continue
        if dst.exists():
            print(f"    ⚠ skip {s['id']} (already exists — remove first)")
            skip += 1
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(s["src"], dst)
        ok += 1
    return ok, skip


def register_mcp(platform_cfg: dict) -> bool:
    """Add ultraskills-hub to platform's MCP settings. Create if missing."""
    settings_path = platform_cfg.get("mcp_settings")
    if not settings_path:
        return False
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    if not settings_path.exists():
        with settings_path.open("w", encoding="utf-8") as f:
            json.dump({}, f)

    with settings_path.open(encoding="utf-8") as f:
        cfg = json.load(f)
    key = platform_cfg["mcp_servers_key"]
    servers = cfg.setdefault(key, {})
    servers["ultraskills-hub"] = {
        "command": platform_cfg["hub_command"],
        "args": platform_cfg["hub_args"],
        "cwd": platform_cfg["hub_cwd"],
    }
    with settings_path.open("w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    return True


def unregister_mcp(platform_cfg: dict) -> bool:
    settings_path = platform_cfg.get("mcp_settings")
    if not settings_path or not settings_path.exists():
        return False
    with settings_path.open(encoding="utf-8") as f:
        cfg = json.load(f)
    key = platform_cfg["mcp_servers_key"]
    servers = cfg.get(key, {})
    if "ultraskills-hub" in servers:
        del servers["ultraskills-hub"]
        with settings_path.open("w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
        return True
    return False


def remove_skills(dst_root: Path) -> int:
    """Remove all UltraSkills symlinks/copies from dst_root (recursive).
    Only removes entries whose target lies inside REPO_ROOT (symlinks) or
    directories that are entirely US-managed copies (heuristic: empty after
    leaf symlinks removed)."""
    if not dst_root.exists():
        return 0
    count = 0
    repo_prefix = str(REPO_ROOT)
    # Walk bottom-up: remove leaf symlinks first, then empty dirs
    for entry in sorted(dst_root.rglob("*"), reverse=True):
        if entry.is_symlink():
            target = str(entry.resolve())
            if target.startswith(repo_prefix):
                entry.unlink()
                count += 1
    # Sweep now-empty directories under dst_root that we likely created.
    # Conservative: only direct children (don't recurse into arbitrary trees).
    for child in dst_root.iterdir():
        if child.is_dir() and not any(child.iterdir()):
            # Empty dir under dst_root — only remove if a sibling symlink had
            # the same name before, indicating this dir was created by US.
            # Heuristic: skip empty dirs unless they match a known US pattern.
            # For safety, leave them — user can `rmdir` manually.
            pass
    return count


def run(platform: str, mode: str, remove: bool) -> int:
    cfg = PLATFORMS.get(platform)
    if not cfg:
        print(f"Unknown platform: {platform}", file=sys.stderr)
        print("Use --platform list to see available", file=sys.stderr)
        return 2

    skill_root = Path(cfg["root"]) / cfg["skill_dir"]
    if remove:
        print(f"Removing UltraSkills from {cfg['label']} ({skill_root})...")
        n = remove_skills(skill_root)
        mcp_removed = unregister_mcp(cfg)
        print(f"  removed {n} skill symlinks/copies")
        if mcp_removed:
            print(f"  ✓ unregistered MCP server from {cfg.get('mcp_settings')}")
        return 0

    if not cfg["root"].exists():
        print(f"  ⚠ {cfg['label']} not detected at {cfg['root']} — skipping")
        return 0

    print(f"Deploying to {cfg['label']} ({skill_root}, mode={mode})...")
    skills = load_skills_from_index()
    if mode == "symlink":
        ok, skip = deploy_symlink(skills, skill_root)
    elif mode == "copy":
        ok, skip = deploy_copy(skills, skill_root)
    else:
        print(f"  ✗ unknown mode: {mode}", file=sys.stderr)
        return 2
    print(f"  ✓ {ok} skills deployed ({skip} skipped)")

    if register_mcp(cfg):
        print(f"  ✓ MCP server registered in {cfg['mcp_settings']}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--platform", default="claude-code", help="platform name or 'list' or 'all'")
    ap.add_argument("--mode", choices=["symlink", "copy"], default="symlink")
    ap.add_argument("--remove", action="store_true", help="uninstall instead of install")
    args = ap.parse_args()

    if args.platform == "list":
        list_platforms()
        return 0

    if args.platform == "all":
        rc = 0
        for name in PLATFORMS:
            r = run(name, args.mode, args.remove)
            if r != 0:
                rc = r
        return rc

    return run(args.platform, args.mode, args.remove)


if __name__ == "__main__":
    sys.exit(main())