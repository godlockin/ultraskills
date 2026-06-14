# Search API Reference

> `devops/ultraskills-hub/scripts/search.py` 完整参数文档

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

### Overview

The search API provides keyword search, tag filtering, cluster browsing, and skill comparison capabilities for the UltraSkills library.

**Location:** `devops/ultraskills-hub/scripts/search.py`

**Data Source:** `index.json` (root directory)

---

### Command Reference

#### 1. Keyword Search (Default)

```bash
python3 devops/ultraskills-hub/scripts/search.py <query terms...>
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query terms` | string(s) | Yes | One or more search keywords |

**Scoring Algorithm:**
| Match Type | Points | Description |
|------------|--------|-------------|
| Exact ID match | +20 | Keyword equals skill ID |
| Partial ID match | +5 | Keyword contained in skill ID |
| Tag match | +6 | Keyword found in tags |
| Recommended-for match | +5 | Keyword in recommended_for field |
| Description hit | +2 each | Each occurrence in description |
| Fuzzy match (Levenshtein ≤2) | +8 | When no exact match found |
| Arena winner bonus | +15 | If skill is cluster winner (requires score ≥10) |
| Arena score bonus | +0-10 | `arena_score × 0.10` |
| Quality dimension | +0-1.5 | `quality × 0.15` |
| Maintainability dimension | +0-1.0 | `maintainability × 0.10` |
| Category match | +4 | Query matches arena category |

**Chinese Support:**
- Automatic bigram tokenization for Chinese text
- Characters split into overlapping pairs: `视频剪辑` → `视频`, `频剪`, `剪辑`

**Example:**
```bash
# English search
python3 devops/ultraskills-hub/scripts/search.py "code review"

# Chinese search
python3 devops/ultraskills-hub/scripts/search.py "视频剪辑"

# Multi-term search
python3 devops/ultraskills-hub/scripts/search.py react component testing
```

**Output (JSON array):**
```json
[
  {
    "id": "receiving-code-review",
    "path": "/path/to/skill",
    "description": "Handle code review feedback effectively",
    "tags": ["engineering", "review"],
    "arena_score": 9.2,
    "arena_rank": 1,
    "arena_category": "engineering-code-quality",
    "quality_score": 8.5,
    "is_winner": true,
    "winner_reason": "#1 in engineering-code-quality category, arena score 9.2",
    "match_score": 42.5
  }
]
```

**No Results Handling:**
Returns fuzzy suggestions via `did_you_mean`:
```json
{
  "results": [],
  "did_you_mean": ["react-expert", "react-native-expert", "remotion"]
}
```

---

#### 2. Tag Filter

```bash
python3 devops/ultraskills-hub/scripts/search.py --tag <tag>
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tag` | string | Yes | Exact tag name to filter by |

**Example:**
```bash
python3 devops/ultraskills-hub/scripts/search.py --tag video
```

**Returns:** Up to 30 skills with the specified tag, sorted by arena score.

---

#### 3. List All Tags

```bash
python3 devops/ultraskills-hub/scripts/search.py --list-tags
```

**Returns:** Sorted JSON array of all unique tags in the index.

```json
["agent", "ai", "architecture", "browser", "code-review", ...]
```

---

#### 4. Exact ID Lookup

```bash
python3 devops/ultraskills-hub/scripts/search.py --id <skill-id>
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skill-id` | string | Yes | Exact or partial skill ID |

**Behavior:**
- Exact match: Returns single skill with path
- Partial match (single): Returns that skill
- Partial match (multiple): Returns up to 5 candidates

**Example:**
```bash
python3 devops/ultraskills-hub/scripts/search.py --id remotion
```

**Output:**
```json
{"id": "remotion", "path": "/path/to/ultraskills/com/remotion"}
```

---

#### 5. Winners Only

```bash
python3 devops/ultraskills-hub/scripts/search.py --winners
```

**Returns:** Up to 50 arena winners, sorted by match score.

---

#### 6. Compare Skills

```bash
python3 devops/ultraskills-hub/scripts/search.py --compare <skill-a> <skill-b>
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `skill-a` | string | Yes | First skill ID |
| `skill-b` | string | Yes | Second skill ID |

**Example:**
```bash
python3 devops/ultraskills-hub/scripts/search.py --compare remotion video-analyzer
```

**Output:**
```json
{
  "skill_a": {
    "id": "remotion",
    "description": "Programmatic video editing with React",
    "path": "/path/to/skill",
    "total": 9.7,
    "speed": 8.5,
    "quality": 9.5,
    "maintainability": 9.2,
    "is_winner": true,
    "rank": 1,
    "category": "content-video"
  },
  "skill_b": { ... },
  "winner": "remotion",
  "dimension_winners": {
    "speed": "remotion",
    "quality": "remotion",
    "maintainability": "remotion",
    "total": "remotion"
  },
  "score_delta": 1.2
}
```

---

#### 7. List Clusters

```bash
python3 devops/ultraskills-hub/scripts/search.py --clusters
```

**Returns:** All clusters with metadata, sorted by skill count.

```json
[
  {
    "id": "engineering-code-quality",
    "name": "工程·代码质量",
    "skill_count": 30,
    "winner": "receiving-code-review",
    "description": "Code review, linting, quality metrics",
    "triggers": ["review", "lint", "quality"],
    "parent": "engineering"
  }
]
```

---

#### 8. Skills in Cluster

```bash
python3 devops/ultraskills-hub/scripts/search.py --cluster <cluster-id>
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `cluster-id` | string | Yes | Cluster ID (case-insensitive) |

**Example:**
```bash
python3 devops/ultraskills-hub/scripts/search.py --cluster content-video
```

**Returns:** Skills in the cluster, sorted by rank.

---

#### 9. Category Hierarchy

```bash
python3 devops/ultraskills-hub/scripts/search.py --hierarchy
```

**Returns:** Two-level category tree with skill counts.

```json
[
  {
    "id": "engineering",
    "name": "Engineering",
    "total_skills": 114,
    "cluster_count": 12,
    "children": [
      {"id": "engineering-code-quality", "name": "代码质量", "skill_count": 30, "winner": "receiving-code-review"},
      ...
    ]
  }
]
```

---

#### 10. Related Clusters

```bash
python3 devops/ultraskills-hub/scripts/search.py --related <cluster-id>
```

**Returns:** Parent cluster, related clusters, and suitability hints.

```json
{
  "cluster": {"id": "content-video", "name": "内容·视频", "description": "..."},
  "parent": {"id": "content"},
  "related": [
    {"id": "content-social-media", "name": "社交媒体", "skill_count": 24}
  ],
  "suitable_for": ["video editing", "content creation"],
  "not_suitable_for": ["audio-only tasks"]
}
```

---

### Return Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (index not found, corrupted, or validation failed) |

### Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `index.json not found` | Missing index file | Run arena pipeline |
| `index.json is corrupted` | Invalid JSON or missing keys | Run `python3 scripts/arena_scan.py && python3 scripts/arena_cluster_score.py && python3 scripts/arena_build_index.py` |
| `skill not found` | ID doesn't exist | Check spelling or use `--list-tags` |
| `cluster not found` | Invalid cluster ID | Use `--clusters` to list valid IDs |

---

<a name="中文"></a>
## 中文

### 概述

搜索 API 提供关键词搜索、标签过滤、分类浏览和技能对比功能。

**位置:** `devops/ultraskills-hub/scripts/search.py`

**数据源:** `index.json`（根目录）

---

### 命令速查

| 命令 | 说明 |
|------|------|
| `search.py <关键词>` | 关键词搜索（默认） |
| `search.py --tag <标签>` | 按标签过滤 |
| `search.py --list-tags` | 列出所有标签 |
| `search.py --id <skill-id>` | 精确 ID 查找 |
| `search.py --winners` | 仅显示 Arena 冠军 |
| `search.py --compare <a> <b>` | 技能对比 |
| `search.py --clusters` | 列出所有分类 |
| `search.py --cluster <id>` | 查看分类下的技能 |
| `search.py --hierarchy` | 分类层级树 |
| `search.py --related <id>` | 相关分类 |

---

### 评分算法

| 匹配类型 | 分数 | 说明 |
|----------|------|------|
| ID 精确匹配 | +20 | 关键词 = skill ID |
| ID 部分匹配 | +5 | 关键词包含在 ID 中 |
| 标签匹配 | +6 | 关键词在 tags 中 |
| 推荐场景匹配 | +5 | 关键词在 recommended_for 中 |
| 描述命中 | +2/次 | 每次出现在 description 中 |
| 模糊匹配 | +8 | Levenshtein 距离 ≤2 |
| Arena 冠军加成 | +15 | 分类冠军（需基础分 ≥10） |
| Arena 分数加成 | +0-10 | `arena_score × 0.10` |

---

### 中文搜索支持

自动双字符切分（bigram）：
- `视频剪辑` → `视频` + `频剪` + `剪辑`
- 提高中文描述匹配率

**示例:**
```bash
python3 devops/ultraskills-hub/scripts/search.py "代码审查"
python3 devops/ultraskills-hub/scripts/search.py "视频编辑"
```

---

### 输出格式

所有输出均为 JSON 格式，包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 技能 ID |
| `path` | string | 绝对路径 |
| `description` | string | 描述 |
| `tags` | array | 标签列表 |
| `arena_score` | float | Arena 评分 (0-10) |
| `arena_rank` | int | 分类内排名 |
| `arena_category` | string | 所属分类 |
| `is_winner` | bool | 是否分类冠军 |
| `match_score` | float | 搜索匹配分 |

---

### 错误处理

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `index.json not found` | 索引文件缺失 | 运行 arena pipeline |
| `index.json is corrupted` | JSON 格式错误 | 重建索引 |
| `skill not found` | ID 不存在 | 检查拼写 |
| `cluster not found` | 分类 ID 无效 | 用 `--clusters` 查看有效 ID |

**重建索引命令:**
```bash
python3 scripts/arena_scan.py && \
python3 scripts/arena_cluster_score.py && \
python3 scripts/arena_build_index.py
```
