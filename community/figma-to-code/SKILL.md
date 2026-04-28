---
name: figma-to-code
description: 用 Figma MCP / Figma API 把设计稿转成生产级代码。三档接入：Figma Dev Mode MCP (Figma 官方/Cursor/Claude Code) > Framelink Figma-Context-MCP (开源) > REST API 直拉 (token + node-id)。输出 React/Vue/Tailwind/CSS。Trigger on figma / design to code / 设计稿转代码 / figma to react / figma node。
version: 1.0.0
created_at: 2026-04-28
entry_point: scripts/fetch.sh
dependencies: ["node>=18 (for MCP servers)", "FIGMA_ACCESS_TOKEN env var"]
backends: ["figma-mcp-official (Dev Mode)", "framelink-mcp (open-source)", "rest-api (raw)"]
tags: [figma, design-to-code, mcp, ui, frontend, design, community]
---

# figma-to-code

把 Figma 设计稿 → React/Vue/Tailwind/HTML 代码。

## 三档后端

| 后端 | 来源 | 优势 | 劣势 |
|---|---|---|---|
| **Figma Dev Mode MCP** ⭐ | Figma 官方 | 最准；图层名/变量/Auto-layout 全保留 | 需 Figma 桌面端 + Pro 账号 |
| **Framelink Figma-MCP** | github.com/GLips/Figma-Context-MCP | 免费 / 仅需 PAT | 解析有损 |
| **REST API** | api.figma.com | 零依赖 | 自己拼 prompt，原始 JSON |

## When to use

- 把 Figma 一个组件/一页 → React + Tailwind 代码
- 把设计 token (颜色/字号/间距) → 同步到 Tailwind config
- 把 Figma 评论/标注 → 提交到代码 PR

## When NOT to use

- 要"像素级 1:1 截图" → 不靠谱，用截图 + LLM vision
- 复杂手绘/插画 → 直接导出 SVG 用
- 要 Figma 设计本身（不是消费） → 用 Figma 官方插件/编辑

## Quick Start

### 方案 A：Figma Dev Mode MCP（推荐）

```bash
# Claude Code 配置 (.claude/mcp.json 或 ~/.claude.json):
# {
#   "mcpServers": {
#     "figma-dev-mode": {
#       "url": "http://127.0.0.1:3845/mcp",
#       "transport": "sse"
#     }
#   }
# }
# 然后在 Figma 桌面 → Preferences → Enable Dev Mode MCP Server
```

启动后 Claude 直接有 `get_code` / `get_image` / `get_variable_defs` 等工具。

### 方案 B：Framelink (开源 MCP)

```bash
# 一次性安装
bash scripts/install.sh

# 配 ~/.claude.json mcpServers:
# "framelink-figma": {
#   "command": "npx",
#   "args": ["-y", "figma-developer-mcp", "--figma-api-key=YOUR_PAT", "--stdio"]
# }
```

### 方案 C：REST API 直拉

```bash
export FIGMA_ACCESS_TOKEN="figd_xxx"

# 拉一个文件的 node JSON
bash scripts/fetch.sh --file FILE_KEY --node "1:23" -o node.json

# 导出为 PNG
bash scripts/fetch.sh --file FILE_KEY --node "1:23" --format png -o frame.png

# 拉颜色/字号变量
bash scripts/fetch.sh --file FILE_KEY --variables -o tokens.json
```

## 拿到 file key 和 node id

URL: `https://www.figma.com/design/<FILE_KEY>/Title?node-id=1-23`
- `<FILE_KEY>` = 路径中那段
- node id = `1-23` → API 里写 `1:23`（短横转冒号）

## Workflow

```
Figma URL ─→ fetch (MCP / API) ─→ 结构化 JSON ─→ Claude 生成代码 ─→ tailwind.config.js + components/*.tsx
                                ↘ 导出 PNG ─→ 给 LLM vision 做对照
```

## License

- This skill: MIT
- Figma MCP: Figma 官方，使用受 Figma TOS
- Framelink: MIT
