import importlib.util
import json
import os
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import atomic_json
import pipeline_lock


def test_atomic_json_replaces_complete_document(tmp_path):
    target = tmp_path / "index.json"
    atomic_json.atomic_write_json(target, {"skills": ["new"]})
    assert json.loads(target.read_text()) == {"skills": ["new"]}
    assert list(tmp_path.glob(".*.tmp")) == []


def test_lock_is_exclusive_and_only_owner_releases(tmp_path, monkeypatch):
    lock_path = tmp_path / ".pipeline.lock"
    monkeypatch.setattr(pipeline_lock, "LOCK_FILE", lock_path)
    owner = pipeline_lock.acquire_lock("test")
    try:
        with pytest.raises(pipeline_lock.PipelineLockError):
            pipeline_lock.acquire_lock("other")
        pipeline_lock.release_lock()
        assert lock_path.exists()
    finally:
        pipeline_lock.release_lock(owner)
    assert not lock_path.exists()


def test_runner_up_and_defeated_use_eligible_only():
    spec = importlib.util.spec_from_file_location("arena_cluster_score", SCRIPTS / "arena_cluster_score.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    members = ["winner", "archived", "aux"]
    records = {
        "winner": {},
        "archived": {"archived": True},
        "aux": {"auxiliary": True},
    }
    scores = {sid: {"total": score} for sid, score in [("winner", 9), ("archived", 10), ("aux", 8)]}
    ranked = module.rank_eligible(members, records.get, scores)
    assert ranked == ["winner"]


def test_git_pull_failure_is_not_ignored():
    source = (SCRIPTS / "sync_skills.py").read_text()
    assert "git pull failed" in source
    assert "result.returncode != 0" in source
