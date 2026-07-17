# Orchestration Patterns (5 End-to-End Engineering Pipelines)

---

## 🔍 Pattern E1: Code Quality / Refactor

### When

- User has PR feedback / tech debt / smells
- Output target: improved codebase + changelog + regression tests
- Phase: mid-development or pre-merge

### Steps

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | receiving-code-review | Process reviewer feedback | Action plan |
| 2 | improve-codebase-architecture | Find deepening opportunities | Architecture plan |
| 3 | changelog-generator | User-facing changelog | CHANGELOG.md |
| 4 | code-documenter | Add docstrings + API docs | Inline docs |
| 5 | test-case-templates | Regression tests | Test suite |
| 6 | qa | End-to-end QA | Health score |
| 7 | devex-review | Live developer experience | DX audit |

### Adapted Variants

- **Pure refactor (no PR feedback yet)**: Steps 2, 4, 5, 6 only
- **Add docstrings only**: Step 4 only
- **Add changelog only**: Step 3 only
- **Cross-repo audit**: Step 2 + `skills-audit` to detect config drift

### Timing

- Manual: 1-2 days per PR
- Orchestrator: 30-45 minutes
- **compression**: ~15x

---

## 🏗️ Pattern E2: Build Feature (Greenfield or Add)

### When

- User wants to build new feature / module / API
- Output target: working code + tests + review-ready
- Phase: design → implementation → pre-merge

### Steps

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | information-architecture | IA + sitemap + user flows | IA doc |
| 2 | design-an-interface | Multiple interface shapes parallel | Variants |
| 3 | ubiquitous-language | DDD glossary | Glossary |
| 4 | api-designer or framework skill | API design | OpenAPI / spec |
| 5 | code-documenter | Document as you build | Inline + API docs |
| 6 | test-case-templates | TDD test suite | Red-green-refactor |
| 7 | receiving-code-review | Self-review | Issues caught |
| 8 | qa | End-to-end QA gate | Health score |

### Adapted Variants

- **Module without UI**: Skip step 2 (no design)
- **Backend only**: Step 4 → api-designer only; skip step 1
- **Frontend only**: Step 4 → frontend-design; skip ubiquitous-language if no DDD context
- **Library / SDK**: Step 4 = single-skill (python/library-expert)
- **Mobile**: Insert awesome-android-ui or zoom-sdk as framework step

### Cross-Cluster Bridge

For frontend-heavy features, **defer to `design-orchestrator`** before final implementation. Engineering skills focus on backend / API / business logic — visual discipline lives with design.

### Timing

- Manual: 1-2 weeks
- Orchestrator: 1.5-3 hours
- **compression**: ~10-15x

---

## 🚨 Pattern E3: Production Debug / Incident

### When

- Production is down, errors spiking, user reports a bug
- Output target: root cause + fix + regression test
- Phase: incident response / post-incident

### Steps

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | triage-issue | Reproduce + classify + ticket | Issue file |
| 2 | systematic-debugging | Hypothesize → test → eliminate | Hypothesis tree |
| 3 | investigate | 4-phase root cause investigation | Root cause |
| 4 | code-fix | Apply minimal-blast-radius fix | Patch |
| 5 | test-case-templates | Regression test for the bug | Test case |
| 6 | qa | Verify fix in staging | Health score |
| 7 | pre-mortem (post-incident) | Lessons learned | Post-mortem |

### Severity Routing

| Severity | Steps | Time budget |
|----------|-------|-------------|
| **SEV1** (prod down) | 1 → 2 → 3 → 4 → 5 → 6 → rollback | < 30 min |
| **SEV2** (degraded) | 1 → 2 → 3 → 4 → 5 → 6 | 1-2 hours |
| **SEV3** (user-reported minor) | 1 → 2 → 4 → 5 → 6 | 4-8 hours |
| **Post-incident** | All 7 (add pre-mortem) | +1 day |

### Adapted Variants

- **Unknown bug (no clear symptom)**: Steps 1, 2, 3 only
- **Known regression**: Steps 4, 5, 6 only
- **Multi-service cascade**: Insert `investigate` Phase 4 explicitly

### Timing

- Manual: 4-8 hours for SEV2/SEV3
- Orchestrator: 30-60 minutes
- **compression**: ~10x

---

## 🚀 Pattern E4: Deploy / Operate

### When

- User wants to ship to production
- Output target: deployed + monitored + healthy
- Phase: post-merge / go-live / release

### Steps

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | setup-deploy | Detect platform + configure | Deploy config |
| 2 | land-and-deploy | Merge → wait CI → deploy | Live deploy |
| 3 | canary | Post-deploy monitoring | Health signals |
| 4 | codex (optional) | Multi-AI diff review | Independent review |
| 5 | skills-audit (optional) | Config health check | Audit report |

### Adapted Variants

- **First-time deploy**: Steps 1 → 2 → 3
- **Repeat deploy (same env)**: Step 2 → 3
- **Multi-AI safety check**: Insert Step 4 between 2 and 3
- **Rollback (post-canary fail)**: canary triggers; route to E3 (debug)

### Mandatory Canary

```
⚠️ Step 3 (canary) is MANDATORY after any production deploy.
   Skipping canary = silent failures waiting to happen.
   Canary watches for: console errors, latency spikes, error rates,
   conversion dropoff, infrastructure alerts.
```

### Cross-Cluster Bridge

For first-time prod, defer to `business-orchestrator` Path B4 (compliance-check, audit-support, draft-response to user).

### Timing

- Manual: 30 min - 2 hours (depending on CI)
- Orchestrator: 10-20 minutes
- **compression**: ~5x

---

## 🛡️ Pattern E5: Security Audit

### When

- Pre-launch / periodic / post-incident / regulatory
- Output target: vulnerability list + fix + verification
- Phase: pre-ship / post-deploy / scheduled

### Steps

| # | Skill | Purpose | Output |
|---|-------|---------|--------|
| 1 | pre-mortem | PRD/launch plan risk analysis | Risk register |
| 2 | strategy-red-team | Attack load-bearing assumptions | Threat model |
| 3 | cso | OWASP Top 10 + STRIDE audit | Vulnerability report |
| 4 | triage-issue | Create tickets per finding | Issue list |
| 5 | code-fix (per ticket) | Apply fix per triage | Patches |
| 6 | test-case-templates | Regression + security test | Test suite |
| 7 | qa | Re-audit | Verified |

### Mandatory Re-Audit

```
⚠️ Step 7 (re-audit via qa) is MANDATORY after every fix batch.
   Security is iterative. cso must be re-run after each fix batch
   to verify no regressions and new vuln introductions.
```

### Adapted Variants

- **Plan-stage only**: Steps 1, 2 (no code yet)
- **Code-stage only**: Steps 3, 4, 5, 6, 7
- **Pentest outcome**: Steps 4, 5, 6, 7 (cso already done)

### Timing

- Manual: 2-4 weeks
- Orchestrator: 3-6 hours
- **compression**: ~10-15x

---

## Cross-Pipeline Checkpoints

After every 4 steps, pause and ask the user. Prevents 8-step chains going off-rails.

## Pipeline Hygiene

1. **Always end with qa gate** in E1/E2/E3/E5
2. **Always include canary** in E4
3. **Hard limit ≤ 8 steps per pipeline**
4. **Test before declaring done** in E1/E2/E3/E5
5. **Cross-link to design-orchestrator** for UI-heavy features
