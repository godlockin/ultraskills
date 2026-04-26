---
name: agent-reach
description: 给 AI Agent 一键装上互联网能力 - 读取网页、搜索 Twitter/YouTube/GitHub、解析小红书/抖音等
# EXTENDED METADATA (MANDATORY)
github_url: https://github.com/Panniantong/Agent-Reach
github_hash: 15a2961dfa673cb2c8d78c79d2dae51f28e5b5e1
version: v1.2.0
created_at: 2026-02-27
entry_point: scripts/wrapper.py
dependencies: ["pip", "gh CLI", "Node.js", "yt-dlp", "mcporter", "xreach", "docker"]
tags: [community]
---

# Agent Reach - AI Agent 互联网能力工具

## 功能概述

Agent Reach 是一个脚手架工具，帮助 AI Agent 获得以下互联网能力：

| 平台 | 能力 | 依赖工具 |
|------|------|----------|
| **网页** | 读取任意网页 | Jina Reader |
| **YouTube** | 字幕提取 + 视频搜索 | yt-dlp |
| **Twitter/X** | 读取推文、搜索、发布 | xreach CLI |
| **GitHub** | 读取公开仓库、搜索、提 Issue/PR | gh CLI |
| **B站** | 字幕提取 + 视频搜索 | yt-dlp |
| **RSS** | 订阅和阅读 RSS/Atom 源 | feedparser |
| **全网搜索** | AI 语义搜索 | Exa (via mcporter) |
| **Reddit** | 搜索帖子和评论 | Exa |
| **小红书** | 读取笔记、搜索、发布、评论 | xiaohongshu-mcp (Docker) |
| **抖音** | 视频解析、无水印下载 | douyin-mcp-server |
| **LinkedIn** | 读取公开页面、职位搜索 | linkedin-mcp |
| **Boss直聘** | 搜索职位、联系 HR | mcp-bosszp |

## 安装命令

**自动安装（推荐）：**
```bash
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto
```

**安全模式（不自动修改系统）：**
```bash
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto --safe
```

**预览模式：**
```bash
agent-reach install --env=auto --dry-run
```

## 常用命令

### 健康检查
```bash
agent-reach doctor
```

### 配置 Twitter Cookie
```bash
agent-reach configure twitter-cookies "PASTED_COOKIE_STRING"
```

### 配置代理
```bash
agent-reach configure proxy http://user:pass@ip:port
```

### 配置小红书（需要 Docker）
```bash
docker run -d --name xiaohongshu-mcp -p 18060:18060 xpzouying/xiaohongshu-mcp
mcporter config add xiaohongshu http://localhost:18060/mcp
```

### 卸载
```bash
agent-reach uninstall
```

## 使用示例

安装完成后，Agent 可以直接调用上游工具：

- 读取网页：`curl https://r.jina.ai/URL`
- 查看 GitHub 仓库：`gh repo view owner/repo`
- 提取 YouTube 字幕：`yt-dlp --dump-json URL`
- 搜索 Twitter：`xreach search "关键词" --json`
- 订阅 RSS：`feedparser` 解析

## 安全说明

1. **Cookie 只存本地**：不上传不外传
2. **建议使用小号**：Twitter、小红书等平台建议使用专用小号
3. **代码完全开源**：随时可审查
4. **安全模式**：`--safe` 参数不会自动修改系统

## 相关文档

- 安装文档：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
- 故障排查：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/troubleshooting.md