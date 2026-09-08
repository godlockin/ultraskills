---
name: autoresearch:analyze
description: "Analyze experiment history, generate insights, visualize trends, recommend next steps. 分析实验历史: 生成洞察 / 趋势可视化 / 推荐下一步. Trigger on 实验分析 / analyze experiments / pareto front / 趋势分析 / 洞察."
version: 1.1.0
tags: [engineering, optimization, analysis]
---

# Autoresearch Analyze

Analyze recorded experiments and recommend the next informative test. Read [research protocol](../references/research-protocol.md) for evidence levels and record format.

## Workflow

1. Load actual manifests, metrics and decision records. Identify missing artifacts instead of inventing a progress report. Use an existing project ledger where possible.
2. Group comparable runs by protocol/version, data split, budget and inference settings. Explain confounded comparisons; do not rank them as matched ablations.
3. Report primary metrics, guardrails, coverage and missing counts. Include per-case/per-group tails and paired recoveries/regressions when the objective concerns every case or subgroup.
4. Separate process failure, rejected hypothesis, retained candidate and achieved goal. Missing metrics are null/unknown, never a fabricated zero score.
5. Describe the evidence level: training fit, oracle coverage, replay consistency, development prediction or untouched evaluation. Repeated development selection is not independent validation.
6. Recommend a test that distinguishes explanations: candidate coverage versus ranking, representation versus label ambiguity, seed sensitivity versus stable gain. Record source assumptions and untested branches.
7. Append concise decision rationale and next step, linking original artifacts rather than copying reports.

## Reporting rules

- Use observed numbers with denominator and units. Explain whether missing predictions count as failures. Do not silently remove outliers or alter expert labels to improve scores.
- A better mean can coexist with worse tails. Report both and enforce the original target literally.
- A subgroup selected after viewing results is exploratory. Freeze its selector and evaluate without test-label selection before claiming improvement.
- Historical keep rates are descriptive, not calibrated probabilities of future success. Label uncertain expected gains; do not import numerical gains from unrelated literature as forecasts.
- Pareto fronts include only eligible comparable runs and respect metric direction. Show the reason for choosing an incumbent.
- Budget exhaustion or a plateau demonstrates neither target achievement nor exhaustion of all usable methods.
- Structural skill scores and exact checkpoint replay are checks of their respective mechanisms, not proof of research effectiveness or model generalization.

## Example

Input: candidate has a slightly lower mean but a worse P95, four extra threshold failures and an improved subset chosen after inspecting labels.
Output: reject whole-model promotion under the declared tail guardrail; preserve the subset hypothesis as exploratory and specify a label-independent follow-up selector/evaluation.

## Outputs

Produce the requested concise status, paired comparison, per-group table or full report. Preserve machine-readable source metrics and link the decision ledger. Use visualizations only when they clarify distributions or trade-offs. State deployed model version separately from experimental candidates.
