---
name: contract-risk-highlighter
description: Contract risk analyzer - flags legal landmines in 30min (saves 6h legal review)
version: 1.0.0
tags: [legal, contract-review, risk-analysis, compliance, procurement, ROI-9.0]
---

# Contract Risk Highlighter

**ROI:** 9.0/10 - Saves 6h → 30min per contract with automated risk flagging

AI-powered contract review focusing on liability, indemnity, termination, and negotiation leverage.

---

## Risk Categories

### 1. Liability & Indemnity (High Risk)

**Red flags:**
- ❌ **Unlimited liability** ("Party A liable for all damages")
  - **Fix:** Cap at 12-month contract value
- ❌ **Broad indemnification** ("Indemnify for any third-party claims")
  - **Fix:** Limit to IP infringement + gross negligence
- ❌ **Consequential damages** ("Including lost profits, business interruption")
  - **Fix:** Exclude consequential/punitive damages

---

### 2. Termination Rights (Medium Risk)

**Red flags:**
- ⚠️ **Termination for convenience** (Customer can cancel anytime)
  - **Fix:** 90-day notice + early termination fee
- ⚠️ **Auto-renewal without notice** (Renews unless 180-day notice)
  - **Fix:** 60-day notice window

---

### 3. Data & Privacy (High Risk)

**Red flags:**
- ❌ **Data ownership ambiguity** ("All data property of Customer")
  - **Fix:** Customer data = theirs, anonymized aggregates = ours
- ❌ **GDPR non-compliance** (No data processing addendum)
  - **Fix:** Add DPA, appoint DPO

---

### 4. Payment Terms (Low Risk)

**Green flags:**
- ✅ **Net 30** (industry standard)
- ✅ **Annual upfront** (better than quarterly)

**Yellow flags:**
- ⚠️ **Net 60-90** (negotiate to Net 30)

---

## Analysis Template

**Contract:** [Vendor/Customer Name] - [Service Description]
**Value:** $[X] annually
**Term:** [X] years
**Review Date:** [Date]

### Risk Summary

| Category | Risk Level | Key Issues | Action |
|----------|------------|------------|--------|
| Liability | 🔴 High | Unlimited liability, broad indemnity | **Must fix** |
| Termination | 🟡 Medium | Term for convenience clause | Negotiate |
| Data/Privacy | 🟢 Low | Standard DPA included | Accept |
| Payment | 🟢 Low | Net 30, annual billing | Accept |

### Overall Assessment: 🟡 **Medium Risk - Negotiate**

### Must-Have Changes (Dealbreakers)

1. **Cap liability** at 12-month fees ($[X])
2. **Limit indemnity** to IP + gross negligence
3. **Exclude consequential damages**

### Nice-to-Have Changes

1. Reduce termination notice to 60 days
2. Add service level credits (if SLA miss >5%)

### Fallback Position

If they won't budge on liability cap:
- Require $[X]M insurance policy
- Add audit rights (verify their coverage)

---

## Negotiation Playbook

**Vendor contract (we're buying):**
- Aggressive on liability (we take the risk)
- Flexible on payment terms (if discount offered)

**Customer contract (we're selling):**
- Protect our liability (cap aggressively)
- Flexible on termination (if high retention confidence)

---

## Red Flag Checklist

- [ ] Liability unlimited
- [ ] Indemnity too broad
- [ ] Consequential damages included
- [ ] IP ownership ambiguous
- [ ] Non-compete clause (unreasonable scope)
- [ ] Exclusive partnership (lock-in risk)
- [ ] Force majeure missing (COVID lesson)
- [ ] Governing law in unfavorable jurisdiction

---

## References

- ai-boost: Legal Analyst prompt
- IRAC methodology (Issue, Rule, Application, Conclusion)
- Standard contract templates (Cooley GO, Y Combinator SAFE)
