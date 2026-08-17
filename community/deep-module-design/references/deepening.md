# Deepening — 加深一个浅模块集群

本文假设你已读过 [SKILL.md](../SKILL.md) 并掌握 **module / interface / seam / adapter** 词汇。

## 依赖分类

评估候选加深模块时，先分类其依赖。类别决定了加深后如何跨 seam 测试。

### 1. 进程内（In-process）

纯计算、内存状态、无 I/O。**总可加深**——合并模块，直接通过新接口测试。不需要 adapter。

### 2. 本地可替代（Local-substitutable）

依赖有本地测试替代物（PGLite 替 Postgres、内存文件系统替真文件系统）。若有 stand-in，**可加深**。加深后的模块用测试 suite 内的 stand-in 测试。seam 是内部的；模块外部接口**不需要 port**。

### 3. 远程但自有（Remote but owned，Ports & Adapters）

你自己的服务跨网络边界（微服务、内部 API）。在 seam 上定义 **port**（接口）。深模块拥有逻辑；transport 作 **adapter** 注入。测试用内存 adapter，生产用 HTTP/gRPC/queue adapter。

**推荐形态**："Define a port at the seam, implement an HTTP adapter for production and an in-memory adapter for testing, so the logic sits in one deep module even though it's deployed across a network."

### 4. 真外部（True external，Mock）

你不控制的第三方服务（Stripe、Twilio）。加深模块把外部依赖作注入 port；测试提供 mock adapter。

---

## Seam 纪律

- **一个 adapter = 假设 seam；两个 adapter = 真实 seam。** 除非至少两个 adapter 是合理的（典型：生产 + 测试），否则不要引入 port。单 adapter seam 只是间接层。
- **内部 seam vs 外部 seam。** 深模块可以有内部 seam（私有，内部测试用）+ 外部 seam（公开接口）。不要因为测试方便就把内部 seam 暴露到接口。

---

## 测试策略：替换，不是叠加

- 旧浅模块上的单元测试 → 加深后**删除**（已被加深模块新接口的测试替代）。
- 在加深模块的**接口**上写新测试。**接口即测试面**。
- 测试断言通过接口的可观察结果，**不查内部状态**。
- 测试应在内部重构后存活——它描述行为，不是实现。若测试必须随实现变更而变 → 它越过了接口。

---

## 来源

本文改编自 [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design/DEEPENING.md)，遵循 MIT License。