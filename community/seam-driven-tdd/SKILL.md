---
name: seam-driven-tdd
description: Seam 驱动的 TDD——红绿循环 + 在预先约定的 seam 上测试 + tracer bullet 垂直切片。Use when user wants to build features or fix bugs test-first, mentions "red-green-refactor", wants integration tests, or is using /deep-module-design vocabulary. 核心铁律:test only at pre-agreed seams + vertical slice + red before green + expected values from independent source of truth。用法关键词:TDD、红绿循环、测试驱动、垂直切片、tracer bullet、seam 测试、单元测试、回归测试。
version: 1.0.0
tags: [engineering, tdd, testing, methodology, community]
source: https://github.com/mattpocock/skills (MIT)
author: Matt Pocock
---

# Seam-Driven TDD（Seam 驱动的 TDD）

TDD 是 red → green 循环。本 skill 是让该循环产生**值得保留的测试**的参考：什么是好测试、测试去哪、反模式、循环规则。每节在每个 cycle 都适用——**循环前和循环中**查，不是之后。

> **核心**：与 `/deep-module-design` 配合使用——seam 词汇 + TDD 纪律 = 完整方法论。

探索代码库前，先读项目 `CONTEXT.md`（若有）让测试名和接口词汇匹配项目领域语言，并尊重触及区域的 ADR。

---

## 什么是好测试

测试通过**公共接口**验证行为，**不**验证实现细节。代码可完全变；测试不应。好测试读起来像规范——"user can checkout with valid cart" 告诉有什么能力——且因不关心内部结构而存活重构。

见 [references/tests.md](references/tests.md) 看示例，[references/mocking.md](references/mocking.md) 看 mock 指南。

---

## Seam — 测试去哪

**Seam** 是公共边界——观察行为而不伸手进去的接口。测试活在 seam 上，永不针对内部。

**只在预先约定的 seam 上测。** 写任何测试前，写下要测的 seam 并与用户确认。未确认的 seam 上不写测试。你不能测一切——事前约定 seam 是让测试力量落在关键路径和复杂逻辑而非每个边缘情况上。

问："公共接口是什么，应测哪些 seam？"

---

## 反模式

- **Implementation-coupled**（实现耦合）—— mock 内部协作者，测私有方法，或通过侧通道验证（查 DB 代替用接口）。信号：refactor 后行为没变但测试挂。
- **Tautological**（重言式）—— 断言按代码方式重算期望值（`expect(add(a, b)).toBe(a + b)`、手动 snapshot 用同样方式导出、常量断言等于自身），所以按构造通过，永不和代码不一致。期望值必须来自独立真相源——known-good literal、worked example、spec。
- **Horizontal slicing**（水平切片）—— 先写所有测试，再写所有实现。批量测试验证 _想象的_ 行为：你测事物的_形状_而非用户面对行为，测试对真实变化不敏感，且你在理解实现前就承诺了测试结构。改用 **vertical slice**——一个测试 → 一个实现 → 重复，每个测试是**tracer bullet**，响应上一个循环教你的东西。

---

## 循环规则

- **Red 在 green 前。** 先写失败测试，再写恰好让它过的代码。不预想未来测试或加投机功能。
- **一次一片。** 一个 seam、一个测试、一个最小实现每个 cycle。
- **重构不是循环的一部分。** 它属于 review 阶段（见 `code-review` skill），不是 red → green 实现 cycle。

---

## 与 deep-module-design 的协同

| deep-module-design 概念 | 在 TDD 中的角色 |
|---|---|
| **Seam** | 测试的唯一合法位置 |
| **Interface** | 测试断言的可观察面 |
| **Adapter** | 测试需要的 mock 对象 |
| **Depth** | 深模块 = 少测试覆盖多行为 |
| **删除测试** | "删掉测试，复杂度是否集中回到 caller？" |

组合威力：深模块设计让 seam 自然小且稳定，TDD 纪律让测试不越过 seam、断言通过 seam、期望值独立。

---

## 引用与致谢

本 skill 改编自 Matt Pocock 的 [`tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)，遵循 MIT License。含完整的 `tests.md`（好/坏测试对比）和 `mocking.md`（mock 时机）参考文档。