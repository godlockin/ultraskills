# Method Cross-Reference Index (DRY, Not Duplication)

Read the source skill before applying.

## Code Review

| Method | Source |
|--------|--------|
| Process reviewer feedback | receiving-code-review |
| Self-review pre-merge | receiving-code-review |
| Multi-AI independent review | codex |

## Architecture / Design

| Method | Source |
|--------|--------|
| Information architecture (sitemap + flows) | information-architecture |
| API design (REST / GraphQL / OpenAPI) | api-designer |
| Multi-variant interface design | design-an-interface |
| DDD ubiquitous language | ubiquitous-language |
| Improve codebase architecture | improve-codebase-architecture |

## Language / Framework Specialization

| Method | Source |
|--------|--------|
| Django | django-expert |
| FastAPI / Pydantic | fastapi-expert |
| Laravel / Eloquent | laravel-specialist |
| Rust | rust-engineer |
| C++ (modern) | cpp-pro |
| C# / .NET | csharp-developer |
| Frontend distinctive interfaces | frontend-design |
| Shopify themes/apps | shopify-expert |
| Salesforce / Apex | salesforce-developer |
| Android UI/UX libraries | awesome-android-ui |

## Debugging / Investigation

| Method | Source |
|--------|--------|
| Triage (reproduce + classify + ticket) | triage-issue |
| Systematic debugging | systematic-debugging |
| 4-phase root cause | investigate |

## Testing / QA

| Method | Source |
|--------|--------|
| Test templates | test-case-templates |
| QA end-to-end (gstack) | qa |
| DevEx audit | devex-review |

## DevOps / Deploy

| Method | Source |
|--------|--------|
| CI/CD configuration | setup-deploy |
| Land + deploy | land-and-deploy |
| Canary monitoring | canary |
| Git worktree isolation | using-git-worktrees |
| Branch finishing | finishing-a-development-branch |

## Security

| Method | Source |
|--------|--------|
| Pre-mortem risk analysis | pre-mortem |
| Strategy red team | strategy-red-team |
| OWASP Top 10 + STRIDE audit | cso |

## Documentation

| Method | Source |
|--------|--------|
| User-facing changelog | changelog-generator |
| Inline docstrings + API docs | code-documenter |

## Acceleration Tools (cross-pipeline)

| Tool | Source | When to use |
|------|--------|-------------|
| CodeGraph booster | codegraph-booster | Architecture exploration, call-chain tracing |
| Multi-AI codex | codex | Independent diff review |
| Skills config audit | skills-audit | Periodic config health |
| Git guardrails hooks | git-guardrails-claude-code | Block dangerous git ops |

## How to Apply

1. **Identify what method is needed** based on brief
2. **Open source skill's SKILL.md**
3. **Apply methodology** without deviation
4. **Cross-check** with `qa` / `codex` for gating

## Quick Reference

```
Method              → Source skill                  → Path
──────────────────────────────────────────────────────────────
Process PR feedback → receiving-code-review         → E1
Architecture review → improve-codebase-architecture → E1
Changelog           → changelog-generator           → E1
Docstrings          → code-documenter                → E1/E2
DDD glossary        → ubiquitous-language           → E2
IA / sitemap        → information-architecture       → E2
API design          → api-designer                   → E2
Test suite          → test-case-templates            → E1/E2/E3/E5
End-to-end QA       → qa                            → all gating
Deploy              → land-and-deploy / setup-deploy → E4
Canary              → canary                        → E4 mandatory
Triage bug          → triage-issue                  → E3
Debug               → systematic-debugging / investigate → E3
Pre-mortem          → pre-mortem                    → E5 step 1
Red team            → strategy-red-team             → E5 step 2
OWASP audit         → cso                           → E5 step 3
Worktree            → using-git-worktrees           → all
Branch finish       → finishing-a-development-branch → E4 step 1
CodeGraph           → codegraph-booster             → all (exploration)
Multi-AI review     → codex                         → E4 step 4
Skills audit        → skills-audit                  → E4 step 5
Doc framework       → *_expert / _specialist        → 1-shot E2
```

## What This Orchestrator Does NOT Cover

The following are routed to **1-shot** (single skill):
- Backend framework deep dive (`django-expert`, `fastapi-expert`)
- Specific language deep dive (`rust-engineer`, `cpp-pro`)
- Quick doc fixes (`code-documenter`)
- Platform-specific build (`shopify-expert`, `salesforce-developer`)
- Git workflow help (`using-git-worktrees`, `finishing-a-dev-branch`)

If integrating into pipeline, route as sub-step — not primary path.
