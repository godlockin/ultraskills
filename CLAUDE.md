# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Default Skills

**caveman mode is ALWAYS ON** — talk like caveman by default. Cut filler words. Keep technical accuracy. Use `/caveman lite|full|ultra` to adjust intensity or "normal mode" to disable.

## Project Overview

**UltraSkills** is a 556-skill library for Claude Code. Modular, arena-ranked AI prompt patterns following the S.C.A.L.E. model. Primarily a documentation/prompt library.

---

## Repository Structure

```
ultraskills/
├── setup.sh                    # Install: hub-only / --top / --all / --remove
├── index.json                  # Machine-readable index (556 skills, arena scores)
├── SKILLS_INDEX.md             # Human-readable index (556 × 39 categories)
├── CONTRIBUTING.md             # S-Tier skill standards
├── _template_skill/            # New skill template
├── devops/
│   └── ultraskills-hub/        # ⭐ Hub search skill (main entry point)
│       └── scripts/search.py  # Keyword search over index.json
├── engineering/                # Engineering skills
├── productivity/               # Productivity tools
├── devops/                     # Skill management utilities
├── creative/                   # Creative/design skills
├── community/                  # Community-contributed skills
└── external/                   # Externally-sourced skills
```

---

## Skill Structure Standard

Every skill follows this pattern:

```
[skill-name]/
├── SKILL.md              # Required: Core definition with YAML Frontmatter
├── examples/             # Required: At least 1-3 case studies
├── templates/            # Optional: Reusable code snippets
└── resources/            # Optional: Documentation, images
```

**SKILL.md must include YAML frontmatter:**
```yaml
---
name: [Skill Name]
description: [One-line description]
version: 1.0.0
tags: [tag1, tag2]
---
```

---

## Skill Categories

| Category | Description |
|----------|-------------|
| `engineering/` | Prompt optimization, git workflows, code patterns |
| `productivity/` | Media downloading, task analysis |
| `devops/` | Skill management, GitHub automation |
| `creative/` | Design, video, art generation skills |
| `community/` | Community-contributed skills |
| `external/` | Externally-sourced skills |

---

## Development Commands

**Skill Management:**
- Skills indexed in `index.json` — update when adding skills
- Use `_template_skill/` as template for new skills

**Python Helper Scripts:**
- `devops/skill-manager/scripts/` — Skill lifecycle management
- `devops/skill-evolution-manager/scripts/` — Evolution/feedback integration
- `devops/github-to-skills/scripts/` — Convert GitHub repos to skills

**Verification:**
- `devops/skill-manager/scripts/scan_and_check.py` — validate skill structure

---

## Working with Skills

1. **Finding skills**: Use `ultraskills-hub` skill to search by keyword → returns SKILL.md paths from index.json

2. **Creating new skills**: Copy `_template_skill/` to new directory, fill SKILL.md per CONTRIBUTING.md standards

3. **Updating skills**: Maintain examples, keep docs living per S.C.A.L.E. model

4. **Skill invocation**: Invoke by name via the `Skill` tool

---

## Key Files

- `index.json` — Master index (556 skills, arena scores, tags)
- `SKILLS_INDEX.md` — Human-readable index (39 categories, arena winners)
- `CONTRIBUTING.md` — S-Tier skill standards
- `setup.sh` — Install skills into ~/.claude/skills/
- `devops/ultraskills-hub/scripts/search.py` — Hub search engine

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

Key routing rules:
- Search for skills, find what skill to use → invoke ultraskills-hub
- Code review, check my diff → invoke review
- Save progress, checkpoint, resume → invoke checkpoint
- Code quality, health check → invoke health
- Architecture review → invoke plan-eng-review
- Design system, brand → invoke design-consultation
- Visual audit, design polish → invoke design-review
- Weekly retro → invoke retro
