# Usage Decline Recovery - SaaS Platform

**Account:** Enterprise software company, $120K ARR
**Health Score Drop:** 85 → 62 in 60 days
**Trigger:** DAU dropped from 180 users to 95 users (47% decline)

---

## Diagnosis Phase (Week 1)

### Data Analysis
- **Usage pattern:** Sharp drop starting March 1
- **Affected segment:** Engineering team (primary users)
- **Support tickets:** 3 tickets about "slow dashboard load times"
- **Champion status:** Still employed, but not responding

### Root Cause Investigation

**CSM outreach call:**

CSM: "I noticed usage dropped 50% in March. What changed?"

Customer (Engineering Manager): "Honestly, we switched to [Competitor Tool] for our daily standups. Your dashboard takes 30 seconds to load with our data volume. Our team got frustrated."

**Real issue:** Performance degradation, not adoption failure

---

## Intervention (Week 2-4)

### Immediate Actions

1. **Product escalation** (Day 1)
   - Alerted engineering team about performance issue
   - Reproduced bug with customer's data volume
   - Fast-tracked fix (2-week sprint)

2. **Quick win delivery** (Day 3)
   - Implemented database indexing (temp fix)
   - Load time: 30s → 8s (same day)
   - Called customer to confirm improvement

3. **Competitive retention** (Day 5)
   - Acknowledged [Competitor] strength (real-time collaboration)
   - Positioned complementary use: "[Competitor] for standups, us for analytics"
   - Offered integration: Pull [Competitor] data into our dashboards

### Re-engagement Campaign

**Week 2-3:** Power-user training
- 30-min session: "Advanced filters that [Competitor] can't do"
- Showcased 3 features they weren't using
- Engineering team found value in custom reporting

**Week 4:** Executive alignment
- QBR with VP Engineering
- Showed ROI: $180K saved annually in manual reporting
- Committed to quarterly roadmap sync

---

## Results (90-Day Follow-up)

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **DAU** | 95 | 165 | +74% |
| **Health Score** | 62 | 88 | +26 pts |
| **Support Tickets** | 3/mo | 0.5/mo | -83% |
| **Feature Adoption** | 40% | 68% | +28 pts |
| **NPS** | 6 | 8.5 | +2.5 |

**Outcome:**
- Renewed at $140K (+17% expansion)
- Became case study customer
- Referred 2 peer companies

---

## Key Lessons

1. **Usage decline ≠ adoption failure** - Investigate root cause (often product/performance)
2. **Quick wins matter** - 8s load time fix bought goodwill for 2-week permanent fix
3. **Acknowledge competition** - Don't fight, find complementary positioning
4. **Executive re-engagement** - QBR at yellow stage prevented red crisis

**Playbook refinement:**
Added "performance monitoring" as leading indicator (track p95 load times weekly)
