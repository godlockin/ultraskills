# Skills Usage Tracking System

> 追踪 skills 实际使用情况，结合竞技场评分实现基于数据的淘汰决策

---

## 现状问题

**当前淘汰机制**：
- 仅基于静态评分（文档质量 + 功能明确性 + 可维护性）
- **缺失**：实际使用频率、用户满意度、成功率
- **结果**：`template-skill` 连续10轮低分，但从未真正淘汰

**需要什么数据**：
| 指标 | 说明 | 数据源 |
|------|------|--------|
| 调用次数 | Skill 被触发的总次数 | Claude Code 日志 |
| 成功率 | 任务完成 / 总调用 | 用户反馈 + 任务状态 |
| 平均耗时 | 执行时间中位数 | Session 计时 |
| 用户评分 | 1-5星评价 | 主动收集 |
| 最近使用 | 最后一次调用时间 | 时间戳 |

---

## 方案选择

### 方案 A：集成 Serena（现有项目）

**Serena** 是既有的 Master-Slaver 多智能体框架（`~/.claude/skills/eket`），包含：
- SQLite 数据库（`~/.eket/eket.db`）
- Skill 执行追踪
- 任务完成度记录

**改造方案**：

#### Step 1: 扩展 Serena 数据表

```sql
-- 在 ~/.eket/eket.db 添加表
CREATE TABLE IF NOT EXISTS skill_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id TEXT NOT NULL,
    invoked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id TEXT,
    task_id TEXT,
    status TEXT CHECK(status IN ('started', 'completed', 'failed', 'abandoned')),
    duration_ms INTEGER,
    user_rating INTEGER CHECK(user_rating BETWEEN 1 AND 5),
    notes TEXT
);

CREATE INDEX idx_skill_usage_skill_id ON skill_usage(skill_id);
CREATE INDEX idx_skill_usage_invoked_at ON skill_usage(invoked_at);
```

#### Step 2: Hook Claude Code Skill 调用

在 `~/.claude/hooks/SessionStart.js`（或类似）添加：

```javascript
// 拦截 Skill tool 调用
function onSkillInvoke(skillName) {
  // 记录到 Serena DB
  exec(`eket skill:track-start ${skillName}`);
}

function onSkillComplete(skillName, status, durationMs) {
  exec(`eket skill:track-end ${skillName} --status=${status} --duration=${durationMs}`);
}
```

#### Step 3: Rust CLI 命令（eket binary）

添加到 `~/.claude/skills/eket/rust/eket-cli/`:

```rust
// skill:track-start <skill_id>
pub fn track_skill_start(skill_id: &str, session_id: &str) -> Result<i64> {
    let db = Database::open()?;
    db.execute(
        "INSERT INTO skill_usage (skill_id, session_id, status) VALUES (?1, ?2, 'started')",
        params![skill_id, session_id],
    )?;
    Ok(db.last_insert_rowid())
}

// skill:track-end <skill_id> --status=<completed|failed> --duration=<ms>
pub fn track_skill_end(skill_id: &str, status: &str, duration_ms: u64) -> Result<()> {
    let db = Database::open()?;
    db.execute(
        "UPDATE skill_usage SET status = ?1, duration_ms = ?2 WHERE skill_id = ?3 AND status = 'started' ORDER BY invoked_at DESC LIMIT 1",
        params![status, duration_ms, skill_id],
    )?;
    Ok(())
}

// skill:stats <skill_id>
pub fn get_skill_stats(skill_id: &str) -> Result<SkillStats> {
    let db = Database::open()?;
    let stats: SkillStats = db.query_row(
        "SELECT 
            COUNT(*) as total_calls,
            SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as success_count,
            AVG(duration_ms) as avg_duration,
            MAX(invoked_at) as last_used
         FROM skill_usage WHERE skill_id = ?1",
        params![skill_id],
        |row| Ok(SkillStats {
            total_calls: row.get(0)?,
            success_count: row.get(1)?,
            avg_duration: row.get(2)?,
            last_used: row.get(3)?,
        }),
    )?;
    Ok(stats)
}
```

#### Step 4: 合并评分逻辑

在 `scripts/arena_cluster_score.py` 中：

```python
import sqlite3

def get_usage_boost(skill_id):
    """基于使用数据给予加分"""
    conn = sqlite3.connect(os.path.expanduser('~/.eket/eket.db'))
    cursor = conn.execute("""
        SELECT 
            COUNT(*) as calls,
            AVG(CASE WHEN status='completed' THEN 1.0 ELSE 0.0 END) as success_rate,
            AVG(user_rating) as avg_rating,
            MAX(invoked_at) as last_used
        FROM skill_usage WHERE skill_id = ?
    """, (skill_id,))
    row = cursor.fetchone()
    
    if not row or row[0] == 0:  # 无使用数据
        return 0.0
    
    calls, success_rate, avg_rating, last_used = row
    
    # 使用频率加分 (max +1.0)
    freq_boost = min(1.0, calls / 100)
    
    # 成功率加分 (max +1.0)
    success_boost = success_rate if success_rate else 0.0
    
    # 用户评分加分 (max +1.0)
    rating_boost = (avg_rating / 5.0) if avg_rating else 0.0
    
    # 活跃度惩罚 (6个月未使用 -0.5)
    from datetime import datetime, timedelta
    if last_used:
        last_dt = datetime.fromisoformat(last_used)
        if datetime.now() - last_dt > timedelta(days=180):
            freq_boost -= 0.5
    
    return (freq_boost + success_boost + rating_boost) / 3

# 应用到最终分数
final_score = static_score + get_usage_boost(skill_id)
```

---

### 方案 B：轻量级追踪（独立系统）

不依赖 Serena，创建独立追踪：

#### 结构

```
skill-arena/
├── usage_tracking/
│   ├── tracker.py           # 追踪逻辑
│   ├── usage.db             # SQLite（同 Serena schema）
│   └── analyzer.py          # 分析脚本
```

#### Hook 实现

在 `~/.claude/hooks/ToolUsed.js`:

```javascript
function onToolUsed(tool, args, result) {
  if (tool === 'Skill') {
    const skillName = args.skill;
    const startTime = Date.now();
    
    // 写入 CSV（简单版）
    const logPath = os.path.expanduser('~/.claude/skill-usage.csv');
    fs.appendFileSync(logPath, `${skillName},${new Date().toISOString()},started\n`);
    
    // 监听完成
    registerCallback(() => {
      const duration = Date.now() - startTime;
      fs.appendFileSync(logPath, `${skillName},${new Date().toISOString()},completed,${duration}\n`);
    });
  }
}
```

---

## 推荐方案：Serena 集成（方案 A）

**理由**：
1. ✅ 已有完整数据库基础设施（SQLite + Rust ORM）
2. ✅ 与既有 Master-Slaver 工作流无缝集成
3. ✅ 可复用 eket CLI（已有 session/task tracking）
4. ✅ 支持跨会话持久化

**实施路径**：
1. Serena 添加 `skill_usage` 表
2. Serena 添加 Rust CLI 命令（`eket skill:track-*`）
3. Claude Code Hook 调用 eket 命令
4. Arena pipeline 读取 usage 数据加权评分

---

## 淘汰决策矩阵

综合静态评分 + 动态使用数据：

| 条件 | 操作 |
|------|------|
| 静态分 < 4.0 **且** 使用次数 < 5（6个月内） | 🚨 立即淘汰 |
| 静态分 < 4.0 **但** 使用次数 > 50 | ⚠️ 警告，需人工审核（可能评分不准） |
| 静态分 ≥ 7.0 **但** 6个月未使用 | 💤 归档（移到 `archived/`） |
| 静态分 < 6.0 **且** 成功率 < 50% | 🔄 重构候选 |

---

## 用户反馈收集

在 skill 执行完成后，偶尔弹出评分（不干扰）：

```
┌─────────────────────────────────────────┐
│ Skill "visual-forge" 已完成             │
│                                         │
│ 是否满意输出？                          │
│ ⭐⭐⭐⭐⭐  (点击评分，可选)             │
│                                         │
│ [跳过]   [从不再问此 skill]             │
└─────────────────────────────────────────┘
```

触发频率：
- 每个 skill 前 5 次调用：100%
- 5-20 次：50%
- 20+ 次：10%

---

## 实施清单

### Phase 1: Serena 扩展（1-2天）
- [ ] 在 Serena 添加 `skill_usage` 表
- [ ] 实现 `eket skill:track-start/end/stats` 命令
- [ ] 单元测试

### Phase 2: Hook 集成（1天）
- [ ] 创建 Claude Code Hook（ToolUsed / SessionEnd）
- [ ] 测试 skill 调用追踪
- [ ] 验证数据写入

### Phase 3: Arena 集成（1天）
- [ ] `arena_cluster_score.py` 读取 usage 数据
- [ ] 加权算法实现
- [ ] 淘汰决策矩阵实现

### Phase 4: 用户反馈（可选，1天）
- [ ] 评分弹窗 UI
- [ ] 写入 `user_rating` 字段
- [ ] 统计分析

---

## 数据隐私

- 使用数据**仅本地存储**（`~/.eket/eket.db`）
- 不上传到远程服务器
- 用户可随时删除：`rm ~/.eket/eket.db`

---

## 下一步

**立即可做**（无需代码）：
1. 手动审查 `low_performers.json` 中 `consecutive_low >= 3` 的 skills
2. 检查 `template-skill` 是否真的无用（很可能是占位符，应删除）
3. 创建 `skill-arena/eliminated.json` 记录首批淘汰

**待开发**（需 Serena 升级）：
1. 实施 Phase 1-3
2. 运行 2-4 周收集真实使用数据
3. 基于数据重新评估淘汰候选

---

*Last Updated: 2026-05-08*
