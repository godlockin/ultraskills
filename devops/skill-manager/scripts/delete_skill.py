#!/usr/bin/env python3
"""Delete one skill directory safely."""

import argparse
import re
import shutil
from pathlib import Path

SAFE_SKILL_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def safe_skill_name(skill_name: str) -> str:
    if not isinstance(skill_name, str) or not SAFE_SKILL_ID.fullmatch(skill_name) or skill_name in {".", ".."}:
        raise ValueError(f"unsafe skill name: {skill_name!r}")
    return skill_name


def resolve_within(root: Path, name: str) -> Path:
    root_resolved = root.resolve()
    target = (root_resolved / name).resolve()
    try:
        target.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"target escapes skills root: {target}") from exc
    return target


def delete_skill(skills_root: str, skill_name: str, *, yes: bool = False) -> bool:
    """Delete one safe, single-level skill directory after confirmation."""
    try:
        safe_name = safe_skill_name(skill_name)
        skill_dir = resolve_within(Path(skills_root), safe_name)
    except (TypeError, ValueError) as exc:
        print(f"❌ Error: {exc}")
        return False

    if not skill_dir.exists():
        print(f"❌ Error: Skill '{skill_name}' not found at {skill_dir}")
        return False

    if not yes:
        answer = input(f"⚠️  Delete {skill_dir}? [y/N] ").strip().lower()
        if answer != "y":
            print("Aborted.")
            return False

    try:
        shutil.rmtree(skill_dir)
        print(f"✅ Successfully deleted skill: {safe_name}")
        return True
    except OSError as exc:
        print(f"❌ Error deleting skill '{safe_name}': {exc}")
        return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete one skill safely")
    parser.add_argument("skill_name")
    parser.add_argument("skills_root", nargs="?", help="skills root directory")
    parser.add_argument("--yes", action="store_true", help="skip deletion confirmation")
    args = parser.parse_args()

    skills_root = args.skills_root
    if skills_root is None:
        for candidate in (Path.home() / ".claude" / "skills", Path.home() / ".trae" / "skills"):
            if candidate.exists():
                skills_root = str(candidate)
                break
    if skills_root is None:
        parser.error("Could not find default skills directory; specify skills_root")

    raise SystemExit(0 if delete_skill(skills_root, args.skill_name, yes=args.yes) else 1)


if __name__ == "__main__":
    main()
