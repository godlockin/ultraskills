# 示例：诊断循环实战

## 例 1：API 路由返回 500

**症状**：用户报告 `/api/orders/:id` 偶尔返回 500。
**问题**：偶发，无明确重现路径。

### Phase 1 — 建反馈环

```bash
# 1. curl 构造复现
curl -X GET "http://localhost:3000/api/orders/12345"
# 2. 期望 200，实际 500 ✓ red-capable
```

### Phase 2 — 重现 + 最小化

跑 100 次：
```bash
for i in $(seq 1 100); do
  curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:3000/api/orders/12345"
done
# 90 次 200，10 次 500 → 10% 复现率
```

最小化：去掉请求体、去掉 cookie、换不同 id → 发现只有 id 末位为 0 的请求偶发 500。

### Phase 3 — 假设（3 个）

1. **数据库连接池耗尽**（id 末位 0 触发特殊查询路径，加重了连接占用）—— 预测：把 id 末位改 1，重现率下降
2. **特定 id 触发 SQL 解析 bug**（末位 0 → 数字字面量歧义）—— 预测：在 query 中显式 cast 末位 0，bug 消失
3. **缓存击穿**（id 末位 0 不在缓存，并发请求击穿到 DB）—— 预测：加 mutex 后重现率显著下降

展示给用户 → 用户："我们上周改了 #2 的 SQL parser"

### Phase 4 — 插桩

```typescript
// [DEBUG-a4f2] 在 ORM 层加日志
console.log('[DEBUG-a4f2] query:', sql, 'params:', params);
```

跑 100 次 → 日志显示末位 0 的 id 被 ORM 序列化成 `WHERE id = `（无值，syntax error）。

### Phase 5 — 修复 + 回归测试

```typescript
// 修复：强制参数化
const result = await db.query('SELECT * FROM orders WHERE id = $1', [id]);
```

回归测试（之前 10% flake，现在 0%）：
```typescript
test('id ending in 0 returns 200', async () => {
  for (let i = 0; i < 100; i++) {
    const res = await request(app).get('/api/orders/12340');
    expect(res.status).toBe(200);
  }
});
```

### Phase 6 — 清理

- [x] 重跑原 repro：100% 200
- [x] 回归测试通过
- [x] `grep -r "DEBUG-a4f2"` → 已删
- [x] PR message 写明："末位 0 id 触发 ORM 参数化 bug，原因 #2 假设正确"

---

## 例 2：性能回退

**症状**：某 endpoint 从 100ms 退化到 800ms。

### Phase 1 — feedback loop

```typescript
// timing harness
const start = performance.now();
const result = await fetchOrders();
const elapsed = performance.now() - start;
// 期望 < 150ms，实际 800ms ✓
```

### Phase 4 — perf 优先

不是加日志，而是**先建基线**：
- 二分 commit：`git bisect run npm test` 找到引入 commit
- 用 `EXPLAIN ANALYZE` 看 query plan
- 用 profiler（clinic.js / 0x）看火焰图

发现是新加的 `LEFT JOIN users` 触发全表扫描（users 表 100 万行）。

### Phase 5 — 修复

加索引：
```sql
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

性能回到 95ms。

### Phase 6 — 复盘

什么本可阻止？**加索引是 schema 变更，应该走 ADR review**。交给 `/improve-codebase-architecture`：建议加 pre-commit hook 检查新增 column 有无索引。

---

## 来源

本文示例基于 [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/diagnosing-bugs/) 的 6 阶段方法论，遵循 MIT License。