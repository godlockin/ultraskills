# 示例：深 vs 浅

## 例 1：浅 → 深（加深的经典例子）

**浅版本**（多个薄包装层）：

```typescript
// ❌ 每个模块都是 pass-through
function getUserFromDB(id: string): Promise<User> {
  return db.query(`SELECT * FROM users WHERE id = ${id}`);
}

function parseUser(row: any): User {
  return { id: row.id, name: row.name, email: row.email };
}

function cacheUser(user: User): void {
  cache.set(user.id, user);
}

function getUserWithCache(id: string): Promise<User> {
  return getUserFromDB(id).then(parseUser).then(cacheUser);
}
```

调用方必须知道 4 个函数。bug 散落四处：DB schema、解析、缓存键、一致性。

**深版本**（小接口 + 大实现）：

```typescript
// ✅ 一个深模块，小接口
interface UserRepository {
  findById(id: string): Promise<User | null>;
}

class PostgresUserRepository implements UserRepository {
  async findById(id: string): Promise<User | null> {
    const row = await db.query(`SELECT * FROM users WHERE id = $1`, [id]);
    return row ? this.parse(row) : null;  // 内部 seam：parse 是私有的
  }

  private parse(row: any): User { /* ... */ }
}
```

调用方只学 1 个方法。bug 集中在一处。

## 例 2：删除测试

考虑 `CacheWrapper<T>` —— 一个把任意类型包进 cache 的薄包装类。

**删除测试**：
- 删掉 `CacheWrapper`。
- 谁来负责 cache 调用？是每个 caller。
- 增加的复杂度 = N 个 caller × cache 调用代码 = **pass-through**。
- → 删除测试显示它是浅的，应内联到 caller。

考虑 `UserRepository.findById` —— 上面那种。

**删除测试**：
- 删掉 `UserRepository`。
- 谁来负责 SQL 拼接、解析、错误处理？散落到 N 个 caller。
- 增加的复杂度 = **巨大**。
- → 它值得存在。

## 例 3：设计可选性（什么时候加 adapter？）

```typescript
// 一个 adapter：仅用于单元测试
class MockEmailService implements EmailService { /* ... */ }

// ❌ 生产环境只用 HttpEmailService，测试用 MockEmailService
// 单一用途 — 这是个"假设 seam"，不引入接口
class HttpEmailService implements EmailService { /* ... */ }
```

**问题**：仅测试需要 mock 时，没必要加接口。直接 `new HttpEmailService()`，测试用依赖注入传 mock 实例，**不需要接口**。

**何时需要接口**：当生产环境需要**两个 adapter**（如同时支持 `HttpEmailService` 和 `SmtpEmailService`），或者**真正外部的依赖**（Stripe、Twilio）必须被 mock 时。

---

## 来源

本文示例基于 [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/codebase-design/) 的方法论，遵循 MIT License。