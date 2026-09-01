---
name: gh-fix-ci
description: Inspect GitHub PR checks with gh, pull failing GitHub Actions logs, summarize failure context, then create a fix plan and implement after user approval. Use when a user asks to debug or fix failing PR CI/CD checks on GitHub Actions and wants a plan + code changes; for external checks (e.g., Buildkite), only report the details URL and mark them out of scope.
metadata:
  short-description: Fix failing Github CI actions
github_url: https://github.com/ComposioHQ/awesome-codex-skills/tree/711ee69d724457093d52f685d729917f5389c686/gh-fix-ci
github_hash: 711ee69d724457093d52f685d729917f5389c686
version: 1.0.0
created_at: 2026-04-26T00:00:00Z
tags: [community, composio, github, ci, devops]
---

# Gh Pr Checks Plan Fix

## Overview

Use gh to locate failing PR checks, fetch GitHub Actions logs for actionable failures, summarize the failure snippet, then propose a fix plan and implement after explicit approval.
- Depends on the `plan` skill for drafting and approving the fix plan.

Prereq: ensure `gh` is authenticated (for example, run `gh auth login` once), then run `gh auth status` with escalated permissions (include workflow/repo scopes) so `gh` commands succeed. If sandboxing blocks `gh auth status`, rerun it with `sandbox_permissions=require_escalated`.

> ⚠️ **Token 权限边界**：使用最小权限 token；只读操作（logs / status）只需 `repo` read + `workflow` read。修改 `.github/workflows/*.yml` 必须使用专用 service account，不要用个人 token。`sandbox_permissions=require_escalated` 是 fallback 而非常态，仅在确认无恶意注入后使用。

## Inputs

- `repo`: path inside the repo (default `.`)
- `pr`: PR number or URL (optional; defaults to current branch PR)
- `gh` authentication for the repo host

## Safety Gates（破坏性操作防护）

> 任何 CI yaml 修改属破坏性操作，必须全部满足：

1. **diff 必先展示**：实施修改前必须 `git diff -- .github/workflows/` 输出完整 diff 并由用户确认。
2. **备份原 yaml**：修改前 `cp .github/workflows/<file>.yml /tmp/<file>.yml.bak`，失败时用其回退。
3. **影响范围检查**：读取 workflow 中所有 `needs:`、`uses:` 与 `secrets.*`，列出修改会影响的下游 jobs。
4. **优先改源而非 CI**：默认尝试修改源码、依赖版本或环境变量；改 workflow 本身只作为最后手段。
5. **干跑 / 受影响 jobs 复跑**：修改后只 `gh run rerun <run_id> --failed-only`，不要全量重跑。
6. **回滚路径**：保留原 commit hash（`git reflog`），失败时立即 `git revert <hash>`。

## Quick start

- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "<number-or-url>"`
- Add `--json` if you want machine-friendly output for summarization.

## Workflow

> Workflow 拆为 `diagnose`（只读）与 `fix`（写）两阶段；只有 diagnose 完成后用户显式授权才能进 fix。

1. **diagnose · gh authentication**（只读）
   - 运行 `gh auth status`；如有 sandbox 限制才使用 `sandbox_permissions=require_escalated`。
   - 未登录：停止，请用户先 `gh auth login`。
2. **diagnose · Resolve the PR**（只读）
   - 优先使用当前分支 PR：`gh pr view --json number,url`。
   - 用户提供 PR 号 / URL 时直接用。
3. **diagnose · Inspect failing checks**（GitHub Actions only；只读）
   - 优先使用 bundled script；只读 logs 与 status。
4. **diagnose · Scope non-GitHub Actions checks**（只读）
   - 非 GitHub Actions 的 check 只输出 URL，不进入 fix 阶段。
5. **diagnose · Summarize failures**（只读）
   - 输出 failing check / run URL / log 摘要；显式标注缺失 logs。
6. **fix · Create a plan**
   - 用 `plan` skill 起草 fix 计划，明确区分"修改源码"和"修改 CI yaml"。
   - 若计划涉及 `.github/workflows/*.yml`，必须额外执行上面"破坏性操作防护"全部 6 项；否则只执行 1、3、4 项。
7. **fix · Implement after approval**
   - 用户显式同意后实施；展示 diff、备份路径、影响范围；失败时立即按 Safety Gate 6 回滚。
8. **diagnose · Recheck**
   - 修改后用受影响 jobs 复跑 `gh pr checks`，不重跑无关 jobs。

## Bundled Resources

### scripts/inspect_pr_checks.py

Fetch failing PR checks, pull GitHub Actions logs, and extract a failure snippet. Exits non-zero when failures remain so it can be used in automation.

Usage examples:
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "123"`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --pr "https://github.com/org/repo/pull/123" --json`
- `python "<path-to-skill>/scripts/inspect_pr_checks.py" --repo "." --max-lines 200 --context 40`
