---
name: content-orchestrator
description: "Routes content creation requests to the right skill in the 130-skill content cluster, and composes them into end-to-end pipelines. Four orchestration paths (doc/writing, visual/image/deck, video/audio, social/SEO/distribution) cover ~80% of content requests. Includes routing decision table, cross-reference index to writing/visual/video/social methods, and version-sync mechanism. Trigger on 'write a blog post', 'build a deck', 'make a video', 'post to social media', 'optimize for SEO', or any content brief that does not map to a single skill."
version: 1.0.0
tags: [content, orchestrator, router, writing, document, video, image, social, seo, presentation, deck, community]
---

# Content Orchestrator

> 130 content skills, one entry point. Routes, composes, never duplicates.

## 🎯 Goal

UltraSkills has 130 skills in the `content` root across 9 sub-clusters (`内容·视频` 28, `内容·社交媒体` 21, `内容·文档生成` 19, `内容·图像设计` 17, `内容·写作` 16, `内容·视频制作` 13, `内容·演示设计` 6, `内容·中文社交` 6, `内容·SEO` 4). Users face three problems:

1. **Format confusion** — write? design? video? social? — same message needs different formats
2. **Multi-format pipelines** — campaign = doc + image + video + social posts (4+ skills chained)
3. **Localization duplication** — translating for X-platform vs Y-platform has different conventions

This skill is the **conductor** for the content cluster. It:
- Routes a brief via a 9-row sub-cluster decision table
- Composes 4 end-to-end pipelines (Doc / Visual / Video / Social)
- Cross-references (not duplicates) writing/visual/video/social methods
- Includes version sync mechanism

## 🧠 Core Concepts

### The 4 Orchestration Paths

```
┌────────────────────────────────────────────────────────────────┐
│ C1 · Doc / Writing       (article, doc, book, transcript)      │
│ C2 · Visual / Deck       (image, infographic, presentation)   │
│ C3 · Video / Audio       (faceless, motion, captioned, narr.) │
│ C4 · Social / SEO        (post, campaign, optimize, publish)   │
└────────────────────────────────────────────────────────────────┘
```

### Routing by Sub-Cluster (9 layers)

| Sub-cluster | Count | Path coverage | Example skills |
|-------------|-------|---------------|----------------|
| content-writing | 16 | **C1 (core)** | doc-coauthoring, document-release, support-ticket-triage |
| content-doc | 19 | **C1 + C2** | magazine-web-ppt, baoyu-markdown-to-html, baoyu-slide-deck |
| content-presentation | 6 | **C2 (core)** | deck-that-wins, spreadsheet-formula, to-prd |
| content-video | 28 | **C3 (core)** | remotion, video-content-analyzer, video-analyzer |
| content-image | 17 | **C2 (core)** | baoyu-article-illustrator, baoyu-comic, baoyu-cover-image |
| content-social | 21 | **C4 (core)** | baoyu-format-markdown, baoyu-translate, baoyu-post-to-wechat |
| content-seo | 4 | **C4 (gating)** | ai-seo, programmatic-seo, schema-markup, seo-audit |
| social-media-cn | 6 | **C4 (CN-specialized)** | xhs-publish, xiaohongshu-skills, xhs-content-ops |
| video-production | 13 | **C3 (production)** | faceless-explainer, motion-graphics, embedded-captions |

**Important**: This skill does not generate content itself. It tells the model *which* skill to invoke next, *in what order*, *with what adaptation gates*.

## 🚀 Workflow

### Phase 1 — Routing Decision Table

**Heuristics:**

| Signal | Likely path |
|--------|------------|
| "write blog post" / "book chapter" / "doc" | **C1** |
| "design deck" / "presentation" / "infographic" / "image" | **C2** |
| "make a video" / "faceless" / "YouTube" / "podcast" | **C3** |
| "post to X/小红书/微博" / "social campaign" / "SEO" | **C4** |
| "translate this article" | C1 step (baoyu-translate) |
| "localize for CN market" | C4 CN-specialized (social-media-cn) |

### Phase 2 — Composition (4 Pipelines)

#### 📝 Path C1: Doc / Writing (long-form)

**Trigger**: *"write a blog post"*, *"draft documentation"*, *"coauthor a book chapter"*, *"transcribe meeting"*

```
Step 1: doc-coauthoring           [structured workflow: outline → draft → review]
Step 2: markdown-mermaid-writing  [write + diagrams in markdown]
Step 3: baoyu-markdown-to-html    [publish-ready HTML with theme]
Step 4: support-ticket-triage     [if user wants ticket categorization]
Step 5: document-release          [post-publish doc update]
Step 6: ai-seo or seo-audit (gate)[make it discoverable]
```

#### 🎨 Path C2: Visual / Deck / Image

**Trigger**: *"build a slide deck"*, *"design infographic"*, *"create cover image"*

```
Step 1: deck-that-wins or baoyu-slide-deck [deck skeleton]
Step 2: baoyu-article-illustrator or baoyu-image-cards [visuals]
Step 3: baoyu-cover-image or baoyu-diagram [cover/diagram]
Step 4: baoyu-markdown-to-html (if web) [publish-ready]
Step 5: zero-debt-lint (gating) [quality gate for slides]
Step 6: awesome-design-md (optional) [brand discipline]
```

#### 🎬 Path C3: Video / Audio

**Trigger**: *"make a YouTube video"*, *"faceless explainer"*, *"add captions"*, *"repurpose podcast"*

```
Step 1: faceless-explainer        [if no talking head]
        OR talking-head-recut      [if repurposing existing footage]
Step 2: motion-graphics           [if motion is the message]
Step 3: hyperframes-cli           [manage video frame catalog]
Step 4: embedded-captions         [captioning step]
Step 5: video-analyzer            [if user wants analysis first]
        OR remotion               [if React/Remotion programmatic creation]
Step 6: youtube-script-optimizer  [gating for YouTube]
```

#### 📱 Path C4: Social / SEO / Distribution

**Trigger**: *"post to LinkedIn/X"*, *"share to 小红书"*, *"run a campaign"*, *"optimize for SEO"*

```
Step 1: baoyu-format-markdown     [normalize front matter + structure]
Step 2: ai-seo (gating)           [discoverability check]
Step 3: seo-audit or programmatic-seo [if scale → SEO template]
Step 4: baoyu-translate           [if multilingual]
Step 5: baoyu-post-to-wechat      [if WeChat OA]
        OR xhs-publish            [if 小红书]
        OR baoyu-danger-x-to-markdown [if from X/Twitter]
Step 6: schema-markup             [if web distribution, gating]
```

### Phase 3 — Cross-Reference Index

This skill **never duplicates** content methods. Quick lookup:

| Category | Source |
|----------|--------|
| Long-form doc coauthoring | doc-coauthoring |
| Markdown + Mermaid diagrams | markdown-mermaid-writing |
| Markdown → HTML (WeChat themes) | baoyu-markdown-to-html |
| Slide deck generation | baoyu-slide-deck / deck-that-wins |
| Magazine-style web PPT | magazine-web-ppt |
| Article illustration | baoyu-article-illustrator |
| Knowledge comics | baoyu-comic |
| Cover image generation | baoyu-cover-image |
| Infographic cards | baoyu-image-cards |
| AI image (multi-provider) | baoyu-imagine |
| SVG diagrams (dark theme) | baoyu-diagram |
| Brand discipline | awesome-design-md |
| Deck quality gate | zero-debt-lint |
| Faceless video | faceless-explainer |
| React/Remotion programmatic video | remotion |
| Talking head recut | talking-head-recut |
| Motion graphics | motion-graphics |
| Embedded captions | embedded-captions |
| Video frame extraction | video-frame-extractor |
| Video analysis | video-analyzer |
| YouTube script optimization | youtube-script-optimizer |
| Markdown formatting | baoyu-format-markdown |
| WeChat OA publishing | baoyu-post-to-wechat |
| Translation (multi-mode) | baoyu-translate |
| X/Twitter → markdown | baoyu-danger-x-to-markdown |
| AI SEO | ai-seo |
| Programmatic SEO | programmatic-seo |
| Schema markup | schema-markup |
| SEO audit | seo-audit |
| 小红书 publishing | xhs-publish |
| 小红书 automation | xiaohongshu-skills |

## 💡 Best Practices

### Do

- **Always ask format first** (long-doc / visual / video / social)
- **Always run ai-seo (C4) or zero-debt-lint (C2) as gating**
- **Always include translation step** if multilingual audience (insert before Step 5 in C4)
- **Always pair doc generation (C1) with markdown-to-html** for ready-to-publish
- **Always run deck quality gate** after generating any deck (C2 step 5)
- **Use baoyu-* skills for Chinese content** — they're best-in-class for the CN ecosystem

### Don't

- **Don't run all 130 skills** — chain ≤ 8 steps per pipeline
- **Don't generate slides without zero-debt-lint gating** — typos/lint hurt credibility
- **Don't post to social without ai-seo check** — invisible content is wasted
- **Don't translate via generic skill** — use `baoyu-translate` (3 modes: quick / dual / formal)
- **Don't mix WeChat / X / 小红书 publishing** — each has API/protocol differences

## 🔀 Routing Decision Table (Full 130-row)

```
User says                              → Path / Entry skill
──────────────────────────────────────────────────────────
"write a blog post"                   → C1 (doc-coauthoring)
"draft documentation"                  → C1 (markdown-mermaid)
"coauthor a book"                      → C1 (doc-coauthoring)
"transcribe / summarize notes"         → C1 (doc-coauthoring)
"build slide deck"                     → C2 (deck-that-wins or baoyu-slide-deck)
"create magazine-style web"            → C2 (magazine-web-ppt)
"design infographic"                   → C2 (baoyu-image-cards)
"article with illustrations"           → C2 (baoyu-article-illustrator)
"create cover image"                   → C2 (baoyu-cover-image)
"write knowledge comic"                → C2 (baoyu-comic)
"design system diagram"                → C2 (baoyu-diagram)
"make YouTube video" / "faceless"      → C3 (faceless-explainer)
"repurpose talking head video"         → C3 (talking-head-recut)
"add captions to video"                → C3 (embedded-captions)
"create motion graphic"                → C3 (motion-graphics)
"programmatic React video"             → C3 (remotion)
"post to WeChat OA"                    → C4 (baoyu-post-to-wechat)
"post to 小红书"                       → C4 (xhs-publish)
"post to X / Twitter"                  → C4 (markdown + manual)
"social media campaign"                → C4 (full pipeline)
"AI SEO / cited by LLMs"               → C4 (ai-seo)
"SEO at scale"                         → C4 (programmatic-seo)
"add schema markup"                    → C4 (schema-markup)
"SEO audit"                            → C4 (seo-audit)
"translate"                            → single (baoyu-translate)
"X/Twitter → markdown"                 → single (baoyu-danger-x-to-markdown)
```

## 🔧 Version Sync

```bash
python3 community/content-orchestrator/scripts/version-sync-check.py
```

Same mechanism as the other orchestrators.

**Upstream bumps to watch for:**
- `baoyu-*` series — frequent minor updates as Baoyu maintains them
- `remotion` — major version bumps affect React API
- `magazine-web-ppt` / `baoyu-slide-deck` — template updates
- `ai-seo` — LLM ranking algorithm changes

## 📚 Resources

* [Routing decision table](./references/routing-table.md) — 9 sub-cluster matrix
* [Orchestration patterns](./references/orchestration-patterns.md) — 4 paths
* [Method cross-reference](./references/method-index.md) — DRY methods
* [Case studies](./examples/case-studies.md) — 4 paths real scenarios
* [Version sync script](./scripts/version-sync-check.py)

---

**差异化定位**: 130 个 content skill 解决单点; content-orchestrator 是调度层. 0 内容重复, 100% DRY. 跟 `design-orchestrator` / `business-orchestrator` / `engineering-orchestrator` 同方法论.
