---
name: feature-prioritization
description: Feature prioritization (RICE/ICE/KANO) - rank backlog in 15min, saves 2h
version: 1.0.0
tags: [product-management, prioritization, rice, ice, roadmap, backlog, ROI-8.5]
---

# Feature Prioritization

**ROI:** 8.5/10 - Saves 2h → 15min with objective scoring frameworks

Ranks features using RICE, ICE, or KANO to maximize impact.

---

## RICE Framework (Most Common)

**Formula:** (Reach × Impact × Confidence) ÷ Effort

**Definitions:**
- **Reach:** Users affected per time period (e.g., 1000/month)
- **Impact:** Value per user (0.25=minimal, 0.5=low, 1=med, 2=high, 3=massive)
- **Confidence:** % certainty (100%=proven, 80%=high, 50%=medium, <50%=low)
- **Effort:** Person-months (0.5=week, 1=month, 3=quarter)

**Example:**

| Feature | Reach | Impact | Confidence | Effort | RICE | Rank |
|---------|-------|--------|------------|--------|------|------|
| Saved cards | 1000/mo | 3 | 80% | 2mo | 120 | #1 |
| Dark mode | 500/mo | 1 | 100% | 0.5mo | 100 | #2 |
| API v2 | 50/mo | 2 | 50% | 3mo | 16.7 | #3 |

**Build order:** Saved cards > Dark mode > API v2

---

## ICE Framework (Simpler)

**Formula:** (Impact + Confidence + Ease) ÷ 3

**Scoring (1-10 scale):**
- **Impact:** Business value (revenue, retention, NPS)
- **Confidence:** How sure you are
- **Ease:** Inverse of effort (easy=10, hard=1)

**Example:**

| Feature | Impact | Confidence | Ease | ICE | Rank |
|---------|--------|------------|------|-----|------|
| Saved cards | 9 | 8 | 4 | 7.0 | #1 |
| Dark mode | 5 | 10 | 9 | 8.0 | #2 |
| API v2 | 7 | 5 | 2 | 4.7 | #3 |

---

## KANO Model (Feature Type)

**Categories:**
- **Must-Have:** Absence = dissatisfaction (e.g., security, uptime)
- **Performance:** More = better (e.g., speed, accuracy)
- **Delight:** Unexpected wow (e.g., easter eggs, animations)
- **Indifferent:** Doesn't move the needle
- **Reverse:** Some users hate it

**Strategy:**
1. Ship all Must-Haves first
2. Optimize Performance features
3. Sprinkle Delighters
4. Skip Indifferent/Reverse

---

## Decision Matrix (When to Use)

| Scenario | Best Framework |
|----------|----------------|
| Data-driven org | RICE (quantitative) |
| Fast-moving startup | ICE (quick estimates) |
| User satisfaction focus | KANO (feature type) |
| Limited resources | RICE (ROI-focused) |

---

## References

- Intercom RICE framework
- Sean McBride ICE scoring
- KANO model (Noriaki Kano)
- ai-boost: Product Manager prompt
