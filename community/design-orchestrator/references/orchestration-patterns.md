# Orchestration Patterns (3 End-to-End Pipelines)

Three pipelines cover ~80% of design requests. Each is a **template** — adapt steps as the brief demands, but preserve the **rhythm** (start broad, converge on tokens, finalize HTML, anti-slop gate last).

---

## 🌱 Pattern 1: Greenfield (Build from Scratch)

### When

- User has a brief, no existing code
- Project stage: ideation / first draft / MVP
- Output target: landing page, app shell, complete site

### When NOT to use

- User has existing code (use Pattern 2 instead)
- User shows a URL/screenshot (use Pattern 3 instead)

### Steps

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | design-consultation | Understand product, research landscape, propose aesthetic | aesthetic tokens (font + color preview) |
| 2 | ui-ux-pro-max-skill | Generate complete design system (pattern + style + palette + typography + anti-patterns) | Full system spec |
| 3 | design-tokens | Compile DTCG tokens → CSS / Tailwind / SCSS / JSON | Multi-platform tokens |
| 4 | motion-design | Pick 2-3 microinteractions (feedback, direction, hierarchy) | Animation snippets |
| 5 | icon-system | Pull icons from Lucide / Phosphor / Heroicons | Icon components |
| 6 | awwwards-design-intelligence | Anti-pattern check against Awwwards 12 trends + 5 patterns | Risk report |
| 7 | hallmark audit | Pass 53 slop-test gates, refuse italic headers / purple gradients / 3-icon grids | Slop pass |
| 8 | design-html | Final Pretext-native HTML/CSS output | Working code |

### Adapted "Lite" Variants

- **No animation**: Skip step 4
- **Existing brand**: Insert `awesome-design-md` between steps 2 and 3
- **Color theory question**: Insert `color-expert` between steps 1 and 2
- **Icons only**: Skip steps 4-8, just produce icon-components

### Example Trace

> User: "Build a SaaS landing for our AI-powered analytics tool. We're B2B, technical buyers, want to feel premium without being intimidating."

Orchestrator routes:
1. design-consultation (understand: AI analytics, B2B technical, premium-not-intimidating tone)
2. ui-ux-pro-max-skill (industry: SaaS / data analytics → modern-minimal, dark mode optional)
3. design-tokens (compile OKLCH palette → CSS vars + Tailwind config)
4. motion-design (subtle scroll-triggered opacity, NOT bounces)
5. icon-system (Phosphor `regular` weight, line icons)
6. awwwards-check (verify NOT Premium Black-in-Darkness; avoid Pagination UI / Bento)
7. hallmark audit (no invented metrics, no italic headers, no three-icon grid)
8. design-html (Pretext-native, 30KB, smart API routing)

---

## 🔧 Pattern 2: Existing Site (Audit + Redesign)

### When

- User has live code at `/path` or URL
- Wants to: audit, redesign, polish, fix slop
- Project stage: post-MVP, iteration

### When NOT to use

- No code exists (use Pattern 1 instead)
- User wants inspiration for a fresh build (use Pattern 3 instead)

### Steps

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | plan-design-review | Plan-mode critique, 0-10 dimensions | Plan document |
| 2 | design-review | Live visual audit + atomic fixes | Before/after screenshots |
| 3 | accessibility-review | WCAG 2.1 AA pass (contrast, keyboard, touch targets) | A11y report |
| 4 | hallmark audit `<target>` | Slop-test against 53 gates | Punch list |
| 5 | design-shotgun (optional) | Generate N redesign variants if user wants options | Comparison board |
| 6 | design-html | Final Pretext-native HTML/CSS output | Working code |
| 7 | design-handoff | Engineering spec: tokens, components, states, breakpoints | Handoff doc |

### Adapted Variants

- **Quick polish only**: Steps 2 → 4 only
- **Full rebrand**: Insert Pattern 1 between steps 5 and 6
- **A11y concern alone**: Just step 3
- **Design-system overhaul**: Insert `design-tokens` + `color-expert` between steps 5 and 6

### Example Trace

> User: "/workspace feels AI-generated. Polish it. Don't change brand or copy."

Orchestrator routes:
1. plan-design-review (get user buy-in on what "polish" means — clarify scope)
2. design-review (live audit: spacing, hierarchy, AI slop patterns)
3. accessibility-review (in case polish introduces a11y regression)
4. hallmark audit `/workspace` (53 gates — italic headers? Purple gradients? Three-icon grid? Empty catches?)
5. (skip shotgun — user said "don't change brand")
6. design-html (apply atomic fixes to existing files, additive where possible)
7. (skip handoff — internal polish)

---

## 🎨 Pattern 3: Inspiration (URL / Screenshot / Brand)

### When

- User attaches image or pastes URL
- User names a brand ("make it look like Stripe")
- User says "I saw this design..."
- Project stage: ideation, capturing reference, learning

### When NOT to use

- No inspiration material available (use Pattern 1 instead)
- User has working code at /workspace (use Pattern 2 instead)

### Steps (URL Mode)

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | awwwards-design-intelligence | Extract DNA: macrostructure, archetypes, type-pairing, color anchor | Diagnosis report |
| 2 | design-an-interface | Generate 3 radically different module shapes (parallel agents) | Variants |
| 3 | ui-ux-pro-max-skill | Adapt design system for **user's** brand (not source's) | Adapted system |
| 4 | design-tokens | Compile tokens | Multi-platform tokens |
| 5 | hallmark audit | Slop-test against inspiration, ensure not literal clone | DNA lock + slop pass |
| 6 | design-html | Final HTML/CSS with user's brand voice | Working code |

### Steps (Brand-Clone Mode)

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | awesome-design-md | Load that brand's DESIGN.md | Brand spec |
| 2 | design-consultation | Adapt brand spec to user's product | Adapted spec |
| 3 | design-html | Final HTML/CSS in brand voice | Working code |

### Steps (Screenshot Mode)

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | hallmark study | Extract DNA from screenshot, refuse pixel-clones | DNA report |
| 2 | design-an-interface | 3 variants in parallel | Variants |
| 3 | design-html | Final HTML/CSS | Working code |

### Adapted Variants

- **Just lock the DNA**: Step 1 only, produce a portable `design.md` (no code)
- **Multi-brand mashup**: awesome-design-md (multiple) → color-expert (harmonize palettes)
- **Want UI from URL of competitor**: awwwards → design-an-interface → design-html

### Example Trace

> User: "I love Deadstock Coffee's site. Build a similar vibe for our coffee subscription."

Orchestrator routes:
1. awwwards-design-intelligence (Deadstock: Streetwear/Hype Drop, dark + orange accent)
2. design-an-interface (3 different subscription-site shapes in parallel)
3. ui-ux-pro-max-skill (industry: subscription/D2C, not streetwear — adjust genre to subscription)
4. design-tokens (compile)
5. hallmark audit (ensure NOT literal streetwear clone — subscription context needs different cadence)
6. design-html (final)

---

## Pipeline Hygiene Rules

1. **Always end with anti-slop gate** — `hallmark audit` is non-negotiable for Steps 7/8
2. **Don't run all steps blindly** — if user asks only for design, skip handoff
3. **Tokens before HTML** — design-tokens should compile before design-html integrates them
4. **20-step limit hard** — if your chain exceeds ~10 skills, you're over-composing
5. **Fallback to single skill** — if a brief is genuinely one-shot (e.g. "what color is this?"), just invoke `color-expert` directly

## Cross-Pipeline Checkpoints

After every 3 steps, the orchestrator should **pause and ask the user** if continuing in the same direction still matches intent. This prevents 6-step pipelines going off-rails.
