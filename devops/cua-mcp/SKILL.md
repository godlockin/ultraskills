---
name: cua-mcp
description: Computer-use MCP server for native desktop automation. Wraps trycua/cua to drive macOS, Windows, Linux, and Android GUIs via screenshot/mouse/keyboard — exposes tools for Claude Code through `cua-mcp-server`. Use when browser automation (Playwright) can't reach the target, for OSWorld-style benchmarks, or for driving legacy native apps. Triggers: "computer use", "desktop automation", "screenshot and click", "OSWorld", "sandbox VM".
version: 1.0.0
tags: [devops, mcp-server, computer-use, sandbox, desktop-automation]
---

# Cua MCP — Computer-Use Server

## Goal

Give Claude Code (and any MCP-compatible client) the ability to drive native desktop apps — click buttons, type into fields, take screenshots, run shell commands inside a sandbox VM. Bridges the gap between **browser automation** (Playwright, web-only) and **full OS control**.

## When to use

| Scenario | Use this skill | Use Playwright instead |
|----------|---------------|------------------------|
| Native macOS app (Notes, Safari outside web stack, Finder) | ✅ | ❌ |
| Windows desktop app (legacy UI) | ✅ | ❌ |
| Linux desktop (GIMP, custom GTK) | ✅ | ❌ |
| Android app via emulator | ✅ | ❌ |
| OSWorld benchmark runs | ✅ | ❌ |
| Web app, SPA, any browser | ❌ | ✅ |
| Headless server task | ❌ (use cua-sandbox) | ✅ |

## Quick install

```bash
# 1. Initialize submodule
git submodule update --init --recursive

# 2. Create venv + install (Python 3.12 or 3.13 required)
uv venv --python 3.12 external/cua/.venv
external/cua/.venv/bin/pip install external/cua/libs/python/cua external/cua/libs/python/mcp-server

# 3. Register the MCP server globally
bash devops/cua-mcp/install-global-mcp.sh

# 4. Restart Claude Code — `/mcp` should now list `cua-mcp-server`
```

## What you get

The MCP server exposes tools to Claude Code:

- `screenshot` — capture current desktop state
- `mouse.click(x, y)` — left-click at coordinates
- `mouse.move(x, y)` — move cursor
- `keyboard.type(text)` — type string
- `keyboard.press(key)` — press key combination
- `shell.run(cmd)` — execute shell command in sandbox
- `screenshot.find(text)` — locate UI element by text
- `screenshot.click(text)` — find and click by text (high-level helper)

## Decision matrix: local vs cloud sandbox

| Mode | Setup | Cost | Best for |
|------|-------|------|----------|
| **Local VM (lume)** | Apple Silicon only, ~5GB download | Free | Privacy-sensitive, offline |
| **Cloud sandbox (cua.ai)** | API key | Pay per use | Always-on, multi-OS |
| **Docker (lumier)** | Docker host | Free | Linux-only tasks |
| **Local Android emulator** | Android Studio | Free | Mobile testing |

By default, `cua-mcp-server` uses the local `lume` VM (M-series Mac) or cloud sandbox. Switch via `CUA_SANDBOX_MODE=cloud` env var.

## ⚠️ Pitfall: do NOT install `cua-agent[omni]`

The `cua-agent[omni]` extra pulls in **ultralytics/AGPL-3.0**. AGPL is a copyleft license that would contaminate the whole project. Only install:
- `cua` (MIT) — meta-package
- `cua-mcp-server` (MIT) — MCP server
- `cua-computer` (MIT) — low-level computer interface

Never run `pip install cua-agent[omni]` or `pip install cua[omni]`.

## Architecture

```
devops/cua-mcp/
├── SKILL.md                        # This file
├── .no-skill                       # Skip arena/deploy (it's a tool, not a content skill)
├── scripts/
│   ├── check_install.py            # Find cua-mcp-server in PATH → fall back to submodule venv
│   └── run_cua_driver.sh           # Wrapper: ensure venv exists, then exec cua-mcp-server
├── install-global-mcp.sh           # Append (not overwrite!) cua-mcp-server to ~/.claude/mcp.json
├── examples/
│   └── screenshot-click-verify.md  # Walkthrough: screenshot, find, click, verify
└── references/
    ├── cua-cli-commands.md         # Full CLI reference
    └── mcp-config-schema.md        # Exact JSON shape we write to mcp.json
```

External dependency: `external/cua/` (git submodule tracking trycua/cua upstream, MIT).

## References

- `references/cua-cli-commands.md` — full `cua-mcp-server` flags
- `references/mcp-config-schema.md` — the JSON we write
- `examples/screenshot-click-verify.md` — end-to-end walkthrough
- [trycua/cua on GitHub](https://github.com/trycua/cua) — upstream repo
- [trycua docs](https://docs.trycua.com) — official docs
