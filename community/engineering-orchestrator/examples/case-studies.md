# Engineering Orchestrator — 案例研究 (5 路径实操)

---

## 案例 E1: PR Review — "Process CTO's PR Feedback"

**用户输入**: "I got harsh PR feedback. Process it, fix, and re-submit."

### Orchestrator 决策表

**phase**: review feedback → Path E1
**deliverable**: improved code + tests + QA pass
**entry**: receiving-code-review

### 编排执行

| Step | Skill | 触发原因 | 输出 |
|------|-------|---------|------|
| 1 | receiving-code-review | 处理 12 条反馈 | Sorted by impact |
| 2 | improve-codebase-architecture | 反馈中 4 条是结构性 | Architecture plan |
| 3 | code-documenter | 反馈 3 条"docstring 缺失" | Doc fix |
| 4 | test-case-templates | 反馈 5 条"missing test" | Test suite |
| 5 | qa | Final gate | Health +8 |

### 跳过

- changelog-generator (内部 PR, 不需要)
- devex-review (微调, 非 DX 完整审计)

### 耗时

- Manual: 1-2 天
- Orchestrator: 30-45 分钟
- **compression**: ~15x

---

## 案例 E2: Build Feature — "Multi-tenant SaaS Feature: Tenant Context Middleware"

**用户输入**: "Build tenant context middleware. Support header-based isolation + row-level security."

### Orchestrator 决策表

**phase**: build → Path E2
**deliverable**: working code + tests + review-ready PR
**entry**: information-architecture (or skip if user already specified shape)

### 编排执行

| Step | Skill | 触发原因 | 输出 |
|------|-------|---------|------|
| 1 | (skip — user has shape) | — | — |
| 2 | (skip — backend only) | — | — |
| 3 | ubiquitous-language | Tenant vs Org vs Workspace 术语澄清 | Glossary |
| 4 | api-designer | Tenant context header spec + RLS policy table | OpenAPI snippet |
| 5 | code-documenter | Doc as built | Docstrings |
| 6 | test-case-templates | TDD — tenant isolation matrix | Test suite |
| 7 | receiving-code-review | Self-review | Issues caught |
| 8 | qa | End-to-end | Health score |

### 关键决策

- Step 3 避免术语漂移（Tenant vs Org vs Workspace）
- Step 4 API 决定: header X-Tenant-ID vs JWT claim
- Step 6 测试矩阵: 5 tenant × 6 endpoints = 30 cases
- Step 8 qa: 验证横向越权防御 (cross-tenant leak)

### 耗时

- Manual: 1 周
- Orchestrator: 2.5 小时
- **compression**: ~10-15x

---

## 案例 E3: Production Debug — "Checkout API Returns 500 Randomly"

**用户输入**: "Production checkout throws 500 about 1/200 requests. No clear pattern. Need root cause + fix."

### Orchestrator 决策表

**phase**: production debug → Path E3
**severity**: SEV2 (degraded, not full outage)
**entry**: triage-issue

### 编排执行

| Step | Skill | 触发原因 | 输出 |
|------|-------|---------|------|
| 1 | triage-issue | 确认 5xx rate + 触发条件 | Ticket + repro |
| 2 | systematic-debugging | 假设清单（race / pool / serialization） | Hypothesis tree |
| 3 | investigate | 4-phase deep dive (Phase 3 use logs / APM) | Root cause: race + connection pool |
| 4 | code-fix | 加 mutex + 增加 pool size + connection timeout | Patch |
| 5 | test-case-templates | Concurrency harness regression | Tests |
| 6 | qa | Staging verify, then canary | Health recovered |
| 7 | pre-mortem | Lessons: observability gap + race condition pattern | Post-mortem doc |

### 关键决策

- Step 3 Phase 4 是 APM 上的 lock contention graph
- Step 4 最小 blast radius: 不重构整个 checkout, 只 race 路径
- Step 5 多线程 harness: 10 goroutines × 100 attempts
- Step 7 trigger pre-mortem 一定写, 即使 SEV2

### 耗时

- Manual: 4-8 小时
- Orchestrator: 45-60 分钟
- **compression**: ~10x

---

## 案例 E4: Deploy — "Ship Multi-tenant Middleware to Production"

**用户输入**: "Ship the tenant middleware to prod. AWS / ECS / Fargate."

### Orchestrator 决策表

**phase**: deploy → Path E4
**deliverable**: live + canary verified
**entry**: setup-deploy

### 编排执行

| Step | Skill | 触发原因 | 输出 |
|------|-------|---------|------|
| 1 | setup-deploy | 检测 AWS Fargate, 配置 deploy.yml | Config |
| 2 | land-and-deploy | 合并 PR → CI → Fargate rollout | Live |
| 3 | canary | Watch 5xx / latency / error rate | Health OK |
| 4 | (skip codex — middleware reviewed in E2) | — | — |
| 5 | skills-audit (optional) | 月度 config health | Audit |

### Mandatory Canary

```
⚠️ Step 3 (canary) MANDATORY.
   Watch: 5xx rate, p99 latency, checkout success rate,
   connection pool saturation. Threshold: error rate < 0.1%
   for 30 min before declaring green.
```

### 关键决策

- Step 1 Fargate 的 task definition 需要更新 env (tenant-key rotation)
- Step 3 Canary 关键: "connection pool saturation" 是 SEV3 prior bug, 这次部署后看是否回落

### 反例

| 错误路径 | 为什么错 |
|---------|---------|
| 跳过 step 3 canary | 缺乏 runtime signal, 部署出问题晚发现 |
| 跳过 step 1 setup-deploy | 直接 land-and-deploy 会缺 env / IAM / secrets |
| Insert codex step | 中间件已经在 E2 验过, 重复=review fatigue |

### 耗时

- Manual: 30-60 分钟 (CI 等待)
- Orchestrator: 10-15 分钟 (含 canary 30 min window)
- **compression**: ~3-4x

---

## 案例 E5: Security Audit — "Pre-launch Audit of New SaaS"

**用户输入**: "We're launching next month. Run a full security audit before we go live."

### Orchestrator 决策表

**phase**: security audit → Path E5
**deliverable**: vulnerability list + fix + verified
**entry**: pre-mortem → strategy-red-team → cso

### 编排执行

| Step | Skill | 触发原因 | 输出 |
|------|-------|---------|------|
| 1 | pre-mortem | Launch plan risk analysis | 12 risks categorized |
| 2 | strategy-red-team | Attack load-bearing assumptions | 4 attack vectors |
| 3 | cso | OWASP Top 10 + STRIDE audit | 8 findings |
| 4 | triage-issue | Each finding → ticket | 8 tickets |
| 5 | code-fix (per ticket) | Apply fix | Patches |
| 6 | test-case-templates | Regression + security test | Test suite |
| 7 | qa | Re-audit (cso replay) | All clean |

### ⚠️ Mandatory Re-Audit

```
Step 7 (qa → re-cso) is MANDATORY.
Without re-audit, fixes could introduce new vulns.
```

### 关键决策

- Step 1 + 2 是 plan-stage, Step 3 是 code-stage
- Step 4 优先级排序: OWASP A01 (broken access control) + A03 (injection) first
- Step 5 fix 顺序按风险 register 排序, 不按 ticket 顺序
- Step 7 重新跑完整 cso, 不只 spot-check

### 耗时

- Manual: 2-4 周
- Orchestrator: 4-6 小时
- **compression**: ~10-15x

---

## 5 案例 meta-pattern

1. **Phase first** — design/build/test/review/ship/debug/audit 是 7 种意图
2. **Test/QA gating is mandatory** in E1/E2/E3/E5
3. **Canary mandatory** in E4
4. **Re-audit mandatory** in E5 after fixes
5. **Cross-cluster bridge** for UI features → defer to `design-orchestrator`
6. **Severity routing** in E3 (SEV1/2/3 budget)
