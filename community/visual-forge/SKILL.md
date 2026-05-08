---
name: visual-forge
description: Professional presentation and web design system combining brand precision (68+ design systems), narrative structure, and 30+ visual styles. Generates PPT decks, landing pages, and infographics with pixel-perfect execution. Use when user asks to create slides, web pages, landing pages, or visual content.
version: 1.0.0
tags: [design, presentation, web, ui, ppt, slides, landing-page, infographic, visual-design]
---

# Visual Forge

**一站式视觉内容生成系统** — 融合品牌规范、叙事结构、视觉风格的专业设计工具。

## 何时使用 (When to Use)

触发关键词：
- **PPT/幻灯片**："做个PPT"、"create slides"、"presentation deck"、"演示文稿"
- **网页设计**："landing page"、"官网"、"产品页"、"网页设计"、"web design"
- **信息图**："infographic"、"可视化"、"信息图表"、"visual summary"
- **风格探索**："推荐设计风格"、"什么风格合适"、"design direction"

## 核心能力概览

1. **品牌精度库** — 68+ 设计系统（Vercel/Apple/Stripe/Notion...）
2. **叙事结构** — 竞赛级 PPT 框架（WDC 2026 获胜规则）
3. **视觉风格** — 30+ 设计方向（企业/科技/创意/经典/北欧/艺术）
4. **智能推荐** — 基于内容/受众/行业自动匹配最佳组合

---

## 工作流程 (4 阶段)

### Phase 1: 需求理解

使用 `AskUserQuestion` 工具收集 4 个关键维度：

1. **内容类型**：PPT / Landing Page / 信息图 / 其他
2. **目标受众**：专业人士 / 高管 / 初学者 / 投资人
3. **情感基调**：专业严谨 / 友好亲和 / 创新前卫 / 信任权威 / 大胆有趣
4. **品牌参考**（可选）：Vercel / Apple / Stripe / Notion / 无

**追问**（如需要）：
- 内容来源：有素材吗？（文档/数据/旧PPT/文章）
- 图片素材：有图吗？放哪？
- 硬约束：必须包含 XX / 不能出现 YY

### Phase 2: 风格推荐

基于 Phase 1 输入，从以下组合中推荐 **3 个方向**：

**推荐逻辑示例**：

| 输入组合 | 推荐方向 1 | 推荐方向 2 | 推荐方向 3 |
|---------|-----------|-----------|-----------|
| PPT + 高管 + 专业 | Vercel Minimal | Apple Product Focus | Swiss Style Clean |
| Landing + 大众 + 友好 | Notion Warm | Airbnb Friendly | Mid-Century Modern |
| PPT + 评委 + 创新 | Stripe Gradient Data | Linear Sharp | Brutalist Tech |
| 信息图 + 专业人士 + 数据 | Data Viz Dense | Magazine Editorial | Corporate Clean |

每个推荐包含：

```markdown
### 方向 1: [品牌名 + 风格名]

**为什么推荐**：[1-2 句理由]

**色板**：
- Primary: #HEX
- Background: #HEX
- Text: #HEX
- Accent: #HEX

**字体**：
- Heading: [Font Family] [Weight]
- Body: [Font Family] [Weight]

**视觉特征**：
- [3-5 个关键词，如：极简、留白充足、无衬线、渐变色]

**适用场景**：
- [具体适用的内容类型和受众]

**AI 提示词模板**：
```
[可直接用于 Midjourney/DALL-E/Gemini 的 prompt]
```
```

**确认步骤**：
- 向用户展示 3 个方向
- 用户选择 1 个（或要求"混合 1+2" / "全新方向"）
- 确认后进入 Phase 3

### Phase 3: 内容规划

#### 3.1 PPT 专用：叙事弧 + 页数规划

使用 **黄金叙事弧**（基于 WDC 2026 APAC 获胜规则）：

```
┌─ Hook (1 页) ──────────────────────────┐
│  反差/问题/硬数据抓眼球                  │
│  ❌ "Our solution is innovative"       │
│  ✅ "95% of teams waste 10h/week on X" │
└────────────────────────────────────────┘
┌─ Context (1-2 页) ─────────────────────┐
│  背景/身份/为什么讲这个                  │
│  ❌ "Founded in 2020, 50 employees"    │
│  ✅ "India is building. China is       │
│      freezing. Japan monetizes         │
│      aesthetics." (记忆度语言)          │
└────────────────────────────────────────┘
┌─ Core (3-5 页) ────────────────────────┐
│  核心内容，视觉穿插                      │
│  Layout 建议：                           │
│  - 图文 1:1 (大图+短文)                  │
│  - 数据可视化 (图表主导)                  │
│  - 三栏对比 (Before/After/Impact)       │
│  - 流程图 (Timeline/步骤)                │
└────────────────────────────────────────┘
┌─ Shift (1 页) ─────────────────────────┐
│  打破预期/新观点                         │
│  ❌ "Here's our roadmap"               │
│  ✅ "What if [反常识洞察]?"              │
└────────────────────────────────────────┘
┌─ Takeaway (1-2 页) ────────────────────┐
│  金句/悬念/行动建议                      │
│  ❌ "Thank you for your attention"     │
│  ✅ "The question is not whether to    │
│      act, but who acts first."         │
└────────────────────────────────────────┘
```

**竞赛级质量检查清单**：
- [ ] **记忆度语言**：每个关键主张能在 10 分钟后复述吗？
- [ ] **零感官债务**：0 拼写错误、0 绝对路径、0 占位符、0 Lorem ipsum
- [ ] **自夸控制**：Team/方法论/致谢合并 ≤ 1 页
- [ ] **视觉节奏**：连续 3 页以上纯文字？必须插入视觉页（图/图表/图标）

输出：`outline.md`（大纲文件）

#### 3.2 Landing Page 专用：分屏规划

使用 **Hero + 3-5 核心分屏 + CTA** 结构：

```
┌─ Hero (Above Fold) ────────────────────┐
│  · 主标题 (8-12 字，核心价值主张)         │
│  · 副标题 (20-30 字，补充说明)           │
│  · CTA 按钮 (Start Free / Get Demo)    │
│  · Hero 图 (产品截图/视觉插画)           │
└────────────────────────────────────────┘
┌─ Section 1: Problem (问题场景) ─────────┐
│  视觉：痛点插画 / Before 对比图           │
└────────────────────────────────────────┘
┌─ Section 2: Solution (解决方案) ────────┐
│  视觉：产品功能截图 / 流程图               │
└────────────────────────────────────────┘
┌─ Section 3: Proof (社会证明) ───────────┐
│  视觉：客户 Logo / 数据可视化 / 用户评价   │
└────────────────────────────────────────┘
┌─ Section 4 (可选): Features ───────────┐
│  视觉：3 栏卡片 / Icon + 文字             │
└────────────────────────────────────────┘
┌─ CTA Section (Bottom) ─────────────────┐
│  · 行动号召 (立即开始 / 预约 Demo)        │
│  · 次级链接 (阅读文档 / 查看定价)         │
└────────────────────────────────────────┘
```

输出：`wireframe.md`（线框图描述）

#### 3.3 信息图专用：布局选择

从 21 种布局中推荐 1 个：

| 布局类型 | 适用场景 | 视觉特征 |
|---------|---------|---------|
| **Timeline** | 历史事件、产品路线图、流程步骤 | 横向时间轴、节点标注 |
| **Comparison** | 产品对比、Before/After、方案选择 | 左右对比、表格、色块区分 |
| **Hierarchy** | 组织架构、分类体系、决策树 | 金字塔、树状图、层级嵌套 |
| **Flow** | 用户旅程、业务流程、数据流 | 箭头连接、泳道图、流程图 |
| **Data Story** | 数据洞察、研究报告、趋势分析 | 图表主导、数字突出、配色分类 |
| **Grid Mosaic** | 多维度对比、产品矩阵、概念全景 | 九宫格、卡片阵列、图标 + 文字 |

详见 `references/infographic-layouts.md`（21 种完整列表）

输出：`layout-spec.md`（布局规格说明）

### Phase 4: 生成执行

#### 4.1 技术路径选择

根据输出格式选择工具链：

| 输出格式 | 推荐路径 | 工具 |
|---------|---------|------|
| **HTML 网页** | 直接生成 HTML + CSS | 模板引擎 + 内联样式 |
| **PPT (可编辑)** | HTML → PPTX | `html2pptx` 转换 |
| **PDF (打印)** | HTML → PDF | Playwright 截图 / Puppeteer |
| **PNG (分享)** | HTML → PNG | Playwright 逐页截图 |

#### 4.2 代码生成规范

**HTML 模板结构**：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[项目名]</title>
  <style>
    /* ===== 主题变量 ===== */
    :root {
      /* 品牌色（从 Phase 2 选定的风格） */
      --color-primary: #HEX;
      --color-background: #HEX;
      --color-text: #HEX;
      --color-accent: #HEX;
      
      /* 字体 */
      --font-heading: "Inter", sans-serif;
      --font-body: "Inter", sans-serif;
      --font-code: "SF Mono", monospace;
      
      /* 间距（8px 网格） */
      --space-xs: 8px;
      --space-sm: 16px;
      --space-md: 24px;
      --space-lg: 48px;
      --space-xl: 96px;
      
      /* 断点 */
      --breakpoint-sm: 640px;
      --breakpoint-md: 768px;
      --breakpoint-lg: 1024px;
    }
    
    /* ===== Reset + Base ===== */
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: var(--font-body);
      color: var(--color-text);
      background: var(--color-background);
      line-height: 1.6;
    }
    
    /* ===== 组件样式 ===== */
    /* 根据选定的品牌风格生成对应的 button/card/section 样式 */
  </style>
</head>
<body>
  <!-- 内容区 -->
</body>
</html>
```

**代码质量要求**：
- ✅ 语义化 HTML5 标签（`<header>`, `<section>`, `<article>`）
- ✅ CSS 变量系统（可一键换主题）
- ✅ 响应式设计（移动端适配）
- ✅ 无内联 `style` 属性（全部走 CSS 类）
- ✅ 图片优化（WebP 格式，lazy loading）
- ❌ 禁用绝对路径（`/Users/...`）
- ❌ 禁用占位符内容（Lorem ipsum）
- ❌ 禁用硬编码尺寸（用 CSS 变量 + rem）

#### 4.3 输出文件结构

```
project-name/
├── index.html              # 主文件
├── images/                 # 图片资源
│   ├── hero.webp
│   ├── feature-1.webp
│   └── ...
├── outline.md              # 大纲 (PPT 专用)
├── wireframe.md            # 线框图 (Landing Page 专用)
├── layout-spec.md          # 布局规格 (信息图专用)
└── README.md               # 使用说明
```

---

## 进阶功能

### 1. 品牌设计系统深度应用

如果用户选择了品牌参考（如 Vercel），从 `references/brand-systems/vercel.md` 加载完整规范：

```yaml
# references/brand-systems/vercel.md 示例
name: Vercel
philosophy: "Minimalism with purpose. Every pixel serves function."

colors:
  primary: "#000000"
  background: "#FFFFFF"
  text: "#000000"
  text_muted: "#666666"
  border: "#EAEAEA"
  accent: "#0070F3"

typography:
  heading:
    family: "Inter"
    weights: [600, 700]
    sizes: [32px, 48px, 64px]
    line_height: 1.2
    letter_spacing: "-0.02em"
  body:
    family: "Inter"
    weight: 400
    size: 16px
    line_height: 1.6

spacing:
  grid: "8px"
  section_gap: "96px"
  card_padding: "24px"

components:
  button:
    border_radius: "6px"
    padding: "12px 24px"
    font_size: "14px"
    font_weight: 500
    transition: "all 200ms cubic-bezier(0.4, 0, 0.2, 1)"
```

### 2. 参考图样式提取

如果用户提供参考图（`--ref <files...>`），使用 3 种模式：

| 模式 | 用法 |
|------|------|
| `direct` | 传递给 AI 图生成工具作为风格参考 |
| `style` | 提取特征（线条/纹理/氛围）→ 追加到 prompt |
| `palette` | 提取颜色 hex 值 → 覆盖主题色 |

**palette 提取示例**：

```bash
# 使用 ImageMagick 提取主色板
convert ref-image.jpg -resize 1x1\! -format "%[pixel:p{0,0}]" info:-
# 或使用 Python PIL
python scripts/extract_palette.py ref-image.jpg --colors 5
# 输出：["#2E3440", "#D8DEE9", "#88C0D0", "#BF616A", "#A3BE8C"]
```

### 3. 多语言支持

自动检测用户语言（中文/英文/日文...），响应、文件名、提示词全部跟随：

- 中文用户 → `项目名/大纲.md`, `生成时间: 2026-05-08`
- 英文用户 → `project-name/outline.md`, `Generated: 2026-05-08`
- 日文用户 → `プロジェクト名/アウトライン.md`, `生成日時: 2026-05-08`

---

## 附录资源

### A. 品牌系统库 (68+)

详见 `references/brand-systems.md`（每个品牌独立 YAML 文件）

**开发者品牌**：Vercel, Linear, Stripe, GitHub, Supabase, Tailwind, shadcn/ui, Radix UI, Clerk, Raycast, Arc Browser, Cal.com, Resend, Mintlify, Dub, v0, Cursor, Replicate, Modal, Anthropic

**消费者品牌**：Apple, Airbnb, Spotify, Notion, Figma, Framer, Dropbox, Discord, Slack, Shopify, Atlassian, Miro, Canva, Airtable, Monday

### B. 视觉风格库 (30+)

详见 `references/visual-styles.md`（每种风格包含调色板、字体、空间、元素、情绪）

### C. 信息图布局库 (21 种)

详见 `references/infographic-layouts.md`

### D. 叙事模板库

详见 `templates/narrative-arcs/`

- `pitch-deck.md` — 融资路演模板
- `training.md` — 培训材料模板
- `product-launch.md` — 产品发布模板
- `research-report.md` — 研究报告模板

---

## 常见问题 (FAQ)

**Q: 和 awesome-design-md / magazine-web-ppt / baoyu-slide-deck 有什么区别？**

A: **Visual Forge** 是整合版：
- 继承 `awesome-design-md` 的 68 品牌精确规范
- 继承 `deck-that-wins` 的竞赛级叙事框架
- 继承 `magazine-web-ppt` 的主题色系统
- 继承 `baoyu-slide-deck` 的受众细分 + 参考图机制
- 继承 `canvas-design` 的视觉哲学创作方法
- 继承 `huashu-design` 的 3 方向推荐逻辑

**新增能力**：
- 统一工作流（4 阶段，适配 PPT/Landing/信息图）
- 智能推荐系统（输入 → 自动匹配最佳组合）
- 技术路径选择（HTML/PPTX/PDF/PNG 自动适配）

**Q: 输出的 HTML 可以直接用吗？**

A: 是的，但推荐流程：
1. 生成 HTML → 浏览器预览
2. 用户确认 → 如需调整，修改 CSS 变量或局部组件
3. 最终确认 → 转换为目标格式（PPTX/PDF/PNG）

**Q: 如何添加新的品牌系统？**

A: 在 `references/brand-systems/` 创建新 YAML：

```yaml
# references/brand-systems/my-brand.md
name: My Brand
philosophy: "..."

colors: {...}
typography: {...}
spacing: {...}
components: {...}
```

然后在 `references/brand-systems.md` 索引中添加入口。

**Q: 竞赛级 PPT 规则适用于日常使用吗？**

A: 适用，但可降级：
- **竞赛场景**：严格遵守（零感官债务、记忆度语言、音频质量）
- **日常场景**：选择性应用（叙事弧 + 视觉节奏必须，音频质量可选）

**Q: 支持暗色模式吗？**

A: 部分支持。如果选定的品牌有暗色规范（如 GitHub Dark），会生成对应变量：

```css
:root {
  --color-background-light: #FFFFFF;
  --color-background-dark: #0D1117;
  --color-text-light: #000000;
  --color-text-dark: #E6EDF3;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-background: var(--color-background-dark);
    --color-text: var(--color-text-dark);
  }
}
```

---

## 版本历史

**v1.0.0** (2026-05-08)
- 初始发布
- 整合 8 个前辈 skills 的最佳实践
- 支持 PPT / Landing Page / 信息图 3 种输出
- 68+ 品牌系统，30+ 视觉风格
- 4 阶段工作流 + 智能推荐系统

---

**Meta**: 本 skill 基于以下前辈 skills 的精华整合而成：
- `awesome-design-md` — 品牌精度
- `deck-that-wins` — 竞赛叙事
- `magazine-web-ppt` — 主题系统
- `baoyu-slide-deck` — 受众细分
- `baoyu-infographic` — 布局矩阵
- `canvas-design` — 视觉哲学
- `ikea-designer` — 北欧美学
- `huashu-design` — 风格推荐

择其善者而从之，其不善者而改之。
