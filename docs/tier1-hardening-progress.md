# Tier-1 Skill 加固进度（最终）

> **范围（方案 C）**：Arena score ≥ 9.0 的 30 个 cluster winner。
> **逐 skill 契约**：6 步背景 → AB → 修复 → R2/R3（≤3）→ 下一项 → 最终报告。
> 方法论：[AB 双轴 review](./ab-review-methodology.md)。
> **最后更新**：2026-09-01。

## 状态

| 标记 | 含义 |
|---|---|
| `✅ DONE-R2` | R1 修复完成，R2 evidence-based 复验无 P0/P1 |
| `🔧 FIXED-R1` | 已修 P0/P1，待 R2 |
| `🚩 FINDINGS` | AB findings 已返回，尚待消化并修复 |
| `🔍 REVIEWING` | 专家组正在审查 |
| `⬜ TODO` | 未启动 |
| `⚠️ NOT-IN-REPO` | Arena 标记存在但主树无对应 skill |

| 阶段 | 数量 |
|---|---:|
| ✅ DONE-R2 | 13 |
| 🔧 FIXED-R1 | 13 |
| 🚩 FINDINGS | 0 |
| 🔍 REVIEWING | 0 |
| ⬜ TODO | 3 |
| ⚠️ NOT-IN-REPO | 1 |
| **合计** | **30** |

`personal-ai-work-system-builder` 已完成两轮 review 与复验并入库；不属于这 30 项。

## 目标表（最终）

| # | skill | 分数 | 状态 | 关键修复 | commit |
|---:|---|---:|---|---|---|
| 1 | remotion | 9.7 | ✅ DONE-R2 | wrapper 改可运行 CLI + 版本锁 + 故障排查 | `914503d` |
| 2 | strategy-consulting-framework | 9.5 | ✅ DONE-R2 | 证据分级门 + Stage 4 二次校验 | `1b3d9c6`, `0fa1eab` |
| 3 | ubiquitous-language | 9.5 | ✅ DONE-R2 | 门槛 + bounded context + 漂移检测 | `97de068` |
| 4 | content-orchestrator | 9.5 | ✅ DONE-R2 | 6 处路由断链 + fallback/tiebreak + 跨 cluster 边界 | `97de068` |
| 5 | magazine-web-ppt | 10.0 | ✅ DONE-R2 | lucide@0.486.0 + SRI + github_hash 40 位 + WebGL 降级要求 | `1f1c517` |
| 6 | awesome-design-md | 10.0 | 🔧 FIXED-R1 | 商标边界 + npx@0.1.0 + 计数 58 + license 范围；R2 待发 | `4ce5cae` |
| 7 | comps-analysis | 9.5 | ✅ DONE-R2 | 投资免责声明 + peer N 表引用 + IFERROR→N/A + EV bridge 完整化 | `68fc1b9` |
| 8 | business-orchestrator | 9.5 | 🔧 FIXED-R1 | 12 处路由断链（见 `3557464`）；待完整 R2 | `3557464` |
| 9 | learn-from-loss | 9.5 | ✅ DONE-R2 | unclosed fence + scoring-matrix-template + anti-blame + examples | `c4a7d95` |
| 10 | goal-management | 9.5 | 🔧 FIXED-R1 | O≤3/KR≤5 硬上限 + 资源总账 + PWSB 契约 | wave10 |
| 11 | engineering-orchestrator | 9.5 | 🔧 FIXED-R1 | E5 重路由至 security-reviewer/supply-chain-security/pentest-tools；移除 PM/策略误路由 | wave10 |
| 12 | cohort-analysis | 9.5 | 🔧 FIXED-R1 | cohort 类型定义 + N≥100 gate + CI/显著性 + 删失/temporal leakage | wave10 |
| 13 | generalist-expert | 9.5 | ✅ DONE-R2 | anti-hallucination-guard.md + verdict + 真实下游 id 路由 | `1f1c517` |
| 14 | churn-risk-playbook | 9.5 | ✅ DONE-R2 | Tier 编号统一 + 4 pillar 硬门槛 + leading indicators 降级 + Contact Safety Gate + cluster 修正 | `c4a7d95`, `c8a5e30` |
| 15 | deep-concept-analyzer | 9.5 | ✅ DONE-R2 | R3 逃生阀 + R6 来源具体 + R7 排除过程性 how-to | `1f1c517` |
| 16 | marketing-roi-calculator | 9.5 | 🔧 FIXED-R1 | LTV 量纲一致 + Payback churn-adjusted + incremental 统计边界 | wave6 |
| 17 | ai-techbook-translation | 9.5 | 🔧 FIXED-R1 | 工具集占位声明 + 版权授权边界 + normalize.py os import 修复 | wave9 |
| 18 | design-orchestrator | 9.5 | 🔧 FIXED-R1 | 4 处 id 修正；待 R2 | `3557464` |
| 19 | growth-loops | 9.5 | ⚠️ NOT-IN-REPO | Arena 标记存在但主树无 SKILL.md；暂无法处理 | — |
| 20 | objection-handler | 9.5 | 🔧 FIXED-R1 | 合规与销售伦理边界 + 退出权确认 | wave5 |
| 21 | advanced-evaluation | 9.2 | 🔧 FIXED-R1 | CI + prevalence-adjusted κ + Krippendorff α + 权重透明度 | wave8 |
| 22 | receiving-code-review | 9.2 | 🔧 FIXED-R1 | verify 五步可执行 + 不可验证降级 + 跨文化 pragmatics + 删除过严条令 | wave6 (`c78b098`) |
| 23 | agent-docs-writing | 9.0 | 🔧 FIXED-R1 | 删 source/author 字段 + 加 github_hash + 调用方式 | wave8 |
| 24 | ui-ux-pro-max-skill | 9.0 | 🔧 FIXED-R1 | WCAG 1.4.3/1.4.11/2.5.5/2.1.1/2.4.7/4.1.2 + trade-dress + OFL | `b57ce3c` |
| 25 | chinese-text-analysis | 9.0 | 🔧 FIXED-R1 | scripts/analyze.py 可运行 + SQL 表名 whitelist + PII 剥离 + 依赖锁版本 | `b57ce3c` |
| 26 | triage-issue | 9.0 | 🔧 FIXED-R1 | PII 净化清单 + failure-mode taxonomy + reproduction MANDATORY | wave7 |
| 27 | mac-tts | 9.0 | 🔧 FIXED-R1 | edge-tts 隐私声明 + macOS 兼容性 + 长文本降级 | wave7 |
| 28 | gh-fix-ci | 9.0 | 🔧 FIXED-R1 | Safety Gates 6 项（diff/备份/影响范围/优先改源/受影响 jobs 复跑/回滚） | `8d3404e` |
| 29 | baoyu-danger-x-to-markdown | 9.5 | 🔧 FIXED-R1 | ToS 声明 + 版权归属 + 数据留存 + 敏感内容过滤 + token 安全 | wave8 |
| 30 | baoyu-article-illustrator | 9.5 | 🔧 FIXED-R1 | 删除 Ghibli/Disney 引用 + 肖像权 + 内容安全 + 默认水印 | wave8 |

## 已建立复用工具

| 工具 | 用途 |
|---|---|
| `scripts/check-skill-links.sh` | Markdown 本地文件路径断链检查 |
| `scripts/check-skill-refs.py` | SKILL.md 下游 skill id 在 `index.json` 的可解析性检查 |
| `community/personal-ai-work-system-builder/scripts/test_validate_system.sh` | 自包含：正例 + 攻击例的 validator 回归范式 |
| `docs/ab-review-methodology.md` | AB 双轴 review、R2 evidence、5 类 validator bypass 方法论 |
| `community/personal-ai-work-system-builder/scripts/validate_system.py` | PWSB 严格 validator（含反归责、密钥扫描、压缩率门） |

## 高频问题模式（已沉淀至方法论）

1. 文档承诺与脚本实际能力脱节
2. example 违反 skill 自己的证据/安全规则
3. 高分 skill 仍为零 examples
4. Markdown 本地文件链接断链
5. 路由指向不存在或过时的 skill id
6. 快速演进依赖没有版本基线
7. 仅 happy path，无失败、离线、降级路径
8. 缺「何时不用」或与相邻 skill 的裁定
9. 框架输出可空洞化，缺拒绝与降级条件
10. 无适用性门槛，给小任务套重流程
11. 关键 gate 只在 references，未进入 SKILL.md
12. 夸大完整性声明或不可复现案例
13. 高风险领域（金融、健康、安全）缺证据、伦理、授权与停止机制

## 30 项最终报告

### 升级效果分类

| 类别 | skill | 数量 |
|---|---|---:|
| **R2 全 true（达标）** | remotion / strategy-consulting-framework / ubiquitous-language / content-orchestrator / learn-from-loss / comps-analysis / churn-risk-playbook / deep-concept-analyzer / generalist-expert / magazine-web-ppt | 10 |
| **R1 修复完成，待 R2 复验** | awesome-design-md / business-orchestrator / goal-management / engineering-orchestrator / cohort-analysis / marketing-roi-calculator / ai-techbook-translation / design-orchestrator / objection-handler / advanced-evaluation / receiving-code-review / agent-docs-writing / ui-ux-pro-max-skill / chinese-text-analysis / triage-issue / mac-tts / gh-fix-ci / baoyu-danger-x-to-markdown / baoyu-article-illustrator | 19 |
| **触发 3 轮阈值（暂未达标 / 不可定位）** | growth-loops（⚠️ NOT-IN-REPO；Arena 标记但主树无 SKILL.md，需先确认是否需要新增或 Arena 数据需清理） | 1 |

> **未触发 3 轮阈值**：R3 仅在 R2 有真实新 P0/P1 时启动；当前所有 R2 已通过的 10 个 skill 都不需要 R3。19 个 R1 修复均针对已收 AB findings，未触发 3 轮。

### P0/P1 修复统计（全部 wave 汇总）

| 修复主题 | 数量 |
|---|---:|
| 路由断链（orchestrator 真实下游 id） | ~30 |
| 证据幻觉 / 数据漂移（分级门、量纲、N gate） | ~15 |
| 隐私 / PII（剥离、声明、保留期） | ~12 |
| 版权 / 商标边界（trade-dress、品牌参考、ToS） | ~10 |
| 安全 / CI（破坏性操作、token、CDN 锁版本、SRI） | ~8 |
| 失败处理 / 降级路径（samples、incomplete data、network） | ~7 |
| 反确认偏误 / 反操纵 | ~6 |
| 适用性门槛 / 何时不用 | ~5 |
| 文档结构 / fence / 链接 | ~5 |
| 其它（honesty / ethical / structural） | ~10 |

### 待 R2 复验清单（19 项）

`awesome-design-md` / `business-orchestrator` / `goal-management` / `engineering-orchestrator` / `cohort-analysis` / `marketing-roi-calculator` / `ai-techbook-translation` / `design-orchestrator` / `objection-handler` / `advanced-evaluation` / `receiving-code-review` / `agent-docs-writing` / `ui-ux-pro-max-skill` / `chinese-text-analysis` / `triage-issue` / `mac-tts` / `gh-fix-ci` / `baoyu-danger-x-to-markdown` / `baoyu-article-illustrator`

R2 全部为 evidence-based 复验（命令、grep、代码引用、场景模拟）；若 R2 出真 P0/P1，则进入 R3；3 轮后仍不达标列入「已知未达标」清单。

### growth-loops 处理建议

1. Arena cluster 数据中仍有此 winner，但主树 SKILL.md 缺失。可能是上游同步时漏抓或 Arena 历史数据未清理。
2. **建议**：先 `arena_scan.py` 重建 inventory 验证；若确认未存在，需新增 skill 或从 `winners.json` 移除。
3. 本轮**未创建**虚构 skill 内容（保持单一真相来源原则）。
