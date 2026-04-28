---
name: poster-print-design
description: 用 HTML/CSS 出海报、社交卡片 (OG / Twitter card)、印刷品 (A3/A4/名片)。Playwright 截图 → PNG/JPG/PDF（含 CMYK 出血提示）。模板库：博客分享卡、活动海报、Slogan 卡、价格表。Trigger on poster / 海报 / og image / social card / 分享卡 / print / a4 / 名片 / banner。
version: 1.0.0
created_at: 2026-04-28
entry_point: scripts/render.sh
dependencies: ["node>=18", "playwright (auto-install)"]
tags: [poster, print, social-card, og-image, design, html-to-png, community]
---

# poster-print-design

需要做：博客分享图、活动海报、产品价格表、名片？这个 skill 全用 **HTML+CSS** 做，再用 Playwright 渲染成 PNG/PDF。

## 为什么 HTML/CSS 而不是 Figma/PS

- ✅ AI 能直接改（修文案/换色/换图就一行）
- ✅ 模板可复用 (传 props)
- ✅ 版本控制 (git)
- ✅ 批量出图（数据驱动）
- ❌ 印刷级 CMYK 不完美（重要印刷活还是给印刷厂走 PDF/X）

## 适用尺寸

| 用途 | 尺寸 (px @ 96dpi) | 备注 |
|---|---|---|
| OG image | 1200×630 | Twitter / FB / LinkedIn |
| 微信分享 | 500×400 | 但建议 1200×900 高清 |
| Twitter banner | 1500×500 | |
| Instagram post | 1080×1080 / 1080×1350 | |
| YouTube thumbnail | 1280×720 | |
| 海报 A4 | 794×1123 (96dpi) / 2480×3508 (300dpi) | 印刷必须 300dpi |
| 海报 A3 | 1123×1587 (96dpi) / 3508×4961 (300dpi) | |
| 名片 | 1050×600 (90×54mm @300dpi) | 含 3mm 出血 → 1086×636 |

## Quick Start

```bash
# 一次性安装
bash scripts/install.sh

# 用模板出 OG image
bash scripts/render.sh og \
  --title "10 Lessons from Building UltraSkills" \
  --subtitle "Open-source skill library, 564 entries" \
  --author "@miao" \
  -o og.png

# 自定义 HTML → PNG
bash scripts/render.sh custom my-poster.html --width 1200 --height 1600 -o out.png

# 出印刷 PDF (300dpi)
bash scripts/render.sh custom flyer.html --pdf --size A4 -o flyer.pdf

# 批量（数据驱动）
cat events.json | bash scripts/render.sh batch event-template.html --out posters/
```

## 模板库

`templates/` 目录下：

| 模板 | 尺寸 | 字段 |
|---|---|---|
| `og.html` | 1200×630 | title, subtitle, author, gradient |
| `quote.html` | 1080×1080 | quote, author, brand |
| `event.html` | 794×1123 | title, date, venue, hosts |
| `pricing.html` | 1080×1350 | tiers[], features[] |
| `product.html` | 1200×630 | product, headline, cta |
| `card.html` | 1086×636 | name, title, contact, qr |

## CMYK / 印刷出血

HTML 默认 sRGB。要给印刷厂：
1. 用 **px @ 300dpi**（A4 = 2480×3508）
2. 加 **3mm 出血**（每边）+ **3mm 安全区**
3. 重要色（logo）用 **专色 swatch**（HTML 不支持 → 把 logo 作为预先转好的 PDF/X 嵌入）
4. 输出选 PDF（Playwright `--pdf`）

不重要的活（数字屏 / 网络分享）忽略 1-3。

## 反模式

- ❌ 用 96dpi 给印刷
- ❌ 标题 < 20px 在海报上
- ❌ 字段过多（4+ 行字 + 3+ 图标）→ 看着乱
- ❌ 默认 Web font 渲染 → 印刷小心 fallback
- ❌ 渐变 + 半透明在 CMYK 上掉色严重

## License: MIT
