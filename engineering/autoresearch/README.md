# Autoresearch: Universal Task Optimization Framework

Transform any measurable, iterable task into a self-improving system through conversational design and intelligent optimization loops.

## Quick Start

```
User: "I want to optimize my image segmentation model"

→ System guides you through configuration
→ Generates task_config.yaml
→ Runs autonomous optimization overnight
→ Wake up to improved system + full experiment log
```

## Features

- 🎯 **Conversational Design**: Describe your task in natural language
- 🔄 **Autonomous Loops**: Runs indefinitely until goals met
- 📊 **Multi-Objective**: Balance competing metrics intelligently
- 🛡️ **Global Progress**: Avoids local optimization traps
- 💾 **Auto-Fallback**: SQLite → files, adapts to your environment

## Architecture

```
autoresearch (main skill)
├── design    - Conversational task configuration
├── execute   - Single experiment runner
├── optimize  - Autonomous optimization loop
└── analyze   - Experiment analysis & insights
```

## Usage

### Automatic Mode
```
"Help me optimize [your task]"
→ System handles everything
```

### Manual Mode
```
"autoresearch:design - configure new task"
"autoresearch:optimize - start optimization"
"autoresearch:analyze - show results"
```

## Strategy Templates

- **git_based**: Code optimization with git versioning
- **config_snapshot**: Config tuning without git
- **multi_objective**: Balance multiple metrics (pareto optimization)
- **bandit**: Large search space exploration (UCB)

## Examples

See `examples/` for:
- LLM training optimization
- Image segmentation tuning
- System performance optimization

## Documentation

- See individual `SKILL.md` files in each subdirectory
- Full design doc: `/docs/plans/2026-04-07-autoresearch-meta-framework-design.md`

## Installation

No installation needed - just a Claude Code skill!

Dependencies handled automatically:
- SQLite (built-in Python) or file-based fallback
- All other features use standard library

## License

MIT
