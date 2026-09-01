---
brand: stripe
type: example
license: MIT (example only)
---

# Example: Build a Stripe-inspired Landing Page

> ⚠️ **Fan-made example.** The values below are community-curated interpretations inspired by publicly observable Stripe web design. They are not Stripe's official design system. For production work, consult Stripe's licensed assets or build your own original design.

## Setup

```bash
npx -y getdesign@0.1.0 add stripe
```

## Prompt to AI

```
Build a hero section for a SaaS landing page, inspired by Stripe's publicly observable design language.

Requirements (use only as inspiration, not as official values):
- Dark navy heading (not pure black)
- Purple CTA button
- Multi-layer blue-tinted shadow on the card
- sohne-var equivalent OR system font fallback with matching weight / tracking
- Light gray background with subtle gradient
```

## What You Get

The AI produces UI inspired by Stripe's publicly observable design language, for example:
- `#533afd`-style purple for CTAs
- `#061b31`-style deep navy for headings (not plain black)
- Weight 300 headlines with negative letter-spacing
- `rgba(50,50,93,0.25)`-style blue-tinted shadows
- 4–8px border radius (no pill shapes)

> These values are community observations; verify before using in production.

## CSS Variables Example (community observation)

```css
/* Values inspired by community observations; verify against your own design intent. */
--accent: #533afd;          /* purple CTA */
--heading: #061b31;         /* deep navy */
--shadow-blue: rgba(50,50,93,0.25);
--radius: 6px;
--bg-subtle: #f6f9fc;
```
