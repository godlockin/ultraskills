# Brand Systems Library

68+ 设计系统精确规范库，每个品牌包含色彩/字体/间距/组件/动效完整定义。

## Quick Index

| Category | Brands |
|----------|--------|
| **Developer Tools** (20) | Vercel, Linear, Stripe, GitHub, Supabase, Tailwind, shadcn/ui, Radix UI, Clerk, Raycast, Arc Browser, Cal.com, Resend, Mintlify, Dub, v0, Cursor, Replicate, Modal, Anthropic |
| **Consumer Apps** (15) | Apple, Airbnb, Spotify, Notion, Figma, Framer, Dropbox, Discord, Slack, Shopify, Atlassian, Miro, Canva, Airtable, Monday |
| **Enterprise** (10) | Salesforce, HubSpot, Asana, Trello, Zoom, Microsoft, Google Workspace, Adobe, Zendesk, Intercom |
| **E-commerce** (8) | Amazon, Etsy, eBay, Walmart, Target, Best Buy, Wayfair, Overstock |
| **Media & Content** (8) | Netflix, YouTube, Medium, Substack, Ghost, WordPress, Wix, Squarespace |
| **Finance** (7) | Stripe, PayPal, Square, Coinbase, Robinhood, Revolut, Wise |

---

## Brand Detail Format

每个品牌独立文件：`brand-systems/[brand-slug].md`

示例结构（以 Vercel 为例）：

```yaml
name: Vercel
philosophy: "Minimalism with purpose. Every pixel serves function. Speed is UX."
industry: Developer Tools
url: https://vercel.com

# Visual Theme
theme:
  mood: Professional, Fast, Developer-First
  keywords: [Minimalist, High-Contrast, Monochrome, Futuristic]
  avoid: [Gradients, Shadows, Rounded-Heavy, Playful]

# Colors
colors:
  # Primary
  black: "#000000"
  white: "#FFFFFF"
  
  # Grays
  gray_50: "#FAFAFA"
  gray_100: "#F5F5F5"
  gray_200: "#E5E5E5"
  gray_300: "#D4D4D4"
  gray_400: "#A3A3A3"
  gray_500: "#737373"
  gray_600: "#525252"
  gray_700: "#404040"
  gray_800: "#262626"
  gray_900: "#171717"
  
  # Accent
  blue: "#0070F3"
  pink: "#FF0080"
  cyan: "#50E3C2"
  
  # Semantic
  success: "#0070F3"
  error: "#EE0000"
  warning: "#F5A623"

# Typography
typography:
  heading:
    family: "Inter"
    weights: [600, 700]
    sizes:
      h1: 64px
      h2: 48px
      h3: 32px
      h4: 24px
    line_height: 1.2
    letter_spacing: "-0.02em"
  
  body:
    family: "Inter"
    weight: 400
    size: 16px
    line_height: 1.6
    letter_spacing: "0"
  
  label:
    family: "Inter"
    weight: 500
    size: 14px
    line_height: 1.4
    letter_spacing: "0.01em"
  
  code:
    family: "Menlo, Monaco, 'Courier New', monospace"
    weight: 400
    size: 14px
    line_height: 1.6

# Spacing
spacing:
  grid: 8px
  section_gap: 96px
  card_padding: 24px
  button_padding: "12px 24px"
  
  breakpoints:
    sm: 640px
    md: 768px
    lg: 1024px
    xl: 1280px

# Components
components:
  button:
    primary:
      background: "#000000"
      color: "#FFFFFF"
      border: "none"
      border_radius: "6px"
      padding: "12px 24px"
      font_size: "14px"
      font_weight: 500
      transition: "all 200ms cubic-bezier(0.4, 0, 0.2, 1)"
      hover:
        background: "#262626"
    
    secondary:
      background: "#FFFFFF"
      color: "#000000"
      border: "1px solid #EAEAEA"
      border_radius: "6px"
      padding: "12px 24px"
      font_size: "14px"
      font_weight: 500
      transition: "all 200ms cubic-bezier(0.4, 0, 0.2, 1)"
      hover:
        border_color: "#000000"
  
  card:
    background: "#FFFFFF"
    border: "1px solid #EAEAEA"
    border_radius: "8px"
    padding: "24px"
    shadow: "0 2px 8px rgba(0, 0, 0, 0.04)"
    hover:
      shadow: "0 4px 16px rgba(0, 0, 0, 0.08)"
  
  input:
    background: "#FFFFFF"
    border: "1px solid #D4D4D4"
    border_radius: "6px"
    padding: "12px 16px"
    font_size: "14px"
    color: "#000000"
    transition: "border-color 200ms"
    focus:
      border_color: "#000000"
      outline: "none"

# Motion
motion:
  transition:
    fast: "100ms cubic-bezier(0.4, 0, 0.2, 1)"
    normal: "200ms cubic-bezier(0.4, 0, 0.2, 1)"
    slow: "400ms cubic-bezier(0.4, 0, 0.2, 1)"
  
  animation:
    fade_in:
      duration: "200ms"
      easing: "ease-out"
    
    slide_up:
      duration: "400ms"
      easing: "cubic-bezier(0.16, 1, 0.3, 1)"

# Code Examples
code_examples:
  css_variables: |
    :root {
      --color-black: #000000;
      --color-white: #FFFFFF;
      --color-gray-50: #FAFAFA;
      --color-blue: #0070F3;
      
      --font-heading: "Inter", sans-serif;
      --font-body: "Inter", sans-serif;
      --font-code: "Menlo", monospace;
      
      --space-xs: 8px;
      --space-sm: 16px;
      --space-md: 24px;
      --space-lg: 48px;
      --space-xl: 96px;
      
      --transition-normal: 200ms cubic-bezier(0.4, 0, 0.2, 1);
    }
  
  button_component: |
    .btn-primary {
      background: var(--color-black);
      color: var(--color-white);
      border: none;
      border-radius: 6px;
      padding: 12px 24px;
      font-size: 14px;
      font-weight: 500;
      transition: var(--transition-normal);
    }
    
    .btn-primary:hover {
      background: #262626;
    }
```

---

## Quick Comparison Table

| Brand | Primary Color | Font | Mood | Best For |
|-------|--------------|------|------|----------|
| **Vercel** | Black (#000) | Inter | Minimalist | Developer tools, SaaS dashboards |
| **Linear** | Blue (#5E6AD2) | Inter | Sharp, Focused | Project management, Task tools |
| **Stripe** | Purple (#635BFF) | Inter + SF Mono | Data-driven | Fintech, Analytics, Dashboards |
| **Apple** | Gray (#1D1D1F) | SF Pro | Premium, Elegant | Product pages, Hardware launches |
| **Notion** | Beige (#F7F6F3) | Inter | Warm, Friendly | Note-taking, Collaboration, Wiki |
| **Airbnb** | Coral (#FF385C) | Cereal | Welcoming | Travel, Hospitality, Community |
| **Figma** | Multi (#F24E1E + #A259FF) | Inter | Creative, Bold | Design tools, Creative platforms |

---

## Usage

1. **选择品牌**：基于用户输入的行业/受众/基调匹配最相关的 3 个品牌
2. **加载规范**：从 `brand-systems/[slug].md` 读取完整 YAML
3. **应用到代码**：使用 `code_examples.css_variables` 作为 `:root` 块
4. **组件生成**：基于 `components.*` 生成对应 HTML/CSS

---

## 贡献新品牌

要添加新品牌系统，创建 `brand-systems/new-brand.md`，格式遵循上述 YAML 结构，包含：

- [ ] `philosophy` — 1-2 句设计哲学
- [ ] `colors` — 至少 primary, background, text, accent, semantic 5 组
- [ ] `typography` — heading, body, label, code 4 套完整定义
- [ ] `spacing` — grid, section_gap, 断点
- [ ] `components` — button, card, input 最低 3 个
- [ ] `motion` — transition + animation 示例
- [ ] `code_examples` — 可直接复制的 CSS 变量

然后在本文件顶部 Quick Index 添加索引项。

---

**Note**: 完整的 68 个品牌文件存放在 `references/brand-systems/` 目录，本文件仅为索引和示例。需要时读取对应品牌的独立文件。
