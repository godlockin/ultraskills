---
name: autoresearch:execute
description: "Execute a single experiment: modify code/config, run command, extract metrics, handle errors."
---

# Autoresearch Execute: Single Experiment Runner

## Purpose

Executes one experiment cycle: apply a hypothesis, run the experiment, extract metrics, and return results. This is the atomic unit of work called by `autoresearch:optimize`.

## Inputs

Requires:
1. `task_config.yaml` - task definition
2. Hypothesis - what to try (e.g., "increase depth to 6")

## Workflow

```
1. Apply Modification
   └─ Edit target files based on hypothesis

2. Git Commit (if git_based strategy)
   └─ Commit with descriptive message

3. Run Experiment
   └─ Execute command with timeout
   └─ Redirect output to run.log

4. Extract Metrics
   └─ Parse primary metric from output
   └─ Parse auxiliary metrics
   └─ Parse constraint values

5. Handle Errors
   └─ Detect crashes, OOM, timeouts
   └─ Attempt simple fixes if possible
   └─ Return structured error info

6. Return Results
   └─ All metrics + metadata + status
```

## Output Structure

```python
{
    "status": "success" | "crash" | "timeout",
    "primary_metric": {
        "name": "iou",
        "value": 0.8612
    },
    "auxiliary_metrics": {
        "dice": 0.86,
        "inference_time": 43
    },
    "constraints": {
        "vram_gb": {"value": 14.2, "limit": 16.0, "met": True},
        "inference_time": {"value": 43, "limit": 100, "met": True}
    },
    "execution_time": 305.2,
    "commit_hash": "b2c3d4e",  # if git_based
    "error_log": null,  # or error message if crashed
    "hypothesis": "Increase depth to 6"
}
```

## Error Handling

### Crash Detection

**OOM (Out of Memory)**:
```
Detected: "CUDA out of memory" in logs
Action: Suggest reducing batch_size or model_size
Retry: Yes, with smaller config
```

**Import Error**:
```
Detected: "ModuleNotFoundError" or "ImportError"
Action: Check if it's a typo, suggest fix
Retry: Yes, after fix
```

**Numerical Instability**:
```
Detected: "NaN" or "Inf" in metrics
Action: Suggest lower learning rate
Retry: Maybe (user decision)
```

### Timeout Handling

If experiment exceeds timeout:
```
1. Kill process
2. Mark as "timeout" status
3. Log partial output
4. Return timeout result (primary_metric = None)
```

### Metric Extraction Failure

If pattern doesn't match output:
```
1. Show last 50 lines of output
2. Ask user to verify pattern
3. Offer to adjust pattern in config
4. Retry with corrected pattern
```

## Example Execution

```
Input hypothesis: "Increase DEPTH from 4 to 6"

[Step 1] Applying modification to train.py...
  - Changed: DEPTH = 4 → DEPTH = 6

[Step 2] Committing changes...
  - Commit b2c3d4e: "experiment: increase depth to 6"

[Step 3] Running experiment...
  - Command: python train.py --val > run.log 2>&1
  - Timeout: 300s
  - Status: ████████████████████ 100% (305s elapsed)

[Step 4] Extracting metrics...
  ✓ Primary: iou = 0.8612
  ✓ Auxiliary: dice = 0.86, inference_time = 43ms
  ✓ Constraints: vram_gb = 14.2 (< 16.0 ✓), inference_time = 43 (< 100 ✓)

[Step 5] All constraints satisfied, experiment successful!

Result: {
  "status": "success",
  "primary_metric": {"name": "iou", "value": 0.8612},
  ...
}
```

## Retry Logic

**Simple errors → Auto-retry (up to 3 times)**:
- Typos in code
- Missing imports (can be added)
- Syntax errors (can be fixed)

**Resource errors → Suggest and ask**:
- OOM → "Try reducing BATCH_SIZE to 64?"
- Timeout → "Try reducing DEPTH or NUM_EPOCHS?"

**Fundamental errors → Give up**:
- Missing data files
- Invalid configuration
- Incompatible dependencies

## Integration with Strategies

### git_based
```python
1. Modify files
2. git add + git commit
3. Run experiment
4. If discard → git reset --hard HEAD~1
5. If keep → do nothing (commit stays)
```

### config_snapshot
```python
1. Save current config to .autoresearch/snapshots/
2. Modify config
3. Run experiment
4. If discard → restore from snapshot
5. If keep → delete snapshot
```

### multi_objective & bandit
Same as git_based or config_snapshot, strategy only affects decision logic.

## Usage

**Automatic** (called by `autoresearch:optimize`):
```
[optimize loop]
  → generate hypothesis
  → autoresearch:execute(hypothesis)
  → receive results
  → make decision
```

**Manual** (for testing):
```
User: "autoresearch:execute - try increasing depth to 6"
→ Applies change, runs, reports results
```

## Output Storage

Results are written to:
- **Database mode**: `.autoresearch/experiments.db`
- **File mode**: `.autoresearch/results.tsv` + `experiments/exp_NNN.json`

Storage layer handles this automatically (see `lib/storage.py`).

## Key Features

- ✅ Atomic execution (one hypothesis → one result)
- ✅ Structured error handling (categorize and suggest fixes)
- ✅ Timeout protection (never hang indefinitely)
- ✅ Metric validation (check constraints before returning)
- ✅ Version tracking (git commits or snapshots)

## Notes

- This skill is **stateless** - it doesn't remember previous experiments
- State management is handled by `autoresearch:optimize`
- All experiment history is in the storage layer
