---
name: awwwards-design-intelligence
description: 基于 Awwwards 高分网站的设计鉴赏与趋势洞察，拆解决策背后的设计逻辑
version: 1.0.0
tags: [design, ui, ux, awwwards, trend-analysis, visual-design]
---

# Awwwards Design Intelligence

> 鉴赏 > 生成。通过拆解 Awwwards 高分网站，理解决策背后的设计逻辑。

**核心价值**: 现有 design skill 都是"生成"，本 skill 是"鉴赏"——帮助用户理解决策为什么好，而非怎么实现。

## 目标 (Goal)

* 解析 Awwwards 高分网站的共同设计模式
* 提炼 2026 UI 设计趋势关键词
* 建立可复用的设计模式分类体系
* 输出审美判断力，而非代码模板

## 核心概念 (Core Concepts)

### 2026 设计趋势关键词

| # | 关键词 | 说明 | 代表案例 |
|---|--------|------|----------|
| 1 | **Dark Mode First** | 深色主题成为默认选择 | Cooldock |
| 2 | **Glassmorphism** | 玻璃拟态、毛玻璃效果 | Get Blue |
| 3 | **Neo-Brutalism** | 新粗野主义、粗黑边框 | Deadstock Coffeee |
| 4 | **Micro-animations** | 微动效、滚动触发动画 | Awwwards 全站 |
| 5 | **Bento Grid** | 便当盒式布局、碎片化网格 | Studio OL |
| 6 | **Editorial Layout** | 杂志编辑风长滚动 | AI in Design Report |
| 7 | **Split Screen** | 分屏对半分栏设计 | Get Blue |
| 8 | **Gradient Accents** | 渐变色点缀 | Flora Café |
| 9 | **Typography-First** | 字体设计驱动视觉 | Russell Numo |
| 10 | **Scarcity UI** | 限量提示、紧迫感设计 | Solt Wagner |

### 色彩心理学

**黄金比例**: 主色 70%(背景) + 辅助色 25%(区块) + 点缀色 5%(CTA/徽章)

| 配色模式 | 情绪影响 | 适用场景 |
|---------|---------|---------|
| 暗色底 + 亮色点缀 | 专业感、沉浸、聚焦 | 技术产品、数据密集型 |
| 暖色系(深红/奶油白) | 亲和、信任、人文 | 创作者工具、社区平台 |
| 高对比度点缀(橙黄/电光蓝) | 活力、紧迫感、CTA | 行动号召、通知、徽章 |

**推荐色板**:
```css
:root {
  --bg-primary: #0a0a0f;      /* 深黑背景 */
  --bg-secondary: #141418;    /* 次级区块 */
  --text-primary: #fafafa;    /* 主文字 */
  --accent-primary: #FF6B00;  /* 活力橙 CTA */
  --accent-secondary: #667eea; /* 电光蓝渐变 */
}
```

### 字体配对

| 层级 | 推荐字体 | 字重/尺寸 |
|-----|---------|----------|
| 大标题 | Space Grotesk / Inter | Bold, 48-64px, Uppercase |
| 章节标题 | DM Sans / Plus Jakarta Sans | SemiBold, 24-32px |
| 正文 | IBM Plex Sans / Source Sans 3 | Regular, 16-18px |
| 代码/标签 | JetBrains Mono | Regular, 14px |

**组合公式**: 几何无衬线标题 + 人文无衬线正文 + 等宽字体代码

### 5 类可复用设计模式

**Pattern 1: Premium Dark Launch Landing**
- 深黑背景(#0a0a0f) + 高对比白色文字
- 中央对齐 Hero 区域：大标题 + CTA 按钮
- 功能特性三列卡片展示
- Testimonials 用户证言区
- FAQ 手风琴折叠
- 底部固定导航/CTA

**Pattern 2: Split-Screen Portfolio**
- 左侧大图 + 右侧文字描述
- 滚动时图片从边缘滑入
- 交替左右排列
- 锚点导航跳转章节
- 作品集卡片网格

**Pattern 3: Editorial Long-Scroll**
- 大号章节编号(01, 02, 03)
- 长文案 + 高质量配图
- 统计数字大字体展示
- 引用区块突出
- 底部订阅 CTA

**Pattern 4: Wellness Brand Identity**
- 暖色系(红/橙/米白)
- 衬线标题 + 无衬线正文
- 轮播图展示
- 植物/自然元素
- 手写感字体点缀

**Pattern 5: Streetwear/Hype Drop**
- 全屏 Hero 产品图
- 倒计时/限量标识
- 黑色背景 + 亮色强调(黄/橙)
- 粗体无衬线字体
- 邮件订阅入口

## 使用流程 (Workflow)

### Step 1: 识别设计风格

分析网站属于哪类设计模式：

```
技术产品/SaaS → Pattern 1 (Premium Dark)
作品集/创意展示 → Pattern 2 (Split-Screen)
品牌故事/内容站 → Pattern 3 (Editorial)
健康/生活方式 → Pattern 4 (Wellness)
电商/限量发售 → Pattern 5 (Hype Drop)
```

### Step 2: 分析设计要素

逐项检查：

| 维度 | 检查点 |
|------|--------|
| 色彩 | 主色/辅助色/点缀色比例是否合理？ |
| 排版 | 标题/正文/代码层级是否清晰？ |
| 布局 | Hero/Split/Bento/Grid 哪种布局？ |
| 动效 | 滚动触发/Hover/过渡动画？ |
| 信任 | 徽章/证言/数据/承诺？ |

### Step 3: 输出设计洞察

格式：

```markdown
## [网站名] 设计洞察

### 设计风格
[Pattern X 类型]

### 色彩系统
- 主色: #XXXXXX (占比 70%)
- 辅助色: #XXXXXX (占比 25%)
- 点缀色: #XXXXXX (占比 5%)

### 设计亮点
1. [亮点 1]
2. [亮点 2]
3. [亮点 3]

### 可借鉴点
- [可复用模式]

### 风险点
- [需要注意的地方]
```

## 最佳实践 (Best Practices)

### Do

* **预设 Dark Mode First**: 深黑 #0a0a0f 底 + #ffffff 主文字
* **大量留白分区块**: 32px+ 段落间距区分章节
* **统一图形语言**: 固定圆角 8px、图标风格(线性)
* **色彩标记系统**: 用固定颜色编码类别(工程=蓝、创意=紫)
* **3 秒法则**: 首屏同时完成价值声明 + 信任锚点 + 行动召唤

### Don't

* **不要盲目追求某一种风格**: 根据品牌调性选择
* **不要使用未授权素材**: 优先 CC0/CC BY 许可素材
* **不要省略信任信号**: 每个页面需 ≥3 种信任元素
* **不要忽略可访问性**: WCAG 对比度 ≥4.5:1
* **不要过度动效**: 动效时长 100-600ms，尊重 prefers-reduced-motion

## 反模式 (Anti-Patterns)

以下为 AI 生成的 boilerplate，鉴赏时需避免：

* ❌ 紫色渐变作为主色调
* ❌ 三列图标网格
* ❌ 居中一切的布局
* ❌ 统一的圆角 border-radius
* ❌ 渐变按钮作为主要 CTA
* ❌ 用 emoji 代替图标

## CSS 变量模板

```css
/* 设计 Token */
:root {
  /* 色彩 */
  --color-bg-primary: #0a0a0f;
  --color-bg-secondary: #141418;
  --color-bg-tertiary: #1e1e24;
  --color-text-primary: #fafafa;
  --color-text-secondary: #a1a1aa;
  --color-accent-primary: #FF6B00;
  --color-accent-secondary: #667eea;
  --color-accent-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

  /* 字体 */
  --font-heading: 'Space Grotesk', sans-serif;
  --font-body: 'IBM Plex Sans', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* 间距 */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 32px;
  --space-xl: 64px;

  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 16px;

  /* 阴影 */
  --shadow-sm: 0 2px 8px rgba(0,0,0,0.3);
  --shadow-md: 0 8px 32px rgba(0,0,0,0.4);
  --shadow-lg: 0 16px 48px rgba(0,0,0,0.5);
}

/* 玻璃拟态 */
.glass {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.1);
}

/* 渐变文字 */
.gradient-text {
  background: var(--color-accent-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

## 资源引用

* [Awwwards UI Design](https://www.awwwards.com/websites/ui-design/)
* [Deadstock Coffee](https://deadstockcoffee.com/) — Streetwear × Premium
* [Get Blue](https://www.getblue.com/) — Split-Screen Wellness
* [Cooldock](https://dock.cool) — Premium Dark SaaS
* [AI in Design Report 2026](https://stateofaidesign.com/) — Editorial Long-Scroll
* [Fontshare](https://fontshare.com/) — 可商用字体
* [Google Fonts](https://fonts.google.com/) — Inter, Space Grotesk

---

**差异化定位**: 现有 design skill (ui-ux-pro-max/awesome-design-md/design-html) 都是"生成"，本 skill 是"鉴赏"——帮助用户理解决策背后的设计逻辑。
