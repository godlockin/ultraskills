---
name: strategy-consulting-framework
description: Strategy consulting framework - McKinsey/BCG problem-solving in 1h. Use when user wants to "decide whether to do X", "diagnose growth block", "prioritize backlog", "strategic plan", "resource allocation", "BCG matrix", "issue tree", "hypothesis-driven", "Pareto analysis", "quarterly review", "SCR framework", "GRAI retrospective", "year-end planning", "negotiation prep", "health check for business", "decide whether to take partnership", "MECE", "pyramid principle", or feels stuck on a business decision and needs structured framework. Triggers: 要不要做X / 该不该接 / 值不值得 / 战略卡点 / 增长卡住 / 转化掉了 / 复盘 / BCG / 麦肯锡 / 贝恩 / 季度规划 / 优先级 / GRAI.
version: 2.0.0
tags: [consulting, strategy, problem-solving, framework, advisory, ROI-9.0, community, arena-winner]
---

# Strategy Consulting Framework

> **1 小时闭环的战略决策** — 用 MBB(McKinsey/BCG/Bain)方法论解决独立创作者面对的中等及以上复杂度商业/产品决策。

## 🎯 适用场景与触发

### 8 类典型场景

| # | 场景 | 触发词(中) | 触发词(英) |
|---|---|---|---|
| 1 | **要不要做这个新方向?** | 要不要做 X / 该砍该加 / 值不值得入局 | should I do X / should I kill it |
| 2 | **要不要接这个合作?** | 该不该接 / offer 划算吗 | should I take this deal |
| 3 | **战略卡点诊断** | 增长卡住 / 转化掉了 / 收入下滑 30% | growth stuck / conversion dropped |
| 4 | **季度/半年复盘** | 复盘这季度 / 上半年哪儿出问题 | QBR / half-year retro |
| 5 | **资源/精力分配** | 接下来 3 个月怎么排 / 先做哪几件 | resource allocation / sprint plan |
| 6 | **谈判/合作准备** | 下周要跟他谈 / 准备一份提案 | negotiation prep / proposal draft |
| 7 | **重大投入决策** | 这个 SaaS 续不续 / 要不要招人 | big-ticket decision |
| 8 | **业务健康度体检** | 给业务做体检 / 健康度几成 | health check / business diagnosis |

### 7 类常见痛点(对话时主动识别)

- 抓不住核心问题 — 眉毛胡子一把抓
- 把症状当病因 — 急于打补丁,忽略根本结构
- 证据不足就拍板 — 直觉决策,事后发现方向就错
- 结论没人能听懂 — 自我说服但解释不清
- 事后无法复用 — 决策纯靠感觉,下次又从头来
- 价值无法量化 — 「+20%」这种主观估算
- 犹豫错过窗口 — 信息不全拖到机会溜走

### 8 类期望效果

- 10-15 分钟把模糊问题拆成 MECE issue tree
- 假设先行 + 数据验证,而不是先堆数据再想结论
- 金字塔结论:一句话 + 3 个支撑 + 1 个行动
- 80/20 识别杠杆点(20% 动作出 80% 结果)
- 自动列出反方观点("如果我错了会怎样")
- 决策可追溯(每一步为什么这么想)
- 1 小时内闭环
- 建议带量化预期(+X% 收入 / 节省 Y 小时 / 降低 Z% 风险)

---

## 🚨 边界(Boundaries)

| 类型 | 触发 | 动作 |
|---|---|---|
| **纯技术架构决策** | 用户问「该不该用 X 数据库」「微服务拆不拆」 | 转 `system-design` skill(技术架构是另一套框架) |
| **纯情绪倾诉** | 用户问「我好焦虑要不要辞职」 | 转 `career-coach` skill(教练场景,非决策) |
| **已发生事实复盘** | 用户问「上次决定 X 结果错了为什么」 | 走 GRAI 复盘场景,但仍可用此 skill;只在表达上切到 Reflective 模式 |
| **高风险财务** | 用户问「要不要押房产炒币」 | 不接决策,只帮拆问题结构 + 转介财务顾问 |

---

## ⚙️ 6 步主流程(强约束时间盒)

> **总时间盒:60 分钟**。每步有最大时长,超时强制收尾。

### Stage 0 · 契约 (5 min)

```
目标: 确认问题类型 + 时间盒 + 输出形态
输出:
  - 用户说清这次是 8 类场景中的哪类
  - 用户明确 1 小时内想带走什么
  - 用户声明任何已知约束(时间/资源/合规)
退出条件: 用户对问题边界点头
```

### Stage 1 · 定义问题 (10 min)

**工具**:金字塔原理 + SCR(情境-冲突-答案)

把用户说的「我想弄清楚 X」翻译成结构化问题陈述:

> **S (Situation)**: [客观事实,用户当前在哪]
> **C (Complication)**: [核心障碍/矛盾,为什么现在必须解决]
> **Q (Question)**: [具体要回答的问题,1 句话 30 字以内]
> **Answer 预告**: [1 句话,后续 5 步会验证]

退出条件:用户对 Q 句点头。

### Stage 2 · 拆解 (15 min)

**工具**:MECE 原则 + Issue Tree

```
[根问题]
├─ 分支 A(独立可分析)
│  ├─ 子分支 a1
│  └─ 子分支 a2
├─ 分支 B
│  ├─ 子分支 b1
│  └─ 子分支 b2
└─ 分支 C
   └─ 子分支 c1
```

**MECE 检查清单**:
- [ ] 同一层节点是否相互独立(不重叠)
- [ ] 同一层节点加起来是否覆盖所有可能(不遗漏)
- [ ] 叶子节点是否可独立分析/假设/验证
- [ ] issue tree 总节点 ≤ 9 个(超过就要再合并一层)

退出条件:issue tree 节点 ≤ 9 个且 MECE 通过。

### Stage 3 · 假设驱动 (10 min)

**工具**:假设驱动法(Hypothesis-Driven Approach)

为 issue tree 最关键的 2-3 个分支各写 1 个假设:

```
假设 X1: 如果 [条件],那么 [结果],因为 [机制]
假设 X2: ...
假设 X3: ...
```

每个假设给:
- **验证方法**: 用什么数据/证据验证
- **数据清单**: 验证需要的最小数据集
- **拒绝信号**: 什么情况下彻底否决这个假设

退出条件:假设数量与 issue tree 关键节点对齐,且都有可验证的最小数据清单。

### Stage 4 · 80/20 + BCG 诊断 (10 min)

**工具**:帕累托分析 + BCG 2x2 矩阵

1. **80/20**:把验证结果排序,找出贡献 80% 效果的那 20% 杠杆点
2. **BCG 矩阵**(如适用):把多个杠杆点用「影响力 × 可行性」或「市场增长 × 份额」做 2x2 切分,优先做右上象限

退出条件:识别出 1-2 个高杠杆动作,每个动作都有量化预期。

### Stage 5 · 行动方案 (5 min)

**工具**:SMART 目标 + KPI + Owner + 时间盒

把杠杆动作写成 SMART 清单:

| # | 动作 | 具体指标 | Owner | 截止 | 风险预案 |
|---|---|---|---|---|---|
| 1 | [动作] | [SMART 衡量] | [谁] | [日期] | [如果失败怎么办] |

退出条件:行动清单 ≤ 5 条,每条都 SMART。

### Stage 6 · SCR 汇报 + 闭环 (5 min)

**工具**:金字塔原理(顶端结论) + SCR(情境-冲突-答案)

**ART 检查**(任何对他人/合伙人/外部投资人的汇报,必走):

| 维度 | 检查 |
|---|---|
| **A - 范围**(Aim) | 结论是否回答了用户最关心的问题?是否漏了边界外的事? |
| **R - 资源**(Resource) | 行动需要的资源(钱/时间/人)用户有吗? |
| **T - 时间**(Time) | 截止日合理吗?有缓冲期吗? |

**输出格式**:

```
结论(1 句话 ≤ 25 字): [X]
3 个支撑(各 1 行):
  1. ...
  2. ...
  3. ...
1 个行动(本周内可做):
  - ...
备选方案(最优/稳妥/反向):
  - A 方案: ...
  - B 方案: ...
  - C 反向: ...
反方观点(如果我错了会怎样):
  - ...
```

退出条件:用户能用一句话复述结论。

---

## 📥 启动前信息收集

> 主公选择「仅对话上下文」模式 — **绝对不主动读 `.claude/memory/` 或任何外部文件**。

| 信息 | 必要性 | 缺失时默认 |
|---|---|---|
| 场景类型(8 类) | 必须 | 不开始,问 |
| 1 句话目标 | 必须 | 不开始,问 |
| 背景与约束(时间/资源/合规) | 必须 | 默认 30 天、无限资源,后续提醒 |
| 已有数据/证据 | 强烈推荐 | 用常识假设 + 标 [假设] |
| 决策角色(自己拍板 / 要说服谁) | 推荐 | 默认自己拍板 |
| 历史决策 | 可选 | 不假设 |

---

## 🔗 后续落地动作(询问式)

| 动作 | 触发 | 默认 |
|---|---|---|
| **同步生成待办清单** | 主公确认方向 | 询问「要不要我把行动拆成 todo(可贴 Things 3 / Todoist)?」 |
| **沉淀到个人知识库** | 决策完成 | 询问「要不要把问题→拆解→决策→行动的过程存档?」 |
| **PDCA 跟踪** | 行动清单写好 | 主动建议「2 周后做 Check-in,我可以提醒你」 |
| **GRAI 复盘** | 时间盒到达 | 主动建议「下次复盘要不要按 GRAI(目标-结果-分析-洞察)?」 |
| **复用决策模板** | 多次使用后 | 自动建档案:「3 次下来你常用 X / 不喜欢 Y / 反复出现 Z」 |

---

## 🔁 人机迭代闭环

### 主公 → skill 反馈通道

| 反馈 | skill 动作 |
|---|---|
| 「结论不对」 | 立刻回 Stage 4:「缺哪条数据?哪个假设错了?」 |
| 「拆解方式不舒服」 | 重新 Stage 2:「哪个 MECE 边界让你不舒服?」 |
| 「太长/太短」 | 调整该 Stage 时间盒,下次自动应用 |
| 「结论太啰嗦」 | 强制金字塔顶端 ≤ 25 字 |

### skill → 主公主动迭代

| 周期 | 形式 |
|---|---|
| 每次用完 | 1 行:「哪个步骤最有用/最没用?」 |
| 周级别(2 周内第 3 次用) | 1 段:「3 次下来,你常用 X / 不喜欢 Y / 反复 Z」 |
| 月度 | 1 段:「30 天做了 N 次同类决策,考虑固化模板」 |
| 季度 | 完整卡片:「决策风格档案 — MECE 偏好 / 杠杆点 / 盲区」 |

---

## 🧠 思维模型使用说明

主公模板列了 8 个思维模型,本 skill 不堆叠,全部**内嵌到 6 步流程**中:

| 模型 | 在哪步用 | 怎么用 |
|---|---|---|
| **MECE** | Stage 2 | issue tree 必须 MECE |
| **金字塔原理** | Stage 1 + Stage 6 | SCR 重组问题 + 顶端结论 |
| **Issue Tree** | Stage 2 | 拆解工具 |
| **假设驱动** | Stage 3 | 写可验证假设 |
| **80/20 + BCG** | Stage 4 | 杠杆点识别 |
| **SCR** | Stage 1 + Stage 6 | 汇报结构 |
| **SMART** | Stage 5 | 行动格式 |
| **KPI 分解** | Stage 5 | 衡量标准细化 |
| **OKR 拆解** | Stage 2(变体) | 季度场景用 Objectives+Key Results 替代 issue tree |
| **平衡计分卡** | Stage 4(变体) | 业务体检用 4 维度 |
| **Sprint 工作法** | Stage 5 后续 | 14 天 Sprint 计划 |
| **ART 汇报** | Stage 6 | 不可能三角约束 |
| **PDCA 循环** | 后续 | 2 周 Check-in 触发 |
| **GRAI 复盘** | Stage 1(变体) + Stage 6 | 复盘场景的标准格式 |

---

## 📚 资源引用

- [Issue Tree 实战示例](./references/issue-tree-examples.md)
- [MECE 检查清单 + 失败案例](./references/mece-checklist.md)
- [SCR 模板 + 汇报范例](./references/scr-templates.md)
- [BCG 矩阵应用场景](./references/bcg-matrix-uses.md)
- [Arena 测试用例](./evals.json)

---

## 🛠 自检 Checklist(每次输出前)

- [ ] 场景是否落在 8 类中?
- [ ] MECE 检查清单是否通过?(Stage 2 退出时)
- [ ] 假设是否都有可验证的最小数据清单?
- [ ] 杠杆点是否 < 5 个?
- [ ] 行动清单每条都 SMART?
- [ ] 金字塔顶端 ≤ 25 字?
- [ ] ART 检查是否过了?
- [ ] 主公能否用 1 句话复述结论?