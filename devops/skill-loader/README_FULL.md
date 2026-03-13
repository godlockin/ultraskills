# Skill Loader - 高效动态加载系统

> 为 UltraSkills 项目提供高效的 Skills 索引、缓存、搜索和路由服务

## 特性

| 特性 | 描述 | 性能 |
|------|------|------|
| 🗄️ **双层缓存** | 内存缓存 + 磁盘缓存 | 查询 <10ms |
| 🔄 **增量更新** | 文件监听，自动更新 | O(1) 变化处理 |
| 🔍 **语义搜索** | 关键词 + 类别 + 任务类型匹配 | 智能排序 |
| 🎯 **智能路由** | 根据任务复杂度推荐技能 | 多技能组合 |
| 🔌 **MCP 集成** | 标准 MCP 协议接口 | 无缝集成 |

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    User / Claude Code                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   MCP Server Interface                       │
│  Tools: list_skills, search_skills, get_skill, route        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Skill Router Layer                         │
│  - Keyword Matcher (倒排索引)                                │
│  - Task Type Detector (任务类型识别)                         │
│  - Composition Recommender (技能组合推荐)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                Skill Index Cache Layer                       │
│  - Memory Cache (运行时)                                     │
│  - Disk Cache (JSON 持久化)                                  │
│  - File Watcher (watchdog)                                   │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  File System Skills                          │
│  engineering/ productivity/ devops/ creative/ community/     │
└─────────────────────────────────────────────────────────────┘
```

## 安装

### 1. 安装依赖

```bash
cd devops/skill-loader
pip install -r requirements.txt
```

### 2. 构建初始索引

```bash
python cli.py rebuild
```

### 3. 配置 MCP Server

在 Claude Code 的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "skills": {
      "command": "python",
      "args": ["/absolute/path/to/devops/skill-loader/mcp_server.py"],
      "cwd": "/absolute/path/to/devops/skill-loader"
    }
  }
}
```

## 使用方法

### CLI 命令

```bash
# 重建索引
python cli.py rebuild

# 搜索技能
python cli.py search --query "video processing"

# 路由任务（智能推荐）
python cli.py route --query "fix the bug in login flow"

# 查看统计
python cli.py stats

# 监控文件变化
python cli.py watch

# 启动 MCP Server
python cli.py serve
```

### Python API

```python
from skill_loader import get_cache, get_router

# 获取缓存
cache = get_cache()

# 搜索
results = cache.search("tdd", top_n=5)

# 获取路由推荐
router = get_router()
result = router.route("I need to fix a bug and add tests")

print(result['primary_skill'])  # 主推荐技能
print(result['composition'])    # 技能组合建议
print(result['suggested_workflow'])  # 工作流程建议
```

### MCP 工具调用

```
# 列出所有技能
/list_skills

# 搜索技能
/search_skills query="code review"

# 获取技能详情
/get_skill skill_id="requesting-code-review" include_content=true

# 查看统计
/get_stats

# 重建索引
/rebuild_index force=true
```

## 索引缓存机制

### 缓存结构

```json
{
  "index": {
    "tdd": {
      "id": "tdd",
      "name": "Test-Driven Development",
      "path": "./superpowers/tdd/SKILL.md",
      "description": "...",
      "tags": ["testing", "development"],
      "file_hash": "abc123...",
      "file_mtime": 1234567890.0,
      "content_length": 5000,
      "section_count": 10,
      "last_scanned": "2026-03-13T10:00:00"
    }
  },
  "metadata": {
    "version": "1.0.0",
    "created_at": "2026-03-13T10:00:00",
    "updated_at": "2026-03-13T12:00:00",
    "total_skills": 560,
    "file_hashes": {"./superpowers/tdd/SKILL.md": "abc123..."}
  }
}
```

### 增量更新流程

1. **File Watcher** 检测到 `SKILL.md` 文件变化
2. 计算新文件的 hash
3. 与缓存中的 hash 比较
4. 如果有变化，更新索引并保存
5. 如果无变化，跳过处理

### 缓存过期策略

- **TTL**: 5 分钟自动过期
- **启动检查**: 每次启动检查缓存有效性
- **手动重建**: `rebuild_index force=true`

## 语义匹配算法

### 评分规则

| 匹配类型 | 分数 | 说明 |
|----------|------|------|
| name_exact | 100 | 名称完全匹配 |
| name_contains | 50 | 名称包含关键词 |
| name_word | 20 | 名称单词匹配 |
| tag_exact | 30 | 标签完全匹配 |
| tag_partial | 15 | 标签部分匹配 |
| task_type | 40 | 任务类型匹配 |
| category | 8 | 类别关键词 |
| desc_word | 5 | 描述单词匹配 |

### 任务类型检测

```python
bug_fix    -> ["bug", "fix", "error", "fail", "broken"]
feature    -> ["add", "new", "feature", "implement"]
refactor   -> ["refactor", "clean", "simplify"]
review     -> ["review", "check", "audit", "verify"]
research   -> ["research", "explore", "investigate"]
deploy     -> ["deploy", "release", "ship", "merge"]
```

## 性能基准

| 操作 | 首次 | 缓存 | 增量 |
|------|------|------|------|
| 索引加载 | ~2s | ~50ms | ~10ms |
| 搜索查询 | - | ~5ms | - |
| 路由推荐 | - | ~10ms | - |
| 文件更新 | - | - | ~5ms |

## 文件结构

```
devops/skill-loader/
├── __init__.py          # 包入口，导出 API
├── cli.py               # CLI 入口脚本
├── mcp_server.py        # MCP Server 实现
├── skill_cache.py       # 索引缓存系统
├── skill_router.py      # 路由和匹配引擎
├── requirements.txt     # Python 依赖
├── package.json         # MCP 插件配置
├── README.md            # 本文档
└── .cache/              # 缓存目录（自动生成）
    ├── skill_index.json # 索引缓存
    └── metadata.json    # 元数据缓存
```

## 故障排除

### 缓存损坏

```bash
# 删除缓存重建
rm -rf devops/skill-loader/.cache/
python cli.py rebuild
```

### MCP Server 无法启动

检查路径配置：
```bash
# 验证路径
ls /absolute/path/to/devops/skill-loader/mcp_server.py

# 测试启动
python devops/skill-loader/mcp_server.py
```

### 文件监控不工作

确保 watchdog 已安装：
```bash
pip install watchdog
```

## 扩展和定制

### 添加新的匹配规则

编辑 `skill_router.py`:

```python
class KeywordMatcher:
    CATEGORY_KEYWORDS = {
        "my_category": ["keyword1", "keyword2"],
        # ...
    }
```

### 自定义缓存策略

编辑 `skill_cache.py`:

```python
CACHE_TTL_SECONDS = 300  # 修改过期时间
```

### 添加新的 MCP 工具

编辑 `mcp_server.py`:

```python
@server.list_tools()
async def list_tools():
    return [
        Tool(name="my_new_tool", ...),
        # ...
    ]
```

## 未来计划

- [ ] 添加向量相似度搜索（embedding）
- [ ] 支持技能热度统计
- [ ] 添加技能依赖图
- [ ] 支持技能版本管理
- [ ] 添加技能使用分析

## 许可证

MIT License
