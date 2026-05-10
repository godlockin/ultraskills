---
name: marketing-roi-calculator
description: Marketing ROI calculator - calculates CAC, LTV, payback, attribution across channels in 20min
version: 1.0.0
tags: [marketing, roi-analysis, cac, ltv, attribution, marketing-ops, ROI-8.5]
---

# Marketing ROI Calculator

**ROI:** 8.5/10 - Saves 4h → 20min for monthly marketing analysis

Systematic marketing ROI framework covering CAC, LTV, channel attribution, and campaign effectiveness. Turns spreadsheet chaos into executive-ready insights.

---

## When to Use

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

**Formula:** ARPA ÷ Churn rate

**Example:**
- ARPA (Average Revenue Per Account): $500/month
- Monthly churn: 3%
- **LTV: $500 ÷ 0.03 = $16,667**

**Alternative (for non-subscription):**
- LTV = Avg purchase × Purchase frequency × Customer lifespan
- Example: $100 purchase × 4 times/year × 3 years = $1,200

**Benchmark:** LTV:CAC ratio >3x (healthy), >5x (excellent)

---

### 3. Payback Period

**Formula:** CAC ÷ Gross margin per month

**Example:**
- CAC: $2,000
- MRR: $500
- Gross margin: 80%
- **Payback: $2,000 ÷ ($500 × 0.8) = 5 months**

**Benchmark:**
- SaaS: <12 months (healthy), <6 months (excellent)
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

**Q1 2026 cohort LTV tracking:**

| Month | Customers | MRR | Churn | Cumulative LTV |
|-------|-----------|-----|-------|----------------|
| Jan (M0) | 30 | $15K | 0% | $500 |
| Feb (M1) | 30 | $15K | 3% | $1,000 |
| Mar (M2) | 29 | $14.5K | 3% | $1,483 |
| Apr (M3) | 28 | $14K | 3% | $1,983 |

**Projection:** If 3% monthly churn holds, LTV = $16,667

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

**Example result:**
- Control geos: 100 paid + 50 organic = 150 total
- Holdout geos: 0 paid + 70 organic = 70 total
- **Cannibalization:** 20 organic customers came from paid
- **Incremental:** 80 customers truly incremental
- **True CAC:** $15K spend ÷ 80 = $188 (not $150)

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
