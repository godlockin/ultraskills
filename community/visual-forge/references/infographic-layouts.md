# Infographic Layouts Library

21 种信息图布局类型，每种包含适用场景、结构说明、代码模板。

## Quick Reference Table

| # | Layout Type | 适用场景 | 视觉特征 | 信息密度 |
|---|------------|---------|---------|---------|
| 1 | Timeline | 历史事件、产品路线图、流程步骤 | 横/竖时间轴、节点标注 | 中 |
| 2 | Comparison | 产品对比、Before/After、方案选择 | 左右对比、表格、色块区分 | 高 |
| 3 | Hierarchy | 组织架构、分类体系、决策树 | 金字塔、树状图、层级嵌套 | 中 |
| 4 | Flow | 用户旅程、业务流程、数据流 | 箭头连接、泳道图、流程图 | 中 |
| 5 | Data Story | 数据洞察、研究报告、趋势分析 | 图表主导、数字突出、配色分类 | 高 |
| 6 | Grid Mosaic | 多维度对比、产品矩阵、概念全景 | 九宫格、卡片阵列、图标+文字 | 高 |
| 7 | Radial | 中心主题扩散、关系网络、影响因素 | 圆形辐射、连线、中心节点突出 | 中 |
| 8 | Map | 地理分布、位置服务、全球化 | 地图底图、气泡标注、区域色块 | 中 |
| 9 | Process | 制造流程、服务步骤、方法论 | 编号步骤、箭头导向、阶段分区 | 中 |
| 10 | Statistical | 调研结果、市场数据、用户洞察 | 饼图/柱状图/折线图 + 解读文字 | 高 |
| 11 | List | 排名、清单、要点罗列 | 编号/图标 + 文字，上下堆叠 | 低-中 |
| 12 | Venn | 交集关系、共性对比、分类重叠 | 圆形交集、色彩半透明叠加 | 低 |
| 13 | Matrix | 优先级矩阵、四象限分析、定位图 | 2x2 或 3x3 网格、象限标签 | 中 |
| 14 | Funnel | 转化漏斗、销售流程、用户流失 | 倒三角、每层标注百分比/数量 | 中 |
| 15 | Mindmap | 头脑风暴、概念关联、知识图谱 | 树状分支、自由连线、色彩分类 | 中-高 |
| 16 | Storyboard | 用户故事、场景叙事、分镜脚本 | 连续画面、序号、简短旁白 | 中 |
| 17 | Icon Grid | 功能特性、优势列举、服务项目 | 图标阵列、简短文字、整齐排列 | 低-中 |
| 18 | Hero Number | 关键数据突出、单一指标强调 | 巨大数字、小字解释、单一焦点 | 低 |
| 19 | Circular | 循环流程、闭环系统、周期性 | 环形箭头、阶段标注、无明显起点 | 中 |
| 20 | Pyramid | 层次结构、需求层次、重要性排序 | 三角形分层、底层宽、顶层窄 | 中 |
| 21 | Waterfall | 级联效应、累积影响、阶梯递进 | 阶梯状、逐级叠加、流水形态 | 中-高 |

---

## Detailed Specifications

### 1. Timeline (时间线)

**适用场景**：公司历史、产品路线图、项目里程碑、事件回顾

**结构说明**：
- 主轴：水平或垂直时间线
- 节点：关键时间点，用圆点/图标标注
- 内容：每个节点附带日期 + 标题 + 简短描述
- 变体：横向（历史类）、竖向（移动端友好）

**HTML 模板**：
```html
<div class="timeline horizontal">
  <div class="timeline-item">
    <div class="date">2020</div>
    <div class="marker"></div>
    <div class="content">
      <h3>公司成立</h3>
      <p>3 位创始人在车库开始创业</p>
    </div>
  </div>
  <div class="timeline-item">
    <div class="date">2021</div>
    <div class="marker"></div>
    <div class="content">
      <h3>种子轮融资</h3>
      <p>获得 $2M 投资，团队扩展到 15 人</p>
    </div>
  </div>
  <!-- More items... -->
</div>
```

**CSS 模板**：
```css
.timeline.horizontal {
  display: flex;
  gap: var(--space-xl);
  position: relative;
}

.timeline.horizontal::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--color-border);
}

.timeline-item {
  text-align: center;
  position: relative;
}

.timeline-item .marker {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--color-primary);
  margin: 0 auto var(--space-sm);
}

.timeline-item .date {
  font-weight: 700;
  font-size: 18px;
  margin-bottom: var(--space-xs);
}
```

---

### 2. Comparison (对比)

**适用场景**：产品对比、方案优劣、Before/After、竞品分析

**结构说明**：
- 左右分屏：各占 50%，中间分隔线
- 表格形式：行列对比，勾叉标注
- 色块区分：不同选项用不同背景色

**HTML 模板**：
```html
<div class="comparison">
  <div class="compare-column left">
    <h2>免费版</h2>
    <ul class="feature-list">
      <li class="included">✓ 基础功能</li>
      <li class="included">✓ 5 个项目</li>
      <li class="excluded">✗ 高级分析</li>
      <li class="excluded">✗ 优先支持</li>
    </ul>
    <button class="btn-secondary">开始使用</button>
  </div>
  
  <div class="compare-divider"></div>
  
  <div class="compare-column right">
    <h2>专业版</h2>
    <ul class="feature-list">
      <li class="included">✓ 所有基础功能</li>
      <li class="included">✓ 无限项目</li>
      <li class="included">✓ 高级分析</li>
      <li class="included">✓ 优先支持</li>
    </ul>
    <button class="btn-primary">立即升级</button>
  </div>
</div>
```

---

### 5. Data Story (数据叙事)

**适用场景**：年度报告、市场研究、用户洞察、趋势分析

**结构说明**：
- 主图表：占据 60-70% 空间（折线图/柱状图/饼图）
- 数字突出：关键数据用大号字体、彩色高亮
- 解读文字：每个数据点附带简短洞察
- 配色：按类别/维度用不同颜色

**示例场景**：
```
[巨大数字] 74%
[小字] 的用户表示产品提升了工作效率

[折线图] 用户增长趋势 (2020-2026)
- 2020: 1K
- 2023: 50K ← 转折点：推出企业版
- 2026: 500K

[柱状图] 各行业用户占比
- 科技: 45% (蓝色)
- 金融: 25% (绿色)
- 教育: 20% (橙色)
- 其他: 10% (灰色)
```

---

### 6. Grid Mosaic (网格拼图)

**适用场景**：功能矩阵、产品线、多维度对比、概念全景

**结构说明**：
- 网格布局：2x2, 3x3, 4x4...
- 每格内容：图标 + 标题 + 简短描述
- 配色：按类别使用不同背景色或边框色

**HTML 模板**：
```html
<div class="grid-mosaic cols-3">
  <div class="grid-item">
    <div class="icon">🚀</div>
    <h3>快速部署</h3>
    <p>一键部署到全球 CDN</p>
  </div>
  
  <div class="grid-item">
    <div class="icon">🔒</div>
    <h3>安全可靠</h3>
    <p>企业级加密和备份</p>
  </div>
  
  <div class="grid-item">
    <div class="icon">📊</div>
    <h3>实时分析</h3>
    <p>深度洞察用户行为</p>
  </div>
  
  <!-- More items... -->
</div>
```

---

### 14. Funnel (漏斗)

**适用场景**：销售转化、用户流失、营销漏斗、招聘流程

**结构说明**：
- 倒三角：顶部最宽，逐层收窄
- 每层标注：阶段名称 + 数量 + 百分比
- 配色：渐变或单色，越往下越深

**示例**：
```
┌─────────────────────────────────┐
│  访问网站: 10,000 (100%)         │
├─────────────────────────────┐   │
│  注册账号: 2,000 (20%)       │   │
├─────────────────────────┐   │   │
│  试用产品: 500 (5%)       │   │   │
├─────────────────────┐   │   │   │
│  付费订阅: 100 (1%)   │   │   │   │
└─────────────────────┴───┴───┴───┘
```

---

## Layout Selection Logic

根据内容类型自动推荐布局：

| 内容特征 | 推荐布局 TOP 3 |
|---------|---------------|
| **时间相关**（历史、路线图） | Timeline, Process, Storyboard |
| **对比类**（产品/方案选择） | Comparison, Venn, Matrix |
| **层次关系**（组织/分类） | Hierarchy, Pyramid, Mindmap |
| **流程类**（步骤/旅程） | Flow, Process, Circular |
| **数据类**（数字/趋势） | Data Story, Statistical, Funnel |
| **多维度**（功能/特性） | Grid Mosaic, Icon Grid, List |
| **关系网络**（影响因素） | Radial, Mindmap, Venn |
| **地理分布** | Map, Grid Mosaic (with icons) |
| **单一焦点**（强调一个数据） | Hero Number, Pyramid (top layer) |

---

## Usage

1. **内容分析**：识别信息类型（时间/对比/层次/流程/数据...）
2. **布局匹配**：从 Selection Logic 表查找 TOP 3
3. **加载模板**：使用对应的 HTML/CSS 模板
4. **填充内容**：替换占位符为真实数据
5. **样式调整**：应用选定的品牌色 + 视觉风格

---

## Adding New Layouts

补充新布局需包含：

- [ ] 布局名称 (中英文)
- [ ] 适用场景 (3-5 个具体场景)
- [ ] 结构说明 (200 字以内)
- [ ] HTML 模板 (带注释)
- [ ] CSS 模板 (基于 CSS 变量)
- [ ] 示例截图或 ASCII 示意图

---

**Total Layouts**: 21  
**Last Updated**: 2026-05-08
