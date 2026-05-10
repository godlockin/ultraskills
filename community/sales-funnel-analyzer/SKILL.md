---
name: sales-funnel-analyzer
description: Sales funnel efficiency analyzer - diagnoses conversion bottlenecks and calculates pipeline health
version: 1.0.0
tags: [sales, funnel-analysis, conversion-optimization, pipeline-health, sales-ops, ROI-9.0]
---

# Sales Funnel Analyzer

**ROI:** 9.0/10 - Identifies $M+ in stuck pipeline, pinpoints exact conversion leaks

Systematic sales funnel diagnostic that turns CRM data into actionable insights. Finds where deals die, why, and how to fix it.

---

## When to Use

- **Weekly pipeline review**: Identify stuck deals + bottlenecks
- **Quarterly planning**: Forecast accuracy + capacity planning
- **Sales coaching**: Rep-level performance diagnosis
- **Exec reporting**: Board-ready funnel metrics
- **New hire onboarding**: Teach funnel discipline

**Frequency:** Weekly ops review + monthly executive summary

---

## Core Framework

### Standard B2B SaaS Funnel

```
MQL → SQL → Discovery → Demo → Proposal → Negotiation → Closed-Won
 ↓      ↓        ↓         ↓         ↓           ↓            ↓
100   40%      60%       70%       50%         80%          40%
```

**Benchmark conversion rates** (Enterprise SaaS):
- MQL → SQL: 40% (qualification filter)
- SQL → Discovery: 60% (first meeting booked)
- Discovery → Demo: 70% (qualified need)
- Demo → Proposal: 50% (budget + authority confirmed)
- Proposal → Negotiation: 80% (legal/procurement)
- Negotiation → Closed-Won: 40% (final decision)

**Overall MQL → Closed-Won:** ~3-5% (enterprise), 10-15% (SMB)

---

## Funnel Health Metrics

### 1. Conversion Rate by Stage

**Formula:** (Deals advanced ÷ Deals entered) × 100

**Example:**
- 100 SQLs enter Discovery stage
- 60 advance to Demo
- **Conversion rate:** 60%

**Diagnosis:**
- >Benchmark: Strong (qualification working)
- <Benchmark: **Leak** (investigate root cause)

---

### 2. Stage Velocity (Days in Stage)

**Benchmark:**
- Discovery: 7-14 days
- Demo: 7-10 days
- Proposal: 14-21 days
- Negotiation: 14-30 days

**Red flags:**
- Deal >2x benchmark = stalled (needs intervention)
- Deal <0.5x benchmark = rushed (quality risk)

---

### 3. Pipeline Coverage

**Formula:** (Total pipeline value ÷ Quarterly quota) × Win rate

**Healthy coverage:** 3-5x quota
- Example: $1M quota, 30% win rate → need $3.3M - $5M pipeline

**Diagnosis:**
- <3x: Insufficient pipeline (increase top-of-funnel)
- >5x: Too much, can't close (focus or qualify harder)

---

### 4. Win Rate Analysis

**Overall win rate:** Closed-Won ÷ (Closed-Won + Closed-Lost)

**Segmented win rates:**
- By deal size: <$50K vs $50-250K vs >$250K
- By industry: Finance vs Healthcare vs Tech
- By rep: Top vs average vs bottom quartile
- By source: Inbound vs outbound vs referral

**Benchmark:** 20-30% overall (enterprise SaaS)

---

## Diagnostic Workflow

### Step 1: Calculate Stage Conversion Rates

**Input:** CRM data (last 90 days)

| Stage | Entered | Advanced | Conversion | Benchmark | Gap |
|-------|---------|----------|------------|-----------|-----|
| SQL | 500 | 180 | 36% | 40% | **-4%** |
| Discovery | 180 | 126 | 70% | 60% | +10% ✅ |
| Demo | 126 | 50 | 40% | 50% | **-10%** |
| Proposal | 50 | 40 | 80% | 80% | 0% |
| Negotiation | 40 | 12 | 30% | 40% | **-10%** |

**Key leaks identified:**
1. SQL → Discovery (-4%): Qualification too loose
2. Demo → Proposal (-10%): Demo not converting
3. Negotiation → Closed (-10%): Losing at finish line

---

### Step 2: Identify Root Causes

#### Leak 1: SQL → Discovery (-4%)

**Hypothesis tests:**
- **Marketing alignment:** Are MQLs actually qualified?
  - **Test:** Sample 20 lost SQLs, review lead source/score
  - **Finding:** 60% from low-intent content downloads (not buying signals)
  - **Fix:** Tighten MQL criteria (demo requests only)

- **SDR follow-up speed:** How fast are SQLs contacted?
  - **Test:** Measure time-to-first-contact
  - **Finding:** Average 48 hours (should be <5 hours)
  - **Fix:** Implement SDR round-robin + SLA

---

#### Leak 2: Demo → Proposal (-10%)

**Hypothesis tests:**
- **Discovery quality:** Are AEs qualifying before demoing?
  - **Test:** MEDDIC score distribution (1-10)
  - **Finding:** 40% of demos done with MEDDIC <6 (unqualified)
  - **Fix:** Mandate discovery call before demo

- **Demo relevance:** Are demos customized or generic?
  - **Test:** Listen to 10 demo recordings
  - **Finding:** 70% use generic pitch deck (not tailored)
  - **Fix:** Require pre-demo prep doc (customer research)

---

#### Leak 3: Negotiation → Closed (-10%)

**Hypothesis tests:**
- **Pricing objections:** Are we losing on price?
  - **Test:** Review Closed-Lost reasons
  - **Finding:** 50% cite "went with cheaper competitor"
  - **Fix:** ROI calculator + value selling training

- **Procurement friction:** Are legal/procurement stalling?
  - **Test:** Measure negotiation stage duration
  - **Finding:** Average 45 days (2x benchmark)
  - **Fix:** Standard contract templates + legal playbook

---

### Step 3: Segment Analysis (Find Patterns)

**By deal size:**
| Segment | Win Rate | Avg Cycle | Key Insight |
|---------|----------|-----------|-------------|
| <$50K | 35% | 30 days | High win rate, fast close |
| $50-250K | 25% | 60 days | Benchmark performance |
| >$250K | 15% | 120 days | **Losing big deals** |

**Action:** Enterprise deals need exec sponsor involvement (currently missing)

---

**By rep:**
| Rep | Win Rate | Avg Deal Size | Pipeline Coverage |
|-----|----------|---------------|-------------------|
| Sarah | 40% | $180K | 4.2x ✅ |
| Mike | 28% | $120K | 3.8x |
| Alex | 12% | $90K | 2.1x ⚠️ |

**Action:** Coach Alex on qualification (accepting bad-fit deals)

---

**By lead source:**
| Source | Win Rate | Cost per SQL | CAC Payback |
|--------|----------|--------------|-------------|
| Inbound | 35% | $500 | 6 months ✅ |
| Outbound | 18% | $1,200 | 14 months |
| Referral | 55% | $200 | 3 months ✅✅ |

**Action:** Double down on referral program

---

## Advanced Diagnostics

### Cohort Analysis (Time-Based Trends)

**Question:** "Is funnel performance improving or degrading?"

**Method:** Compare conversion rates by cohort

| Cohort | SQL→Discovery | Discovery→Demo | Overall Win Rate |
|--------|---------------|----------------|------------------|
| Q1 2026 | 38% | 45% | 22% |
| Q2 2026 | 40% | 48% | 25% |
| Q3 2026 | 42% | 52% | 28% ✅ |

**Insight:** Improving trend = process improvements working

---

### Multi-Touch Attribution

**Question:** "Which marketing touches drive highest win rate?"

**Example:**
- Deal with 1 touch (demo request): 20% win rate
- Deal with 3 touches (webinar + case study + demo): 35% win rate
- Deal with 5+ touches (nurtured over 6 months): 45% win rate

**Insight:** Longer nurture = higher quality pipeline

---

### Velocity Benchmarking

**Question:** "Where do deals get stuck?"

**Method:** Average days in stage by outcome

| Stage | Won Deals | Lost Deals | Insight |
|-------|-----------|------------|---------|
| Discovery | 10 days | 25 days | Lost deals linger 2.5x longer |
| Demo | 8 days | 18 days | Speed = confidence |
| Proposal | 20 days | 45 days | **Stuck proposals = death** |

**Action:** If proposal sits >30 days, escalate to manager

---

## Actionable Outputs

### 1. Weekly Pipeline Health Report

**Format:** 1-page exec summary

**Sections:**
- **Pipeline coverage:** [X]x quota (target: 3-5x)
- **Stage distribution:** % of pipeline by stage (visualized)
- **Conversion rates:** vs benchmark (red/yellow/green)
- **At-risk deals:** >2x velocity in any stage
- **Top actions:** 3 priorities for next week

---

### 2. Rep Scorecards

**Individual performance vs team avg:**

| Metric | Sarah | Team Avg | Gap |
|--------|-------|----------|-----|
| Win Rate | 40% | 25% | +15% ✅ |
| Avg Deal Size | $180K | $130K | +$50K ✅ |
| Sales Cycle | 55 days | 65 days | -10 days ✅ |
| Pipeline Coverage | 4.2x | 3.5x | +0.7x ✅ |

**Coaching focus:** Sarah = top performer, replicate her process

---

### 3. Forecast Accuracy Tracker

**Method:** Compare forecasted vs actual closed revenue

| Quarter | Forecast | Actual | Accuracy | Insight |
|---------|----------|--------|----------|---------|
| Q1 | $1.2M | $900K | 75% | Under-delivered |
| Q2 | $1.5M | $1.4M | 93% ✅ | Improving |
| Q3 | $1.8M | $1.7M | 94% ✅ | Consistent |

**Best practice:** >90% accuracy = predictable business

---

## Intervention Playbooks

### Playbook 1: Unstick Stalled Deals

**Trigger:** Deal >2x stage velocity benchmark

**Actions:**
1. **Manager review** (within 48h)
   - Why is it stuck?
   - MEDDIC score check (1-10)
   - Competitive threat?
2. **Customer pulse check** (phone call, not email)
   - "Where are you in the process?"
   - "What's blocking the decision?"
3. **Executive alignment** (if >$100K deal)
   - Offer exec-to-exec meeting
   - Escalate to remove friction

**Example:** See `examples/unsticking-stalled-enterprise-deal.md`

---

### Playbook 2: Fix Conversion Leak

**Trigger:** Stage conversion <10% below benchmark for 2 consecutive months

**Actions:**
1. **Root cause analysis** (sample 20 lost deals)
   - Common objection themes
   - MEDDIC gaps
   - Competitive losses
2. **Process fix:**
   - Update qualification criteria
   - Refine demo/discovery process
   - Train reps on new playbook
3. **A/B test** (new process vs old)
   - Track conversion improvement
   - Roll out if >5% lift

---

### Playbook 3: Scale Top Performer

**Trigger:** Rep with >35% win rate (top quartile)

**Actions:**
1. **Shadow top rep** (3 calls: discovery, demo, negotiation)
2. **Document playbook** (what makes them different?)
3. **Train team** (monthly rep exchange)
4. **Incentivize sharing** (coaching bonus)

---

## Tools + Data Sources

**Required CRM fields:**
- Deal stage + stage entry date
- Closed date + closed reason (won/lost)
- Deal value + product mix
- Lead source + campaign
- Rep owner + manager

**Analytics:**
- Salesforce Reports (or CRM equivalent)
- Gong/Chorus (call recording analysis)
- Marketing attribution platform

**Dashboards:**
- Executive: Win rate + pipeline coverage trends
- Sales ops: Stage conversion funnel chart
- Reps: Personal scorecard vs team

---

## Success Metrics

Track in CRM/BI tool:

| Metric | Target |
|--------|--------|
| **Overall win rate** | >25% (enterprise SaaS) |
| **Pipeline coverage** | 3-5x quota |
| **Forecast accuracy** | >90% |
| **Sales cycle** | <90 days (enterprise), <30 days (SMB) |
| **SQL → Discovery** | >40% |
| **Discovery → Demo** | >60% |
| **Demo → Proposal** | >50% |
| **Proposal → Closed** | >30% |

**Benchmark sources:** SaaS Capital, OpenView, ProfitWell

---

## References

- Naas notebooks: Analyze_Sales_Funnel_Efficiency
- SaaS Sales Funnel Benchmarks (OpenView)
- Predictable Revenue (Aaron Ross)
- MEDDIC qualification framework
