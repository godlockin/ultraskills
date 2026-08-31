# Routing Decision Table — Engineering Cluster (16 sub-clusters, 135 skills)

## Master Mapping: User Intent → Path → Entry Skill

| Cluster | Count | E1 Quality | E2 Build | E3 Debug | E4 Deploy | E5 Security | 1-shot |
|---------|-------|-----------|----------|----------|-----------|-------------|--------|
| engineering-fullstack | 24 | — | ✅ core | — | — | — | ✅ |
| engineering-arch | 15 | ✅ | ✅ Step 1-3 | — | — | — | ✅ |
| engineering-code | 10 | ✅ core | ✅ | ✅ | — | — | ✅ |
| engineering-framework | 10 | — | ✅ alt | — | ✅ alt | — | ✅ |
| engineering-devops | 10 | — | ✅ | — | ✅ core | — | ✅ |
| engineering-qa | 10 | ✅ gating | ✅ gating | ✅ gating | — | ✅ gating | ✅ |
| engineering-lang | 8 | — | ✅ alt | — | — | — | ✅ |
| engineering-mobile | 8 | — | ✅ alt | — | — | — | ✅ |
| dev-tools | 8 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| engineering-debug | 7 | — | — | ✅ core | — | — | ✅ |
| engineering-testing | 5 | ✅ gating | ✅ gating | ✅ gating | — | ✅ gating | ✅ |
| engineering-frontend | 5 | — | ✅ alt | — | — | — | ✅ |
| engineering-platform | 4 | — | ✅ alt | — | — | — | ✅ |
| engineering-security | 4 | — | — | — | — | ✅ core | ✅ |
| engineering-git | 4 | ✅ | ✅ (worktree) | ✅ | ✅ | — | ✅ |
| engineering-ml | 3 | — | ✅ alt | — | — | — | ✅ |

## Top Skills by Sub-Cluster (cross-reference)

| Cluster | Top skill | Route |
|---------|-----------|-------|
| engineering-code | receiving-code-review (9.2) | E1 step 1 |
| engineering-arch | design-an-interface (9.5) | E2 step 2 |
| engineering-arch | ubiquitous-language (9.5) | E2 step 3 |
| engineering-arch | information-architecture (9.0) | E2 step 1 |
| engineering-devops | land-and-deploy (8.8) | E4 step 2 |
| engineering-devops | setup-deploy (8.8) | E4 step 1 |
| engineering-devops | canary (8.5) | E4 step 3 |
| engineering-debug | systematic-debugging (8.3) | E3 step 2 |
| engineering-debug | investigate (8.0) | E3 step 3 |
| engineering-debug | git-guardrails-claude-code (8.5) | all (hook setup) |
| engineering-qa | qa (7.9) | E1/E2/E3/E5 gating |
| engineering-qa | devex-review (8.8) | E1 step 7 |
| engineering-security | pre-mortem (9.0) | E5 step 1 |
| engineering-security | cso (8.0) | E5 step 3 |
| engineering-security | strategy-red-team (6.8) | E5 step 2 |
| engineering-testing | triage-issue (9.0) | E3 step 1 / E5 step 4 |
| engineering-testing | test-case-templates (8.5) | E1/E2/E3/E5 gating |
| engineering-git | using-git-worktrees (8.3) | all (isolation) |
| engineering-git | finishing-a-development-branch (7.8) | E4 step 1 |
| dev-tools | codex (8.5) | E4 step 4 |
| dev-tools | codegraph-booster (8.5) | all (acceleration) |
| dev-tools | skills-audit (8.5) | E4 step 5 |

## Anti-Override Rules

These skills **must not** be invoked unless context demands:

- **cso** — only when "security audit", "OWASP", "STRIDE", "red team" appears
- **land-and-deploy** — only when "deploy", "ship", "go live" appears
- **pre-mortem** — only when "launch plan", "PRD", "go-to-market" appears
- **strategy-red-team** — only when "red team", "attack", "false assumption" appears
- **design-an-interface** — only when "design", "interface", "API shape" (it's gstack-level)
- **test-case-templates** — internal; only use when explicitly building test suites

## Fallback

If user request doesn't match any engineering cluster:
1. **AskUserQuestion** to clarify phase (design / build / test / review / ship / debug / audit)
2. Default to **Path E2 (Build)** — most common
3. Never invoke all 135 skills

## Cross-Cluster Bridges

| Engineering ask | Defer to |
|-----------------|----------|
| Frontend feature with UI | `design-orchestrator` (visual discipline) |
| Marketing analytics on app data | `data-viz` or `business-orchestrator` Path B4 |
| Multi-AI code review | `codex` (single-skill, not pipeline) |
| Production incident with PR | `design-orchestrator` if UI broken |
