#!/usr/bin/env python3
"""
pipeline_lock.py - 简易文件锁，防止 arena pipeline 并发执行损坏索引。
"""

import os
import json
import time
from pathlib import Path
from contextlib import contextmanager

LOCK_FILE = Path(__file__).parent.parent / ".pipeline.lock"


def _is_pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def acquire_lock(operation: str):
    if LOCK_FILE.exists():
        try:
            data = json.loads(LOCK_FILE.read_text())
            pid = data.get("pid", 0)
            if _is_pid_alive(pid):
                print(f"\n⚠️  Pipeline locked by '{data.get('operation')}' "
                      f"(PID {pid}, started {data.get('time', '?')})")
                print("Another pipeline operation is in progress. Wait or force-unlock:")
                print(f"  rm {LOCK_FILE}\n")
                raise SystemExit(1)
            else:
                # stale lock - process dead
                LOCK_FILE.unlink()
        except (json.JSONDecodeError, KeyError):
            LOCK_FILE.unlink(missing_ok=True)

    LOCK_FILE.write_text(json.dumps({
        "pid": os.getpid(),
        "operation": operation,
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }))


def release_lock():
    LOCK_FILE.unlink(missing_ok=True)


@contextmanager
def PipelineLock(operation: str):
    acquire_lock(operation)
    try:
        yield
    finally:
        release_lock()
