---
name: motion-design
description: Web 微交互/动效模式库：何时用动画、用什么 (Framer Motion / Web Animations API / CSS transitions / GSAP)、easing 怎么选、duration 多长、prefers-reduced-motion 怎么处理。包含 12 种常用模式起手代码。Trigger on motion / 动效 / 微交互 / animation / framer motion / transitions / interaction design。
version: 1.0.0
created_at: 2026-04-28
entry_point: scripts/snippet.sh
dependencies: []
tags: [motion, animation, ui, design, framer-motion, gsap, microinteraction, community]
---

# motion-design

动效不是装饰——是**反馈**和**叙事**。这个 skill 给原则 + 12 种常用模式代码。

## 何时用动效（5 个目的）

1. **反馈** — 点击/拖拽/加载有响应
2. **方向** — 进出场告诉用户元素去哪了
3. **关系** — 元素之间的因果（点这里→展开那里）
4. **品牌** — 弹性/刚硬/优雅的表达
5. **吸引注意** — 谨慎用，过度即骚扰

不要用动效：纯装饰的循环、看不出意图的 fancy 转场、>500ms 阻塞用户的过场。

## 库选型

| 场景 | 推荐 |
|---|---|
| React，复杂交互 | **Framer Motion** ⭐ |
| 极简 / 无依赖 | **CSS transitions** + Web Animations API |
| 复杂 timeline / SVG 路径 | **GSAP** |
| 滚动驱动 | scroll-timeline (CSS) / Framer `useScroll` |
| Lottie 矢量动画 | `lottie-web` / `dotlottie` |
| Vue | `@vueuse/motion` |

## 时长 (duration) 速查

| 元素 | 时长 | 说明 |
|---|---|---|
| 微交互 (hover/focus) | 100–150ms | 即时感 |
| 元素状态切换 | 200–300ms | 默认 |
| 进出场 (modal/toast) | 250–400ms | 可感知 |
| 页面/路由切换 | 400–600ms | 别太长 |
| 装饰循环 | 1500ms+ | 慢 |

> 大动作（位移大）→ 时长加；小动作（hover）→ 时长减。

## Easing 速查

| 用途 | 函数 |
|---|---|
| **进场** (落入) | `ease-out` / `cubic-bezier(0,0,0.2,1)` (Material) |
| **出场** (淡出) | `ease-in` / `cubic-bezier(0.4,0,1,1)` |
| **双向** (拖动归位) | `ease-in-out` / spring |
| **弹性** | spring `{stiffness: 300, damping: 30}` |
| **线性** (loading) | `linear` |

> 永远不用 `ease`（默认 ease-in-out）做进场——感觉慢启动。

## a11y 必做

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Framer Motion: `<MotionConfig reducedMotion="user">` 或读 `useReducedMotion()`。

## 12 种常用模式

```bash
bash scripts/snippet.sh list                    # 看全部
bash scripts/snippet.sh fade-in --lib framer    # 单个
bash scripts/snippet.sh modal --lib framer
bash scripts/snippet.sh skeleton --lib css
```

模式：`fade-in` `slide-up` `scale-in` `modal` `drawer` `toast` `accordion` `skeleton` `shake` `confetti` `magnetic-button` `stagger-list`

## 反模式

- ❌ duration > 600ms 的频繁交互
- ❌ 纯装饰的无限循环（除非 loading）
- ❌ 动 6 个元素同时进场（错峰 stagger 50ms）
- ❌ 不做 reduced-motion 适配
- ❌ 用 `width/height/top/left` 动画（用 `transform` + `opacity`，GPU 加速）
- ❌ 弹太久的 spring（damping 调高）

## License: MIT
