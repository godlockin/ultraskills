#!/usr/bin/env python3
"""
snapshot.py — backup local edits to deployed UltraSkills skills.

When users edit `~/.claude/skills/<skill>/SKILL.md` directly (common during
forks/customization), those edits live only on disk and get blown away on
re-run of setup.sh. This script:

  1. Walks platform skill dirs
  2. For each skill symlinked to US repo, compares deployed SKILL.md
     against the upstream file
  3. If different (local edit), writes a snapshot to
     ~/.ultraskills/snapshots/<skill>/<timestamp>.md
  4. Captures a unified diff alongside

Also:
  snapshot.py list <skill>          # show snapshots for a skill
  snapshot.py restore <skill> <ts>  # copy snapshot back to skill dir
  snapshot.py snapshot              # take new snapshots (default action)
"""

import argparse
import datetime as dt
import difflib
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SNAPSHOT_ROOT = Path.home() / ".ultraskills" / "snapshots"

# Same platform table as distribute.py. Could DRY by importing, but keep
# independent so snapshot.py is standalone-runnable.
PLATFORMS = {
    "claude-code": Path.home() / ".claude" / "skills",
    "cursor":      Path.home() / ".cursor" / "skills",
    "windsurf":    Path.home() / ".codeium" / "windsurf" / "skills",
    "codex":       Path.home() / ".codex" / "skills",
    "gemini":      Path.home() / ".gemini" / "skills",
    "cline":       Path.home() / ".cline" / "skills",
    "trae":        Path.home() / ".trae" / "skills",
}


def find_local_edits(platform_dir: Path) -> list[dict]:
    """Return [{skill, platform, upstream, local}] for US-managed skills
    (symlink OR real-dir copy from US) where local SKILL.md differs from
    upstream."""
    if not platform_dir.exists():
        return []
    repo_prefix = str(REPO_ROOT)
    out = []
    for entry in platform_dir.iterdir():
        if entry.is_symlink():
            # Symlink mode: target is upstream; compare SKILL.md in target vs entry
            target = entry.resolve()
            if not str(target).startswith(repo_prefix):
                continue
            skill_md = target / "SKILL.md" if target.is_dir() else None
            local_md = entry / "SKILL.md" if entry.is_dir() else None
        elif entry.is_dir():
            # Copy mode: local IS a copy. Look for upstream by id in repo.
            # We rely on the platform dir being US-managed (deploy scripts
            # only write here). Find upstream by scanning common locations.
            upstream_skill_md = find_upstream_skill_md(entry.name)
            if not upstream_skill_md:
                continue
            skill_md = upstream_skill_md
            local_md = entry / "SKILL.md"
            if not local_md.exists():
                continue
        else:
            continue

        if not (skill_md and skill_md.exists() and local_md and local_md.exists()):
            continue
        upstream = skill_md.read_text(encoding="utf-8")
        local = local_md.read_text(encoding="utf-8")
        if upstream != local:
            out.append({
                "skill": entry.name,
                "platform": platform_dir.parent.name,
                "upstream": skill_md,
                "local": local_md,
                "upstream_text": upstream,
                "local_text": local,
            })
    return out


def find_upstream_skill_md(skill_id: str) -> Path | None:
    """Find SKILL.md for a given skill id in US repo. Used by copy mode."""
    index_file = REPO_ROOT / "index.json"
    if not index_file.exists():
        return None
    import json
    with index_file.open(encoding="utf-8") as f:
        idx = json.load(f)
    for s in idx.get("skills", []):
        if s.get("id") == skill_id:
            p = REPO_ROOT / (s.get("path") or "").lstrip("./")
            return p if p.exists() else None
    return None


def take_snapshot() -> int:
    """Walk all platforms, snapshot any locally-edited skills. Return count."""
    SNAPSHOT_ROOT.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    count = 0
    for name, platform_dir in PLATFORMS.items():
        edits = find_local_edits(platform_dir)
        for ed in edits:
            skill_dir = SNAPSHOT_ROOT / ed["skill"]
            skill_dir.mkdir(parents=True, exist_ok=True)
            snap = skill_dir / f"{now}.md"
            snap.write_text(ed["local_text"], encoding="utf-8")
            diff_text = "".join(difflib.unified_diff(
                ed["upstream_text"].splitlines(keepends=True),
                ed["local_text"].splitlines(keepends=True),
                fromfile=f"upstream/{ed['skill']}/SKILL.md",
                tofile=f"local/{ed['skill']}/SKILL.md",
            ))
            (skill_dir / f"{now}.diff").write_text(diff_text, encoding="utf-8")
            print(f"  ✓ {ed['platform']}/{ed['skill']} → {snap}")
            count += 1
    if count == 0:
        print("  no local edits detected")
    return count


def list_snapshots(skill: str) -> int:
    d = SNAPSHOT_ROOT / skill
    if not d.exists():
        print(f"  no snapshots for {skill}")
        return 0
    snaps = sorted(s for s in d.glob("*.md") if not s.name.endswith(".diff"))
    print(f"  {len(snaps)} snapshot(s) for {skill}:")
    for s in snaps:
        size = s.stat().st_size
        print(f"    {s.stem}  ({size} bytes)")
    return 0


def restore_snapshot(skill: str, timestamp: str) -> int:
    # Allow timestamp with or without .md suffix
    if not timestamp.endswith(".md"):
        timestamp = timestamp + ".md"
    snap = SNAPSHOT_ROOT / skill / timestamp
    if not snap.exists():
        print(f"  ✗ snapshot not found: {snap}", file=sys.stderr)
        return 1
    # Find a real (non-symlink) skill dir across platforms — symlinks point
    # into US repo so we can't write there
    target_skill_dir = None
    for plat_dir in PLATFORMS.values():
        candidate = plat_dir / skill
        if candidate.exists() and not candidate.is_symlink() and candidate.is_dir():
            target_skill_dir = candidate
            break
    if not target_skill_dir:
        # Fall back: first symlink location (we'll restore as side file)
        for plat_dir in PLATFORMS.values():
            candidate = plat_dir / skill
            if candidate.is_symlink() or candidate.exists():
                target_skill_dir = candidate
                break
    if not target_skill_dir:
        print(f"  ✗ skill {skill} not deployed to any platform", file=sys.stderr)
        return 1
    backup_path = target_skill_dir / "SKILL.md.restored"
    if not target_skill_dir.is_symlink() and target_skill_dir.is_dir():
        shutil.copy(snap, backup_path)
        print(f"  ✓ restored to {backup_path}")
        print(f"    Review: cat {backup_path}")
        print(f"    Apply:  cp {backup_path} {target_skill_dir}/SKILL.md")
    else:
        print(f"  ⚠ skill at {target_skill_dir} is a symlink into US repo.")
        print(f"    To restore, deploy with --mode copy first:")
        print(f"    python3 scripts/distribute.py --platform cursor --mode copy")
        print(f"    Then re-run restore.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd")

    ap.add_argument("--snapshot", action="store_true", help="take snapshots (default)")
    ap.add_argument("--restore", nargs=2, metavar=("SKILL", "TIMESTAMP"), help="restore a snapshot")

    sub.add_parser("list", help="list snapshots for a skill").add_argument("skill")
    sub.add_parser("snapshot", help="take new snapshots")

    args = ap.parse_args()

    if args.restore:
        return restore_snapshot(args.restore[0], args.restore[1])

    if args.cmd == "list":
        return list_snapshots(args.skill)

    # default: snapshot
    return 0 if take_snapshot() >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())