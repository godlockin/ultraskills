---
name: icon-system
description: 一站式图标方案：从 100k+ 开源图标库 (Iconify / Lucide / Heroicons / Phosphor / Tabler) 搜图标 → 拉 SVG → 生成 React/Vue 组件 / sprite / icon-font。包含命名规范、size grid、stroke 一致性检查。Trigger on icon / 图标 / svg icon / heroicons / lucide / iconify / icon library / 图标库。
version: 1.0.0
created_at: 2026-04-28
entry_point: scripts/icon.sh
dependencies: ["curl", "node>=18 (optional, for component gen)"]
tags: [icon, svg, design, ui, design-system, lucide, heroicons, iconify, community]
---

# icon-system

设计师/前端常见痛点：图标到处找、风格混乱、尺寸不齐、tree-shaking 不动。这个 skill 给方案。

## 推荐图标库

| 库 | 数量 | 风格 | License | 特色 |
|---|---|---|---|---|
| **Lucide** | ~1500 | outline 24px stroke | ISC | Feather 后继者，精修 |
| **Heroicons** | ~300 | outline / solid | MIT | Tailwind 团队官方 |
| **Phosphor** | ~9000 | thin/light/regular/bold/fill/duotone 6 风格 | MIT | 风格一致 |
| **Tabler** | ~5800 | outline 24 stroke | MIT | 极全，新出快 |
| **Iconify** | **220k+** | 聚合 200+ 套 | 各源 license | 终极搜索 |
| Material Symbols | ~3500 | Google MD3 | Apache 2.0 | Android/Web 标 |
| Bootstrap Icons | ~2000 | mixed | MIT | Bootstrap 系 |

**默认推荐：Lucide**（小巧 + 漂亮 + tree-shake 友好）。
**找不到？查 Iconify**（一站式，全宇宙 22 万图标）。

## Quick Start

```bash
# 搜图标（Iconify API，220k 全库）
bash scripts/icon.sh search "user heart"

# 拉一个 SVG
bash scripts/icon.sh fetch lucide:heart -o heart.svg

# 拉一组 → 生成 React 组件 (TS)
bash scripts/icon.sh batch lucide:heart,lucide:user,lucide:settings \
     --out src/icons/ --format react-tsx

# 整套库 → sprite (一个 svg 文件)
bash scripts/icon.sh sprite lucide --names heart,user,settings -o sprite.svg
```

## 设计系统规范

- **统一 stroke**：1.5–2px outline；solid 不混用
- **统一 grid**：24×24（工具栏）/ 20×20（按钮）/ 16×16（行内）
- **命名**：`Icon<Name>`，无歧义（`<TrashIcon>` 不要 `<DelIcon>`）
- **a11y**：装饰性图标加 `aria-hidden="true"`；功能图标加 `<title>` + `aria-label`
- **颜色**：用 `currentColor` 让 fill/stroke 跟文字色

## 与设计 token 集成

```bash
# 同步 stroke/size 到 design-tokens
echo '{"icon": {"size": {"sm":16,"md":20,"lg":24}, "stroke": 1.5}}' \
  > tokens/icon.json
# 然后 design-tokens skill 会发布到 tailwind / css vars
```

## 反模式

- ❌ 同页面混 outline + solid + duotone
- ❌ stroke 1px / 1.25px / 2px 乱用
- ❌ 把 emoji 当 icon（没法控色/对齐）
- ❌ icon font（用 SVG，可访问 + tree-shake）
- ❌ 自己画一套（除非 brand 必须）

## License: MIT
