---
name: ultraskills-hub
description: Search engine for 555+ AI skills. Use when you need a specialized skill but don't know which one. Trigger: "find skill for X", "search ultraskills", or whenever a task might benefit from a specialized skill that isn't already loaded.
version: 1.0.0
tags: [hub, search, discovery, meta]
entry_point: SKILL.md
---

# UltraSkills Hub

Search engine for 555+ AI skills. Find and load the right skill on demand — without pre-loading everything into system-reminder.

## When to Use

Invoke this skill when:
- You need a specialized capability (git workflow, evaluation, marketing, etc.)
- You're unsure if a relevant skill exists
- A task description matches any known skill category
- User asks "do you have a skill for X"

## Search

```bash
python3 {HUB_DIR}/scripts/search.py <query terms>
```

Replace `{HUB_DIR}` with this skill's directory (absolute path, available from SKILL.md location).

### Examples

```bash
# Find skills for LLM evaluation
python3 .../scripts/search.py evaluate LLM judge quality

# Find git workflow skills
python3 .../scripts/search.py git commit workflow

# Find marketing skills
python3 .../scripts/search.py content strategy social media

# List arena winners only
python3 .../scripts/search.py --winners

# Exact lookup by id
python3 .../scripts/search.py --id git-commit-master

# Browse by tag
python3 .../scripts/search.py --tag engineering
```

### Output

JSON array. Key fields:
- `id` — skill identifier
- `path` — absolute path to skill directory
- `description` — what it does / when to trigger
- `is_winner` — arena winner (highest quality)
- `winner_reason` — human-readable explanation of winner status, e.g. `"#1 in eng-devops category, arena score 91.5"`; `null` if not a winner
- `match_score` — relevance to your query

## Load a Skill

After finding a skill:

1. Note the `path` from search results
2. Read `{path}/SKILL.md` using the Read tool
3. Follow the skill's instructions directly

```
# Example workflow:
results = search("git commit")          # → path: /Users/.../git-commit-master
Read /Users/.../git-commit-master/SKILL.md
# Now follow git-commit-master instructions
```

## Hub Location

This skill lives at:
```
{ULTRASKILLS_REPO}/devops/ultraskills-hub/SKILL.md
```

The search script is at:
```
{ULTRASKILLS_REPO}/devops/ultraskills-hub/scripts/search.py
```

Where `{ULTRASKILLS_REPO}` = the ultraskills repo root (same dir as `index.json`).

To find the repo root from this file's location:
```python
import os
hub_dir = os.path.dirname(os.path.abspath(__file__))  # .../devops/ultraskills-hub
repo_root = os.path.abspath(os.path.join(hub_dir, "../.."))
search_script = os.path.join(hub_dir, "scripts/search.py")
```

## Available Tags

Run `python3 .../scripts/search.py --list-tags` for full tag list.

Common tags: `engineering`, `community`, `arena-winner`, `marketing`, `devops`, `productivity`, `creative`

## Index

555+ skills indexed at `{ULTRASKILLS_REPO}/index.json`. Updated automatically when new skills are added.
