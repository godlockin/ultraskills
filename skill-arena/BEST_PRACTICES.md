# UltraSkills Best Practices Guide

> **从 619 个 skills 的竞技场评测中提炼的最佳实践**

> **Based on**: Arena Report 2026-05-08

---

## Executive Summary

本指南从 **54 个类别 winners** 和 **Top 20 overall skills** 中提炼共性模式，指导新 skill 创建和既有 skill 改进。

## 卓越 Skills 的共性特征

### 文档结构模式

**发现**: Top 20 skills 平均拥有 **6.8 个 tags**

**推荐结构** (基于满分 skills: magazine-web-ppt, awesome-design-md):

```
skill-name/
├── SKILL.md              # 核心定义（含完整 frontmatter）
├── examples/             # 至少 2-3 个实战案例
│   ├── case-1.md
│   ├── case-2.md
│   └── screenshots/      # 可选：输出截图
├── references/           # 知识库/参考文档
│   ├── guide.md
│   └── api-reference.md
├── scripts/              # 可选：自动化脚本
│   └── helper.py
└── templates/            # 可选：代码/配置模板
    └── template.yaml
```

### Frontmatter 最佳实践

**示例** (参考 visual-forge, 9.5 分):

```yaml
---
name: visual-forge
description: Professional presentation and web design system combining brand precision (68+ design systems), narrative structure, and 30+ visual styles
version: 1.0.0
tags: [design, presentation, web, ui, ppt, slides, landing-page, infographic, visual-design]
---
```

**关键点**:
1. **name**: kebab-case，简洁有辨识度
2. **description**: 具体量化（"68+ design systems"），避免泛泛（"帮助设计"）
3. **version**: 语义化版本号（x.y.z）
4. **tags**: 3-9 个，覆盖功能域 + 应用场景 + 输出类型

### Description 写作公式

**高分模式** (分析 Top 10):

```
[核心功能] + [关键数字/特性] + [差异化价值]
```

**对比**:

| ❌ 低分描述 | ✅ 高分描述 |
|------------|------------|
| "帮助用户生成PPT" | "Professional presentation system combining 68+ brand systems, narrative structure, 30+ visual styles" |
| "提供设计建议" | "UI/UX review tool with heuristic analysis, WCAG compliance check, and actionable recommendations" |
| "分析代码" | "AST-based code quality analyzer detecting 15+ anti-patterns with auto-fix suggestions" |

## 按类别的最佳实践

### 内容创作类 (Content Skills)

**代表**: 7 winners (magazine-web-ppt, awesome-design-md, remotion...)

**模式**:
- ✅ 提供模板/示例（templates/, examples/）
- ✅ 明确输出格式（HTML/Markdown/PDF/PNG）
- ✅ 包含风格/主题参考库（references/）
- ✅ 自动化脚本（scripts/ 用于转换/渲染）

**示例结构** (visual-forge):
```
visual-forge/
├── references/
│   ├── brand-systems.md      # 68+ 品牌设计系统
│   ├── visual-styles.md       # 30+ 视觉风格
│   └── infographic-layouts.md # 21 种布局
├── templates/
│   └── narrative-arcs/
│       └── pitch-deck.md      # 融资PPT模板
└── examples/                  # 实战案例
```

### 工程类 (Engineering Skills)

**代表**: 15 winners (design-an-interface, chinese-text-analysis, triage-issue...)

**模式**:
- ✅ 提供检查清单（checklists）
- ✅ 代码示例（examples/ 含多语言）
- ✅ 工具脚本（scripts/ 自动化检测）
- ✅ 最佳实践参考（references/ 含反模式）

### Agent 类 (Agent Skills)

**代表**: 8 winners (multi-agent-patterns, context-compression, planning-with-files...)

**模式**:
- ✅ 明确工作流步骤（numbered steps）
- ✅ 状态机/流程图（diagrams）
- ✅ 错误处理策略（fallback logic）
- ✅ 性能基准（benchmarks/）

### 商业类 (Business Skills)

**代表**: 7 winners (learn-from-loss, chief-of-staff...)

**模式**:
- ✅ 提供决策框架（decision trees）
- ✅ 模板文档（templates/ 报告/邮件/PPT）
- ✅ 行业案例（examples/ 匿名化真实案例）
- ✅ 指标定义（metrics references）

## Tags 策略

**Top 20 skills 高频 tags**:

- `community` (16 次)
- `design` (6 次)
- `presentation` (3 次)
- `ui` (3 次)
- `claude` (3 次)
- `ppt` (2 次)
- `slides` (2 次)
- `review` (2 次)
- `competition` (2 次)
- `landing-page` (2 次)
- `architecture` (2 次)
- `ddd` (2 次)
- `arena-winner` (2 次)
- `github` (2 次)
- `ux` (2 次)

**推荐 Tags 组合**:

```
tags: [
  # 功能域 (1-2个)
  "design", "engineering", "business", "agent", "content", "marketing",
  
  # 应用场景 (2-3个)
  "presentation", "code-quality", "testing", "architecture", "workflow",
  
  # 输出类型 (1-2个)
  "html", "pdf", "report", "code", "diagram"
]
```

## 常见陷阱 (从低分 skills 学习)

**分析**: 4 skills 得分 < 4.0

**反模式**:

### ❌ 泛泛而谈
```yaml
description: "帮助用户完成任务"
# 问题：什么任务？如何帮助？输出什么？
```

**修正**:
```yaml
description: "Automated task breakdown tool generating GitHub issues from high-level goals with acceptance criteria"
```

### ❌ 缺少示例
仅有 SKILL.md，无 examples/ 或 references/

**修正**: 至少添加 1-2 个 markdown 示例到 `examples/`

### ❌ Tags 混乱
```yaml
tags: [helper, tool, useful, skill]
# 问题：tags 无意义，无法聚类
```

**修正**: 使用标准词汇，参考 Top 20 高频 tags

### ❌ 版本缺失
无 `version` 字段 → 可维护性 -3 分

**修正**: 添加 `version: 1.0.0`（初版）

## 改进路线图

### 从 C-Tier (6-7分) 升级到 A-Tier (8-9分)

**步骤**:
1. ✅ 补全 frontmatter（version + tags）
2. ✅ 添加 2-3 个 examples/
3. ✅ 重写 description（使用高分公式）
4. ✅ 添加 references/ 或 scripts/
5. ✅ 明确触发条件和输出格式

**预期提升**: +2-3 分

### 从 A-Tier (8-9分) 冲刺 S-Tier (9-10分)

**关键**:
- 🔥 **差异化**: 与同类 skills 明显区别（功能/方法/输出）
- 🔥 **量化**: description 中加数字（"68+ systems", "30+ styles"）
- 🔥 **完整性**: examples + references + scripts 三者齐全
- 🔥 **可维护性**: 清晰的目录结构 + 版本控制 + 依赖说明

**参考**: visual-forge (9.5), magazine-web-ppt (10.0)

## 新 Skill 创建检查清单

**Pre-launch**:

- [ ] Frontmatter 四要素齐全（name/description/version/tags）
- [ ] Description 使用高分公式（功能+数字+差异化）
- [ ] Tags 3-9 个，覆盖功能域+场景+输出
- [ ] examples/ 至少 2 个实战案例
- [ ] references/ 或 scripts/ 至少一个存在
- [ ] 明确触发条件（"When to use"）
- [ ] 明确输出格式（"Expected output"）
- [ ] 与同类 skills 差异化明显

**Post-launch**:

- [ ] 运行 arena pipeline 获得评分
- [ ] 若 < 7.0，按改进路线图优化
- [ ] 收集用户反馈，迭代 version

## 案例研究

### 📚 Case 1: visual-forge (9.5/10)

**成功要素**:
- 文档质量: 10/10（完整 frontmatter + 3 references + 1 template + README）
- 功能明确性: 9/10（4阶段工作流 + 3类输出格式 + 68+30+21 量化）
- 可维护性: 9/10（清晰目录结构 + 版本1.0.0 + 9个tags）

**可学习点**:
1. 量化具体化（"68+ brand systems"）
2. 多层级 references/（brand-systems.md, visual-styles.md, layouts.md）
3. 模板化输出（templates/narrative-arcs/）

### 📚 Case 2: magazine-web-ppt (10.0/10)

**成功要素**:
- 文档质量: 10/10（完美 frontmatter + 丰富 examples + scripts）
- 功能明确性: 10/10（明确 HTML→PPTX 流程 + 主题系统）
- 可维护性: 10/10（模块化脚本 + 版本控制 + 标准 tags）

**可学习点**:
1. 自动化脚本完整（scripts/ 含转换工具）
2. 主题系统可扩展（theme/）
3. 输出格式多样（HTML/PPTX/PDF）

---

## 总结

**高分 Skill 的公式**:

```
完整 Frontmatter (10分)
+ 具体化 Description (量化+差异化)
+ 丰富 Examples (2-3个实战)
+ 知识库 References/Scripts
+ 清晰触发条件和输出
────────────────────────────
= S-Tier Skill (9.0+)
```

**持续改进**:
- 每月重跑 arena 评测
- 参考同类 winner 优化
- 收集用户反馈迭代

---

*本指南基于 619 skills 的竞技场数据生成，持续更新中*
