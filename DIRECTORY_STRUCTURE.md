# UltraSkills Directory Structure Guide

> Auto-generated: 2026-05-08

## Overview

```
ultraskills/
├── 📦 Core Files
│   ├── index.json              # Master index (619 skills + arena scores)
│   ├── SKILLS_INDEX.md         # Human-readable category index
│   ├── setup.sh                # Installation script
│   └── package.json            # Node.js CLI config
│
├── 🏗️ Infrastructure
│   ├── bin/                    # CLI entry points
│   ├── lib/                    # Core Node.js modules
│   ├── scripts/                # Arena pipeline (Python)
│   └── skill-arena/            # Arena data (JSON files)
│
├── 📚 Skill Collections
│   ├── community/              # Community skills (162)
│   ├── external/               # External submodules (440)
│   ├── engineering/            # Engineering patterns (5)
│   ├── productivity/           # Productivity tools (1)
│   ├── devops/                 # DevOps & management (11)
│   └── meta/                   # Meta-skills (1)
│
├── 📖 Documentation
│   ├── docs/                   # Project docs
│   ├── CLAUDE.md               # Claude Code instructions
│   ├── CONTRIBUTING.md         # Contribution guide
│   └── README.md               # Project README
│
└── 🧪 Development
    ├── test/                   # Test suites
    ├── _template_skill/        # Skill template
    └── auth/                   # Authentication (if needed)
```

## Skill Categories (by Arena Cluster)

See [SKILLS_INDEX.md](./SKILLS_INDEX.md) for full categorization by:
- **Agent Skills**: 架构, 评估, 上下文管理, 工作流, 记忆系统...
- **Engineering Skills**: ML/AI, 代码质量, 测试, 架构...
- **Content Skills**: 演示设计, 文档生成, 视频, 图像设计...
- **Business Skills**: 项目管理, 高管顾问, 人力资源...
- **Media Skills**: 语音音频, 图像处理...
- **Design Skills**: UX/产品设计...
- **Skills Management**: 管理工具...

## Path Conventions

All skill paths follow this format:

```
./[category]/[skill-name]/SKILL.md
./[category]/[skill-name]/[subskill]/SKILL.md  (for nested skills)
```

**Examples**:
- `./community/visual-forge/SKILL.md`
- `./external/claude-code/plugins/plugin-dev/skills/skill-development/SKILL.md`
- `./devops/ultraskills-hub/SKILL.md`

## Virtual vs Physical Structure

**Physical Structure** (directories):
- Optimized for git submodule management
- Most skills in `community/` and `external/`
- Keeps external sources isolated

**Virtual Structure** (arena clusters):
- Semantic categorization by functionality
- 54 clusters (Agent, Engineering, Content, Business, etc.)
- See `index.json` → `arena.cluster_name` field

## Adding New Skills

1. **Choose physical location**:
   - Community contribution → `community/[skill-name]/`
   - External source → `external/[source-name]/`
   - Internal tool → `devops/[tool-name]/`

2. **Create structure**:
   ```bash
   cp -r _template_skill/ [category]/[skill-name]/
   # Edit SKILL.md frontmatter + content
   ```

3. **Rebuild index**:
   ```bash
   python3 scripts/arena_scan.py && \
   python3 scripts/arena_cluster_score.py && \
   python3 scripts/arena_build_index.py
   ```

4. **Verify categorization**:
   ```bash
   grep '"id": "[skill-name]"' index.json -A 15
   ```

## Arena Data Flow

```
SKILL.md files (all directories)
    ↓ arena_scan.py
skill-arena/skills_inventory.json
    ↓ arena_cluster_score.py
skill-arena/{clusters, scores, winners}.json
    ↓ arena_build_index.py
index.json (master index)
    ↓ (manual trigger)
SKILLS_INDEX.md (human-readable)
```

## Statistics

| Metric | Value |
|--------|-------|
| Total Skills | 619 |
| Total Clusters | 54 |
| Avg Arena Score | 7.33/10 |
| External Skills | 440 (71%) |
| Community Skills | 162 (26%) |
| DevOps/Internal | 17 (3%) |

**Last Updated**: 2026-05-08

---

For detailed skill listings by category, see [SKILLS_INDEX.md](./SKILLS_INDEX.md)
