# Cua CLI Reference

## Core commands

### `cua-mcp-server` — the MCP server we register

```
cua-mcp-server                  # start the MCP server on stdio
cua-mcp-server --port 9877     # also expose HTTP (experimental)
cua-mcp-server --help
```

Environment variables:
- `CUA_SANDBOX_MODE` — `local` (lume VM), `cloud` (cua.ai API), `docker` (lumier)
- `CUA_API_KEY` — required for `cloud` mode
- `CUA_COMPUTER` — explicit computer/server URI (e.g., `lume:///`, `cloud://`, `docker://`)

### `cua` — top-level CLI (umbrella)

```
cua --help
cua computer list              # list available sandboxes
cua computer run "echo hi"     # one-shot shell command in sandbox
cua computer shell             # open interactive shell
```

### `lume` — local macOS VM (Apple Silicon only)

```
lume create macos-sequoia      # create VM
lume start macos-sequoia       # boot VM
lume stop macos-sequoia        # shut down
lume list                      # list VMs
lume --help
```

### `lumier` — Docker-based Linux sandbox

```
lumier run xfce               # start an XFCE Linux desktop in Docker
lumier list
lumier --help
```

### `cua-bench` — benchmarks (OSWorld, ScreenSpot, etc.)

```
cua-bench list                # available benchmarks
cua-bench run osworld         # run OSWorld suite
cua-bench run screenspot
cua-bench run --agent my-agent osworld
```

## Python SDK

```python
from cua.agent import ComputerAgent
from cua.computer import Computer

async with Computer(provider="lume", os="macos") as computer:
    await computer.screenshot()            # returns PNG bytes
    await computer.mouse.click(100, 200)
    await computer.keyboard.type("Hello")
    await computer.shell.run("ls -la")
```

## MCP tool surface (exposed to Claude Code)

| Tool | Args | Description |
|------|------|-------------|
| `screenshot` | `region: [x,y,w,h]?` | Capture desktop (full or region) |
| `mouse.click` | `x: int, y: int, button: "left"\|"right"` | Click at coordinates |
| `mouse.move` | `x: int, y: int` | Move cursor |
| `mouse.scroll` | `dx: int, dy: int` | Scroll wheel |
| `keyboard.type` | `text: str` | Type literal string |
| `keyboard.press` | `keys: list[str]` | Press key combination (e.g. `["cmd", "c"]`) |
| `shell.run` | `cmd: str` | Run shell command in sandbox |
| `screenshot.find` | `text: str` | OCR locate text in screenshot, return coords |
| `screenshot.click` | `text: str` | Find text and click it |
| `screenshot.annotate` | — | Returns screenshot with element bounding boxes drawn |

## License and AGPL warning

| Package | License | Install? |
|---------|---------|----------|
| `cua` (meta) | MIT | ✅ |
| `cua-mcp-server` | MIT | ✅ |
| `cua-computer` | MIT | ✅ |
| `cua-agent` (core) | MIT | ✅ |
| `cua-agent[omni]` (ultralytics) | **AGPL-3.0** | ❌ NEVER |

If you accidentally install `cua-agent[omni]`, your entire project becomes AGPL-bound. Always:
```bash
pip install cua cua-mcp-server   # NOT: pip install cua[omni]
```
