---
name: churn-risk-playbook
description: Customer churn prevention playbook with health scoring - saves 4h→15min weekly at-risk account review. Use when user wants to "save a churn account", "客户要流失", "客户用得越来越少", "续约谈判", "降级信号", "QBR prep", "客户要降级", "客户要退出", "客户健康度低", "客户没回应", "客户用了下个月就停了", "save churn", "renewal negotiation", "account at risk", "expansion qualification", "executive intervention". Distinguishes from objection-handler (mid-deal objections) — this is post-sale retention.
version: 2.0.0
tags: [customer-success, churn-prevention, health-scoring, retention, expansion, QBR, ROI-9.5, community, arena-winner]
---

# Churn Risk Playbook

**ROI:** 9.5/10 - Saves 4h → 15min for weekly at-risk account review

Systematic churn prevention framework using health scoring, leading indicators, and intervention playbooks. Turns reactive firefighting into proactive retention.

---

## 🎯 适用场景与触发

### 6 类典型场景

| # | 场景 | 触发词 |
|---|---|---|
| 1 | **客户流失预警** | 客户要流失 / 客户要退出 / 客户用得越来越少 / save churn |
| 2 | **续约谈判** | 续约谈判 / 续签 / 续约前评估 / renewal negotiation |
| 3 | **降级信号** | 客户要降级 / 客户预算减半 / 客户说用不到那么多 |
| 4 | **健康度体检** | 客户健康度低 / 客户没回应 / health check 账户 |
| 5 | **扩张机会** | 客户用得好要 upsell / 客户预算增 / expansion qualification |
| 6 | **QBR 准备** | QBR prep / 季度业务回顾 / 高管对话 |

### 6 类常见痛点

- **事后救火** — 客户走了才知道
- **健康分拍脑袋** — 没有量化指标
- **预警不到位** — 续约前 30 天才发现
- **救火动作随机** — 凭直觉联系客户
- **预防动作缺失** — 只救火不防
- **原因分析不深** — 不知道「为什么走」

### 8 类期望效果

- 健康分量化(0-100 + 4 pillar 加权)
- 风险分级(Tier 1 红 / Tier 2 黄 / Tier 3 绿)
- 提前 90 天预警(leading indicators)
- 标准 Playbook A/B/C 干预
- Executive intervention 触发条件明确
- 主动扩张机会识别
- 季度复盘 + 流失原因统计
- 可视化 account health dashboard

---

## 🚨 边界

| 类型 | 触发 | 动作 |
|---|---|---|
| **未成交客户** | 用户问「如何赢得新客户」 | 不接,转 objection-handler / sales-orchestrator |
| **纯产品 bug** | 客户要走是因为产品功能缺失 | 转 engineering-orchestrator 排期 + 本 skill 维护 |
| **法律/合规原因** | 客户走是因为合规问题 | 转律师 + 内部流程 audit |
| **沉默 ≠ 同意** | 客户无回复 ≥ 30 天或多次回避 | 不得自动升级到高管/私人渠道；先确认沉默原因（休假、时区、组织变更、沟通偏好），按客户首选渠道在冷却期后再联系 |
| **越权画像** | LinkedIn 等渠道去推断个人状态、裁员、绩效 | 禁止；仅允许使用客户已公开且与业务直接相关的信息 |
| **个人绩效归因** | 复盘结论用于客户内部个人绩效、晋升、降级 | 停止本流程；输出仅用于系统/流程/交付物改进，由授权 HR/管理流程评估个人 |
| **跨境/PIPL 数据** | 客户数据跨境传输或包含敏感个人信息 | 启动 PWSB 数据分级 + PIPL Art.38/39 复核；未确认前不输出健康分 |
| **未验证预测** | 把 leading indicators 当成“必发生” | 不得输出确定性预测；按启发式 + 人工复核 + 验证协议标注 |

---

## 📥 启动前信息收集

| 信息 | 必要性 | 缺失时默认 |
|---|---|---|
| **账户名 + 历史合同** | 必须 | 不开始,问 |
| **4 pillar 原始数据**(Usage / Engagement / Support / Outcome) | **必须** | 输出 `Insufficient data — cannot score`，**禁止补 0、不允许补默认值、不允许把 N/A 当 0** |
| **数据来源 + 观测窗口 + 采集时间** | 必须 | 不接受估算 |
| **客户关系图**(Exec / Champion / 用户) | 必须 | 不假设 1+2-3，必须由用户提供 |
| **已尝试过的救火动作** | 必须 | 不假设 0；缺失则问 |
| **竞品动态**(若知道) | 推荐 | 不假设 |

> **健康分最低门槛：必须同时具备 4 pillar 的真实原始数据 + 观测窗口 + 数据来源 + 时间戳，否则输出 `Insufficient data`、禁止打分、禁止给出 Tier 与动作。**

---

## 🔗 后续落地动作

| 动作 | 触发 | 默认 |
|---|---|---|
| **存档案例** | 救火成功/失败 | 询问「这次流失复盘要不要存到 `references/churn-cases.md`?」 |
| **更新健康分阈值** | 3 次使用后 | 建议「根据流失实际原因,调整 4 pillar 权重」 |
| **预防 vs 救火比例** | 季度复盘 | 主动建议「本季度救火 80% / 预防 20%,是不是要倒过来?」 |
| **跨团队升级** | 多账户同时流失 | 主动建议「要不要触发 product/engineering 走 [通用流程]?」 |

---

## 📇 Contact Safety Gate（任何客户触达前必过）

> 失败任一条 = 停止该触达；不通过沉默或绕渠道绕过。

- **渠道偏好**：使用客户在合同或既往沟通中已确认的渠道；未确认时默认邮件，且首次必须以邮件开场。
- **同意状态**：客户必须就本触达目的表达过同意；沉默不构成同意。
- **合法业务目的**：每次触达能说出 1 句具体业务目的与客户可获价值。
- **最大尝试次数**：单一议题 7 个自然日内 ≤ 2 次；超限须冷却 ≥ 14 天。
- **冷却期**：被忽略 ≥ 30 天再升级到下一渠道或高管，需先内部评审是否还存在业务目的。
- **退订与拒绝**：客户明确退订、要求暂停或拒绝联系后立即停止非必要触达，并记录在 CRM。
- **跨级联系**：未取得关系授权或合规批准前不得联系 CFO/Exec；联系前记录理由与授权人。
- **个人信息**：不得使用 LinkedIn 等渠道推断个人状态、裁员、绩效；只使用客户已公开且与业务直接相关的事实。
- **跨境**：跨境触达或涉及个人敏感信息时走 PWSB 数据分级 + PIPL Art.38/39 复核。

### 主公 → skill 反馈通道

| 反馈 | skill 动作 |
|---|---|
| 「健康分不对」 | 询问「哪个 pillar 高估/低估?」调整权重 |
| 「Playbook 没用」 | 询问「尝试了哪一步? 客户反应?」重做诊断 |
| 「没救回来」 | 询问「最后流失原因?」更新 leading indicators |
| 「救回来了」 | 询问「关键动作是哪个?」提炼为新 Playbook |

### skill → 主公主动迭代

| 周期 | 内容 |
|---|---|
| 每周 | 「本周 at-risk 账户 Top 3」 |
| 每月 | 「本月 Tier 1 数量趋势 + 救火成功率」 |
| 每季度 | 「本季度流失原因 Top 5 + 建议调整的权重」 |
| 半年 | 「健康分模型是否仍 calibration? 重新评估指标权重」 |

---

## 🛠 自检 Checklist(每次输出前)

- [ ] 4 pillar 真实原始数据 + 观测窗口 + 来源 + 时间戳 全部齐全？缺任一则输出 `Insufficient data`
- [ ] 健康分每个 pillar 都标注了来源、窗口、采集时间、缺失字段、置信度？
- [ ] Tier 分级明确？Tier 编号与 `references/health-scoring-guide.md` 矩阵一致？
- [ ] 预测性语句是否已降级为「未验证启发式」？未依赖 `60–90 天`、`3x` 等确定性数字？
- [ ] 任何对外触达都过 Contact Safety Gate？退订 / 拒绝后停止非必要触达？
- [ ] 救火动作对应 Playbook 编号？
- [ ] 时间窗明确?(48h/1 周/2 周)
- [ ] Executive intervention 触发条件满足 + 已取得授权？
- [ ] Expansion 机会识别？只对 Tier 3 Healthy？
- [ ] Next step 有 Owner + 日期？
- [ ] 数据能驱动复盘(流失原因分类)？
- [ ] 个人绩效归因被排除？跨境 / 个人信息走 PWSB 复核？

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

**Leading indicators** (unverified heuristics — not validated predictions; treat as triage signals, not forecast):
- Usage decline >20% MoM
- No exec contact >45 days
- Support escalations
- Champion turnover
- Competitive eval signals

> ⚠️ 本 skill 不提供经过验证的 churn 预测模型。leading indicators 是候选启发式，必须配合人工复核、明确的 churn outcome 定义、precision/recall 评估与时间外推验证后才可作为决策依据。`3+ indicators = playbook activation` 是建议阈值，不是验证过的触发器。

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

**Red flag:** Customer cancels/reschedules QBR 2x — 提示需复核健康度，**不等于自动判定 churn risk**；先确认客户偏好与原因再走 Contact Safety Gate 升级。

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
