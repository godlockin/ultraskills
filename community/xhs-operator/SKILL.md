---
name: xhs-operator
description: 小红书账号运营助手——Cookie 保活检测、多账号健康巡检、过期通知。依赖 xhs-skills 子模块（external/xhs-skills）提供 API 能力。
version: 1.0.0
tags: [xhs, 小红书, cookie, 保活, 运营, 账号管理, social-media]
---

# xhs-operator — 小红书运营助手

## 概述

此 skill 专注于小红书账号的**Cookie 保活与健康管理**，补充 `xhs-apis` skill 缺失的运维能力：

- **多账号 Cookie 健康检查**：批量验证 cookie 是否有效
- **自动保活**：每 2 小时定时巡检（推荐配置 cron）
- **过期通知**：支持企业微信 / 钉钉 / Slack webhook 推送
- **状态持久化**：将检测结果写入 JSON，便于追踪历史

## 前置依赖

```bash
# 1. 安装 xhs-skills Python 依赖（如尚未安装）
pip install -r external/xhs-skills/skills/xhs-apis/scripts/requirements.txt

# 2. 安装 xhs-skills Node 依赖（签名算法需要 Node.js）
cd external/xhs-skills/skills/xhs-apis/scripts && npm install && cd -
```

## 快速开始

### 1. 准备 cookies 配置文件

参考 `examples/cookies_sample.json`，创建你的账号配置：

```json
[
  {
    "name": "账号A",
    "type": "pc",
    "cookies_str": "a1=xxx; web_session=xxx; ..."
  },
  {
    "name": "账号B",
    "type": "pc",
    "cookies_str": "a1=yyy; web_session=yyy; ..."
  }
]
```

### 2. 运行健康检查

```bash
# 单次检查
python3 community/xhs-operator/scripts/cookie_health.py \
  --cookies-file community/xhs-operator/examples/my_cookies.json

# 检查并推送 webhook 通知（企业微信/钉钉）
python3 community/xhs-operator/scripts/cookie_health.py \
  --cookies-file my_cookies.json \
  --webhook-url https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx

# 结果写入文件
python3 community/xhs-operator/scripts/cookie_health.py \
  --cookies-file my_cookies.json \
  --out health_report.json
```

### 3. 配置定时保活（每 2 小时）

```bash
# crontab -e
0 */2 * * * cd /path/to/ultraskills && python3 community/xhs-operator/scripts/cookie_health.py \
  --cookies-file /path/to/my_cookies.json \
  --webhook-url https://your-webhook-url \
  >> /var/log/xhs_health.log 2>&1
```

## Token 刷新说明

**小红书没有 OAuth refresh_token 机制**。实际机制如下：

| 阶段 | 行为 |
|------|------|
| cookie 有效期 | PC `web_session` 约 30 天；Creator `customer_session` 约 14 天 |
| 保活原理 | 定期调用 `get_user_self_info` API，保持 session 活跃 |
| 过期处理 | 自动检测 → 通知用户 → 用户重新扫码/手机验证码登录 |
| 无自动续期 | 小红书平台限制，无法在无人工介入下自动刷新 |

## 与 xhs-apis skill 的关系

```
xhs-apis  →  提供底层 API 能力（搜索、笔记、发布）
xhs-operator  →  运维层（保活、健康检查、通知）
```

两者配合使用：先用 `xhs-operator` 保活确认 cookie 有效，再用 `xhs-apis` 执行业务操作。

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `jsdom not found` | Node 依赖未安装 | `cd external/xhs-skills/skills/xhs-apis/scripts && npm install` |
| `execjs.ProgramError` | Node.js 未安装或版本过低 | 安装 Node.js 20+ |
| `cookie 无效` 但实际有效 | 签名算法需要 a1 cookie | 确保 `cookies_str` 含 `a1` 字段 |
| 2h 后仍未通知 | cron 未配置或路径错误 | 检查 crontab，使用绝对路径 |
