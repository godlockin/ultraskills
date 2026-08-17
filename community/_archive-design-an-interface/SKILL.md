---
name: design-an-interface
description: ⚠️ ARCHIVED — 内容已被 community/deep-module-design 完整覆盖（含 references/design-it-twice.md）。Use community/deep-module-design 代替本 skill。
github_url: https://github.com/mattpocock/skills
github_hash: 60aa99c0230fbac087514ba5fca2ae6e519965fe
version: 1.0.0
created_at: 2026-04-26T00:00:00Z
archived_at: 2026-08-05T00:00:00Z
archived_reason: 70% 重合于 deep-module-design，后者是完整词汇体系 + 含 design-it-twice 流程
replacement: community/deep-module-design
entry_point: SKILL.md
dependencies: []
tags: [design, architecture, api, interface, parallel-agents, archived]
---

> **⚠️ 本 skill 已归档（2026-08-05）**
>
> 原因：70% 内容重合于 `community/deep-module-design`，后者是完整词汇体系（module/interface/seam/adapter/leverage/locality/depth）+ 包含完整的 design-it-twice 流程（references/design-it-twice.md）。
>
> **请使用 `deep-module-design`** 替代本 skill。
>
> 本文件保留以维护 git 历史与 arena 历史分数。

# Design an Interface

Based on "Design It Twice" from "A Philosophy of Software Design": your first idea is unlikely to be the best. Generate multiple radically different designs, then compare.

## Workflow

### 1. Gather Requirements

Before designing, understand:

- [ ] What problem does this module solve?
- [ ] Who are the callers? (other modules, external users, tests)
- [ ] What are the key operations?
- [ ] Any constraints? (performance, compatibility, existing patterns)
- [ ] What should be hidden inside vs exposed?

Ask: "What does this module need to do? Who will use it?"

### 2. Generate Designs (Parallel Sub-Agents)

Spawn 3+ sub-agents simultaneously using Task tool. Each must produce a **radically different** approach.

```
Prompt template for each sub-agent:

Design an interface for: [module description]

Requirements: [gathered requirements]

Constraints for this design: [assign a different constraint to each agent]
- Agent 1: "Minimize method count - aim for 1-3 methods max"
- Agent 2: "Maximize flexibility - support many use cases"
- Agent 3: "Optimize for the most common case"
- Agent 4: "Take inspiration from [specific paradigm/library]"

Output format:
1. Interface signature (types/methods)
2. Usage example (how caller uses it)
3. What this design hides internally
4. Trade-offs of this approach
```

### 3. Present Designs

Show each design with:

1. **Interface signature** - types, methods, params
2. **Usage examples** - how callers actually use it in practice
3. **What it hides** - complexity kept internal

Present designs sequentially so user can absorb each approach before comparison.

### 4. Compare Designs

After showing all designs, compare them on:

- **Interface simplicity**: fewer methods, simpler params
- **General-purpose vs specialized**: flexibility vs focus
- **Implementation efficiency**: does shape allow efficient internals?
- **Depth**: small interface hiding significant complexity (good) vs large interface with thin implementation (bad)
- **Ease of correct use** vs **ease of misuse**

Discuss trade-offs in prose, not tables. Highlight where designs diverge most.

### 5. Synthesize

Often the best design combines insights from multiple options. Ask:

- "Which design best fits your primary use case?"
- "Any elements from other designs worth incorporating?"

## Evaluation Criteria

From "A Philosophy of Software Design":

**Interface simplicity**: Fewer methods, simpler params = easier to learn and use correctly.

**General-purpose**: Can handle future use cases without changes. But beware over-generalization.

**Implementation efficiency**: Does interface shape allow efficient implementation? Or force awkward internals?

**Depth**: Small interface hiding significant complexity = deep module (good). Large interface with thin implementation = shallow module (avoid).

## Anti-Patterns

- Don't let sub-agents produce similar designs - enforce radical difference
- Don't skip comparison - the value is in contrast
- Don't implement - this is purely about interface shape
- Don't evaluate based on implementation effort
