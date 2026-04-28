---
name: information-architecture
description: 信息架构 (IA) 工具集：sitemap 生成、用户流 (user flow) 设计、卡片分类 (card sorting) 方法论、navigation pattern 选型 (tab / sidebar / breadcrumb / mega-menu)、URL 命名规范、内容审计 (content audit)。Trigger on IA / sitemap / 信息架构 / user flow / 用户流 / navigation / 导航 / 网站地图 / card sorting。
version: 1.0.0
created_at: 2026-04-28
entry_point: scripts/sitemap.py
dependencies: ["python>=3.9"]
tags: [ia, information-architecture, sitemap, ux, navigation, design, community]
---

# information-architecture

设计师/产品经理常需要：定网站结构、画 user flow、起 URL。这个 skill 给方法 + 工具。

## 何时用

- 新产品 → 定 sitemap + 主导航
- 老产品 → content audit 找冗余/孤岛
- 复杂功能 → 画 user flow
- 重命名 → 卡片分类用户测试

## 工作流（5 步）

```
1. 列内容清单 (inventory)        ← scripts/audit.py
2. 卡片分类 (card sort)          ← 用户研究
3. 画 sitemap                    ← scripts/sitemap.py
4. 画 user flow (任务级)         ← mermaid
5. 选 navigation pattern        ← 看下表
```

## Navigation Pattern 选型

| 信息量 | 层级 | 推荐 |
|---|---|---|
| 少 (<10) | 1 层 | top tabs / segmented |
| 中 (10–30) | 2 层 | top nav + dropdown |
| 大 (30–100) | 2–3 层 | sidebar |
| 超大 (>100) | 3+ 层 | sidebar + search + breadcrumb |
| 电商 (千 SKU) | flat + facet | mega menu + filter |
| 移动端 | 任意 | bottom tab (≤5) + drawer |

通用规则：
- ≤7 项放一级（米勒法则）
- 第三层尽量避免（用 search 替代深层导航）
- breadcrumb 一定要可点
- 当前位置高亮

## URL 规范

- 全小写 + 连字符：`/blog/how-to-x`，不要 `/Blog/HowToX` 或 `/blog_post`
- 名词复数（资源）：`/users`, `/posts`
- 动词谨慎用（API 用，UI 不用）：✅ `/settings`，❌ `/edit-settings`
- 短优先：`/u/123` > `/profile/user/123`
- 别带技术前缀：`/v2/api/...` 是 API 的事，UI 别露
- 多语言：`/zh/blog/...` 而非 `/blog/?lang=zh`
- SEO：日期不要嵌 URL（除非是新闻），用 slug

## Quick Start

```bash
# 用 YAML 定义 → 出 sitemap.json + mermaid 图
bash scripts/sitemap.py site.yaml -o sitemap.json --mermaid

# 内容审计：扫现有站，列 URL + 标题 + 字数
python3 scripts/audit.py https://example.com --depth 2 -o audit.csv

# user flow：定起点 → 终点 + 步骤 → mermaid
python3 scripts/user-flow.py "checkout" --steps cart,address,pay,confirm
```

site.yaml 示例：
```yaml
title: "MyApp"
nav:
  - label: Home
    path: /
  - label: Products
    path: /products
    children:
      - { label: All, path: /products }
      - { label: New, path: /products/new }
  - label: Blog
    path: /blog
  - label: About
    path: /about
```

## Mermaid 出图

sitemap → mermaid `graph TD`：
```
graph TD
  Home[Home /] --> Products[Products /products]
  Products --> All[All /products]
  Products --> New[New /products/new]
  Home --> Blog[Blog /blog]
  Home --> About[About /about]
```

User flow → mermaid `flowchart LR`：
```
flowchart LR
  Cart --> Address --> Pay --> Confirm
  Pay -- fail --> Pay
```

## 反模式

- ❌ 一级 >7 项（拆成 2 层）
- ❌ 隐藏关键功能在三级
- ❌ 「关于我们」做成首页主导航第一个
- ❌ 用 hover 做唯一打开方式（移动端死）
- ❌ URL 含 query string 当主路径 (`?page=about`)
- ❌ 重命名后不做 301

## License: MIT
