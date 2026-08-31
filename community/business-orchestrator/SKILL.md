---
name: business-orchestrator
description: "Routes business/finance/sales/HR/legal requests to the right skill in the 164-skill business cluster, and composes them into end-to-end pipelines. Four orchestration paths (equity coverage / M&A transaction / pitch & investor materials / SMB operations) cover ~80% of business requests. Includes routing decision table, cross-reference index to comps/DCF/LBO/3-statement methods, and version-sync mechanism. Trigger on 'analyze this company', 'model the deal', 'build a pitch deck', 'help me close this month', 'draft my fundraising', or any business brief that does not map to a single skill."
version: 1.0.0
tags: [business, finance, orchestrator, router, sales, marketing, hr, legal, operations, equity-research, ma, pitch-deck, smb, community]
---

# Business Orchestrator

> 164 business skills, one entry point. Routes, composes, never duplicates.

## 🎯 Goal

UltraSkills has 164 skills in the `business` root across 13 sub-clusters (`商业·财务` 56, `商业·小微企业` 26, `商业·销售增长` 13, `商业·业务运营` 13, `商业·高管顾问` 11, `商业·产品` 11, `商业·财务会计` 7, `商业·人才管理` 6, `商业·法务合规` 6, `商业·法务合规` 6, `商业·项目管理` 5, `商业·人力资源` 3, `商业·战略分析` 1). Users face three problems:

1. **Domain confusion** — analyst ask? banker ask? SMB ask? PMM ask? — same sentence reads differently.
2. **Pipeline gap** — equity coverage requires comps + DCF + earnings + datapacks; no skill chains them.
3. **Compliance/legal blindspot** — many financial outputs (DCF, pitch decks, contracts) need legal/HR/compliance review; no skill enforces that follow-up.

This skill is the **conductor** for the business cluster. It:
- Routes a brief via a 13-row sub-cluster decision table
- Composes 4 end-to-end pipelines (Coverage / M&A / Pitch / SMB Ops)
- Cross-references (not duplicates) every analytic method
- Includes version sync mechanism so upstream bumps don't silently desync

## 🧠 Core Concepts

### The 4 Orchestration Paths

```
┌────────────────────────────────────────────────────────────────┐
│ B1 · Coverage / Equity Research (analyst write-up)            │
│ B2 · M&A / Transaction (dealmaker model)                       │
│ B3 · Pitch / Investor Materials (founder/PMM deck)             │
│ B4 · SMB Operations (owner/operator close, invoice, sales)      │
└────────────────────────────────────────────────────────────────┘
```

These four paths cover ~80% of business requests. The remaining 20% — single-skill asks like "variance analysis" or "draft this offer letter" — the orchestrator dispatches directly without a pipeline.

### Routing by Sub-Cluster (13 layers)

| Sub-cluster | Count | Path coverage | Example skills |
|-------------|-------|---------------|----------------|
| business-finance | 56 | B1 + B2 | comps-analysis, dcf-model, lbo-model, earnings-analysis, initiating-coverage |
| small-business-ops | 26 | B4 | smb-onboard, canva-creator, cash-flow-snapshot, invoice-chase, customer-pulse |
| sales-marketing | 13 | B3 + B4 | objection-handler, pitch-deck, okr-alignment-checker, lead-magnets |
| business-operations | 13 | B4 | sop-writer, crisis-comms-playbook, customer-escalation, kb-article |
| business-clevel | 11 | B3 | data-viz, digital-brain, plan-ceo-review, office-hours |
| business-product | 11 | (1-shot) | prioritize-assumptions, prioritization-frameworks |
| finance-accounting | 7 | B4 | variance-analysis, journal-entry, close-management |
| business-legal | 6 | B2 (always!) | compliance-check, legal-risk-assessment, contract-risk-highlighter, legal-response |
| legal-compliance | 6 | B2 + B3 | review-contract, triage-nda, vendor-check |
| hr-talent | 6 | (1-shot) | performance-review, comp-analysis, draft-offer |
| business-pm | 5 | (1-shot) | learn-from-loss, to-issues, retro, grill-me |
| business-hr | 3 | (1-shot) | lead-magnets, interview-scorecard-generator |
| business-strategy | 1 | (1-shot) | competitive-intelligence |

**Important**: This skill does not generate any financial analysis itself. It tells the model *which* skill to invoke next, *in what order*, *with what review gates*.

## 🚀 Workflow

### Phase 1 — Routing Decision Table

When the user says anything about business/finance/sales/legal, run the decision table to find the right entry.

**Routing rules:**
1. **Detect role signal** — am I hearing an analyst, banker, founder, SMB owner, operator?
2. **Detect deliverable** — research note? model? deck? invoice? contract?
3. **Detect single vs. multi-skill** — one-shot (e.g. "draft NDA review") or pipeline-worthy (e.g. "build me a comps set + DCF + pitch deck")?
4. **Map to entry skill** + recommend path.

**Heuristics:**

| Signal in user prompt | Likely path |
|---------------------|------------|
| "company analysis" / "valuation" / "DCF" / "comps" / "earnings" / "initiate coverage" | **B1** (Coverage) |
| "deal" / "LBO" / "M&A" / "merger" / "buyout" / "leverage" / "transaction" | **B2** (M&A) |
| "pitch deck" / "fundraising" / "Series A" / "investor materials" / "one-pager" / "deck refresh" | **B3** (Pitch) |
| "small business" / "SMB" / "invoice" / "close the books" / "onboard customer" / "cash flow" / "owner" | **B4** (SMB) |
| "offer letter" / "review" / "performance review" / "interview" | 1-shot (hr-talent) |
| "NDA" / "contract review" / "compliance check" | 1-shot (legal-compliance) or B2 step |
| "OKR" / "objection" / "outreach" / "lead magnet" | 1-shot (sales-marketing) |

### Phase 2 — Composition (4 Pipelines)

#### 📊 Path B1: Coverage / Equity Research (analyst write-up)

**Trigger**: *"write an initiating coverage report on X"*, *"analyze Q3 earnings for Y"*, *"build a comps set for sector Z"*

```
Step 1: initiating-coverage       [report skeleton: 8-12 page template]
Step 2: comps-analysis            [institutional-grade comps with operating metrics]
Step 3: dcf-model                 [DCF valuation, sensitivity table]
Step 4: earnings-analysis         [if user has Q3 numbers → integrate into report]
Step 5: datapack-builder          [data appendix: all numbers traceable]
Step 6: 3-statement-model         [income/balance/cashflow forecasts]
Step 7: data-viz                  [chart types: waterfall/EPS bridge/multiple charts]
Step 8: review-contract (if material agreements)  [sanity-check legal tail risk]
```

Output: institutional-quality initiation/earnings report. **8-12 pages**, all numbers traceable to a datapack.

#### 🤝 Path B2: M&A / Transaction (dealmaker model)

**Trigger**: *"help me model an LBO of X"*, *"evaluate this acquisition"*, *"build a merger model"*

```
Step 1: deal-sourcing              [if user is sourcing: market scan]
Step 2: comps-analysis             [precedent transactions + public comps]
Step 3: dcf-model                  [DCF of target]
Step 4: lbo-model                  [Sources & Uses, debt schedule, returns waterfall]
Step 5: pitch-deck                 [IC memo or buyer-facing pitch]
Step 6: review-contract            [LOI / merger agreement review]
Step 7: triage-nda                 [bidder NDA triage]
Step 8: legal-risk-assessment      [regulatory / antitrust early read]
```

Output: complete M&A memo with model + pitch + legal gates. **Compliance is mandatory** before any external pitch.

#### 🎤 Path B3: Pitch / Investor Materials (founder/PMM deck)

**Trigger**: *"build our Series A deck"*, *"refresh our pitch"*, *"make a one-pager for customer X"*

```
Step 1: office-hours               [YC-style 6 questions on founder/PMM mode]
Step 2: plan-ceo-review            [CEO-mode plan review: 10-star problem?]
Step 3: comps-analysis             [if user wants market sizing — top-down comps]
Step 4: data-viz                   [chart selection: bar/TAM/SAM/SOM/funnel]
Step 5: pitch-deck or sales-enablement [deck creation, 10-15 slides]
Step 6: pitch-deck-critic          [VC-grade review → revise]
Step 7: create-an-asset            [one-pager/landing page alternative]
Step 8: okr-alignment-checker      [sanity-check the company's stated OKRs match the pitch narrative]
```

Output: investor-ready or buyer-ready deck + supporting assets + alignment sanity-check. **VC review gate is mandatory**.

#### 🏪 Path B4: SMB Operations (owner/operator close, invoice, sales)

**Trigger**: *"close the books this month"*, *"draft overdue invoice reminder"*, *"set up payroll"*, *"onboard this customer"*

```
Step 1: cash-flow-snapshot         [current AR/AP position]
Step 2: invoice-chase              [overdue invoice reminder]
Step 3: lead-triage                [if new inbound lead: score]
Step 4: customer-pulse             [aggregate PayPal/HubSpot feedback]
Step 5: sop-writer                 [document new process]
Step 6: smb-onboard                [if onboarding new employee/tool]
Step 7: customer-escalation        [if customer escalation exists]
Step 8: draft-response             [reply to customer]
```

Output: end-to-end weekly/monthly ops loop. **Compliance + legal hooks** activated when contracts/SOX.

### Phase 3 — Cross-Reference Index (Not Duplication)

This skill **never duplicates** analytic methods. Quick lookup:

| Category | Source | Where |
|----------|--------|-------|
| **Comparable analysis (operating metrics, multiples)** | comps-analysis | `external/anthropic-financial-services/comps-analysis/SKILL.md` |
| **DCF (WACC, sensitivity, terminal value)** | dcf-model | `external/anthropic-financial-services/dcf-model/SKILL.md` |
| **LBO (sources & uses, debt schedule, returns)** | lbo-model | `external/anthropic-financial-services/lbo-model/SKILL.md` |
| **Datapack construction (traceable numbers)** | datapack-builder | `external/anthropic-financial-services/datapack-builder/SKILL.md` |
| **3-statement model** | 3-statement-model | `external/anthropic-financial-services/3-statement-model/SKILL.md` |
| **Earnings analysis (8-12 page)** | earnings-analysis | `external/anthropic-financial-services/earnings-analysis/SKILL.md` |
| **Initiating coverage (8-12 page institutional)** | initiating-coverage | `external/anthropic-financial-services/initiating-coverage/SKILL.md` |
| **Pitch deck (10-15 slides)** | pitch-deck | `external/anthropic-financial-services/pitch-deck/SKILL.md` |
| **Sales objection handling (MEDDIC/BANT)** | objection-handler | `community/sales-marketing/objection-handler/SKILL.md` |
| **OKR alignment** | okr-alignment-checker | `community/business-operations/okr-alignment-checker/SKILL.md` |
| **SOP writing** | sop-writer | `community/business-operations/sop-writer/SKILL.md` |
| **Crisis communications** | crisis-comms-playbook | `community/business-operations/crisis-comms-playbook/SKILL.md` |
| **Legal risk (severity × likelihood)** | legal-risk-assessment | `external/knowledge-work-plugins/legal/skills/legal-risk-assessment/SKILL.md` |
| **NDA triage** | triage-nda | `external/knowledge-work-plugins/legal/skills/triage-nda/SKILL.md` |
| **Contract review** | review-contract | `external/knowledge-work-plugins/legal/skills/review-contract/SKILL.md` |
| **Compliance check** | compliance-check | `external/knowledge-work-plugins/legal/skills/compliance-check/SKILL.md` |

For an end-to-end pipeline, the orchestrator guarantees **at least one legal/compliance gate**:
- B1 (Coverage): Step 8 `review-contract` if material agreements involved
- B2 (M&A): Steps 6-8 are all legal (`review-contract`, `triage-nda`, `legal-risk-assessment`) — **mandatory**
- B3 (Pitch): No legal gate by default — but if your deck references LOIs/NDAs, insert `triage-nda`
- B4 (SMB): Compliance triggered if SOX/audit-relevant (insert `audit-support`)

## 💡 Best Practices

### Do

- **Always ask role first** (analyst / banker / founder / SMB owner / operator)
- **Always chain to one legal gate** if any financial deliverable touches contracts
- **Always set 8-12 page target for B1 / 10-15 slide for B3** — institutional VC-grade output
- **Always trace numbers to datapack** in B1/B2 — never write figures that can't be sourced
- **Always include sensitivity tables** in DCF/LBO outputs (WACC range, multiple range)
- **Use comps-analysis + dcf-model together** when valuation = triangulation, never pick one

### Don't

- **Don't run all 164 skills** — chain ≤ 8 steps per pipeline
- **Don't write pitch deck without comps analysis** — top-down sizing without bottom-up check is slop
- **Don't skip legal review in B2** — M&A without contract/NDA/legal-risk gates is malpractice
- **Don't confuse B1 (Coverage) with B3 (Pitch)** — coverage is for buy-side analysts, pitch is for selling
- **Don't invoke legal skill without `compliance-check` if SOX/healthcare/financial-product** — those need compliance first

## 🔀 Routing Decision Table (Full 164-row)

```
User says                              → Path / Entry skill
──────────────────────────────────────────────────────────
"write research report on X"          → B1 (initiating-coverage)
"Q3 earnings come out tomorrow"       → B1 (earnings-analysis)
"build comp set for tech sector"      → B1 (comps-analysis)
"model our 3 statements"              → B1 (3-statement-model)
"build a DCF on X"                    → B1 / B2 (dcf-model)
"we're buying Y - LBO model"          → B2 (lbo-model)
"evaluate this acquisition"           → B2 (deal-sourcing → comps → DCF → LBO)
"help me on a Series A deck"          → B3 (office-hours → pitch-deck)
"refresh our pitch before QBR"        → B3 (deck-refresh)
"review this NDA"                     → 1-shot (triage-nda)
"contract looks weird - flag risks"   → 1-shot (review-contract)
"draft an offer letter"               → 1-shot (draft-offer)
"performance review prep"             → 1-shot (performance-review)
"close the books this month"          → B4 (close-management + variance-analysis)
"draft overdue invoice reminder"      → B4 (invoice-chase)
"set up payroll"                      → B4 (close-management + audit-support)
"onboard new customer"                → B4 (customer-pulse → draft-response)
"weekly metrics review"               → 1-shot (metrics-review) — product, not business
"OKRs make sense?"                    → 1-shot (okr-alignment-checker)
"postmortem on the lost deal"         → 1-shot (learn-from-loss)
```

## 🔧 Version Sync (Upstream Drift Protection)

Same mechanism as `design-orchestrator`. Run after any orchestrator change OR weekly:

```bash
python3 community/business-orchestrator/scripts/version-sync-check.py
```

Flags drift in referenced upstream skills (comps-analysis, dcf-model, pitch-deck, etc). Exit 0 = aligned, 1 = drift, 2 = errors.

**Upstream bumps to watch for:**
- `comps-analysis` / `dcf-model` / `lbo-model` (anthropic-financial-services) — methodology drift is rare but breaking-change exists
- `pitch-deck` / `initiating-coverage` — template structure changes
- `triage-nda` / `review-contract` — legal taxonomy drift
- `okr-alignment-checker` — framework version

## 📚 Resources

* [Routing decision table](./references/routing-table.md) — 13-subcluster × path coverage
* [Orchestration patterns](./references/orchestration-patterns.md) — 4 paths in detail
* [Method cross-reference](./references/method-index.md) — analytic methods (DRY)
* [Case studies](./examples/case-studies.md) — 4 paths in real scenarios
* [Version sync script](./scripts/version-sync-check.py) — upstream drift detector

---

**差异化定位**: 164 个 business skill 解决单点问题; business-orchestrator 是**调度层**. 0 内容重复, 100% DRY. 跟 `design-orchestrator` 同样的方法论 — 路由 + 编排 + 引用.
