#!/usr/bin/env python3
"""wechat-mp: 微信公众号全量 API CLI (纯标准库)."""
import os
import uuid

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


import urllib.request, urllib.error, urllib.parse

API_BASE = "https://api.weixin.qq.com"


class WechatApiError(Exception):
    """服务端返回 errcode != 0。payload 为原始 JSON dict。"""
    def __init__(self, payload):
        self.payload = payload
        super().__init__(payload.get("errmsg", "unknown"))


class WechatNetworkError(Exception):
    pass


def http_json(method, path, query=None, body=None):
    """底层 HTTP: 返回解析后的 dict。errcode!=0 抛 WechatApiError,网络问题抛 WechatNetworkError。"""
    url = API_BASE + path
    if query:
        url += "?" + urllib.parse.urlencode(query)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8"))  # 微信 5xx 也回 JSON
        except ValueError:
            raise WechatNetworkError(f"HTTP {e.code}") from e
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise WechatNetworkError(str(e)) from e


def fetch_stable_token(app_id, secret, force_refresh=False):
    body = {"grant_type": "client_credential", "appid": app_id, "secret": secret,
            "force_refresh": force_refresh}
    payload = http_json("POST", "/cgi-bin/stable_token", body=body)
    if payload.get("errcode", 0) != 0:
        raise WechatApiError(payload)
    return payload["access_token"], payload["expires_in"]


def get_access_token(force_refresh=False):
    if not force_refresh:
        cached = read_token_cache()
        if cached:
            return cached
    app_id, secret = load_config()
    if not app_id or not secret:
        missing = "WECHAT_APP_ID" if not app_id else "WECHAT_APP_SECRET"
        print(json.dumps({"errcode": -1, "errmsg": f"missing credential: {missing} "
                          f"(set env or .wechat-mp/.env)"}, indent=2, ensure_ascii=False))
        raise SystemExit(2)
    token, expires_in = fetch_stable_token(app_id, secret, force_refresh)
    write_token_cache(token, expires_in)
    return token


def build_multipart(fields, file_field, filename, content, file_mime="application/octet-stream"):
    boundary = "----wechatmp" + uuid.uuid4().hex
    parts = []
    for k, v in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    parts.append(
        f'--{boundary}\r\nContent-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n'
        f'Content-Type: {file_mime}\r\n\r\n'.encode() + content + b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def _upload_multipart(url, fields, file_field, filename, content):
    body, ctype = build_multipart(fields, file_field, filename, content)
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", ctype)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode("utf-8"))
        except ValueError:
            raise WechatNetworkError(f"HTTP {e.code}") from e
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise WechatNetworkError(str(e)) from e


RETRYABLE_CODES = {40001, 42001}


def api_call(method, path, body=None, file=None, file_field="media",
             extra_query=None, token=None):
    """网关: 附 token 调任意端点。file=(filename, bytes)。返回服务端 dict。"""
    for attempt in (0, 1):  # 最多两次
        if token is None:
            token = get_access_token(force_refresh=attempt == 1)
        query = dict(extra_query or {})
        query["access_token"] = token
        url = API_BASE + path + "?" + urllib.parse.urlencode(query)
        try:
            if file is not None:
                payload = _upload_multipart(url, body or {}, file_field, file[0], file[1])
            else:
                payload = http_json(method, path, query=query, body=body)
        except WechatNetworkError:
            raise
        if payload.get("errcode", 0) in RETRYABLE_CODES and attempt == 0:
            token = None
            continue
        return payload
