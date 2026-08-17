---
name: agent-docs-writing
description: 为 agent 写文档的方法论——skill / AGENTS.md / CLAUDE.md / 任何 agent 消费的指针文件。Use when creating or editing skills, modifying AGENTS.md or CLAUDE.md, or auditing an existing agent-facing document. 核心关注:上下文指针 + 信息层级 + 双成本预算 + leading words + 完成标准 + pruning。用法关键词:skill 写作、上下文预算、CLAUDE.md 优化、prompt 工程、agent-friendly 文档、信息层级、leading words、trigger 词。
version: 1.0.0
tags: [meta, engineering, writing, methodology, prompt-engineering, community]
source: https://github.com/mattpocock/skills (MIT)
author: Matt Pocock
---

# Agent Docs Writing（为 Agent 写文档）

写任何 agent 消费的文档——skill、`AGENTS.md` / `CLAUDE.md`、被指针指向的 doc——的参考。**包装不同，写作相同**：同一套杠杆让每个文档可预测——agent 每次跑同一**过程**，不是同一输出。

> **本 skill 的核心价值**：让 agent 文档不是"碰运气"，而是每次触发都给出可预测的工程化结果。

当文档本身是 skill 时，另读 [`references/skill-mechanics.md`](references/skill-mechanics.md) 看 frontmatter / invocation 选择 / router skill。

---

## 上下文指针（Context Pointer）

**上下文指针**是 agent 上下文中持有的引用，命名某个外部材料并编码触发条件。skill 的 description 是一个；`AGENTS.md` 里命名某 doc 的一行也是同种东西。指针的**措辞**——不是它的目标——决定 agent 何时抵达该材料，且多可靠。**弱措辞指针 + 必读目标 = variance bug**：先磨利措辞，磨不动再 inline。

指针做两件事——说明材料是什么，列出**应该触发抵达它的分支**（分支是文档处理的不同情形，所以不同跑次走不同路径）。**always-loaded 指针的每个字都每轮花钱**，比正文更值得剪枝：

- **首词前置**——指针在其触发工作处发力
- **每个分支一个 trigger**——给单一分支换同义词是同一分支写两遍；合并掉，只留真正不同的分支
- **剪掉正文已承载的身份**——别重复"这个 skill 是关于 X 的"

---

## 两个成本（Two Loads）

每个加进来的文档 / 指针花两份预算之一：

- **上下文成本（Context load）**——always-loaded 材料花在 agent 窗口上的代价：`AGENTS.md` 一行、skill description、任何每轮都坐在上下文里的东西，无论是否触发都烧 token 和注意力
- **认知成本（Cognitive load）**——花在人的代价：哪些文档存在、何时取用哪个。人就是索引。不是要最小化的成本——它是人的主动权的代价；在人的判断重要的地方面它，在不重要的地方撤它

只通过指针抵达的材料以指针自身一行的代价逃避上下文成本；完全没指针的材料完全压在认知成本上。

---

## 信息层级（Information Hierarchy）

文档由两种内容类型构成——**步骤**（agent 按序做的动作）和**参考**（按需查阅的定义、规则、事实）——可自由混合：全步骤（菜谱）、全参考（评审规则，本 skill）、或两者兼有。核心决策是每块在**信息层级**上的位置，按 agent 多立即需要该材料排序：

1. **In-file 步骤**——主层：agent 按序做的
2. **In-file 参考**——按需查阅。常是合理平铺的 peer-set（评审的每条规则在一级）——这是合理安排，不是 smell
3. **披露参考**——推到独立文件，靠上下文指针抵达，仅在指针触发时加载。跨度从同文件夹的 sibling 文件到完全外部参考（住在任何地方，任何文档可指）

推下去太少→顶层臃肿；推下去太多→隐藏了 agent 真正需要的材料。那股张力就是整个决策。

**渐进披露（Progressive disclosure）**是沿梯下移——出主文件，进指针后——让顶层保持清晰。**不**主要是 token 优化：它是层级如何被保护。**分支**是最干净的披露测试：每个分支需要的 inline；仅部分分支抵达的推指针后。当文档有步骤时，应被披露的 in-file 参考会埋没步骤，把关注它们变成掷色子——**variance 杠杆**，不只是清晰度问题。

**共置（Co-location）**是文件内的伙伴：梯子决定一块**走多远下**，共置决定**放什么旁边**。把概念的定义、规则、caveats 放一个标题下，别散开——读一处带出邻居。测试：文档读起来要像"为 agent 写的文档"——分组的材料那样读，散开的材料不。（与重复不同：重复在两处复述一个意思；散开把一个意思碎成多片。）

**蔓延（Sprawl）**是这里的失败模式：文档单纯太长，即使每行都活着且独特。注意力在富余处变薄，每多一行就是多一行保持相关。治疗是梯子：披露参考进指针，按分支或序列切，让每条路径只带它需要的。

---

## 步骤与完成标准

每个步骤终止于**完成标准**——告诉 agent 工作完成的条件。两个属性让它成为杠杆：

- **清晰度（Clarity）**——agent 能分辨 done vs not-done 吗？模糊的边界（"达到理解"）招来**过早完成（premature completion）**：在真完成前结束步骤，注意力滑向"已完成"。前方可见的步骤——**完成后步骤（post-completion steps）**——提供拉力；标准的清晰度是阻力。顺序防守：**先磨利边界**（局部便宜）；仅在不可化约地模糊**且**观察到赶时间时，按序列切把后置步骤藏起来——且只在跨真实上下文边界（handoff 或 subagent dispatch；inline 调用把后置步骤留在上下文里，啥也没清）时藏才有效。
- **要求（Demand）**——它要求多少。"每个修改的模型都被考虑"在"产生变更列表"做不到的地方强制彻底工作。需求驱动**跑腿（legwork）**——agent 在工作中挖的料，潜在措辞里而非写成独立步骤——它不绑步骤："每条规则都应用"绑一组平铺参考就像"每步都完成"绑一个序列，这是全参考文档仍承载穷尽性门槛的方式。

最强标准既可检查又穷尽。

---

## 何时拆分

一份文档拆两份花两份成本之一，所以只在切口赚得到时拆：

- **按序列**——拆步骤链中后置步骤诱惑 agent 赶前一步的地方。把它们藏起来逼对当前任务做更多跑腿。小心反面：合序列把每步的后置步骤暴露给后续，招过早完成。
- **按 invocation**——skill 专属：见 [`references/skill-mechanics.md`](references/skill-mechanics.md)。

---

## Leading Words（首词）

**首词**是模型预训练里已活着的紧凑概念，agent 跑文档时用它思考（_lesson_、_fog of war_、_tracer bullets_）。作为 token 重复，绝不作为句子，它积累分布式定义并以最少 token 锚定一整片行为，靠招募模型已持有的先验。清晰定义时造自己的词也行，但造词不招先验——你用定义 token 付了 pretrained 词免费给的钱；**先用现成的**。

它锚两次。在正文，_执行_：agent 每次该词出现都触及同一行为，且在平铺参考里把注意力聚焦到要找的一类事物。在指针，_触发_：同词活在你的 prompt、文档、代码库里，agent 把共享语言链到材料，更可靠地触及它。

猎机会用首词重构。三处展开的三位一体、用一句话比划一概念的指针——每处都是求塌成单 token 的段落：

- "fast, deterministic, low-overhead" → _tight_（一个 _tight_ 循环）
- "a loop you believe in" → _red_——模糊门变二元可观察状态（循环对 bug _变红_，或不变）

你赢两次：更少 token，给 agent 更利钩挂思考。**假设每份文档都背着首词应退役的复述——去找它们**。

**否定（Negation）**是这个杠杆旁的失败模式：以禁令驾驶把禁止行为拉进上下文，让它_更_可用，不是更不。_别想大象_，大象就在那；否定是弱修饰符，被强激活概念溢出，所以禁令半读成去做那事的指令。提示**正向**——说出目标行为（"写单行注释"）让被禁的永不被说。禁令只在不能正向表达时作为硬护栏赚它位置；即使那时，配上正向目标让注意力落该做的。

---

## 修剪（Pruning）

- 每个意思在**单一真相来源**——一个权威处，改行为只改一处。**重复**——同意思在多于一地——花维护和 token，并把意思在梯上的突出度吹到超出真实排位。（首词的偶发反面：刻意重复 token，绝不重复意思。）
- **环境**也是真相来源——`package.json` 脚本、配置文件、目录布局、`--help` 输出——重述它们的文档是**缓存**：一份 lookup 副本，仅当 lookup 昂贵时赚它的成本。缓存 agent 找不到的：未写的惯例、选择背后的原因、没配置坦白的坑。把单文件、单命令查找留给环境，那里不会过时。
- 逐行检查**相关性**：它还与文档做的事有关吗？一行因从无关任务（仅说明，或应被披露的分支）或描述的行为/世界变了而失去相关性而失相关。更短文档更易保持相关。无修剪纪律，默认命运是**沉积（sediment）**：陈层因添加感安全、移除感风险而沉降，直到你必须穿透它们找还活着的。
- 逐句猎**空操作（no-op）**：模型默认就遵守的指令花钱说空话。测试——它是否相对默认改变了行为？——是模型相对的，不是读者相对的：两人对 no-op 意见不一就是对默认意见不一，跑文档解决，不是辩论。当句子失败，删整句而非剪字。测试也评首词：词太弱打不过默认（_be thorough_ 当 agent 已 thorough-ish）就是 no-op，**修法是更强的词**（_relentless_），不是换技巧。

---

## 引用与致谢

本 skill 改编自 Matt Pocock 的 [`writing-for-agents`](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents)，遵循 MIT License。本仓库引入保留核心方法论与 SKILL-MECHANICS 完整内容。