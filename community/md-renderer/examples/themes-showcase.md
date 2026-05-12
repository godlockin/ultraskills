# Magazine Themes Showcase

Enhanced md-renderer now includes **5 精心调配的杂志主题**，每套主题都经过配色优化，适合不同场景。

---

## 🖋 墨水经典 (Monocle)

**适合场景:** 通用分享、商业发布、科技产品

**特点:** 纯墨黑 + 暖米白，杂志感最强

```bash
python3 scripts/md_render_enhanced.py doc.md --theme monocle
```

**配色:**
- 主色: `#0a0a0b` (墨黑)
- 背景: `#f1efea` (暖米白)
- 风格: Monocle / Apricot / A Book Apart

---

## 🌊 靛蓝瓷 (Indigo Porcelain)

**适合场景:** 科技/研究/数据分享、工程师文化、深度内容

**特点:** 深靛蓝 + 瓷白，冷静、理性、有深度

```bash
python3 scripts/md_render_enhanced.py doc.md --theme indigo
```

**配色:**
- 主色: `#0a1f3d` (深靛蓝)
- 背景: `#f1f3f5` (瓷白)
- 风格: 学术期刊 / 蓝印花瓷器

---

## 🌿 森林墨 (Forest Ink)

**适合场景:** 自然/可持续/文化/非虚构内容、户外品牌

**特点:** 深森林绿 + 象牙，沉稳、有呼吸感

```bash
python3 scripts/md_render_enhanced.py doc.md --theme forest
```

**配色:**
- 主色: `#1a2e1f` (森林绿)
- 背景: `#f5f1e8` (象牙)
- 风格: 《国家地理》旧版

---

## 🍂 牛皮纸 (Kraft Paper)

**适合场景:** 怀旧/人文/阅读/历史/文学分享、独立杂志

**特点:** 深棕 + 暖米，温暖、有年代感

```bash
python3 scripts/md_render_enhanced.py doc.md --theme kraft
```

**配色:**
- 主色: `#2a1e13` (深棕)
- 背景: `#eedfc7` (暖米)
- 风格: 牛皮信封 / 老笔记本

---

## 🌙 沙丘 (Dune)

**适合场景:** 艺术/设计/创意/时尚分享、画廊手册

**特点:** 炭灰 + 沙色，克制、高级、中性

```bash
python3 scripts/md_render_enhanced.py doc.md --theme dune
```

**配色:**
- 主色: `#1f1a14` (炭灰)
- 背景: `#f0e6d2` (沙色)
- 风格: 沙漠黄昏 / 建筑设计图册

---

## 快速选择指南

| 内容类型 | 推荐主题 |
|---------|---------|
| 不知道选啥 / 第一次用 | 🖋 墨水经典 |
| AI / 技术 / 产品发布 | 🌊 靛蓝瓷 |
| 内容 / 行业观察 / 文化 | 🌿 森林墨 |
| 书评 / 生活方式 / 人文 | 🍂 牛皮纸 |
| 设计 / 艺术 / 品牌 | 🌙 沙丘 |

---

## Interactive Features

All themes include:

- **Sidebar TOC** — Auto-generated from headings, sticky positioning
- **Reading Progress Bar** — Top of page, smooth animation
- **Copy Code Buttons** — Hover to reveal, click to copy
- **Active State Tracking** — TOC highlights current section
- **Responsive Layout** — Mobile-friendly
- **Print-Optimized** — Clean print CSS

---

## Typography

**Headings:** Noto Serif SC + Playfair Display (衬线，典雅)  
**Body:** Noto Sans SC + Inter (非衬线，易读)  
**Code:** IBM Plex Mono (等宽，专业)

---

## Demo

See `examples/demo_*.html` for all 5 themes applied to the same content.

```bash
# Generate all themes
for theme in monocle indigo forest kraft dune; do
    python3 scripts/md_render_enhanced.py examples/demo.md \
      -o "examples/demo_${theme}.html" \
      --theme "$theme"
done
```
