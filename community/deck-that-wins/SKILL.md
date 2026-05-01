---
name: deck-that-wins
description: Build competition-ready presentation decks that win — 6 iron rules, 8 pass criteria, 8 bonus items distilled from WDC 2026 APAC postmortem analysis of winners vs losers
version: 1.0.0
tags: [presentation, competition, deck, pitch, storytelling, design]
---

# Competition Deck — Build Decks That Win

## Overview

This skill encodes the hard-won lessons from a real competition (WDC 2026 APAC) where we lost, analyzed every winner, and codified what separates "good content, bad delivery" from "memorable and actionable." The 6 iron rules are non-negotiable; the 8 pass criteria are must-pass gates; the 8 bonus items are what push you from "solid" to "unforgettable."

## When to Use

- Building a competition submission deck (hackathon, case competition, pitch)
- Preparing a high-stakes presentation where judges/VCs compare you against others
- Auditing an existing deck before submission
- Training a team on presentation fundamentals

## The 6 Iron Rules

### L1 — Carrier Wins the Battle, Content Wins the War

What the judge carries out of the room matters more than what you analyzed in it.

| Carrier | Judge Experience | Winner Example |
|---------|-----------------|----------------|
| Self-contained HTML | Double-click, zero dependency | Data Five |
| QR → App | Scan and use | Insights Fund |
| Agent | Login to existing platform | Homy |
| Video | Embed anywhere | Vikings |
| PPT | Must download, paginate, lose | Us (old) |

**Rule:** Day-0 question is not "what do we analyze?" but "what file format is easiest for the judge to open?"

### L2 — Team Personality = 24-Hour Memorability

If the judge can recite one sentence about you the next day, you win. If not, everything was wasted.

| Team | Hook | Memory Mechanism |
|------|------|-----------------|
| Data Five | "五行缺数据" | Cultural pun + team name + mission triple-helix |
| Vikings | "We came for the data, but stayed for the insights" | Quotable line + nautical metaphor throughout |
| Homy | "Yasmine, what should I buy?" | Personified Agent |
| Us (old) | "EKET Plan A" | No story, no metaphor, even misspelled |

**Rule:** Team name = first hook. Must have origin story + cultural/visual metaphor threaded throughout.

### L3 — Market Identity Language > Project Status Language

| Type | Example | Effect |
|------|---------|--------|
| Market identity (winners) | "India is building. China is freezing. Japan monetizes aesthetics." | Judges recite it 24h later |
| Project status (us, old) | "Self-Care PROVEN · Cooking RE-FRAME · Pet SEEDED" | Judges forget on exit |

**Rule:** One verb per market, parallel structure, memorable, quotable. The verb IS the market identity, not the project status.

### L4 — APAC = 5 Homes, Not 1 Country

The judges are APAC HQ, not China lead. 80% content about 1 country = "what does this have to do with my other 4 countries?"

**Rule:** 5-country balance is a hard pass threshold. Each country must have its own insight + action + one-sentence story.

### L5 — Talk About Findings, Not About Yourself

| Content | Winners | Us (old) |
|---------|---------|---------|
| Methodology/pipeline | ≤ 1 page or 0 | Full page P13 |
| Team intro | 0 (one line at bottom) | Full page P14 + placeholder |
| Acknowledgments | 0 | Full page P15 |
| **Self-talk ratio** | **0–5%** | **20%** |

**Rule:** "Talking about ourselves" pages total ≤ 1. Every page's first sentence must be "a finding for the judges," not "a description of our process."

### L6 — Sensory Debt Compounds with Interest

Individually minor; collectively = "this team is unprofessional."

- Cover misspelling "Spakling"
- Team page "TEAM PHOTO PLACEHOLDER"
- Absolute paths `/Users/name/working/...`
- Video exposing Teams UI
- Final frame is PowerPoint edit mode

**Rule:** Must run lint before submission. Spelling, paths, placeholders, audio quality — any single failure = don't submit.

## The 8 Pass Criteria (Must-Pass Gates)

Any single failure = judges instinctively downgrade, no matter how good the content.

| # | Gate | Standard | Verification |
|---|------|----------|-------------|
| G1 | **Carrier = HTML or equivalent** | Judge can open with double-click/scan, zero install | Test on clean machine |
| G2 | **5-country balance** | Each country ≥ 1 page insight + 1 action | Count slides per country |
| G3 | **Zero sensory debt** | 0 spelling errors, 0 absolute paths, 0 placeholders | Run `lint_text.sh` |
| G4 | **Team personality** | Team name has story + ≥ 1 metaphor/visual throughout | Cold-read test: recite after 10 min? |
| G5 | **Self-talk ≤ 1 page** | Team/methodology/acknowledgments combined ≤ 1 | Page audit |
| G6 | **Audio baseline** | WPM 130–150, silence ≤ 8%, LUFS -16 to -23 | `lint_audio.sh` + ffmpeg ebur128 |
| G7 | **Multiple speakers** | ≥ 2 different voices rotating | Audio audit |
| G8 | **Bilingual** | Judge can switch language | URL param / toggle test |

## The 8 Bonus Items (Nice-to-Have)

These push you from "solid" to "unforgettable."

| # | Bonus | Effect | Reference |
|---|-------|--------|-----------|
| B1 | **Market identity quotable** | One sentence holds 5 countries | Data Five |
| B2 | **Cultural pun team name** | Name explains everything, dual-culture resonance | Data Five |
| B3 | **Video format** | Full demo video + multi-voice rotation | Vikings |
| B4 | **Counter-intuitive hook** | One question grabs attention | Vikings |
| B5 | **QR code / direct link** | Judge scans and sees immediately — adoption cost = 0 | Insights Fund |
| B6 | **Hover interaction** | Mouse-over reveals data details — feels like a product | Data Five |
| B7 | **AI voice completeness** | 0% silence, flat waveform — signals completeness | Data Five |
| B8 | **Closing quotable** | "We came for the data, but stayed for the insights" | Vikings |

## Next-Level Upgrade Path

### From Deck to Product

| Stage | Form | Investment | Effect |
|-------|------|-----------|--------|
| Now | HTML slides (static) | Done | ≈ Data Five |
| Next | HTML + hover interaction + data drill-down | 2–3 days | Surpass Data Five |
| End state | Databricks App / Notion / Agent | 1–2 weeks | ≈ Insights Fund / Homy |

### Day-0 Checklist (Every Competition)

```
□ Judge persona workshop (KPI / takeaways / who are they)
□ Team name + origin story + 1 metaphor (within 4 hours)
□ Default carrier is NOT PPT (disprove PPT first, then choose HTML/App/Video)
□ Write pre-mortem: "if we lose, why?"
□ 5-country / 5-dimension symmetric skeleton (before Day-2)
□ External cold read (before Day-4)
□ Lint all pass + audio self-check (before Day-6)
```

## Anti-Patterns

1. **"Our content is strong, the format doesn't matter"** — Wrong. The carrier determines whether judges engage at all.
2. **"Let's add a methodology page to show rigor"** — Winners show 0–5% self-talk. Rigor shows through the findings, not through describing your process.
3. **"We'll polish the slides at the end"** — Sensory debt compounds. Lint continuously, not at the end.
4. **"APAC leadership cares about the China story"** — They care about all 5 countries equally. 80% China = 80% irrelevance to 4 out of 5 judges.
5. **"The team name is just a label"** — It's the first hook. "五行缺数据" told the entire story before slide 1.

## Verification Checklist

Before submission, verify every item:

- [ ] Opens on a clean machine (no dependencies)
- [ ] Each country has ≥ 1 insight page + 1 action
- [ ] `lint_text.sh` passes with 0 errors
- [ ] `lint_audio.sh` passes for all WAV files
- [ ] Team name is memorable and has an origin story
- [ ] First cold reader can recite one line after 10 minutes
- [ ] Self-talk pages ≤ 1
- [ ] ≥ 2 voices in audio track
- [ ] Language toggle works (?lang=en / ?lang=cn)
- [ ] No absolute paths, no placeholders, no misspellings
