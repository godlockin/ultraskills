---
name: rtk-bridge
description: Track and install the RTK (Rust Token Killer) PreToolUse hook for Claude Code. RTK transparently rewrites shell commands (git status → rtk git status) to save 60-90% output tokens. This skill provides a tracked copy of the hook installer so any clone of UltraSkills gets the same setup.
version: 1.0.0
tags: [devops, token-saver, hook, rtk, bash]
---

# rtk-bridge

Track the RTK PreToolUse hook as part of the UltraSkills repository. Anyone who clones UltraSkills and runs `setup.sh` will get the hook installed in their `~/.claude/hooks/`.

## Why

RTK lives in `~/.claude/hooks/rtk-rewrite.sh` (installed by the official `rtk init -g`). It is **not** tracked by UltraSkills — losing the home directory loses the hook. This bridge:

1. Pins a known-good version of the hook installer in the repo
2. Adds an idempotent install step to `setup.sh`
3. Provides uninstall + status check scripts

## Quick start

```bash
# Install (idempotent)
bash devops/rtk-bridge/scripts/install-hook.sh

# Status
bash devops/rtk-bridge/scripts/check-status.sh

# Uninstall
bash devops/rtk-bridge/scripts/uninstall-hook.sh
```

Or just run the project installer (handles everything):

```bash
./setup.sh           # hub + RTK hook
./setup.sh --top     # + 33 curated skills
```

## Architecture

```
UltraSkills repo
  devops/rtk-bridge/
    SKILL.md                  ← you are here
    scripts/
      install-hook.sh         ← copies hook to ~/.claude/hooks/
      uninstall-hook.sh       ← removes it
      check-status.sh         ← reports state
    references/
      hook-source.md          ← canonical RTK hook source (pinned v3)
```

**Source of truth**: the hook script comes from RTK upstream. We pin to the version we tested. To upgrade, fetch a newer `rtk-rewrite.sh` from RTK and update `references/hook-source.md`.

## What the hook does

On every `Bash` tool call, before execution, the hook:

1. Checks if `rtk` is in PATH and version >= 0.23.0
2. Calls `rtk rewrite <command>` — RTK returns either:
   - `0 + stdout` → rewrite found, allow
   - `1` → no equivalent, pass through
   - `2` → deny rule, pass through
   - `3 + stdout` → ask rule, rewrite but prompt user
3. Writes the rewritten command back so Claude Code runs `rtk <cmd>` instead

**Limits** (per RTK docs): only Bash tool calls. `Read` / `Grep` / `Glob` are not intercepted. Use `rtk read` / `rtk grep` explicitly for those.

## Prerequisites

- `rtk >= 0.23.0` in PATH (install: `brew install rtk-ai/tap/rtk` or see https://github.com/rtk-ai/rtk)
- `jq` in PATH (install: `brew install jq`)
- Bash 4+

## Token savings (from RTK docs)

- 30-min session: ~80% reduction (118k → 23.9k tokens)
- 100+ commands supported (git, cargo, npm, docker, etc.)
- Universal wrappers: `rtk err <cmd>` (errors only), `rtk test <cmd>` (test failures only)

### Read/Grep/Glob prefilter (Haiku 4.5)

The companion hook is a **fill-in for RTK's blind spot**. RTK only intercepts `Bash`; large `Read` outputs (10K+ lines) still consume tokens.

Behavior:
- Skips files < 50KB (not worth a round-trip)
- Asks Haiku 4.5 whether to `allow` / `summary` / `skip`
- 3-second timeout; pass through on any error
- Requires `ANTHROPIC_API_KEY` (or `ANTHROPIC_AUTH_TOKEN`); without it, the hook is a no-op

Cost: ~$0.0001 per invocation × N tool calls. 100 calls ≈ $0.01.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `rtk: command not found` | RTK not in PATH | `brew install rtk-ai/tap/rtk` |
| `jq: command not found` | jq missing | `brew install jq` |
| Hook silently no-op | RTK < 0.23.0 | Update RTK |
| Commands not rewritten | Hook not installed | `bash devops/rtk-bridge/scripts/install-hook.sh` |
| Two rtk hooks fire | Stale old hook | `bash devops/rtk-bridge/scripts/uninstall-hook.sh` then reinstall |

## See also

- RTK project: https://github.com/rtk-ai/rtk
- Hook source reference: `references/hook-source.md`
- UltraSkills token-saver cluster: `devops/ultraskills-hub/`
