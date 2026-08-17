# 示例：两轴 Review

## 例 1：Standards pass, Spec fail

**变更**：
```typescript
// PR 添加用户导出功能
function exportUsersToCsv(users: User[]): string {
  const rows = users.map(u => `${u.id},${u.name},${u.email}`);
  return rows.join('\n');
}
```

**Standards 轴**：
- ✅ 项目规范要求 typed CSV handling——这里直接字符串拼接，**违反** `CODING_STANDARDS.md` 的 "Use papaparse for CSV"
- ✅ 无 Fowler smell
- **结果**：1 finding（Standards 违反）

**Spec 轴**：
- ❌ Issue #42 要求"导出包含用户最后登录时间"——diff 中完全没加
- ❌ Issue #42 要求"超过 10000 行分块下载"——diff 是单文件下载
- **结果**：2 finding（Spec 缺失需求）

**汇总**：1 Standards + 2 Spec。**Spec fail 是阻塞，Standards fail 是次要**。

---

## 例 2：Spec pass, Standards fail

**变更**：issue 要求实现"乐观锁更新库存"

```typescript
async function updateStock(productId: string, newStock: number) {
  // SPEC: 100% 对齐 — 使用 version 字段做 CAS
  const product = await db.query('SELECT * FROM products WHERE id = $1', [productId]);
  await db.query(
    'UPDATE products SET stock = $1, version = version + 1 WHERE id = $2 AND version = $3',
    [newStock, productId, product.version]
  );
}
```

**Standards 轴**：
- ❌ 项目要求所有 DB query 走 repository pattern，**这里直接 db.query**
- ❌ Smell: **Primitive Obsession** — `newStock` 是裸 number，应该 `Stock` 类型
- ❌ Smell: **Shotgun Surgery** — 加 stock 字段要在 3 处编辑
- **结果**：3 finding

**Spec 轴**：
- ✅ 完全对齐 issue 描述
- **结果**：0 finding

**汇总**：3 Standards + 0 Spec。**Standards fail 可改，Spec pass 是事实**——两轴价值正是这种分离。

---

## 例 3：双 fail

**变更**：issue 要求加 log，所有标准都符合，除了...

```typescript
// SPEC: log 应该包含 user_id
console.log('user action');
// Spec fail: 没 user_id

// STANDARDS: 项目要求 console.log 用 logger
console.log('user action', userId);
// Standards fail: 应该用 logger.info()
```

**两轴各 1 finding**。修复时两个都改：

```typescript
logger.info('user action', { user_id: userId });
```

---

## 来源

本文示例基于 [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/code-review/) 的两轴方法论，遵循 MIT License。