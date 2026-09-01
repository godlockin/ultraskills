---
name: awesome-design-md
description: Fetch and apply brand-inspired DESIGN.md files for AI-assisted UI scaffolding. Triggers when user asks to "make it look like [brand]", "use [brand] design style", "add DESIGN.md", or "apply [brand] theme". Supports 57 brands including Stripe, Vercel, Linear, Figma, Supabase, Notion, and more. Each entry is a community-curated spec inspired by publicly observable design patterns; not an official brand asset.
version: 1.1.0
tags: [design, ui, branding, frontend, css, theming, design-system, community, arena-winner]
github_url: https://github.com/VoltAgent/awesome-design-md
github_hash: 12c50a413f1aad774ed23770dcdbeb13aaf702be
created_at: 2026-04-16
entry_point: npx -y getdesign@0.1.0 add <brand>
dependencies: []
license: MIT (covers code only; brand-inspired design specs are unofficial)
---

# awesome-design-md

> ⚠️ **Trademark & Brand Asset Notice**
> Brand names (Stripe, Vercel, Linear, Apple, etc.) are trademarks of their respective owners. The DESIGN.md files in this collection are **community-curated specifications inspired by publicly observable design patterns**. They are **not** official brand assets, do not represent any affiliation with or endorsement by the brands, and must not be used to misrepresent association with the brand owner.
> Use them as **design intelligence for prototyping and learning**. For commercial production, consult each brand's official design system, brand guidelines, or licensed assets.

Curated collection of brand-inspired DESIGN.md files — detailed plain-text design specs for **57** developer-focused brands. Drop one into any project, tell your AI agent "build a page following this spec", and produce UI that resembles the brand's publicly observable patterns.

## When to Use

Trigger this skill when the user says any of:
- "make it look like Stripe / Vercel / Linear / [brand]"
- "use [brand] design style"
- "add DESIGN.md for [brand]"
- "apply [brand] theme to this project"
- "I want the UI to feel like [brand]"
- "what design brands are available?"
- "list available DESIGN.md"

## How It Works

Each DESIGN.md contains:
- **Visual Theme & Atmosphere** — brand personality, design philosophy
- **Color Palette** — exact hex codes with semantic roles (primary, background, text, accent, etc.)
- **Typography** — font families, weights, sizes, line heights, letter spacing
- **Spacing & Layout** — grid systems, breakpoints, padding conventions
- **Components** — button styles, card patterns, form inputs, badges
- **Motion & Animation** — transition curves, durations, interaction patterns
- **Code Examples** — real CSS variables and component snippets

This is NOT a design system library. It's a **design intelligence file** — a human-readable spec that AI agents can follow to produce UI that resembles a brand's publicly observable design language. It is **not an official brand asset**.

### Reproducibility & Staleness

- The skill depends on the `getdesign` npm package and the upstream GitHub repo. If those are unavailable, the fetch command will fail.
- `github_hash` documents the upstream commit this skill was tested against; it may go stale. When in doubt, run the fetch and review `DESIGN.md` before relying on it.
- Offline / sandboxed environments: copy any previously fetched `DESIGN.md` from version control as a fallback.

## Install a Brand's DESIGN.md

```bash
# Fetch and drop DESIGN.md into current project
npx -y getdesign@0.1.0 add stripe
npx -y getdesign@0.1.0 add vercel
npx -y getdesign@0.1.0 add linear
```

This creates a `DESIGN.md` file in your current directory.

Then tell the AI: **"Build a landing page following DESIGN.md"**

## Available Brands (57 total)

### AI / LLM Tools
| Brand | Command |
|-------|---------|
| Claude (Anthropic) | `npx -y getdesign@0.1.0 add claude` |
| Cohere | `npx -y getdesign@0.1.0 add cohere` |
| Mistral | `npx -y getdesign@0.1.0 add mistral.ai` |
| MiniMax | `npx -y getdesign@0.1.0 add minimax` |
| Ollama | `npx -y getdesign@0.1.0 add ollama` |
| Replicate | `npx -y getdesign@0.1.0 add replicate` |
| RunwayML | `npx -y getdesign@0.1.0 add runwayml` |
| Together.ai | `npx -y getdesign@0.1.0 add together.ai` |
| x.ai (Grok) | `npx -y getdesign@0.1.0 add x.ai` |
| ElevenLabs | `npx -y getdesign@0.1.0 add elevenlabs` |

### Developer Tools
| Brand | Command |
|-------|---------|
| Vercel | `npx -y getdesign@0.1.0 add vercel` |
| Linear | `npx -y getdesign@0.1.0 add linear.app` |
| Figma | `npx -y getdesign@0.1.0 add figma` |
| Cursor | `npx -y getdesign@0.1.0 add cursor` |
| Raycast | `npx -y getdesign@0.1.0 add raycast` |
| Warp | `npx -y getdesign@0.1.0 add warp` |
| Posthog | `npx -y getdesign@0.1.0 add posthog` |
| Sentry | `npx -y getdesign@0.1.0 add sentry` |
| Framer | `npx -y getdesign@0.1.0 add framer` |
| Webflow | `npx -y getdesign@0.1.0 add webflow` |
| Mintlify | `npx -y getdesign@0.1.0 add mintlify` |
| Expo | `npx -y getdesign@0.1.0 add expo` |
| Sanity | `npx -y getdesign@0.1.0 add sanity` |
| MongoDB | `npx -y getdesign@0.1.0 add mongodb` |
| Hashicorp | `npx -y getdesign@0.1.0 add hashicorp` |
| ClickHouse | `npx -y getdesign@0.1.0 add clickhouse` |
| Composio | `npx -y getdesign@0.1.0 add composio` |
| Opencode.ai | `npx -y getdesign@0.1.0 add opencode.ai` |
| VoltAgent | `npx -y getdesign@0.1.0 add voltagent` |
| IBM | `npx -y getdesign@0.1.0 add ibm` |

### SaaS / Productivity
| Brand | Command |
|-------|---------|
| Notion | `npx -y getdesign@0.1.0 add notion` |
| Airtable | `npx -y getdesign@0.1.0 add airtable` |
| Miro | `npx -y getdesign@0.1.0 add miro` |
| Intercom | `npx -y getdesign@0.1.0 add intercom` |
| Superhuman | `npx -y getdesign@0.1.0 add superhuman` |
| Zapier | `npx -y getdesign@0.1.0 add zapier` |
| Resend | `npx -y getdesign@0.1.0 add resend` |
| Cal.com | `npx -y getdesign@0.1.0 add cal` |
| Semrush | `npx -y getdesign@0.1.0 add semrush` |
| Lovable | `npx -y getdesign@0.1.0 add lovable` |

### Fintech / Crypto
| Brand | Command |
|-------|---------|
| Stripe | `npx -y getdesign@0.1.0 add stripe` |
| Coinbase | `npx -y getdesign@0.1.0 add coinbase` |
| Kraken | `npx -y getdesign@0.1.0 add kraken` |
| Revolut | `npx -y getdesign@0.1.0 add revolut` |
| Wise | `npx -y getdesign@0.1.0 add wise` |

### Consumer / Social
| Brand | Command |
|-------|---------|
| Spotify | `npx -y getdesign@0.1.0 add spotify` |
| Airbnb | `npx -y getdesign@0.1.0 add airbnb` |
| Pinterest | `npx -y getdesign@0.1.0 add pinterest` |
| Uber | `npx -y getdesign@0.1.0 add uber` |
| Supabase | `npx -y getdesign@0.1.0 add supabase` |
| Clay | `npx -y getdesign@0.1.0 add clay` |

### Automotive / Luxury
| Brand | Command |
|-------|---------|
| Tesla | `npx -y getdesign@0.1.0 add tesla` |
| BMW | `npx -y getdesign@0.1.0 add bmw` |
| Ferrari | `npx -y getdesign@0.1.0 add ferrari` |
| Lamborghini | `npx -y getdesign@0.1.0 add lamborghini` |
| Renault | `npx -y getdesign@0.1.0 add renault` |
| SpaceX | `npx -y getdesign@0.1.0 add spacex` |

## Workflow

### Step 1: Fetch the DESIGN.md
```bash
# Run in project root
npx -y getdesign@0.1.0 add stripe
# → Creates DESIGN.md in current directory
```

### Step 2: Reference in your prompt
After fetching, tell the AI agent:
- "Build a pricing page following DESIGN.md"
- "Create a dashboard component. Use the design system in DESIGN.md"
- "Style this React component to match DESIGN.md"

### Step 3: The AI reads DESIGN.md and applies
The agent will use color tokens, typography specs, spacing rules, and component patterns exactly as defined.

## Tips

- **Multiple brands**: Fetch → review → delete → fetch another to compare
- **Brand fusion**: Copy sections from two DESIGN.md files (e.g., Stripe colors + Linear typography)
- **Version control**: Commit DESIGN.md to share design context with the whole team
- **AI context**: Add DESIGN.md to your `.claude/context/` for persistent access in Claude Code

## Source

- Repo: https://github.com/VoltAgent/awesome-design-md
- Tool: https://getdesign.md
- License: MIT (covers code only; brand-inspired design specs are unofficial and remain the property of their respective brand owners)
