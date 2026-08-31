---
name: learn-from-loss
description: Postmortem methodology for competition results — multi-expert panel review, 8-dimension scoring, winner-vs-loser gap analysis, lessons codification, iron-rules bank. Use when user wants to "postmortem a competition", "review why we lost", "recover lessons from failure", "team retrospective after losing", "WDC postmortem", "WDC debrief", "我做得不错但没赢", "输在哪了", "赛后复盘", "给团队复盘", "比赛结果复盘", "disagree with judging", "validate deliverable vs competitors", or mentions winning/losing/competition/赛后复盘/复盘/输赢复盘. Distinguishes from career-coach (emotional support) — this is structured methodology.
version: 2.0.0
tags: [postmortem, review, analysis, competition, retrospective, scoring, community, arena-winner]
---

# Postmortem Review — Learn More from Losing Than Winning

## 🎯 适用场景与触发

### 6 类典型场景

| # | 场景 | 触发词(中) | 触发词(英) |
|---|---|---|---|
| 1 | **比赛结果复盘** | 比赛输了 / 赛后复盘 / 输在哪了 / 作品没获奖 | postmortem a competition / why we lost / WDC postmortem |
| 2 | **个人/团队总结** | 复盘这季度 / 团队做项目结果差 / 项目没达到预期 | retrospective / team debrief |
| 3 | **多份方案对比** | 跟同行的差距在哪 / 我做得不错但没赢 | gap analysis / benchmark vs competitors |
| 4 | **失败教训沉淀** | 输过的教训 / 历史踩坑 / 哪些不能再犯 | lessons codification / failure lessons bank |
| 5 | **领导/客户交付复盘** | 给客户提案失败 / 项目交付不达标 | client deliverable review / post-mortem |
| 6 | **方法论迭代** | 我们以前的方法过时了 / 重新构建框架 | methodology refresh / process iteration |

### 6 类常见痛点

- 输给谁 / 差在哪 / 哪里可以更好 — **没有结构化拆解,只有模糊感觉**
- 评委判断和我不一样 — **觉得是运气差/有黑幕,不肯直视自己**
- 复盘完写不出可执行规则 — **流于感性感叹**
- 下次还会犯同样的错 — **没有 Day-0 checklist**
- 团队每个人复盘结论不一样 — **没有统一打分维度**
- 跨团队/跨项目经验无法复用 — **没有 Iron Rules 沉淀机制**

### 8 类期望效果

- 多维度打分矩阵(自己 + 至少 3 个赢家/标杆)
- Gap 表(每维度:自己 vs 标杆 vs 差值 vs 根因 vs 修复)
- 3-agent 独立 panel(内容/设计/工艺 3 视角)
- 5-7 条 Iron Rules(绝对不能犯)
- Pass Criteria 二元门(每条带验证方法)
- Bonus Items(从"合格"到"难忘"的细节)
- Day-0 Checklist(下次开始 1 小时内要做的)
- Iron Rules Bank 长期沉淀(团队共用,跨项目复用)

## Overview

A structured postmortem turns a loss into a reusable playbook. This skill provides the methodology used after WDC 2026 APAC: analyze every winner across 8 dimensions, run a 3-agent independent expert panel, codify lessons into iron rules and pass criteria, and build a Day-0 checklist for next time.

## When to Use

- After a competition result (win or loss — both have lessons)
- When preparing a retrospective for a high-stakes presentation
- When comparing your deliverable against competitors
- When codifying team knowledge into reusable playbooks

## Phase 1: Winner Analysis (Day 0–1)

### Collect All Winners

Don't just look at 1st place. Analyze the top 3–5 and any team that scored differently from you.

```markdown
| Rank | Team | Carrier | Hook | Score | What They Did Differently |
|------|------|---------|------|-------|--------------------------|
| 1 | Data Five | HTML | "五行缺数据" | 92 | Cultural team name, hover interactions |
| 2 | Vikings | Video | "came for data, stayed for insights" | 89 | Multi-voice, quotable closing |
| 3 | Insights Fund | QR → App | Scan to use | 87 | Zero-friction adoption |
| ... | Us | PPT | "EKET Plan A" | 72 | Strong content, poor delivery |
```

### 8-Dimension Scoring Matrix

Score yourself AND each winner on the same 8 dimensions (1–10 scale):

| # | Dimension | What It Measures |
|---|-----------|-----------------|
| 1 | Carrier convenience | How easy is it for the judge to open/engage? |
| 2 | Memorability | Can the judge recite a line 24h later? |
| 3 | Actionability | Does the judge know what to do next? |
| 4 | Market coverage | Are all markets represented equally? |
| 5 | Methodology rigor | Is the analysis defensible and replicable? |
| 6 | Visual consistency | Does every slide look like the same team made it? |
| 7 | Sensory quality | Audio, spelling, paths — zero debt? |
| 8 | Story arc | Does the deck have a beginning, middle, end? |

### Gap Identification

For each dimension where you scored below the winner:

```markdown
| Dimension | Us | Winner | Gap | Root Cause | Fix |
|-----------|----|--------|-----|-----------|-----|
| 1 Carrier | 4 | 9 | -5 | Chose PPT without questioning | Day-0 carrier workshop |
| 2 Memorability | 3 | 9 | -6 | Generic team name, no hook | Cultural pun + origin story |
| 4 Coverage | 5 | 8 | -3 | 80% China content | 5-country skeleton locked early |
```

## Phase 2: Independent Expert Panel Review (Day 1–2)

### Panel Composition

Run 3 parallel reviewers, each with a distinct lens:

| Agent | Focus | Checks |
|-------|-------|--------|
| Content Accuracy | Data vs claims | YAML ↔ HTML consistency, footnote accuracy, citation verification |
| Design System | Visual quality | CSS token usage, WCAG contrast, hardcoded colors, responsive scaling |
| Audio & Pipeline | Production quality | Voice script accuracy, silence ratios, toolchain completeness, file integrity |

### Review Protocol

Each agent receives:
1. The full deck directory
2. The content source of truth (`content.yaml`)
3. The design token file (`tokens.css`)
4. The audio files and build script
5. A checklist of known failure patterns

Each agent outputs:

```markdown
## Review: [Agent Name]
**Verdict:** PASS / CONDITIONAL PASS / FAIL

### Issues Found
| # | Severity | File | Line | Description | Suggested Fix |
|---|----------|------|------|-------------|---------------|
| 1 | P0 | 06_korea.html | 285 | Footnote cites proxy source | Replace with neutral text |
| 2 | P1 | 03_india.html | 273 | Chart path is absolute | Change to ../assets/ |
| 3 | P2 | tokens.css | 45 | Missing badge tokens | Add --badge-signed etc. |

### Summary
[2–3 sentences on overall quality]
```

### Severity Scale

| Level | Definition | Action |
|-------|-----------|--------|
| P0 | Blocks submission. Judges will notice. | Fix immediately |
| P1 | Degrades quality. Attentive judges notice. | Fix before submission |
| P2 | Minor inconsistency. Won't affect score. | Fix if time permits |

## Phase 3: Fix and Re-Review (Day 2–3)

### Fix Priority Order

1. All P0 issues (blocking)
2. All P1 issues (quality)
3. P2 issues if time permits
4. Run lint scripts to verify

### Re-Review Protocol

After fixes, run the same 3 agents again but only check:
- Previously flagged items (did the fix work?)
- Adjacent files (did the fix introduce new issues?)
- Full lint pass (text + audio)

## Phase 4: Codification (Day 3–4)

### Extract Iron Rules

From the gap analysis and review, extract 5–7 non-negotiable rules. Format:

```markdown
### Rule Name

<what the rule says — one sentence>

| Good | Bad | Why |
|------|-----|-----|
| Example from winner | Example from loser | Mechanism |
```

### Define Pass Criteria

For each iron rule, define a binary pass/fail gate:

```markdown
| # | Gate | Standard | Verification Method |
|---|------|----------|-------------------|
| G1 | Carrier works | Opens on clean machine | Test on VM |
| G2 | 5-country balance | Each country ≥ 1 page | Slide count |
```

### Define Bonus Items

What the winners did that pushed them from "solid" to "unforgettable":

```markdown
| # | Bonus | Effect | Who Did It |
|---|-------|--------|-----------|
| B1 | Cultural pun name | Dual-culture resonance | Data Five |
| B2 | QR code link | Zero-friction adoption | Insights Fund |
```

### Build Day-0 Checklist

Every competition starts with this checklist:

```markdown
□ Judge persona workshop (who, what KPIs, what they carry out)
□ Team name + origin story + 1 metaphor (within 4 hours)
□ Default carrier ≠ PPT (disprove PPT first)
□ Pre-mortem: "if we lose, why?"
□ N-dimension symmetric skeleton (locked early)
□ External cold read (before last third of timeline)
□ Lint all pass (before submission)
```

## Anti-Patterns

### 无归责复盘与使用边界（必遵守）

本流程只用于改进**系统、流程、交付物与决策条件**，不得作为个人绩效、晋升、降级、纪律处分、排名或报复的依据。默认不点名归责；记录时分开写清事实、可观察行为、系统条件与决策，而非把结果归因给个人品格。

公司内部使用时：只对齐业务 KPI／流程结果，使用脱敏后的最小必要数据，并先取得参与者对复盘目的和可见范围的同意。用户若明确要求评价个人绩效、追责或惩罚，停止本流程，转为经授权的 HR／管理程序。

1. **"We lost because of X" (single cause)** — Losses are always multi-causal. Use the 8-dimension matrix to find ALL gaps.
2. **"The winners just got lucky"** — Luck doesn't produce consistent patterns across multiple winners. Study what they did deliberately.
3. **"Our content was strong, only the format was wrong"** — If the format prevents engagement, the content never existed for the judge.
4. **"Next time we'll just try harder"** — "Harder" is not a strategy. Iron rules and pass criteria are.
5. **Skipping the independent panel** — Self-review has blind spots. External reviewers catch what you can't.

## Deliverables Checklist

A complete postmortem produces:

- [ ] Winner analysis matrix (8 dimensions × all teams)
- [ ] Gap identification table (per dimension: us vs winner)
- [ ] 3-agent independent review (content + design + audio)
- [ ] Fix log (what was fixed, what was deferred)
- [ ] Iron rules document (5–7 non-negotiable rules)
- [ ] Pass criteria (binary gates, each with verification method)
- [ ] Bonus items (what winners did that we didn't)
- [ ] Day-0 checklist (for next competition)
- [ ] Next-level upgrade path (what to improve if given more time)

## Template: Postmortem Document Structure

```markdown
# [Project] Postmortem

## 1. Result Summary
- Score: X/100
- Rank: N of M
- Top gap: [dimension] (-Y vs winner)

## 2. Winner Analysis
[8-dimension matrix]

## 3. Gap Analysis
[Per-dimension: us vs winner, root cause, fix]

## 4. Expert Panel Review
### 4.1 Content Accuracy
[Agent findings]
### 4.2 Design System
[Agent findings]
### 4.3 Audio & Pipeline
[Agent findings]

## 5. Iron Rules (L1–L6)
[Non-negotiable rules with examples]

## 6. Pass Criteria (G1–G8)
[Binary gates with verification methods]

## 7. Bonus Items (B1–B8)
[Nice-to-haves that separate good from unforgettable]

## 8. Next-Level Upgrade Path
[From current state to end state, with investment estimates]

```

## 🚨 边界(Boundaries)

| 类型 | 触发 | 动作 |
|---|---|---|
| **纯情绪宣泄** | 用户没具体方案/比赛结果,只是想倾诉「我好气」 | 转 `career-coach`(情绪场景,非结构化复盘) |
| **想吵架/告评委** | 用户想辩解规则不公平、黑幕 | 不接反驳路线,只接「规则不变情况下我能改进什么」 |
| **照搬方法到新比赛** | 用户问「这套能不能直接复制到下个比赛」 | 提醒:Day-0 checklist 需要重新评估维度 |
| **公司内部复盘** | 用户问的是团队 OKR 复盘/季度总结 | 可用,但去掉「评委」维度,改成「业务 KPI」对齐,且只对齐流程/交付物结果,不用于个人绩效归因 |

---

## 📥 启动前信息收集

| 信息 | 必要性 | 缺失时默认 |
|---|---|---|
| **作品/结果本身**(URL/文档/演示截图) | 必须 | 不开始,问 |
| **比赛规则 + 评委人数/画像** | 强烈推荐 | 假设 5 个评委 + 综合评分,后续提醒 |
| **至少 3 个标杆/赢家样本** | 强烈推荐 | 假设公开可访问,后续提醒 |
| **提交前你的预期/预判** | 推荐 | 假设 70% 信心,后续提醒 |
| **时间窗**(复盘截止时间) | 可选 | 默认 1 周内完成 |

> **特别说明**: 主公选择「仅对话上下文」,**绝对不主动读** `.claude/memory/`。所有素材需用户在对话内粘贴或描述。

---

## 🔗 后续落地动作

| 动作 | 触发 | 默认 |
|---|---|---|
| **归档 Iron Rules** | Day-0 checklist 完成后 | 询问「要不要把 Iron Rules 加进团队 handbook?」 |
| **下次比赛复用** | 距下次比赛 ≤ 30 天 | 主动建议「下次开始时调用本 skill,从 Day-0 checklist 起手」 |
| **PDCA 跟踪** | Iron Rules 实施后 | 询问「要不要 2 周后 Check-in 验证 Rules 可行性?」 |
| **跨项目推广** | 多次使用后 | 主动建议「这套方法也适合 [X 类项目],要不要扩展?」 |

---

## 🔁 人机迭代闭环

### 主公 → skill 反馈通道

| 反馈 | skill 动作 |
|---|---|
| 「这个维度不对」 | 询问补充维度,扩展 8 维度矩阵到 10 维度 |
| 「Pass Criteria 太严/松」 | 询问具体例子,调整 standard |
| 「Day-0 checklist 走不完」 | 询问时间约束,精简到 3 条核心项 |
| 「没标杆可比」 | 改用行业标准/历史最佳替代 |

### skill → 主公主动迭代

| 周期 | 内容 |
|---|---|
| **每次用完** | 「哪个 Phase 最有用/最没用?」 |
| **3 次使用后** | 「3 次下来,你常用 X / 反复卡在 Y / 漏掉 Z」 |
| **半年/年度** | 「累积了 N 条 Iron Rules,建议回顾 top 5 是否仍适用」 |
| **跨领域复制** | 「本方法已在 A 类项目验证,建议扩到 B 类项目」 |

---

## 🧠 思维模型使用说明

| 模型 | 在哪步用 | 怎么用 |
|---|---|---|
| **MECE** | Phase 1 (Winner Analysis) | 8 维度必须相互独立 |
| **80/20 帕累托** | Phase 1 (Gap Identification) | 找贡献 80% 差距的 20% 维度 |
| **多视角 Panel** | Phase 2 | 3 个独立 agent 盲评防自利偏差 |
| **ABC 优先级** | Phase 3 (Fix Priority) | P0/P1/P2 三级,先治根因再修表象 |
| **Rule Codification** | Phase 4 | Iron Rules 必须二元可验证 |

---

## 📚 资源引用

- [Iron Rules 历史沉淀库](./references/iron-rules-bank.md)
- [8 维度评分模板(可复制)](./references/scoring-matrix-template.md)

---

## 🛠 自检 Checklist(每轮输出前)

- [ ] 场景是否落在 6 类中?
- [ ] 8 维度是否都给了分数?(不能只评 3 维度)
- [ ] 至少 3 个标杆对比?(避免单点比较)
- [ ] Gap 表每行都有「根因」?
- [ ] 3 个 Panel agent 独立运行?(避免串联偏差)
- [ ] Iron Rules 是二元可验证?(不是「尽量」)
- [ ] Day-0 checklist 1 小时内可走完?(不超 10 项)
- [ ] 文档是否归档 / 加入团队 handbook?
```
