# Example: Build a Stripe-style Landing Page

## Setup

```bash
# In your project root
npx getdesign@latest add stripe
```

## Prompt to AI

```
I need a hero section for a SaaS landing page.
Follow DESIGN.md exactly — colors, typography, shadow system, and spacing.

Requirements:
- Dark navy heading (not black)
- Purple CTA button
- Multi-layer blue-tinted shadow on the card
- sohne-var equivalent (or system font fallback with matching weight/tracking)
- Light gray background with subtle gradient
```

## What You Get

The AI will produce output matching Stripe's actual design system:
- `#533afd` purple for CTAs
- `#061b31` deep navy for headings (not plain black)
- Weight 300 headlines with negative letter-spacing
- `rgba(50,50,93,0.25)` blue-tinted shadows
- 4-8px border radius (no pill shapes)

## CSS Variables Example (from Stripe DESIGN.md)

```css
:root {
  --color-primary: #533afd;
  --color-heading: #061b31;
  --color-body: #64748d;
  --color-background: #ffffff;
  --shadow-card: 0 7px 14px rgba(50,50,93,0.1), 0 3px 6px rgba(0,0,0,0.08);
  --shadow-button: 0 4px 6px rgba(50,50,93,0.11), 0 1px 3px rgba(0,0,0,0.08);
  --font-display-weight: 300;
  --font-display-tracking: -0.04em;
  --radius-sm: 4px;
  --radius-md: 8px;
}
```
