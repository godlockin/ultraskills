#!/usr/bin/env python3
"""Exclusive lock for Arena/index pipeline writers."""

import errno
import json
import os
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

LOCK_FILE = Path(__file__).parent.parent / ".pipeline.lock"


class PipelineLockError(RuntimeError):
    """Raised when another process owns the pipeline lock."""


class _LockHandle:
    def __init__(self, fd: int, path: Path):
        self.fd = fd
        self.path = path
        self.released = False

    def release(self) -> None:
        if self.released:
            return
        self.released = True
        try:
            owns_file = os.fstat(self.fd) == os.stat(self.path)
        except (FileNotFoundError, OSError):
            owns_file = False
        try:
            os.close(self.fd)
        finally:
            if owns_file:
                try:
                    self.path.unlink()
                except FileNotFoundError:
                    pass


def _lock_payload(operation: str) -> bytes:
    return (json.dumps({
        "pid": os.getpid(),
        "operation": operation,
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
    }, ensure_ascii=False) + "\n").encode("utf-8")


def acquire_lock(operation: str) -> _LockHandle:
    """Atomically acquire lock; stale locks require explicit operator cleanup."""
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(str(LOCK_FILE), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            details = "unknown owner"
            try:
                details = LOCK_FILE.read_text(encoding="utf-8").strip()
            except OSError:
                pass
            raise PipelineLockError(
                f"Pipeline locked; refusing to remove чужой lock: {details}"
            ) from exc
        raise
    try:
        os.write(fd, _lock_payload(operation))
        os.fsync(fd)
    except BaseException:
        try:
            owns_file = os.fstat(fd).st_ino == os.stat(LOCK_FILE).st_ino
        except OSError:
            owns_file = False
        os.close(fd)
        if owns_file:
            try:
                LOCK_FILE.unlink()
            except FileNotFoundError:
                pass
        raise
    return _LockHandle(fd, LOCK_FILE)


def release_lock(handle: Optional[_LockHandle] = None) -> None:
    """Release only supplied handle; no handle means no-op for compatibility."""
    if handle is not None:
        handle.release()


@contextmanager
def PipelineLock(operation: str):
    if os.environ.get("ULTRASKILLS_PIPELINE_LOCK_HELD") == "1":
        yield
        return
    handle = acquire_lock(operation)
    try:
        yield
    finally:
        release_lock(handle)
