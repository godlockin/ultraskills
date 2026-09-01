---
name: marketing-roi-calculator
description: Marketing ROI calculator - calculates CAC, LTV, payback, attribution across channels in 20min. Use when user wants to "算 CAC", "看哪个渠道投入产出高", "营销月报", "老板问投入产出比", "ROI review", "channel attribution", "campaign analysis", "marketing budget allocation", "看下个月预算怎么分", "广告费没效果", "SEO 还是 SEM", "看每条渠道 ROI", "看获客成本", "LTV 是多少", "payback period", "marketing ops", "marketing metrics". Frequency: monthly + per campaign.
version: 2.0.0
tags: [marketing, roi-analysis, cac, ltv, attribution, marketing-ops, ROI-8.5, community, arena-winner]
---

# Marketing ROI Calculator

**ROI:** 8.5/10 - Saves 4h → 20min for monthly marketing analysis

Systematic marketing ROI framework covering CAC, LTV, channel attribution, and campaign effectiveness. Turns spreadsheet chaos into executive-ready insights.

---

## 🎯 适用场景与触发

### 6 类典型场景

| # | 场景 | 触发词 |
|---|---|---|
| 1 | **月度营销复盘** | 营销月报 / 月度 ROI / monthly reporting |
| 2 | **预算分配** | 下个月预算怎么分 / budget allocation / 把预算挪给哪条渠道 |
| 3 | **渠道优化** | 看哪个渠道投入产出高 / channel optimization / SEO 还是 SEM |
| 4 | **Campaign 复盘** | 这次 campaign 值不值 / campaign analysis |
| 5 | **老板汇报** | 老板问投入产出比 / board decks / investor metrics |
| 6 | **LTV 健康度** | LTV 是多少 / payback period / 投资回收期 |

### 5 类常见痛点

- **数据散落** — 多个平台各自有数据,没法整合
- **算不出 CAC** — 不知道把销售成本放哪
- **不知道对不对** — 算出来但不确定数字是否合理
- **拆不到渠道** — 总 CAC 知道,但分不出每条渠道
- **看不到回收期** — 不知道几个月回本

### 6 类期望效果

- CAC + LTV + Payback 三件套(分渠道 + 分产品)
- 行业 benchmark 对比(自动提醒偏离)
- Attribution 模型选择(首次/末次/线性)
- 行动建议(加预算 / 砍渠道 / 重分配)
- Executive 1 页纸(可视化 + Insight)
- 季度 trend(同比环比)

---

## 🚨 边界

| 类型 | 触发 | 动作 |
|---|---|---|
| **品牌广告** | 用户问「品牌曝光 ROI」 | 短期不接(品牌曝光非 attribution 友好),建议改问「品牌 recall」 |
| **纯自然流量** | 用户问「SEO 多少 ROI」 | 可算但口径需明示(SEO 长期归因,不要混在月度报表) |
| **B2B 大单销售** | 用户问「单笔 100 万合同的 ROI」 | 转 strategy-consulting-framework(决策级,非营销级) |

---

## 📥 启动前信息收集

| 信息 | 必要性 | 缺失时默认 |
|---|---|---|
| **渠道列表 + 各渠道 spend** | 必须 | 不开始,问 |
| **新客数**(同期) | 必须 | 不开始,问 |
| **收入数据**(ARPA / LTV) | 强烈推荐 | 用行业默认,后续提醒 |
| **产品类型**(SaaS / 电商 / App) | 强烈推荐 | 假设 SaaS B2B |
| **Cohort 数据**(若算 payback) | 推荐 | 不假设 |

---

## 🔗 后续落地动作

| 动作 | 触发 | 默认 |
|---|---|---|
| **预算调整建议** | 计算完成后 | 主动建议「要不要给具体预算调整建议?」 |
| **A/B 测试联动** | 渠道 ROI 差异大 | 主动建议「要不要给那条高 ROI 渠道跑 A/B test?」 |
| **季度 trend** | 累计 3 次使用 | 主动建议「要不要做同比环比趋势图?」 |
| **行业 benchmark 对比** | 数字算出后 | 主动对比行业基准,标偏离 |

---

## 🔁 人机迭代闭环

### 主公 → skill 反馈通道

| 反馈 | skill 动作 |
|---|---|
| 「CAC 算错」 | 询问「分子包含哪些项?」回到原始口径 |
| 「数字不对」 | 检查 attribution 模型 + 时间窗(7/14/30 天) |
| 「拆不到渠道」 | 检查 utm 标记 + 数据管道 |
| 「benchmark 偏离大」 | 询问业务阶段(早期 vs 成熟)调整 |

### skill → 主公主动迭代

| 周期 | 内容 |
|---|---|
| 每月 | 「本月 Top 3 渠道 + Bottom 3 渠道 + 建议动作」 |
| 季度 | 「本季度 CAC trend + LTV:CAC 趋势」 |
| 半年 | 「Attribution 模型是否需要切换(首次→末次→线性)?」 |
| 一年 | 「CAC 偏离行业基准的复盘 + 修正建议」 |

---

## 🛠 自检 Checklist

- [ ] CAC 口径明示(分子包含哪些项)?
- [ ] LTV 计算口径合理(月费 / 毛利 / 流失周期)?
- [ ] 渠道细分(至少分 3-5 条渠道)?
- [ ] 产品/客群细分(B2B / SMB / Enterprise)?
- [ ] 时间窗明示(7/14/30 天)?
- [ ] Attribution 模型选定?
- [ ] 行业 benchmark 对比?
- [ ] 1 页纸 executive summary 有建议?

---

- **Monthly reporting**: Executive marketing performance review
- **Budget planning**: Allocate next quarter's spend
- **Channel optimization**: Double down or cut underperformers
- **Campaign analysis**: Post-mortem on what worked
- **Board decks**: Investor-grade metrics

**Frequency:** Monthly analysis + per-campaign review

---

## Core Metrics Framework

### 1. CAC (Customer Acquisition Cost)

**Formula:** (Sales + Marketing spend) ÷ New customers

**Example:**
- Q1 spend: $50K marketing + $30K sales = $80K
- New customers: 40
- **CAC: $2,000**

**Benchmark:**
- SaaS B2B: $200-500 (SMB), $1K-5K (mid-market), $10K+ (enterprise)
- Ecommerce: $10-50
- Consumer app: $1-10

**Segmented CAC (required):**
- By channel (paid, organic, referral)
- By product tier (freemium, starter, pro, enterprise)
- By cohort (month acquired)

---

### 2. LTV (Lifetime Value)

**Formula (MUST keep units consistent):**

| 口径 | 公式 | 示例 |
|---|---|---|
| **月度** | `LTV = Monthly ARPA ÷ Monthly Churn Rate` | $500/月 ÷ 3% = $16,667 |
| **年度** | `LTV = Annual ARPA ÷ Annual Churn Rate` | $6,000/年 ÷ 36% = $16,667 |

> ⚠️ **量纲一致性**：ARPA 与 churn 必须是同一时间口径（月度对月度、年度对年度），否则 LTV 计算会差 10× 以上。脚本里必须显式校验两者时间单位一致。

**Alternative (for non-subscription):**
- LTV = Avg purchase × Purchase frequency × Customer lifespan
- Example: $100 purchase × 4 times/year × 3 years = $1,200

**Benchmark:** LTV:CAC ratio >3x (healthy), >5x (excellent)

---

### 3. Payback Period

**Naive formula (忽略流失，会低估):** `CAC ÷ Gross margin per month`

**Churn-adjusted formula (推荐):**
```
Effective Monthly Margin = MRR × Gross Margin × (1 − Monthly Churn)
Payback (months) = CAC ÷ Effective Monthly Margin
```

**Example (churn-adjusted):**
- CAC: $2,000
- MRR: $500
- Gross margin: 80%
- Monthly churn: 3%
- **Naive:** $2,000 ÷ ($500 × 0.8) = 5.0 months（低估）
- **Adjusted:** $2,000 ÷ ($500 × 0.8 × 0.97) = **5.15 months**
- Higher-churn sensitivity: 8% 月流失 → Effective margin = $368 → Payback ≈ 5.43 月

> 当月流失率 > 5% 时，naive 公式与 churn-adjusted 公式差距 ≥ 0.5 个月，必须使用 adjusted 版本以避免现金流风险。
- Ecommerce: <3 months

---

### 4. Channel ROI

**Formula:** (Revenue attributed - Spend) ÷ Spend

**Example (Paid Search):**
- Spend: $10K
- Revenue attributed: $50K
- **ROI: ($50K - $10K) ÷ $10K = 4x or 400%**

**Benchmark by channel:**
- Paid search: 2-4x
- Paid social: 1.5-3x
- Content marketing: 3-6x (longer payback)
- Referral: 5-10x (lowest CAC)

---

## Analysis Workflow

### Step 1: Gather Data

**Required inputs:**
- Marketing spend (by channel, monthly)
- Sales spend (salaries, commissions, tools)
- New customers (with attribution source)
- Revenue (by customer cohort)
- Churn rate (monthly or annual)

**Data sources:**
- Marketing platforms (Google Ads, Meta, LinkedIn)
- CRM (Salesforce, HubSpot)
- Analytics (GA4, Mixpanel)
- Finance (actual spend, not estimates)

---

### Step 2: Calculate Blended Metrics

**Blended CAC (all channels combined):**

| Month | Total Spend | New Customers | Blended CAC |
|-------|-------------|---------------|-------------|
| Jan | $45K | 30 | $1,500 |
| Feb | $52K | 35 | $1,486 |
| Mar | $60K | 50 | $1,200 |

**Trend:** CAC improving (efficiency gain)

---

### Step 3: Channel Attribution

**Last-touch attribution example:**

| Channel | Spend | Customers | CAC | Revenue | ROI |
|---------|-------|-----------|-----|---------|-----|
| Paid Search | $15K | 15 | $1,000 | $75K | 4.0x ✅ |
| Paid Social | $20K | 10 | $2,000 | $40K | 1.0x ⚠️ |
| Content SEO | $10K | 20 | $500 | $100K | 9.0x ✅✅ |
| Referral | $5K | 5 | $1,000 | $50K | 9.0x ✅✅ |

**Insights:**
- **Winner:** Content SEO ($500 CAC, 9x ROI)
- **At-risk:** Paid Social (2x CAC, breakeven ROI)
- **Action:** 2x content budget, cut paid social 50%

---

### Step 4: Cohort Analysis

**Q1 2026 cohort LTV tracking (illustrative):**

| Month | Customers | MRR | Churn | Cumulative Gross Margin |
|-------|-----------|-----|-------|--------------------------|
| Jan (M0) | 30 | $15,000 | 0% | $6,000 |
| Feb (M1) | 30 | $15,000 | 3% | $12,000 |
| Mar (M2) | 29 | $14,500 | 3% | $17,800 |
| Apr (M3) | 28 | $14,000 | 3% | $23,560 |

> **示例假设**：每个客户月初贡献当月 MRR；Cumulative Gross Margin = Σ(MRR × Gross Margin)。`Churn=0% at M0` 表示当月新签无即时流失；之后 3% 反映下月开始的 cohort-level 流失。客户数 = 30 × (1 − 0.03)^(n−1) 向上取整；MRR = Customer × ARPA（ARPA = $500/月）。实际数据若按日跟踪、按比例流失，请重做表格。

**Projection:** If 3% monthly churn holds, gross-margin LTV ≈ $500 × (1 − 0.80) × Σ(0.97^n) ≈ $16,667（与上方 LTV 公式一致）。

---

### Step 5: Attribution Models

**Multi-touch attribution (advanced):**

Customer journey: Organic search → Paid ad → Webinar → Demo → Purchase

| Model | Attribution Logic | Use Case |
|-------|-------------------|----------|
| **Last-touch** | 100% to demo | Quick, favors bottom-funnel |
| **First-touch** | 100% to organic | Top-of-funnel credit |
| **Linear** | 25% each touchpoint | Equal credit |
| **Time-decay** | More credit to recent | Favors closer-to-purchase |
| **Position-based** | 40% first, 40% last, 20% middle | Balanced |

**Best practice:** Use last-touch for ops, multi-touch for strategy

---

## Campaign Post-Mortem Template

**Campaign:** Q1 Product Launch - Paid LinkedIn

**Investment:**
- Ad spend: $25K
- Creative production: $5K
- Landing page: $2K (designer)
- **Total: $32K**

**Results:**
- Impressions: 500K
- Clicks: 10K (2% CTR)
- Leads (MQLs): 200 (2% conversion)
- SQLs: 80 (40% qual rate)
- Customers: 8 (10% close rate)
- Revenue: $40K (8 × $5K ARPU)

**Metrics:**
- **CAC:** $32K ÷ 8 = $4,000
- **Payback:** 10 months ($4K ÷ $400 monthly margin)
- **ROI:** ($40K - $32K) ÷ $32K = 0.25x (25%)

**Verdict:** ⚠️ **Underperformed**
- CAC too high ($4K vs $2K target)
- ROI below breakeven (<1x)

**Root cause:**
- CTR good (2%), conversion poor (2% → should be 5%)
- **Problem:** Landing page messaging mismatch

**Action:**
- A/B test 3 new landing pages
- Retarget 9,800 clicks (nurture with content)
- Don't scale spend until conversion >4%

---

## Dashboard Template

**Monthly Marketing Scorecard:**

```
┌─────────────────────────────────────────┐
│ BLENDED METRICS (All Channels)         │
├─────────────────────────────────────────┤
│ CAC:           $1,200  (-15% MoM) ✅   │
│ LTV:           $16,667 (stable)        │
│ LTV:CAC:       13.9x   (+18% MoM) ✅   │
│ Payback:       5 months                 │
│ New Customers: 50      (+25% MoM)      │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ CHANNEL PERFORMANCE                     │
├─────────────────────────────────────────┤
│ ✅ Content SEO   $500 CAC   9.0x ROI   │
│ ✅ Paid Search   $1K CAC    4.0x ROI   │
│ ✅ Referral      $1K CAC    9.0x ROI   │
│ ⚠️ Paid Social   $2K CAC    1.0x ROI   │
│ ❌ Events        $5K CAC    0.5x ROI   │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ ACTIONS                                 │
├─────────────────────────────────────────┤
│ 1. +100% content budget ($10K → $20K)  │
│ 2. -50% paid social ($20K → $10K)      │
│ 3. Pause events (CAC 2.5x target)      │
│ 4. Launch referral incentive program   │
└─────────────────────────────────────────┘
```

---

## Advanced Analysis

### Incrementality Testing

**Question:** "Does paid search cannibalize organic?"

**Method:** Geo-holdout test
- Turn off paid search in 50% of geos for 30 days
- Measure organic lift in holdout geos
- Compare total customers (paid + organic) vs control

**Example result (illustrative — not empirical evidence):**
- Control geos: 100 paid + 50 organic = 150 total
- Holdout geos: 0 paid + 70 organic = 70 total
- Apparent cannibalization: 20 organic customers seemed to come from paid
- **Incremental:** 80 customers truly incremental
- **True incremental CAC:** $15K spend ÷ 80 = **$188** (vs naive blended $15K ÷ 150 = $100, or "$150" cited in older versions)

> ⚠️ **必读**：
> - 30 天 geo-holdout 对 B2B 决策周期（90–180 天）可能不足；B2B 场景至少 90 天或基于历史 sales cycle 校准。
> - 必须做季节性调整（Q4 vs Q1 差异显著）与竞争者响应控制（对手可能趁机扩量）。
> - cannibalization 结论必须做统计显著性验证（p-value、CI），不能仅看差值。
> - 任何 MMM / incrementality 结论只能标注 `illustrative` 或 `internal benchmark`，不得作为对外承诺。

---

### Marketing Mix Modeling

**Question:** "What's optimal budget allocation?"

**Method:** Regression on historical spend × channel

**Example output:**
- Doubling content budget → +30% customers
- Doubling paid social → +5% customers (diminishing returns)
- **Optimal mix:** 60% content, 30% paid search, 10% referral

---

## Common Mistakes

### Mistake 1: Ignoring Attribution Window

**Problem:** Customer touches ad on Jan 1, purchases Feb 15
- If attribution window = 30 days, **no credit** to ad
- If attribution window = 60 days, **full credit** to ad

**Fix:** Use 90-day window for B2B, 30-day for B2C

---

### Mistake 2: Forgetting Fully-Loaded CAC

**Incomplete CAC:**
- Ad spend only: $1,000

**Fully-loaded CAC:**
- Ad spend: $1,000
- Marketing salaries (allocated): $300
- Tools (Marketo, analytics): $100
- Agency fees: $200
- **True CAC: $1,600**

---

### Mistake 3: LTV Optimism

**Rookie error:** Use projected LTV ($16K) vs actual ($8K after 18 months)

**Fix:** Use cohort-based LTV (actual revenue from 12-month-old cohort)

---

## ROI Optimization Playbook

### Playbook 1: Fix High-CAC Channel

**Trigger:** Channel CAC >2x blended CAC for 2 months

**Actions:**
1. **Pause immediately** (stop bleeding)
2. **Root cause:**
   - Targeting too broad? (narrow audience)
   - Creative fatigue? (refresh ads)
   - Landing page weak? (A/B test)
3. **Test fix** (small budget, 30 days)
4. **Scale or kill** (if CAC doesn't drop 30%, cut permanently)

---

### Playbook 2: Scale Winner

**Trigger:** Channel ROI >5x for 3 months

**Actions:**
1. **2x budget** (test scalability)
2. **Monitor for plateau** (diminishing returns)
3. **Expand variants:**
   - New creatives (same audience)
   - New audiences (same creative)
   - New platforms (same strategy)

---

## References

- Naas notebooks: Analyze_Marketing_ROI
- SaaS marketing benchmarks (OpenView, ProfitWell)
- Multi-touch attribution (Bizible, HubSpot)
