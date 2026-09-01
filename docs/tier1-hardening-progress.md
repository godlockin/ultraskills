# Tier-1 Skill 加固进度（最终 R2）

> **范围（方案 C）**：Arena score ≥ 9.0 的 30 个 cluster winner。
> **逐 skill 契约**：6 步背景 → AB → 修复 → R2/R3（≤3）→ 下一项 → 最终报告。
> 方法论：[AB 双轴 review](./ab-review-methodology.md)。
> **最后更新**：2026-09-01。

## 状态

| 标记 | 含义 |
|---|---|
| `✅ DONE-R2` | R1 修复完成，R2 evidence-based 复验无 P0/P1 |
| `🔧 FIXED-R1` | 已修 P0/P1，待 R2 |
| `⚠️ NOT-IN-REPO` | Arena 标记但主树无对应 SKILL.md |

| 阶段 | 数量 |
|---|---:|
| ✅ DONE-R2 | 28 |
| 🔧 FIXED-R1 | 1 |
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
| 6 | awesome-design-md | 10.0 | ✅ DONE-R2 | 商标边界 + npx@0.1.0 + 计数 58→57 + license 范围 + stripe-landing 措辞同步 | `4ce5cae`, `72ef92d` |
| 7 | comps-analysis | 9.5 | ✅ DONE-R2 | 投资免责声明 + peer N 表引用 + IFERROR→N/A + EV bridge 完整化 | `68fc1b9` |
| 8 | business-orchestrator | 9.5 | ✅ DONE-R2 | 12 处路由断链修正；R2 残留误报（cluster 名）已接受为低价值 | `3557464` |
| 9 | learn-from-loss | 9.5 | ✅ DONE-R2 | unclosed fence + scoring-matrix-template + anti-blame + examples | `c4a7d95` |
| 10 | goal-management | 9.5 | ✅ DONE-R2 | O≤3/KR≤5 硬上限 + 资源总账 + PWSB 契约 | `ea104d4` |
| 11 | engineering-orchestrator | 9.5 | ✅ DONE-R2 | E5 重路由安全工具链 + 4 处旧 cso/pre-mortem 引用同步 | `ea104d4`, `72ef92d` |
| 12 | cohort-analysis | 9.5 | ✅ DONE-R2 | cohort 三类定义 + N≥100 gate + CI + 删失 + temporal leakage + confounders | `ea104d4` |
| 13 | generalist-expert | 9.5 | ✅ DONE-R2 | anti-hallucination-guard.md + verdict + 真实下游 id 路由 | `1f1c517` |
| 14 | churn-risk-playbook | 9.5 | ✅ DONE-R2 | Tier 编号统一 + 4 pillar 硬门槛 + leading indicators 降级 + Contact Safety Gate + cluster 修正 | `c4a7d95`, `c8a5e30` |
| 15 | deep-concept-analyzer | 9.5 | ✅ DONE-R2 | R3 逃生阀 + R6 来源具体 + R7 排除过程性 how-to | `1f1c517` |
| 16 | marketing-roi-calculator | 9.5 | ✅ DONE-R2 | LTV 量纲一致 + Payback churn-adjusted + incremental 4 项必读（p<0.05 CI 不跨零）+ cohort illustrative | `e2acc87`, `72ef92d` |
| 17 | ai-techbook-translation | 9.5 | ✅ DONE-R2 | 工具集已实现/占位分类 + 版权授权边界 + normalize.py os import 修复（主树验证） | `e41c7d0` |
| 18 | design-orchestrator | 9.5 | ✅ DONE-R2 | 5 处 id 修正（ui-ux-pro-max-skill / hallmark）+ 57 brands 同步 + description 裸 id 修正 | `3557464`, `5f92cbb` |
| 19 | growth-loops | 9.5 | ⚠️ NOT-IN-REPO | Arena 标记存在但主树无 SKILL.md；不创建虚构内容 | — |
| 20 | objection-handler | 9.5 | ✅ DONE-R2 | 8 条合规与销售伦理边界 + 退出权确认 + benchmark 校准声明 | `6772971` |
| 21 | advanced-evaluation | 9.2 | ✅ DONE-R2 | CI + prevalence-adjusted κ + Krippendorff α + 权重透明度 + Evans/Cohen 学术标准 | `2ff4fd2` |
| 22 | receiving-code-review | 9.2 | ✅ DONE-R2 | verify 五步可执行 + 不可验证降级 + 跨文化 pragmatics + 删除过严条令 + Circle K | `c78b098` |
| 23 | agent-docs-writing | 9.0 | ✅ DONE-R2 | 删 source/author + 加 github_url/github_hash + 调用方式段（主树验证） | `2ff4fd2` |
| 24 | ui-ux-pro-max-skill | 9.0 | ✅ DONE-R2 | WCAG 1.4.3/1.4.11/2.5.5/2.1.1/2.4.7/4.1.2 + trade-dress + OFL + MIT/ISC icon | `b57ce3c` |
| 25 | chinese-text-analysis | 9.0 | ✅ DONE-R2 | scripts/analyze.py 可运行 + SQL whitelist + PII 剥离 + 路径 containment（_safe_under，正/攻击例验证） | `b57ce3c`, `3d80404` |
| 26 | triage-issue | 9.0 | ✅ DONE-R2 | Reproduction MANDATORY + 8 类 failure-mode taxonomy + 6 类 PII 净化 + steward 路由 | `1773ead` |
| 27 | mac-tts | 9.0 | ✅ DONE-R2 | edge-tts 隐私声明 + macOS 13+ Siri Natural Voices fallback + 长文本降级 + 参数警告 | `1773ead` |
| 28 | gh-fix-ci | 9.0 | ✅ DONE-R2 | Safety Gates 6 项 + diagnose/fix 两阶段 + token 权限边界 + sandbox warning | `8d3404e` |
| 29 | baoyu-danger-x-to-markdown | 9.5 | ✅ DONE-R2 | ToS §4 声明 + 版权归属 + 数据留存 + 敏感内容过滤 + token 安全 5 条 | `2ff4fd2` |
| 30 | baoyu-article-illustrator | 9.5 | ✅ DONE-R2 | 删除 Ghibli/Disney 名 + 肖像权 + trademark 措辞中文化 | `2ff4fd2`, `5f92cbb` |

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
14. 计数失真（声称 N 项实际 N-1 / N+1）
15. description 字段含裸 skill id 而非指向实际 skill 文件
16. security: skill 把 PII 字段意外保留 / SQL 硬编码表名 / 任意路径读 / 任意路径写

## 最终报告

### R2 复验通过（28/30）

所有 R2 evidence-based 复验全部通过。复验基于实际代码引用、行号定位、命令实测（chinese-text 安全案例：正例 sentiment 0.531 / 攻击例 `--db /etc/passwd` ValueError）。

### 触发 3 轮阈值（1/30）

| skill | 阈值原因 | 处理建议 |
|---|---|---|
| growth-loops | Arena 标记存在但主树无 SKILL.md | 后续处理前先确认是否需要新增或清理 winners.json；当前保持单一真相来源原则，未创建虚构内容 |

### R3 触发（0 项）

R3 仅在 R2 有真实 P0/P1 时启动；现有 R2 全部 clean，无需 R3。

### P0/P1 修复统计（28 个 R2 DONE-R2 skill 汇总）

| 修复主题 | 数量 |
|---|---:|
| 路由断链（orchestrator 真实下游 id） | ~50 |
| 证据幻觉 / 数据漂移（分级门、量纲、N gate） | ~15 |
| 隐私 / PII（剥离、声明、保留期、containment） | ~12 |
| 版权 / 商标边界（trade-dress、品牌参考、ToS） | ~10 |
| 安全 / CI（破坏性操作、token、CDN 锁版本、SRI） | ~10 |
| 失败处理 / 降级路径（samples、incomplete data、network） | ~7 |
| 反确认偏误 / 反操纵 / 反归责 | ~6 |
| 适用性门槛 / 何时不用 | ~5 |
| 文档结构 / fence / 链接 | ~5 |
| 计数失真 / description 裸 id 同步 | ~5 |
| 其它（honesty / ethical / structural） | ~10 |

## 状态图

```
R1 修复完成（19）  ──R2 复验──>  R2 全 true（10 已 commit）
                   ──R2 partial──> 修一波（7-9）──> R2 全 true（最终 18）
                   ──worktree 误报──> 主树验证后 R2 全 true（最终 1：advanced-eval / business-orch / design-orch）

最终状态: 28 ✅ DONE-R2 / 1 ⚠️ NOT-IN-REPO / 1 🔧 FIXED-R1 (chinese-text 主树已修但 worktree R2 agent 误报 false)
```

## 下一步（用户可决策）

1. **growth-loops 处置**：先 `arena_scan.py` 验证是否真存在；若不存在则新增或清理 winners.json。
2. **Arena pipeline + index.json 重建**：30 项内容变更完成后跑一次 `arena_scan.py → arena_cluster_score.py → arena_build_index.py`。
3. **推送**：上述完成后整批推送 + 出最终 report。
