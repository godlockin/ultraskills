---
name: data-viz
description: 给数据自动选图表类型 + 输出代码（D3 / Recharts / ECharts / Observable Plot / Vega-Lite / matplotlib）。包含图表类型决策树（比较/分布/构成/关系/时序/地理）、配色规范、可访问性。Trigger on chart / dataviz / data visualization / 数据可视化 / 画图 / 图表 / plot / dashboard / 可视化。
version: 1.0.0
created_at: 2026-04-28
entry_point: scripts/recommend.py
dependencies: ["python>=3.9", "optional: pandas/matplotlib for inspect"]
tags: [data-viz, charts, d3, recharts, echarts, vega-lite, dashboard, design, community]
---

# data-viz

不会选图表类型？给数据 → 自动推荐 + 出代码。

## 决策树（看意图）

| 想表达 | 首选图表 | 第二选 |
|---|---|---|
| **比较类目** | 横/竖 bar | dot plot |
| **构成 (整体的部分)** | stacked bar / 100% bar | sunburst / treemap |
| **饼图？** | **不要**用饼图（>3 切片就难读）| 100% bar |
| **分布** | histogram | violin / box |
| **关系/相关** | scatter | hexbin (大数据)|
| **时序** | line | area (累积量)|
| **多变量时序** | small multiples | parallel coordinates |
| **排名/Top N** | sorted bar | bump chart |
| **流转 (A→B)** | sankey | chord |
| **地理** | choropleth | hex grid (避免人口偏差) |
| **网络** | force-directed graph | adjacency matrix |
| **不确定性** | error bars / confidence band | gradient/dotted |

## 库选型

| 场景 | 推荐 |
|---|---|
| React 仪表板，要快 | **Recharts** / Tremor |
| 一次性研究图，要美 | **Observable Plot** |
| 中文/复杂交互 (大屏) | **ECharts** |
| 完全自定义 | **D3** + visx |
| 声明式简洁 | **Vega-Lite** |
| Python 笔记 | matplotlib + seaborn / plotly |
| 静态 Markdown / PPT | Vega-Lite + svg 导出 |

## 配色规范

- **类别配色** ≤8 类：用 d3.schemeCategory10 / Tableau10 / Okabe-Ito (色盲友好)
- **顺序配色** (低→高)：viridis / cividis（色盲友好，避免彩虹色）
- **发散配色** (负←0→正)：RdBu / BrBG
- **永远** 标 colorbar / 图例 / 单位
- **永远** 检查 WCAG 对比度 ≥3:1（图与背景）

## Quick Start

```bash
# 输入数据样本 → 推荐图表 + 起始代码
echo '[{"x":1,"y":3},{"x":2,"y":7},{"x":3,"y":4}]' | \
  python3 scripts/recommend.py --intent trend --library recharts

# 指定 (类别×数值×维度数)
python3 scripts/recommend.py --rows 50 --x-type cat --y-type num --intent compare

# 配色生成
python3 scripts/palette.py --type sequential --n 9 --colorblind
```

## 反模式（不要做）

- ❌ 3D 饼图 / 3D 柱
- ❌ 双 Y 轴（除非 y2 是 y1 的衍生量）
- ❌ 默认彩虹/jet 色阶
- ❌ Y 轴不从 0 开始的 bar chart（line 可以）
- ❌ 类别多于 7 还用饼图
- ❌ 不标单位
- ❌ 删数据点为"清爽"（用 alpha/jitter/bin 代替）

## 与其他 skill 组合

```bash
# 1) autoresearch 出数据 → data-viz 出图
# 2) data-viz 给 recharts → 嵌入 nextjs-developer 的 dashboard
# 3) 出 svg → poster-print-design 排进海报
```

## License: MIT
