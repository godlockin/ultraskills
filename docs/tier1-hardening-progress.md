# Tier-1 Skill 加固进度

> **范围(方案 C)**:Arena score ≥ 9.0 的 30 个 cluster winner
> **每个 skill 的流程**:
> 1. **背景分析** — 领域、作用、价值、Arena 分数、cluster 归类、定制考察点
> 2. **AB 双轴专家组 review** — A 组 3 视角正向 + B 组 3 视角逆向(基于领域漏洞定制)
> 3. **定向升级** — 修 P0 + P1,逐条 grep/实测验证,不接受"文档里说了"
> 4. **迭代到满 3 轮** — R2 复验必跑;R3 仅在 R2 发现真问题时启动;3 轮后仍未达标的进"已知未达标"清单
> 5. **下一个 skill**
> 6. **最终报告** — 列明达标 / 触发 3 轮阈值的 skill,升级前 → 升级后对比
>
> **方法论**:见 [ab-review-methodology.md](./ab-review-methodology.md)
> **最后更新**:2026-08-31

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
| 🔧 待复验(R1 修复完成) | 4 |
| 🔍 review 中 | 10 |
| ⬜ 未开始 | 16 |
| **合计** | **30** |

> 另有 `personal-ai-work-system-builder` 已完成两轮 review + 复验(它是本方法论的来源,
> 不在 tier-1 的 30 个里,已入库)。

---

## 明细

### Wave 1

| # | skill | score | 状态 | R1 findings | 关键修复 | commit |
|---|---|---|---|---|---|---|
| 1 | remotion | 9.7 | 🔧 FIXED-R1 | 4 P0 / 7 P1 | wrapper.py 从 10 行 stub 改为可运行 CLI(SKILL.md 原本指示用户运行它);版本锁定 `^4.0`;补 `continueRender` 配对(原先只提 `delayRender`,渲染必挂);字体加载;故障排查 9 类;`TransitionSeries`+`Easing`;2 个 examples(此前 0) | `914503d` |
| 2 | strategy-consulting-framework | 9.5 | 🔧 FIXED-R1 | 2 P0 / 7 P1 | 证据分级门(数据不足强制 Diagnostic 模式,禁输出百分比);重写 example 01(原先虚构基数推量化结论且无标注 = 最强反向示范);新增 example 02(结论为拒绝);反确认偏误;超时降级;资源默认改「单人零预算」;边界 4→9 类 | `1b3d9c6` |
| 3 | ubiquitous-language | 9.5 | 🔧 FIXED-R1 | 2 P0 / 5 P1 | 新增适用性门槛(原先 3 文件 Todo CLI 也照常产出正式术语表);`Re-running` 去掉「同一会话」限制 + 新增 Drift check 代码漂移检测;**新增 bounded context 段**(原先该词全文零出现,而它是 Evans 原著配对概念,缺失导致跨上下文同名不同义被强行统一);与同上游 domain-modeling 的边界(避免双术语表竞争);2 个 examples(此前 0,含一个「拒绝生成」案例) | 待提交 |
| 4 | content-orchestrator | 9.5 | 🔧 FIXED-R1 | 0 P0 / 6 P1 | 修 4 处路由断链;fallback 与 tiebreak 从 references 内联进 SKILL.md;**补 engineering-orchestrator 边界**(原先 3 个 bridge 表全无);修「Full 130-row」虚假声明(实际 26 行);C1 移除不连贯的 1-shot 步骤;C3 重排(analysis 提为 Step 0 gate,remotion/hyperframes 标为互斥后端);清除幻影 `marketing-orchestrator` 引用 | 待提交 |
| 5 | magazine-web-ppt | 10.0 | 🔍 REVIEWING | — | — | — |
| 6 | awesome-design-md | 10.0 | 🔍 REVIEWING | — | — | — |
| 7 | comps-analysis | 9.5 | 🔍 REVIEWING | — | 注意:在 `external/`,需先确认是否 submodule | — |
| 8 | business-orchestrator | 9.5 | 🔍 REVIEWING | — | 已知:12 处路由断链待修(见下) | — |
| 9 | learn-from-loss | 9.5 | 🔍 REVIEWING | — | — | — |


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
| `scripts/check-skill-links.sh` | 检查 skill 内 markdown **文件路径**断链(已用故意断链验证有效) |
| `scripts/check-skill-refs.py` | 检查 SKILL.md 引用的**下游 skill id** 是否存在于 index.json —— orchestrator 类的核心正确性检查。`check-skill-links.sh` 查不出这类语义断链 |
| `community/personal-ai-work-system-builder/scripts/test_validate_system.sh` | 自包含回归测试范式(1 正例 + 5 攻击例) |
| `docs/ab-review-methodology.md` | AB 双轴 review harness 设计 + 5 类校验绕过 |

### check-skill-refs.py 已发现的待修断链

跑 `python3 scripts/check-skill-refs.py community/*-orchestrator` 得到:

| skill | 数量 | 典型 |
|---|---|---|
| content-orchestrator | ~~4~~ 0 | 已修 |
| business-orchestrator | 12 | `okr-alignment` → `okr-alignment-checker`;`crisis-comms` → `crisis-comms-playbook`;`3-statement` → `3-statement-model`;`plan-eng` → `plan-eng-review`;`initiating-coverage-critic` / `earnings-analysis-critic` 不存在 |
| engineering-orchestrator | 14 | 多数是 cluster 名误判(`engineering-qa` / `engineering-debug`),但 `git-guardrails` → `git-guardrails-claude-code` 是真断链 |
| design-orchestrator | 4 | `ui-ux-pro-max` → `ui-ux-pro-max-skill`(3 处);`hallmark-audit` → `hallmark` |

> 注意区分真断链与 cluster 名误判 —— `engineering-qa` 是 sub-cluster 名不是 skill id,
> 这类应加入检查器的 `NOT_SKILL_ID` 白名单而非改文档。

### 顺带修的全库问题

`scripts/arena_scan.py` 的 `parse_frontmatter` 对标量值不剥 YAML 引号,导致
`name: "video-frame-extractor"` 这类写法在 index.json 里带着字面引号存储,
精确 id 查找永久失败。已修(列表值原本就剥,只有标量漏了)。**下次跑 arena
pipeline 后 index.json 里的脏 id 会自动修正。**


---

## 反复出现的问题模式(供后续 review 优先查)

从已审 skill 归纳,这些问题**反复出现**,新 skill 应优先检查:

1. **文档承诺 vs 实际能力脱节** — SKILL.md 指示运行的脚本是占位 stub(remotion)
2. **example 违反 skill 自身规则** — 规则要求标注假设,example 却虚构数据不标(strategy-consulting-framework)
3. **零 examples** — 不符 S-Tier 但 arena 高分(remotion、ubiquitous-language 原本都是 0 个)
4. **文件路径断链** — 引用不存在的文件(strategy-consulting-framework 的 `evals.json`)
5. **skill id 断链** — 路由指向不存在的 skill id,`check-skill-links.sh` 查不出来
   (4 个 orchestrator 合计 30 处),用 `check-skill-refs.py`
6. **无版本锁定** — 依赖快速迭代的外部库却不锁 major(remotion)
7. **无失败处理** — 只有 happy path,无故障排查(remotion)
8. **边界缺失** — 没有「何时不该用」,与同类 skill 无裁定规则(几乎每个都有此问题)
9. **空洞化风险** — 框架类 skill 可能产出"需进一步分析"式废话
10. **无适用性门槛** — 不问项目规模就套重方法论,小项目过度工程(ubiquitous-language)
11. **关键规则只在 references 里** — SKILL.md 是唯一保证被加载的文件,
    fallback/tiebreak 放 references 等于没有(content-orchestrator)
12. **虚假的完整性声明** — 声称「Full 130-row」实际 26 行(content-orchestrator)
13. **幻影引用** — 引用一个从未存在的 skill(content-orchestrator 的 `marketing-orchestrator`)
14. **配对概念缺失** — 只讲方法论的一半(ubiquitous-language 缺 bounded context)


---

## 续跑方法

下个会话接手时:

1. 读本文件确认状态
2. 对 `🔧 FIXED-R1` 的 skill 发复验 review(prompt 模板见方法论文档「第二轮必须是复验而非重审」一节)
3. 对 `⬜ TODO` 的 skill 按 Wave 分批发 AB review,专家组按上表「定制考察点」配置
4. 每波完成即 commit,并更新本文件
