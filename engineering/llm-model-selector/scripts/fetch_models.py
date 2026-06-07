#!/usr/bin/env python3
"""
fetch_models.py - 拉取 + 缓存 models.dev 数据

数据源: https://models.dev/api.json
缓存:   <skill>/.cache/models.json (24h TTL)

Usage:
    python3 fetch_models.py              # 拉取 (cache miss 或过期)
    python3 fetch_models.py --force      # 强制刷新
    python3 fetch_models.py --info       # 显示 cache 状态
"""

import json
import sys
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
CACHE_DIR = SKILL_DIR / ".cache"
CACHE_FILE = CACHE_DIR / "models.json"
API_URL = "https://models.dev/api.json"
CACHE_TTL = 86400  # 24 hours


def cache_is_fresh() -> bool:
    if not CACHE_FILE.exists():
        return False
    age = time.time() - CACHE_FILE.stat().st_mtime
    return age < CACHE_TTL


def fetch_from_api() -> dict:
    req = Request(API_URL, headers={"User-Agent": "ultraskills-llm-model-selector/1.0"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def save_cache(data: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def load_cache() -> dict:
    return json.loads(CACHE_FILE.read_text(encoding="utf-8"))


def show_info() -> None:
    print(f"Cache path: {CACHE_FILE}")
    print(f"Exists:     {CACHE_FILE.exists()}")
    if CACHE_FILE.exists():
        age = time.time() - CACHE_FILE.stat().st_mtime
        hours = age / 3600
        fresh = cache_is_fresh()
        status = "FRESH" if fresh else "STALE"
        print(f"Age:        {hours:.1f} hours ({status})")
        try:
            data = load_cache()
            provider_count = len(data)
            model_count = sum(len(p.get("models", {})) for p in data.values())
            print(f"Providers:  {provider_count}")
            print(f"Models:     {model_count}")
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Cache corrupt: {e}")


def main():
    if "--info" in sys.argv:
        show_info()
        return 0

    force = "--force" in sys.argv

    if not force and cache_is_fresh():
        print(f"✓ Cache fresh (< 24h): {CACHE_FILE}")
        return 0

    print(f"→ Fetching {API_URL} ...")
    try:
        data = fetch_from_api()
    except URLError as e:
        if CACHE_FILE.exists():
            print(f"⚠ Network error, using stale cache: {e.reason}")
            return 0
        print(f"✗ Network error: {e.reason}", file=sys.stderr)
        return 1

    save_cache(data)
    provider_count = len(data)
    model_count = sum(len(p.get("models", {})) for p in data.values())
    print(f"✓ Saved: {provider_count} providers, {model_count} models → {CACHE_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
