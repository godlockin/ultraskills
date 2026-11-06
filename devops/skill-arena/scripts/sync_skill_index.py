#!/usr/bin/env python3
"""
sync_skill_index.py — 用统一扫描口径增量同步 index.json

设计约束（重要）：index.json 常常带有用户未提交的 arena / cluster 成果，
本脚本绝不重建整个文件，只做三件最小改动：

  1. 追加「全量登记范围」里尚未登记的自有 skill（最小条目，不伪造 arena 评分）
  2. --prune-stale 时移除指向模板 / 测试夹具的历史脏条目
  3. 更新 meta.total_skills / meta.updated_at / meta.contract_version

默认 dry-run，只有显式 --apply 才写盘；写盘前自动备份当前工作区文件。

Usage:
  python3 sync_skill_index.py                          # dry-run
  python3 sync_skill_index.py --apply --prune-stale    # 落盘
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skill_contract as sc

REPO_ROOT = sc.REPO_ROOT
INDEX_FILE = os.path.join(REPO_ROOT, "index.json")
BACKUP_DIR = os.path.abspath(
    os.path.join(REPO_ROOT, "..", "_backup_20261106_ultraskills_index")
)


def skill_dir(raw_path):
    p = os.path.normpath(os.path.join(REPO_ROOT, raw_path.lstrip("./")))
    return os.path.dirname(p) if p.endswith("SKILL.md") else p


def as_tags(value):
    if isinstance(value, list):
        return value
    if not value:
        return []
    return [t.strip().strip("\"'") for t in str(value).split(",") if t.strip()]


def make_entry(rel_posix, fields, used_ids):
    base = rel_posix.split("/")[-1].lower().replace("_", "-").replace(" ", "-")
    sid, n = base, 2
    while sid in used_ids:
        sid = f"{base}-{n}"
        n += 1
    used_ids.add(sid)
    entry = {
        "id": sid,
        "name": fields.get("name", base),
        "path": f"./{rel_posix}/SKILL.md",
        "description": fields.get("description", ""),
        "tags": as_tags(fields.get("tags")) or [rel_posix.split("/")[0]],
        "recommended_for": [],
        "arena": None,
        "index_source": "auto-synced",
        "synced_at": datetime.now().strftime("%Y-%m-%d"),
    }
    if fields.get("version"):
        entry["version"] = fields["version"]
    return entry


def main():
    ap = argparse.ArgumentParser(description="Sync index.json with unified skill scan")
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry-run)")
    ap.add_argument("--prune-stale", action="store_true", help="drop index entries outside scan scope")
    args = ap.parse_args()

    with open(INDEX_FILE, encoding="utf-8") as f:
        idx = json.load(f)

    indexed_paths = {skill_dir(s["path"]) for s in idx["skills"]}
    used_ids = {s["id"] for s in idx["skills"]}
    scan_set = {norm for norm, _, _ in sc.iter_skill_dirs()}

    to_add, to_prune = [], []
    for norm_root, rel, skill_md in sc.iter_skill_dirs():
        if norm_root in indexed_paths:
            continue
        if not sc.in_full_index_scope(rel):
            continue
        with open(skill_md, encoding="utf-8", errors="replace") as f:
            fields = sc.parse_frontmatter(f.read()) or {}
        to_add.append(make_entry(rel.replace(os.sep, "/"), fields, used_ids))

    if args.prune_stale:
        for s in idx["skills"]:
            if skill_dir(s["path"]) not in scan_set:
                to_prune.append(s)

    print(f"当前 index.json: {len(idx['skills'])} 条")
    print(f"统一口径扫描:   {len(scan_set)} 个 skill 目录")
    print(f"待追加(全量登记范围): {len(to_add)}")
    for e in to_add:
        print(f"  + {e['id']:<28} {e['path']}")
    print(f"待清理(范围外脏条目): {len(to_prune)}")
    for s in to_prune:
        print(f"  - {s['id']:<28} {s['path']}")

    if not to_add and not to_prune:
        print("\n无需改动，index.json 已与统一口径一致。")
        return

    if not args.apply:
        print("\n[DRY-RUN] 未写盘。确认后加 --apply [--prune-stale]。")
        return

    # 备份当前工作区文件（含用户未提交改动，git 无法回滚到这个状态）
    os.makedirs(BACKUP_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = os.path.join(BACKUP_DIR, f"index.json.{stamp}.bak")
    shutil.copy2(INDEX_FILE, backup)
    print(f"\n已备份当前工作区 index.json → {backup}")

    prune_ids = {s["id"] for s in to_prune}
    idx["skills"] = [s for s in idx["skills"] if s["id"] not in prune_ids]
    idx["skills"].extend(to_add)

    idx.setdefault("meta", {})
    idx["meta"]["total_skills"] = len(idx["skills"])
    idx["meta"]["updated_at"] = datetime.now().strftime("%Y-%m-%d")
    idx["meta"]["contract_version"] = sc.CONTRACT_VERSION
    idx["meta"]["index_scope"] = "全量登记(非 external) + 精选登记(external)"

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(idx, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"已写入 {INDEX_FILE}：{len(idx['skills'])} 条")


if __name__ == "__main__":
    main()
