# Anthropic Financial Services Skills

> 从 Anthropic 官方 financial-services 项目提取并转换为 UltraSkills 格式

**原项目**: https://github.com/anthropics/financial-services
**Stars**: 17.8k⭐
**License**: Apache-2.0
**Last Synced**: 2026-05-08

---

## 转换说明

- **原始格式**: Claude Code Plugin
- **转换格式**: UltraSkills (YAML frontmatter)
- **转换内容**: 55 skills
- **排除内容**: MCP 连接器配置、Agents 配置、Managed Agent 模板

---

## Skills 分类

### Financial Analysis（金融分析核心）
- comps-analysis - 可比公司分析
- dcf-model - DCF 估值模型
- lbo-model - LBO 杠杆收购模型
- 3-statement-model - 三表财务模型
- audit-xls - Excel 模型审计
- competitive-analysis - 竞争分析
- ... 共13个

### Investment Banking（投资银行）
- cim-builder - CIM 文档构建
- teaser - 匿名公司简介
- buyer-list - 买方名单生成
- merger-model - 并购分析模型
- pitch-deck - 融资路演PPT
- ... 共9个

### Private Equity（私募股权）
- deal-sourcing - 交易采购
- dd-checklist - 尽调清单
- ic-memo - 投委会备忘录
- unit-economics - 单位经济学
- portfolio-monitoring - 投后监控
- ai-readiness - AI 就绪度评估
- ... 共10个

### Equity Research（股权研究）
- earnings-analysis - 财报分析
- initiating-coverage - 覆盖启动报告
- model-update - 模型更新
- sector-overview - 行业概览
- ... 共9个

### Wealth Management（财富管理）
- financial-plan - 财务规划
- portfolio-rebalance - 组合再平衡
- tax-loss-harvesting - 税损收割
- ... 共6个

### Fund Admin（基金管理）
- gl-reconciler - 总账对账
- month-end-closer - 月结
- valuation-reviewer - 估值审核
- ... 共6个

### Operations（运营合规）
- kyc-screener - KYC 筛查
- ... 共2个

---

## 使用说明

### 前置条件

大部分 skills 设计为与 MCP 数据连接器配合使用（Daloopa/FactSet/Morningstar等）。

**无MCP环境**下的使用方式：
1. 手动提供数据（CSV/Excel文件）
2. 使用公开数据源（Yahoo Finance/SEC EDGAR）
3. 聚焦方法论学习（不依赖实时数据）

### 触发示例

```
"帮我做个可比公司分析"          → comps-analysis
"DCF估值这个公司"               → dcf-model
"分析这份财报"                  → earnings-analysis
"写个投委会备忘录"              → ic-memo
"评估客户的单位经济学"          → unit-economics
```

---

## 与 UltraSkills 既有内容对比

| 类别 | Anthropic Financial | UltraSkills 既有 | 重叠度 |
|------|---------------------|------------------|--------|
| 金融建模 | 13 skills | 0 | 0% |
| 投行/PE | 19 skills | 0 | 0% |
| 股权研究 | 9 skills | 0 | 0% |
| 财富管理 | 6 skills | 0 | 0% |
| 会计/合规 | 8 skills | 0 | 0% |

**结论**: 完全填补空白，0重叠。

---

## 维护

- **上游同步**: 每月检查 anthropics/financial-services 更新
- **本地改进**: 可基于用户反馈调整（不影响上游）
- **Arena 评测**: 每次同步后重跑

---

**Converted**: 55 skills
**Failed**: 0 skills
**Conversion Date**: 2026-05-08
