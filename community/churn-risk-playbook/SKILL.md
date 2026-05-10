---
name: churn-risk-playbook
description: Customer churn prevention playbook with health scoring - saves 4h→15min weekly at-risk account review
version: 1.0.0
tags: [customer-success, churn-prevention, health-scoring, retention, expansion, QBR, ROI-9.5]
---

# Churn Risk Playbook

**ROI:** 9.5/10 - Saves 4h → 15min for weekly at-risk account review

Systematic churn prevention framework using health scoring, leading indicators, and intervention playbooks. Turns reactive firefighting into proactive retention.

---

## When to Use

- **Weekly at-risk review**: Identify + triage churn risks
- **QBR prep**: Build exec-ready account health reports
- **Expansion qualification**: Spot upsell-ready accounts
- **Team onboarding**: Train CSMs on churn signals
- **Executive reporting**: Quantify retention metrics

**Frequency:** Weekly reviews + per-account intervention

---

## Core Framework

### Health Score Model (0-100)

**4 pillars** (weighted):

| Pillar | Weight | Green (80-100) | Yellow (50-79) | Red (0-49) |
|--------|--------|----------------|----------------|------------|
| **Product Usage** | 40% | DAU >70% licensed seats | 40-70% | <40% |
| **Engagement** | 25% | Exec engaged, QBRs held | Sporadic contact | No exec access |
| **Support Health** | 20% | <2 tickets/mo, <24h resolution | 3-5 tickets, 2-day avg | >5 tickets, >3 days |
| **Business Outcome** | 15% | ROI proven, case study | Value unclear | No measurable value |

**Leading indicators** (predict 90 days out):
- Usage decline >20% MoM
- No exec contact >45 days
- Support escalations
- Champion turnover
- Competitive eval signals

---

## Churn Risk Tiers

### Tier 1: Critical (Red Health Score 0-49)
**Characteristics:**
- Contract renewal <60 days
- Usage collapsed (>40% drop)
- Exec ghosting
- Active competitor eval

**Response:** Executive intervention playbook
- **Who:** VP CS + Account Exec
- **Timeline:** 48 hours to first meeting
- **Goal:** Understand root cause, offer rescue plan

---

### Tier 2: At-Risk (Yellow 50-79)
**Characteristics:**
- Declining usage trend
- Support ticket spike
- Champion turnover
- Delayed QBR (>30 days overdue)

**Response:** Proactive CSM outreach
- **Who:** Assigned CSM
- **Timeline:** 1 week to intervention
- **Goal:** Re-engage, deliver quick win

---

### Tier 3: Healthy (Green 80-100)
**Characteristics:**
- Stable/growing usage
- Regular exec engagement
- Low support volume
- Measurable ROI

**Response:** Expansion qualification
- **Who:** CSM + Account Exec
- **Goal:** Identify upsell opportunities

---

## Intervention Playbooks

### Playbook A: Usage Decline Recovery

**Trigger:** Product usage drops >20% MoM for 2 consecutive months

**Diagnosis questions:**
1. "What changed in your workflow 60 days ago?"
2. "Are you using a workaround or alternative tool?"
3. "Did we lose a champion or power user?"

**Recovery tactics:**
- **Quick win**: Identify 1 underutilized feature that solves current pain
- **Training refresh**: 30-min power-user session
- **Gamification**: Usage contest (team with highest adoption wins [prize])

**Success metric:** Usage back to baseline within 30 days

**Example:** See `examples/usage-decline-saas.md`

---

### Playbook B: Executive Ghosting Recovery

**Trigger:** No exec contact >45 days + renewal <6 months

**Diagnosis:**
- Champion still there? (Check LinkedIn)
- Org changes? (Acquisition, layoffs, restructure)
- Budget freeze? (Talk to finance contact)

**Re-engagement tactics:**
1. **Value summary email** (don't ask for meeting yet):
   ```
   Subject: [Company] results - Q3 impact summary
   
   Hi [Exec],
   
   Quick data share (no meeting ask):
   
   - [Metric 1]: Improved X% since go-live
   - [Metric 2]: Saved $Y in [timeframe]
   - [Customer testimonial]: "[Quote from peer]"
   
   Anything here not tracking with your priorities?
   ```

2. **Peer connection** (if email ignored):
   - Intro to similar customer exec
   - Industry event invite
   - Advisory board opportunity

3. **Executive Business Review** (EBR, not QBR):
   - 30-min strategic discussion (not product demo)
   - Agenda: Their goals + our alignment
   - Deliverable: Joint success plan

**Success metric:** Exec meeting booked within 14 days

---

### Playbook C: Support Escalation Response

**Trigger:** >5 support tickets in 30 days OR 1 Severity-1 escalation

**Immediate actions (24 hours):**
1. CSM reviews all tickets (find pattern)
2. Call customer (not email): "I see [pattern]. What's really going on?"
3. Escalate to product/engineering if systemic bug

**Root cause categories:**
- **Product bug**: Fast-track fix, offer workaround
- **Misaligned expectations**: Re-onboard on correct use case
- **Missing feature**: Roadmap transparency, alternative solution

**Churn prevention:**
- Offer **premium support SLA** (temp upgrade)
- Assign **dedicated CSE** (Customer Success Engineer)
- Weekly check-ins until resolved

**Success metric:** Ticket volume <3/mo within 60 days

---

### Playbook D: Champion Turnover

**Trigger:** Primary contact leaves company

**72-hour response:**
1. **Identify new stakeholder** (ask outgoing champion)
2. **Re-onboard** (don't assume knowledge transfer)
3. **Quick win delivery** (show value fast)

**Relationship rebuild:**
- **Week 1**: Intro call + value summary doc
- **Week 2-4**: Usage audit + training refresh
- **Week 5-8**: First QBR with new champion

**Churn risk:** 3x higher for 90 days post-turnover

**Example:** See `examples/champion-turnover-recovery.md`

---

## Expansion Qualification (Green Accounts)

**Don't expand at-risk accounts.** Fix health first.

**Expansion readiness checklist:**
- ✅ Health score >80 for 90+ days
- ✅ Executive sponsor engaged
- ✅ ROI documented (case study-worthy)
- ✅ Usage >70% of licensed seats
- ✅ Feature adoption >60% of paid modules

**Expansion triggers:**
- New use case adoption (e.g., added team/department)
- Power-user feature requests
- "Can we get more seats?" inbound ask

**Expansion playbook:**
1. **Business case builder** (CSM creates draft)
   - Current ROI × expansion = projected value
   - Competitive benchmark (peers using more)
2. **Executive alignment** (AE-led meeting)
   - Tie expansion to strategic initiative
   - Multi-year commit discount offer
3. **Pilot offer** (de-risk expansion)
   - 60-day trial of premium tier
   - Usage-based pricing (pay for what you use)

**Success metric:** 30% of green accounts expand annually

---

## QBR Framework (Quarterly Business Review)

**Purpose:** Strategic alignment, not product demo

**Agenda (45 min):**
1. **Business context** (5 min)
   - Customer shares: Goals, challenges, priorities
2. **Impact summary** (10 min)
   - Metrics delivered (vs baseline)
   - ROI quantification
3. **Looking ahead** (20 min)
   - Roadmap alignment (what's coming that helps them)
   - Expansion opportunities
   - Success plan for next 90 days
4. **Action items** (10 min)
   - Mutual commitments with owners/dates

**QBR assets:**
- **Pre-read deck** (sent 48h before)
- **Impact one-pager** (leave-behind)
- **Success plan doc** (shared doc, living)

**Red flag:** Customer cancels/reschedules QBR 2x = churn risk

**Example:** See `examples/qbr-deck-template.md`

---

## Weekly Churn Review (Team Ritual)

**15-minute standup** (every Monday):

1. **Tier 1 critical** (5 min)
   - Who owns? What's the plan? ETA?
2. **New at-risk accounts** (5 min)
   - What triggered yellow? Intervention assigned?
3. **Wins** (5 min)
   - Recovered accounts (green again)
   - Expansion closed

**Output:** Updated health score dashboard + intervention tracker

---

## Metrics Dashboard

Track in CRM/CS platform:

| Metric | Green | Yellow | Red |
|--------|-------|--------|-----|
| **Gross Churn Rate** | <5% annual | 5-10% | >10% |
| **Net Retention** | >110% | 100-110% | <100% |
| **Health Score (avg)** | >80 | 60-80 | <60 |
| **At-Risk → Recovered** | >60% | 40-60% | <40% |
| **QBR Completion** | >90% | 70-90% | <70% |
| **Expansion Rate** | >20% | 10-20% | <10% |

**Benchmark:** Best-in-class SaaS = <3% gross churn, >120% net retention

---

## Anti-Patterns (Never Do)

❌ **Ignore yellow scores** - "They'll be fine" → Tier 2 becomes Tier 1
❌ **Upsell at-risk accounts** - Expansion on red health = accelerated churn
❌ **Ghost struggling customers** - "Too hard to save" = self-fulfilling prophecy
❌ **Product-first QBRs** - Feature roadmap ≠ business value discussion
❌ **Manual health scoring** - Use automated data, not CSM gut feel

✅ **Do instead:**
- Automate health scoring (usage + engagement + support data)
- Intervene at yellow (before red crisis)
- Fix first, expand second
- QBR = strategic business review, not demo
- Data-driven, not opinion-driven

---

## References

- ai-boost/awesome-prompts: Customer Success Strategist
- Naas notebooks: Create_A_Customer_Success_Playbook
- SaaS retention benchmarks (OpenView, ChartMogul)

**Sources:**
- Leading indicator research: Gainsight, Totango
- QBR frameworks: Success Coaching, CSM Practice
