# Example: LLM Training Optimization

This is the original autoresearch use case - optimizing LLM training code.

## Task Configuration

```yaml
task:
  name: "llm_training_optimization"
  description: "Optimize GPT training to minimize val_bpb"
  created_at: "2026-04-07T00:00:00Z"

inner:
  type: "code_modification"
  files: ["train.py"]
  execution:
    command: "uv run train.py > run.log 2>&1"
    timeout: 360  # 6 minutes (5 min training + 1 min overhead)
    working_dir: "."

  evaluation:
    primary_metric:
      name: "val_bpb"
      pattern: "^val_bpb:\\s+([0-9.]+)"
      objective: "minimize"

    auxiliary_metrics:
      - name: "mfu_percent"
        pattern: "^mfu_percent:\\s+([0-9.]+)"
        objective: "maximize"

    constraints:
      hard:
        - metric: "peak_vram_mb"
          condition: "< 50000"  # 50GB
      soft:
        - metric: "num_params_M"
          weight: 0.2
          objective: "minimize"

    success_criteria:
      type: "threshold"
      primary_metric: "< 0.95"
      max_iterations: 100

outer:
  strategy: "git_based"

  decision:
    keep_threshold: 0.001  # 0.1% improvement
    simplicity_weight: 0.3
    auxiliary_importance: 0.1

  limits:
    max_iterations: 100
    time_budget: 28800  # 8 hours
    max_consecutive_failures: 5

  hypothesis_generation:
    mode: "guided"
    search_space:
      hyperparameters:
        DEPTH: [6, 8, 10, 12]
        ASPECT_RATIO: [48, 64, 80]
        EMBEDDING_LR: [0.4, 0.6, 0.8]
        MATRIX_LR: [0.02, 0.04, 0.06]
```

## Usage

```bash
# In the autoresearch LLM training directory
cd /path/to/autoresearch

# Start Claude Code
claude

# Then say:
"Load autoresearch and optimize train.py using the config in examples/llm_training_config.yaml"

# Or design from scratch:
"I want to optimize train.py to reduce val_bpb"
```

## Expected Behavior

1. System analyzes train.py
2. Generates hypotheses like:
   - "Increase DEPTH from 8 to 10"
   - "Adjust EMBEDDING_LR to 0.8"
   - "Change WINDOW_PATTERN to LLLL"

3. Each experiment:
   - Modifies train.py
   - Commits to git
   - Runs for 5 minutes
   - Extracts val_bpb from output
   - Keeps if improved, discards otherwise

4. Runs overnight (~100 experiments in 8 hours)

5. Next morning: analyze results
   ```
   "autoresearch:analyze - show me the best experiments"
   ```

## Tips

- Let it run overnight for best results
- Check progress occasionally with `autoresearch:analyze`
- The simplicity_weight prevents overly complex changes
- VRAM constraint prevents OOM crashes
