---
name: goal-management
description: 目标管理 Skill — 工作场景下的目标拆解、资源协调、防甩锅、月度复盘闭环。Use when 领导布置工作 / 经营会后拆目标 / 跨团队对齐 / 周月会议准备 / 进度汇报 / 申请资源 / 防范背锅 / 月度复盘 / OKR 拆解 / KPI 分解 / Sprint 排期 / 50 万业绩怎么做 / 帮我做目标拆解方案 等。调用 SMART / OKR / KPI / 平衡积分卡 / Sprint / ART(目标-资源-时间不可能三角)/ PDCA / GRAI 复盘 8 个模型。前置需补齐 4 项情境信息(组织战略 / 领导风格 / 个人优劣 / 同事关系),后置产出 5 项沉淀(周报 / 项目追踪 / 复盘 / 作品集 / 知识库)。月度生成目标管理学习报告(长板/弱点/待提升/需注意)并双向迭代了解你。
version: 1.0.0
tags: [productivity, leadership, management, goal, okr, kpi, community]
---

# 目标管理 Skill

> 「领导没说清,我没拆明,事太多,资源不够,怕背锅,不会汇报 — 一个闭环解。」

## 📌 何时该用本 skill

| 触发场景 | 典型例句 |
|---|---|
| **领导布置工作** | "领导让我下周做到 50 万业绩,怎么做" / "老板让我接手 X" |
| **经营/工作会议后** | "刚开完季度会,目标拆解成方案" / "周会布置的目标怎么落地" |
| **跨人对齐目标** | "一对一和老板对不齐" / "和同事对目标拉不齐" / "部门间踢皮球" |
| **月/周/复盘会** | "月报怎么写" / "周会怎么开" / "项目复盘怎么搞" |
| **资源/时间申请** | "怎么和老板要人" / "怎么申请预算" / "事情太多做不完" |
| **防范被甩锅** | "这件事怕最后背锅" / "同事在甩责任给我" / "怎么留痕自保" |
| **OKR/KPI 拆解** | "帮我把年度 OKR 拆成 Q1" / "KPI 怎么分到团队" |
| **月度复盘** | "这个月我做得好不好" / "目标管理学习报告" |

**主公记住**: 不是只写「怎么做」— 而是从**目标理解 → 关键动作 → 资源时间 → 汇报对齐 → 防背锅 → 沉淀闭环** 6 步完整出方案。

---

## 🧠 核心信念 (Core Stance)

1. **领导没说的不等于不存在** — 反复追问 5 Why,目标才显形。
2. **不可能三角永远存在** — 目标(A)、资源(R)、时间(T),三者必舍一。**永远先和领导讲清楚这三角**。
3. **汇报 ≠ 表功** — 准时 + 风险前置 + 解决方案,比完美结果更让领导安心。
4. **背锅 90% 是因为没留痕** — 关键决策书面化、抄送关键人、日期戳记。
5. **沉淀 > 完成** — 单一项目结束不算数,经验进入知识库才算闭环。

---

## 🧩 8 个思维模型(速查)

> 完整说明 + 模板 → `references/models/`。**不要在主体展开。**

| # | 模型 | 何时用 | 一句话核心 |
|---|---|---|---|
| 1 | **SMART** | 定目标时 | Specific / Measurable / Achievable / Relevant / Time-bound — 模糊目标 → 死亡 |
| 2 | **OKR 拆解** | 大目标到执行 | O 定方向,KR 量化结果;每层 OKR 上下一致 |
| 3 | **KPI 分解** | 已有指标往下传 | 顶层 KPI → 部门 KPI → 个人 KPI,各背 30%-40% |
| 4 | **平衡积分卡 BSC** | 多维度平衡 | 财务 / 客户 / 流程 / 学习成长 — 不偏科 |
| 5 | **Sprint 工作法** | 短周期执行 | 2 周冲刺 + 站会 + 燃尽图 + 评审回顾 |
| 6 | **ART 不可能三角** | 和领导谈资源 | A 目标 / R 资源 / T 时间 — 三选二,必舍一 |
| 7 | **PDCA** | 持续迭代 | Plan → Do → Check → Act — 4 步闭环,每步必出物 |
| 8 | **GRAI 复盘** | 周期回顾 | Goal / Result / Analysis / Insight — 不追责,只挖规律 |

**调用决策树**:

```
[刚接到目标] ─── SMART + OKR
                │
                ├─→ [要拆团队] ── KPI + BSC
                │
                ├─→ [要做短周期] ─ Sprint
                │
                ├─→ [和领导谈资源] ─ ART 不可能三角
                │
                ├─→ [持续执行] ── PDCA
                │
                └─→ [周期复盘] ── GRAI
```

---

## 🚀 5 步工作流 (Workflow)

> 严格按 5 步走,**任何一步没做完都不进下一步**。
> 每步必出物(括号内),缺一不可。

### Step 1 · 目标理解 (Understand)

**目标**: 把领导/会议说的人话,翻译成可量化目标。

**必出物**:
- 一句话目标陈述(主语 + 动作 + 量化 + 时间)
- 隐藏目标识别(领导没说但其实想要的)
- 5 Why 链 — 至少问 3 层"为什么"

**工具**:
- SMART 检查清单
- 5 Why 追问表
- 隐藏目标识别清单(老板没说的 6 件事)

**详细**: `references/scenarios/01-leader-assigns-task.md` · `references/models/smart-principles.md`

### Step 2 · 关键动作拆解 (Decompose)

**目标**: 把目标变成可执行的关键动作清单。

**必出物**:
- MECE 动作树(最多 3 层)
- 每动作的:负责人 / 起止日 / 衡量 / 风险预案
- 关键路径标注(必须按时完成的节点)
- 80/20 杠杆识别 — 找 20% 动作产出 80% 结果

**工具**:
- OKR 拆解表(O → KR1/KR2/KR3)
- KPI 分解矩阵
- 平衡积分卡四象限
- Sprint 2 周冲刺

**详细**: `references/models/okr-decomposition.md` · `references/scenarios/02-after-meeting.md`

### Step 3 · 资源 + 时间 (ART 不可能三角)

**目标**: 显性化资源/时间瓶颈,**和领导达成共识**。

**核心**: A 目标 / R 资源 / T 时间,三选二。

**必出物**:
- 当前 ART 三角的 3 个方案(目标不变动 vs 资源追加 vs 时间延后)
- 资源清单(人 / 钱 / 信息 / 时间 / 协作)
- 时间分配表(季度/月/周/日)
- **和领导沟通的 ART 沟通话术**

**工具**:
- ART 不可能三角画布
- 资源申请清单

**详细**: `references/models/art-impossible-triangle.md` ← **重点文件**

### Step 4 · 汇报对齐 + 防甩锅 (Report + CYA)

**目标**: 让领导知道进度,让同事无法甩锅,**留痕自保**。

**必出物**:
- 汇报节奏表(日 / 周 / 月 / 季度)
- 风险前置模板(问题 + 影响 + 解决方案)
- 留痕清单:每件关键决策邮件化 + 抄送关键人
- 防甩锅协议 5 条(谁说 + 何时 + 怎么记)

**工具**:
- 周报模板(月度复盘核心)
- 风险前置 SCQA 框架
- 留痕清单

**详细**: `references/scenarios/04-weekly-meeting.md` · `references/templates/weekly-report.md`

### Step 5 · 沉淀闭环 (Closure)

**目标**: 项目结束 ≠ 经验沉淀,**进入知识库才算闭环**。

**必出物**:
- 复盘报告(GRAI 四段)
- 个人作品集更新
- 知识库沉淀条目
- **月度目标管理学习报告(本 skill 特色)**

**工具**:
- GRAI 复盘模板
- PDCA 闭环表
- 月度学习报告模板(自动模板)

**详细**: `references/models/grai-retrospective.md` · `references/models/pdca-cycle.md` · `references/templates/monthly-learning-report.md`

---

## 🔍 前置 — 情境智慧 (Context First)

**主公触发本 skill 后,我需要先补齐 4 项信息**:

| 项 | 来源 | 补不齐怎么办 |
|---|---|---|
| **① 组织战略目标** | 主公主动给 / 公司 OKR / 战略文件 | 主公对话里给关键句 |
| **② 领导管理风格** | 主公描述 + 历史互动 | 主公描述 1-2 句即可 |
| **③ 主公个人优劣** | 主公自评 + 历次对话沉淀 | 月度报告里自动更新 |
| **④ 同事关系 + 部门政治** | 主公描述 | 主公说关键人即可 |

**协议**:
- **首次使用**: 我会主动问这 4 项,主公可选口头补,也可让我搜本地文件
- **后续使用**: 主公不必重复 — 我从对话历史/月度报告里读
- **省略兜底**: 主公说"跳过情境"时,我会**用行业默认假设 + 明确标注假设前提**

详细:`references/context-gathering.md`

---

## 🔄 后置 — 沉淀落实 (Closure)

**5 项产出,每次目标结束都要交**:

| 项 | 触发 | 模板 |
|---|---|---|
| **周报提交** | 每周五 | `references/templates/weekly-report.md` |
| **项目追踪表** | 每次 Sprint 结束 | `references/templates/project-tracker.md` |
| **复盘总结** | 季度/项目结束 | `references/models/grai-retrospective.md` |
| **个人作品集** | 月度 | 主公作品集目录(主公指定) |
| **知识库沉淀** | 任何新规律 | `references/templates/knowledge-base-entry.md` |

---

## 🔁 月度迭代闭环 (Monthly Learning Loop)

> **本 skill 区别于普通目标工具的核心特色**。

### 月度自动产出

每月最后一周,我会主动整理本月 4 项主公的**目标管理表现**:

| 维度 | 来源 | 输出 |
|---|---|---|
| **长板** | 哪类目标拆得好 / 哪些汇报效果好 | "本月你最好的动作: ..." |
| **弱点** | 哪类目标反复拖延 / 哪些资源协调失败 | "本月你反复卡在: ..." |
| **待提升** | 比上月进步的地方 + 还可继续练 | "本月你比上月进步: ..." |
| **需注意** | 哪些事差点背锅 / 哪些关系没维护好 | "本月你的盲点: ..." |

**报告模板**: `references/templates/monthly-learning-report.md`

### 双向迭代机制

```
主公 ←→ skill
  │         │
  │  多次目标拆解  │
  │ ─────────→ │
  │         沉淀主公风格
  │         沉淀主公弱项
  │         沉淀主公典型失败模式
  │         │
  │  ←───────── │
  │  月度报告  │
  │  + 更准的提问 │
  │  + 更准的方案 │
```

**为什么这样设计**:
- 用得越多,我越了解主公(避免每次重新问 4 项情境)
- 用得越多,主公越清楚自己的模式(避免盲点)
- **互为镜像的成长** — skill 是主公的"外脑教练",主公是 skill 的"训练数据源"

---

## 🚨 必守 8 条 Hard Rules

| # | Rule | 违反即停 |
|---|---|---|
| R1 | **不替领导拆目标** — SMART 是辅助拆,不是替他定;模糊就让领导说清 | ✋ |
| R2 | **ART 三角必显化** — 任何目标调整都要先讲清楚"动 A 还是动 R 还是动 T" | ✋ |
| R3 | **汇报含风险+方案** — 不许只报进度不报问题 | ✋ |
| R4 | **关键决策必留痕** — 邮件化 + 抄送 + 日期戳;口头决策不算 | ✋ |
| R5 | **背锅预警必触发** — 涉及跨部门/上级交办/合规风险,必主动留痕 | ✋ |
| R6 | **不接甩过来的锅** — 同事说"你顺便做下" — 必须用 ART 三角回应 | ✋ |
| R7 | **月度报告必生成** — 每月最后一周主动产出,不漏 | ✋ |
| R8 | **项目结束必 GRAI** — 没有复盘不算闭环,经验不入知识库 | ✋ |

---

## 🚨 防甩锅协议 5 条 (Blame-Defense Protocol)

> 主公原始痛点之一 — 单列。

1. **口头决策必转邮件** — "老板说周一前交" → 立即发邮件确认"理解周一前交,是这样吗"
2. **跨部门协作必有书面记录** — 微信群里说的话不算,必须有邮件或文档
3. **明确"不是我的责任范围"** — 同事甩活过来,立刻 ART 三角回应("做这件事,谁的目标/A 还是 R 谁出/什么时候要")
4. **进度主动透明** — 不让领导最后一天才知道延期;问题前置 24-48h
5. **失败复盘不带情绪** — "我没做到"vs"我被甩锅了" — 复盘只挖规律,不追责

详细:`references/blame-defense-protocol.md`

---

## 🚨 Anti-Patterns · 红线

| ❌ 反模式 | 为什么坏 | 修正 |
|---|---|---|
| **承接所有目标** | 来者不拒 = 资源被稀释 | ART 三角,必显化 |
| **汇报只报喜** | 领导最怕"突然延期" | 风险前置 + 解决方案 |
| **拆目标用大词** | "提升用户体验" = 没拆 | SMART 量化 |
| **不主动同步** | "我以为他知道了" | 关键节点必汇报 |
| **复盘追责** | 把复盘搞成批斗会 | GRAI 只挖规律 |
| **月度报告缺漏** | 错过自我迭代窗口 | 每月最后一周强制产出 |
| **同事甩活直接做** | 默认承接 = 默认背锅 | ART 三角回应 |
| **不写就干** | 重要事情不写文档 | R4 留痕协议 |

---

## 📚 资源引用

### 模型详解(references/models/)

| 文件 | 内容 |
|---|---|
| [`smart-principles.md`](references/models/smart-principles.md) | SMART 5 维度 + 模糊目标 vs 量化目标对照 |
| [`okr-decomposition.md`](references/models/okr-decomposition.md) | OKR O/KR 拆解 + 3 层 OKR 嵌套 + Q1/Q2/Q3 季度化 |
| [`kpi-breakdown.md`](references/models/kpi-breakdown.md) | KPI 顶层→中层→执行层分解 + 权重分配 |
| [`balanced-scorecard.md`](references/models/balanced-scorecard.md) | BSC 4 象限 + 战略地图 |
| [`sprint-methodology.md`](references/models/sprint-methodology.md) | Sprint 2 周冲刺 + 站会 + 燃尽图 |
| [`art-impossible-triangle.md`](references/models/art-impossible-triangle.md) | **A/R/T 不可能三角** — 重点文件,3 套方案模板 |
| [`pdca-cycle.md`](references/models/pdca-cycle.md) | PDCA 4 步闭环 + 每步必出物 |
| [`grai-retrospective.md`](references/models/grai-retrospective.md) | GRAI 复盘 + 与 PDCA 区别 |

### 场景模板(references/scenarios/)

| 文件 | 内容 |
|---|---|
| [`01-leader-assigns-task.md`](references/scenarios/01-leader-assigns-task.md) | 领导布置工作 → 5 Why + 隐藏目标识别 |
| [`02-after-meeting.md`](references/scenarios/02-after-meeting.md) | 经营会议后拆目标 → OKR + KPI 拆解 |
| [`03-cross-team-alignment.md`](references/scenarios/03-cross-team-alignment.md) | 跨人对齐 → RACI + 共识协议 |
| [`04-weekly-meeting.md`](references/scenarios/04-weekly-meeting.md) | 周月会议 → 议程 + 站会 |
| [`05-retrospective.md`](references/scenarios/05-retrospective.md) | 复盘会 → GRAI 流程 + 主持脚本 |
| [`06-resource-request.md`](references/scenarios/06-resource-request.md) | 资源申请 → ART 沟通话术 |

### 模板库(references/templates/)

| 文件 | 内容 |
|---|---|
| [`weekly-report.md`](references/templates/weekly-report.md) | 周报模板:本周完成 / 下周计划 / 风险 / 资源需求 |
| [`project-tracker.md`](references/templates/project-tracker.md) | 项目追踪表:动作/负责人/起止/状态/风险 |
| [`monthly-learning-report.md`](references/templates/monthly-learning-report.md) | 月度目标管理学习报告 — 本 skill 核心特色 |
| [`knowledge-base-entry.md`](references/templates/knowledge-base-entry.md) | 知识库沉淀条目模板 |

### 协议文件

| 文件 | 内容 |
|---|---|
| [`context-gathering.md`](references/context-gathering.md) | 前置情境智慧:4 项信息怎么补齐 |
| [`blame-defense-protocol.md`](references/blame-defense-protocol.md) | 防甩锅 5 条协议详细 |
| [`hidden-goals-checklist.md`](references/hidden-goals-checklist.md) | 领导没说的 6 件事 — 隐藏目标识别 |

### examples/

| 文件 | 内容 |
|---|---|
| [`examples/01-leader-50w-sales.md`](examples/01-leader-50w-sales.md) | **主公原用例**:领导让下周做 50 万业绩,HTML 完整方案 |
| [`examples/02-cross-team-alignment.md`](examples/02-cross-team-alignment.md) | 跨部门目标对齐案例 |
| [`examples/03-blame-incident.md`](examples/03-blame-incident.md) | 差点背锅 — 怎么处理 |

---

## 🛠 自检 Checklist(每个方案输出前)

- [ ] Step 1-5 每步都有必出物?(缺哪步 → 补)
- [ ] 目标 SMART 过了吗?(Specific / Measurable / Achievable / Relevant / Time-bound)
- [ ] ART 三角显化了吗?(给领导看的方案有 A/R/T 三选项)
- [ ] 风险前置了吗?(汇报里有"问题 + 影响 + 方案")
- [ ] 留痕清单做了吗?(关键决策邮件化了吗)
- [ ] 同事甩活的话用 ART 回应了吗?
- [ ] 触发月度报告生成?(每月最后一周)
- [ ] GRAI 复盘做了吗?(项目结束)
- [ ] Hard Rules 8 条全过?

**主公记住**: **接目标 → SMART 拆 → ART 谈 → 汇报对齐 → 防甩锅 → 月度闭环**。漏一步就埋雷。