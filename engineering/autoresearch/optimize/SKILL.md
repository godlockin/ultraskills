---
name: autoresearch:optimize
description: "Autonomous optimization loop: generate hypotheses, run experiments, make decisions, repeat until success criteria met."
---

# Autoresearch Optimize: Autonomous Experimentation Loop

## Purpose

The "outer task" - runs an infinite optimization loop that autonomously improves your system. Generates ideas, executes experiments, learns from results, and makes keep/discard decisions.

## Core Loop

```
LOOP FOREVER (until success criteria met):
  1. Generate Hypothesis
     └─ Present options A/B/C with estimates
     └─ Give recommendation
     └─ User picks (or auto-select if running autonomously)

  2. Execute Experiment
     └─ Call autoresearch:execute
     └─ Get structured results

  3. Evaluate Results
     └─ Check hard constraints (pass/fail)
     └─ Measure primary metric improvement
     └─ Consider auxiliary metrics
     └─ Weigh complexity trade-offs
     └─ [Multi-objective] Global progress check every N successes

  4. Make Decision
     └─ Keep (advance state) or Discard (rollback)
     └─ Record to database/files

  5. Check Success Criteria
     └─ Threshold reached?
     └─ Max iterations?
     └─ Time budget exhausted?
     └─ Plateau detected?
     └─ If not met → goto step 1
     └─ If met → report and stop
```

## Hypothesis Generation

Three sources (priority order):

### 1. User-Defined Search Space
```yaml
search_space:
  hyperparameters:
    learning_rate: [0.001, 0.01, 0.1]
    depth: [4, 6, 8, 10]
```
→ Sample from this space

### 2. Code Analysis
```python
# Automatically detect in target files:
DEPTH = 4              # adjustable constant
LEARNING_RATE = 0.01   # tunable hyperparameter
activation = "relu"    # architectural choice
```
→ Generate modifications

### 3. Historical Patterns
```
History shows:
- Increasing depth: 60% success rate
- Adjusting LR: 40% success rate
- Changing activation: 20% success rate
```
→ Prioritize successful directions

## Hypothesis Presentation

```
System: "I've analyzed current state. Here are next experiment options:

A) Increase model depth from 6 to 8
   Expected time: 5-7 minutes
   Expected gain: +2.3% IoU (based on 5 similar experiments)
   Risk: Medium - may hit VRAM limit
   Rationale: Depth increases have 60% success rate historically

B) Reduce learning rate from 0.01 to 0.005
   Expected time: 5-6 minutes
   Expected gain: +0.8% IoU (based on 3 similar experiments)
   Risk: Low - safe memory-wise
   Rationale: Current loss curve suggests we may be overshooting

C) Switch activation from ReLU to GELU
   Expected time: 5-6 minutes
   Expected gain: +1.5% IoU (based on literature)
   Risk: Low - no resource impact
   Rationale: GELU often improves segmentation tasks

My recommendation: A) Increase depth
Best expected ROI, and we have VRAM headroom (14.2/16 GB used).

Which experiment should I run? (A/B/C, or suggest your own idea)
"
```

### Autonomous Mode

When running overnight (user not present):
```python
if mode == "autonomous":
    choice = select_highest_expected_value(options)
    print(f"[Autonomous] Selected: {choice.description}")
else:  # interactive
    choice = ask_user(options, recommendation)
```

## Decision Logic

### Single-Objective

```python
def should_keep(experiment, config):
    # 1. Hard constraints (one-vote veto)
    if not experiment.constraints_met:
        return False, "Hard constraint violated"

    # 2. Primary metric improvement
    improvement = (
        (experiment.primary - baseline.primary) / baseline.primary
    )

    if improvement < config.keep_threshold:
        return False, f"Improvement {improvement:.2%} < threshold"

    # 3. Auxiliary metrics (weighted)
    aux_score = sum(
        weight * evaluate_metric(metric)
        for metric, weight in config.auxiliary_weights.items()
    )

    # 4. Simplicity penalty
    if experiment.complexity_delta > 0:
        penalty = config.simplicity_weight * experiment.complexity_delta
        if improvement < penalty:
            return False, "Complexity increase not justified"

    # 5. Final decision
    total = improvement + aux_score - penalty
    return total > 0, f"Total score: {total:.3f}"
```

### Multi-Objective (with Global Check)

```python
def should_keep_multi_objective(experiment, history, config):
    # 1. Hard constraints
    if not experiment.constraints_met:
        return False, "Hard constraint violated"

    # 2. Pareto dominance
    if is_dominated_by(experiment, history.pareto_front):
        return False, "Dominated by existing solution"

    # 3. Periodic global evaluation
    if history.successes_since_last_check >= 5:
        return evaluate_global_progress(experiment, history, config)

    # 4. Add to pareto front
    return True, "Joined pareto front"

def evaluate_global_progress(experiment, history, config):
    """
    Check if we're making OVERALL progress across all metrics.
    Prevents: optimizing A while degrading B in a cycle.
    """
    window = config.multi_objective.global_check_window  # 10
    recent = history.get_recent_keeps(window)
    baseline = recent[0]
    current = experiment

    # Weighted improvement across ALL metrics
    overall = 0
    for metric, weight in config.metric_weights.items():
        delta = calculate_improvement(
            current.get(metric),
            baseline.get(metric),
            config.metrics[metric].objective
        )
        overall += weight * delta

    if overall < 0:
        print(f"""
        ⚠️  GLOBAL REGRESSION DETECTED ⚠️

        Over the last {window} experiments, overall progress is NEGATIVE: {overall:.2%}

        This suggests we're optimizing one metric at the expense of others.

        Recent trend:
        {format_metric_trends(recent, config.metrics)}

        Options:
        A) Rollback to best overall point (experiment #{recent[0].id})
        B) Adjust metric weights (currently {config.metric_weights})
        C) Continue exploring (you think this is temporary exploration)

        What should I do?
        """)

        user_choice = ask_user_decision()

        if user_choice == "A":
            rollback_to(recent[0])
            return False, "Global regression - rolled back"
        elif user_choice == "B":
            new_weights = ask_for_weights()
            config.metric_weights = new_weights
            return False, "Global regression - adjusted weights"
        else:  # C
            return True, "Global regression acknowledged, continuing"

    return True, f"Global progress: {overall:.2%}"
```

## Strategy Templates

### git_based
```python
def git_based_strategy():
    while not success_criteria_met():
        hypothesis = generate_hypothesis()
        result = execute(hypothesis)  # includes git commit

        if should_keep(result):
            # Commit stays, advance
            record_success(result)
        else:
            # Rollback
            git_reset_hard("HEAD~1")
            record_failure(result)
```

### config_snapshot
```python
def config_snapshot_strategy():
    while not success_criteria_met():
        snapshot = save_current_config()
        hypothesis = generate_hypothesis()
        result = execute(hypothesis)

        if should_keep(result):
            delete_snapshot(snapshot)
            record_success(result)
        else:
            restore_from_snapshot(snapshot)
            record_failure(result)
```

### multi_objective
```python
def multi_objective_strategy():
    pareto_front = []

    while not success_criteria_met():
        hypothesis = generate_hypothesis_near_pareto(pareto_front)
        result = execute(hypothesis)

        if should_keep_multi_objective(result, pareto_front):
            pareto_front.append(result)
            update_pareto_front(pareto_front)  # remove dominated
            record_success(result)
        else:
            record_failure(result)
```

### bandit
```python
def bandit_strategy():
    arms = initialize_arms_from_search_space()

    while not success_criteria_met():
        # UCB selection
        arm = select_arm_ucb(arms, exploration=0.1)
        hypothesis = generate_from_arm(arm)
        result = execute(hypothesis)

        # Update arm statistics
        reward = calculate_reward(result)
        arms[arm].update(reward)

        if should_keep(result):
            record_success(result)
        else:
            record_failure(result)
```

## Success Criteria

### Threshold
```yaml
success_criteria:
  type: "threshold"
  primary_metric: "> 0.90"
```
→ Stop when IoU > 0.90

### Iterations
```yaml
success_criteria:
  type: "iterations"
  max_iterations: 100
```
→ Stop after 100 experiments

### Time Budget
```yaml
success_criteria:
  type: "time_budget"
  hours: 8
```
→ Stop after 8 hours

### Plateau
```yaml
success_criteria:
  type: "plateau"
  patience: 20
  min_improvement: 0.001
```
→ Stop if no 0.1% improvement in 20 experiments

### Pareto Plateau (multi-objective only)
```yaml
success_criteria:
  type: "pareto_plateau"
  patience: 15
```
→ Stop if pareto front doesn't expand in 15 experiments

## Usage

### Automatic (after design)
```
User: "I want to optimize my segmentation model"
→ autoresearch:design completes
→ System: "Configuration saved. Ready to optimize?"
→ User: "Yes"
→ Automatically loads autoresearch:optimize
→ Runs autonomously until success or interruption
```

### Manual (explicit start)
```
User: "autoresearch:optimize - use multi_objective strategy"
→ Loads task_config.yaml
→ Applies specified strategy (overrides config if specified)
→ Starts optimization loop
```

### Resuming
```
User: "autoresearch:optimize - resume from last checkpoint"
→ Loads experiment history
→ Continues from where it left off
```

## Key Features

- 🔄 **Never stops autonomously** - runs until success criteria or manual interrupt
- 🎯 **Intelligent hypothesis generation** - learns from history
- 🤖 **Autonomous or interactive** - adapt to user presence
- 🛡️ **Global progress checks** - avoids multi-objective traps
- 📊 **Strategy templates** - proven optimization patterns
- 💾 **Persistent state** - can resume after interruption

## Safety Features

- **Max consecutive failures**: Stop if 5 crashes in a row
- **Global regression detection**: Warn if overall progress is negative
- **Timeout protection**: Each experiment has hard timeout
- **Resource monitoring**: Track VRAM, disk, etc.
- **User override**: Can always interrupt and adjust

## Output

Experiment history stored in:
- SQLite: `.autoresearch/experiments.db`
- Files: `.autoresearch/results.tsv` + `experiments/*.json`

Use `autoresearch:analyze` to visualize results.

---

**This is the heart of autoresearch** - the autonomous researcher that never sleeps.
