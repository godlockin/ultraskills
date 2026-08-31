# Business Orchestrator — 案例研究 (4 路径实操)

每个案例演示一次 orchestrator 从用户输入到完整 skill 链。

---

## 案例 B1: Coverage — "Initiating Coverage on Snowflake"

**用户输入**: "I need to initiate coverage on Snowflake (SNOW). Build me an 8-12 page institutional research report."

### Orchestrator 决策表

**role signal**: 分析师 / fund manager → Path B1
**deliverable**: 8-12 page initiating report
**single vs multi**: pipeline-worthy (multi skill)
**entry**: initiating-coverage

### 编排执行

| Step | Skill | 触发原因 | 输出 |
|------|-------|---------|------|
| 1 | initiating-coverage | 模板 8-12 页 | skeleton (inv thesis / KPIs / valuation / risks) |
| 2 | comps-analysis | Snowflake 头部 growth-tier peers | Datadog/MongoDB/Confluent/Couchbase peer table |
| 3 | dcf-model | DCF 估值 | WACC range 8-11%, terminal growth 3%, 64% upside |
| 4 | earnings-analysis | Q3 实际数据 | NRR 158%, consumption 130%, FCF margin 25% |
| 5 | datapack-builder | 每个数字溯源 | 完整 datapack + 财务模型 |
| 6 | 3-statement-model | 5 年预测 | 模型 + balance sheet flows |
| 7 | data-viz | chart 选择 | waterfall/EPS bridge/multiples chart |
| 8 | review-contract | 检查 material 协议（如 MSFT 数据中心） | 法律 tail risk note |

### 关键决策

- **Step 3 DCF sensitivity**: WACC × growth 两轴, 让 reader 看见什么动什么变
- **Step 4 NRR data**: 不能编, 必须从 datapack 拉真实数字
- **Step 8 legal gate**: SNOW 跟 MSFT / AWS 的 supplier agreement 重要, 不能漏
- **Risk Section**: 用 comps-analysis 的 peer multiples 作为 anchor + DCF range

### Quality Gate Enforcement

- [x] 每个数字可追到 datapack (Step 5)
- [x] DCF sensitivity 7-12% WACC × 2-3% growth
- [x] 5+ peers (Step 2)
- [x] Earnings bridge 跟 Q3 actual 衔接 (Step 4)
- [x] 3-statement model balance (Step 6)
- [x] 无 invented metrics

### 耗时

- Manual: 2-3 weeks analyst, 1-2 weeks associate = 4-5 周
- Orchestrator: 60-90 分钟
- **Compression**: ~30x

---

## 案例 B2: M&A — "Kohlberg & Co wants to buy a SaaS company, $200M ARR"

**用户输入**: "We're evaluating an LBO of a B2B SaaS company, ~$200M ARR. Run the deal."

### Orchestrator 决策表

**role signal**: PE banker → Path B2
**deliverable**: full M&A memo + LBO model + IC deck
**single vs multi**: pipeline-worthy (mandatory legal gates)
**entry**: deal-sourcing → comps-analysis

### 编排执行

| Step | Skill | 触发原因 | 输出 |
|------|-------|---------|------|
| 1 | deal-sourcing | (skip — target identified) | — |
| 2 | comps-analysis | 找 SaaS comps + precedents | 8 peers, 3 precedents |
| 3 | dcf-model | Target DCF | Standalone EV $2.5B |
| 4 | lbo-model | S&U, 6.0x TLA/TLB, 60% LTV | IRR 22%, MOIC 2.8x |
| 5 | pitch-deck | IC deck 15 slides | Full IC memo |
| 6 | review-contract | LOI / merger agreement | Risk flags (representations, MAC clause) |
| 7 | triage-nda | Bidder NDA | GREEN (standard) |
| 8 | legal-risk-assessment | HSR / antitrust early read | Low risk (sub-threshold) |

### ⚠️ Mandatory Legal Gates Enforcement

```
B2 may NOT skip review-contract, triage-nda, OR legal-risk-assessment
before any external pitch.

✓ review-contract (Step 6)
✓ triage-nda (Step 7)
✓ legal-risk-assessment (Step 8)
```

### 关键决策

- **Step 4 LBO structure**: $200M ARR × 12-14x EBITDA × 6.0x leverage
- **Step 6 contract risk**: 重点 flag 12 项 rep & warranties 跟 1 个 MAC carve-out
- **Step 8 antitrust**: SaaS 行业 < $5B 通常 HSR sub-threshold, 但需看 concentration
- **IC pitch**: Step 5 包含 financial highlights + risk register + recommendation (BID / HOLD)

### 反例: 不该走的死胡同

| 错误路径 | 为什么错 |
|---------|---------|
| 跳过 Step 6 review-contract | 任何 PE 交易合规要求 legal review |
| Step 4 LBO 用高 leverage 但缺 debt 文档 | 失实的模型 vs 实操 |
| 跳过 Step 8 antitrust | $200M SaaS 可能有 4(c)/4(d) HSR trigger |

### 耗时

- Manual: 4-8 weeks (deal team + analyst + legal + compliance + banker)
- Orchestrator: 90-120 分钟 (含 3 个 legal gate)
- **Compression**: ~25-35x

---

## 案例 B3: Pitch — "Series A Deck for Vertical AI Startup"

**用户输入**: "We're raising Series A — $8M. Build investor deck."

### Orchestrator 决策表

**role signal**: founder → Path B3
**deliverable**: 10-15 slide Series A deck
**single vs multi**: pipeline
**entry**: office-hours

### 编排执行

| Step | Skill | 触发原因 | 输出 |
|------|-------|---------|------|
| 1 | office-hours | YC-style 6 forcing questions | Founder brief (clinic ops inefficiency) |
| 2 | plan-ceo-review | CEO-mode plan review | 10-star problem framing |
| 3 | comps-analysis (light) | TAM: $40B → SAM: $8B → SOM: $500M | Top-down market |
| 4 | data-viz | Chart selection | Funnel, bar, KPI tracking |
| 5 | pitch-deck | 12 slides | Deck |
| 6 | pitch-deck-critic | VC-grade feedback | "Slide 7 missing wedge", "LTV/CAC off" |
| 7 | (skip — no separate asset) | — | — |
| 8 | okr-alignment-checker | OKR sanity | "Q2 ARR target $1M mismatched with pitch $5M target" |

### 关键决策

- **Step 2 CEO review**: 创始人常见陷阱 — 把 solution 当 problem. 必须 10-star
- **Step 3 light**: only market sizing comps (not full peer set)
- **Step 6 VC critic**: 类似 Garry Tan / a16z 标准, 5 维评分
- **Step 8 OKR alignment**: 一致性 sanity, 防 narrative 漂移

### Cross-Cluster Bridge

如果 deck 含 hero image / animation:
- defer to `design-orchestrator` for visual discipline
- 避免 manufactured AI slop

### 反例

| 错误路径 | 为什么错 |
|---------|---------|
| 跳过 office-hours (Step 1) | 缺少 6 forcing questions, pitch 容易空 |
| 用 pitch-deck-critic 之前未做 office-hours | VC 反馈变成 cosmetic |
| 用 plan-ceo-review 之前未做 plan-eng-review | CEO 视角缺工程 anchor |
| OKR alignment check 之前未做 deck | 检查 dependency 反转 |

### 耗时

- Manual: 1-2 weeks (founder + designer + advisor)
- Orchestrator: 45-60 分钟
- **Compression**: ~20-25x

---

## 案例 B4: SMB — "Friday Afternoon Ops Close"

**用户输入**: "It's Friday. Run my weekly ops — close the books, chase invoices, review feedback, update SOP."

### Orchestrator 决策表

**role signal**: SMB owner/operator → Path B4
**deliverable**: end-of-week ops loop
**single vs multi**: full loop
**entry**: cash-flow-snapshot

### 编排执行

| Step | Skill | 触发原因 | 输出 |
|------|-------|---------|------|
| 1 | cash-flow-snapshot | 周 5 起点 | AR $42K / AP $18K |
| 2 | invoice-chase | 3 张 overdue | 3 封 draft 邮件 |
| 3 | (skip — Friday afternoon, no new lead) | — | — |
| 4 | customer-pulse | 周 5 review | 5 痛点 + 2 风险 |
| 5 | sop-writer | 客户反馈触发新流程 | New return SOP draft |
| 6 | (skip — onboarding 是周一) | — | — |
| 7 | customer-escalation | 1 个 payment issue | Handoff 给 ops |
| 8 | draft-response | 1 个 product bug 反馈 | Reply 已写好 |

### Compliance Activation (Conditional)

```
if SMB is healthcare/fintech:
    insert compliance-check before Step 7
✓ Not needed here (clothing retailer)
```

### 关键决策

- **Skip 3, 6**: SMB 周 5 下午主要做 close / chase / review, 不是 outreach / onboarding
- **Step 5 SOP 联动 Step 4 pulse**: 客户反馈→文档化, 闭环
- **Step 7+8**: 1 escalation package + 1 reply, 周一进

### 耗时

- Manual: 30-60 分钟分散操作
- Orchestrator: 20-25 分钟
- **Compression**: ~2x (lower because loop 是 operational, 不是 deep generation)

---

## 4 案例的 meta-pattern

1. **总是从 role signal 出发** — 分析师 / 银行家 / 创始人 / SMB 是不同的决策路径
2. **B2 (M&A) 是唯一 mandatory legal gates** — 其他 3 路径法律 review 是 conditional
3. **B1/B2 永远 trace numbers to datapack** — 数字不能凭空
4. **Insert 是常态** — compliance-check / audit-support 经常作为 conditional step
5. **每个路径都有"skip 多数 steps"的 lite 模式** — 不是必须跑全部 8 步
6. **Cross-cluster bridge** — B3 经常 defer to design-orchestrator / content-orchestrator
