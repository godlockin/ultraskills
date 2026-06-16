---
name: ultraskills-hub
description: ⚡ MUST INVOKE FIRST for ANY specialized task — search engine for 564+ AI skills (TTS, voice clone, video analysis, design, figma, posters, design tokens, motion, icons, data-viz, IA, git workflows, evaluation, marketing, RAG, FastAPI, code intelligence, etc.). Skills are NOT pre-loaded into system-reminder — discover via this hub. Trigger on ANY of: "find skill", "do you have skill for X", "search ultraskills", or whenever a request matches a skill domain (语音克隆 / voice clone / TTS / video / 视频 / 海报 / poster / figma / 设计 / design / icon / 动效 / motion / 图表 / chart / sitemap / 信息架构 / design token / 配色 / palette / git / commit / review / evaluation / RAG / fastapi / marketing / SEO / architecture / 架构探索 / explore / call chain / 调用链 / impact analysis / 影响分析 / semantic search / 代码图谱 / computer use / desktop automation / OSWorld / sandbox VM / cua / etc.).
version: 1.1.0
tags: [hub, search, discovery, meta, routing, MUST-USE-FIRST]
entry_point: SKILL.md
---

# UltraSkills Hub — Skill Discovery & Routing

⚡ **CRITICAL ROUTING RULE** ⚡

`~/.claude/skills/` only contains THIS hub. The other 564 skills are NOT in your system-reminder. You will NOT see them listed. You MUST search this hub to find them.

**If a user request mentions ANY specialized capability — voice clone, TTS, video analysis, poster, figma, design tokens, icons, motion, charts, data viz, sitemap, git workflow, code review, evaluation, RAG, marketing, SEO, etc. — your FIRST action MUST be to run the search script below. Do NOT answer from general knowledge. Do NOT say "no skill exists". Search first.**

## How the Link Works

```
User asks "克隆我的声音"
   ↓
You invoke this hub (ultraskills-hub)
   ↓
Run: python3 {HUB_DIR}/scripts/search.py "voice clone 语音克隆"
   ↓
Get JSON with `path` field, e.g. /Users/.../community/mac-voice-clone/SKILL.md
   ↓
Read that SKILL.md with the Read tool
   ↓
Follow its instructions (run install.sh, then clone.sh, etc.)
```

The hub is just a routing index. It does NOT do the work itself — it tells you which SKILL.md to read.

## When to Use

Invoke this skill when:
- User asks "do you have a skill for X" / "找一下 X 的 skill"
- User describes a task that might match a known skill domain (see trigger list in description)
- You're about to answer a specialized question from general knowledge — STOP and search first
- You've completed a task and want to find a follow-up skill

## Search

```bash
python3 {HUB_DIR}/scripts/search.py <query terms>
```

Replace `{HUB_DIR}` with this skill's directory (absolute path, available from SKILL.md location).

### Examples

```bash
# Voice cloning
python3 .../scripts/search.py "voice clone 语音克隆"
# → community/mac-voice-clone/SKILL.md

# Video analysis
python3 .../scripts/search.py "video analyze 视频拆解"
# → community/video-analyzer/SKILL.md

# Poster / OG image
python3 .../scripts/search.py "poster og image 海报"
# → community/poster-print-design/SKILL.md

# Figma → code
python3 .../scripts/search.py "figma to code"
# → community/figma-to-code/SKILL.md

# Design tokens
python3 .../scripts/search.py "design tokens"
# → community/design-tokens/SKILL.md

# LLM evaluation
python3 .../scripts/search.py evaluate LLM judge quality

# List arena winners
python3 .../scripts/search.py --winners

# Exact id lookup
python3 .../scripts/search.py --id git-commit-master

# Browse by tag
python3 .../scripts/search.py --tag engineering
```

### Output

JSON array. Key fields:
- `id` — skill identifier
- `path` — **absolute path to SKILL.md (READ THIS NEXT)**
- `description` — what it does / when to trigger
- `is_winner` — arena winner (highest quality)
- `winner_reason` — explanation, e.g. `"#1 in eng-devops, score 91.5"`
- `match_score` — relevance to your query

## Load a Skill (mandatory follow-up after search)

After search returns a path:

1. **Read** `{path}` (the full SKILL.md) using the Read tool
2. **Follow its instructions verbatim** — run install scripts, then entry_point script
3. If the SKILL.md says `bash scripts/install.sh` then `bash scripts/clone.sh ...`, do exactly that
4. Do NOT skip install — most skills need a one-time setup

```
# Canonical workflow:
search("voice clone")                          # → path: /Users/.../mac-voice-clone/SKILL.md
Read /Users/.../mac-voice-clone/SKILL.md       # learn install + usage
Bash: bash .../mac-voice-clone/scripts/install.sh   # one-time
Bash: bash .../mac-voice-clone/scripts/clone.sh ... # actual work
```

## Hub Location

```
{ULTRASKILLS_REPO}/devops/ultraskills-hub/SKILL.md
{ULTRASKILLS_REPO}/devops/ultraskills-hub/scripts/search.py
```

`{ULTRASKILLS_REPO}` = the ultraskills repo root (same dir as `index.json`). Find it from this file's symlink target.

```python
import os
hub_dir = os.path.dirname(os.path.abspath(__file__))  # .../devops/ultraskills-hub
repo_root = os.path.abspath(os.path.join(hub_dir, "../.."))
search_script = os.path.join(hub_dir, "scripts/search.py")
```

## Available Tags

`python3 .../scripts/search.py --list-tags` for full list.

Common: `engineering`, `community`, `arena-winner`, `marketing`, `devops`, `productivity`, `creative`, `tts`, `voice-clone`, `design`, `figma`, `motion`, `data-viz`, `icon`, `poster`, `design-tokens`, `information-architecture`.

## Index

564+ skills indexed at `{ULTRASKILLS_REPO}/index.json`. Updated automatically when new skills are added.

## Anti-Patterns (DON'T)

- ❌ Answering "no skill exists for that" without searching first
- ❌ Reading random SKILL.md files by guessing paths
- ❌ Using general knowledge for tasks that have a specialized skill
- ❌ Forgetting to run install.sh before the entry_point script

