# Health Scoring Reference Guide

Quick-reference for calculating and acting on customer health scores.

---

## Health Score Calculation

**Formula:** Weighted average of 4 pillars

```
Health Score = (Usage × 0.4) + (Engagement × 0.25) + (Support × 0.2) + (Outcome × 0.15)
```

Each pillar scored 0-100, then weighted.

---

## Pillar Breakdown

### 1. Product Usage (40% weight)

**Metrics:**
- DAU/MAU ratio (daily active ÷ monthly active)
- Feature adoption rate (% of paid features used)
- Session duration (engagement depth)
- Data volume (records processed, reports run)

**Scoring:**
- **100 pts:** >80% of licenses active daily, >70% feature adoption
- **75 pts:** 60-80% daily active, 50-70% features
- **50 pts:** 40-60% daily active, 30-50% features
- **25 pts:** <40% daily active, <30% features

**Red flags:**
- 20%+ MoM decline in DAU
- Core feature (reason they bought) unused >30 days
- Only 1-2 power users (concentration risk)

---

### 2. Engagement (25% weight)

**Metrics:**
- Executive sponsor engaged (Y/N)
- QBR cadence (on-time vs delayed)
- Champion strength (can they sell internally?)
- Response time to CSM outreach

**Scoring:**
- **100 pts:** Exec engaged, QBRs on-time, strong champion, <24h response
- **75 pts:** Mid-level engaged, QBRs occasional, champion exists
- **50 pts:** Individual contributor only, no QBRs, weak champion
- **25 pts:** Ghosting CSM, no exec access, champion left

**Red flags:**
- No exec contact >45 days
- QBR cancelled/rescheduled 2x
- Champion turnover (no replacement identified)

---

### 3. Support Health (20% weight)

**Metrics:**
- Ticket volume (count per month)
- Severity mix (% critical vs informational)
- Resolution time (avg hours to close)
- CSAT score (support satisfaction)

**Scoring:**
- **100 pts:** <2 tickets/mo, no P1s, <24h resolution, CSAT >4.5
- **75 pts:** 3-5 tickets/mo, occasional P1, 1-2 day resolution
- **50 pts:** 6-10 tickets/mo, frequent P1s, 3-day resolution
- **25 pts:** >10 tickets/mo, P1 escalations, >5-day resolution

**Red flags:**
- Ticket volume spike (3x normal)
- P1 escalation to exec team
- Angry tone in tickets ("This is unacceptable...")
- Same issue reported 3+ times (unresolved)

---

### 4. Business Outcome (15% weight)

**Metrics:**
- ROI achieved (vs promised)
- Case study-worthy (Y/N)
- NPS score (promoter/passive/detractor)
- Renewal sentiment (likely/maybe/no)

**Scoring:**
- **100 pts:** ROI proven, case study done, NPS >8, renewal certain
- **75 pts:** ROI directional, NPS 7-8, renewal likely
- **50 pts:** ROI unclear, NPS 5-6, renewal uncertain
- **25 pts:** No ROI, NPS <5, renewal at-risk

**Red flags:**
- Customer can't articulate value
- "We're not sure it's worth it" sentiment
- Competitive evaluation underway

---

## Automated vs Manual Scoring

**Automate these:**
- Usage metrics (pull from product analytics)
- Support tickets (CRM integration)
- Engagement cadence (last contact date)

**Manual (CSM judgment):**
- Champion strength (qualitative assessment)
- Renewal sentiment (conversation-based)
- Political context (org changes, budget freezes)

**Best practice:** 80% automated data, 20% CSM overlay

---

## Health Score Actions Matrix

| Score Range | Tier | Action | Owner | Frequency |
|-------------|------|--------|-------|-----------|
| **90-100** | Tier 0: Champions | Expansion qualify, case study | CSM + AE | Quarterly |
| **80-89** | Tier 1: Healthy | Standard QBR, maintain | CSM | Quarterly |
| **65-79** | Tier 2: Yellow | Proactive outreach, quick win | CSM | Bi-weekly |
| **50-64** | Tier 3: At-Risk | Intervention playbook | CSM + Manager | Weekly |
| **0-49** | Tier 4: Critical | Executive escalation | VP CS + Exec team | Daily |

---

## Trend Analysis (More Important Than Score)

**Declining trend = bigger risk than low static score**

Example:
- Account A: Score 60 (stable for 6 months) = Medium risk
- Account B: Score 75 → 70 → 65 (3-month decline) = **High risk**

**Why:** Decline indicates active problem (new pain), static low score = status quo

**Track:**
- 30-day trend (MoM change)
- 90-day trend (quarterly movement)
- 12-month trend (annual health)

**Alert triggers:**
- Score drops >10 pts in 30 days
- Score drops >20 pts in 90 days
- Score below 70 for >90 days

---

## Leading Indicator Checklist

These predict churn 60-90 days before renewal:

- [ ] Usage decline >20% MoM (2 consecutive months)
- [ ] No exec contact >45 days
- [ ] Champion left company (no replacement)
- [ ] Support escalation (P1 ticket)
- [ ] QBR cancelled/rescheduled 2x
- [ ] Competitive evaluation (mentioned in conversation)
- [ ] Budget freeze / layoffs at customer
- [ ] Contract value <$50K (low priority for them)
- [ ] Single user dependency (not org-wide adoption)
- [ ] Feature request repeatedly denied

**Intervention threshold:** 3+ indicators = immediate playbook activation

---

## Sample Health Score Card

**Account:** Acme Corp
**ARR:** $150K
**Renewal Date:** 2026-09-15 (120 days out)

| Pillar | Score | Weight | Weighted | Trend |
|--------|-------|--------|----------|-------|
| Usage | 55 | 40% | 22.0 | ↘️ -15 pts MoM |
| Engagement | 70 | 25% | 17.5 | ↔️ Stable |
| Support | 80 | 20% | 16.0 | ↗️ +5 pts (improving) |
| Outcome | 60 | 15% | 9.0 | ↔️ Stable |
| **Total** | **64.5** | **100%** | **64.5** | **↘️ Declining** |

**Tier:** 3 (At-Risk)
**Action:** Intervention Playbook A (Usage Decline Recovery)
**Owner:** CSM (Jane)
**Next Review:** 2026-05-17 (weekly check-in)

---

## Integration with CRM

**Required fields:**
- Health Score (calculated field)
- Health Trend (30d/90d change)
- At-Risk Flag (boolean, auto-set if score <70)
- Last Intervention Date
- Intervention Playbook Used

**Dashboards:**
- Executive: Accounts by tier (pie chart)
- CSM: My at-risk accounts (table, sorted by renewal date)
- Operations: Churn prediction model (score + tenure + ARR)

---

## Team Calibration (Monthly Ritual)

**Purpose:** Align CSM judgment scores

**Process:**
1. Pick 5 accounts (mix of scores)
2. Each CSM scores independently
3. Compare scores (variance >10 pts = discuss)
4. Align on scoring rubric

**Why:** Prevent CSM bias (optimism/pessimism) from skewing data

---

## References

- Gainsight Health Score Framework
- ChartMogul SaaS Metrics Benchmark
- Totango Customer Success Playbook
