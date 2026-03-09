# Skill Arena - Usage Guide

> AI Skills benchmark testing framework with expert panel-designed test cases and LLM-based evaluation.

## Quick Start

```bash
# Run full pipeline: scan → cluster → test → score → report → update
python devops/skill-arena/scripts/skill-arena.py full

# Or run steps individually
python devops/skill-arena/scripts/skill-arena.py scan    # Scan and cluster
python devops/skill-arena/scripts/skill-arena.py test    # Run benchmarks
python devops/skill-arena/scripts/skill-arena.py score   # Score and rank
python devops/skill-arena/scripts/skill-arena.py report  # Generate report
python devops/skill-arena/scripts/skill-arena.py update  # Update index.json
```

## Commands

| Command | Description |
|---------|-------------|
| `scan` | Scan all skills and cluster by similarity |
| `test` | Run PK tests for each cluster (expert-designed test cases) |
| `score` | Calculate weighted scores and rankings |
| `report` | Generate markdown benchmark report |
| `update` | Update index.json with arena data |
| `full` | Run complete pipeline |
| `backtrack` | Re-test all skills with updated test cases |

## Test Execution Modes

### Simulated Mode (Default)
Fast, no API keys required:
```bash
python devops/skill-arena/scripts/skill-arena.py test
```

### LLM Mode (Production)
Real skill invocation and LLM Judge evaluation:
```bash
# Anthropic Claude
export ANTHROPIC_API_KEY=your-api-key
python devops/skill-arena/scripts/skill-arena.py test --use-llm --provider anthropic

# OpenAI
export OPENAI_API_KEY=your-api-key
python devops/skill-arena/scripts/skill-arena.py test --use-llm --provider openai

# Google
export GOOGLE_API_KEY=your-api-key
python devops/skill-arena/scripts/skill-arena.py test --use-llm --provider google
```

### Parallel Execution Control
```bash
# Default: 4 workers
python devops/skill-arena/scripts/skill-arena.py test --workers 8

# Sequential execution
python devops/skill-arena/scripts/skill-arena.py test --no-parallel
```

## Output Files

After running `full` pipeline:

```
devops/skill-arena/
├── clusters.json                    # Cluster assignments (17 categories)
├── winners.json                     # Category winners
├── reports/
│   ├── raw-results.json             # Raw test execution results
│   ├── rankings.json                # Scored rankings
│   └── benchmark-report-YYYY-MM-DD.md  # Human-readable report
├── test-suites/
│   ├── [category]/
│   │   ├── tests.yaml               # Expert-designed test cases
│   │   └── expert-discussion.json   # Expert roundtable records
└── templates/
    └── test-case-templates/
        └── SKILL.md                 # Test case template library
```

## Index.json Updates

Each skill gets additional fields:

```json
{
  "id": "page-cro",
  "name": "Page Conversion Rate Optimization",
  "arena": {
    "rank": 1,
    "category": "cro",
    "score": 93.5,
    "scores": {
      "speed": 28.0,
      "quality": 47.5,
      "maintainability": 18.0
    },
    "is_winner": true,
    "test_date": "2026-03-09",
    "test_version": "1.0.0"
  },
  "priority": 1,
  "recommended_for": ["best-cro-skill", "landing-page-review", "conversion-audit"],
  "tags": ["arena-winner", "cro", "marketing"]
}
```

## Adding New Test Cases

Edit `test-suites/[category]/tests.yaml`:

```yaml
test_cases:
  - id: tc-006
    name: "New Test Case Name"
    description: "What this test evaluates"
    input:
      type: url | text | scenario | code
      value: "..."
    expected_outputs:
      - "Expected output 1"
      - "Expected output 2"
    scoring:
      speed: { weight: 0.3, max_points: 30 }
      quality: { weight: 0.5, max_points: 50 }
      maintainability: { weight: 0.2, max_points: 20 }
```

Then run `backtrack` to re-test all skills with new test cases.

## Expert Panels

Each category has a dedicated expert panel (3-4 experts) who design test cases:

| Category | Experts | Focus Areas |
|----------|---------|-------------|
| CRO | Dr. Sarah Chen, Marcus Rodriguez, Dr. Emily Watson, James Park | Conversion optimization, UX research, behavioral psychology |
| Engineering | Martin Fowler, Kent Beck, Jessica Kerr, Will Larson | Software architecture, TDD, observability, engineering leadership |
| SEO | Dr. Michael Brenner, Lisa Chang, Ahmed Hassan, Rachel Green | Technical SEO, content optimization, AI search, link building |
| Product | Marty Cagan, Teresa Torres, Don Norman, Lenny Rachitsky | Product discovery, user research, UX design, product-led growth |
| Marketing | Neil Patel, Rand Fishkin, Avinash Kaushik, Mari Smith | Growth marketing, attribution, analytics, social media |
| ... | ... | ... |

See `devops/skill-arena/scripts/expert_panels.py` for full expert definitions.

## Scoring Formula

```
Total = (Speed × 0.30) + (Quality × 0.50) + (Maintainability × 0.20)

Speed (0-30 points):
  - Response time < 50% threshold: 30 points
  - Response time < threshold: Linear scaling
  - Response time >= threshold: Bonus points for speed

Quality (0-50 points) - LLM Judge evaluated:
  - Accuracy (15 points): Factual accuracy and relevance
  - Completeness (15 points): Coverage of required aspects
  - Actionability (10 points): Specificity of recommendations
  - Depth (10 points): Analysis depth vs surface-level

Maintainability (0-20 points):
  - Structure (10 points): Organization and formatting
  - Clarity (10 points): Readability and shareability
```

## Winner's Challenge Mechanism

When a new skill is added:

1. Run `scan` to identify its category
2. Run `test --new [skill_id]` to test only the new skill
3. If it scores higher than the current winner, it becomes the new winner
4. Results are logged in `winners.json` with challenge history

## Environment Variables

For LLM-based testing, set these environment variables:

```bash
# Anthropic (default)
export ANTHROPIC_API_KEY=sk-ant-...

# OpenAI (alternative)
export OPENAI_API_KEY=sk-...

# Google (alternative)
export GOOGLE_API_KEY=...
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Skill Arena Pipeline                      │
├─────────────────────────────────────────────────────────────┤
│  1. Scan → 2. Cluster → 3. Expert Design → 4. Execute       │
│       ↓              ↓              ↓              ↓         │
│   297 skills    17 categories   85 tests    Parallel/LLM    │
│                                                              │
│  5. Score → 6. Rank → 7. Report → 8. Update index.json      │
│       ↓           ↓           ↓            ↓                 │
│   3 dimensions  Leaderboard  Markdown    arena.* fields     │
└─────────────────────────────────────────────────────────────┘
```

## Files Reference

| File | Purpose |
|------|---------|
| `skill-arena.py` | Main entry point |
| `cluster_skills.py` | Skill scanning and clustering |
| `expert_panels.py` | 60+ expert definitions |
| `expert_collaboration.py` | Expert roundtable simulation |
| `design_tests.py` | Test case generation |
| `run_benchmarks.py` | Test execution (simulated or LLM) |
| `llm_invoker.py` | LLM skill invocation |
| `llm_judge.py` | LLM-based quality evaluation |
| `score_results.py` | Scoring and ranking |
| `generate_report.py` | Report generation |
| `update_index.py` | index.json updates |
