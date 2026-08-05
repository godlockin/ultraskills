# Good and Bad Tests — 好与坏测试

## Good Tests

**Integration-style**：通过真接口测，不用 mock 内部部件。

```typescript
// GOOD: Tests observable behavior
test("user can checkout with valid cart", async () => {
  const cart = createCart();
  cart.add(product);
  const result = await checkout(cart, paymentMethod);
  expect(result.status).toBe("confirmed");
});
```

特征：

- 测试用户/调用方关心的行为
- 仅用公共 API
- 内部重构后存活
- 描述 WHAT，不 HOW
- 每测试一个逻辑断言

## Bad Tests

**Implementation-detail tests**：耦合内部结构。

```typescript
// BAD: Tests implementation details
test("checkout calls paymentService.process", async () => {
  const mockPayment = jest.mock(paymentService);
  await checkout(cart, payment);
  expect(mockPayment.process).toHaveBeenCalledWith(cart.total);
});
```

红旗：

- mock 内部协作者
- 测私有方法
- 断言调用次数/顺序
- 无行为变化的 refactor 后测试挂
- 测试名描述 HOW 不 WHAT
- 通过外部手段验证而非接口

```typescript
// BAD: Bypasses interface to verify
test("createUser saves to database", async () => {
  await createUser({ name: "Alice" });
  const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
  expect(row).toBeDefined();
});

// GOOD: Verifies through interface
test("createUser makes user retrievable", async () => {
  const user = await createUser({ name: "Alice" });
  const retrieved = await getUser(user.id);
  expect(retrieved.name).toBe("Alice");
});
```

**Tautological tests**：期望值复述实现，所以测试按构造通过。

```typescript
// BAD: Expected value is recomputed the way the code computes it
test("calculateTotal sums line items", () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0);
  expect(calculateTotal(items)).toBe(expected);
});

// GOOD: Expected value is an independent, known literal
test("calculateTotal sums line items", () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```

---

## 来源

本文档改编自 [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd/tests.md)，遵循 MIT License。