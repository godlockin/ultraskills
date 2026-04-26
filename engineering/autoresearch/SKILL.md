---
name: autoresearch
description: "Universal autonomous task optimization framework. Transforms any measurable, iterable task into a self-improving system through conversational design and intelligent optimization loops."
version: 1.0.0
tags: [engineering, arena-winner]
---

# Autoresearch: Universal Task Optimization Framework

## Overview

Autoresearch is a meta-framework that applies autonomous optimization to **any task** with measurable outcomes. It abstracts the inner/outer task pattern from LLM training research into a general-purpose system.

**Core Concepts:**
- **Inner Task**: The work being optimized (code, config, parameters)
- **Outer Task**: The optimization strategy (hypothesis generation, experimentation, decision-making)

**Key Features:**
- 🎯 Conversational task design - describe your task in natural language
- 🔄 Autonomous optimization loops - runs indefinitely until goals met
- 📊 Multi-objective support - balance competing metrics intelligently
- 🛡️ Global progress tracking - avoids local optimization traps
- 💾 Auto-fallback storage - SQLite → files, adapts to your environment

## When to Use This Skill

Use `autoresearch` when you need to:
- Optimize any code/config through iterative experimentation
- Balance multiple competing metrics (speed vs accuracy, cost vs performance)
- Run autonomous overnight experiments
- Find optimal hyperparameters or architectural choices
- Systematically explore a search space

**Examples:**
- "Help me optimize a model training script"
- "I want to tune my API performance"
- "Optimize this image segmentation pipeline"
- "Find the best system configuration for my workload"

## Sub-Skills

This skill provides specialized sub-commands for different phases:

### `autoresearch:design`
Conversational task design - helps you define:
- What to optimize (objectives, metrics)
- How to evaluate (primary/auxiliary metrics, constraints)
- When to stop (success criteria)

### `autoresearch:execute`
Single experiment execution:
- Modifies code/config based on hypothesis
- Runs experiment and extracts metrics
- Handles errors and timeouts

### `autoresearch:optimize`
Autonomous optimization loop:
- Generates hypotheses (with options, estimates, recommendations)
- Manages experiment lifecycle
- Makes keep/discard decisions
- Implements strategy templates (git_based, multi_objective, bandit, config_snapshot)

### `autoresearch:analyze`
Experiment analysis and insights:
- Queries experiment history
- Generates reports and visualizations
- Identifies successful patterns
- Recommends next directions

## Usage Modes

### 🤖 Automatic Mode (Recommended)
Just describe what you want - the system automatically routes to appropriate sub-skills:

```
User: "I want to optimize a U-Net segmentation model"
→ Loads autoresearch:design
→ After configuration, automatically starts autoresearch:optimize
→ Periodically shows progress via autoresearch:analyze
```

### 🎯 Manual Mode (Expert Control)
Explicitly invoke sub-skills:

```
User: "autoresearch:design - configure a new optimization task"
User: "autoresearch:optimize - start optimization with multi_objective strategy"
User: "autoresearch:analyze - show me the pareto front"
```

## How It Works

1. **Design Phase** (`autoresearch:design`)
   - User describes task in natural language
   - System extracts: files, commands, metrics, objectives, constraints
   - Guides user to fill missing critical information
   - Generates `task_config.yaml`

2. **Optimization Phase** (`autoresearch:optimize`)
   - Loads strategy template (auto-recommended or user-specified)
   - Enters autonomous loop:
     - Generate hypothesis (present options A/B/C with estimates)
     - Execute experiment (`autoresearch:execute`)
     - Evaluate results (multi-dimensional decision logic)
     - Keep or discard (update database/files)
     - Check success criteria (continue or stop)

3. **Analysis Phase** (`autoresearch:analyze`)
   - Query experiment database
   - Generate insights (best experiments, trends, patterns)
   - Visualize progress
   - Suggest next steps

## Strategy Templates

Four built-in optimization strategies:

| Strategy | Best For | Key Features |
|----------|----------|--------------|
| **git_based** | Code optimization | Git versioning, simplicity weighting |
| **config_snapshot** | Config tuning | Lightweight snapshots, no git required |
| **multi_objective** | Multiple metrics | Pareto optimization, global progress checks |
| **bandit** | Large search spaces | UCB exploration-exploitation balance |

The system auto-recommends the best strategy based on your task characteristics.

## Configuration Example

```yaml
task:
  name: "image_segmentation_optimization"
  description: "Optimize U-Net for medical images"

inner:
  type: "code_modification"
  files: ["models/unet.py"]
  execution:
    command: "python train.py --val > run.log 2>&1"
    timeout: 300

  evaluation:
    primary_metric:
      name: "iou"
      pattern: "^IoU: ([0-9.]+)"
      objective: "maximize"

    constraints:
      hard:
        - metric: "vram_gb"
          condition: "< 16.0"

    success_criteria:
      type: "threshold"
      primary_metric: "> 0.90"

outer:
  strategy: "multi_objective"
  decision:
    keep_threshold: 0.01
```

## Design Principles

1. **Conversational by default**: Natural language → structured config
2. **Intelligent but transparent**: Give options, explain trade-offs, recommend
3. **Adaptive**: Auto-fallback for storage, auto-recommend strategies
4. **Holistic optimization**: Not just single metrics, consider constraints and trade-offs
5. **Safe exploration**: Global checks prevent optimization traps

---

**Ready to optimize?** Just say what you want to improve, and I'll guide you through the rest.
