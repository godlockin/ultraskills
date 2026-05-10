---
name: objection-handler
description: Sales objection handling framework using MEDDIC/BANT - converts 1h prep to 5min per call
version: 1.0.0
tags: [sales, objection-handling, MEDDIC, BANT, deal-acceleration, ROI-9.5]
---

# Objection Handler

**ROI:** 9.5/10 - Saves 1h prep → 5min per sales call

High-frequency sales skill that instantly generates objection responses using proven frameworks (MEDDIC, BANT, SPIN). Used before every sales call, demo, or negotiation.

---

## When to Use

- **Pre-call prep**: Anticipate objections for upcoming sales calls
- **Live call recovery**: Real-time objection response during demos
- **Proposal defense**: Handle pricing/contract pushback
- **Deal rescue**: Unstick stalled opportunities
- **Team training**: Build objection handling playbooks

**Frequency:** Every sales interaction (daily for AEs/SEs)

---

## Core Frameworks

### MEDDIC Qualification
- **M**etrics: Quantify business impact ("reduce churn 15% → save $2M/yr")
- **E**conomic Buyer: Identify budget authority
- **D**ecision Criteria: Map evaluation rubric
- **D**ecision Process: Timeline + approval chain
- **I**dentify Pain: Root cause, not symptom
- **C**hampion: Internal advocate with power/credibility

### BANT Screening
- **B**udget: Confirmed budget vs estimated range
- **A**uthority: Decision maker(s) engaged
- **N**eed: Business pain quantified
- **T**imeline: Buying window defined

### Objection Categories
1. **Price** - "Too expensive"
2. **Authority** - "Need to check with [person]"
3. **Need** - "Not a priority right now"
4. **Trust** - "Unproven solution"
5. **Timing** - "Call us next quarter"
6. **Competition** - "Already using [competitor]"

---

## Usage

**Input format:**
```
Objection: [exact words prospect said]
Context: [deal stage, MEDDIC score, competitive situation]
Goal: [close this week / keep alive / book next meeting]
```

**Output:** 3-tier response:
1. **Acknowledge** - Validate concern (don't dismiss)
2. **Reframe** - Shift perspective using metrics/case studies
3. **Advance** - Propose next step (meeting, trial, reference call)

---

## Example: Price Objection

**Prospect:** "Your pricing is 40% higher than [Competitor X]."

**Bad response:** "We're worth it because we have better features."
*(Defensive, feature-dump, no business case)*

**MEDDIC response:**

**Acknowledge:**
"Thanks for sharing that benchmark. Price discipline is critical when you're managing [their budget size]."

**Reframe (Metrics):**
"Two questions help here:
1. What's the cost of your current churn rate? [If 20% annual at $5M ARR = $1M lost]
2. What's a 5-point churn reduction worth? [Our avg customer sees 8-point drop in 6mo]

At your scale, that's $400K retained revenue in year 1. Our price delta is $50K — 8x ROI."

**Advance (Champion development):**
"Would it help to connect you with [Similar Customer], who had the same concern? They're now at 120% net retention and just renewed early."

---

## Common Objection Playbook

### "Not a priority right now"

**Diagnose:** BANT fail - no urgency

**SPIN question:**
"Help me understand: what would need to happen for this to become top-3 priority?"
*(Uncover the pain threshold)*

**Reframe:**
"Our customers who wait 6 months typically lose [X metric]. What if we scoped a 30-day pilot to prove value before you commit?"

---

### "We're already using [Competitor]"

**Diagnose:** Competitive displacement needed

**MEDDIC check:**
1. Who owns the renewal decision? (Economic Buyer)
2. What's missing in current solution? (Identify Pain)
3. When's their contract up? (Decision Process)

**Battle card response:**
"Most [Competitor] customers we work with keep them for [legacy use case] and add us for [differentiated value].

Example: [Customer X] runs both in parallel — [Competitor] for [commodity task], us for [high-value workflow]. Their team says the combo gives them [specific outcome]."

**Advance:**
"Would a side-by-side ROI model help? We can show exact cost/benefit of running both vs switching."

---

### "Need to check with my boss"

**Diagnose:** BANT fail - no Authority

**Acknowledge:**
"Absolutely — this decision needs exec buy-in."

**Champion building:**
"What's the best way to help you sell this internally?
- Would a 1-pager business case help?
- Should we do a 15min exec briefing with [boss name]?
- Do you need reference calls from similar companies?"

**MEDDIC alignment:**
"Walk me through the approval process: who reviews, what criteria matter most, and when's the decision meeting?"

---

## Advanced Techniques

### Pre-empting Objections

Before they say it:
"Most prospects at this stage ask about [common objection]. Let me address that upfront..."
*(Shows you've seen it before, builds credibility)*

### The Columbo Close

After handling objection:
"If we solve [this concern], is there anything else preventing us from moving forward?"
*(Flushes out hidden blockers)*

### Social Proof Stacking

"3 companies in [their industry] had the same concern:
1. [Company A] - [outcome in X months]
2. [Company B] - [metric improvement]
3. [Company C] - [case study link]

Would any of these be helpful references?"

---

## Anti-Patterns (Never Do)

❌ **Argue with prospect** - "Actually, you're wrong about..."
❌ **Feature dump** - "But we have 47 integrations!"
❌ **Discount immediately** - "I can do 20% off today"
❌ **Ignore the objection** - "Let's talk about something else"
❌ **Give up** - "Okay, call us if things change"

✅ **Do instead:**
- Ask clarifying questions (SPIN)
- Quantify with metrics (MEDDIC)
- Share analogous customer stories
- Propose micro-commitment (pilot, reference call, exec meeting)

---

## Integration with Sales Process

| Deal Stage | Objection Focus | MEDDIC Priority |
|------------|----------------|-----------------|
| Discovery | "Not a priority" | Identify Pain |
| Demo | "Missing feature X" | Decision Criteria |
| Proposal | "Price too high" | Metrics + Economic Buyer |
| Negotiation | "Contract terms" | Champion + Decision Process |
| Closing | "Need more time" | Timeline + Authority |

---

## Team Training Use

**Build objection library:**
1. Collect real objections from lost deals (CRM notes)
2. Workshop responses using this framework
3. A/B test responses across team
4. Update battle cards with winners

**Role-play drill:**
- AE plays prospect with hardest objection
- SE responds using MEDDIC framework
- Team scores response (1-10)
- Iterate until 9+ score

---

## Success Metrics

Track in CRM:
- **Objection → Close rate** (target: >40% for qualified deals)
- **Time to objection resolution** (target: <1 business day)
- **Objection recurrence** (same objection twice = process failure)
- **Discount rate** (lower = better value articulation)

**Benchmark:** Top AEs handle 80% of objections without discounting.

---

## References

- MEDDIC qualification framework
- BANT sales methodology
- SPIN Selling (Rackham)
- Challenger Sale (Dixon/Adamson)

**Sources:**
- ai-boost/awesome-prompts: Sales Strategist prompt
- Proven sales frameworks from enterprise SaaS

---

## Examples

See `examples/` directory:
- Price objection (SaaS 7-figure deal)
- Competitive displacement (vs market leader)
- Authority objection (multi-stakeholder)
- Timing objection (budget cycle mismatch)
