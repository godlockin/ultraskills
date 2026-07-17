# Orchestration Patterns (4 End-to-End Business Pipelines)

Four pipelines cover ~80% of business requests. Each is a **template** — adapt steps as the brief demands.

---

## 📊 Pattern B1: Coverage / Equity Research (Analyst Write-Up)

### When

- User is an analyst/fund manager
- Output target: 8-12 page institutional-grade research report
- Need: comps + DCF + earnings integration + datapack

### When NOT to use

- User is a banker (use B2 instead)
- User is a founder (use B3 instead)
- User is an SMB owner (use B4 instead)

### Steps

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | initiating-coverage | 8-12 page template | Skeleton with mandatory sections |
| 2 | comps-analysis | Operating metrics + multiples | Peer group table |
| 3 | dcf-model | DCF valuation | Sensitivity table |
| 4 | earnings-analysis | Q3 numbers if available | Earnings bridge |
| 5 | datapack-builder | Trace every number | Working appendix |
| 6 | 3-statement-model | Income / balance / cashflow | 5-year forecast |
| 7 | data-viz | Chart selection | Waterfall / bridge / multiples chart |
| 8 | review-contract (optional) | Material agreement review | Legal tail risk |

### Quality Gates (mandatory before publication)

- [ ] All numbers traceable to datapack (step 5)
- [ ] DCF sensitivity table shows WACC range 7-12% + terminal growth 2-3%
- [ ] Comps set has ≥5 peers
- [ ] Earnings bridge ties to last quarter's actuals
- [ ] 3-statement model balances (assets = liabilities + equity)
- [ ] No invented projections without explicit assumption callout

### Timing

- Manual: 2-3 weeks analyst + 1-2 weeks associate
- Orchestrator: 60-90 minutes
- **compression**: ~40x

---

## 🤝 Pattern B2: M&A / Transaction (Dealmaker Model)

### When

- User is a banker / PE / corp dev
- Output target: full M&A memo with model + pitch + legal gates
- Need: comps + DCF + LBO + pitch + legal/compliance/NDA review

### When NOT to use

- User wants just an equity write-up (use B1 instead)
- User is a founder (use B3 instead)

### Steps

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | deal-sourcing | Market scan if user is sourcing | Target list |
| 2 | comps-analysis | Precedent + public comps | Transaction comps |
| 3 | dcf-model | Target DCF | Standalone valuation |
| 4 | lbo-model | Sources & uses + debt schedule + returns | Returns waterfall |
| 5 | pitch-deck | IC memo or buyer-facing pitch | Deck |
| 6 | review-contract | LOI / merger agreement | Risk flags |
| 7 | triage-nda | Bidder NDA | GREEN/YELLOW/RED |
| 8 | legal-risk-assessment | Regulatory / antitrust early read | Risk register |

### Mandatory Legal Gates

Unlike other paths, **all three legal steps (6-7-8) are mandatory**:

```
⚠️ Compliance rule:
   B2 may NOT skip review-contract, triage-nda, OR legal-risk-assessment
   before any external pitch
```

### Adapted Variants

- **Buyer-side**: skip step 1, steps 2-8 only
- **Seller-side**: step 1 = reverse-engineered buyer list
- **Strategic acquirer**: step 8 = antitrust focus specifically
- **PE buyer**: step 4 = standard LBO with debt schedule 60-70% LTV

### Timing

- Manual: 4-8 weeks (banker + analyst + legal + compliance)
- Orchestrator: 90-120 minutes (with legal gates)
- **compression**: ~30x

---

## 🎤 Pattern B3: Pitch / Investor Materials (Founder/PMM Deck)

### When

- User is a founder / fundraising / PMM
- Output target: 10-15 slide deck + one-pager
- Need: customer/market insight + comps + data-viz + pitch review

### When NOT to use

- User is an analyst (use B1 instead)
- User is a banker (use B2 instead)

### Steps

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | office-hours | YC-style 6 forcing questions | Founder-mode brief |
| 2 | plan-ceo-review | CEO-mode plan review | 10-star problem framing |
| 3 | comps-analysis (light) | TAM/SAM/SOM via market sizing | Top-down market |
| 4 | data-viz | Chart selection (bar, TAM funnel) | Charts |
| 5 | pitch-deck or deck-refresh | 10-15 slides | Deck |
| 6 | pitch-deck-critic | VC-grade feedback | Punch list |
| 7 | create-an-asset (optional) | One-pager / landing page | Alternative asset |
| 8 | okr-alignment-checker | Sanity-check OKRs vs pitch | Coherence review |

### Adapted Variants

- **Seed stage**: Steps 1, 4, 5, 6 only (lighter)
- **Series A+**: All 8 steps
- **Existing deck refresh**: Steps 4-6 only (revise not redo)
- **Customer-facing one-pager**: Replace step 5 with `create-an-asset` (landing page)

### Cross-Cluster Bridges

This path **should defer** to:
- `design-orchestrator` if the deck needs production-grade visual discipline
- `content-orchestrator` if the campaign involves video/social beyond deck

### Timing

- Manual: 1-2 weeks
- Orchestrator: 45-60 minutes
- **compression**: ~25x

---

## 🏪 Pattern B4: SMB Operations (Owner/Operator)

### When

- User is an SMB owner / operator / bookkeeper
- Output target: end-to-end weekly/monthly ops loop
- Need: cash/invoice/lead/SOP/escalation handling

### When NOT to use

- User is institutional (use B1/B2/B3 instead)

### Steps

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | cash-flow-snapshot | Current AR/AP | Cash position |
| 2 | invoice-chase | Overdue reminders | Email drafts |
| 3 | lead-triage | Inbound scoring | Sorted leads |
| 4 | customer-pulse | Feedback aggregation | Insights |
| 5 | sop-writer | New process doc | SOP document |
| 6 | smb-onboard | Customer / employee / tool | Onboarding runbook |
| 7 | customer-escalation | Issue packaging | Handoff to eng/PM |
| 8 | draft-response | Reply customer | Drafter |

### Compliance + Legal Activation

Insert **compliance-support** when SOX/audit-relevant:

```
if SMB is publicly-traded OR SOX-relevant OR healthcare/fintech:
    insert audit-support after step 1
    insert compliance-check before step 8
```

### Adapted Variants

- **Weekly close only**: Steps 1, 2, 8 (cashflow + invoice + reply)
- **New customer onboarding**: Steps 4, 6 (pulse + onboard)
- **Sales pipeline**: Steps 3 + 8 (triage + reply)
- **Process documentation**: Step 5 only (SOP writer)

### Timing

- Manual: scattered, 30-60 min per task
- Orchestrator: 20-30 minutes per full loop
- **compression**: ~2-3x (lower because SMB loops are mostly operational repetition, not design)

---

## Cross-Pipeline Checkpoints

After every 4 steps, the orchestrator should **pause and ask the user** if continuing in the same direction still matches intent. This prevents 8-step pipelines going off-rails.

## Pipeline Hygiene Rules

1. **Always end with legal/quality gate** in B1/B2 (mandatory in B2)
2. **Don't run all steps blindly** — skip what doesn't apply
3. **Always trace numbers** in B1/B2 (datapack before any claim)
4. **Hard limit: ≤ 8 steps per pipeline** — if more needed, split into multiple iterations
