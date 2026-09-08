---
name: autoresearch:execute
description: "Execute a single experiment: modify code/config, run command, extract metrics, handle errors. 单次实验执行: 改代码 / 跑命令 / 提取指标 / 处理错误. Trigger on 跑实验 / run experiment / 改配置执行 / extract metric."
version: 1.1.0
tags: [engineering, optimization, execution]
---

# Autoresearch Execute

Execute one hypothesis and return verifiable artifacts. Read [research protocol](../references/research-protocol.md), especially lifecycle and comparison rules.

## Inputs and preparation

Require the objective contract, hypothesis, baseline ID, editable scope, execution command, evaluation protocol and available budget. Reuse existing project records rather than create a competing database. Check data availability, units, dependencies and disk before large downloads or outputs. Validate only assumptions relevant to this experiment.

Before changing files, snapshot or hash experiment inputs and preserve existing work. Use an isolated checkout/configuration where available. A commit is optional; do not stage unrelated files or commit merely to run an experiment.

## Run lifecycle

1. Allocate a unique run ID and output directory. Record parent attempt, code/config/data/split hashes, training IDs, seed streams, expected cases, command, runtime environment and configured deadline.
2. Start the command through the environment's background execution mechanism. Persist its job handle, start time and log path. Follow repository logging rules; avoid progress streams.
3. Inspect bounded status snapshots, not live log streams. A tool observation timeout means the process may still be running. Terminate only for a verified execution deadline, cancellation or diagnosed condition requiring termination.
4. Confirm terminal state and exit code. A completed command is not yet a valid evaluation. Check finite metrics, expected folds/cases, missing predictions, protocol identity and output hashes.
5. Return execution state and artifact paths. Keep/discard and goal achievement belong to the optimization decision, not process exit status.

## Recovery

- Inspect concise failure context. Fix ordinary local defects within existing authorization; preserve failed attempt evidence.
- A change to batch size, training steps, loss or code creates a new attempt/configuration. Reassess comparability; do not silently overwrite the failed run.
- Reparse completed output after parser repairs; do not rerun expensive training solely to fix metric extraction.
- Verify checkpoint compatibility and completed folds before resuming. Never start a duplicate job because an observer stopped waiting.
- Missing data/dependencies: investigate accessible alternatives. Report the specific unresolved dependency if no authorized path remains.
- Record partial runs as partial; never rank them against complete runs as if denominators matched.

## Output contract

Use the project's equivalent fields or the [record template](../references/research-protocol.md#record-template). Distinguish running/completed/failed/cancelled/unknown execution states; valid/partial/invalid evaluation; pending/keep/reject/incomparable decision. Unknown exit code remains unknown, not zero.

The bundled [storage adapter](../lib/storage.py) is optional. Inspect its schema before use: a storage helper does not implement job orchestration, leakage checks or promotion gates. Preserve richer provenance in an artifact manifest if the adapter cannot represent it.

## Example

Input: observer returns after 30 seconds; configured training deadline is 2 hours.
Output: record running or unknown from actual job state, retain handle, check later. Do not kill/restart training or label the experiment failed solely from the observation timeout.

## Checklist

- Unique artifacts and actual process handle retained.
- Exit and output completeness verified.
- Retry lineage explicit; existing user changes preserved.
- No deployment or research-success claim inferred from exit zero.
