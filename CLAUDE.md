# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Default Skills

**caveman mode is ALWAYS ON** — talk like caveman by default. Cut filler words. Keep technical accuracy. Use `/caveman lite|full|ultra` to adjust intensity or "normal mode" to disable.

## Project Overview

**UltraSkils** is an extensive AI Skills library that defines modular, reusable, and verifiable AI prompt patterns following the S.C.A.L.E. model (Standardized, Composable, Automated/Auditable, Living, Examples). This is primarily a documentation/prompt library rather than a traditional code project.

---

## Repository Structure

```
ultraskils/
├── index.json                  # Machine-readable skill index (auto-generated)
├── README.md                  # Library entry point
├── CONTRIBUTING.md            # S-Tier skill standards and contribution guide
├── _template_skill/           # Template for creating new skills
│   ├── SKILL.md              # Skill definition with YAML frontmatter
│   ├── examples/             # Usage examples
│   ├── templates/            # Reusable templates
│   └── resources/            # Documentation, cheat sheets
├── engineering/              # Engineering-focused skills
├── productivity/             # Productivity tools
├── devops/                   # Skill management utilities
├── creative/                 # Creative/design skills
└── community/                # Community-contributed skills
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
| `community/` | Third-party and extended skills |

---

## Development Commands

This is primarily a prompt library. Development involves:

**Skill Management:**
- Skills are indexed in `index.json` - keep it updated when adding skills
- Use `_template_skill/` as the template for new skills

**Python Helper Scripts:**
- `devops/skill-manager/scripts/` - Skill lifecycle management
- `devops/skill-evolution-manager/scripts/` - Skill evolution/feedback integration
- `devops/github-to-skills/scripts/` - Convert GitHub repos to skills

**Verification:**
- Run `devops/skill-manager/scripts/scan_and_check.py` to validate skill structure
- Ensure all new skills have YAML frontmatter and at least one example

---

## Working with Skills

1. **Finding skills**: Check `index.json` for the complete skill catalog with paths and descriptions

2. **Creating new skills**: Copy `_template_skill/` to a new directory, fill in the SKILL.md following CONTRIBUTING.md standards

3. **Updating skills**: Follow the S.C.A.LE. model - maintain examples, keep documentation living

4. **Skill invocation**: Each skill in the catalog can be invoked by name via the `Skill` tool

---

## Key Files

- `index.json` - Master index of all available skills with metadata
- `CONTRIBUTING.md` - Detailed S-Tier skill standards
- `_template_skill/SKILL.md` - Template for new skills
- `README.md` - User-facing library documentation
- `.envrc` - Environment configuration (likely for direnv)
## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

Key routing rules:
- Product ideas, "is this worth building", brainstorming → invoke office-hours
- Bugs, errors, "why is this broken", 500 errors → invoke investigate
- Ship, deploy, push, create PR → invoke ship
- QA, test the site, find bugs → invoke qa
- Code review, check my diff → invoke review
- Update docs after shipping → invoke document-release
- Weekly retro → invoke retro
- Design system, brand → invoke design-consultation
- Visual audit, design polish → invoke design-review
- Architecture review → invoke plan-eng-review
- Save progress, checkpoint, resume → invoke checkpoint
- Code quality, health check → invoke health
