# MCP Config Schema

The exact JSON shape we write to `~/.claude/mcp.json`.

## File location

- macOS / Linux: `$HOME/.claude/mcp.json`
- Windows: `%USERPROFILE%\.claude\mcp.json`

## Schema

```json
{
  "mcpServers": {
    "<server-name>": {
      "type": "stdio",
      "command": "<absolute-path-to-executable>",
      "args": ["<arg1>", "<arg2>"],
      "env": {
        "<VAR>": "<value>"
      }
    }
  }
}
```

## What we write for cua-mcp-server

```json
{
  "mcpServers": {
    "cua-mcp-server": {
      "type": "stdio",
      "command": "/Users/<you>/working/sourcecode/tools/ultraskills/devops/cua-mcp/scripts/run_cua_driver.sh",
      "args": [],
      "env": {}
    }
  }
}
```

The `command` is our wrapper script (`run_cua_driver.sh`), which itself resolves the actual `cua-mcp-server` binary. This indirection lets us add bootstrap logic (venv activation, env var setup) without changing the MCP config.

## What we do NOT clobber

If other MCP servers are already registered (e.g., `skills-discovery` from `devops/skill-loader/install-global-mcp.sh`), they remain in the file. Our installer does:

1. Read existing `mcp.json`
2. If invalid JSON, back up to `mcp.json.bak` and start fresh
3. Merge in `cua-mcp-server` under `mcpServers`
4. Write back

## Multiple wrappers per project

You can run multiple `install-global-mcp.sh` scripts (one per MCP server) safely — they all use the same merge logic.

## Disabling temporarily

Comment out the `cua-mcp-server` entry in `mcp.json`, then restart Claude Code. The wrapper script and submodule stay on disk; re-enable by uncommenting.

## Alternative: project-local MCP config

For project-specific MCP servers (not recommended for cua — it's a global tool), Claude Code also reads `.mcp.json` in the project root. Format is identical. The global `~/.claude/mcp.json` is preferred for cua since the same VM should be available across all your projects.
