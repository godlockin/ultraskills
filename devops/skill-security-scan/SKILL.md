---
name: skill-security-scan
description: Pre-install security gate for community and external skills. Wraps NVIDIA SkillSpector (64 patterns / 16 categories: prompt injection, MCP tool poisoning, memory poisoning, supply-chain CVEs) to score 0-100 with SAFE / CAUTION / DO NOT INSTALL bands. Run before merging any community/ or external/ skill. Triggers: "scan skill security", "check skill safety", "security gate", "skill audit".
version: 1.0.0
tags: [devops, security, gate, audit]
---

# Skill Security Scan

## Goal

Pre-install security gate. Block any `community/` or `external/` skill that contains prompt-injection payloads, data-exfiltration patterns, poisoned MCP tool definitions, or known supply-chain vulnerabilities.

## When to use

- Before merging a new community/ skill PR
- Before adding a new external/ submodule
- Periodically on existing skills (re-scan when SkillSpector patterns update)
- In CI as a required check

## Quick command

```bash
# One-time setup (Python 3.12+ in a venv)
git submodule update --init --recursive
pip install -e external/skillspector/

# Scan a skill (static-only, no API key needed)
python3 devops/skill-security-scan/scripts/run_skillspector.py <skill-path> --no-llm

# Example: scan a community skill
python3 devops/skill-security-scan/scripts/run_skillspector.py community/remotion --no-llm
```

## Decision matrix

| Band | Risk Score | Critical Patterns | Action |
|------|------------|-------------------|--------|
| **SAFE** | 0-29 | None | Merge allowed |
| **CAUTION** | 30-69 | None | Manual review by maintainer; document in PR |
| **DO NOT INSTALL** | ≥70 OR any "critical" | Hard block | Reject PR; ask upstream to fix |

## Integration with health check

The wrapper is wired into the skill-manager health check (Stage 2.5) — after structure/examples checks, before tags check. Run the full pipeline:

```bash
# from repo root
python3 devops/skill-manager/scan_and_check.py --health community/
```

The security stage only runs on `community/*` and `external/*` paths; `devops/` and `engineering/` skills are skipped (they're authored in-house).

## Fallback behavior

If SkillSpector is not installed (`skillspector` binary missing), the gate **skips with a clear warning** — it never silently passes. The warning is:

```
WARN: [skill-name] security scan skipped: skillspector CLI not found
WARN:        install with: pip install -e external/skillspector/
```

## Architecture

```
devops/skill-security-scan/
├── SKILL.md                        # This file
├── .no-skill                       # Opt out of arena indexing (it's a tool, not a content skill)
├── scripts/
│   ├── run_skillspector.py         # Thin shim: `skillspector scan <path> --no-llm --format json`
│   └── health_gate.py              # Parses SkillSpector JSON, returns List[str] of warnings
├── examples/
│   └── scan-community-skill.md     # Walkthrough
└── references/
    └── skillspector-patterns.md    # 16 detection categories
```

External dependency: `external/skillspector/` (git submodule tracking NVIDIA/SkillSpector upstream, Apache 2.0).

## References

- `references/skillspector-patterns.md` — full list of 16 detection categories
- `examples/scan-community-skill.md` — step-by-step walkthrough
- [NVIDIA/SkillSpector on GitHub](https://github.com/NVIDIA/SkillSpector) — upstream repo
