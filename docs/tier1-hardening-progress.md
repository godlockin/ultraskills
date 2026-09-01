# Tier-1 Skill 加固进度

> **范围（方案 C）**：Arena score ≥ 9.0 的 30 个 cluster winner。
>
> **逐 skill 契约**：
> 1. 分析背景、作用、价值、purpose 与领域风险；
> 2. 按领域召集 A 组正向／B 组逆向的多元专家；
> 3. 依据 findings 修 P0/P1，并给可运行或可检查证据；
> 4. R2 复验；有真实 P0/P1 才进 R3；第 3 轮后仍不达标明确记录；
> 5. 再进入下一 skill；
> 6. 最终报告列升级前后、满意项、P2 残留、触发三轮阈值项。
>
> 方法论：[AB 双轴 review](./ab-review-methodology.md)。最后更新：2026-08-31。

## 状态

| 标记 | 含义 |
|---|---|
| `✅ DONE-R2` | R1 修复完成，R2 证据复验无 P0/P1 |
| `🔧 FIXED-R1` | 已修 P0/P1，待 R2 |
| `🚩 FINDINGS` | AB findings 已返回，尚待消化并修复 |
| `🔍 REVIEWING` | 专家组正在审查 |
| `⬜ TODO` | 未启动 |
| `⚠️ BLOCKED` | 有明确外部阻塞 |

| 阶段 | 数量 |
|---|---:|
| ✅ DONE-R2 | 5 |
| 🔧 FIXED-R1 | 6 |
| 🚩 FINDINGS | 4 |
| 🔍 REVIEWING | 4 |
| ⬜ TODO | 11 |
| **合计** | **30** |

`personal-ai-work-system-builder` 已完成两轮 review 与复验并入库；不属于这 30 项。

## 目标表

| # | skill | 分数 | 状态 | 背景／purpose | 定制专家组与关键审查点 | 已知结果／下一步 |
|---:|---|---:|---|---|---|---|
| 1 | remotion | 9.7 | ✅ DONE-R2 | React 视频渲染 | 视频工程、Node/渲染可靠性、版权边界；版本／异步渲染／OOM | 4 P0/7 P1 已修；R2 仅 P2 examples 残留 |
| 2 | strategy-consulting-framework | 9.5 | ✅ DONE-R2 | 战略决策框架 | 策略顾问、统计证据、反确认偏误；数据幻觉 | 2 P0/7 P1 已修；R2 evidence gate 追加修复 |
| 3 | ubiquitous-language | 9.5 | ✅ DONE-R2 | DDD 术语治理 | DDD、领域建模、维护性；bounded context／漂移 | 2 P0/5 P1 已修；R2 仅自动 drift P2 |
| 4 | content-orchestrator | 9.5 | ✅ DONE-R2 | 内容生产编排 | 内容策略、路由正确性、平台合规；下游 id／fallback | 6 P1 已修；R2 仅 P2 |
| 5 | magazine-web-ppt | 10.0 | 🔧 FIXED-R1 | 网页化演示稿 | 前端、设计系统、供应链；CDN pin／真实案例 | 已锁 lucide@0.486.0 + SRI；github_hash 改 40 位；待 R2 |
| 6 | awesome-design-md | 10.0 | 🔧 FIXED-R1 | 品牌设计参考 | 品牌／版权、设计系统、工具链；清单真实性／trade dress | 商标边界 + npx@0.1.0 锁版 + 计数 58 + license 范围限定；待 R2 |
| 7 | comps-analysis | 9.5 | 🔧 FIXED-R1 | 可比公司估值 | 投资分析、统计、开源合规；免责声明／N gate／EV bridge | 投资免责声明 + peer N 表引用 + Valid N 门槛 + IFERROR→N/A + EV bridge 完整化 + 删失效 example 引用；待 R2 |
| 8 | business-orchestrator | 9.5 | 🔧 FIXED-R1 | 商业任务路由 | 业务架构、路由、审计；真实下游 id／tiebreak | 已修已知 id；待完整 R2 |
| 9 | learn-from-loss | 9.5 | ✅ DONE-R2 | 赛后复盘与经验沉淀 | 组织心理、复盘、伦理；anti-blame／绩效滥用 | 4 P1 已修；R2 全 true：fence、broken link、anti-blame、examples |
| 10 | goal-management | 9.5 | 🚩 FINDINGS | 目标与 KR 管理 | OKR、资源规划、PWSB 编排；总账／容量约束 | 加硬上限、冲突裁定、输入输出契约 |
| 11 | engineering-orchestrator | 9.5 | 🔧 FIXED-R1 | 工程任务路由 | 软件架构、安全、路由；安全请求正确下游 | 已修一处 id；必须重做 E5 安全路由并 R2 |
| 12 | cohort-analysis | 9.5 | 🚩 FINDINGS | 留存 cohort 数据分析 | 统计、产品分析、数据质量；样本量／CI／删失 | 加 N gate、显著性、缺失降级、案例 |
| 13 | generalist-expert | 9.5 | 🔧 FIXED-R1 | 通用专家组模板 | 专家系统、路由、可复现性；verdict／handoff | 补 anti-hallucination-guard.md + 输出 verdict + handoff 真实 id；待 R2 |
| 14 | churn-risk-playbook | 9.5 | 🔧 FIXED-R1 | 客户流失风险干预 | 客户成功、预测科学、隐私伦理；评分证据／停止规则 | Tier 编号统一；4 pillar 硬门槛；leading indicators 降级；Contact Safety Gate；Arena cluster 修正（新增 customer-success-retention）；待 R2 |
| 15 | deep-concept-analyzer | 9.5 | 🔧 FIXED-R1 | 深层概念拆解 | 教育学、知识论、引用审计；来源／适用边界 | R3 加逃生阀 + R6 来源具体可追溯 + R7 排除过程性 how-to；待 R2 |
| 16 | marketing-roi-calculator | 9.5 | ⬜ TODO | 营销 ROI 计算 | 增长、财务建模、统计；计算正确性／假设透明 | 待 AB review |
| 17 | ai-techbook-translation | 9.5 | ⬜ TODO | 技术书翻译 | 翻译、术语、QA；配套 review 一致性 | 待 AB review |
| 18 | design-orchestrator | 9.5 | 🔧 FIXED-R1 | 设计任务路由 | 产品设计、路由、版权；真实 id／边界 | 已修 4 处 id；待 R2 |
| 19 | growth-loops | 9.5 | ⬜ TODO | 增长循环设计 | 增长、实验设计、因果推断；可验证性 | 待 AB review |
| 20 | objection-handler | 9.5 | ⬜ TODO | 异议处理话术 | 销售伦理、沟通、合规；反操纵 | 待 AB review |
| 21 | advanced-evaluation | 9.2 | ⬜ TODO | 高级评估框架 | 测量学、统计、审计；评价严谨性 | 待 AB review |
| 22 | receiving-code-review | 9.2 | ⬜ TODO | 接收 code review | 软件工程、审查、协作；验证而非盲从 | 待 AB review |
| 23 | agent-docs-writing | 9.0 | ⬜ TODO | agent 文档写作 | 技术写作、DX、信息架构；标准自洽 | 待 AB review |
| 24 | ui-ux-pro-max-skill | 9.0 | ⬜ TODO | UI/UX 设计建议 | 设计系统、无障碍、版权；与设计 skill 边界 | 待 AB review |
| 25 | chinese-text-analysis | 9.0 | ⬜ TODO | 中文文本分析 | 中文 NLP、语言学、评估；分词／语义 | 待 AB review |
| 26 | triage-issue | 9.0 | ⬜ TODO | issue 分诊 | 工程管理、支持运营、可复现性；规则可执行 | 待 AB review |
| 27 | mac-tts | 9.0 | ⬜ TODO | macOS TTS | macOS、音频、隐私；版本／平台降级 | 待 AB review |
| 28 | gh-fix-ci | 9.0 | ⬜ TODO | GitHub CI 故障修复 | CI、安全、变更管理；破坏性操作防护 | 待 AB review |
| 29 | baoyu-danger-x-to-markdown | 9.5 | ⬜ TODO | X 内容转 Markdown | 内容归档、平台合规、安全；风险声明 | 待 AB review |
| 30 | baoyu-article-illustrator | 9.5 | ⬜ TODO | 文章配图生成 | 版权、视觉设计、内容安全；生成图权利 | 待 AB review |

## 已建立复用工具

| 工具 | 用途 |
|---|---|
| `scripts/check-skill-links.sh` | Markdown 本地文件路径断链检查（已用故意断链验证） |
| `scripts/check-skill-refs.py` | SKILL.md 下游 skill id 在 `index.json` 的可解析性检查 |
| `community/personal-ai-work-system-builder/scripts/test_validate_system.sh` | 自包含：正例 + 攻击例的 validator 回归范式 |
| `docs/ab-review-methodology.md` | AB 双轴 review、R2 evidence、validator bypass 方法论 |

## 高频问题模式

1. 文档承诺与脚本实际能力脱节。
2. example 违反 skill 自己的证据／安全规则。
3. 高分 skill 仍为零 examples。
4. Markdown 本地文件链接断链。
5. 路由指向不存在或过时的 skill id。
6. 快速演进依赖没有版本基线。
7. 仅 happy path，无失败、离线、降级路径。
8. 缺「何时不用」或与相邻 skill 的裁定。
9. 框架输出可空洞化，缺拒绝与降级条件。
10. 无适用性门槛，给小任务套重流程。
11. 关键 gate 只在 references，未进入 `SKILL.md`。
12. 夸大完整性声明或不可复现案例。
13. 高风险领域缺证据、伦理、授权与停止机制。

## 续跑

1. 先消化 `🔍 REVIEWING` 与 `🚩 FINDINGS`，逐项完成 R1 修复；
2. 每项跑本地链接／引用及领域验证；
3. 发 R2 证据复验，必要时 R3；
4. 每波独立提交，避免混入用户原有 bazi/face/palm 与 `external/reverse-skill` 改动；
5. 30 项完成后才全量 Arena pipeline、更新 index、提交推送、出总报告。
