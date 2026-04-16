---
name: awesome-design-md
description: Fetch and apply brand DESIGN.md files for pixel-perfect AI-assisted UI. Triggers when user asks to "make it look like [brand]", "use [brand] design style", "add DESIGN.md", or "apply [brand] theme". Supports 68 brands including Stripe, Vercel, Linear, Apple, Figma, Supabase, Notion, and more.
version: 1.0.0
tags: [design, ui, branding, frontend, css, theming]
github_url: https://github.com/VoltAgent/awesome-design-md
github_hash: 12c50a413f1aad774ed23770dcdbeb13aaf702be
created_at: 2026-04-16
entry_point: npx getdesign@latest add <brand>
dependencies: []
---

# awesome-design-md

Curated collection of DESIGN.md files — detailed plain-text design system specs for 68 developer-focused brands. Drop one into any project, tell your AI agent "build a page that looks like this", and get pixel-perfect UI matching the brand's actual design patterns.

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

This is NOT a design system library. It's a **design intelligence file** — human-readable spec that AI agents can follow to produce authentic brand-matched UI.

## Install a Brand's DESIGN.md

```bash
# Fetch and drop DESIGN.md into current project
npx getdesign@latest add stripe
npx getdesign@latest add vercel
npx getdesign@latest add linear
```

This creates a `DESIGN.md` file in your current directory.

Then tell the AI: **"Build a landing page following DESIGN.md"**

## Available Brands (68 total)

### AI / LLM Tools
| Brand | Command |
|-------|---------|
| Claude (Anthropic) | `npx getdesign@latest add claude` |
| Cohere | `npx getdesign@latest add cohere` |
| Mistral | `npx getdesign@latest add mistral.ai` |
| MiniMax | `npx getdesign@latest add minimax` |
| Ollama | `npx getdesign@latest add ollama` |
| Replicate | `npx getdesign@latest add replicate` |
| RunwayML | `npx getdesign@latest add runwayml` |
| Together.ai | `npx getdesign@latest add together.ai` |
| x.ai (Grok) | `npx getdesign@latest add x.ai` |
| ElevenLabs | `npx getdesign@latest add elevenlabs` |

### Developer Tools
| Brand | Command |
|-------|---------|
| Vercel | `npx getdesign@latest add vercel` |
| Linear | `npx getdesign@latest add linear.app` |
| Figma | `npx getdesign@latest add figma` |
| Cursor | `npx getdesign@latest add cursor` |
| Raycast | `npx getdesign@latest add raycast` |
| Warp | `npx getdesign@latest add warp` |
| Posthog | `npx getdesign@latest add posthog` |
| Sentry | `npx getdesign@latest add sentry` |
| Framer | `npx getdesign@latest add framer` |
| Webflow | `npx getdesign@latest add webflow` |
| Mintlify | `npx getdesign@latest add mintlify` |
| Expo | `npx getdesign@latest add expo` |
| Sanity | `npx getdesign@latest add sanity` |
| MongoDB | `npx getdesign@latest add mongodb` |
| Hashicorp | `npx getdesign@latest add hashicorp` |
| ClickHouse | `npx getdesign@latest add clickhouse` |
| Composio | `npx getdesign@latest add composio` |
| Opencode.ai | `npx getdesign@latest add opencode.ai` |
| VoltAgent | `npx getdesign@latest add voltagent` |
| IBM | `npx getdesign@latest add ibm` |

### SaaS / Productivity
| Brand | Command |
|-------|---------|
| Notion | `npx getdesign@latest add notion` |
| Airtable | `npx getdesign@latest add airtable` |
| Miro | `npx getdesign@latest add miro` |
| Intercom | `npx getdesign@latest add intercom` |
| Superhuman | `npx getdesign@latest add superhuman` |
| Zapier | `npx getdesign@latest add zapier` |
| Resend | `npx getdesign@latest add resend` |
| Cal.com | `npx getdesign@latest add cal` |
| Semrush | `npx getdesign@latest add semrush` |
| Lovable | `npx getdesign@latest add lovable` |

### Fintech / Crypto
| Brand | Command |
|-------|---------|
| Stripe | `npx getdesign@latest add stripe` |
| Coinbase | `npx getdesign@latest add coinbase` |
| Kraken | `npx getdesign@latest add kraken` |
| Revolut | `npx getdesign@latest add revolut` |
| Wise | `npx getdesign@latest add wise` |

### Consumer / Social
| Brand | Command |
|-------|---------|
| Spotify | `npx getdesign@latest add spotify` |
| Airbnb | `npx getdesign@latest add airbnb` |
| Pinterest | `npx getdesign@latest add pinterest` |
| Uber | `npx getdesign@latest add uber` |
| Supabase | `npx getdesign@latest add supabase` |
| Clay | `npx getdesign@latest add clay` |

### Automotive / Luxury
| Brand | Command |
|-------|---------|
| Tesla | `npx getdesign@latest add tesla` |
| BMW | `npx getdesign@latest add bmw` |
| Ferrari | `npx getdesign@latest add ferrari` |
| Lamborghini | `npx getdesign@latest add lamborghini` |
| Renault | `npx getdesign@latest add renault` |
| SpaceX | `npx getdesign@latest add spacex` |

## Workflow

### Step 1: Fetch the DESIGN.md
```bash
# Run in project root
npx getdesign@latest add stripe
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
- License: MIT
