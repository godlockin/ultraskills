# Routing Decision Table — Content Cluster (9 sub-clusters, 130 skills)

## Master Mapping

| Cluster | Count | C1 Doc | C2 Visual | C3 Video | C4 Social | 1-shot |
|---------|-------|--------|-----------|----------|-----------|--------|
| content-writing | 16 | ✅ core | — | — | — | ✅ |
| content-doc | 19 | ✅ core | ✅ (doc→deck/HTML) | — | — | ✅ |
| content-presentation | 6 | — | ✅ core | — | — | ✅ |
| content-video | 28 | — | — | ✅ core | — | ✅ |
| content-image | 17 | — | ✅ core | — | — | ✅ |
| content-social | 21 | ✅ | — | — | ✅ core | ✅ |
| content-seo | 4 | — | — | — | ✅ gating | ✅ |
| social-media-cn | 6 | — | — | — | ✅ CN | ✅ |
| video-production | 13 | — | — | ✅ production | — | ✅ |

## Top Skills per Sub-Cluster

| Cluster | Top skill | Route |
|---------|-----------|-------|
| content-writing | doc-coauthoring (8.8) | C1 step 1 |
| content-writing | document-release (8.8) | C1 step 5 |
| content-writing | support-ticket-triage (8.0) | 1-shot |
| content-writing | youtube-script-optimizer (8.0) | C3 step 6 |
| content-doc | magazine-web-ppt (10.0) | C2 |
| content-doc | baoyu-markdown-to-html (9.5) | C1 step 3 / C2 step 4 |
| content-doc | baoyu-slide-deck (9.5) | C2 step 1 |
| content-doc | visual-forge (9.5) | C2 step 1 alt |
| content-doc | baoyu-diagram (9.0) | C2 step 3 |
| content-presentation | awesome-design-md (10.0) | C2 brand discipline |
| content-presentation | deck-that-wins (9.5) | C2 step 1 |
| content-presentation | spreadsheet-formula-helper (8.5) | 1-shot |
| content-presentation | to-prd (8.5) | 1-shot |
| content-presentation | meeting-notes-and-actions (8.0) | C1 alt |
| content-video | remotion (9.7) | C3 step 5 alt |
| content-video | video-content-analyzer (9.0) | C3 analysis |
| content-video | video-analyzer (8.5) | C3 step 5 |
| content-video | video-frame-extractor (8.5) | C3 step 3 alt |
| content-video | zero-debt-lint (8.5) | C2 gate |
| content-image | baoyu-article-illustrator (9.5) | C2 step 2 |
| content-image | baoyu-comic (9.5) | C2 |
| content-image | baoyu-cover-image (9.5) | C2 step 3 |
| content-image | baoyu-image-cards (9.5) | C2 step 2 |
| content-image | baoyu-imagine (9.5) | 1-shot generation |
| content-social | baoyu-danger-x-to-markdown (9.5) | C4 step 5 alt |
| content-social | baoyu-format-markdown (9.5) | C4 step 1 |
| content-social | baoyu-post-to-wechat (9.5) | C4 step 5 |
| content-social | baoyu-translate (9.5) | C4 step 4 |
| content-social | baoyu-xhs-images (deprecated) | C2 (use baoyu-image-cards) |
| content-seo | ai-seo (7.8) | C4 gate |
| content-seo | programmatic-seo (7.8) | C4 step 3 |
| content-seo | schema-markup (7.8) | C4 step 6 |
| content-seo | seo-audit (7.3) | 1-shot |
| social-media-cn | xhs-publish (7.8) | C4 CN step |
| social-media-cn | xiaohongshu-skills (6.8) | C4 CN |
| video-production | faceless-explainer (7.8) | C3 step 1 |
| video-production | hyperframes-cli (7.8) | C3 step 3 |
| video-production | motion-graphics (7.8) | C3 step 2 |
| video-production | talking-head-recut (7.8) | C3 step 1 alt |
| video-production | embedded-captions (7.3) | C3 step 4 |

## Anti-Override Rules

These skills **must not** be invoked unless context demands:
- **ai-seo** — only when "SEO", "discovery", "AI citation"
- **schema-markup** — only when "structured data", "rich result"
- **baoyu-post-to-wechat** — only when "WeChat", "公众号"
- **xhs-publish** — only when "小红书"
- **remotion** — only when "programmatic React video"
- **faceless-explainer** — only when "no talking head"
- **baoyu-translate** — only when "translate", "localize"

## Cross-Cluster Bridges

| Content ask | Defer to |
|-------------|----------|
| High-fidelity UI mockup | `design-orchestrator` |
| Investor pitch (with financial) | `business-orchestrator` Path B3 |
| Marketing campaign (with finance) | `business-orchestrator` Path B4 |

## Fallback

If no skill matches:
1. **AskUserQuestion** to clarify format (doc / visual / video / social)
2. Default to **Path C1 (Doc)** — most common
3. Never invoke all 130 skills
