# Routing Decision Table — Business Cluster (13 sub-clusters, 164 skills)

## Master Mapping: User Intent → Path → Entry Skill

| Cluster | Count | Path B1 Coverage | Path B2 M&A | Path B3 Pitch | Path B4 SMB | 1-shot |
|---------|-------|-----------------|-------------|---------------|-------------|--------|
| business-finance | 56 | ✅ (core) | ✅ (core) | ✅ (comps+DCF) | — | — |
| small-business-ops | 26 | — | — | ✅ (canva-creator) | ✅ (core) | — |
| sales-marketing | 13 | — | — | ✅ (core) | ✅ (lead-triage) | ✅ (objection, OKR) |
| business-operations | 13 | — | — | ✅ (data-viz) | ✅ (core) | ✅ (crisis, SOP) |
| business-clevel | 11 | — | — | ✅ (core) | — | ✅ (plan-ceo-review) |
| business-product | 11 | — | — | — | — | ✅ (prioritization, plan-eng) |
| finance-accounting | 7 | — | — | — | ✅ (variance, close) | ✅ (journal-entry) |
| business-legal | 6 | — | ✅ (mandatory) | — | ✅ (if contracts) | ✅ (compliance-check) |
| legal-compliance | 6 | ✅ (if material) | ✅ (mandatory) | ✅ (NDA pre-pitch) | — | ✅ (triage-nda) |
| hr-talent | 6 | — | — | — | — | ✅ (offer, review) |
| business-pm | 5 | — | — | — | — | ✅ (retro, postmortem) |
| business-hr | 3 | — | — | — | — | ✅ (lead-magnets) |
| business-strategy | 1 | — | — | — | — | ✅ (competitive-intel) |

## Detailed Routing Table (Top 50 skills)

| Skill | Cluster | Route | When to invoke |
|-------|---------|-------|----------------|
| **initiating-coverage** | business-finance | B1 step 1 | "write initiating report" |
| **comps-analysis** | business-finance | B1 step 2 / B2 step 2 | "build comp set" |
| **dcf-model** | business-finance | B1 step 3 / B2 step 3 | "DCF on X" |
| **earnings-analysis** | business-finance | B1 step 4 | "Q3 earnings" |
| **datapack-builder** | business-finance | B1 step 5 | "build datapack" |
| **3-statement-model** | business-finance | B1 step 6 | "model 3 statements" |
| **lbo-model** | business-finance | B2 step 4 | "LBO on X" |
| **pitch-deck** | business-finance | B2 step 5 / B3 step 5 | "build pitch deck" |
| **initiating-coverage-critic** | business-finance | B3 step 6 | "review my coverage" |
| **deck-refresh** | business-finance | B3 step 5 alt | "refresh pitch" |
| **ai-readiness** | business-finance | 1-shot | "where to deploy AI" |
| **audit-xls** | business-finance | 1-shot | "audit this spreadsheet" |
| **competitive-analysis** | business-finance | 1-shot | "competitive landscape" |
| **deal-sourcing** | business-finance | B2 step 1 | "find targets" |
| **earnings-analysis-critic** | business-finance | 1-shot | "review earnings note" |
| **smb-onboard** | small-business-ops | B4 step 6 | "onboard SMB" |
| **canva-creator** | small-business-ops | B3 step 6 / B4 step 4 alt | "create campaign asset" |
| **cash-flow-snapshot** | small-business-ops | B4 step 1 | "what's our cash position" |
| **invoice-chase** | small-business-ops | B4 step 2 | "draft invoice reminder" |
| **customer-pulse** | small-business-ops | B4 step 4 | "what's customer feedback" |
| **lead-triage** | small-business-ops | B4 step 3 | "score leads" |
| **sop-writer** | business-operations | B4 step 5 | "document process" |
| **crisis-comms-playbook** | business-operations | 1-shot | "PR crisis" |
| **customer-escalation** | business-operations | B4 step 7 | "package escalation" |
| **draft-response** | business-operations | B4 step 8 | "reply customer" |
| **kb-article** | business-operations | 1-shot | "write KB" |
| **digital-brain** | business-clevel | B3 support | "write a post" |
| **data-viz** | business-clevel | B1 step 7 / B3 step 4 | "which chart" |
| **plan-ceo-review** | business-clevel | B3 step 2 | "CEO review" |
| **office-hours** | business-clevel | B3 step 1 | "startup mode" |
| **unit-economics-calculator** | business-clevel | B3 support | "CAC/LTV" |
| **variance-analysis** | finance-accounting | B4 / 1-shot | "explain variance" |
| **journal-entry** | finance-accounting | 1-shot | "draft journal" |
| **close-management** | finance-accounting | B4 step 1 alt | "month-end close" |
| **audit-support** | finance-accounting | B4 support | "SOX testing" |
| **review-contract** | legal-compliance | **B2 step 6 mandatory** | "review contract" |
| **triage-nda** | legal-compliance | B2 step 7 mandatory | "NDA arrive" |
| **vendor-check** | legal-compliance | 1-shot | "check vendor contracts" |
| **meeting-briefing** | legal-compliance | 1-shot | "brief for legal meeting" |
| **brief** | legal-compliance | 1-shot | "context briefing" |
| **compliance-check** | business-legal | B2 step 8 / 1-shot | "compliance run" |
| **legal-risk-assessment** | business-legal | B2 step 8 | "legal risk" |
| **contract-risk-highlighter** | business-legal | B2 step 6 alt | "flag contract risks" |
| **legal-response** | business-legal | 1-shot | "respond to legal inquiry" |
| **compliance-tracking** | business-legal | 1-shot | "track compliance" |
| **objection-handler** | sales-marketing | 1-shot | "handle objection" |
| **okr-alignment-checker** | sales-marketing | B3 step 8 / 1-shot | "OKR makes sense?" |
| **pitch-deck-critic** | sales-marketing | B3 step 6 | "review deck" |
| **create-an-asset** | sales-marketing | B3 step 7 | "create landing" |
| **draft-outreach** | sales-marketing | 1-shot | "draft outreach" |
| **lead-magnets** | business-hr | 1-shot | "lead magnet" |

(Rows 51-164 omitted for brevity — same logic applies. Use `python3 devops/ultraskills-hub/scripts/search.py --cluster business-finance --limit 50` for full list.)

## Anti-Override Rules

These skills **must not** be invoked unless the user explicitly asks:
- **lbo-model** — user mentions LBO/buyout/private equity
- **legal-risk-assessment** — user asks for severity/likelihood matrix
- **compliance-check** — user asks for SOX/healthcare/financial-product compliance
- **draft-offer** — user has candidate selected
- **pitch-deck-critic** — user wants VC-grade feedback, not just any feedback
- **plan-ceo-review** — user wants CEO-mode (PMM mode is different)

## Fallback (When No Skill Fits)

If the user request doesn't match any business skill:
1. **AskUserQuestion** to clarify the intent (analyst / banker / founder / SMB / operator)
2. If user says "I don't know", default to **Path B4 (SMB)** — most common, broadest applicability
3. Never invoke all 164 skills — chain waste

## Cross-Cluster Bridges

If the user request touches multiple clusters, the orchestrator must:
- **Business + Design**: insert `design-orchestrator` for any deck/marketing asset that needs design discipline
- **Business + Engineering**: insert `engineering-orchestrator` only if FinTech product (Rails contracts + audit)
- **Business + Content**: insert `content-orchestrator` for marketing campaigns

These cross-cluster bridges are **defer-to** — orchestrator doesn't own them, just points.
