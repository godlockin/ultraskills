---
name: agent-optimizer-loop
description: "Use when designing or running an autonomous Agent optimization loop — where an Agent iteratively modifies an 'experiment unit', evaluates a metric, and keeps or discards changes. Based on the autoresearch pattern by Karpathy. Trigger when: user wants to auto-optimize prompts, code, configs, or any artifact via repeated Agent experimentation."
version: 1.0.0
tags: [agent, optimization, autonomous, loop, experiment]
---

# Agent Optimizer Loop

你是一个"自主优化循环"的设计者和执行者。这个模式让 Agent 像研究员一样，在无人值守的情况下持续迭代实验，寻找最优解。

---

## 核心模式：两层结构

```
外层（你执行）
  └─ 提假设 → 修改实验单元 → 触发内层 → 读结果 → keep/discard → 循环

内层（子进程/工具执行）
  └─ 输入: 一份实验单元
     执行: 固定资源预算
     输出: 一个目标指标数字
```

---

## 适用条件检查（设计新任务前必读）

### 硬性规定（五个，缺一不可）

| # | 条件 | 说明 |
|---|------|------|
| H1 | 单一可量化指标 | 一个数字，越高/低=越好，无歧义，不能是主观判断 |
| H2 | 评估完全自动化 | Agent 自己能读出数字，不需要人工参与 |
| H3 | 单次评估耗时有上限 | 理想几分钟，上限几小时，不确定何时结束=不可用 |
| H4 | 实验单元边界清晰 | 能改什么/不能改什么开始前定死，防止改掉评估标准 |
| H5 | 改进可叠加 | 好结果成为下次起点，否则是并行采样不是优化循环 |

### 软性规定（满足越多越好）

| # | 条件 | 说明 |
|---|------|------|
| S1 | 指标归一化 | 与 scale 无关，实验变化后结果仍可比 |
| S2 | 搜索空间有语义 | 代码/文本/配置 > 纯数字参数（后者用贝叶斯优化更好）|
| S3 | 外部记忆 | results.tsv 类的记录，对抗 context 遗忘 |
| S4 | simplicity criterion | 防止 Agent 堆 trick，明确简洁性偏好 |
| S5 | 失败模式确定 | 崩溃/超时可判断；"结果不太好"模糊，keep/discard 会出错 |

### 设计新优化任务的五个问题

在开始任何优化循环之前，必须明确：

1. **实验单元**：Agent 能修改什么？边界在哪里？（对应 autoresearch 的 train.py）
2. **目标指标**：单一可量化数字，更高/更低=更好，防止游戏化（对应 val_bpb）
3. **资源预算**：时间/token/调用次数上限，保证实验可比（对应 5 分钟时间预算）
4. **保留策略**：keep/discard 的判断标准，是否有 simplicity criterion
5. **审计机制**：人类如何事后理解发生了什么（对应 git log + results.tsv）

---

## 执行流程

### 阶段一：Setup（与用户确认后一次性执行）

```
1. 确定 run tag（如日期），创建分支/目录
2. 读取所有相关上下文文件
3. 验证评估函数可运行
4. 初始化 results.tsv（只写 header）
5. 跑一次 baseline（不做任何改动）
```

### 阶段二：实验循环（NEVER STOP，直到人工中断）

```
LOOP:
  1. 检查当前状态（git/文件/上一次结果）
  2. 提出一个具体的实验假设
  3. 修改实验单元
  4. commit（记录假设和修改）
  5. 运行评估：将输出重定向到 run.log，不要让输出污染 context
     示例: uv run train.py > run.log 2>&1
  6. 读取关键指标：grep 而非读全文
     示例: grep "^val_bpb:\|^peak_vram_mb:" run.log
  7. 判断结果：
     - 崩溃 → 尝试修复（≤3次），否则 discard，记 crash
     - 超时（>2x预算）→ kill，记 crash
     - 改善 → keep，advance
     - 持平/退步 → git reset，discard
  8. 记录到 results.tsv（tab分隔，不要逗号）
  9. 回到 1
```

### results.tsv 格式

```
commit\tmetric\tresource\tstatus\tdescription
```

- `metric`: 目标指标值，crash 记 0.000000
- `resource`: 资源使用量（内存/时间/费用），crash 记 0.0
- `status`: `keep` | `discard` | `crash`
- `description`: 这次实验尝试了什么（不要用逗号）

**此文件不提交到 git，保持 untracked。**

---

## 关键约束（不可违反）

- **NEVER STOP**：循环开始后不询问"要继续吗"，不等待用户确认
- **不污染 context**：训练/评估输出必须重定向到文件，只 grep 关键行
- **不修改 prepare.py 等锁定文件**：评估函数是地基，不可动
- **不安装新依赖**：只用已有工具
- **超时即 kill**：实验超过 2x 预算直接终止，记 crash

---

## Simplicity Criterion

每次决定是否 keep 时，额外问自己：

| 情况 | 决策 |
|------|------|
| 指标改善 + 代码更简单 | 强力 keep |
| 指标改善 + 代码复杂度不变 | keep |
| 指标微小改善（<0.1%）+ 代码更复杂 | discard |
| 指标不变 + 代码更简单 | keep（简化胜利）|
| 指标不变 + 代码更复杂 | discard |

---

## 反卡顿策略

如果连续 5 次实验都 discard 或 crash：

1. 回顾 results.tsv，找出历史上 discard 的实验
2. 分析：哪些方向还没尝试过？
3. 尝试更激进的变化（而不是继续微调）
4. 若实在卡住，可以回退到某个早期 keep 的 commit，从那里开辟新方向

---

## 适用场景举例

| 实验单元 | 目标指标 | 资源预算 |
|----------|----------|----------|
| prompt 文本 | 评估模型输出质量分数 | 每次 N 个 API 调用 |
| Python 函数 | 测试通过率 + 执行速度 | 30 秒运行时间 |
| 系统配置文件 | 延迟/吞吐量 | 1 分钟压测 |
| LLM 训练代码 | val_bpb | 5 分钟 GPU 时间 |
| RAG 检索策略 | 召回率@K | 固定测试集评估 |

---

## 与 autoresearch 的对应关系

此 skill 是从 [karpathy/autoresearch](https://github.com/karpathy/autoresearch) 项目中提炼的通用模式。
原项目：用 Agent 自动迭代 GPT 训练代码，固定 5 分钟时间预算，最小化 val_bpb。
本 skill：将同样的外层循环结构通用化，适配任意优化任务。
