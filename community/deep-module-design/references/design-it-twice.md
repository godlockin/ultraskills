# Design It Twice — 用并行 sub-agent 设计多个接口

当用户想为某个加深候选模块探索替代接口时，使用本并行 sub-agent 模式。基于 John Ousterhout 的 "Design It Twice"——你的第一个想法几乎从来不是最好的。

本文假设你已读过 [SKILL.md](../SKILL.md) 并掌握 **module / interface / seam / adapter / leverage** 词汇。

---

## 流程

### 1. 框定问题空间

spawn sub-agent 前，先写一份面向用户的问题空间说明：

- 任何新接口都需满足的约束
- 它依赖什么、依赖属于哪个分类（见 [deepening.md](deepening.md)）
- 一个粗略示例代码 sketch 来落地约束——不是提案，只是把约束具体化

向用户展示此说明后**立即**进入第 2 步。用户阅读和思考时，sub-agent 并行工作。

### 2. 并行 spawn sub-agent

用 Agent tool 并行 spawn 至少 3 个 sub-agent。每个必须产出**根本不同的**接口。

给每个 sub-agent 独立的技术 brief（文件路径、耦合细节、来自 [deepening.md](deepening.md) 的依赖分类、seam 背后是什么）。brief 与第 1 步面向用户的问题空间说明**相互独立**。给每个 agent **不同的设计约束**：

- Agent 1: "最小化接口——目标 1-3 个入口点。最大化单位入口点的 leverage。"
- Agent 2: "最大化灵活性——支持多种用例和扩展。"
- Agent 3: "为最常见调用方优化——让默认情况 trivial。"
- Agent 4（如适用）: "围绕 ports & adapters 为跨 seam 依赖设计。"

brief 中同时包含 [SKILL.md](../SKILL.md) 词汇和项目 `CONTEXT.md` 词汇，让每个 sub-agent 用与架构语言和项目领域语言一致的名字。

每个 sub-agent 输出：

1. Interface（类型、方法、参数 + 不变量、顺序、错误模式）
2. 用法示例（调用方如何使用）
3. seam 后实现隐藏了什么
4. 依赖策略和 adapters（见 [deepening.md](deepening.md)）
5. 权衡——leverage 在哪高、在哪薄

### 3. 展示并对比

依次展示设计让用户吸收，然后用散文对比。按 **depth**（接口 leverage）、**locality**（变更集中点）、**seam placement** 对比。

对比后给出你自己的推荐：哪个设计最强，为什么。若不同设计的元素可结合，提出 hybrid。**要观点鲜明**——用户要的是强读，不是菜单。

---

## 来源

本文改编自 [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design/DESIGN-IT-TWICE.md)，遵循 MIT License。