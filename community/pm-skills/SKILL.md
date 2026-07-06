---
name: pm-skills
description: "Product management workflow collection (22 skills across the full PM lifecycle — discovery, strategy, execution, GTM, data analytics) from phuryn/pm-skills v2.1.0. Encodes proven frameworks from Teresa Torres (Continuous Discovery), Marty Cagan (Inspired), Alberto Savoia (assumption testing), Geoffrey Moore (beachhead segment). Use when doing product discovery, writing a PRD, mapping opportunities, running pre-mortems, prioritizing features, building growth loops, designing experiments, analyzing cohorts or A/B tests, creating competitive battlecards, drafting product vision, or any PM lifecycle task. Triggers: 'product discovery', 'opportunity solution tree', 'OST', 'write a PRD', 'product requirements', 'user interview', 'pre-mortem', 'red team strategy', 'growth loops', 'beachhead segment', 'lean canvas', 'SWOT', 'Porter five forces', 'value proposition', 'cohort analysis', 'A/B test analysis', 'competitive battlecard', 'stakeholder map', 'prioritization framework', 'release notes', 'product vision', 'product strategy'."
version: 1.0.0
tags: [product-management, pm, discovery, strategy, execution, gtm, prd, okr, growth, marketing, community]
source: https://github.com/phuryn/pm-skills
source_version: v2.1.0
license: MIT
---

# PM Skills — Product Management Workflow Collection

Curated subset (22 of 68) of `phuryn/pm-skills` covering the full PM lifecycle. Each sub-skill is a self-contained SKILL.md under this directory tree. Invoke by description match or by path.

## Structure

```
pm-skills/
├── discovery/                  # Continuous discovery + assumption testing
│   ├── opportunity-solution-tree    # Teresa Torres OST
│   ├── brainstorm-ideas-new
│   ├── identify-assumptions-new
│   ├── prioritize-assumptions
│   ├── interview-script
│   └── summarize-interview
├── strategy/                   # Strategic frameworks
│   ├── product-vision
│   ├── value-proposition
│   ├── lean-canvas
│   ├── swot-analysis
│   └── porters-five-forces
├── execution/                  # PRDs, OKRs, sprint planning, risk
│   ├── create-prd                # 8-section PRD template
│   ├── pre-mortem
│   ├── prioritization-frameworks  # 9 frameworks reference
│   ├── stakeholder-map
│   └── release-notes
├── gtm/                        # Go-to-market + growth
│   ├── growth-loops
│   ├── competitive-battlecard
│   └── beachhead-segment         # Geoffrey Moore
├── data/                       # Analytics
│   ├── cohort-analysis
│   └── ab-test-analysis
└── toolkit/
    └── dummy-dataset
```

## Lifecycle Routing

| Stage | Skills |
|-------|--------|
| **Discover** what to build | opportunity-solution-tree → brainstorm-ideas-new → identify-assumptions-new → prioritize-assumptions |
| **Validate** with users | interview-script → summarize-interview |
| **Define** strategy | product-vision → value-proposition → lean-canvas → swot-analysis → porters-five-forces |
| **Plan** execution | create-prd → prioritization-frameworks → stakeholder-map |
| **Mitigate** risk | pre-mortem → release-notes |
| **Launch** to market | beachhead-segment → competitive-battlecard → growth-loops |
| **Measure** outcomes | cohort-analysis → ab-test-analysis → dummy-dataset |

## Trigger Patterns

- "I need to write a PRD" → `execution/create-prd`
- "Help me prioritize features" → `execution/prioritization-frameworks`
- "Map our opportunities" → `discovery/opportunity-solution-tree`
- "Run a pre-mortem on this plan" → `execution/pre-mortem`
- "Build growth loops" → `gtm/growth-loops`
- "Analyze this cohort" → `data/cohort-analysis`
- "Set up A/B test analysis" → `data/ab-test-analysis`
- "Draft a battlecard" → `gtm/competitive-battlecard`
- "Interview customers about X" → `discovery/interview-script`
- "Where should we launch first?" → `gtm/beachhead-segment`
- "Review our positioning" → `strategy/value-proposition` or `swot-analysis`

## Design Philosophy (from upstream)

- **Skills = concepts.** Frameworks and analytical knowledge auto-loaded by description match.
- **No cross-plugin hard references.** Each skill stands alone; chaining is suggested in natural language, not enforced.
- **Frontmatter is lean, body has depth.** Progressive disclosure.
- **Methodology-first.** Each skill encodes a named, cited PM framework (Teresa Torres, Marty Cagan, Alberto Savoia, Geoffrey Moore, Dan Olsen).

## Source

- Upstream: `https://github.com/phuryn/pm-skills` (MIT, 22.6k stars, v2.1.0 / 2026-07-03)
- Synced via submodule at `external/phuryn-pm-skills`
- This wrapper curates 22 skills covering the full PM lifecycle; remaining 46 upstream skills are accessible directly via the submodule path.

## Complementary Skills (already in UltraSkills)

These existing skills complement but do not duplicate this collection — use them when scope is narrower:

- `to-prd` — quick PRD draft from conversation context
- `feature-prioritization` — quick RICE/ICE/KANO scoring (subset of prioritization-frameworks)
- `okr-alignment-checker` — validates cascading, does not generate
- `user-story-mapper` — visual journey mapping
- `user-persona-generator` — research-based persona synthesis
- `competitive-analysis` — institutional-grade comp analysis (financial focus)
- `comps-analysis` — financial comparable companies
- `ab-test-setup` — experiment design (use pm-skills `ab-test-analysis` for post-hoc analysis)
- `retro` — sprint retro (use pm-skills `pre-mortem` for forward-looking risk)
- `launch-strategy` — basic launch planning
- `pricing-strategy` — pricing model selection