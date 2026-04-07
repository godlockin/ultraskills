# Example: Image Segmentation Optimization

Optimize a U-Net model for medical image segmentation.

## Task Configuration

```yaml
task:
  name: "medical_image_segmentation"
  description: "Optimize U-Net IoU while keeping inference fast"
  created_at: "2026-04-07T00:00:00Z"

inner:
  type: "code_modification"
  files:
    - "models/unet.py"
    - "configs/training_config.py"
  execution:
    command: "python train.py --val --eval-only > run.log 2>&1"
    timeout: 300
    working_dir: "."

  evaluation:
    primary_metric:
      name: "iou"
      pattern: "^IoU:\\s+([0-9.]+)"
      objective: "maximize"

    auxiliary_metrics:
      - name: "dice"
        pattern: "^Dice:\\s+([0-9.]+)"
        objective: "maximize"
      - name: "inference_time"
        pattern: "^Inference time:\\s+([0-9.]+)ms"
        objective: "minimize"

    constraints:
      hard:
        - metric: "vram_gb"
          condition: "< 16.0"
        - metric: "inference_time"
          condition: "< 100"  # Must be under 100ms

      soft:
        - metric: "model_size_mb"
          weight: 0.2
          objective: "minimize"

    success_criteria:
      type: "threshold"
      primary_metric: "> 0.90"
      max_iterations: 100

outer:
  strategy: "multi_objective"

  decision:
    keep_threshold: 0.01  # 1% improvement
    simplicity_weight: 0.3

  multi_objective:
    metric_weights:
      iou: 0.7
      inference_time: 0.3
    global_check_interval: 5  # Check every 5 successes
    global_check_window: 10
    rollback_on_regression: "ask_user"

  limits:
    max_iterations: 100
    max_consecutive_failures: 5

  hypothesis_generation:
    mode: "guided"
    search_space:
      architecture:
        depth: [3, 4, 5, 6]
        base_channels: [32, 48, 64]
        use_attention: [true, false]
      hyperparameters:
        learning_rate: [0.0001, 0.0005, 0.001]
        dropout: [0.0, 0.1, 0.2]
```

## Usage

```bash
cd /path/to/your/segmentation/project

# Start Claude Code
claude

# Then say:
"I want to optimize my U-Net segmentation model to improve IoU while keeping inference under 100ms"
```

## Multi-Objective Behavior

The system will:

1. **Explore pareto front**
   - Find solutions that balance IoU vs speed
   - Some experiments prioritize accuracy
   - Others prioritize speed

2. **Global progress check** (every 5 successes)
   ```
   Recent experiments:
   - #42: IoU 0.88, Time 60ms (good!)
   - #43: IoU 0.89, Time 70ms (better!)
   - #44: IoU 0.90, Time 85ms (even better!)
   - #45: IoU 0.88, Time 55ms (faster but lower IoU)
   - #46: IoU 0.87, Time 50ms (getting worse on IoU)

   ⚠️ Warning: Overall trend shows we're optimizing speed
   at the expense of accuracy. Weighted score decreased.

   Options:
   A) Rollback to #44 (best overall)
   B) Adjust weights (currently 70% IoU, 30% speed)
   C) Continue (maybe this is exploration)
   ```

3. **Pareto visualization**
   ```
   "autoresearch:analyze - show pareto front"

   IoU ↑│         D(0.90, 85ms)
   0.90 │
   0.88 │    C(0.88, 60ms)
   0.86 │  B(0.86, 50ms)
   0.84 │A(0.84, 45ms)
        └─────────────────────── Time →
   ```

## Expected Hypotheses

The system might try:
- "Reduce depth from 5 to 4" (faster)
- "Add attention layers" (better accuracy)
- "Increase channels to 64" (better accuracy, slower)
- "Add dropout 0.1" (better generalization)
- "Use depthwise separable conv" (faster)

## Tips

- Multi-objective takes longer (needs to explore trade-offs)
- Global checks prevent cycling (optimizing A, then B, then A...)
- Set weights based on your priority (70/30 = prefer accuracy)
- Review pareto front periodically to pick your preferred solution
