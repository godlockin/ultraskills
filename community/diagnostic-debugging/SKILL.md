---
name: diagnostic-debugging
description: 硬 bug 与性能回退的诊断循环。Use when user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow. 严格 6 阶段：建反馈环 → 重现+最小化 → 假设 → 探测 → 修复+回归测试 → 清理+复盘。核心铁律：Phase 1 必须先有 tight red-capable 反馈环，未达标禁止进入 Phase 2。用法关键词:debug、bug 排查、性能回退、假设驱动、最小重现、回归测试。
version: 1.0.0
tags: [engineering, debugging, methodology, performance, testing, community]
source: https://github.com/mattpocock/skills (MIT)
author: Matt Pocock
---

# Diagnostic Debugging（诊断调试）

硬 bug 的纪律。**没有明确理由不跳过任何阶段**。

> **本 skill 的核心铁律**：跳到"先读代码做理论"是本 skill 阻止的**确切失败**。Phase 1 必须先有 tight red-capable 反馈环，未达标禁止进入 Phase 2。

探索代码库前，先读项目的 `CONTEXT.md`（若有）获取相关模块的心智模型，并检查触及区域的 ADR。

---

## Phase 1 — 建反馈环（This is the skill）

**这是核心。** 其他阶段都是机械执行。如果你有一个 **tight** 的通过/失败信号能针对**此** bug 变红——你会找到根因；二分、假设、插桩都只是消耗这个信号。如果你没有，再怎么盯着代码也没救。

**在这里花不成比例的努力。要激进，要创造，拒绝放弃。**

### 构造反馈环的方法（按此顺序尝试）

1. **失败测试**——任何能触及 bug 的 seam：单元、集成、E2E
2. **Curl / HTTP 脚本**——对运行中的 dev server
3. **CLI 调用 + fixture 输入**——diff stdout 与 known-good snapshot
4. **无头浏览器脚本**（Playwright / Puppeteer）——驱动 UI，断言 DOM/console/network
5. **重放捕获的 trace**——把真实网络请求 / payload / event log 存盘，在隔离环境重放
6. **临时 harness**——起一个最小系统子集（一个服务，mock 依赖），单次函数调用覆盖 bug 路径
7. **属性 / fuzz 循环**——若 bug 是"有时输出错"，跑 1000 个随机输入看失败模式
8. **二分 harness**——若 bug 出现在两个已知状态间（commit、dataset、version），自动化 "boot 在状态 X，检查，重复"，可用 `git bisect run`
9. **差分 loop**——同一输入跑老版本 vs 新版本（或两种配置），diff 输出
10. **HITL bash 脚本**——最后一招。若必须人点击，用 `scripts/hitl-loop.template.sh` 驱动他们，loop 仍是结构化的。捕获的输出喂回给你

**建好正确反馈环，bug 80% 已解。**

### 收紧 loop

把 loop 当产品。一旦有 _一个_ loop，**收紧**：

- 能更快吗？（缓存 setup、跳过不相关 init、缩窄测试范围）
- 信号更尖锐吗？（断言具体症状，不是"没崩"）
- 更确定性吗？（固定时间、seed RNG、隔离文件系统、冻结网络）

30 秒 flaky loop 几乎等于无 loop；2 秒确定性 loop 是**调试超能力**。

### 非确定性 bug

目标不是干净复现，而是**更高复现率**。触发 100 次，并行，加压力，缩窄时间窗口，注入 sleep。50% flaky bug 可调试；1% 不可——继续提高复现率到可调试为止。

### 当你真的建不出 loop

**停下来明确说**。列出尝试过的。请用户提供：(a) 能复现的环境访问，(b) 捕获的产物（HAR、日志 dump、core dump、带时间戳的录屏），或 (c) 添加临时生产插桩的权限。**不要**没 loop 就跳到假设。

### 完成标准 — 一个 tight loop that goes red

Phase 1 完成当且仅当 loop **tight** 且 **red-capable**：你能说出**一条命令**——脚本路径、测试调用、curl——已**实际跑过至少一次**（贴出调用和输出），且满足：

- [ ] **Red-capable**——驱动实际 bug 代码路径，断言**用户的精确症状**，能在此 bug 上变红，修好后变绿。不是"跑不崩"——必须能**抓住这个具体 bug**
- [ ] **确定性**——每次跑同 verdict（flaky bug：固定 + 高复现率，见上）
- [ ] **快速**——秒级，不是分钟
- [ ] **Agent 可跑**——无人值守可跑；人在 loop 中只能通过 `scripts/hitl-loop.template.sh`

**若发现自己在此命令存在前读代码建理论，停下来——跳到假设正是本 skill 阻止的失败。没有 red-capable 命令，没有 Phase 2。**

---

## Phase 2 — 重现 + 最小化

跑 loop。看它变红——bug 出现。

确认：

- [ ] Loop 产生的失败模式是**用户描述的**——不是附近的另一个失败。错 bug = 错修复
- [ ] 多次跑都可重现（或对非确定性 bug，重现率高到可调试）
- [ ] 已捕获精确症状（错误消息、错误输出、慢耗时），后续阶段可验证修复是否真解决它

### 最小化

一旦红了，把 repro 缩到**还能变红的最小场景**。一次一个地切输入、调用方、配置、数据、步骤，每次切后重跑 loop——只保留对失败 load-bearing 的部分。

为什么：最小 repro 缩小 Phase 3 的假设空间（更少活动部件可怀疑），且成为 Phase 5 的干净回归测试。

**Done when**：每个剩余元素都是 load-bearing——移走任何一个都让 loop 变绿。

未同时完成重现 + 最小化，禁止进入 Phase 3。

---

## Phase 3 — 假设

测试任何假设前先生成 **3–5 个排序好的假设**。单假设生成会锚定在第一个似是而非的想法上。

每个假设必须**可证伪**——说出它作的预测。

> 格式："如果 <X> 是原因，那么 <改变 Y> 会让 bug 消失 / <改变 Z> 会让 bug 加重。"

若说不出预测，假设只是 vibe——丢弃或磨利它。

**测试前向用户展示排序列表。** 他们常有领域知识能瞬间重排（"我们刚部署了 #3 的变更"），或知道已排除的假设。廉价检查点，大时间节省。不阻塞——用户 AFK 时按你的排序继续。

---

## Phase 4 — 插桩

每个探针必须对应 Phase 3 的一个具体预测。**一次只改一个变量。**

工具偏好：

1. **Debugger / REPL 检查**（若环境支持）。一个断点 > 10 个日志
2. **针对性日志**——在能区分假设的边界处
3. **绝不**"日志全打再 grep"

**每个调试日志加唯一前缀**，如 `[DEBUG-a4f2]`。清理时一个 grep。未加标签的日志活下来，加标签的日志死。

**性能分支。** 对性能回退，日志通常错。改用：建基线测量（timing harness、`performance.now()`、profiler、query plan），然后二分。**先测，再修**。

---

## Phase 5 — 修复 + 回归测试

**先**写回归测试**再**修——但仅当有**正确 seam**。

正确 seam 是测试在其中能以调用方实际发生的方式执行**真实 bug 模式**的 seam。若唯一可用 seam 太浅（单调用方测试，但 bug 需要多调用方；单测无法复现触发 bug 的链路），那儿的回归测试给人虚假信心。

**若无正确 seam，这就是发现本身。** 标注它。代码库架构在阻止 bug 被锁定。给下一阶段标记。

若有正确 seam：

1. 把最小 repro 转成该 seam 的失败测试
2. 看它失败
3. 应用修复
4. 看它通过
5. 对原始（未最小化的）场景重跑 Phase 1 反馈环

---

## Phase 6 — 清理 + 复盘

宣布 done 前必须：

- [ ] 原始 repro 不再重现（重跑 Phase 1 loop）
- [ ] 回归测试通过（或已记录 seam 缺失）
- [ ] 所有 `[DEBUG-...]` 插桩已删除（grep 前缀）
- [ ] 临时原型已删除（或移至明确标记的 debug 位置）
- [ ] 实际正确的假设已写进 commit / PR message——让下一个调试者学到

**然后问：什么本可阻止这个 bug？** 若答案涉及架构变更（无好测试 seam、调用方纠缠、隐藏耦合），把具体内容交给 `/improve-codebase-architecture` skill。**修复落地后**再建议——你现在比开始时信息更多。

---

## 引用与致谢

本 skill 改编自 Matt Pocock 的 [`diagnosing-bugs`](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs)，遵循 MIT License。本仓库引入已剥离项目特定配置（hitl-loop 脚本需用户自行实现），保留 6 阶段纪律与方法论。