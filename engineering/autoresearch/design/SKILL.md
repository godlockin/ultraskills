---
name: autoresearch:design
description: "Conversational task design. Helps you define optimization objectives, metrics, constraints, and success criteria through natural dialogue. 对话式设计任务: 定目标 / 选指标 / 配约束 / 设成功标准. Trigger on 任务设计 / define objective / configure task / 设计实验."
version: 1.1.0
tags: [engineering, optimization, task-design]
---

# Autoresearch Design: Conversational Task Configuration

## Research integrity

Before designing or running experiments, read [research protocol](../references/research-protocol.md). Freeze the objective, comparison protocol and evidence boundary; record decisions during execution. These skills guide an agent and are not an installed autonomous scheduler. Existing authorization persists; do not ask again merely to proceed to the next phase.

## Purpose

This skill helps you transform a vague idea into a complete task definition through natural conversation. It extracts information from your description and guides you to fill in missing pieces.

## How It Works

1. **Free-form description**: You describe what you want to optimize (can be detailed or brief)
2. **Intelligent extraction**: System identifies all information it can from your description
3. **Guided refinement**: System asks targeted questions only for critical missing information
4. **Configuration generation**: System produces a complete `task_config.yaml`
5. **Review and adjust**: You review and can modify the configuration

## What Gets Configured

### 🎯 Goal Layer (Most Important)
- What are you optimizing?
- Single objective or multi-objective trade-offs?
- What does success look like?

### 📊 Evaluation Layer
- Primary metric (the main success indicator)
- Auxiliary metrics (secondary indicators)
- How to extract these from outputs

### 🛡️ Constraint Layer
- Hard constraints (must satisfy, e.g., "VRAM < 16GB")
- Soft constraints (try to optimize, e.g., "prefer smaller models")

### ⚙️ Execution Layer
- Which files to modify
- How to run experiments
- Timeout settings

### 🔄 Strategy Layer
- Which optimization strategy to use
- Keep/discard thresholds
- Success criteria

## Layered Questioning Approach

The skill asks questions from general to specific:

**Level 1: Goals**
```
"What do you want to optimize? A single metric or balance multiple concerns?"
```

**Level 2: Metrics**
```
"How will you measure progress? What's the main indicator?"
"Are there other important metrics to track?"
```

**Level 3: Constraints**
```
"Are there hard limits? (memory, time, etc.)"
"Any soft preferences? (simpler is better, smaller models, etc.)"
```

**Level 4: Execution**
```
"Which files contain what you're optimizing?"
"What command runs an experiment?"
"How do we extract metrics from the output?"
```

## Smart Inference

The system makes intelligent inferences to minimize questions:

- "speed" mentioned → likely needs time constraint
- "memory issues" → add VRAM hard constraint
- "keep it simple" → set simplicity_weight
- "overnight" → set time_budget or iteration limit

## Example Interaction

```
User: "I want to optimize a U-Net model for medical image segmentation.
      Need to improve IoU but keep inference under 100ms. I have 16GB VRAM."

System: [Extracts]
✓ Task type: image segmentation optimization
✓ Primary metric: IoU (maximize)
✓ Hard constraint: inference_time < 100ms
✓ Hard constraint: VRAM < 16GB
✓ Likely files: models/*.py or segment.py

System: [Asks only missing info]
"What's your code file called and how do you run validation?"

User: "models/unet.py, run with: python train.py --val"

System: [Extracts pattern]
✓ Files: ["models/unet.py"]
✓ Command: python train.py --val > run.log 2>&1

System: "How does your script output the IoU metric?"

User: "It prints 'IoU: 0.8534' at the end"

System: [Complete config]
✓ Pattern: ^IoU: ([0-9.]+)

System: "What's your success goal? A target IoU value or run N experiments?"

User: "Stop when IoU > 0.90 or after 100 experiments"

System: [Shows complete YAML]
"Here's your complete configuration:

task:
  name: medical_image_segmentation
  ...

Does this look correct? You can ask me to adjust anything."
```

## Strategy Recommendation

Based on your task characteristics, the system recommends a strategy:

```
System: "I analyzed your task. Suggested strategies:

A) git_based strategy
   Time: 5-10 min/experiment, long-term suitable
   Benefits: Full version history, can rollback any time
   Best for: Your code optimization scenario

B) multi_objective strategy
   Time: 5-10 min/experiment, needs more experiments for pareto front
   Benefits: Balances IoU vs inference time optimally
   Best for: You have multiple competing metrics

C) config_snapshot strategy
   Time: 5-10 min/experiment, no git needed
   Benefits: Lightweight, good for config-only changes

My recommendation: A) git_based
Your project has git and you're modifying code. Simple single-objective
optimization with IoU as primary goal.

Which strategy do you prefer? (A/B/C or ask for more details)"
```

## Configuration Output

Generates `task_config.yaml`:

```yaml
task:
  name: "medical_image_segmentation"
  description: "Optimize U-Net IoU while keeping inference < 100ms"
  created_at: "2026-04-07T18:00:00Z"

inner:
  type: "code_modification"
  files: ["models/unet.py"]
  execution:
    command: "python train.py --val > run.log 2>&1"
    timeout: 300
    working_dir: "."

  evaluation:
    primary_metric:
      name: "iou"
      pattern: "^IoU: ([0-9.]+)"
      objective: "maximize"

    constraints:
      hard:
        - metric: "inference_time"
          condition: "< 100"
        - metric: "vram_gb"
          condition: "< 16.0"

    success_criteria:
      type: "threshold"
      primary_metric: "> 0.90"

outer:
  strategy: "git_based"
  decision:
    keep_threshold: 0.01
    simplicity_weight: 0.3

  limits:
    max_iterations: 100
    max_consecutive_failures: 5
```

## Key Features

- **Minimal questions**: Only asks what it can't infer
- **Context-aware**: Understands domain terminology
- **Flexible**: Accepts long descriptions or brief statements
- **Reviewable**: Shows complete config before saving
- **Editable**: Can adjust any part through conversation

## Next Steps

After design is complete:
1. Config is saved as `task_config.yaml`
2. If execution is already authorized, continue with `autoresearch:optimize`.
3. If the request was design-only, return the reviewable configuration.

## Tips for Best Results

**Good descriptions include:**
- What you're optimizing (file/system/config)
- What metric matters most
- Any constraints or limits
- How you currently run experiments

**Example good inputs:**
- "Optimize train.py to reduce val_bpb, runs with 'python train.py', time budget 5 min"
- "Tune nginx.conf for throughput, measure req/sec, keep latency p99 < 100ms"
- "Improve segment.py IoU score, run 'python eval.py', stop at 0.90"

The more context you provide upfront, the fewer questions needed!
