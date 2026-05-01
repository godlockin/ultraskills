---
name: learn-from-loss
description: Structured postmortem methodology for competition results — multi-expert panel review, 8-dimension scoring, winner-vs-loser gap analysis, and lessons codification
version: 1.0.0
tags: [postmortem, review, analysis, competition, retrospective, scoring]
---

# Postmortem Review — Learn More from Losing Than Winning

## Overview

A structured postmortem turns a loss into a reusable playbook. This skill provides the methodology used after WDC 2026 APAC: analyze every winner across 8 dimensions, run a 3-agent independent expert panel, codify lessons into iron rules and pass criteria, and build a Day-0 checklist for next time.

## When to Use

- After a competition result (win or loss — both have lessons)
- When preparing a retrospective for a high-stakes presentation
- When comparing your deliverable against competitors
- When codifying team knowledge into reusable playbooks

## Phase 1: Winner Analysis (Day 0–1)

### Collect All Winners

Don't just look at 1st place. Analyze the top 3–5 and any team that scored differently from you.

```markdown
| Rank | Team | Carrier | Hook | Score | What They Did Differently |
|------|------|---------|------|-------|--------------------------|
| 1 | Data Five | HTML | "五行缺数据" | 92 | Cultural team name, hover interactions |
| 2 | Vikings | Video | "came for data, stayed for insights" | 89 | Multi-voice, quotable closing |
| 3 | Insights Fund | QR → App | Scan to use | 87 | Zero-friction adoption |
| ... | Us | PPT | "EKET Plan A" | 72 | Strong content, poor delivery |
```

### 8-Dimension Scoring Matrix

Score yourself AND each winner on the same 8 dimensions (1–10 scale):

| # | Dimension | What It Measures |
|---|-----------|-----------------|
| 1 | Carrier convenience | How easy is it for the judge to open/engage? |
| 2 | Memorability | Can the judge recite a line 24h later? |
| 3 | Actionability | Does the judge know what to do next? |
| 4 | Market coverage | Are all markets represented equally? |
| 5 | Methodology rigor | Is the analysis defensible and replicable? |
| 6 | Visual consistency | Does every slide look like the same team made it? |
| 7 | Sensory quality | Audio, spelling, paths — zero debt? |
| 8 | Story arc | Does the deck have a beginning, middle, end? |

### Gap Identification

For each dimension where you scored below the winner:

```markdown
| Dimension | Us | Winner | Gap | Root Cause | Fix |
|-----------|----|--------|-----|-----------|-----|
| 1 Carrier | 4 | 9 | -5 | Chose PPT without questioning | Day-0 carrier workshop |
| 2 Memorability | 3 | 9 | -6 | Generic team name, no hook | Cultural pun + origin story |
| 4 Coverage | 5 | 8 | -3 | 80% China content | 5-country skeleton locked early |
```

## Phase 2: Independent Expert Panel Review (Day 1–2)

### Panel Composition

Run 3 parallel reviewers, each with a distinct lens:

| Agent | Focus | Checks |
|-------|-------|--------|
| Content Accuracy | Data vs claims | YAML ↔ HTML consistency, footnote accuracy, citation verification |
| Design System | Visual quality | CSS token usage, WCAG contrast, hardcoded colors, responsive scaling |
| Audio & Pipeline | Production quality | Voice script accuracy, silence ratios, toolchain completeness, file integrity |

### Review Protocol

Each agent receives:
1. The full deck directory
2. The content source of truth (`content.yaml`)
3. The design token file (`tokens.css`)
4. The audio files and build script
5. A checklist of known failure patterns

Each agent outputs:

```markdown
## Review: [Agent Name]
**Verdict:** PASS / CONDITIONAL PASS / FAIL

### Issues Found
| # | Severity | File | Line | Description | Suggested Fix |
|---|----------|------|------|-------------|---------------|
| 1 | P0 | 06_korea.html | 285 | Footnote cites proxy source | Replace with neutral text |
| 2 | P1 | 03_india.html | 273 | Chart path is absolute | Change to ../assets/ |
| 3 | P2 | tokens.css | 45 | Missing badge tokens | Add --badge-signed etc. |

### Summary
[2–3 sentences on overall quality]
```

### Severity Scale

| Level | Definition | Action |
|-------|-----------|--------|
| P0 | Blocks submission. Judges will notice. | Fix immediately |
| P1 | Degrades quality. Attentive judges notice. | Fix before submission |
| P2 | Minor inconsistency. Won't affect score. | Fix if time permits |

## Phase 3: Fix and Re-Review (Day 2–3)

### Fix Priority Order

1. All P0 issues (blocking)
2. All P1 issues (quality)
3. P2 issues if time permits
4. Run lint scripts to verify

### Re-Review Protocol

After fixes, run the same 3 agents again but only check:
- Previously flagged items (did the fix work?)
- Adjacent files (did the fix introduce new issues?)
- Full lint pass (text + audio)

## Phase 4: Codification (Day 3–4)

### Extract Iron Rules

From the gap analysis and review, extract 5–7 non-negotiable rules. Format:

```markdown
### Rule Name

<what the rule says — one sentence>

| Good | Bad | Why |
|------|-----|-----|
| Example from winner | Example from loser | Mechanism |
```

### Define Pass Criteria

For each iron rule, define a binary pass/fail gate:

```markdown
| # | Gate | Standard | Verification Method |
|---|------|----------|-------------------|
| G1 | Carrier works | Opens on clean machine | Test on VM |
| G2 | 5-country balance | Each country ≥ 1 page | Slide count |
```

### Define Bonus Items

What the winners did that pushed them from "solid" to "unforgettable":

```markdown
| # | Bonus | Effect | Who Did It |
|---|-------|--------|-----------|
| B1 | Cultural pun name | Dual-culture resonance | Data Five |
| B2 | QR code link | Zero-friction adoption | Insights Fund |
```

### Build Day-0 Checklist

Every competition starts with this checklist:

```markdown
□ Judge persona workshop (who, what KPIs, what they carry out)
□ Team name + origin story + 1 metaphor (within 4 hours)
□ Default carrier ≠ PPT (disprove PPT first)
□ Pre-mortem: "if we lose, why?"
□ N-dimension symmetric skeleton (locked early)
□ External cold read (before last third of timeline)
□ Lint all pass (before submission)
```

## Anti-Patterns

1. **"We lost because of X" (single cause)** — Losses are always multi-causal. Use the 8-dimension matrix to find ALL gaps.
2. **"The winners just got lucky"** — Luck doesn't produce consistent patterns across multiple winners. Study what they did deliberately.
3. **"Our content was strong, only the format was wrong"** — If the format prevents engagement, the content never existed for the judge.
4. **"Next time we'll just try harder"** — "Harder" is not a strategy. Iron rules and pass criteria are.
5. **Skipping the independent panel** — Self-review has blind spots. External reviewers catch what you can't.

## Deliverables Checklist

A complete postmortem produces:

- [ ] Winner analysis matrix (8 dimensions × all teams)
- [ ] Gap identification table (per dimension: us vs winner)
- [ ] 3-agent independent review (content + design + audio)
- [ ] Fix log (what was fixed, what was deferred)
- [ ] Iron rules document (5–7 non-negotiable rules)
- [ ] Pass criteria (binary gates, each with verification method)
- [ ] Bonus items (what winners did that we didn't)
- [ ] Day-0 checklist (for next competition)
- [ ] Next-level upgrade path (what to improve if given more time)

## Template: Postmortem Document Structure

```markdown
# [Project] Postmortem

## 1. Result Summary
- Score: X/100
- Rank: N of M
- Top gap: [dimension] (-Y vs winner)

## 2. Winner Analysis
[8-dimension matrix]

## 3. Gap Analysis
[Per-dimension: us vs winner, root cause, fix]

## 4. Expert Panel Review
### 4.1 Content Accuracy
[Agent findings]
### 4.2 Design System
[Agent findings]
### 4.3 Audio & Pipeline
[Agent findings]

## 5. Iron Rules (L1–L6)
[Non-negotiable rules with examples]

## 6. Pass Criteria (G1–G8)
[Binary gates with verification methods]

## 7. Bonus Items (B1–B8)
[Nice-to-haves that separate good from unforgettable]

## 8. Next-Level Upgrade Path
[From current state to end state, with investment estimates]

## 9. Day-0 Checklist
[For next competition]
```
