# Visual Forge

Professional presentation and web design system for Claude Code agents.

## Quick Start

```bash
# From Claude Code, invoke the skill:
/visual-forge

# Or trigger naturally:
"做一个关于 AI 产品的 PPT"
"create a landing page for our SaaS"
"design an infographic about user growth"
```

## What's Inside

- **SKILL.md** — Complete workflow (4 phases: understand → recommend → plan → generate)
- **references/**
  - `brand-systems.md` — 68+ brand design systems (Vercel, Apple, Stripe, Notion...)
  - `visual-styles.md` — 30+ visual styles (Corporate, Tech, Creative, Classic, Scandinavian, Data, Art)
  - `infographic-layouts.md` — 21 layout types (Timeline, Comparison, Hierarchy, Flow, Data Story...)
- **templates/**
  - `narrative-arcs/pitch-deck.md` — Fundraising deck template (WDC 2026 APAC winning rules)
  - `html-components/` — Reusable HTML/CSS components
- **examples/** — Sample outputs

## Core Features

### 1. Brand Precision
68+ design systems with exact color palettes, typography, spacing, and components.

Example: Vercel style
```css
:root {
  --color-black: #000000;
  --color-white: #FFFFFF;
  --color-blue: #0070F3;
  --font-heading: "Inter", sans-serif;
  --space-md: 24px;
}
```

### 2. Narrative Structure
Competition-grade PPT framework (WDC 2026 APAC winning rules):

```
Hook (1) → Context (1-2) → Core (3-5) → Shift (1) → Takeaway (1-2)
```

Key rules:
- ✅ Memorable language: "India is building. China is freezing." > "Market validated in 3 regions"
- ✅ Zero sensory debt: 0 typos, 0 absolute paths, 0 placeholders
- ❌ Self-talk ≤ 1 page (team/methodology/thanks combined)

### 3. Visual Styles
30+ design directions across 7 categories:

- Corporate Professional (Corporate Clean, Minimalist Pro, Swiss Style)
- Tech Modern (Brutalist Tech, Glassmorphism, Neumorphism)
- Creative Vibrant (Playful Bold, Gradient Pop, Neon Vibes)
- Classic Timeless (Serif Elegance, Art Deco, Mid-Century Modern)
- Scandinavian Minimal (Scandinavian Minimal, Lagom Aesthetic, IKEA Democratic Design)
- Data-Driven (Data Visualization, Infographic Dense, Magazine Editorial)
- Visual Art (Brutalist Joy, Chromatic Silence, Metabolist Dreams)

### 4. Smart Recommendations
Auto-match best combinations based on:

| Input Dimensions | Output |
|-----------------|--------|
| Content type: PPT / Landing Page / Infographic | → Layout types |
| Audience: Professionals / Executives / Beginners / Investors | → Complexity level |
| Tone: Professional / Friendly / Innovative / Trustworthy / Bold | → Visual style |
| Brand reference (optional): Vercel / Apple / Stripe / Notion / None | → Exact specifications |

## Workflow

### Phase 1: Understand
Collect 4 key dimensions via `AskUserQuestion`:
1. Content type
2. Target audience  
3. Emotional tone
4. Brand reference (optional)

### Phase 2: Recommend
Suggest 3 design directions (brand + style combinations) with:
- Color palette
- Typography pairing
- Visual characteristics
- AI prompt template

### Phase 3: Plan
Generate structure based on content type:

- **PPT**: Narrative arc (Hook → Context → Core → Shift → Takeaway) + slide count planning
- **Landing Page**: Hero + 3-5 sections + CTA
- **Infographic**: Layout selection from 21 types

Output: `outline.md` / `wireframe.md` / `layout-spec.md`

### Phase 4: Generate
Technical path selection:

| Output Format | Path | Tools |
|--------------|------|-------|
| HTML webpage | Direct HTML + CSS | Template engine |
| PPT (editable) | HTML → PPTX | html2pptx converter |
| PDF (print) | HTML → PDF | Playwright screenshot |
| PNG (share) | HTML → PNG | Playwright per-slide |

Code quality requirements:
- ✅ Semantic HTML5
- ✅ CSS variables (theme switchable)
- ✅ Responsive design
- ❌ No inline styles
- ❌ No placeholders (Lorem ipsum)
- ❌ No absolute paths

## Examples

### Example 1: Fundraising Deck

**Input**:
- Type: PPT
- Audience: Investors
- Tone: Professional + Innovative
- Brand: Stripe style

**Output**:
- Narrative: 11 slides (Hook → Problem → Solution → Product → Traction → Business Model → Market → Team → Roadmap → Financials → Ask)
- Style: Stripe Gradient Data (Purple #635BFF + gradients + data visualization)
- File: `pitch-deck/index.html` (convertible to PPTX)

### Example 2: SaaS Landing Page

**Input**:
- Type: Landing Page
- Audience: Developers
- Tone: Minimalist + Fast
- Brand: Vercel style

**Output**:
- Structure: Hero + Problem + Solution + Proof + CTA
- Style: Vercel Minimal (Black/White + Blue accent + Inter font)
- File: `landing/index.html` (deployable)

### Example 3: Growth Infographic

**Input**:
- Type: Infographic
- Audience: Executives
- Tone: Data-driven
- Brand: None

**Output**:
- Layout: Data Story (chart-dominant + key numbers highlighted)
- Style: Data Visualization (multi-color semantic categories + neutral base)
- File: `infographic.png` (social media ready)

## Advanced Features

### Reference Image Modes
If user provides reference images (`--ref <files...>`):

| Mode | Effect |
|------|--------|
| `direct` | Pass file to AI generation tool as style reference |
| `style` | Extract style traits (line treatment, texture, mood) → append to prompt |
| `palette` | Extract hex colors → override theme palette |

### Multi-Language Support
Auto-detect user language (Chinese/English/Japanese...) and adapt:
- Response language
- File names
- Prompt templates

### Extensibility
Add new:
- Brand systems: `references/brand-systems/new-brand.md` (YAML format)
- Visual styles: Update `references/visual-styles.md`
- Infographic layouts: Update `references/infographic-layouts.md`

## FAQ

**Q: vs awesome-design-md / magazine-web-ppt / baoyu-slide-deck?**

A: **Visual Forge** integrates best practices from 8 predecessor skills:
- `awesome-design-md` → Brand precision (68 systems)
- `deck-that-wins` → Competition narrative framework
- `magazine-web-ppt` → Theme color system
- `baoyu-slide-deck` → Audience segmentation + reference modes
- `baoyu-infographic` → Layout matrix (21×21)
- `canvas-design` → Visual philosophy
- `ikea-designer` → Scandinavian aesthetic
- `huashu-design` → Style recommendation logic

**New capabilities**:
- Unified 4-phase workflow (PPT / Landing / Infographic)
- Smart recommendation engine (auto-match combos)
- Tech path selection (HTML/PPTX/PDF/PNG)

**Q: Can I use the generated HTML directly?**

A: Yes, but recommended flow:
1. Generate HTML → Preview in browser
2. Confirm → Adjust CSS variables / components if needed
3. Final confirm → Convert to target format (PPTX/PDF/PNG)

**Q: Support dark mode?**

A: Partial. If selected brand has dark specs (e.g. GitHub Dark), generates corresponding variables:

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-background: var(--color-background-dark);
    --color-text: var(--color-text-dark);
  }
}
```

## Version History

**v1.0.0** (2026-05-08)
- Initial release
- Integrated 8 predecessor skills
- Support PPT / Landing Page / Infographic
- 68+ brand systems, 30+ visual styles
- 4-phase workflow + smart recommendation

## Credits

Built on the shoulders of giants:

- `awesome-design-md` — Brand precision
- `deck-that-wins` — Competition narrative
- `magazine-web-ppt` — Theme system
- `baoyu-slide-deck` — Audience segmentation
- `baoyu-infographic` — Layout matrix
- `canvas-design` — Visual philosophy
- `ikea-designer` — Scandinavian aesthetic
- `huashu-design` — Style recommendation

择其善者而从之，其不善者而改之。

---

**License**: MIT  
**Author**: Extracted and integrated from ultraskills collection  
**Last Updated**: 2026-05-08
