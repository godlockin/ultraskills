# Anti-Slop Index (Cross-Reference, Not Duplication)

This index does NOT duplicate anti-pattern rules. It routes to the right source. **Always read the source before applying any rule.**

## By Category

### 1. Generic Slop (AI Default Outputs)

| Rule | Source | Severity |
|------|--------|----------|
| Italic headers (font-style on heading) | hallmark/slop-test.md gate 38a | Hard fail |
| Purple gradient as primary | hallmark/anti-patterns.md | Hard fail |
| Three-icon feature grid (3 columns icon + text) | hallmark/anti-patterns.md | Hard fail |
| Centered-everything layout | hallmark/anti-patterns.md | Soft fail |
| Uniform border-radius (everywhere same value) | hallmark/anti-patterns.md | Soft fail |
| Gradient button as primary CTA | hallmark/anti-patterns.md | Hard fail |
| Emojis instead of icons | hallmark/anti-patterns.md | Soft fail |
| "Trusted by 50,000+ teams" invented metric | hallmark/anti-patterns.md § Invented metrics | Hard fail |
| "+47% conversion" invented metric | hallmark/slop-test.md gate 46 | Hard fail |
| Re-drawn browser chrome (fake URL pill, traffic dots) | hallmark/anti-patterns.md § Re-drawn UI chrome | Hard fail (gate 47) |

### 2. Mid-Render Token Improvisation

| Rule | Source |
|------|--------|
| No inline OKLCH / hex / rgb() — must use `var(--token)` | hallmark/anti-patterns.md § Mid-render token improvisation (gate 48) |
| No `font-family: "Some Font"` bypassing token block | hallmark/anti-patterns.md |

### 3. Typography

| Rule | Source |
|------|--------|
| Italic survives only in body-copy emphasis | hallmark/anti-patterns.md § Italic headers (gate 38a) |
| Type purity: avoid all-italic display face | hallmark/anti-patterns.md |
| Awwwards typography-pairing formula | awwwards SKILL.md Font Pairing table |

### 4. Color Discipline

| Rule | Source |
|------|--------|
| 70/25/5 ratio (background / secondary / accent) | awwwards SKILL.md Color Psychology |
| Dark mode bias (prefer #0a0a0f to #ffffff base) | awwwards SKILL.md |
| WCAG 2.1 AA: contrast ≥4.5:1 | accessibility-review SKILL.md |
| OKLCH for perceptual uniformity | color-expert SKILL.md (OKLCH section) |

### 5. Layout / Macrostructure

| Rule | Source |
|------|--------|
| Hero → 3-feature → CTA → footer rhythm forbidden (structural variety) | hallmark/SKILL.md Structural variety rule |
| 5 named macrostructures (Bento, Marquee, Long-document, Stat-led, Workbench) | hallmark/macrostructures/ |
| Awwwards 5 pattern categories (Premium Dark / Split-Screen / Editorial / Wellness / Hype) | awwwards SKILL.md |

### 6. State Discipline

| Rule | Source |
|------|--------|
| 8-state component (default / hover / focus / active / disabled / loading / error / success) | hallmark/SKILL.md Component-scope |
| 8-state demo wrapper mandatory | hallmark/SKILL.md § Component-scope emits |

### 7. Mobile Responsiveness

| Rule | Source |
|------|--------|
| Verified at 320 / 375 / 414 / 768 px | hallmark/responsive.md |
| `overflow-x: clip` on html+body, never `hidden` | hallmark/slop-test.md gate 34 |
| Image-bearing grid uses `minmax(0, 1fr)`, never bare `1fr` | hallmark/slop-test.md gate 50 |
| Section heads collapse to one column on mobile | hallmark/slop-test.md gate 52 |

### 8. Accessibility (WCAG 2.1 AA)

| Rule | Source |
|------|--------|
| Color contrast ≥4.5:1 (text), ≥3:1 (UI) | accessibility-review SKILL.md |
| Keyboard navigation all interactive elements | accessibility-review |
| Touch targets ≥44×44 px | accessibility-review |
| `prefers-reduced-motion` honored for any animation | motion-design SKILL.md |
| Screen reader behavior | accessibility-review |

### 9. Brand Compliance (when using `awesome-design-md`)

| Rule | Source |
|------|--------|
| Use exactly the brand's font / spacing / shadow | awesome-design-md / the brand's DESIGN.md |
| Don't bleed brand colors into adjacent gradients | awesome-design-md |

### 10. Industry-Specific (from ui-ux-pro-max)

| Industry | Rule | Source |
|----------|------|--------|
| SaaS / fintech / enterprise | Modern-minimal genre, restraint over flair | ui-ux-pro-max-skill industry rules |
| Beauty / spa / wellness | Warm tones (terracotta, sage, cream) | ui-ux-pro-max-skill industry rules |
| Gaming / esports | Dark + neon accent, dense info | ui-ux-pro-max-skill industry rules |
| Healthcare / medical | Soft + reassuring, white space, no flashing | ui-ux-pro-max-skill industry rules |
| AI / generative / voice | Atmospheric genre, dark + glow | ui-ux-pro-max-skill industry rules |

## How to Apply

1. **Pick the relevant category** based on the brief (e.g. "is this an industry-specific design?" → category 10)
2. **Open the source skill's SKILL.md or referenced file** (do not skip)
3. **Apply the rule as a build constraint, not a post-hoc check** — the gateway is `hallmark audit` at pipeline end
4. **Cross-check** with `awwwards-design-intelligence` for pattern-level anti-patterns and `accessibility-review` for a11y

## Anti-Slop Pass Order (Recommended)

When ending a pipeline, run this order:
1. **awwwards check** — pattern-level (10 minutes)
2. **hallmark audit** — gate-level (5 minutes per file)
3. **accessibility-review** — WCAG (10 minutes)

Total anti-slop overhead: 25 minutes for a typical landing page. Trade-off for avoiding rework.

## Quick Reference Card

```
Slop symptom              → Source skill           → Hard or soft?
─────────────────────────────────────────────────────────────────
Italic header             → hallmark gate 38a      → Hard
Purple gradient           → hallmark anti-pattern  → Hard
3-icon feature grid       → hallmark anti-pattern  → Hard
Border-radius uniform     → hallmark anti-pattern  → Soft
Centered-everything       → hallmark anti-pattern  → Soft
Invented metric           → hallmark gate 46       → Hard
Re-drawn chrome           → hallmark gate 47       → Hard
Mid-render OKLCH inline   → hallmark gate 48       → Hard
Color contrast <4.5:1     → accessibility-review   → Hard (WCAG)
Hero→3feat→CTA→footer     → hallmark structural    → Hard (variety)
No `prefers-reduced-motion` → motion-design        → Hard (a11y)
```
