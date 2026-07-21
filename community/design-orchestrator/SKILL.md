---
name: design-orchestrator
description: "Routes design requests to the right skill in the 22-skill design cluster, and composes them into end-to-end pipelines. Three orchestration paths (greenfield / existing / inspiration) cover 80% of design requests. Includes routing decision table, anti-slop index cross-referencing hallmark 53 gates + ui-ux-pro-max 161 rules + awwwards anti-patterns. Trigger on 'build a new design from scratch', 'redesign this site', 'extract DNA from URL/screenshot', 'audit the design', 'I want a SaaS landing page', or any design brief that does not map to a single skill."
version: 1.0.0
tags: [design, orchestrator, router, design-system, ui, ux, anti-slop, greenfield, redesign, inspiration, community]
---

# Design Orchestrator

> 22 design skills, one entry point. Routes, composes, never duplicates.

## 🎯 Goal

UltraSkills has 22 design-related skills across two clusters (`设计·UX/产品设计`, `设计·产品UX`). New users face three problems:
1. **Routing confusion** — which skill to invoke first?
2. **Composition gap** — no skill tells you how to chain them
3. **Anti-slop fragmentation** — rules live in hallmark (53 gates), ui-ux-pro-max (161 rules), awwwards (12 trends), but no unified index

This skill is the **conductor** for the design cluster. It:
- Routes a brief to 1-N right skills via a decision table
- Composes 3 end-to-end pipelines (greenfield / existing / inspiration)
- Cross-references (not duplicates) every anti-pattern rule across the cluster
- Includes version sync mechanism so upstream bumps don't silently desync

## 🧠 Core Concepts

### The 22-Skill Map (canonical)

| Cluster | Skill | Score | Verb (what it does) |
|---------|-------|-------|---------------------|
| UX/产品设计 | ui-ux-pro-max-skill | 9.0 | Generates complete design system |
| UX/产品设计 | design-consultation | 8.8 | Consultation + DESIGN.md creation |
| UX/产品设计 | design-review | 8.8 | Visual audit + atomic fixes |
| UX/产品设计 | design-shotgun | 8.8 | Multi-variant exploration |
| UX/产品设计 | plan-design-review | 8.8 | Plan-mode design critique |
| UX/产品设计 | design-html | 8.8 | Final HTML/CSS implementation |
| UX/产品设计 | design-tokens | 8.0 | DTCG tokens → multi-platform |
| UX/产品设计 | figma-to-code | 8.0 | Figma → React/Vue |
| UX/产品设计 | icon-system | 8.0 | 100k+ icons integration |
| UX/产品设计 | motion-design | 8.0 | 12 microinteraction patterns |
| UX/产品设计 | "ikea-designer-pro" | 6.8 | IKEA brand role |
| 产品UX | hallmark | 9.2 | Anti-AI-slop 4 verbs + 20 themes |
| 产品UX | design-system | 7.8 | Audit/document/extend |
| 产品UX | write-spec | 7.8 | PRD/Spec |
| 产品UX | color-expert | 7.3 | Color knowledge base |
| 产品UX | metrics-review | 7.3 | Metrics analysis |
| 产品UX | stakeholder-update | 7.3 | Status updates |
| 产品UX | design-critique | 6.8 | Multi-dim feedback |
| 产品UX | design-handoff | 6.8 | Engineering handoff spec |
| 产品UX | accessibility-review | 6.3 | WCAG 2.1 AA audit |
| 产品UX | ux-copy | 6.3 | UX microcopy |
| community | awesome-design-md | 10.0 | 68 brand DESIGN.md |
| community | design-an-interface | 9.5 | Parallel API/interface design |
| community | awwwards-design-intelligence | n/a | 5 Awwwards pattern categories |

**Important**: This skill is a router — it does **not** generate design itself. When invoked, it tells the model *which* skill to call next, *in what order*, *with what context*.

## 🚀 Workflow

### Phase 1 — Routing (Decision Table)

When the user says anything about design, run the decision table to find the right entry skill.

**Routing rules:**

1. **Detect cluster signal** — does the user want brand/style/inspiration, or want to build/audit/redesign?
2. **Detect project state** — greenfield, existing code, or inspiration (screenshot/URL)?
3. **Detect single vs. multi-skill** — is this one-shot (e.g. "audit this"), or pipeline-worthy (e.g. "build a SaaS landing page")?
4. **Map to entry skill** + recommend composition path (Phase 2)

### Phase 2 — Composition (3 Pipelines)

Three paths cover ~80% of design requests. Use them as scaffolding; adapt as needed.

#### 🌱 Path 1: Greenfield (Build from Scratch)

**Trigger**: *"design my SaaS landing page"*, *"build a beauty spa site"*, *"I need a new site for X"*, no existing code.

```
Step 1: design-consultation          [understand product + landscape + brand voice]
Step 2: ui-ux-pro-max-skill          [generate design system: pattern + style + palette + typography + anti-patterns]
Step 3: design-tokens                [compile DTCG tokens → CSS vars / Tailwind / SCSS / JSON]
Step 4: motion-design                [add 2-3 microinteractions, NOT for decoration]
Step 5: icon-system                  [pull icons from Lucide / Phosphor / Heroicons]
Step 6: awwwards-design-intelligence [cross-check: does the design avoid Awwwards anti-patterns?]
Step 7: hallmark audit               [pass all 53 slop-test gates; refuse italic headers / purple gradients / 3-icon grids]
Step 8: design-html                  [final Pretext-native HTML/CSS output]
```

#### 🔧 Path 2: Existing Site (Audit + Redesign)

**Trigger**: *"redesign this site"*, *"audit /workspace"*, *"this design feels AI-generated"*, has existing code.

```
Step 1: plan-design-review           [plan-mode critique: 0-10 dimensions, fix plan first]
Step 2: design-review                [live visual audit + atomic fixes]
Step 3: accessibility-review         [WCAG 2.1 AA pass: contrast 4.5:1, keyboard nav, touch targets]
Step 4: hallmark audit <target>      [slop-test: 53 gates scored]
Step 5: design-shotgun               [if user wants variants: generate N options]
Step 6: design-html                  [final Pretext-native HTML/CSS with new design]
Step 7: design-handoff               [engineering spec: tokens, components, states]
```

#### 🎨 Path 3: Inspiration (URL/Screenshot → Build)

**Trigger**: *"make it look like Stripe"*, *"I saw this site..."*, *"use [brand] style"*, attaches image/URL.

```
Step 1: awwwards-design-intelligence [if URL: extract DNA — pattern / colors / typography]
        OR awesome-design-md           [if brand named: load that brand's DESIGN.md]
        OR hallmark study              [if screenshot: extract DNA, refuse pixel-clones]
Step 2: design-an-interface          [generate 3 radically different module shapes in parallel]
Step 3: ui-ux-pro-max-skill          [generate adapted design system for YOUR brand]
Step 4: design-tokens                [compile tokens]
Step 5: hallmark audit               [slop-test against inspiration, ensure not literal clone]
Step 6: design-html                  [final HTML/CSS with user's brand voice]
```

### Phase 3 — Anti-Slop Index (Cross-References)

This skill **never duplicates** anti-pattern rules. Instead, it points to the right one. Quick lookup:

| Category | Source | Where |
|----------|--------|-------|
| **Slop-test gates (53)** | hallmark | `references/slop-test.md` |
| **Industry reasoning (161 rules)** | ui-ux-pro-max-skill | `community/ui-ux-pro-max-skill/SKILL.md` + `references/` |
| **Awwwards anti-patterns (12)** | awwwards-design-intelligence | `community/awwwards-design-intelligence/SKILL.md` Anti-patterns section |
| **WCAG 2.1 AA (4.5:1 contrast)** | accessibility-review | `external/knowledge-work-plugins/design/skills/accessibility-review/SKILL.md` |
| **Design system consistency** | design-system | `external/knowledge-work-plugins/design/skills/design-system/SKILL.md` |

For a complete session-zero anti-slop pass, the orchestrator runs **hallmark audit** + **awwwards check** + **accessibility-review** as the final QA gate of any greenfield or redesign pipeline.

## 💡 Best Practices

### Do

- **Always ask "greenfield / existing / inspiration" first** if the brief is ambiguous
- **Chain 3-6 skills max per pipeline** — more = coordination overhead, not quality
- **Run `hallmark audit <target>` as the last step** of any build/redesign — it has 53 gates, single best anti-slop filter
- **Use `design-an-interface` for module-shaped asks** ("design the upload flow") — it's parallel-agents-based, faster than ui-ux-pro-max
- **Use `design-shotgun` for visual brainstorming only** — it produces variants, not final design
- **Cross-check brand identity with `color-expert`** when user names a color (free MIT, 140 reference files)

### Don't

- **Don't run all 22 skills on every request** — chains die of overhead. Pick 3-6.
- **Don't invoke ikea-designer-pro unless user explicitly asks for IKEA-style role** — it's roleplay, not a generic skill
- **Don't bypass hallmark audit at end of pipeline** — the 53 gates are not optional
- **Don't conflate `design-consultation` (gstack) with `design-system` (knowledge-work)** — first creates DESIGN.md from scratch, second audits/documents existing
- **Don't mix `awesome-design-md` (68 brands) with `hallmark` 20 themes** — first is "look like Stripe", second is "anti-slop structural variety"

## 🔀 Routing Decision Table (Use This First)

```
┌─────────────────────────────────┬────────────────────────────────────┐
│ User says                       │ Route to                           │
├─────────────────────────────────┼────────────────────────────────────┤
│ "build / new / from scratch"    │ Path 1 (Greenfield)                │
│   + has brief                   │ → design-consultation              │
│ "design [feature/component]"    │ → design-an-interface              │
│ "I want a [style] site"         │ Path 1 + awesome-design-md step    │
│ "redesign this" / "make it     │ Path 2 (Existing)                  │
│   better"                       │ → plan-design-review first         │
│ "audit" / "review the design"  │ Path 2 Step 1+2: design-review     │
│ "looks AI-generated" / "slop"  │ → hallmark audit + awwwards check  │
│ "make it look like [brand]"    │ Path 3 (Inspiration)               │
│ "use [brand] style"            │ → awesome-design-md first          │
│ "look like this URL/screenshot"│ Path 3 Step 1: awwwards OR hallmark│
│ "color theory" / "what color"  │ → color-expert (single skill)      │
│ "accessibility / a11y / WCAG"  │ → accessibility-review             │
│ "PRD" / "spec" / "requirements"│ → write-spec (NOT design)         │
│ "metrics" / "data review"      │ → metrics-review (NOT design)      │
│ "Icons" / "icon library"       │ → icon-system (single skill)       │
│ "Animation" / "motion"         │ → motion-design (single skill)     │
│ "Tokens" / "design system JSON"│ → design-tokens (single skill)     │
└─────────────────────────────────┴────────────────────────────────────┘
```

## 🔧 Version Sync (Upstream Drift Protection)

Upstream skills bump versions independently. To prevent silent desync:

```bash
# Run after every orchestrator change OR weekly:
python3 community/design-orchestrator/scripts/version-sync-check.py
```

This script:
- Reads each referenced upstream's `SKILL.md` frontmatter `version`
- Compares to last-known-good (cached in `.design-orch-version-cache.json`)
- Outputs warnings: `[WARN] hallmark: 1.1.0 → 1.2.0 — orchestrator references anti-slop gates`
- Exit 0 if all aligned, 1 if any upstream moved

**When upstream bumps**:
- `ui-ux-pro-max-skill` style/palette numbers may change → re-test Path 1 Step 2
- `hallmark` adds gates → re-test any audit step
- `awesome-design-md` adds brands → orchestrator templates may need refresh
- `awwwards-design-intelligence` adds patterns → orchestrator Path 3 DNA extraction expands

## 📚 Resources

* [Routing decision table](./references/routing-table.md) — full 22-row matrix
* [Orchestration patterns](./references/orchestration-patterns.md) — 3 paths in detail
* [Anti-slop index](./references/anti-slop-index.md) — cross-referenced rules
* [Case studies](./examples/case-studies.md) — 3 paths in real scenarios
* [Version sync script](./scripts/version-sync-check.py) — upstream drift detector

---

**差异化定位**: 22 个 design skill 解决单点问题; design-orchestrator 是**调度层** — 决定何时调哪个、怎么串、怎么检. 不重复任何上游内容, 只路由 + 编排 + 引用.
