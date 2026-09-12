#!/usr/bin/env python3
"""wechat-mp: 微信公众号全量 API CLI (纯标准库)."""
import os

CONFIG_DIR = ".wechat-mp"


def load_config():
    """返回 (app_id, secret)。env 优先,回退 .wechat-mp/.env。"""
    app_id = os.environ.get("WECHAT_APP_ID")
    secret = os.environ.get("WECHAT_APP_SECRET")
    env_path = os.path.join(CONFIG_DIR, ".env")
    if app_id is None or secret is None:
        if os.path.isfile(env_path):
            data = {}
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        data[k.strip()] = v.strip()
            app_id = app_id or data.get("WECHAT_APP_ID")
            secret = secret or data.get("WECHAT_APP_SECRET")
    return app_id, secret


import json, time

TOKEN_FILE = os.path.join(CONFIG_DIR, "token.json")


def write_token_cache(token, expires_in, now=None):
    if now is None:
        now = time.time()
    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump({"token": token, "expires_at": now + expires_in - 300}, f)


def read_token_cache(now=None):
    if now is None:
        now = time.time()
    try:
        with open(TOKEN_FILE, encoding="utf-8") as f:
            cached = json.load(f)
    except (OSError, ValueError):
        return None
    if not isinstance(cached, dict):
        return None
    token, expires_at = cached.get("token"), cached.get("expires_at")
    if not token or not isinstance(expires_at, (int, float)) or now >= expires_at or expires_at - now > 7200:
        return None  # 过期或异常(倒退超过一个周期)
    return token
