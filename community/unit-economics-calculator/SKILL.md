---
name: unit-economics-calculator
description: Unit economics calculator - CAC payback, LTV:CAC, burn multiple in 30min
version: 1.0.0
tags: [finance, unit-economics, saas-metrics, cac, ltv, burn-rate, ROI-8.5]
---

# Unit Economics Calculator

**ROI:** 8.5/10 - Saves 5h → 30min with investor-grade metrics

Calculates SaaS unit economics: CAC, LTV, payback, burn multiple, magic number.

---

## Core Formulas

### 1. CAC (Customer Acquisition Cost)

**Formula:** (Sales + Marketing spend) ÷ New customers

**Example:**
- Q1 spend: $50K sales + $30K marketing = $80K
- New customers: 40
- **CAC: $2,000**

**Blended vs. Paid:**
- **Blended CAC:** All spend ÷ all customers (includes organic)
- **Paid CAC:** Paid spend ÷ paid customers (excludes organic)

---

### 2. LTV (Lifetime Value)

**Formula:** ARPA ÷ Monthly churn rate

**Example:**
- ARPA: $500/month
- Churn: 3%/month
- **LTV: $500 ÷ 0.03 = $16,667**

**With gross margin:**
- LTV (profit) = (ARPA × Gross margin%) ÷ Churn
- Example: ($500 × 80%) ÷ 3% = $13,333

---

### 3. LTV:CAC Ratio

**Formula:** LTV ÷ CAC

**Example:**
- LTV: $16,667
- CAC: $2,000
- **Ratio: 8.3x**

**Benchmark:**
- <1x: Losing money on every customer ❌
- 1-3x: Unprofitable/break-even ⚠️
- 3-5x: Healthy ✅
- >5x: Excellent ✅✅

---

### 4. CAC Payback Period

**Formula:** CAC ÷ (MRR × Gross margin%)

**Example:**
- CAC: $2,000
- MRR: $500
- Gross margin: 80%
- **Payback: $2,000 ÷ ($500 × 0.8) = 5 months**

**Benchmark:**
- <12 months: Healthy ✅
- 12-18 months: Acceptable ⚠️
- >18 months: Too long ❌

---

### 5. Magic Number

**Formula:** (Net new ARR this quarter) ÷ (Sales + Marketing spend last quarter)

**Example:**
- Q1 sales/marketing: $100K
- Q2 net new ARR: $300K
- **Magic Number: 3.0**

**Benchmark:**
- <0.75: Inefficient, don't scale ❌
- 0.75-1.0: Optimize before scaling ⚠️
- >1.0: Ready to scale ✅

---

### 6. Burn Multiple

**Formula:** Net burn ÷ Net new ARR

**Example:**
- Monthly net burn: $50K
- Monthly net new ARR: $25K
- **Burn Multiple: 2.0**

**Benchmark:**
- <1.0: Capital efficient ✅✅
- 1.0-1.5: Healthy ✅
- 1.5-2.0: Acceptable ⚠️
- >2.0: Burning too fast ❌

---

## Dashboard Template

**SaaS Unit Economics Scorecard:**

```
┌──────────────────────────────────────┐
│ ACQUISITION EFFICIENCY               │
├──────────────────────────────────────┤
│ CAC (Blended):    $2,000            │
│ CAC (Paid):       $2,800            │
│ CAC Payback:      5 months     ✅   │
│ Magic Number:     1.2x         ✅   │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ RETENTION & VALUE                    │
├──────────────────────────────────────┤
│ ARPA:             $500/mo            │
│ Churn:            3%/mo              │
│ LTV:              $16,667            │
│ LTV:CAC:          8.3x         ✅✅  │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│ BURN & EFFICIENCY                    │
├──────────────────────────────────────┤
│ Monthly Burn:     $50K               │
│ Net New ARR/mo:   $25K               │
│ Burn Multiple:    2.0x         ⚠️   │
│ Runway:           12 months          │
└──────────────────────────────────────┘
```

---

## Scenario Analysis

**Question:** "Should we increase sales headcount?"

**Current state:**
- 5 AEs, $2K CAC, 5-month payback
- Adding 5 AEs = +$50K/mo cost

**Model:**
- New CAC: $2,500 (higher due to ramping reps)
- New payback: 6 months
- Break-even: Month 7

**Decision:** Yes, if:
- LTV:CAC stays >3x ($2.5K CAC = need LTV >$7.5K) ✅
- Runway >12 months ✅
- Magic number >0.75 ✅

---

## References

- anthropic-financial-services: DCF + unit economics models
- SaaS Capital benchmarks
- Bessemer SaaS metrics
