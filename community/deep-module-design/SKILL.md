---
name: deep-module-design
description: 设计"深模块"——小接口藏大实现。Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary (module/interface/seam/adapter/leverage/locality/depth). 用法关键词:深模块、seam、接口设计、模块解耦、依赖注入、删除测试、可测试性。
version: 1.0.0
tags: [engineering, design, methodology, code-quality, testing, community]
source: https://github.com/mattpocock/skills (MIT)
author: Matt Pocock
---

# Deep Module Design（深模块设计）

设计**深模块**：小接口 + 大实现，落在干净 seam 上，通过该接口可测。本 skill 提供 Kent Beck + John Ousterhout 体系下的统一词汇与原则。

> **本 skill 的核心价值**：当设计 / 重构 / 评审代码时，使用统一的 module/interface/seam/adapter 词汇，避免"组件/服务/API/边界"等含义模糊的词。

---

## 词汇表（严格使用，禁止替换）

| 词 | 定义 | 避免词 |
|---|---|---|
| **Module（模块）** | 任何有接口 + 实现的东西。规模无关：函数、类、包、跨层切片 | unit、component、service |
| **Interface（接口）** | 调用方使用模块必须知道的一切：类型签名 + 不变量 + 顺序约束 + 错误模式 + 必要配置 + 性能特征 | API、signature（过窄） |
| **Implementation（实现）** | 模块内部代码体。**Adapter（适配器）**是它的特例：小实现 + 大适配器（如 Postgres repo），或大实现 + 小适配器（如内存 fake） | — |
| **Depth（深度）** | 单位接口所能调用的行为量。**深模块** = 小接口 + 大实现；**浅模块** = 大接口 + 薄实现（避免） | — |
| **Seam（接缝）** | Michael Feathers 概念——一个不修改该处就能改变行为的地方，模块接口的**位置** | boundary（与 DDD bounded context 重载） |
| **Adapter（适配器）** | 在 seam 上满足接口的具体事物。描述**角色**，不描述**实质** | — |
| **Leverage（杠杆）** | 调用方从深度获得的好处：单位接口学习量换得更多能力 | — |
| **Locality（局部性）** | 维护方从深度获得的好处：变更 / bug / 知识 / 验证集中一处，**一次修复全局生效** | — |

---

## 深 vs 浅

**深模块** = 小接口 + 大实现（**目标**）：
```
┌─────────────────────┐
│   Small Interface   │  ← Few methods, simple params
├─────────────────────┤
│                     │
│  Deep Implementation│  ← Complex logic hidden
│                     │
└─────────────────────┘
```

**浅模块** = 大接口 + 薄实现（**避免**）：
```
┌─────────────────────────────────┐
│       Large Interface           │  ← Many methods, complex params
├─────────────────────────────────┤
│  Thin Implementation            │  ← Just passes through
└─────────────────────────────────┘
```

**设计接口时自问**：
- 能否减少方法数？
- 能否简化参数？
- 能否把更多复杂度藏起来？

---

## 4 条核心原则

1. **Depth 是接口的属性，不是实现的属性。** 深模块内部可以由小的、可 mock、可替换的部分组成——它们不属于接口。模块可以有**内部 seam**（私有，测试用）和**外部 seam**（公开，调用方用）。

2. **删除测试。** 想象删除该模块。若复杂度消失 → 它只是个 pass-through（浅）。若复杂度在 N 个调用方重新出现 → 它值得存在（深）。

3. **接口即测试面。** 调用方和测试穿过同一 seam。若要**越过**接口测试，模块形状大概率错了。

4. **一个适配器 = 假设 seam；两个适配器 = 真实 seam。** 不要引入 seam，除非真的有变化跨过它。

---

## 为可测试性设计

1. **接受依赖，不创建依赖**：
   ```typescript
   // 可测
   function processOrder(order, paymentGateway) {}

   // 难测
   function processOrder(order) {
     const gateway = new StripeGateway();
   }
   ```

2. **返回结果，不产生副作用**：
   ```typescript
   // 可测
   function calculateDiscount(cart): Discount {}

   // 难测
   function applyDiscount(cart): void {
     cart.total -= discount;
   }
   ```

3. **小表面积**：方法越少 → 测试越少；参数越少 → 测试 setup 越简单。

---

## 词汇关系图

```
Module ──── has ────> Interface
  │                      │
  │ has                  │ measured against
  ▼                      ▼
Seam (where Interface lives)
  │
  │ sits at
  ▼
Adapter
  │
  │ creates
  ▼
Depth → Leverage (for callers)
     → Locality (for maintainers)
```

- Module 只有一个 Interface（对外表面）
- Depth 是 Module 的属性，对 Interface 测量
- Seam 是 Module Interface 所在的位置
- Adapter 在 Seam 上满足 Interface
- Depth 产出 Leverage（给调用方）和 Locality（给维护方）

---

## 拒绝的框架

- ❌ "Depth = 实现行数 / 接口行数"（Ousterhout 早期版本）→ 鼓励实现注水。我们用 **depth-as-leverage**。
- ❌ "Interface" = TypeScript `interface` 关键字或 class 的 public methods → 过窄——这里 interface 包含**调用方必须知道的所有事实**。
- ❌ "Boundary" → 与 DDD bounded context 重载。改说 **seam** 或 **interface**。

---

## 依赖分类（决定如何跨 seam 测试）

| 类别 | 例子 | 加深策略 |
|---|---|---|
| **进程内** | 纯计算、内存状态、无 I/O | **总可加深**——合并模块，直接通过新接口测试，不需要 adapter |
| **本地可替代** | PGLite 替 Postgres、内存文件系统替真文件系统 | 可加深（若有 stand-in）。seam 是内部的；模块外部接口**不需要 port** |
| **远程但自有** | 自己的微服务、内部 API | 在 seam 上定义 **port**。深模块拥有逻辑，transport 作 adapter 注入。测试用内存 adapter，生产用 HTTP/gRPC adapter |
| **真外部** | Stripe、Twilio | 加深模块把外部依赖作注入 port；测试提供 mock adapter |

**Seam 纪律**：
- 一个 adapter = 假设 seam。两个 adapter（典型：生产 + 测试）= 真实 seam。**单 adapter seam 仅为间接层**。
- 内部 seam vs 外部 seam：深模块可以有私有内部 seam（仅内部测试用）+ 公开外部 seam。不要因为测试方便就把内部 seam 暴露到接口上。

**测试策略：替换，不是叠加**：
- 旧浅模块的单元测试 → 加深后**删除**（已被新接口测试替代）。
- 在加深模块的**接口**上写新测试。**接口即测试面**。
- 测试断言通过接口的可观察结果，不是内部状态。
- 测试应在内部重构后存活——它描述行为，不是实现。若测试随实现变更而变 → 它越过了接口。

---

## 深入

- **[references/deepening.md](references/deepening.md)**：依赖分类 + seam 纪律 + 替换而非叠加测试
- **[references/design-it-twice.md](references/design-it-twice.md)**：用并行 sub-agent 设计多个差异化接口，按 depth/locality/seam placement 对比
- **[examples/](examples/)**：本仓库内具体语言示例

---

## 引用与致谢

本 skill 改编自 Matt Pocock 的 [`codebase-design`](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design)，遵循 MIT License。本仓库引入已剥离项目特定配置（issue-tracker / setup 脚手架），保留核心方法论与统一词汇体系。