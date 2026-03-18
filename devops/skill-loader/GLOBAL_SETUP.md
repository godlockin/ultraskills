# Skills MCP - 全局配置指南

> 让所有项目都能使用 Skills 动态加载系统

## 配置完成 ✅

全局 MCP 配置已安装到：`~/.claude/mcp.json`

```json
{
  "mcpServers": {
    "skills-discovery": {
      "command": "python",
      "args": ["/path/to/devops/skill-loader/mcp_server.py"],
      "cwd": "/path/to/devops/skill-loader"
    }
  }
}
```

## 验证配置

### 1. 重启 Claude Code

重启后运行：
```
/mcp
```

应该看到 `skills-discovery` 服务器显示为 **✔ connected**

### 2. 测试命令

```
/list_skills                              # 列出所有技能
/search_skills query="code review"        # 搜索技能
/get_skill skill_id="tdd" include_content=true
/get_stats                                # 查看统计
```

## 可用的 MCP 工具

| 工具 | 描述 | 示例 |
|------|------|------|
| `list_skills` | 列出所有技能 | `/list_skills limit=10` |
| `search_skills` | 搜索技能 | `/search_skills query="video edit"` |
| `get_skill` | 获取技能详情 | `/get_skill skill_id="tdd"` |
| `get_stats` | 查看统计 | `/get_stats` |
| `rebuild_index` | 重建索引 | `/rebuild_index force=true` |

## 在任何项目中使用

配置完成后，在**任何项目**中都可以直接使用：

```
# 搜索技能
/search_skills query="bug fix"

# 获取技能详情
/get_skill skill_id="systematic-debugging"

# 查看可用技能
/list_skills
```

## 安装脚本（可选）

如果需要重新安装或迁移到其他机器：

```bash
cd devops/skill-loader
./install-global-mcp.sh
```

## 卸载

```bash
# 删除全局 MCP 配置
rm ~/.claude/mcp.json

# 重启 Claude Code
```

## 故障排除

### Q: /mcp 看不到 skills-discovery

**A:** 重启 Claude Code，检查配置：
```bash
cat ~/.claude/mcp.json
```

### Q: 连接失败

**A:** 测试 MCP Server 是否能启动：
```bash
python mcp_server.py
```

### Q: 索引为空

**A:** 重建索引：
```bash
cd devops/skill-loader
python cli.py rebuild
```

## 配置位置

| 类型 | 路径 | 作用域 |
|------|------|------|
| 全局 MCP | `~/.claude/mcp.json` | 所有项目 |
| 项目 MCP | `./.mcp.json` | 当前项目 |
| 索引缓存 | `devops/skill-loader/.cache/` | 本地 |

## 性能

| 操作 | 时间 |
|------|------|
| 索引构建 | ~0.5s (305 技能) |
| 搜索查询 | <10ms |
| 路由推荐 | <15ms |

---

**配置日期：** 2026-03-13
**技能库版本：** 1.0.0 (305 技能)
