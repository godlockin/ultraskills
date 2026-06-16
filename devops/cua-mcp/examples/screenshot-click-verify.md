# Example: Screenshot, click, verify with cua-mcp

Scenario: you want Claude to open the macOS Calculator app, click 7, then 8, then =, and report the result (35).

## Step 1 — Install and register

```bash
git submodule update --init --recursive
uv venv --python 3.12 external/cua/.venv
external/cua/.venv/bin/pip install \
    external/cua/libs/python/cua \
    external/cua/libs/python/mcp-server
bash devops/cua-mcp/install-global-mcp.sh
```

Restart Claude Code. Run `/mcp` to confirm `cua-mcp-server` is listed.

## Step 2 — In Claude Code, ask

```
Open macOS Calculator. Click 7, then ×, then 5, then =. Tell me the result.
```

## Step 3 — What happens under the hood

Claude invokes the MCP tools (auto-discovered from `cua-mcp-server`):

```
screenshot                  # capture current desktop
mouse.click(180, 320)       # click 7 (coordinates from screenshot or OCR)
screenshot                  # verify
mouse.click(280, 280)       # click ×
mouse.click(180, 360)       # click 5
mouse.click(380, 440)       # click =
screenshot                  # capture result
shell.run("osascript -e 'tell application \"System Events\" to get name of every process'")
# verify Calculator is in the process list
```

The screenshot-then-click loop is the canonical computer-use pattern: **see → act → verify**.

## Step 4 — Fallback: text-based targeting

If OCR or coordinate-based clicking is unreliable, use the high-level helpers:

```
screenshot.find("7")         # returns coordinates of the "7" button
screenshot.click("7")        # auto-locates and clicks
screenshot.click("×")
screenshot.click("5")
screenshot.click("=")
```

## Step 5 — Cleanup

```
shell.run("osascript -e 'quit app \"Calculator\"'")
```

## Failure modes & recovery

| Symptom | Cause | Fix |
|---------|-------|-----|
| "command not found: cua-mcp-server" | Submodule venv not initialized | Run `bash devops/cua-mcp/install-global-mcp.sh` again |
| `/mcp` doesn't list cua-mcp-server | mcp.json not reloaded | Restart Claude Code |
| Screenshot is black | Sandbox VM not running | Start `lume` VM manually, or set `CUA_SANDBOX_MODE=cloud` |
| Click lands on wrong target | Window resized since last screenshot | Re-screenshot before each click |
| "AGPL-3.0 detected" error | Wrong extra installed | `pip uninstall cua-agent[omni]` then reinstall per Step 1 |
