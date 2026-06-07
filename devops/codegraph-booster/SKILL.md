---
name: codegraph-booster
description: Code探索加速器 - 在架构探索/调用链追踪任务中自动启用语义索引,削减70%工具调用。触发词:explore architecture/架构探索/trace calls/impact analysis/调用链/影响分析/semantic search/代码图谱
version: 1.0.0
tags: [devops, optimization, mcp-server, performance, code-intelligence]
---

# CodeGraph Booster

> 通过语义代码图谱将架构探索成本降低35%、工具调用削减70%的MCP服务器自动化部署方案

## 🎯 目标 (Goal)

* **智能判断**: 根据项目规模自动决定是否启用CodeGraph
* **透明加速**: 在合适场景(中大型项目架构探索)下无感提速
* **成本优化**: 避免在小项目(<500文件)产生初始化开销

## 🧠 核心理念 (Core Concepts)

CodeGraph通过Tree-sitter构建代码AST → SQLite知识图谱,使AI agent能:

1. **一次性获取完整上下文**: \`codegraph_explore\`替代多轮grep/read
2. **精准追踪调用链**: callers/callees瞬时返回
3. **影响半径分析**: 修改前预判波及范围

**适用场景benchmark** (基于7个开源项目):
| 项目规模 | 成本↓ | 工具调用↓ | 典型收益 |
|---------|------|---------|---------|
| >10k文件(VS Code) | 35% | 72% | ⭐⭐⭐⭐⭐ |
| 600-3k文件(Django) | 34% | 81% | ⭐⭐⭐⭐ |
| <150文件(Gin) | 22% | 19% | ⭐ (收益有限) |

## 🚀 使用流程 (Workflow)

### Step 1: 自动判断与初始化 (Automatic Setup)

当检测到以下触发场景时,skill自动执行:

**触发场景**:
- "分析这个项目架构" / "Explore architecture"
- "追踪XX函数的调用链" / "Trace calls"
- "修改XX会影响哪些模块" / "Impact analysis"
- "语义搜索XX符号" / "Semantic search"

**初始化脚本**:
\`\`\`bash
bash {SKILL_DIR}/scripts/setup.sh
\`\`\`

脚本逻辑:
1. 统计项目文件数(仅计算源代码: \`.ts/.py/.go/...\`)
2. **<500文件**: 跳过CodeGraph,输出提示 "项目规模较小,使用原生工具探索"
3. **≥500文件**: 
   - 检查\`.codegraph/\`是否存在
   - 不存在 → 安装CodeGraph MCP + 初始化索引
   - 已存在 → 验证索引健康度

### Step 2: 探索策略切换 (Exploration Strategy)

**启用CodeGraph后的工具优先级**:

| 任务类型 | 推荐工具 | 备选方案 |
|---------|---------|---------|
| 架构理解 | \`codegraph_explore\` | grep + 多次read |
| 符号定位 | \`codegraph_search\` | grep |
| 调用链追踪 | \`codegraph_callers/callees\` | LSP + 手动展开 |
| 影响分析 | \`codegraph_impact\` | 全局搜索引用 |
| 文件结构 | \`codegraph_files\` | ls + tree |

**关键原则**:
- ✅ 在Explore agent提示词中注入CodeGraph使用规则(见Step 3)
- ✅ 主会话仅用轻量级查询工具(\`search/callers/impact\`)
- ❌ 主会话禁用\`codegraph_explore\`(会返回大量源码污染上下文)

### Step 3: Agent提示词注入 (Prompt Injection)

当spawn Explore agent时,在prompt中加入:

\`\`\`markdown
**CodeGraph Rules** (.codegraph/ exists):
1. PRIMARY tool: \`codegraph_explore\` — returns full source sections
2. Follow explore call budget (auto-scales by project size)
3. DON'T re-read files returned by codegraph_explore
4. Only fallback to grep/read for "Additional relevant files"
\`\`\`

### Step 4: 健康检查 (Health Verification)

\`\`\`bash
python3 {SKILL_DIR}/scripts/check_status.py
\`\`\`

输出示例:
\`\`\`
✓ CodeGraph installed: v0.9.4
✓ Index exists: .codegraph/codegraph.db (2.3MB)
✓ Index fresh: last updated 3 minutes ago
✓ Stats: 1,847 symbols | 4,203 edges | 19 languages
✓ Watcher: active (auto-sync enabled)
\`\`\`

## 💡 最佳实践 (Best Practices)

### ✅ Do

* **首次探索大型项目时**: 主动询问用户 "是否初始化CodeGraph加速探索"
* **小项目直接跳过**: <500文件时在响应中说明 "项目规模适合原生工具"
* **增量同步**: 修改代码后等待2秒(watcher debounce窗口)再查询
* **混合策略**: CodeGraph定位+原生工具精读(如需上下文)

### ❌ Don't

* **全局安装**: CodeGraph索引per-project,不要尝试全局\`npm i -g\`后共享
* **主会话调用explore**: 大量源码会占满context,仅在sub-agent用
* **忽略benchmark**: 盲目在小项目初始化会浪费1-2分钟
* **跳过健康检查**: 索引损坏会导致空结果,初始化后必验证

## 🔧 故障排除 (Troubleshooting)

| 问题 | 原因 | 解决 |
|-----|------|-----|
| "database is locked" | 旧版本(<0.9)或网络盘 | 重新安装/移到本地磁盘 |
| "symbols missing" | 索引未自动同步 | \`codegraph sync\` |
| "MCP not connecting" | 服务未启动 | 检查\`~/.claude.json\`配置 |
| 初始化>5分钟 | node_modules未排除 | 确认\`.gitignore\`正确 |

## 📊 成本决策表 (Decision Matrix)

| 项目特征 | 是否启用 | 预期ROI |
|---------|---------|--------|
| >5k文件 | ✅ 强烈推荐 | 50%+ 成本削减 |
| 1k-5k文件 | ✅ 推荐 | 30-40% 优化 |
| 500-1k文件 | ⚠️ 按需 | 20-30% 优化 |
| <500文件 | ❌ 跳过 | <20% (不值得) |
| 频繁架构探索 | ✅ 必备 | 持续收益 |
| 单次快速查询 | ❌ 跳过 | 初始化成本>收益 |

## 📚 资源引用

* [完整benchmark数据](./examples/benchmark-comparison.md)
* [setup.sh源码](./scripts/setup.sh)
* [CodeGraph官方文档](https://github.com/colbymchenry/codegraph)
* [健康检查脚本](./scripts/check_status.py)
