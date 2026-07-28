# Sprint 工作法 · 完整说明

## 一句话核心

> **2 周冲刺 + 站会 + 燃尽图 + 评审回顾** — 短周期、强反馈、可见进度。

---

## Sprint 4 大仪式

| 仪式 | 时点 | 时长 | 目标 |
|---|---|---|---|
| **Sprint Planning** | Sprint 开始 | 2-4h | 选 Sprint Backlog + 定 Sprint Goal |
| **Daily Standup** | 每天 | 15min | 同步进度 + 暴露风险 |
| **Sprint Review** | Sprint 结束 | 1-2h | 演示成果 + 收反馈 |
| **Sprint Retrospective** | Sprint 结束 | 1-1.5h | 复盘过程改进 |

---

## Sprint 完整流程(2 周示例)

```
Day 0  (Sprint Planning)
  ├─ 产品负责人(PO) 选 Backlog Top 项
  ├─ 团队评估容量(Velocity 历史)
  ├─ 定 Sprint Goal(一句话)
  └─ 拆任务到子任务

Day 1-9  (执行)
  ├─ Daily Standup(每天 9:30 / 15min)
  ├─ 燃尽图每日更新
  ├─ 持续集成 + 持续测试
  └─ 中期检查(Sprint 中点)

Day 10  (Review + Retro)
  ├─ Sprint Review: 演示 + 反馈
  └─ Sprint Retrospective: 复盘
```

---

## Sprint Planning 范式

### 5 步

1. **回顾上 Sprint** — Velocity 多少 / 完成率 / 改进点
2. **看 Product Backlog** — PO 讲 Top 优先级
3. **团队评估** — 每个 item 估点(故事点)
4. **容量匹配** — 总点 ≤ 历史 Velocity × 1.1
5. **定 Sprint Goal** — 一句话目标(非任务清单)

**Sprint Goal 示例**:
- ❌ "完成 8 个故事点"(太具体,失焦点)
- ✅ "让用户能完成首次下单"(有意义,可演示)

---

## Daily Standup 范式

### 3 问(每位)

1. 昨天我完成了什么?
2. 今天我要做什么?
3. 有什么阻碍我?

### 严格规则

- **站立会议**(不是坐着开)
- **15 分钟**(超时立即停)
- **不解决问题**(问题会后单独约)
- **不针对个人**(暴露阻碍,不指责)

### 反模式

- ❌ 站会变成状态汇报 → 改成阻碍暴露
- ❌ 站会超过 30 分钟 → 严格掐表
- ❌ 站会讨论技术方案 → 约专题会

---

## Sprint Review 范式

### 议程(1-2h)

```
1. Sprint Goal 回顾 (5min)
   - 完成?部分?未完成?
2. Demo (60-90min)
   - 每个完成项现场演示
   - 关键干系人(领导/客户)参与
3. 收反馈 (15min)
   - 现场记录反馈
4. Backlog 调整 (10min)
   - 基于反馈调整下 Sprint
```

### Demo 规则

- **演示"完成"的项**,不是"做了一半"的
- **真实环境演示**,不是 PPT
- **邀请关键干系人**,不只团队

---

## Sprint Retrospective 范式

### Start / Stop / Continue

- **Start**: 我们下 Sprint 要开始做什么?
- **Stop**: 我们要停止什么?
- **Continue**: 什么要继续?

### 4 Lenses

- **Liked**: 哪些做得好,继续?
- **Learned**: 学到什么?
- **Lacked**: 缺什么?
- **Longed for**: 希望有什么?

### Mad / Sad / Glad

- **Mad**: 什么事让你生气?
- **Sad**: 什么事让你失望?
- **Glad**: 什么事让你高兴?

**选一种范式**,不要每次都换。

---

## 燃尽图(Burndown Chart)

```
Y
^
|  ●
|    ●
|       ●
|          ●
|              ●  ← 实际线
|                 ●
|                     ●
|                        ●
|___________________________●___ 理想线
|                              ●
|_________________________________ X 时间
```

### 解读

- **实际线在理想线上方**(速度慢) — 早期警示
- **实际线在理想线下方**(速度快) — 可加任务或提前结束
- **断崖式下降**(突然完成大量) — 可能故事估点不准
- **持平不动**(零进展) — 立即找根因

---

## Velocity 速度管理

### Velocity 历史表

| Sprint | 估点 | 实际完成 | 完成率 |
|---|---|---|---|
| Sprint 1 | 30 | 28 | 93% |
| Sprint 2 | 35 | 25 | 71% |
| Sprint 3 | 30 | 30 | 100% |
| **平均 Velocity** | — | **27.6** | **88%** |

### 容量规划

```
下 Sprint 容量 = Velocity × 1.0-1.1(留 buffer)
                = 27.6 × 1.05 ≈ 29 故事点
```

### 异常处理

- **Velocity 突降 30%+** — 找根因(团队变动?故事估点不准?外部阻塞?)
- **Velocity 突升 30%+** — 检查是否故事拆太粗(实际没做完)
- **Velocity 持续 3 Sprint 低** — 重新评估团队容量

---

## Sprint 与 OKR 配合

```
季度 OKR
  ├── Sprint 1(达成 OKR 的 25%)
  ├── Sprint 2(达成 OKR 的 50%)
  ├── Sprint 3(达成 OKR 的 75%)
  ├── Sprint 4(达成 OKR 的 100%)
  └── Sprint 5-6(增量/优化)
```

每个 Sprint Backlog 必须**明确服务哪个 OKR/KR**,不相关的任务不进 Sprint。

---

## 输出范式

```markdown
## Sprint #[N] · [起止日期]

### Sprint Goal
[一句话,非任务清单]

### Backlog
| # | User Story | 估点 | Owner | 关联 OKR |
|---|---|---|---|---|
| 1 | 作为用户,我能 X | 5 | 张三 | Q3 OKR1 |
| 2 | ... | | | |

### 容量评估
- 团队: [N] 人
- Velocity 历史: [X] 点
- 本 Sprint 容量: [X×1.0] 点

### 风险
1. [风险 1] + 预案
2. [风险 2] + 预案

### 站会议程
每天 9:30,3 问,15min,超时停

### Review 安排
[日期 + 邀请谁]
```