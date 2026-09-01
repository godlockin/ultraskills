---
name: cohort-analysis
description: "Perform cohort analysis on user engagement data — retention curves, feature adoption trends, and segment-level insights. Use when analyzing user retention by cohort, studying feature adoption over time, investigating churn patterns, or identifying engagement trends."
version: 1.1.0
tags: ['pm', 'data', 'analytics', 'cohort']
---

# Cohort Analysis & Retention Explorer

## Purpose

Analyze user engagement and retention patterns by cohort to identify trends in user behavior, feature adoption, and long-term engagement. Combine quantitative insights with qualitative research recommendations.

> **Cohort 必须先定义清楚**。允许的 cohort 类型：
> - **Acquisition cohort**: 按首次激活 / 注册月划分（最常用）
> - **Behavior cohort**: 按首次完成关键动作的周 / 月划分
> - **Milestone cohort**: 按特定事件（如付费、新功能首发）划分
>
> Cohort 划分不明确时，先与用户确认；不要凭感觉划分。

## Sample Size & Statistical Rigor

- 每个 cohort **最低 N ≥ 100**，否则 retention 曲线噪声过大、无法稳定给出结论。
- N < 30 的 cohort：**只给描述性摘要**，禁止外推、禁止声称趋势。
- 报告必须给 **confidence interval**（建议 95% bootstrap）。
- **显著性检验**：对比两个 cohort 的 retention 之前必须做双比例检验（`scipy.stats.chi2_contingency` 或 bootstrap）；无显著性不写「优于」「劣于」。
- **2-3 个 significant insights** 配额会鼓励噪声幻觉，禁止按数字凑。Findings 必须基于效应量 + CI + p 值。
- 任何 cohort 对比都要记录样本量 + 检验方法 + 显著性 + 效应量。

## How It Works

### Step 1: Read and Validate Your Data
- Accept CSV, Excel, or JSON data files with user cohort information
- Verify data structure: cohort identifier, time periods, engagement metrics
- **Check for missing values, duplicates, and data quality issues**
- **Confirm cohort definition** with the user (acquisition / behavior / milestone) and minimum N ≥ 100
- **Detect right-censoring / survivorship bias**: cohort 中后期（如 month 6+）流失用户可能因删号 / 静默退出而被算作「未回访」；必须说明这是 right-censored 还是真流失
- **Detect temporal leakage**: 最新一期数据若 < 80% 预期记录数，截断或显式标注不完整
- Summarize key statistics (cohort sizes, date ranges, metrics available)

### Step 2: Generate Quantitative Analysis
- Calculate cohort retention rates: `retention_t = cohort_alive_at_t / cohort_initial_N`
- Define "alive" precisely (e.g., performed action X within period Y) — **do not assume** a single definition; ask the user
- Identify retention curves, drop-off patterns, and anomalies
- Compute feature adoption rates across cohorts
- Calculate month-over-month or period-over-period changes
- **Always** include N, CI, and significance test in tables
- Generate Python analysis scripts with `random.seed()` + pandas/numpy version pinned for reproducibility

### Step 3: Create Visualizations
- Generate retention heatmaps (cohorts vs. time periods)
- Create line charts showing cohort progression
- Build comparison charts for feature adoption
- Visualize drop-off points and engagement trends
- Output as interactive charts or static images

### Step 4: Identify Insights & Patterns
- Spot one or more significant patterns:
  - Early churn in specific cohorts
  - Late-stage engagement changes
  - Feature adoption clusters
  - Seasonal or temporal trends
- Highlight surprising findings and deviations
- Compare cohort performance to establish baselines

### Step 5: Suggest Follow-Up Research
- Recommend qualitative research methods:
  - Targeted user interviews with churning users
  - Feature usage surveys with engaged cohorts
  - Session replays of key interaction patterns
  - Win/loss analysis for high vs. low retention cohorts
- Design follow-up quantitative studies
- Suggest A/B tests or feature experiments

## Usage Examples

**Example 1: Upload CSV Data**
```
Upload cohort_engagement.csv with columns: cohort_month, weeks_active,
user_id, feature_x_usage, engagement_score

Request: "Analyze retention patterns and identify why Q4 2025 cohorts
underperform compared to Q3"
```

**Example 2: Describe Data Format**
```
"I have monthly user cohorts from Jan-Dec 2025. Each row shows:
cohort date, user ID, purchase frequency, and support tickets.
Analyze which cohorts show best long-term retention."
```

**Example 3: Feature Adoption Analysis**
```
Upload feature_usage.xlsx with cohort adoption data.

Request: "Compare adoption curves for our new feature across cohorts.
Which cohorts adopted fastest? Any patterns?"
```

## Key Capabilities

- **Data Reading**: Import CSV, Excel, JSON, SQL query results
- **Retention Analysis**: Calculate and visualize retention rates over time
- **Cohort Comparison**: Compare metrics across cohort groups (with N + CI)
- **Anomaly Detection**: Flag unusual patterns or drop-offs
- **Python Scripts**: Generate reusable analysis code with seed + version pinning
- **Visualizations**: Create heatmaps, charts, and interactive dashboards
- **Research Design**: Suggest targeted follow-up studies and interview approaches
- **Statistical Summary**: Provide quantitative metrics with CI and significance tests

## Tips for Best Results

1. **Include time dimension**: Provide data across multiple time periods
2. **Define cohort clearly**: Make cohort grouping explicit (signup month, feature launch date, etc.)
3. **Provide context**: Explain product changes, launches, or events during the period
4. **Multiple metrics**: Include retention, engagement, feature usage, revenue, etc.
5. **Sufficient data**: At least 3-4 cohorts with N ≥ 100 each
6. **Request specific output**: Ask for visualizations, Python scripts, or research recommendations
7. **Beware confounders**: when comparing cohorts across time, control for product changes, seasonality, and acquisition-channel shifts

## Output Format

You'll receive:
- **Data Summary**: Cohort overview, definition, and data quality assessment
- **Quantitative Findings**: Key metrics with N + CI + significance
- **Visualizations**: Charts showing retention curves, adoption patterns
- **Pattern Identification**: Insights grounded in effect size + significance
- **Research Recommendations**: Specific qualitative and quantitative follow-ups
- **Analysis Scripts** (if requested): Python code with seed + version pinning
- **Next Steps**: Prioritized actions based on findings

---

### Further Reading

- [Cohort Analysis 101: How to Reduce Churn and Make Better Product Decisions](https://www.productcompass.pm/p/cohort-analysis)
- [The Product Analytics Playbook: AARRR, HEART, Cohorts & Funnels for PMs](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
