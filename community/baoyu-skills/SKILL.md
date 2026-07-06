---
name: baoyu-skills
description: "Curated content + social publishing toolkit (20 skills) — image generation, illustration, document formatting, social posting. Originally by JimLiu/baoyu-skills (now archived), migrated to community/ for local maintenance. Triggers: 'illustrate article', 'add images to article', 'make infographic', 'generate cover', 'comic strip', 'image cards', 'post to WeChat', 'post to Weibo', 'post to X', 'XHS images', 'X to markdown', 'URL to markdown', 'YouTube transcript', 'translate article', 'markdown to HTML', 'slide deck', 'diagram', 'compress image', 'format markdown'."
version: 1.0.0
tags: [baoyu, content, social, image, doc, community]
source: https://github.com/JimLiu/baoyu-skills (archived)
source_version: v1.114.0 (2026-05-05)
license: MIT-0
---

# baoyu-skills — Content & Social Publishing Toolkit

20 curated skills covering image generation, article illustration, document formatting, and social publishing.

Originally a `JimLiu/baoyu-skills` submodule; upstream archived → migrated to `community/baoyu-skills/` for local maintenance.

## Structure

```
baoyu-skills/
├── image/                        # Image generation & illustration
│   ├── baoyu-imagine                 # Multi-provider image gen (Wan 2.7, etc.)
│   ├── baoyu-article-illustrator     # ⭐ winner: analyze article → pick positions → generate
│   ├── baoyu-infographic             # Info-graphic generation
│   ├── baoyu-comic                   # Comic strip generation
│   ├── baoyu-cover-image             # Cover image generation
│   └── baoyu-image-cards             # Card-style image series
├── doc/                          # Document formatting
│   ├── baoyu-markdown-to-html        # MD → semantic HTML
│   ├── baoyu-slide-deck              # MD → slide deck
│   ├── baoyu-diagram                 # Diagram generation
│   └── baoyu-compress-image          # Image compression
└── social/                       # Social publishing + content extraction
    ├── baoyu-danger-x-to-markdown    # ⭐ winner: scrape X/Twitter safely
    ├── baoyu-danger-gemini-web       # Gemini Web with safety
    ├── baoyu-url-to-markdown         # Generic URL → MD
    ├── baoyu-youtube-transcript      # YouTube transcript extraction
    ├── baoyu-format-markdown         # Markdown formatter
    ├── baoyu-translate               # Article translation
    ├── baoyu-post-to-wechat          # WeChat publishing
    ├── baoyu-post-to-weibo           # Weibo publishing
    ├── baoyu-post-to-x               # X/Twitter publishing
    └── baoyu-xhs-images              # Xiaohongshu images
```

## Cluster Winners

| Cluster | Winner | Score |
|---------|--------|-------|
| content-image | `baoyu-article-illustrator` | 8.8 |
| content-social | `baoyu-danger-x-to-markdown` | 8.8 |

## Trigger Patterns

- "Illustrate this article" → `baoyu-article-illustrator`
- "Generate cover image" → `baoyu-cover-image`
- "Make an infographic" → `baoyu-infographic`
- "Convert MD to slide deck" → `baoyu-slide-deck`
- "Post to WeChat" → `baoyu-post-to-wechat`
- "Scrape this X/Twitter thread" → `baoyu-danger-x-to-markdown`
- "Get YouTube transcript" → `baoyu-youtube-transcript`
- "Translate article to Chinese" → `baoyu-translate`
- "Compress these images" → `baoyu-compress-image`

## Status

- **Migrated from**: `external/baoyu-skills` submodule (2026-07-06)
- **Upstream**: JimLiu/baoyu-skills — archived/deleted, no further syncs possible
- **Local modifications preserved**: dirty changes from upstream (incl. `baoyu-imagine` google.ts provider update)
- **Skipped**: `baoyu-image-gen` (was locally deleted before migration; not in arena index)