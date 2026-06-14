# Migration Guide

> 版本升级与迁移指南

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### Version History

| Version | Date | Key Changes |
|---------|------|-------------|
| 2.1.0 | Current | Clusters, hierarchy, related clusters |
| 2.0.0 | 2024-Q4 | Arena scoring, winners system |
| 1.x | Legacy | Basic skill index |

---

### Upgrading to 2.1.0

#### New Features
- Cluster metadata with `triggers`, `suitable_for`, `not_suitable_for`
- Category hierarchy (`--hierarchy`)
- Related clusters (`--related`)
- Enhanced fuzzy search

#### Breaking Changes
None. Fully backward compatible.

#### Migration Steps

```bash
# 1. Pull latest code
git pull origin main

# 2. Update submodules
git submodule update --init --recursive

# 3. Rebuild index (picks up new fields)
python3 scripts/arena_scan.py && \
python3 scripts/arena_cluster_score.py && \
python3 scripts/arena_build_index.py

# 4. Verify
python3 devops/ultraskills-hub/scripts/search.py --hierarchy
```

---

### Upgrading from 1.x to 2.0

#### Breaking Changes

1. **Index structure changed**
   - Old: `{"skills": [...]}`
   - New: `{"version": "2.0", "skills": [...], "clusters": [...], "hierarchy": {...}}`

2. **Arena fields added**
   - Each skill now has `arena: {score, rank, is_winner, category, scores: {...}}`

3. **Path format normalized**
   - Old: Mixed relative/absolute paths
   - New: All paths relative to repo root, prefixed with `./`

#### Migration Steps

```bash
# 1. Backup existing index
cp index.json index.json.backup

# 2. Pull latest scripts
git pull origin main

# 3. Full rebuild
python3 scripts/arena_scan.py && \
python3 scripts/arena_cluster_score.py && \
python3 scripts/arena_build_index.py

# 4. Verify structure
python3 -c "
import json
with open('index.json') as f:
    data = json.load(f)
assert 'version' in data or 'meta' in data, 'Missing version'
assert 'skills' in data, 'Missing skills'
assert len(data['skills']) > 0, 'Empty skills'
print(f'✅ Valid index: {len(data[\"skills\"])} skills')
"
```

---

### SKILL.md Format Changes

#### Version 2.0+ Required Fields

```yaml
---
name: Skill Name           # Required
description: One liner     # Required
version: 1.0.0            # Required (skill version, not index)
tags: [tag1, tag2]        # Required (at least 1)
---
```

#### Version 2.1+ Optional Fields

```yaml
---
name: Skill Name
description: One liner
version: 1.0.0
tags: [tag1, tag2]
recommended_for: [use-case-1, use-case-2]  # New in 2.1
triggers: [keyword1, keyword2]              # New in 2.1 (search triggers)
---
```

#### Migrating Old SKILL.md

```bash
# Find skills missing required fields
python3 devops/skill-manager/scripts/scan_and_check.py --health community/

# Output shows which skills need updating
```

**Common fixes:**

```yaml
# ❌ Old format (missing frontmatter)
# My Skill
Does something useful.

# ✅ New format
---
name: My Skill
description: Does something useful
version: 1.0.0
tags: [utility]
---

# My Skill
Does something useful.
```

---

### External Skills (Submodules)

#### Updating Submodules

```bash
# Update all submodules to latest
git submodule update --remote --merge

# Then rebuild index
python3 scripts/arena_scan.py && \
python3 scripts/arena_cluster_score.py && \
python3 scripts/arena_build_index.py
```

#### Handling Submodule Conflicts

```bash
# If submodule is in detached HEAD state
cd external/broken-submodule
git checkout main
git pull
cd ../..

# Re-record submodule state
git add external/broken-submodule
git commit -m "Update broken-submodule"
```

#### Adding `github_url` and `github_hash`

External skills need tracking metadata:

```yaml
---
name: External Skill
description: From GitHub
version: 1.0.0
tags: [external]
github_url: https://github.com/org/repo
github_hash: abc1234def5678  # Commit hash at time of import
---
```

**Add automatically:**

```bash
# Use github-to-skills skill
python3 devops/github-to-skills/scripts/create_github_skill.py https://github.com/org/repo
```

---

### Deployment Migration

#### From Manual Copy to deploy_skills.py

**Old method (deprecated):**
```bash
cp -r community/* ~/.claude/skills/
```

**New method:**
```bash
# Hub only
python3 scripts/deploy_skills.py deploy

# Hub + winners
python3 scripts/deploy_skills.py deploy --winners

# All skills
python3 scripts/deploy_skills.py deploy --all

# Check status
python3 scripts/deploy_skills.py status
```

#### Cleaning Up Old Deployments

```bash
# Remove all manually copied skills
rm -rf ~/.claude/skills/*

# Redeploy with new system
python3 scripts/deploy_skills.py deploy --winners
```

---

### Index Format Reference

#### Version 2.1.0 Structure

```json
{
  "version": "2.1.0",
  "meta": {
    "generated": "2024-01-15T10:30:00Z",
    "skill_count": 619,
    "cluster_count": 54
  },
  "skills": [
    {
      "id": "skill-name",
      "path": "./community/skill-name",
      "description": "What it does",
      "tags": ["tag1", "tag2"],
      "recommended_for": ["use-case"],
      "arena": {
        "score": 8.5,
        "rank": 3,
        "is_winner": false,
        "category": "engineering-code-quality",
        "cluster": "engineering-code-quality",
        "scores": {
          "speed": 8.0,
          "quality": 9.0,
          "maintainability": 8.5
        }
      }
    }
  ],
  "clusters": [
    {
      "id": "engineering-code-quality",
      "name": "工程·代码质量",
      "description": "Code review and quality tools",
      "skill_count": 30,
      "winner": "receiving-code-review",
      "triggers": ["review", "lint", "quality"],
      "parent": "engineering",
      "related": ["engineering-testing", "engineering-architecture"],
      "suitable_for": ["code review", "PR checks"],
      "not_suitable_for": ["writing new code"]
    }
  ],
  "hierarchy": {
    "root": ["engineering", "content", "business", "agent"],
    "engineering": ["engineering-code-quality", "engineering-architecture", ...],
    "content": ["content-video", "content-writing", ...]
  }
}
```

---

### Backward Compatibility

#### Reading Old Index

Scripts gracefully handle missing fields:

```python
# Safe access patterns used in search.py
arena = skill.get("arena", {})
score = arena.get("score", 0)
is_winner = arena.get("is_winner", False)
```

#### Writing Compatible Skills

Skills work with all index versions if they have:

```yaml
---
name: Required
description: Required
version: 1.0.0
tags: [at-least-one]
---
```

Additional fields are silently ignored by older parsers.

---

### Rollback Procedures

#### Rollback Index

```bash
# Restore from backup
cp index.json.backup index.json

# Or restore from git
git checkout HEAD~1 -- index.json
```

#### Rollback Deployment

```bash
# Clear current deployment
rm -rf ~/.claude/skills/*

# Checkout older version
git checkout v2.0.0

# Redeploy
python3 scripts/deploy_skills.py deploy --winners
```

#### Rollback Submodule

```bash
cd external/problematic-submodule
git checkout <previous-commit-hash>
cd ../..
git add external/problematic-submodule
git commit -m "Rollback submodule to stable version"
```

---

<a name="中文"></a>
## 中文

### 版本历史

| 版本 | 关键变更 |
|------|----------|
| 2.1.0 | 分类层级、相关分类、触发词 |
| 2.0.0 | Arena 评分系统、冠军机制 |
| 1.x | 基础技能索引 |

---

### 升级到 2.1.0

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 更新子模块
git submodule update --init --recursive

# 3. 重建索引
python3 scripts/arena_scan.py && \
python3 scripts/arena_cluster_score.py && \
python3 scripts/arena_build_index.py

# 4. 验证
python3 devops/ultraskills-hub/scripts/search.py --hierarchy
```

---

### 从 1.x 升级到 2.0

#### 破坏性变更

1. 索引结构变化（新增 version、clusters、hierarchy）
2. 每个技能新增 arena 字段
3. 路径格式统一为相对路径

#### 迁移步骤

```bash
cp index.json index.json.backup
git pull origin main
python3 scripts/arena_scan.py && \
python3 scripts/arena_cluster_score.py && \
python3 scripts/arena_build_index.py
```

---

### SKILL.md 格式变更

#### 必需字段（2.0+）

```yaml
---
name: 技能名称
description: 一句话描述
version: 1.0.0
tags: [标签1, 标签2]
---
```

#### 新增可选字段（2.1+）

```yaml
recommended_for: [使用场景1, 使用场景2]
triggers: [触发词1, 触发词2]
```

---

### 部署迁移

#### 旧方式（废弃）
```bash
cp -r community/* ~/.claude/skills/
```

#### 新方式
```bash
python3 scripts/deploy_skills.py deploy --winners
```

---

### 回滚

```bash
# 回滚索引
git checkout HEAD~1 -- index.json

# 回滚部署
rm -rf ~/.claude/skills/*
git checkout v2.0.0
python3 scripts/deploy_skills.py deploy --winners
```
