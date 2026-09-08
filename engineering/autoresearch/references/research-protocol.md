# Evidence-driven research protocol

Use throughout design, execution, optimization and analysis. Adapt names to existing project artifacts; do not create duplicate sources of truth. Record concise hypotheses, decisions and supporting evidence, not private deliberation transcripts.

## Objective contract

Before the first comparison record metric direction, units, exact inequality, population/group denominator, missing-label and missing-prediction policy, primary objective and hard guardrails. Separate minimum improvement for retaining a candidate from the user's final target. An average or success rate cannot substitute for a requirement concerning every point/case. Missing truth limits what can be verified.

Record editable scope, baseline, evaluation command, budget type (fixed steps, wall time or compute), hardware, seed streams, sampling/aggregation and split manifest. Keep the evaluator fixed across an ablation. If a necessary evaluator bug is fixed, version it and reevaluate the baseline too. Budget or plateau stops are not objective achievement.

## Leakage and comparability

For learned systems, split at the independent entity level (patient, subject, source object, time group as appropriate). Detect duplicate geometry/content; an unverified identity grouping remains a limitation. All normalization, feature selection, templates, learned proposals and training examples must respect the outer holdout boundary. An out-of-fold prediction may still leak into another outer fold through the model that generated it; trace dependency ancestry and regenerate nested artifacts when required.

Repeatedly inspected validation folds are development evidence. Do not rename used cases as a fresh holdout. With scarce data, retain honest cross-validation results, uncertainty and external tests where available; do not claim independence that cannot be established.

Match baseline and candidate split, cases, budget and inference sampling for an ablation. Record intentional differences for broader resource/accuracy comparisons without attributing them to one isolated cause. Keep expected versus completed cases/folds explicit. Use matched seed streams for pairing and additional seeds when a fragile gain could change the decision.

## Cheapest informative experiment

1. Identify failure mechanism and what observation would falsify it.
2. Verify assumptions before training: input modality, units, label mapping, valid gradient, augmentation geometry, platform compatibility.
3. Separate proposal coverage from ranking: oracle distance says a good candidate exists, not that an automatic selector finds it. Training fit, surface residual and checkpoint replay likewise do not establish prediction accuracy.
4. Run the smallest discriminating check, then the matched full evaluation needed for the claim.
5. Inspect subgroup regressions and tail errors. Suspected annotation errors go to expert review; preserve original labels and version approved corrections. Never exclude difficult cases to manufacture a gain.

For external methods record source URL/revision, license, data/weights availability, modalities, required labels and local compatibility. Distinguish source retrieved, method adapted, pipeline executed and measured benefit. A partial adaptation is not full paper reproduction. Track tested, rejected, blocked and untested branches; several failed parameter variants do not exhaust a method family.

## Lifecycle and retention

Persist run identity, lineage, config/code/data/split hashes, actual process handle, start/end/deadline, exit code, log and artifact paths. Separate observer timeout from execution deadline. Before restart or resume inspect actual process state and completed output. A changed retry is a new attempt. A parser repair should reuse completed artifacts.

Use isolated experiment changes; never discard unrelated shared edits. Preserve rejected experiment configuration, metrics and rationale. Large temporary artifacts may follow the project's retention policy, but retain checksums and enough evidence to reproduce decisions. A kept research candidate is not a deployed model.

## Record template

Use equivalent fields in an existing ledger. This is a template, not a schema enforced by the bundled storage adapter.

```yaml
run_id: unique-id
parent_run_id: null
hypothesis: mechanism and falsifying observation
source_evidence: []
contract_version: v1
baseline_run_id: baseline-id
protocol:
  code_hash: required
  config_hash: required
  data_hash: required
  split_hash: required
  budget: {type: steps, value: 1000}
  seed_streams: {training: 1, evaluation: 2}
  inference: fixed sampling and aggregation
execution:
  state: running # completed, failed, cancelled, unknown
  handle: actual-job-handle
  exit_code: null
  log_path: unique-log-path
evaluation:
  state: pending # valid, partial, invalid
  evidence_level: development_prediction
  expected_cases: null
  completed_cases: null
  missing_truth: null
  missing_predictions: null
  metric_artifact: null
decision:
  status: pending # keep, reject, incomparable
  rationale: null
  objective_achieved: false
  stop_reason: null
  deployed: false
next_test: null
```

At each milestone append observation → interpretation → decision → evidence → next test. Update an active-run pointer separately from append-only history. On resumption read the contract, latest decision, active state and artifacts before executing.

## Skill evolution

Keep domain-specific numbers and case IDs in project records. Promote a lesson into a shared skill when it changes a reusable decision rule; link details instead of repeating the SOP across subskills. Add input/expected-action scenarios for the failure being prevented. Validate links, examples and executable snippets; distinguish static validation from actual behavioral evaluation. Do not claim a skill improved model accuracy merely because its documentation score increased.
