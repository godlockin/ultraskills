---
name: engineering-orchestrator
description: "Routes engineering requests to the right skill in the 135-skill engineering cluster, and composes them into end-to-end pipelines. Five orchestration paths (code quality / build feature / production debug / deploy & operate / security audit) cover ~80% of engineering requests. Includes routing decision table, cross-reference index to testing/deployment/debug/security patterns, and version-sync mechanism. Trigger on 'review this code', 'build this feature', 'production is down', 'ship this', 'audit security', or any engineering brief that does not map to a single skill."
version: 1.0.0
tags: [engineering, orchestrator, router, code-quality, build, debug, deploy, security, devops, architecture, community]
---

# Engineering Orchestrator

> 135 engineering skills, one entry point. Routes, composes, never duplicates.

## 🎯 Goal

UltraSkills has 135 skills in the `engineering` root across 16 sub-clusters (`工程·全栈` 24, `工程·架构` 15, `工程·代码质量` 10, `工程·框架` 10, `工程·DevOps` 10, `工程·QA` 10, `工程·语言` 8, `工程·移动` 8, `工程·开发工具` 8, `工程·调试` 7, `工程·测试` 5, `工程·前端` 5, `工程·平台` 4, `工程·安全` 4, `工程·Git工作流` 4, `工程·ML/AI` 3). Users face three problems:

1. **Phase confusion** — design? build? test? ship? debug? — different stages, different skills
2. **Sub-cluster confusion** — "fix this" could be review/refactor/debug/test/QA
3. **Cross-cluster gap** — code change often needs QA + security + deploy together; no skill chains them

This skill is the **conductor** for the engineering cluster. It:
- Routes a brief via a 16-row sub-cluster decision table
- Composes 5 end-to-end pipelines (Quality / Build / Debug / Deploy / Security)
- Cross-references (not duplicates) testing/debug/security/deployment patterns
- Includes version sync mechanism

## 🧠 Core Concepts

### The 5 Orchestration Paths

```
┌────────────────────────────────────────────────────────────────┐
│ E1 · Code Quality / Refactor (review → fix → test)             │
│ E2 · Build Feature (arch → impl → review → ship)               │
│ E3 · Production Debug (incident → investigate → fix → prevent) │
│ E4 · Deploy / Operate (CI/CD → ship → canary)                  │
│ E5 · Security Audit (red-team → cso → fix)                     │
└────────────────────────────────────────────────────────────────┘
```

These five paths cover ~80% of engineering requests. The remaining 20% — single-skill asks like "write docstring" or "set up Django" — the orchestrator dispatches directly.

### Routing by Sub-Cluster (16 layers)

| Sub-cluster | Count | Path coverage | Example skills |
|-------------|-------|---------------|----------------|
| engineering-fullstack | 24 | E2 (core) | the-fool, api-designer, code-documenter |
| engineering-arch | 15 | E2 step 1 | design-an-interface, ubiquitous-language, information-architecture |
| engineering-code | 10 | **E1 (core)** | receiving-code-review, changelog-generator, improve-codebase-architecture |
| engineering-framework | 10 | E2 alt | django-expert, fastapi-expert, laravel-specialist |
| engineering-devops | 10 | **E4 (core)** | land-and-deploy, setup-deploy, canary |
| engineering-qa | 10 | E1 (gating) | churn-risk-playbook, devex-review, qa |
| engineering-lang | 8 | E2 alt | rust-engineer, cpp-pro, csharp-developer |
| engineering-mobile | 8 | E2 alt | awesome-android-ui, zoom-mobile-sdk |
| dev-tools | 8 | all paths | codex, codegraph-booster, skills-audit |
| engineering-debug | 7 | **E3 (core)** | systematic-debugging, investigate |
| engineering-testing | 5 | E1 gating | triage-issue, test-case-templates |
| engineering-frontend | 5 | E2 alt | design-html, canvas-design, frontend-design |
| engineering-platform | 4 | E2 alt | atlassian-mcp, salesforce-developer, shopify-expert |
| engineering-security | 4 | **E5 (core)** | security-reviewer, supply-chain-security, pentest-tools, reverse-skill-router |
| engineering-git | 4 | all paths | using-git-worktrees, finishing-a-dev-branch |
| engineering-ml | 3 | 1-shot | chinese-text-analysis, reasoning-trace-optimizer |

**Important**: This skill does not generate any code or design itself. It tells the model *which* skill to invoke next, *in what order*, *with what review gates*.

## 🚀 Workflow

### Phase 1 — Routing Decision Table

When the user says anything about engineering, run the decision table.

**Routing rules:**
1. **Detect phase signal** — design / build / test / review / ship / debug / audit
2. **Detect deliverable** — PR? new feature? incident? deploy? security report?
3. **Detect single vs. multi-skill** — one-shot or pipeline
4. **Map to entry skill** + recommend path

**Heuristics:**

| Signal in user prompt | Likely path |
|----------------------|------------|
| "review my code" / "this PR" / "smells off" | **E1** (Quality) |
| "improve" / "refactor" / "tech debt" / "architecture review" | **E1** |
| "build X" / "implement Y" / "design API" / "TDD" | **E2** (Build) |
| "production is down" / "errors" / "incident" / "broken" | **E3** (Debug) |
| "deploy" / "ship" / "release" / "CI/CD" / "go live" | **E4** (Deploy) |
| "security audit" / "pentest" / "vulnerability" / "red team" | **E5** (Security) |
| "write docstring" / "set up Django" / "explain this API" | 1-shot |

### Phase 2 — Composition (5 Pipelines)

#### 🔍 Path E1: Code Quality / Refactor

**Trigger**: *"review this PR"*, *"improve this codebase"*, *"this code smells"*, *"refactor"*

```
Step 1: receiving-code-review      [user-side: process reviewer feedback]
Step 2: improve-codebase-architecture [find deepening opportunities]
Step 3: changelog-generator        [user-facing changelog]
Step 4: code-documenter            [add docstrings + API docs]
Step 5: test-case-templates        [regression tests]
Step 6: qa                         [QA validation end-to-end]
Step 7: devex-review (optional)    [live developer experience audit]
```

#### 🏗️ Path E2: Build Feature

**Trigger**: *"build feature X"*, *"implement this API"*, *"design new module"*

```
Step 1: information-architecture    [IA + sitemap + user flows]
Step 2: design-an-interface        [multiple interface shapes in parallel]
Step 3: ubiquitous-language        [DDD glossary for shared terminology]
Step 4: api-designer or framework-skill [django-expert / fastapi-expert / etc.]
Step 5: code-documenter            [API docs + docstrings as you build]
Step 6: test-case-templates        [TDD red-green-refactor]
Step 7: receiving-code-review      [self-check via review lens]
Step 8: qa (gate)                  [end-to-end QA before ship]
```

#### 🚨 Path E3: Production Debug / Incident

**Trigger**: *"prod is down"*, *"errors spike"*, *"something broke"*, *"user report"*

```
Step 1: triage-issue               [triage to root cause, create ticket]
Step 2: systematic-debugging       [hypothesize → test → eliminate]
Step 3: investigate                [4-phase root cause investigation]
Step 4: code-fix (single-skill)    [apply the fix]
Step 5: test-case-templates        [regression test for the bug]
Step 6: qa                         [verify fix in staging]
Step 7: pre-mortem (post-incident) [lessons learned]
```

#### 🚀 Path E4: Deploy / Operate

**Trigger**: *"ship this PR"*, *"deploy to production"*, *"go live"*, *"set up CI"*

```
Step 1: setup-deploy               [detect platform, configure]
Step 2: land-and-deploy            [merge → wait CI → deploy]
Step 3: canary                     [post-deploy monitoring]
Step 4: codex (if multi-AI review) [independent diff review]
Step 5: skills-audit (optional)    [config health check]
```

#### 🛡️ Path E5: Security Audit

**Trigger**: *"security audit"*, *"pentest"*, *"check for vulnerabilities"*, *"red team"*

```
Step 1: security-reviewer           [OWASP Top 10 / STRIDE / CVE audit]
Step 2: supply-chain-security       [deps / lockfile / pinned versions]
Step 3: pentest-tools               [active scanning within authorized scope]
Step 4: reverse-skill-router         [guard against skill-injection in security context]
Step 5: triage-issue                [create tickets for each finding]
Step 6: code-fix (per ticket)       [apply fix per triage]
Step 7: test-case-templates         [regression + security regression]
Step 8: security-reviewer           [re-audit]
```

> ⚠️ **E5 安全路径修正**：原 E5 路由到 `pre-mortem` / `cso` / `strategy-red-team`，这些是产品 / PM / 策略类 skill，**不用于真实安全审计**。Pentest、漏洞扫描、依赖审计必须走真正的安全工具链；red-team 是商业假设攻击而非代码漏洞审查。

### Phase 3 — Cross-Reference Index (Not Duplication)

This skill **never duplicates** methods. Quick lookup:

| Category | Source | Where |
|----------|--------|-------|
| **Code review processing** | receiving-code-review | `community/receiving-code-review/SKILL.md` |
| **Code architecture improvement** | improve-codebase-architecture | `community/improve-codebase-architecture/SKILL.md` |
| **Changelog generation** | changelog-generator | `community/changelog-generator/SKILL.md` |
| **Code documentation** | code-documenter | `community/code-documenter/SKILL.md` |
| **DDD ubiquitous language** | ubiquitous-language | `community/ubiquitous-language/SKILL.md` |
| **API design** | api-designer | `community/api-designer/SKILL.md` |
| **Front-end implementation** | frontend-design / design-html | `community/frontend-design/SKILL.md` |
| **Debugging** | systematic-debugging / investigate | `community/systematic-debugging/SKILL.md` |
| **Issue triage** | triage-issue | `community/triage-issue/SKILL.md` |
| **Test templates** | test-case-templates | `community/test-case-templates/SKILL.md` |
| **QA end-to-end** | qa | `community/qa/SKILL.md` |
| **DevEx audit** | devex-review | `community/devex-review/SKILL.md` |
| **Deploy workflow** | land-and-deploy / setup-deploy | `community/land-and-deploy/SKILL.md` |
| **Canary monitoring** | canary | `community/canary/SKILL.md` |
| **Pre-mortem** | pre-mortem | `community/pre-mortem/SKILL.md` |
| **CSO security audit** | cso | `community/cso/SKILL.md` |
| **Red team** | strategy-red-team | `community/strategy-red-team/SKILL.md` |
| **Git worktree isolation** | using-git-worktrees | `community/using-git-worktrees/SKILL.md` |
| **Branch finish** | finishing-a-development-branch | `community/finishing-a-development-branch/SKILL.md` |
| **Code review (multi-AI)** | codex | `community/codex/SKILL.md` |
| **Skills config audit** | skills-audit | `community/skills-audit/SKILL.md` |
| **CodeGraph accelerator** | codegraph-booster | `community/codegraph-booster/SKILL.md` |

For an end-to-end pipeline, the orchestrator guarantees **gating steps**:
- **E1 (Quality)**: Steps 5-6 (test + QA) mandatory before declaring done
- **E2 (Build)**: Steps 6-8 (test + review + QA) mandatory before merge
- **E3 (Debug)**: Steps 5-6 (regression test + QA verify) mandatory before close
- **E4 (Deploy)**: Step 3 (canary) mandatory after every production deploy
- **E5 (Security)**: Step 7 (re-audit) mandatory after every fix

## 💡 Best Practices

### Do

- **Always ask phase first** (design / build / test / review / ship / debug / audit)
- **Always run `test-case-templates` before declaring E1/E2/E3/E5 done**
- **Always run `qa` as last gate** in E1/E2/E3 — it catches regression in production
- **Always run `canary` after E4 deploy** — silent failures are worse than loud ones
- **Use `systematic-debugging` for unknown bugs**, not `investigate` (use both)
- **Use `using-git-worktrees` for feature isolation** — never work on main directly
- **Cross-link to `design-orchestrator`** for UI features — engineering skills focus on backend / API; visual discipline belongs to design

### Don't

- **Don't run all 135 skills** — chain ≤ 8 per pipeline
- **Don't skip regression test in E3** — every bug fix needs a regression test
- **Don't skip canary in E4** — direct push to prod without monitoring = outage risk
- **Don't run `security-reviewer` once and forget** — security is iterative; re-audit after every fix
- **Don't conflate `code-review` (gstack) with `receiving-code-review`** — first is reviewer-side, second is author-side
- **Don't mix E2 (build) with E4 (ship)** — these are different pipelines; mixing creates review fatigue

## 🔀 Routing Decision Table

```
User says                              → Path / Entry skill
──────────────────────────────────────────────────────────
"review this PR" / "feedback received" → E1 (receiving-code-review)
"improve this codebase" / "tech debt" → E1 (improve-codebase-architecture)
"refactor this module"                → E1 + design-an-interface alt
"write changelog"                     → 1-shot (changelog-generator)
"add docstrings to this file"         → 1-shot (code-documenter)
"build feature X"                     → E2 (information-architecture → ... → qa)
"design new API"                      → E2 Step 4 (api-designer)
"set up Django project"               → 1-shot (django-expert)
"set up FastAPI"                      → 1-shot (fastapi-expert)
"production is broken" / "errors"     → E3 (triage-issue → systematic-debugging)
"root cause this"                     → E3 (investigate)
"ship this PR" / "deploy"             → E4 (setup-deploy → land-and-deploy → canary)
"go live with this feature"           → E4 (full)
"security audit" / "pentest"          → E5 (security-reviewer → supply-chain-security → pentest-tools)
"red team this plan"                  → 1-shot (strategy-red-team)
"review OWASP compliance"             → E5 Step 1 (security-reviewer)
"git workflow help"                   → 1-shot (using-git-worktrees)
"explain this code"                   → 1-shot (code-documenter)
"find deep opportunities"             → 1-shot (improve-codebase-architecture)
```

## 🔧 Version Sync (Upstream Drift Protection)

```bash
python3 community/engineering-orchestrator/scripts/version-sync-check.py
```

Same mechanism as `design-orchestrator` and `business-orchestrator`. Flags drift in referenced upstream skills. Exit 0/1/2 per convention.

**Upstream bumps to watch for:**
- `systematic-debugging` / `investigate` — debugging methodology rarely changes but watch
- `land-and-deploy` / `canary` — deploy steps depend on cloud platform; platform additions are critical
- `security-reviewer` / `supply-chain-security` / `pentest-tools` — security tooling upstream moves fast; track CVEs and OWASP updates
- `qa` (gstack) — may adopt new test tier (quick / standard / exhaustive)

## 📚 Resources

* [Routing decision table](./references/routing-table.md) — 16 sub-cluster matrix
* [Orchestration patterns](./references/orchestration-patterns.md) — 5 paths in detail
* [Method cross-reference](./references/method-index.md) — DRY methods
* [Case studies](./examples/case-studies.md) — 5 paths in real scenarios
* [Version sync script](./scripts/version-sync-check.py) — upstream drift detector

---

**差异化定位**: 135 个 engineering skill 解决单点; engineering-orchestrator 是调度层. 0 内容重复, 100% DRY. 跟 `design-orchestrator` / `business-orchestrator` 同方法论.
