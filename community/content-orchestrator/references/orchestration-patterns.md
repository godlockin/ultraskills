# Orchestration Patterns (4 End-to-End Content Pipelines)

---

## 📝 Pattern C1: Doc / Writing

### When

- Long-form article, blog post, book chapter
- Documentation coauthoring / release notes
- Meeting notes / transcripts

### Steps

| # | Skill | Output |
|---|-------|--------|
| 1 | doc-coauthoring | Outline → draft → review workflow |
| 2 | markdown-mermaid-writing | Markdown + diagrams |
| 3 | baoyu-markdown-to-html | Publish-ready HTML |
| 4 | support-ticket-triage (optional) | If tickets are the input |
| 5 | document-release | Post-publish updates |
| 6 | ai-seo / seo-audit (gate) | Discoverability |

### Adapted Variants

- **Book chapter**: Step 1 only (multiple iterations)
- **Release notes**: Step 5 only
- **Meeting summary**: doc-coauthoring alt = meeting-notes-and-actions

### Timing

- Manual: 4-8 hours
- Orchestrator: 30-45 minutes
- **compression**: ~10x

---

## 🎨 Pattern C2: Visual / Deck / Image

### When

- Slide deck (10-15 slides)
- Infographic / card series
- Article with illustrations
- Cover image

### Steps

| # | Skill | Output |
|---|-------|--------|
| 1 | deck-that-wins or baoyu-slide-deck | Deck skeleton |
| 2 | baoyu-article-illustrator or baoyu-image-cards | Illustrations / cards |
| 3 | baoyu-cover-image or baoyu-diagram | Cover / diagram |
| 4 | baoyu-markdown-to-html | Web HTML (if applicable) |
| 5 | zero-debt-lint | Quality gate |
| 6 | awesome-design-md (optional) | Brand discipline |

### Adapted Variants

- **Pure slide deck**: Steps 1, 5 only
- **Article with illustrations**: Steps 2, 3, 5
- **Magazine-style web PPT**: magazine-web-ppt replaces step 1
- **Knowledge comic**: baoyu-comic replaces step 2

### Cross-Cluster Bridge

For institutional fidelity (investor decks, marketing landing pages), defer to `design-orchestrator`.

### Timing

- Manual: 6-12 hours
- Orchestrator: 45-90 minutes
- **compression**: ~10x

---

## 🎬 Pattern C3: Video / Audio

### When

- YouTube channel (faceless or talking head)
- Social clips / shorts
- Podcast repurposing
- Tutorial with motion graphics

### Steps

| # | Skill | Output |
|---|-------|--------|
| 1 | faceless-explainer OR talking-head-recut | Source footage |
| 2 | motion-graphics (if needed) | Motion intro |
| 3 | hyperframes-cli | Frame catalog mgmt |
| 4 | embedded-captions | Subtitles |
| 5 | video-analyzer OR remotion | Polish / analysis |
| 6 | youtube-script-optimizer (gate) | Script quality |

### Adapted Variants

- **Pure faceless**: Step 1 only (with motion + captions)
- **Repurpose podcast**: Steps 1 (recut) → 4 → 6
- **Programmatic React**: Step 5 = remotion
- **Pre-analysis only**: Step 5 only (video-analyzer)

### Timing

- Manual: 8-16 hours per video
- Orchestrator: 1.5-3 hours
- **compression**: ~5x

---

## 📱 Pattern C4: Social / SEO / Distribution

### When

- LinkedIn / X / WeChat / 小红书 posting
- Multi-platform campaign
- SEO optimization
- Schema markup audit

### Steps

| # | Skill | Output |
|---|-------|--------|
| 1 | baoyu-format-markdown | Front matter + structure |
| 2 | ai-seo (gate) | Discovery check |
| 3 | seo-audit OR programmatic-seo | SEO deep dive (or scale) |
| 4 | baoyu-translate | Multilingual (if needed) |
| 5 | baoyu-post-to-wechat OR xhs-publish OR baoyu-danger-x-to-markdown | Platform publish |
| 6 | schema-markup | Web markup (gating for web) |

### Adapted Variants

- **Single platform**: Steps 1, 5 only
- **Multi-platform campaign**: Steps 1, 2, 4, 5 (× N platforms)
- **SEO-only**: Steps 2, 3, 6
- **Translation only**: Step 4 (single skill)
- **CN-specialized**: Use social-media-cn cluster (xhs-publish, xiaohongshu-skills)

### Cross-Cluster Bridge

For multi-format campaign (article → video → social), chain across C1 → C3 → C4.

### Timing

- Manual: 2-4 hours per platform
- Orchestrator: 15-30 minutes
- **compression**: ~8x

---

## Cross-Pipeline Checkpoints

After every 4 steps, pause and confirm direction with user.

## Pipeline Hygiene

1. **Always end with gating** — `ai-seo` (C4), `zero-debt-lint` (C2), `seo-audit` (C1)
2. **Hard limit ≤ 8 steps** per pipeline
3. **Cross-link** with `design-orchestrator` for UI, `business-orchestrator` for finance
4. **Always tag localization** if target is CN/other language
