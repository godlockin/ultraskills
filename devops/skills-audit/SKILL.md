---
name: skills-audit
description: >
  Audit user's Claude Code plugins and skills configuration. Detects redundancies
  with ultraskills, identifies low-quality or unused skills, and recommends
  optimizations to reduce context overhead. Use when asked to "audit my skills",
  "check my plugins", "optimize my setup", or "reduce context usage".
version: 1.0.0
tags: [devops, audit, optimization, context]
---

# Skills Audit

Analyze Claude Code configuration to optimize skills/plugins usage.

## Trigger

`/skills-audit`, "audit my skills", "check my plugins", "optimize my setup", "what skills am I using"

## Process

Run the audit script:

```bash
python3 devops/skills-audit/scripts/audit.py
```

Or with options:

```bash
# Full report with recommendations
python3 devops/skills-audit/scripts/audit.py --full

# JSON output for programmatic use
python3 devops/skills-audit/scripts/audit.py --json

# Auto-fix (disable redundant plugins)
python3 devops/skills-audit/scripts/audit.py --fix
```

## What It Checks

### 1. Plugin Redundancy
Scans `~/.claude/settings.json` for enabled plugins that duplicate skills already in ultraskills index.

Example output:
```
⚠️  REDUNDANT PLUGINS (4 found)
   superpowers@claude-plugins-official
     → 14 skills already in ultraskills (receiving-code-review, systematic-debugging, ...)
     Recommendation: Disable plugin, use ultraskills-hub search instead

   fullstack-dev-skills@fullstack-dev-skills
     → 66 skills in external/fullstack-dev-skills/
     Recommendation: Disable plugin (already indexed)
```

### 2. Skill Quality
Flags skills with:
- Score < 5.0 (low quality)
- Empty/broken description (parsing issues)
- `auxiliary: true` (helper skills, not standalone)

### 3. Context Overhead
Estimates token cost of loaded skills and suggests reductions:
- Unused niche skills (scientific, financial) that could be lazy-loaded
- Translation variants when original exists
- Deprecated skills with better alternatives

### 4. Duplicate Detection
Finds skills with same/similar functionality:
- Same name in different paths
- Same description across skills
- Overlapping trigger words

## Output

```
╔══════════════════════════════════════════════════════════════╗
║                    SKILLS AUDIT REPORT                       ║
╠══════════════════════════════════════════════════════════════╣
║ Plugins enabled:     5                                       ║
║ Redundant plugins:   4 (80%)                                 ║
║ Skills indexed:      600                                     ║
║ Low-quality skills:  15 (2.5%)                               ║
║ Est. context saved:  ~12,000 tokens/session                  ║
╚══════════════════════════════════════════════════════════════╝

RECOMMENDATIONS:
1. Disable 4 redundant plugins (save ~8k tokens)
2. Mark 47 scientific skills as niche (lazy-load)
3. Remove 5 translation variants (use i18n instead)

Run with --fix to apply recommendation #1 automatically.
```

## Integration

Works with:
- `~/.claude/settings.json` (plugins config)
- `~/.claude/skills/` (installed skills)
- `index.json` (ultraskills master index)
- `~/.claude/plugins/installed_plugins.json` (plugin cache)
