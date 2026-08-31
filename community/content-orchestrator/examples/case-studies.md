# Content Orchestrator — 案例研究 (4 路径)

---

## 案例 C1: Doc — "Write Blog Post on Multi-Agent Architecture"

**用户输入**: "Write a 3000-word blog post on multi-agent orchestration patterns. Optimize for AI search."

### Orchestrator 决策表

**format**: long-doc → Path C1
**deliverable**: blog post + publish HTML + AI SEO optimized
**entry**: doc-coauthoring

### 编排执行

| Step | Skill | 输出 |
|------|-------|------|
| 1 | doc-coauthoring | outline → draft |
| 2 | markdown-mermaid-writing | + 6 Mermaid diagram |
| 3 | baoyu-markdown-to-html | 主题化 HTML (WeChat-ready) |
| 4 | (skip) | — |
| 5 | document-release (optional) | doc update note |
| 6 | ai-seo (gate) | GEO 优化: 引用 LLMs |

### 关键决策

- Step 2 在编码 section 加 sequenceDiagram
- Step 6 关键 query: "multi-agent orchestration" → 优化答案结构

### 耗时

- Manual: 6-8 hours
- Orchestrator: 45 minutes
- **compression**: ~10x

---

## 案例 C2: Visual Deck — "Conference Talk Slides + Visual Identity"

**用户输入**: "Build 15-slide talk deck for QCon. Need motion graphics intro."

### 编排执行

| Step | Skill | 输出 |
|------|-------|------|
| 1 | deck-that-wins | 15-slide skeleton |
| 2 | baoyu-article-illustrator | 4 illustrations |
| 3 | baoyu-diagram | 2 architecture diagrams |
| 4 | baoyu-markdown-to-html | Speaker notes HTML |
| 5 | zero-debt-lint | quality gate (3 typos found) |
| 6 | awesome-design-md | brand discipline |

### 关键决策

- Step 1 deck-that-wins "iron rules" 强制 narrative hook
- Step 5 lint 抓 "powerful" / "leverage" 等 AI slop 词
- Step 6 套 conference brand (可选)

### 耗时

- Manual: 12 hours
- Orchestrator: 1.5 hours
- **compression**: ~8x

---

## 案例 C3: Video — "Faceless YouTube Explainer on RAG"

**用户输入**: "5-min faceless explainer on RAG. For YouTube Shorts + long-form."

### 编排执行

| Step | Skill | 输出 |
|------|-------|------|
| 1 | faceless-explainer | Source footage |
| 2 | motion-graphics | Intro animation |
| 3 | hyperframes-cli | frame catalog |
| 4 | embedded-captions | Subtitles (36 catalog templates) |
| 5 | remotion | React-rendered polish |
| 6 | youtube-script-optimizer | hook / pacing / CTA gate |

### 关键决策

- Step 4 captions: 14pt + Helvetica bold 高对比
- Step 6 关键: 0-3s hook 在"YouTube 80% retention" 测试
- Step 5 polish 切 2 个 short-form clips (60s each)

### Cross-Cluster Bridge

- Step 6 之后 distribute via C4 (baoyu-post-to-wechat 推送 + 简版)

### 耗时

- Manual: 16 hours
- Orchestrator: 2.5 hours
- **compression**: ~6x

---

## 案例 C4: Social Campaign — "SaaS Launch Across 4 Platforms"

**用户输入**: "Launch our SaaS in 4 markets (US / EU / CN / JP) with localized posts."

### 编排执行

| Step | Skill | 输出 |
|------|-------|------|
| 1 | baoyu-format-markdown | Front matter 标准化 |
| 2 | ai-seo (gate) | AI 搜索可见性 (US/EU) |
| 3 | programmatic-seo (if scale) | 模板化变体 |
| 4 | baoyu-translate | 4 语言本地化 |
| 5 | baoyu-post-to-wechat (CN) | 公众号推送 |
|    | xhs-publish (CN 小红书) | 同步 |
|    | baoyu-danger-x-to-markdown (X) | tweet thread |
|    | (LinkedIn via baoyu-format-markdown) | profile post |
| 6 | schema-markup | 网站结构化数据 |

### 关键决策

- Step 4 3-mode translation: `quick` (US/EU 英文) / `dual` (CN 双语) / `formal` (JP 敬体)
- Step 5 平台 protocol 差异: WeChat API vs xhs-publish CDP vs X manual
- Step 6 schema.org/SoftwareApplication 类型

### Cross-Cluster Bridge

- 公司上市逻辑: defer `business-orchestrator` Path B3 (pitch deck 配套)
- 媒体投放/预算分配: defer `marketing-roi-calculator` + `ab-test-setup`
  (无 marketing-orchestrator — 营销类为独立 skill,直接调用)
- 纯营销文案(无预算/无投放): 留在本 cluster C1/C4,不外转

### 耗时

- Manual: 4 hours 平台 × 4 = 16 hours
- Orchestrator: 30 minutes
- **compression**: ~30x (multilingual 收益最大)

---

## 4 案例 meta-pattern

1. **Format first** — 4 个 format, 4 个 path
2. **Always end with gating** — ai-seo / zero-debt-lint / schema-markup / seo-audit
3. **Translation is insertion** — baoyu-translate 总在 step 4, 不在 final
4. **CN ecosystem has dedicated path** — social-media-cn cluster 是 parallel universe
5. **Cross-cluster bridge** — content 跟 design/business 经常需要联动
