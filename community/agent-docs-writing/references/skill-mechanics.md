# Skill Mechanics — Skill 专属写作机制

本文是 [`writing-for-agents`](../SKILL.md) 在 skill 这种文档上的具体延伸：frontmatter、invocation 选择、router skill。其他写作内容是 `SKILL.md` 的通用参考。

---

## Invocation 选择

两个选择，权衡两份成本：

- **Model-invoked skill**保留 `description`，让 agent 自主触发——其他 skill 也能触及。你仍可输它名：model-invocation 永远 _包含_ 用户可达；description 只增加 agent 发现，从不剥夺人的可达。description 是 skill 的顶层上下文指针，强制始终加载——常驻上下文成本换发现性。一个内容全是参考的 model-invoked skill 也是共享参考的家：别的 skill 可 invoke 它，多个 skill 需要的参考住一处。机制：省略 `disable-model-invocation`，写面向模型的 description 携带 trigger 分支（`SKILL.md` 的指针写作规则全适用）。
- **User-invoked skill**把 description 从 agent 范围剥走：只有人输名能触发，没有任何 skill 能。零上下文成本，但花认知成本——你得记得它存在。机制：设 `disable-model-invocation: true`；`description` 变面向人——一行摘要，trigger 列表剥走。

仅在 agent 必须自取或别 skill 必须取时选 model-invocation。若仅手工触发，做 user-invoked 不付上下文成本。

两个 user-invoked skill 都需要的共享参考住哪儿都不行——都没 description，谁也触发不了谁。推到 skill 系统外的纯文件：任何 skill 可指的外部参考。

---

## 按 Invocation 拆分

拆分（writing-for-agents）之 invocation 切（序列切在 `SKILL.md`）：当你有应独立触发的独立首词——你在 prompt 里真用的 trigger 词——或别 skill 必须取时，拆出 model-invoked skill。你为新常驻 description 付上下文成本，所以独立可达必须值。

---

## Router Skills

当 user-invoked skills 多到记不过来，那累积的认知成本由 **router skill** 治好：一个 user-invoked skill 命名其他 skill 并指明何时取用，让人记一个而非多个。它只能提示不能触发：user-invoked skills 没 description，除了人没人能取它们。

---

## 来源

本文改编自 [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents/SKILL-MECHANICS.md)，遵循 MIT License。