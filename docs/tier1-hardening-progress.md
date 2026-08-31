# Tier-1 Skill 加固进度

> **范围(方案 C)**:Arena score ≥ 9.0 的 30 个 cluster winner
> **每个 skill 的流程**:AB 双轴 review → 修 P0+P1 → 复验 AB review → 不合格再迭代(上限 3 轮)
> **方法论**:见 [ab-review-methodology.md](./ab-review-methodology.md)
> **最后更新**:2026-08-30

## 状态图例

| 标记 | 含义 |
|---|---|
| `✅ DONE` | 修复完成且复验通过 |
| `🔧 FIXED-R1` | 第 1 轮修复完成,**待复验** |
| `🔍 REVIEWING` | AB review 进行中 |
| `⬜ TODO` | 未开始 |
| `⚠️ BLOCKED` | 有阻塞(如 submodule 不可改) |

---

## 进度总览

| 阶段 | 数量 |
|---|---|
| ✅ 复验通过 | 1 |
| 🔧 待复验 | 2 |
| 🔍 review 中 | 5 |
| ⬜ 未开始 | 22 |
| **合计** | **30** |

---

## 明细

### Wave 1

| # | skill | score | 状态 | R1 findings | 关键修复 | commit |
|---|---|---|---|---|---|---|
| 1 | remotion | 9.7 | 🔧 FIXED-R1 | 4 P0 / 7 P1 | wrapper.py 从 10 行 stub 改为可运行 CLI(SKILL.md 原本指示用户运行它);版本锁定 `^4.0`;补 `continueRender` 配对(原先只提 `delayRender`,渲染必挂);字体加载;故障排查 9 类;`TransitionSeries`+`Easing`;2 个 examples(此前 0) | `914503d` |
| 2 | strategy-consulting-framework | 9.5 | 🔧 FIXED-R1 | 2 P0 / 7 P1 | 证据分级门(数据不足强制 Diagnostic 模式,禁输出 `+X%`);重写 example 01(原先虚构基数推量化结论且无标注 = 最强反向示范);新增 example 02(结论为拒绝);反确认偏误(强制反向假设);超时降级;资源默认改「单人零预算」;边界 4→9 类 | 待提交 |
| 3 | magazine-web-ppt | 10.0 | 🔍 REVIEWING | — | — | — |
| 4 | awesome-design-md | 10.0 | 🔍 REVIEWING | — | — | — |
| 5 | comps-analysis | 9.5 | 🔍 REVIEWING | — | 注意:在 `external/`,需先确认是否 submodule | — |
| 6 | business-orchestrator | 9.5 | 🔍 REVIEWING | — | 重点:下游 skill 存在性逐个验证 | — |
| 7 | learn-from-loss | 9.5 | 🔍 REVIEWING | — | 重点:归因安全 | — |

### Wave 2

| # | skill | score | 状态 | 定制考察点 |
|---|---|---|---|---|
| 8 | content-orchestrator | 9.5 | ⬜ TODO | 路由完整性(同 business-orchestrator) |
| 9 | cohort-analysis | 9.5 | ⬜ TODO | 统计正确性、样本量不足时的处理 |
| 10 | generalist-expert | 9.5 | ⬜ TODO | 泛化能力 vs 空洞化;与专项 skill 边界 |
| 11 | deep-concept-analyzer | 9.5 | ⬜ TODO | 概念拆解深度、是否流于术语 |
| 12 | ubiquitous-language | 9.5 | ⬜ TODO | DDD 方法论正确性 |
| 13 | goal-management | 9.5 | ⬜ TODO | 与 PWSB 的编排关系(PWSB 会调用它) |
| 14 | churn-risk-playbook | 9.5 | ⬜ TODO | 预测类结论的证据要求 |
| 15 | engineering-orchestrator | 9.5 | ⬜ TODO | 路由完整性 |

### Wave 3

| # | skill | score | 状态 | 定制考察点 |
|---|---|---|---|---|
| 16 | marketing-roi-calculator | 9.5 | ⬜ TODO | 计算正确性、假设透明度 |
| 17 | ai-techbook-translation | 9.5 | ⬜ TODO | 已有配套 review skill,查两者一致性 |
| 18 | design-orchestrator | 9.5 | ⬜ TODO | 路由完整性 + 与 awesome-design-md 边界 |
| 19 | growth-loops | 9.5 | ⬜ TODO | 增长模型可验证性 |
| 20 | objection-handler | 9.5 | ⬜ TODO | 话术伦理(是否教操纵) |
| 21 | advanced-evaluation | 9.2 | ⬜ TODO | 评估方法论严谨性 |
| 22 | receiving-code-review | 9.2 | ⬜ TODO | 与 two-axis-code-review / review 边界 |
| 23 | agent-docs-writing | 9.0 | ⬜ TODO | 文档标准自洽性 |

### Wave 4

| # | skill | score | 状态 | 定制考察点 |
|---|---|---|---|---|
| 24 | ui-ux-pro-max-skill | 9.0 | ⬜ TODO | 与 design 类 skill 重叠 |
| 25 | chinese-text-analysis | 9.0 | ⬜ TODO | 中文分词/语义准确性 |
| 26 | triage-issue | 9.0 | ⬜ TODO | 分类规则可执行性 |
| 27 | mac-tts | 9.0 | ⬜ TODO | 平台依赖、版本兼容 |
| 28 | gh-fix-ci | 9.0 | ⬜ TODO | 破坏性操作防护(会改 CI) |
| 29 | baoyu-danger-x-to-markdown | 9.5 | ⬜ TODO | 名字含 "danger",查风险声明 |
| 30 | baoyu-article-illustrator | 9.5 | ⬜ TODO | AI 生成图版权风险 |

---

## 已建立的复用工具

| 工具 | 用途 |
|---|---|
| `scripts/check-skill-links.sh` | 检查 skill 内 markdown 本地链接断链(已用故意断链验证有效) |
| `community/personal-ai-work-system-builder/scripts/test_validate_system.sh` | 自包含回归测试范式(1 正例 + 5 攻击例) |
| `docs/ab-review-methodology.md` | AB 双轴 review harness 设计 + 5 类校验绕过 |

---

## 反复出现的问题模式(供后续 review 优先查)

从前 3 个 skill 归纳,这些问题**反复出现**,新 skill 应优先检查:

1. **文档承诺 vs 实际能力脱节** — SKILL.md 指示运行的脚本是占位 stub(remotion)
2. **example 违反 skill 自身规则** — 规则要求标注假设,example 却虚构数据不标(strategy-consulting-framework)
3. **零 examples** — 不符 S-Tier 但 arena 高分(remotion 原本 0 个)
4. **断链** — 引用不存在的文件(strategy-consulting-framework 的 `evals.json`)
5. **无版本锁定** — 依赖快速迭代的外部库却不锁 major(remotion)
6. **无失败处理** — 只有 happy path,无故障排查(remotion)
7. **边界缺失** — 没有「何时不该用」,与同类 skill 无裁定规则
8. **空洞化风险** — 框架类 skill 可能产出"需进一步分析"式废话

---

## 续跑方法

下个会话接手时:

1. 读本文件确认状态
2. 对 `🔧 FIXED-R1` 的 skill 发复验 review(prompt 模板见方法论文档「第二轮必须是复验而非重审」一节)
3. 对 `⬜ TODO` 的 skill 按 Wave 分批发 AB review,专家组按上表「定制考察点」配置
4. 每波完成即 commit,并更新本文件
