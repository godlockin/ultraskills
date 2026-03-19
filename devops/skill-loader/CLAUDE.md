# Skill Loader - CLAUDE.md

> 高效的 Skills 动态加载系统

## 快速使用

### 重建索引
```bash
cd devops/skill-loader
python cli.py rebuild
```

### 搜索技能
```bash
python cli.py search --query "code review"
```

### 路由任务
```bash
python cli.py route --query "fix the bug"
```

## Python API

```python
from skill_cache import get_cache
from skill_router import SkillRouter

# 缓存
cache = get_cache(project_root, auto_watch=True)
results = cache.search("tdd", top_n=5)

# 路由
router = SkillRouter()
router.initialize()
result = router.route("fix the bug", top_n=3)
```

## MCP 配置

```json
{
  "mcpServers": {
    "skills": {
      "command": "python",
      "args": ["/abs/path/to/mcp_server.py"],
      "cwd": "/abs/path/to/skill-loader"
    }
  }
}
```

## 文件结构

- `skill_cache.py` - 索引缓存（双层缓存 + 文件监听）
- `skill_router.py` - 路由匹配（关键词 + 任务类型）
- `mcp_server.py` - MCP Server 实现
- `cli.py` - CLI 入口

## 性能

- 索引构建：~0.5s (305 技能)
- 搜索查询：<10ms
- 路由推荐：<15ms
