# 示例：写作技巧实战

## 例 1：弱 trigger 描述 → 强 trigger 描述

### ❌ 弱（variance bug：有时触发有时不）

```yaml
description: Helps with code quality and refactoring tasks.
```

问题：
- "Helps with" 太模糊——agent 不知道何时算"应该"触发
- "code quality" 与现有 skill 重叠，本 skill 实际只做**深度模块词汇**
- 没 trigger 分支

### ✅ 强（每次跑同一过程）

```yaml
description: 设计深模块——小接口藏大实现。Use when user wants to design or improve a module's interface, decide where a seam goes, make code more testable, or when another skill needs the deep-module vocabulary (module/interface/seam/adapter/leverage/locality/depth). 用法关键词:深模块、seam、接口设计、模块解耦、依赖注入、删除测试、可测试性。
```

改进：
- **首词前置**："设计深模块" 立即定位
- **trigger 分支明确**：4 个独立分支（设计 / 改进 / 决定 seam / 其他 skill 需要词汇）
- **用法关键词**：列出中英文关键词，让 user prompt 直接命中
- **领域词列举**：module/interface/seam 让 trigger 更精准

---

## 例 2：信息层级——该披露的披露

### ❌ 平铺（在主文件里塞太多参考）

```markdown
# Code Review Skill

做 code review。  
[200 行内联: 8 种 Fowler smell 详解 + 命名规范 + 类型安全 + 测试原则 + 安全检查清单 + 性能检查清单 + 国际化清单 + ...]
[50 行步骤：拉 diff、看 spec、对比、汇总]
```

问题：步骤只占 1/5，但被 4 倍参考稀释。attention 散开。

### ✅ 披露（参考进指针）

```markdown
# Code Review Skill

[SKILL.md 主文件]
- 步骤 1: 拉 diff
- 步骤 2: 读 spec
- 步骤 3: 并行两个 sub-agent（Standards + Spec）
- 步骤 4: 汇总

[按需查阅]
→ references/fowler-smells.md（仅 Standards 轴触发时载入）
→ references/security-checklist.md（仅安全相关变更触发时载入）
→ references/perf-checklist.md（仅性能敏感变更触发时载入）
```

每个 sub-agent 触发时只载入它要的参考。**主线 1/5 内容，主轴不被稀释**。

---

## 例 3：首词——把复述塌成 token

### ❌ 三处复述

```markdown
- 每个修改的模型必须被记录在 CONTEXT.md
- 每次你修改模型就要更新文档
- 不能修改模型而不更新 CONTEXT.md
```

### ✅ 一次首词 + token 重复

```markdown
- 每个模型变更都要更新 CONTEXT.md（**single source of truth**）
- 模型变更 → CONTEXT.md
- **single source of truth** 失守 = 模型与文档漂移
```

`single source of truth` 是首词——预先训练的紧凑概念，每次出现 agent 自动链接到"一处权威"。

---

## 例 4：完成标准——避免 premature completion

### ❌ 模糊边界

```markdown
## Step 3: Analyze the design

理解设计意图后继续。
```

问题："理解"无清晰边界，agent 会急着进入 Step 4。

### ✅ 清晰 + 穷尽标准

```markdown
## Step 3: Analyze the design

Done when:
- [ ] 已列出所有 module + interface 对应关系
- [ ] 每个 module 已分类 depth（deep / shallow / unknown）
- [ ] 每个 shallow module 已识别其 pass-through 风险（删除测试通过？）
- [ ] 已向用户展示分类表
```

4 个 checkable item，**清晰**（每项可 yes/no）+ **穷尽**（覆盖所有 module）。

---

## 来源

本文示例基于 [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-for-agents/) 的写作方法论，遵循 MIT License。