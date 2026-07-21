# Method Cross-Reference Index (DRY, Not Duplication)

This index does **NOT** duplicate analytic methods. It points to the source skill. Read the source before applying.

## Comparable Analysis (Multiple × Trading / Transaction Comps)

| Method | Source |
|--------|--------|
| Trading multiples (EV/EBITDA, P/E, P/S) | comps-analysis |
| Transaction multiples (premium, structure) | comps-analysis |
| Operating metrics (revenue growth, margin, FCF conversion) | comps-analysis |
| Peer selection criteria | comps-analysis |

## DCF (Discounted Cash Flow)

| Method | Source |
|--------|--------|
| WACC build-up | dcf-model |
| Terminal value (Gordon / Exit multiple) | dcf-model |
| Sensitivity table (WACC × growth) | dcf-model |
| Mid-year / EOP conventions | dcf-model |
| Net debt / minority interest | dcf-model |

## LBO (Leveraged Buyout)

| Method | Source |
|--------|--------|
| Sources & Uses | lbo-model |
| Debt schedule (TLA / TLB / mezz / equity stub) | lbo-model |
| Returns waterfall (IRR / MOIC) | lbo-model |
| Equity stub sensitivity | lbo-model |
| Exit multiple scenario | lbo-model |

## Three Statement Modeling

| Method | Source |
|--------|--------|
| Income statement forecast | 3-statement-model |
| Balance sheet balancing | 3-statement-model |
| Cash flow waterfall | 3-statement-model |
| Working capital days | 3-statement-model |
| Debt schedule linking | 3-statement-model |

## Pitch Deck / Initiating Coverage (Structure)

| Component | Source |
|-----------|--------|
| 10-15 slide template | pitch-deck (anthropic-financial-services) |
| 8-12 page initiating template | initiating-coverage (anthropic-financial-services) |
| Earnings update template | earnings-analysis (anthropic-financial-services) |
| VC-grade feedback taxonomy | pitch-deck-critic (community) |

## Datapack Construction

| Method | Source |
|--------|--------|
| Source attribution | datapack-builder |
| Audit trail / numbers traceable | datapack-builder |
| Multi-source reconciliation | datapack-builder |
| Footnote conventions | datapack-builder |

## Sales / OKR / Operations

| Method | Source |
|--------|--------|
| MEDDIC / BANT objection handling | objection-handler (community) |
| OKR alignment cascading | okr-alignment-checker |
| SOP writing structure | sop-writer |
| Crisis comms 1-hour framework | crisis-comms-playbook |
| Customer escalation template | customer-escalation |
| Customer reply drafting | draft-response |

## Legal / Compliance (Mandatory in B2)

| Method | Source |
|--------|--------|
| Severity × Likelihood risk matrix | legal-risk-assessment |
| NDA triage GREEN/YELLOW/RED | triage-nda |
| Contract risk highlighter | review-contract (or contract-risk-highlighter) |
| Compliance check (SOX/healthcare/financial) | compliance-check |
| Vendor contract status check | vendor-check |
| Legal meeting briefing | meeting-briefing |

## Visualization Rules (Across All Paths)

| Chart Type | When | Source |
|------------|------|--------|
| Multiple bar chart | Compare peer group | data-viz |
| EPS bridge | Earnings surprises | data-viz |
| Waterfall | Sensitivity decomposition | data-viz |
| TAM/SAM/SOM funnel | Market sizing | data-viz |
| Heatmap | Risk matrix | data-viz |
| Sankey | Cash flow waterfall | data-viz |

## How to Apply

1. **Identify what method is needed** based on the brief
2. **Open the source skill's SKILL.md**
3. **Apply the methodology**, do not deviate
4. **Cross-check** with `compliance-check` if output touches healthcare/fintech/SOX

## Quick Reference Card

```
Method              → Source skill                      → Path
──────────────────────────────────────────────────────────────
Comps set           → comps-analysis                    → B1/B2/B3
DCF                 → dcf-model                         → B1/B2
LBO                 → lbo-model                         → B2
3-statement         → 3-statement-model                 → B1
Earnings bridge     → earnings-analysis                 → B1
Initiating report   → initiating-coverage               → B1
Pitch deck          → pitch-deck                        → B2/B3
Deck refresh        → deck-refresh                      → B3
VC feedback         → pitch-deck-critic                 → B3
Datapack            → datapack-builder                  → B1/B2
Cross-source audit  → datapack-builder + audit-xls      → B1/B2
Visualization       → data-viz                          → all paths
Objection           → objection-handler                 → sales
OKR sanity          → okr-alignment-checker             → B3
SOP                 → sop-writer                        → B4
Crisis              → crisis-comms-playbook             → 1-shot
Customer reply      → draft-response / customer-        → B4
                       escalation
Legal triage        → triage-nda                        → B2
Contract review     → review-contract / contract-risk-  → B2
                       highlighter
Legal risk          → legal-risk-assessment             → B2
Compliance check    → compliance-check                  → mandatory if SOX/HC/fin
```

## What This Orchestrator Does NOT Cover

The following are intentionally routed to **1-shot** (single skill), not pipeline:
- Daily standups / retrospectives / postmortems → `learn-from-loss` / `retro`
- Performance reviews → `performance-review`
- Offer letters → `draft-offer`
- Competitive intelligence (single query) → `competitive-intelligence` / `competitive-analysis`
- Plan reviews (engineering/PM) → `plan-eng-review` / `plan-ceo-review`

If you want to integrate those into a larger flow, route them as **sub-steps** of B1/B2/B3/B4 — but they are not pipeline primary.
