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
| content-presentation | 6 | **C2 (core)** | deck-that-wins, spreadsheet-formula-helper, to-prd |
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

**Fallback — 信号不明确时(必读,不要跳到 Phase 2):**

1. **先问,别猜**:用 AskUserQuestion 问交付物形态 —— 文档 / 幻灯片或图 / 视频 / 社媒帖?
2. 用户说不清或只说"帮我搞内容" → **默认 C1**(文档是最通用的中间产物,后续可派生出 C2/C3/C4)
3. 明确说明你的默认选择与理由,让用户能否决:「我按文档处理,如果你其实要的是视频,现在告我」

**Tiebreak — 多路径同时命中:**

| 情形 | 裁定 |
|---|---|
| 一次要 blog + deck + video + 社媒帖 | **C1 先产出规范源文**,C2/C3 从它派生,C4 最后做分发。不要四条并行 —— 会得到四份不一致的内容 |
| "带图的文章" | C1 主,C2 作为其中一步(不是两条路径) |
| "视频脚本" | C1(脚本是文档);"视频成片" → C3 |
| 交付物形态冲突且用户坚持全都要 | 按上面顺序串行,并告知总步数;超过 8 步则拆成两次会话 |

**跨 cluster 边界 — 什么时候不该留在 content:**

| 请求特征 | 转交给 | 裁定依据 |
|---|---|---|
| 技术文档/API 文档,**代码准确性是主要风险** | `engineering-orchestrator` | 写错 API 签名比文笔差危害大 → 工程主导 |
| 技术博客,**叙事与传播是主要目标** | 留在 C1 | 代码只是例子,重点是讲清概念 |
| 附带财务模型/融资数据的 pitch deck | `business-orchestrator` B3 | 数字正确性优先于版式 |
| 纯营销文案,无预算无投放 | 留在 C1/C4 | 就是写作与分发 |
| 媒体投放、预算分配、A/B 测试 | `marketing-roi-calculator` / `ab-test-setup` | 是计算不是创作(注:无 marketing-orchestrator) |
| 高保真 UI 稿、设计系统 | `design-orchestrator` | 封面图/信息图留在 C2,产品界面转设计 |

完整路由表与更多边界见 [references/routing-table.md](references/routing-table.md)。

### Phase 2 — Composition (4 Pipelines)

#### 📝 Path C1: Doc / Writing (long-form)

**Trigger**: *"write a blog post"*, *"draft documentation"*, *"coauthor a book chapter"*, *"transcribe meeting"*

```
Step 1: doc-coauthoring           [structured workflow: outline → draft → review]
Step 2: markdown-mermaid-writing  [write + diagrams in markdown]
Step 3: baoyu-markdown-to-html    [publish-ready HTML with theme]
Step 4: document-release          [post-publish doc update]
Step 5: ai-seo or seo-audit (gate)[make it discoverable]
```

> `support-ticket-triage` 不在此链中 —— 它是 1-shot 分类器,不是长文写作步骤。
> 需要工单分类时单独调用,见下方 1-shot 表。

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
Step 0: video-analyzer            [仅当基于已有素材:先分析再决定怎么剪]
Step 1: 选内容形态
        faceless-explainer        [无真人出镜]
        OR talking-head-recut     [重用已有出镜素材]
Step 2: 选渲染后端(互斥,不要都用)
        remotion                  [React 程序化生成:数据驱动/批量/需组件复用]
        OR hyperframes-cli        [HTML 优先的一次性合成]
Step 3: motion-graphics           [若动效本身是表达重点]
Step 4: embedded-captions         [字幕]
Step 5: youtube-script-optimizer  [YouTube 发布前的 gating]
```

> **Step 0 是 gate 不是可选项**:基于已有素材时先分析,否则后面的剪辑决策没有依据。
> 从零创作则跳过。
> **Step 2 两个后端互斥** —— 它们是竞争关系,不是先后步骤。选择依据见
> [remotion 的边界说明](../remotion/SKILL.md)。

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
- **Always pair doc generation (C1) with baoyu-markdown-to-html** for ready-to-publish
- **Always run deck quality gate** after generating any deck (C2 step 5)
- **Use baoyu-* skills for Chinese content** — they're best-in-class for the CN ecosystem

### Don't

- **Don't run all 130 skills** — chain ≤ 8 steps per pipeline
- **Don't generate slides without zero-debt-lint gating** — typos/lint hurt credibility
- **Don't post to social without ai-seo check** — invisible content is wasted
- **Don't translate via generic skill** — use `baoyu-translate` (3 modes: quick / dual / formal)
- **Don't mix WeChat / X / 小红书 publishing** — each has API/protocol differences

## 🔀 Routing Decision Table (Top-26 高频信号)

> 这里是**最高频的 26 条信号**,不是全量。content cluster 共 130 个 skill,
> 其余按 Phase 1 的 sub-cluster 表 + [references/routing-table.md](references/routing-table.md) 定位。
> 信号不在下表中 → 走 Phase 1 的 Fallback。


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
"post to X / Twitter"                  → C4 (baoyu-format-markdown → 用户手动发布;无自动发布 skill)
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
