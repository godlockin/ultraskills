# Routing Decision Table (22 skills, full matrix)

This is the canonical routing map for the UltraSkills design cluster. Use it whenever the orchestrator skill needs to dispatch to one or more skills.

## Routing by Project State

### Greenfield (no existing code, building from scratch)

| User intent | Entry skill | Pipeline |
|-------------|-------------|----------|
| "Design my SaaS landing" | design-consultation → ui-ux-pro-max-skill → design-tokens → motion-design → icon-system → awwwards-check → hallmark (audit) → design-html | Path 1 |
| "Make me a beauty spa site" | ui-ux-pro-max-skill (industry rules) → design-consultation (DESIGN.md) → design-html | Path 1 lite |
| "Pick colors for my logo" | color-expert | Single |
| "I have a brief, generate 5 designs" | design-shotgun | Single (variants) |
| "Design an API / data model" | design-an-interface | Single (parallel agents) |
| "Build a component" | ui-ux-pro-max-skill → icon-system (if icons needed) → motion-design (if interactive) | Component flow |

### Existing (has live code, audit/redesign)

| User intent | Entry skill | Pipeline |
|-------------|-------------|----------|
| "Audit this site for design" | design-review | Path 2 lite |
| "Audit this site for slop" | hallmark audit | Path 2 lite 2 |
| "Audit this for accessibility" | accessibility-review | Single |
| "Audit this for color/accessibility/design system consistency" | accessibility-review → color-expert → design-system | Triple audit |
| "Redesign my homepage" | plan-design-review (plan first) → design-review (live) → design-shotgun (variants?) → design-html (final) → design-handoff (spec) | Path 2 full |
| "Polish this design — feels AI-generated" | hallmark audit → design-review → design-shotgun (alt) → design-html | Anti-slop flow |

### Inspiration (URL, screenshot, brand)

| User intent | Entry skill | Pipeline |
|-------------|-------------|----------|
| "Make it look like Stripe / Vercel / [brand]" | awesome-design-md (load DESIGN.md) → design-consultation (adapt) → design-html | Brand clone |
| "Extract DNA from [URL]" | awwwards-design-intelligence → design-an-interface → ui-ux-pro-max-skill → design-html | Path 3 URL |
| "Extract DNA from screenshot" | hallmark study → design-an-interface → design-html | Path 3 image |
| "Use [brand]'s design language but with our colors" | awesome-design-md (1st) → color-expert (override) → design-tokens | Brand adaptation |

## Routing by Skill Type (Single-purpose)

| Need | Skill |
|------|-------|
| Anti-slop discipline (4 verbs) | hallmark |
| Brand-clone (68 DESIGN.md) | awesome-design-md |
| Design system from brief | ui-ux-pro-max-skill |
| DTCG tokens → multi-platform | design-tokens |
| Figma → React/Vue | figma-to-code |
| Icons | icon-system |
| Animation/motion | motion-design |
| Color knowledge | color-expert |
| WCAG / accessibility | accessibility-review |
| UX copy/microcopy | ux-copy |
| PRD / spec | write-spec |
| Metrics review | metrics-review |
| Status update | stakeholder-update |
| Design critique (multi-dim feedback) | design-critique |
| Design handoff spec | design-handoff |
| Design system audit | design-system |
| IKEA brand role | "ikea-designer-pro" (only when explicitly asked) |

## Anti-Override Rules

These skills **must not** be invoked unless the user explicitly asks:

- **awesome-design-md** — user names a brand ("Stripe, Vercel") or asks to clone
- **hallmark study** — user attaches URL or image (not for greenfield)
- **ikea-designer-pro** — user asks for IKEA-style role explicitly
- **write-spec** — user asks for PRD/spec (not for visual design)
- **metrics-review** / **stakeholder-update** — product ops, not design

## Skill Conflict Resolution

When two skills could fit, choose by project state:

| Conflict | Greenfield | Existing | Inspiration |
|----------|-----------|----------|-------------|
| ui-ux-pro-max-skill vs design-consultation | design-consultation (1st → understand) | design-consultation (when existing site needs system overhaul) | ui-ux-pro-max-skill |
| awesome-design-md vs ui-ux-pro-max-skill | ui-ux-pro-max-skill | either | awesome-design-md (1st) |
| hallmark audit vs design-review | hallmark audit (slop) | design-review (visual) | both |

## Fallback (When No Skill Fits)

If the user request doesn't match any skill:
1. **AskUserQuestion** to clarify the intent (greenfield / existing / inspiration / single-skill)
2. If user says "I don't know", default to Path 1 (Greenfield) — most common
3. Never invoke all 22 skills — chain waste
