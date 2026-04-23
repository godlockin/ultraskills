---
name: ui-ux-pro-max-skill
description: AI design intelligence for building professional UI/UX. Generates complete tailored design systems (pattern + style + colors + typography + effects + anti-patterns + checklist) from a project brief. 161 industry reasoning rules, 67 UI styles, 161 color palettes, 24 landing page patterns, 57 typography pairings. Trigger on design, UI, UX, landing page, color palette, typography, design system requests.
github_url: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
github_hash: b7e3af80f6e331f6fb456667b82b12cade7c9d35
version: 2.0.0
created_at: 2026-04-22
entry_point: scripts/wrapper.py
dependencies: ["python>=3.x", "uipro-cli (npm, optional)"]
homepage: https://uupm.cc
tags: [design, ui, ux, design-system, color-palette, typography, landing-page]
---

# UI UX Pro Max

AI-powered design intelligence skill that produces a complete, tailored design system for any product brief — pattern, style, colors, typography, effects, anti-patterns to avoid, and a pre-delivery checklist.

Source: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill (commit `b7e3af8`).

## When to use

Trigger this skill when the user:
- Asks to design or generate a UI/landing page for a product, brand, or industry
- Needs a color palette, typography pairing, or component style recommendation
- Wants industry-specific design rules (SaaS, fintech, healthcare, e-commerce, beauty/spa, gaming, etc.)
- Needs an anti-pattern / accessibility / pre-delivery checklist before shipping a UI

## What it produces

For a given product brief (e.g. *"landing page for a beauty spa"*), returns:

1. **Pattern** — landing page structure (Hero-Centric, Long-form, Storytelling, etc.)
2. **Style** — UI style with keywords, best-fit categories, perf/a11y rating
3. **Colors** — primary / secondary / CTA / background / text with mood notes
4. **Typography** — Google Fonts pairing with mood + use cases
5. **Effects** — shadows, transitions, hover states, motion guidelines
6. **Anti-patterns** — what to avoid for the specific industry
7. **Pre-delivery checklist** — accessibility, responsive breakpoints, focus states, reduced-motion

## Architecture (from upstream)

```
USER REQUEST
    │
    ▼
MULTI-DOMAIN SEARCH (5 parallel searches: product, style, colors, pattern, typography)
    │
    ▼
REASONING ENGINE (BM25 ranking, JSON decision rules, anti-pattern filtering)
    │
    ▼
COMPLETE DESIGN SYSTEM OUTPUT
```

- **161 industry rules** across Tech/SaaS, Finance, Healthcare, E-commerce, Services, Creative, Lifestyle, Emerging Tech
- **67 UI styles** (Soft UI Evolution, Brutalism, Glassmorphism, Neumorphism, …)
- **161 color palettes** with industry mood mapping
- **24 landing page patterns**
- **57 typography pairings** (Google Fonts share links included)

## Usage

The upstream tool ships as both a Python skill and an optional npm CLI (`uipro-cli`).

**Option A — call the upstream CLI:**
```bash
npx uipro-cli design "landing page for a beauty spa"
```

**Option B — use this skill's wrapper (clones upstream on demand):**
```bash
python scripts/wrapper.py "landing page for a beauty spa"
```

The wrapper lazily clones the upstream repo into `~/.cache/ui-ux-pro-max/` on first use and invokes its design-system generator.

## Pre-delivery checklist (always apply)

- [ ] No emojis as icons — use SVG (Heroicons / Lucide)
- [ ] `cursor-pointer` on all clickable elements
- [ ] Hover states with smooth transitions (150–300 ms)
- [ ] Light-mode text contrast ≥ 4.5:1
- [ ] Visible focus states for keyboard navigation
- [ ] `prefers-reduced-motion` respected
- [ ] Responsive: 375 / 768 / 1024 / 1440 px

## Update policy

`github_hash` is pinned. To refresh, re-run `github-to-skills` against the upstream URL and bump `github_hash` + `version`.

## License

MIT (per upstream). Verify on the upstream repo before commercial use.
