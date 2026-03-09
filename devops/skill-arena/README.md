# Skill Arena - Usage Guide

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
| `test` | Run PK tests for each cluster |
| `score` | Calculate weighted scores and rankings |
| `report` | Generate markdown benchmark report |
| `update` | Update index.json with arena data |
| `full` | Run complete pipeline |
| `backtrack` | Re-test all skills with updated test cases |

## Output Files

After running `full` pipeline:

```
devops/skill-arena/
├── clusters.json           # Cluster assignments
├── winners.json            # Category winners
├── reports/
│   ├── raw-results.json    # Raw test execution results
│   ├── rankings.json       # Scored rankings
│   └── benchmark-report-YYYY-MM-DD.md  # Human-readable report
└── test-suites/
    ├── cro/tests.yaml      # Test cases for CRO category
    ├── seo/tests.yaml      # Test cases for SEO category
    └── ...
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

## Scoring Formula

```
Total = (Speed × 0.30) + (Quality × 0.50) + (Maintainability × 0.20)

Speed:        Based on response time (faster = higher score)
Quality:      LLM-evaluated output quality + task completion
Maintainability: Code structure, documentation, test coverage
```

## Winner's Challenge Mechanism

When a new skill is added:

1. Run `scan` to identify its category
2. Run `test --new [skill_id]` to test only the new skill
3. If it scores higher than the current winner, it becomes the new winner
4. Results are logged in `winners.json` with challenge history

## Production Deployment

For production use:

1. **Implement actual skill invocation** in `run_benchmarks.py`
2. **Set up LLM judge** for quality evaluation
3. **Configure parallel execution** with rate limiting
4. **Enable result persistence** to database
5. **Set up CI/CD** to run tests on skill changes

```bash
# Example: Run with production settings
python devops/skill-arena/scripts/skill-arena.py full \
  --parallel 8 \
  --judge-model gpt-4 \
  --output-dir results/
```
