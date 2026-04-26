---
name: autoresearch:analyze
description: "Analyze experiment history, generate insights, visualize trends, recommend next steps."
version: 1.0.0
tags: [engineering]
---

# Autoresearch Analyze: Experiment Analysis and Insights

## Purpose

Queries experiment history to understand what worked, what didn't, and where to go next. Provides reports, visualizations, and actionable recommendations.

## What It Analyzes

- 📈 Performance trends over time
- 🏆 Best experiments (by different criteria)
- 🎯 Success patterns (which types of changes work)
- ⚠️ Failure patterns (what to avoid)
- 📊 Pareto front (for multi-objective)
- 🔍 Hypothesis effectiveness (which directions pay off)

## Queries Supported

### Basic Queries

**Show recent experiments**:
```
User: "Show me the last 10 experiments"

Output:
┌────┬─────────────────────┬──────────┬────────┬──────────────────────────┐
│ ID │ Timestamp           │ IoU      │ Status │ Description              │
├────┼─────────────────────┼──────────┼────────┼──────────────────────────┤
│ 42 │ 2026-04-07 18:30:00 │ 0.8723   │ keep   │ Increase depth to 8      │
│ 41 │ 2026-04-07 18:25:00 │ 0.8701   │ keep   │ Adjust LR to 0.008       │
│ 40 │ 2026-04-07 18:20:00 │ 0.8689   │ discard│ Switch to GELU           │
│ 39 │ 2026-04-07 18:15:00 │ 0.0000   │ crash  │ Double model width (OOM) │
│ ...│ ...                 │ ...      │ ...    │ ...                      │
└────┴─────────────────────┴──────────┴────────┴──────────────────────────┘
```

**Best N experiments**:
```
User: "What are the top 5 experiments?"

Output:
Top 5 by IoU:
1. #42: 0.8723 - Increase depth to 8 (1 hour ago)
2. #41: 0.8701 - Adjust LR to 0.008 (1h 5min ago)
3. #38: 0.8689 - Add dropout 0.1 (1h 20min ago)
4. #35: 0.8645 - Increase channels to 64 (2 hours ago)
5. #30: 0.8612 - Baseline (3 hours ago)
```

**Compare two experiments**:
```
User: "Compare experiment #42 and #30"

Output:
Experiment #42 vs #30 (baseline):

Metrics:
  IoU:            0.8723 vs 0.8612 (+1.29% ✓)
  Dice:           0.8650 vs 0.8520 (+1.53% ✓)
  Inference:      52ms vs 45ms (+15.6% ⚠️)
  VRAM:           15.2GB vs 14.2GB (+1.0GB)

Changes made:
  - DEPTH: 6 → 8
  - Added residual connections

Constraints:
  VRAM < 16GB:    ✓ (15.2 < 16.0)
  Time < 100ms:   ✓ (52 < 100)

Decision: KEEP
Reason: Primary metric improved above threshold, all constraints met
```

### Advanced Queries

**Trend analysis**:
```
User: "Show me the improvement trend"

Output:
IoU Progress Over Time:

0.90 ┤
0.88 ┤                                    ●
0.86 ┤                  ●       ●    ●  ●●●
0.84 ┤        ●     ●  ●●  ●  ●●●  ●●●●●●●●
0.82 ┤    ●  ●● ●  ●●●●●●●●●●●●●●●●●●●●●●●●●
0.80 ┤  ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
     └────────────────────────────────────────────
      0    10   20   30   40   50   60   70   80

Key insights:
- Started: 0.8534
- Current best: 0.8723
- Total improvement: +2.21%
- Plateau detected around experiment 60-70
- Recent breakthrough at #75 (new architecture)
```

**Success patterns**:
```
User: "What types of changes work best?"

Output:
Hypothesis Category Success Rates:

Architecture changes:  ████████░░ 8/10 (80%)
  - Depth increases:     5/6 (83%)
  - Residual connections: 2/2 (100%)
  - Attention layers:    1/2 (50%)

Hyperparameter tuning: ██████░░░░ 6/10 (60%)
  - Learning rate:       4/7 (57%)
  - Batch size:          2/3 (67%)

Optimizer changes:     ███░░░░░░░ 3/10 (30%)
  - Adam → AdamW:        0/2 (0%)
  - LR schedules:        3/8 (38%)

Recommendation: Focus on architecture changes, especially depth and residual connections.
```

**Failure analysis**:
```
User: "Why do experiments fail?"

Output:
Failure Breakdown (25 discarded + 5 crashed):

Discarded (25):
  - Insufficient improvement: 18 (72%)
  - Complexity not justified: 5 (20%)
  - Auxiliary metric degraded: 2 (8%)

Crashed (5):
  - OOM (VRAM): 3 (60%)
  - Numerical instability: 2 (40%)

Recommendations:
  1. Be conservative with model size (3 OOM failures)
  2. Watch for NaN with aggressive LR (2 instability crashes)
  3. Set keep_threshold higher if too many marginal improvements
```

### Multi-Objective Queries

**Pareto front**:
```
User: "Show me the pareto front"

Output:
Pareto Front (4 solutions):

IoU↑ │                    D (0.88, 60ms)
0.90 │
0.88 │          C (0.86, 55ms)
0.86 │     B (0.84, 48ms)
0.84 │  A (0.82, 45ms)
0.82 │
     └──────────────────────────────────────────
      40ms    50ms    60ms    70ms    80ms    →Inference Time↓

Solutions:
A: #30 - Baseline (0.82 IoU, 45ms)
B: #35 - Increase channels (0.84 IoU, 48ms)
C: #42 - Add depth (0.86 IoU, 55ms)
D: #48 - Full optimization (0.88 IoU, 60ms)

Current best depends on your priority:
- Need speed? → A
- Balanced? → B or C
- Need accuracy? → D
```

**Trade-off analysis**:
```
User: "Analyze the speed vs accuracy trade-off"

Output:
Speed vs Accuracy Trade-off Analysis:

For every 1% IoU improvement, inference time increases ~5ms on average.

Diminishing returns observed:
- 0.82 → 0.84 IoU: +3ms (good ROI)
- 0.84 → 0.86 IoU: +7ms (acceptable)
- 0.86 → 0.88 IoU: +5ms (good)
- 0.88 → 0.90 IoU: +15ms (poor ROI, not on pareto front)

Current sweet spot: Experiment #42 (0.86 IoU, 55ms)
```

## Visualizations

### Performance over time (text-based)
```
User: "Visualize experiment progress"

Output:
[ASCII chart showing IoU trend]
```

### Metric distributions
```
User: "Show IoU distribution"

Output:
IoU Distribution (all kept experiments):

0.82-0.83: ██░░░░░░░░ 2
0.83-0.84: ████░░░░░░ 4
0.84-0.85: ████████░░ 8
0.85-0.86: ██████░░░░ 6
0.86-0.87: ████░░░░░░ 4
0.87-0.88: ██░░░░░░░░ 2

Mean: 0.8489
Median: 0.8501
Std: 0.0145
```

### Hypothesis effectiveness (heatmap)
```
User: "Which hypotheses are most effective?"

Output:
Hypothesis Type × Outcome:

                   Keep  Discard  Crash
Architecture       8     2        0     ████████
Hyperparameters    6     4        0     ██████
Optimizer          3     7        0     ███
Regularization     4     3        2     ████
Training Schedule  2     5        1     ██

Color intensity = success rate
```

## Recommendations

The analyze skill provides actionable insights:

```
Based on 50 experiments:

✅ Keep doing:
  1. Increasing model depth (83% success rate)
  2. Adding residual connections (100% success, 2/2)
  3. Conservative LR adjustments around 0.008-0.012

⚠️  Be cautious with:
  1. Optimizer changes (30% success rate)
  2. Aggressive LR (>0.02 caused 2 NaN crashes)
  3. Model width beyond 128 channels (3 OOM)

🔍 Unexplored areas:
  1. Attention mechanisms (only 1 experiment)
  2. Data augmentation strategies (0 experiments)
  3. Loss function variations (0 experiments)

🎯 Next recommended experiments:
  A) Add self-attention layer (expected +1.5% IoU)
  B) Try focal loss instead of CE (literature suggests +0.8%)
  C) Increase depth to 10 (following successful depth trend)

My recommendation: Try A first - attention is unexplored and promising.
```

## Export Options

**CSV export**:
```
User: "Export results to CSV"
→ Saves to analysis_2026-04-07.csv
```

**JSON export**:
```
User: "Export full history as JSON"
→ Saves to experiments_2026-04-07.json
```

**Report generation**:
```
User: "Generate a summary report"
→ Creates report.md with all key metrics, charts, insights
```

## Integration with Storage

Works with both storage backends:
- **SQLite**: Efficient queries with SQL
- **Files**: Loads and parses TSV + JSON

Unified interface abstracts the difference:
```python
storage = get_storage()  # auto-detects SQLite or files
experiments = storage.query_experiments(filters)
```

## Usage

**During optimization**:
```
[optimize running...]
User: "autoresearch:analyze - show progress"
→ Quick status update without interrupting optimization
```

**After completion**:
```
User: "autoresearch:analyze - full report"
→ Comprehensive analysis of all experiments
```

**Standalone**:
```
User: "autoresearch:analyze - I want to understand my previous run"
→ Loads history and provides interactive analysis
```

## Key Features

- 📊 Rich queries (recent, best, patterns, trends)
- 📈 Text-based visualizations (works in terminal)
- 🎯 Actionable recommendations
- 🔍 Failure analysis
- 🏆 Multi-objective pareto analysis
- 📁 Export to CSV/JSON/Markdown
- ⚡ Works with SQLite or file storage

## Example Session

```
User: "autoresearch:analyze"

System: "Loaded 50 experiments from .autoresearch/experiments.db

Quick summary:
- Best IoU: 0.8723 (experiment #42)
- Total improvement: 2.21% from baseline
- Success rate: 50% (25 kept / 25 discarded / 5 crashed)
- Time elapsed: 4.2 hours

What would you like to analyze?
1. Show improvement trend
2. Best experiments
3. Success/failure patterns
4. Pareto front (if multi-objective)
5. Detailed report
6. Custom query

(Or just tell me what you want to know)"

User: "What's working and what isn't?"

System: [Generates success pattern analysis + recommendations]
```

---

**Use this skill to understand your experiments and make informed decisions.**
