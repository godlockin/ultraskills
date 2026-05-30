#!/usr/bin/env python3
"""
cookie_health.py — 小红书账号 Cookie 健康检查与保活脚本

依赖: external/xhs-skills 子模块（需已安装 Python + Node 依赖）

用法:
  python3 cookie_health.py --cookies-file accounts.json
  python3 cookie_health.py --cookies-file accounts.json --webhook-url https://...
  python3 cookie_health.py --cookies-file accounts.json --out report.json
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

# 自动定位 xhs_api_tool.py
_SCRIPT_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _SCRIPT_DIR.parent.parent.parent
_XHS_API_TOOL = _REPO_ROOT / "external" / "xhs-skills" / "skills" / "xhs-apis" / "scripts" / "xhs_api_tool.py"


def _locate_api_tool() -> Path:
    if _XHS_API_TOOL.exists():
        return _XHS_API_TOOL
    # 尝试从环境变量获取
    env_path = os.environ.get("XHS_API_TOOL_PATH")
    if env_path:
        p = Path(env_path)
        if p.exists():
            return p
    raise FileNotFoundError(
        f"xhs_api_tool.py not found at {_XHS_API_TOOL}\n"
        "请确认已添加 external/xhs-skills 子模块，或设置 XHS_API_TOOL_PATH 环境变量。"
    )


def check_cookie(cookies_str: str, account_type: str = "pc") -> dict:
    """
    验证单个 cookie 是否有效。
    返回: {"success": bool, "nickname": str, "error": str}
    """
    tool = _locate_api_tool()
    method = "get_user_self_info" if account_type == "pc" else "get_user_info"

    params = json.dumps({"cookies_str": cookies_str})
    try:
        result = subprocess.run(
            [sys.executable, str(tool), "call", "pc" if account_type == "pc" else "creator", method,
             "--params", params],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0:
            error_text = result.stdout or result.stderr or "unknown error"
            try:
                err_data = json.loads(error_text)
                return {"success": False, "nickname": "", "error": err_data.get("error", error_text[:200])}
            except json.JSONDecodeError:
                return {"success": False, "nickname": "", "error": error_text[:200]}

        data = json.loads(result.stdout)
        api_result = data.get("result")
        if isinstance(api_result, (list, tuple)) and len(api_result) >= 2:
            success = bool(api_result[0])
            user_data = api_result[2] if len(api_result) > 2 else {}
            nickname = ""
            if isinstance(user_data, dict):
                nickname = user_data.get("nickname") or user_data.get("userName") or ""
            return {"success": success, "nickname": nickname, "error": "" if success else str(api_result[1])}

        return {"success": False, "nickname": "", "error": f"unexpected result: {str(api_result)[:100]}"}

    except subprocess.TimeoutExpired:
        return {"success": False, "nickname": "", "error": "timeout (20s)"}
    except Exception as exc:
        return {"success": False, "nickname": "", "error": str(exc)}


def run_health_check(accounts: list[dict]) -> list[dict]:
    """批量检查账号 cookie 状态。"""
    results = []
    for account in accounts:
        name = account.get("name", "unknown")
        cookies_str = account.get("cookies_str", "")
        account_type = account.get("type", "pc")

        print(f"  检查 [{name}] ({account_type})...", end=" ", flush=True)
        check = check_cookie(cookies_str, account_type)

        status = "active" if check["success"] else "expired"
        nickname = check.get("nickname", "")
        display = f"✅ {nickname or name}" if check["success"] else f"❌ 过期: {check.get('error', '')}"
        print(display)

        results.append({
            "name": name,
            "type": account_type,
            "status": status,
            "nickname": nickname,
            "error": check.get("error", ""),
            "checked_at": datetime.now().isoformat(),
        })
    return results


def send_webhook(webhook_url: str, expired_accounts: list[dict]) -> None:
    """发送过期账号通知（企业微信 / 钉钉 / 通用 Webhook）。"""
    if not expired_accounts:
        return

    names = "、".join(a["name"] for a in expired_accounts)
    text = f"⚠️ 小红书 Cookie 过期提醒\n\n以下账号 Cookie 已失效，请重新登录：\n{names}\n\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # 自动识别企业微信 / 钉钉格式
    if "qyapi.weixin.qq.com" in webhook_url:
        payload = {"msgtype": "text", "text": {"content": text}}
    elif "oapi.dingtalk.com" in webhook_url:
        payload = {"msgtype": "text", "text": {"content": text}}
    else:
        payload = {"text": text, "expired_accounts": [a["name"] for a in expired_accounts]}

    try:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            webhook_url, data=body,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"  Webhook 发送成功 (HTTP {resp.status})")
    except Exception as exc:
        print(f"  ⚠️ Webhook 发送失败: {exc}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="小红书 Cookie 健康检查")
    parser.add_argument("--cookies-file", required=True,
                        help="账号配置 JSON 文件路径（格式见 examples/cookies_sample.json）")
    parser.add_argument("--webhook-url", default="",
                        help="过期通知 Webhook URL（企业微信/钉钉/通用）")
    parser.add_argument("--out", default="",
                        help="将检测结果写入 JSON 文件")
    parser.add_argument("--fail-on-expired", action="store_true",
                        help="有账号过期时以非零状态码退出（CI 使用）")
    args = parser.parse_args()

    cookies_file = Path(args.cookies_file)
    if not cookies_file.exists():
        print(f"❌ cookies 文件不存在: {cookies_file}", file=sys.stderr)
        sys.exit(1)

    accounts = json.loads(cookies_file.read_text(encoding="utf-8"))
    if not isinstance(accounts, list):
        print("❌ cookies 文件格式错误，应为 JSON 数组", file=sys.stderr)
        sys.exit(1)

    print(f"🔍 开始检查 {len(accounts)} 个账号 Cookie...\n")
    start = time.time()
    results = run_health_check(accounts)
    elapsed = time.time() - start

    expired = [r for r in results if r["status"] == "expired"]
    active_count = len(results) - len(expired)

    print(f"\n📊 检查完成 ({elapsed:.1f}s): {active_count} 有效 / {len(expired)} 过期")

    if expired:
        print(f"\n⚠️  过期账号: {', '.join(r['name'] for r in expired)}")
        if args.webhook_url:
            send_webhook(args.webhook_url, expired)

    if args.out:
        report = {
            "checked_at": datetime.now().isoformat(),
            "total": len(results),
            "active": active_count,
            "expired": len(expired),
            "accounts": results,
        }
        Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"💾 结果已写入: {args.out}")

    if args.fail_on_expired and expired:
        sys.exit(1)


if __name__ == "__main__":
    main()
