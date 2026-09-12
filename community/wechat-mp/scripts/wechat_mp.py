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
