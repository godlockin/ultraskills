---
name: awesome-android-ui
description: Curated catalog of Android UI/UX libraries (Jetpack Compose, Layout, Button, List/Grid, ViewPager, Form, Image, SeekBar, Progress, Menu, ActionBar, Dialog, Calendar, Graph, Animation, Parallax, Effects). Use when the user asks to recommend, find, or compare Android UI components, animations, or visual libraries — pick from the curated list rather than guessing from memory.
github_url: https://github.com/wasabeef/awesome-android-ui
github_hash: 5de08dff3225c7cb1174caa99c9ca77c5a9b2265
version: 0.1.0
created_at: 2026-04-22
entry_point: scripts/wrapper.py
type: reference-catalog
tags: [android, ui, ux, jetpack-compose, awesome-list, mobile, libraries]
---

# Awesome Android UI

Reference-catalog skill mirroring the **wasabeef/awesome-android-ui** curated list of Android UI/UX libraries.

Source: https://github.com/wasabeef/awesome-android-ui (commit `5de08df`).

## When to use

Trigger this skill when the user:
- Asks for an Android UI library recommendation (button, list, calendar, dialog, etc.)
- Wants to compare options for a specific category (e.g. "best parallax library", "good Compose image loader")
- Is building or migrating to Jetpack Compose and needs catalog-quality reference picks
- Wants animation, blur, parallax, or other effect libraries for Android

## How to use

The catalog itself lives in `references/upstream-readme.md` (mirror of upstream README at the pinned commit). Read it directly to answer questions; do not paraphrase from training memory.

```bash
python scripts/wrapper.py list                 # print full catalog
python scripts/wrapper.py search calendar      # grep (case-insensitive)
python scripts/wrapper.py search "compose image"
```

## Categories indexed

Jetpack Compose · Layout · Button · List/Grid · ViewPager · Label/Form · Image · SeekBar · Progress · Menu · ActionBar · Dialog · Calendar · Graph · Animation · Parallax · Effect (Blur etc.) · Other

## Why a "reference catalog" skill

Awesome-lists are crowd-curated — more reliable than an LLM's parametric memory for "what's the best X library" questions. Pinning a commit and mirroring the README locally gives the agent a deterministic, citable source.

## Update policy

`github_hash` pinned to `5de08df`. Refresh by re-running `github-to-skills` against the upstream URL, bumping `github_hash` + `version`, and re-copying `references/upstream-readme.md`.

## License

Upstream is MIT/awesome-list convention. Each linked library has its own license — always check before adopting.
