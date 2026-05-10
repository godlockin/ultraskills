---
name: user-story-mapper
description: User story mapping - visualizes user journeys in 20min, saves 3h planning
version: 1.0.0
tags: [product-management, user-stories, agile, roadmap, backlog, ROI-8.0]
---

# User Story Mapper

**ROI:** 8.0/10 - Saves 3h → 20min with structured story mapping

Creates visual user journey maps to prioritize features and plan releases.

---

## Story Map Structure

```
USER ACTIVITIES (Horizontal - Big steps in journey)
    ↓
USER TASKS (Vertical - Detailed steps under each activity)
    ↓
STORIES (Prioritized - MVP, V2, V3)
```

**Example: E-commerce Checkout**

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│  Browse     │  Add to     │  Checkout   │  Post-      │
│  Products   │  Cart       │             │  Purchase   │
├─────────────┼─────────────┼─────────────┼─────────────┤
│ Search      │ Add item    │ Enter addr  │ Track order │
│ Filter      │ Update qty  │ Payment     │ Review      │
│ View detail │ Save later  │ Promo code  │ Return      │
└─────────────┴─────────────┴─────────────┴─────────────┘

MVP (Must-have):
- Search + view detail + add to cart + basic checkout

V2 (Nice-to-have):
- Filter, update qty, promo code

V3 (Future):
- Save for later, reviews, returns
```

---

## Story Writing Template

**Format:** As a [user type], I want [action], so that [benefit]

**Example:**
- **Epic:** Checkout experience
- **Story:** As a customer, I want to save my payment info, so that future checkouts are faster
- **Acceptance Criteria:**
  - [ ] Can save card securely
  - [ ] Can select saved card at checkout
  - [ ] Can delete saved cards

---

## Prioritization (RICE on stories)

| Story | Reach | Impact | Confidence | Effort | RICE Score |
|-------|-------|--------|------------|--------|------------|
| Save payment | 1000/mo | 3 (high) | 80% | 2 weeks | 120 |
| Promo codes | 500/mo | 2 (med) | 100% | 1 week | 100 |
| Reviews | 200/mo | 1 (low) | 50% | 3 weeks | 3.3 |

**RICE = (Reach × Impact × Confidence) ÷ Effort**

**Prioritize:** Save payment > Promo codes > Reviews

---

## Release Planning

**MVP (Week 1-4):** Core checkout flow
**V2 (Week 5-8):** Enhancements (promo, saved cards)
**V3 (Week 9+):** Delight features (reviews, returns)

---

## References

- Jeff Patton's User Story Mapping
- Agile product roadmap frameworks
