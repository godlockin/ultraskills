# Performance Optimization Guide

> 大规模 skill 部署性能优化建议

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### Overview

UltraSkills contains 600+ skills. Understanding context overhead and deployment strategies is critical for optimal Claude Code performance.

---

### Context Window Impact

#### How Skills Consume Context

When Claude Code starts, it loads skills from `~/.claude/skills/`:

| Deploy Mode | Skills Loaded | Est. Context Tokens | Startup Impact |
|-------------|---------------|---------------------|----------------|
| Hub only | 1 | ~500 | Minimal |
| Hub + Winners | 70 | ~35K | Moderate |
| All skills | 600+ | ~300K+ | **Heavy** |

**Rule of thumb:** Each skill consumes 300-800 tokens of context window.

#### Context Budget

Claude's context window is shared between:
- System prompt + skills
- Conversation history
- Tool outputs

**Recommendation:** Keep startup skills under 100 to preserve context for actual work.

---

### Deployment Strategies

#### Strategy 1: Hub-Only (Recommended)

```bash
python3 scripts/deploy_skills.py deploy
```

**How it works:**
1. Only `ultraskills-hub` loaded at startup (~500 tokens)
2. Search for skills on-demand
3. Load specific skill when needed via `Skill("skill-name")`

**Pros:**
- Minimal startup overhead
- Maximum context for conversation
- 600+ skills accessible via search

**Cons:**
- Extra step to find/load skills
- Search adds latency

**Best for:** General usage, context-heavy tasks, long conversations.

---

#### Strategy 2: Hub + Winners

```bash
python3 scripts/deploy_skills.py deploy --winners
```

**What's included:**
- ultraskills-hub (search)
- 66 arena winners (top skill per category)
- 3 essential dependencies

**Token cost:** ~35K tokens at startup

**Pros:**
- Best-in-class skills pre-loaded
- Instant access to top skills
- Still searchable for non-winners

**Best for:** Most users, balanced performance.

---

#### Strategy 3: All Skills

```bash
python3 scripts/deploy_skills.py deploy --all
```

**Token cost:** ~300K+ tokens

**Pros:**
- Everything immediately available
- No search needed

**Cons:**
- **Significant context overhead**
- Slower startup
- Less room for conversation

**Best for:** Short sessions, skill browsing, testing.

---

### Caching Mechanisms

#### Index Cache

The search engine loads `index.json` once per Python process:

```python
# search.py caches index in memory
def load_index():
    # Loads once, reused for all searches in same process
```

**Optimization:** For scripts making multiple searches, reuse the process:

```bash
# ❌ Slow: spawns new process each time
for term in video audio image; do
  python3 devops/ultraskills-hub/scripts/search.py "$term"
done

# ✅ Fast: single process, index loaded once
python3 -c "
import sys
sys.path.insert(0, 'devops/ultraskills-hub/scripts')
from search import load_index, search
idx = load_index()
for term in ['video', 'audio', 'image']:
    print(search(idx, [term]))
"
```

#### Skill File Cache

Claude Code caches loaded skill content. No action needed.

---

### Index Optimization

#### Reduce Index Size

The full `index.json` includes all metadata (~2MB). For production:

```bash
# Create minimal index (IDs + paths only)
python3 -c "
import json
with open('index.json') as f:
    data = json.load(f)
minimal = {
    'version': data.get('version', '2.0'),
    'skills': [
        {'id': s['id'], 'path': s['path'], 'description': s.get('description', '')[:50]}
        for s in data['skills']
    ]
}
with open('index.minimal.json', 'w') as f:
    json.dump(minimal, f)
"
```

#### Lazy Cluster Loading

For UIs/tools that browse clusters:

```python
# Load clusters separately, not full index
clusters = index.get("clusters", [])
# Only fetch full skill list when user drills into cluster
```

---

### Search Performance

#### Query Optimization

| Query Type | Performance | Tip |
|------------|-------------|-----|
| Single keyword | Fast | Best approach |
| Multiple keywords | Fast | Terms AND'd together |
| Chinese text | Moderate | Bigram tokenization adds overhead |
| Fuzzy match | Slow | Only runs when 0 exact matches |

**Best practices:**

```bash
# ✅ Fast: single keyword
python3 devops/ultraskills-hub/scripts/search.py video

# ✅ Fast: multiple specific terms
python3 devops/ultraskills-hub/scripts/search.py react component

# ⚠️ Slower: very broad terms matching many skills
python3 devops/ultraskills-hub/scripts/search.py code

# ❌ Avoid: full sentences
python3 devops/ultraskills-hub/scripts/search.py "how to edit videos programmatically"
```

#### Limit Results

Default limit is 8. Override for browsing:

```python
# In code, not CLI
results = search(idx, ["video"], limit=50)  # More results but slower sort
```

---

### Skill Loading Patterns

#### On-Demand Loading

```
User: "I need to edit a video"
Claude: [searches hub] → finds remotion → Skill("remotion")
```

**Context cost:** ~500 tokens (hub) + ~800 tokens (remotion) = 1300 total

#### Pre-Loading for Workflows

If you know you'll use specific skills, pre-deploy them:

```bash
# Deploy only what you need
cp -r community/remotion ~/.claude/skills/
cp -r community/video-analyzer ~/.claude/skills/
```

#### Dynamic Skill Rotation

For long sessions, consider:

1. Start with hub-only
2. Load skills as needed
3. Conversation compaction naturally prioritizes recent context

---

### Memory & Disk

#### Index File Sizes

| File | Size | Notes |
|------|------|-------|
| `index.json` | ~2MB | Full metadata |
| `skills_inventory.json` | ~1MB | Scan output |
| `clusters.json` | ~50KB | Clustering |
| `scores.json` | ~200KB | Scoring |

#### Disk Usage per Skill

Average skill directory: 5-50KB (SKILL.md + examples)

Total `~/.claude/skills/` with all skills: ~30-50MB

---

### Benchmarks

#### Search Performance (M1 Mac)

| Operation | Time |
|-----------|------|
| Load index | 50-100ms |
| Single keyword search | 10-30ms |
| Chinese search (with bigrams) | 30-50ms |
| Fuzzy search fallback | 100-200ms |
| `--clusters` listing | 20-40ms |
| `--hierarchy` tree | 30-50ms |

#### Arena Pipeline (M1 Mac)

| Step | Time (600 skills) |
|------|-------------------|
| arena_scan.py | 5-10s |
| arena_cluster_score.py | 3-5s |
| arena_build_index.py | 1-2s |
| **Total** | ~15s |

---

### Recommendations by Use Case

| Use Case | Deploy Mode | Est. Tokens |
|----------|-------------|-------------|
| General coding | Hub + Winners | ~35K |
| Long conversations | Hub only | ~500 |
| Skill development | Hub + Winners | ~35K |
| Quick task | All skills | ~300K |
| CI/CD integration | Hub only | ~500 |
| Browsing/testing | All skills | ~300K |

---

<a name="中文"></a>
## 中文

### 概述

UltraSkills 包含 600+ 技能。理解 context 开销和部署策略对 Claude Code 性能至关重要。

---

### Context 开销

| 部署模式 | 加载技能数 | 预估 Token | 启动影响 |
|----------|------------|------------|----------|
| 仅 Hub | 1 | ~500 | 极小 |
| Hub + 冠军 | 70 | ~35K | 中等 |
| 全部技能 | 600+ | ~300K+ | **很大** |

**经验法则:** 每个技能消耗 300-800 tokens。

---

### 部署策略

#### 策略一：仅 Hub（推荐）

```bash
python3 scripts/deploy_skills.py deploy
```

- 启动仅加载 hub (~500 tokens)
- 按需搜索、按需加载
- 适合：通用场景、长对话

#### 策略二：Hub + 冠军

```bash
python3 scripts/deploy_skills.py deploy --winners
```

- 加载 66 个分类冠

```bash
python3 scripts/deploy_skills.py deploy --all
```

- Token 开销 ~300K+
- 适合：短会话、技能浏览

---

### 搜索优化

| 查询类型 | 性能 | 建议 |
|----------|------|------|
| 单关键词 | 快 | 最佳 |
| 多关键词 | 快 | AND 组合 |
| 中文 | 中等 | bigram 切分增加开销 |
| 模糊匹配 | 慢 | 仅无精确匹配时触发 |

**最佳实践:**
```bash
# ✅ 快：单关键词
python3 devops/ultraskills-hub/scripts/search.py video

# ❌ 避免：完整句子
python3 devops/ultraskills-hub/scripts/search.py "如何用代码编辑视频"
```

---

### 性能基准（M1 Mac）

| 操作 | 耗时 |
|------|------|
| 加载索引 | 50-100ms |
| 单词搜索 | 10-30ms |
| 中文搜索 | 30-50ms |
| Arena 全流程 | ~15s |

---

### 场景推荐

| 场景 | 部署模式 | Token 估算 |
|------|----------|------------|
| 日常编程 | Hub + 冠军 | ~35K |
| 长对话 | 仅 Hub | ~500 |
| 快速任务 | 全部技能 | ~300K |
| CI/CD 集成 | 仅 Hub | ~500 |
