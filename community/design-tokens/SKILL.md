---
name: design-tokens
description: 一套 tokens → 全栈输出 (CSS vars / Tailwind / SCSS / iOS Swift / Android XML / Flutter / JSON)。基于 W3C Design Tokens Community Group (DTCG) 标准格式。集成 Style Dictionary 或自带轻量构建器。多主题 (light/dark/brand)、$type 严格、引用解析。Trigger on design tokens / 设计token / style dictionary / theme / 主题 / dark mode / DTCG / token。
version: 1.0.0
created_at: 2026-04-28
entry_point: scripts/build.py
dependencies: ["python>=3.9", "optional: style-dictionary (npm)"]
tags: [design-tokens, dtcg, style-dictionary, theming, css, tailwind, design, community]
---

# design-tokens

**一套源 → 多端发布**。颜色/字号/圆角/阴影/间距集中管理，改一处全栈生效。

## 标准：W3C DTCG 格式

```json
{
  "color": {
    "brand": {
      "primary":   { "$value": "#0ea5e9", "$type": "color" },
      "secondary": { "$value": "{color.brand.primary}", "$type": "color" }
    }
  },
  "spacing": {
    "sm": { "$value": "8px", "$type": "dimension" }
  }
}
```

`$value` / `$type` / `$description` 是 DTCG 关键字。引用语法 `{path.to.token}`。

## 推荐 token 类别（最小集）

| 类别 | 例 |
|---|---|
| color | brand, neutral, semantic (success/warn/error/info), surface |
| typography | font-family, weight (300-900), size (xs-5xl), line-height, letter-spacing |
| spacing | xs/sm/md/lg/xl (4/8/16/24/32) |
| radius | none/sm/md/lg/full |
| shadow | sm/md/lg/xl |
| z-index | base/dropdown/modal/toast (10/100/1000/9999) |
| breakpoint | sm/md/lg/xl/2xl |
| motion | duration-fast/base/slow, easing-out/in/inout |

## Quick Start

```bash
# 1) 写源 token (DTCG json)
cat > tokens/base.json <<EOF
{
  "color": {
    "brand": { "primary": {"$value":"#0ea5e9","$type":"color"} },
    "neutral": {
      "0":   {"$value":"#ffffff","$type":"color"},
      "900": {"$value":"#0f172a","$type":"color"}
    }
  }
}
EOF

# 2) 主题覆写
cat > tokens/dark.json <<EOF
{ "color": { "neutral": {
  "0":   {"$value":"#0f172a","$type":"color"},
  "900": {"$value":"#ffffff","$type":"color"}
}}}
EOF

# 3) 构建多端
python3 scripts/build.py tokens/ -o dist/ --formats css,tailwind,scss,json

# 输出：
#  dist/tokens.css        (--color-brand-primary: #0ea5e9;)
#  dist/tailwind.config.js
#  dist/_tokens.scss
#  dist/tokens.json
```

## 多主题（light/dark/brand）

```bash
python3 scripts/build.py tokens/ -o dist/ \
  --themes light=base.json,dark=base.json+dark.json,brand-x=base.json+brand-x.json \
  --format css
```

输出：
```css
:root, [data-theme="light"] { --color-brand-primary: #0ea5e9; ... }
[data-theme="dark"]         { --color-neutral-0: #0f172a; ... }
[data-theme="brand-x"]      { ... }
```

## Style Dictionary 集成（可选）

如果你的团队已经用 Style Dictionary：

```bash
# 安装
npm i -D style-dictionary

# 用本 skill 的源 → SD config
bash scripts/to-style-dictionary.sh tokens/ > sd.config.json
npx style-dictionary build --config sd.config.json
```

## 反模式

- ❌ token 命名带 hex/rgb (`color-blue-500-rgb` → 改色就失效)
- ❌ semantic token 引用具体颜色：`button-bg: #0ea5e9` → 改 `button-bg: {color.brand.primary}`
- ❌ token 命名按设计师习惯（"那个蓝"）→ 用 ramp `blue-500`
- ❌ 一个 token 只用一次（合并）；一个值复用 5 处（拆出来）
- ❌ 在代码里写 magic value（写了就要 lint 报错）

## 与其他 skill 组合

```bash
# icon-system: 给 icon size/stroke 加进来
# poster-print-design: render 时注入 brand token
# motion-design: duration/easing 用 token 引用
```

## License: MIT
