# Sample Audit Report

This is an example output from `skills-audit`.

## Scenario: User with redundant plugins

User has enabled plugins that duplicate ultraskills content:

```bash
$ python3 devops/skills-audit/scripts/audit.py --full

╔══════════════════════════════════════════════════════════════╗
║                     SKILLS AUDIT REPORT                      ║
╠══════════════════════════════════════════════════════════════╣
║ Redundant plugins:   4                                        ║
║ Low-quality skills:  15                                       ║
║ Niche skills:        52                                       ║
║ Est. token savings:  ~40,000 tokens/session                  ║
╚══════════════════════════════════════════════════════════════╝

⚠️  REDUNDANT PLUGINS
   superpowers@claude-plugins-official
     → 14 skills already in ultraskills
       Examples: receiving-code-review, systematic-debugging, brainstorming, ...
     💡 Disable plugin, use ultraskills-hub instead

   fullstack-dev-skills@fullstack-dev-skills
     → 66 skills in external/fullstack-dev-skills/
       Examples: terraform-engineer, rust-engineer, react-expert, ...
     💡 Disable plugin (already indexed)

   planning-with-files@community
     → 1 skills already in ultraskills
       Examples: planning-with-files
     💡 Disable plugin, use ultraskills-hub instead

   frontend-design@claude-plugins-official
     → 1 skills already in ultraskills
       Examples: frontend-design
     💡 Disable plugin, use ultraskills-hub instead

⚠️  LOW-QUALITY SKILLS
   caveman-stats                    score=0.0  [auxiliary (not standalone)]
   videocut:安装                    score=4.7  [low score (4.7)]
   huashu-info-search              score=4.8  [low score (4.8)]
   ...

📦 NICHE SKILLS (candidates for lazy-load)
   scientific: 47 skills
     scanpy, rdkit, qiskit, biopython, deepchem, ... (+42 more)
   financial: 15 skills
     comps-analysis, dcf-model, lbo-model, pitch-deck, ... (+10 more)
   translations: 5 skills
     pua-ja, planning-with-files-zht, planning-with-files-ar, ...

💡 RECOMMENDATIONS:
   1. Disable 4 redundant plugins (run with --fix)
   2. Consider lazy-loading 47 scientific skills
   3. Remove 5 translation variants (use i18n)
```

## Auto-fix

```bash
$ python3 devops/skills-audit/scripts/audit.py --fix

✅ Disabled 4 redundant plugins:
   - superpowers@claude-plugins-official
   - fullstack-dev-skills@fullstack-dev-skills
   - planning-with-files@community
   - frontend-design@claude-plugins-official

Restart Claude Code for changes to take effect.
```

## JSON Output

```bash
$ python3 devops/skills-audit/scripts/audit.py --json

{
  "redundant_plugins": [
    {
      "plugin": "superpowers@claude-plugins-official",
      "overlap_count": 14,
      "overlap_skills": ["brainstorming", "dispatching-parallel-agents", ...],
      "source": "community/"
    }
  ],
  "low_quality_skills": [...],
  "niche_skills": {
    "scientific": [...],
    "financial": [...],
    "translations": [...]
  },
  "token_savings": 40000
}
```
