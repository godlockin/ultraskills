# Design Orchestrator — 案例研究 (3 路径实操)

每个案例演示一次 orchestrator 从用户输入到完整 skill 链的执行轨迹。

---

## 案例 1: Greenfield 路径 — "Build SaaS Landing for AI Analytics"

**用户输入**: "Build a SaaS landing page for our AI analytics tool. We're B2B, technical buyers, want to feel premium without being intimidating."

### Orchestrator 决策表

**cluster signal**: brand/style (build) → 选 Path 1
**project state**: greenfield (no code mentioned)
**single vs multi**: pipeline-worthy (landing page 涉及多 skill)
**entry**: design-consultation

### 编排执行

| Step | Skill | 触发原因 | 输出 |
|------|-------|---------|------|
| 1 | design-consultation | 理解产品 + 研究 landscape + 提建议 | "modern-minimal genre, dark mode optional" |
| 2 | ui-ux-pro-max-skill | industry=SaaS, 生完整 design system | "Cobalt cluster, OkLCH, Inter + IBM Plex Mono" |
| 3 | design-tokens | 编译 tokens → CSS + Tailwind | tokens.css + tailwind.config.ts |
| 4 | motion-design | 仅 scroll-triggered opacity, 不要 bounce | scroll-spec.md |
| 5 | icon-system | Phosphor `regular`, line icons | icon library |
| 6 | awwwards-design-intelligence | cross-check: 避开 Bento + Pagination | "OK, 走 modular-stack macro" |
| 7 | hallmark audit | 53 gates | PASS, no italic headers, no invented metrics |
| 8 | design-html | final Pretext HTML | working code |

### 关键决策

- **跳过 `ikea-designer-pro`** (用户没要 IKEA)
- **跳过 `awesome-design-md`** (用户没指定品牌)
- **插入 `color-expert`**: 当 ui-ux-pro-max 输出 palette 时, cross-check 用 color-expert 的 OKLCH formula 验证
- **bridges**: Step 2 输出的 palette → Step 3 tokens → Step 8 HTML 是线性依赖, 不能并行

### 耗时估算

如果手工: 4-6 小时
Orchestrator: 30-45 分钟 (含 25 分钟 anti-slop pass)
**compression**: ~6-8x (跟 gstack CLAUDE.md "feature implementation" 一致)

---

## 案例 2: Existing 路径 — "/workspace Feels AI-Generated"

**用户输入**: "/workspace feels AI-generated. Polish it. Don't change brand or copy."

### Orchestrator 决策表

**cluster signal**: audit/redesign → Path 2
**project state**: existing (路径明确给 /workspace)
**single vs multi**: pipeline-worthy (audit + fix 链条)
**entry**: plan-design-review (先得到维度评分)

### 编排执行

| Step | Skill | 触发原因 | 输出 |
|------|-------|---------|------|
| 1 | plan-design-review | plan-mode critique | "spacing 6/10, AI slop 3/10, hierarchy 7/10" |
| 2 | design-review | live visual audit | punch list with atomic fixes |
| 3 | accessibility-review | polish 可能引入 a11y regression | WCAG pass |
| 4 | hallmark audit `/workspace` | 53 gates | "italic header on hero, purple gradient on CTA" |
| 5 | design-html | atomic in-place fixes (additive, 不删文件) | updated files |
| (skip) | design-handoff | 用户说不改 brand, 不需要 handoff spec | — |

### 关键决策

- **跳过 design-shotgun**: 用户明确说"don't change brand",不要生成变体
- **跳过 design-system audit**: 已经有 design-consultation output 在用
- **关键技巧**: Step 5 用"in-place additive edits",遵循 hallmark 的 implementation safety rail

### 反例: 不该走的死胡同

| 错误路径 | 为什么错 |
|---------|---------|
| 直接 design-shotgun | 用户要 polish,不要新设计 |
| 跳过 plan-design-review 直接 design-review | 失去 plan-mode 维度评分 |
| 跑 完整 Path 2 (含 design-handoff) | 用户没要 spec |
| 加 motion-design | 用户没要动效 |

### 耗时

- 手工: 1-2 小时 (要猜哪些是 slop)
- Orchestrator: 15-20 分钟 (含 10 分钟 audit)
- **compression**: ~5x

---

## 案例 3: Inspiration 路径 — "Make It Look Like Stripe + Vercel"

**用户输入**: "I love Stripe's documentation aesthetic. Build our docs site the same way, but we're Vercel-product (not Stripe)."

### Orchestrator 决策表

**cluster signal**: brand style + clone → Path 3 Brand-Clone mode
**project state**: inspiration (uses named brands)
**single vs multi**: pipeline-worthy
**entry**: awesome-design-md

### 编排执行

| Step | Skill | 触发原因 | 输出 |
|------|-------|---------|------|
| 1 | awesome-design-md | load Stripe DESIGN.md + Vercel DESIGN.md | both spec files |
| 2 | design-consultation | blend Stripe+Vercel aesthetics | hybrid spec |
| 3 | color-expert | harmonize Stripe purple + Vercel black/white | palette |
| 4 | design-tokens | compile tokens | tokens.css |
| 5 | design-html | Stripe typography + Vercel layout patterns | working docs |

### 关键决策

- **跳过 hallmark study**: 用户没贴截图,只是文字提到品牌
- **跳过 awwwards-design-intelligence**: 不是知名 site,要的是商业品牌
- **跳过 design-an-interface**: 用户说"same way"不是"different shapes",不需并行生成
- **插入 color-expert**: 多品牌融合时,颜色协调是核心瓶颈
- **风险**: 多品牌 mashup 可能违反 hallmark "structural variety" — Step 5 后必须追加 hallmark audit

### Anti-Slop Warning

这种 mashup 最容易出的问题:
- 抄了 Stripe 的 "shadow-card" 模式但用了 Vercel 的 "monochrome-gray" → 用户体验割裂
- awwwards check 提醒: hash-link anchors,代码块 visual noise

### 耗时

- 手工: 4-8 小时 (要猜 hybrid 在哪)
- Orchestrator: 25-35 分钟
- **compression**: ~10-15x

---

## 三个案例的 meta-pattern

1. **总是从 path detection 出发**, 不要绕过决策表硬塞 skill 链
2. **永远是 3-6 step**, 超 10 step 必有冗余
3. **最后一步总是 anti-slop gate** (hallmark audit), 不能跳
4. **insertion 是常态** — color-expert / accessibility-review 经常被插入到主路径里
5. **用户的"Don't X" 是 hard constraint** — 立刻 skip 触发它的 skill
