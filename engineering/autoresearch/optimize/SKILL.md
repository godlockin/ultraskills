---
name: autoresearch:optimize
description: "Autonomous optimization loop: generate hypotheses, run experiments, make decisions, repeat until success criteria met. 自主优化循环: 生成假设 / 跑实验 / 决策 / 重复至达标. Trigger on 启动优化 / optimization loop / multi-objective / bandit / Pareto / 开始迭代."
version: 1.1.0
tags: [engineering, optimization, loop]
---

# Autoresearch Optimize

Use for an authorized iterative research loop. Read [research protocol](../references/research-protocol.md) before selecting experiments. These are agent instructions, not an installed scheduler.

## Workflow

1. Load the objective contract, baseline, decision ledger and actual running-job state. Preserve existing user authorization; ask only for missing decisions that block meaningful work.
2. Select a falsifiable hypothesis using code inspection, primary-source evidence and observed failure groups. Record the expected mechanism and cheapest diagnostic that could reject it. Quantitative gain estimates require cited comparable runs; otherwise mark gain unknown.
3. Run a small invariant/gradient/compatibility check when it can prevent an expensive invalid experiment. Then call [execute](../execute/SKILL.md) with a unique run ID and frozen evaluation protocol.
4. Check completeness, comparability and hard guardrails before ranking. Invalid or unmatched results are not keep/discard evidence.
5. Keep a research candidate only when the declared decision rule passes. Preserve rejected runs and rationale. Candidate selection does not deploy a model or prove the user's target.
6. Record the decision, remaining uncertainty and next discriminating experiment. Check objective achievement separately from budget, cancellation, plateau or a blocking dependency.

## Decision rule

For a scalar objective, use improvement in its declared units:

```python
import math

def primary_gain(candidate, baseline, objective):
    if not all(math.isfinite(x) for x in (candidate, baseline)):
        raise ValueError("Non-finite metric")
    if objective not in {"minimize", "maximize"}:
        raise ValueError("Unknown objective")
    return baseline - candidate if objective == "minimize" else candidate - baseline
```

Require gain to exceed a predeclared nonnegative minimum gain and every hard constraint to pass. If reporting relative gain, divide by abs(baseline) only for nonzero baselines; otherwise report the absolute change. Do not combine differently scaled auxiliary metrics without an explicit normalization and weighting contract. Simplicity is a declared tie-breaker or a defined penalty, never an uninitialized value.

For multiple objectives, calculate direction-aware Pareto dominance among complete comparable runs satisfying every hard guardrail. Retaining a nondominated candidate does not automatically replace the incumbent. Check regressions against both the incumbent and original baseline every comparison; weighted improvement cannot waive a hard constraint. Changing metric weights or targets creates a versioned contract, not retroactive success.

## Strategies

- **Git**: use an isolated experiment checkout or tracked patch. Preserve user's uncommitted work. Discard only experiment-owned changes after inspecting current state; never reset a shared checkout to discard an experiment.
- **Config snapshots**: retain the original and candidate configurations with hashes. Restore only if the target still matches this experiment's write; concurrent edits require reconciliation.
- **Multi-objective**: retain the eligible frontier and record why an incumbent was selected.
- **Bandit**: define reward direction, comparable evaluation budget and failed-run handling before updating arm statistics. Adaptive search performance is development evidence.

## Stop and resume

Report separate fields: process state, research decision, objective achieved, stop reason. A configured iteration/time limit or plateau ends that run without claiming the goal was met or all external methods exhausted. Within the authorized scope, diagnose failed approaches and try meaningfully different hypotheses; do not cycle through identical failures indefinitely.

On resume, inspect the job handle, exit record and artifact manifest before starting another process. A tool wait returning early does not establish that training stopped. Continue a verified compatible checkpoint; changed code/data/config requires a new attempt and explicit lineage.

## Example

Input: mean error decreases, but the declared per-group maximum error guardrail fails.
Output: reject whole-model promotion, preserve metrics and checkpoints; any improved subset is exploratory until a fixed selector is evaluated without access to its test labels.

## Completion checklist

- Matched protocol and complete denominators checked.
- Research decision supported by linked artifacts, including regressions.
- User target evaluated literally, independent of stopping budget.
- Resume state and next hypothesis recorded; deployed state identified separately.
