# Skill Loader - 快速开始

> 高效的 Skills 动态加载和发现系统

## 核心特性

| 特性 | 性能提升 |
|------|----------|
| 双层缓存（内存 + 磁盘） | 查询 <10ms |
| 文件监听增量更新 | O(1) 变化处理 |
| 语义搜索和路由 | 智能任务匹配 |
| MCP 协议支持 | 无缝集成 Claude Code |

## 架构

```
用户/Claude Code
       │
       ▼
┌──────────────────────────┐
│   MCP Server (可选)      │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│   Skill Router           │
│   - 关键词匹配           │
│   - 任务类型识别         │
│   - 技能组合推荐         │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│   Skill Index Cache      │
│   - 内存缓存 (运行时)    │
│   - 磁盘缓存 (JSON)      │
│   - File Watcher         │
└──────────┬───────────────┘
           │
           ▼
┌──────────────────────────┐
│   技能文件 (SKILL.md)    │
└──────────────────────────┘
```

## 安装和配置

### 1. 安装依赖

```bash
cd devops/skill-loader
pip install -r requirements.txt
```

### 2. 构建索引

```bash
python cli.py rebuild
```

### 3. 配置 MCP Server (可选)

在 Claude Code 的 MCP 配置 (`~/.claude/settings.json` 或项目配置) 中添加：

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

## 使用方式

### CLI 命令

```bash
# 重建索引
python cli.py rebuild

# 查看统计
python cli.py stats

# 搜索技能
python cli.py search --query "video processing"

# 路由任务（智能推荐）
python cli.py route --query "fix the bug"
```

### Python API

```python
from skill_loader import get_cache, get_router

# 获取缓存
cache = get_cache()

# 搜索技能
results = cache.search("tdd", top_n=5)

# 获取路由推荐
router = get_router()
result = router.route("I need to fix a bug")

print(result['primary_skill'])  # 主推荐技能
print(result['suggested_workflow'])  # 工作流程建议
```

### MCP 工具调用

配置 MCP Server 后，在 Claude Code 中使用：

```
/list_skills                     # 列出所有技能
/search_skills query="code review"  # 搜索技能
/get_skill skill_id="tdd"        # 获取技能详情
/get_stats                       # 查看统计
```

## 性能基准

| 操作 | 时间 |
|------|------|
| 首次索引构建 | ~0.5s (300+ 技能) |
| 缓存加载 | ~50ms |
| 搜索查询 | ~5ms |
| 路由推荐 | ~10ms |
| 文件更新 | ~5ms |

## 文件结构

```
devops/skill-loader/
├── skill_cache.py      # 索引缓存系统
├── skill_router.py     # 路由和匹配引擎
├── mcp_server.py       # MCP Server 实现
├── cli.py              # CLI 入口
├── test_loader.py      # 测试脚本
├── requirements.txt    # Python 依赖
└── .cache/             # 缓存目录（自动生成）
    └── skill_index.json
```

## 故障排除

**缓存损坏：**
```bash
rm -rf devops/skill-loader/.cache/
python cli.py rebuild
```

**MCP Server 无法启动：**
```bash
# 验证路径
ls /absolute/path/to/devops/skill-loader/mcp_server.py

# 测试启动
python devops/skill-loader/mcp_server.py
```

## 扩展

### 添加新的匹配规则

编辑 `skill_router.py` 中的 `KeywordMatcher.CATEGORY_KEYWORDS`：

```python
CATEGORY_KEYWORDS = {
    "my_category": ["keyword1", "keyword2"],
    # ...
}
```

### 自定义缓存策略

编辑 `skill_cache.py`：

```python
CACHE_TTL_SECONDS = 300  # 修改过期时间（秒）
```

## 许可证

MIT License
