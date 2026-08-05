---
name: two-axis-code-review
description: 两轴 PR/code review——Standards（代码是否符合项目规范 + Fowler smell 基线）+ Spec（代码是否忠实实现 issue/spec 需求）。Use when user wants to review a branch, a PR, work-in-progress changes, or asks "review since X" / "评审这段改动" / "review this diff"。两个 sub-agent 并行跑，输出侧并排。用法关键词:code review、PR 评审、diff 审查、Standards axis、Spec axis、Fowler smells。
version: 1.0.0
tags: [engineering, code-review, methodology, quality, community]
source: https://github.com/mattpocock/skills (MIT)
author: Matt Pocock
---

# Two-Axis Code Review（两轴代码评审）

对一个固定点（commit、branch、tag 或 merge-base）起的变更做两轴 review。两个轴并行跑 sub-agent 不互相污染上下文，然后本 skill 汇总它们的发现。

**两个轴**：
- **Standards**——代码是否符合本仓库文档化的编码规范？
- **Spec**——代码是否忠实实现来源 issue / spec？

---

## 流程

### 1. 固定点（Fixed Point）

用户说的固定点都行——commit SHA、branch 名、tag、`main`、`HEAD~5` 等。若用户未指定，问。

一次捕获 diff 命令：`git diff <fixed-point>...HEAD`（三点，对比 merge-base）。也记 commit 列表：`git log <fixed-point>..HEAD --oneline`。

进入下一步前，确认固定点可解析（`git rev-parse <fixed-point>`）且 diff 非空。坏 ref 或空 diff 应在此失败——不在两个并行 sub-agent 里。

### 2. 识别 Spec 来源

按顺序找来源 spec：

1. commit message 里的 issue 引用（`#123`、`Closes #45`、GitLab `!67` 等）——通过 issue tracker 流程拉取
2. 用户作为参数传的路径
3. `docs/`、`specs/`、`.scratch/` 下与 branch 名或 feature 匹配的 spec 文件
4. 都没找到，问用户 spec 在哪。若用户说没有，**Spec** sub-agent 跳过并报告"无可用 spec"

### 3. 识别 Standards 来源

仓库里任何文档化代码该如何写的东西，如 `CODING_STANDARDS.md` 或 `CONTRIBUTING.md`。

除仓库文档外，Standards 轴**始终**带下面 **smell 基线**——一套固定的 Fowler code smells（_Refactoring_, ch.3），即便仓库啥也没文档化也适用。两条规则绑定它：

- **仓库覆盖。** 文档化的仓库标准总是赢；若它认可基线会 flag 的东西，抑制该 smell。
- **始终判断调用。** 每个 smell 是标注的启发（"可能 Feature Envy"），从不是硬违规——且像这里任何标准一样，跳过工具已强制执行的。

每个 smell 读 _它是什么_ → _如何修_；对照 diff：

- **Mysterious Name** — 函数/变量/类型名不揭示做什么或持什么。→ 重命名；若取不出诚实名，设计本身模糊。
- **Duplicated Code** — 同逻辑形状在变更的多个 hunk 或文件出现。→ 抽出共享形状，两处都调它。
- **Feature Envy** — 方法伸手进另一对象的数据多于自己的。→ 把方法移到它 envious 的数据上。
- **Data Clumps** — 同一小组字段或参数总一起旅行（一个想被生出来的类型）。→ 打成单一类型，传它。
- **Primitive Obsession** — 基本类型或字符串代替该有自己类型的领域概念。→ 给概念自己的小类型。
- **Repeated Switches** — 同 switch/if 级联在同一类型上反复出现在变更中。→ 换多态，或一处两站共享的 map。
- **Shotgun Surgery** — 一个逻辑变更迫 diff 中散落的多文件编辑。→ 把一起变的聚到一个 module。
- **Divergent Change** — 一个文件/module 因多个不相关原因被编辑。→ 切开让每个 module 只因一个原因变。
- **Speculative Generality** — 为 spec 没有的需求加的抽象/参数/钩子。→ 删；inline 回直到真需求出现。
- **Message Chains** — 调用方不该依赖的长 `a.b().c().d()` 导航。→ 把 walk 藏到第一个对象的一方法后。
- **Middle Man** — 主要只 delegate 下去的一个 class 或函数。→ 切掉，直接调真目标。
- **Refused Bequest** — 子类或实现者忽略或覆盖大部分继承来的。→ 丢继承，用组合。

### 4. 并行 spawn 两个 sub-agent

单条消息两次 `Agent` tool 调用。两个都用 `general-purpose`。

**Standards sub-agent prompt** — 含：

- 完整 diff 命令和 commit 列表
- 第 3 步找到的 standards-source 文件清单，**加上第 3 步的 smell 基线全文**粘贴——sub-agent 没有别的途径拿它
- brief："Report — 按 file/hunk 相关—— (a) diff 违反每个文档化标准的位置：cite 标准（文件 + 规则）；和 (b) 你看到的 baseline smell：起名它并 quote hunk。区分硬违规和判断调用——文档化标准违反可硬，但 baseline smell 始终判断调用，文档化仓库标准覆盖 baseline。跳过工具强制执行的。400 字以内。"

**Spec sub-agent prompt** — 含：

- diff 命令和 commit 列表
- spec 路径或已取内容
- brief："Report: (a) spec 要求但缺失或部分缺失的需求；(b) diff 中未被要求的行为（scope creep）；(c) 看起来已实现但实现像错的需求。每条 finding quote spec 行。400 字以内。"

若 spec 缺失，跳过 Spec sub-agent 并在最终报告里标注。

### 5. 汇总

在 `## Standards` 和 `## Spec` 标题下呈现两份报告，原样或微清理。**不**合并或重排 finding——两个轴是刻意分开的（见下 _为什么两轴_）。

结尾一行摘要：每轴总 finding 数，每轴内最严重问题（若有）。不要在两轴间挑单一赢家——那正是分离要阻止的重排。

---

## 为什么两轴

变更可过一轴败另一轴：

- 代码遵循每条标准但实现错东西 → **Standards pass, Spec fail.**
- 代码恰好做了 issue 要的事但破坏项目惯例 → **Spec pass, Standards fail.**

分开报告防止一轴掩盖另一轴。

---

## 引用与致谢

本 skill 改编自 Matt Pocock 的 [`code-review`](https://github.com/mattpocock/skills/tree/main/skills/engineering/code-review)，遵循 MIT License。本仓库引入已剥离项目特定配置（issue-tracker / `.scratch` 约定），保留两轴 + smell 基线核心方法论。