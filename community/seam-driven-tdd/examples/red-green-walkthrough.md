# 示例：Seam-Driven TDD 实战

## 例 1：红绿循环（tracer bullet）

**目标**：实现 `applyDiscount(cart, code)` —— 给购物车应用折扣码。

### Cycle 1：第一个 seam

**Step 1 — Red**：写测试在 seam `applyDiscount` 上。

```typescript
test('applyDiscount rejects invalid code', () => {
  const cart = createCart([{ id: 'p1', price: 100 }]);
  const result = applyDiscount(cart, 'INVALID');
  expect(result.ok).toBe(false);
  expect(result.error).toBe('unknown code');
});
```

跑 → 失败（`applyDiscount` 不存在）。

**Step 2 — Green**：写最小实现。

```typescript
function applyDiscount(cart, code) {
  if (code === 'INVALID') return { ok: false, error: 'unknown code' };
  // ... stub
}
```

跑 → 通过。

### Cycle 2：第二个 tracer bullet

**Step 1 — Red**：

```typescript
test('applyDiscount applies 10% off with VALID10 code', () => {
  const cart = createCart([{ id: 'p1', price: 100 }]);
  const result = applyDiscount(cart, 'VALID10');
  expect(result.cart.total).toBe(90);
});
```

**Step 2 — Green**：

```typescript
function applyDiscount(cart, code) {
  const discounts = { VALID10: 0.1 };
  const rate = discounts[code];
  if (!rate) return { ok: false, error: 'unknown code' };
  return { ok: true, cart: { ...cart, total: cart.total * (1 - rate) } };
}
```

### Cycle 3：扩 seam

每个 cycle 加一个 seam 相关的 test（用户明确同意的），不写"未来可能用到"的测试。

---

## 例 2：Tautological 反模式 → 修正

### ❌ Tautological

```typescript
test('calculateTotal sums line items', () => {
  const items = [{ price: 10 }, { price: 5 }];
  const expected = items.reduce((sum, i) => sum + i.price, 0); // ← 用代码方式算
  expect(calculateTotal(items)).toBe(expected);
});
```

问题：若 `calculateTotal` 用 `items.reduce` 实现，测试按构造通过——永远绿。

### ✅ Independent source of truth

```typescript
test('calculateTotal sums line items', () => {
  expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
});
```

期望值是手算 literal。若 `calculateTotal` 写错，测试**必挂**。

---

## 例 3：Vertical vs Horizontal slicing

### ❌ Horizontal（先全测试再全实现）

```typescript
// 第一天：写 50 个测试覆盖想象的功能
test('validates code format', ...);
test('checks expiration', ...);
test('applies percentage', ...);
test('applies fixed amount', ...);
test('stacks with sale', ...);
test('rejects one-time use', ...);
// ... 50 个

// 第二天：实现
function applyDiscount(cart, code) { /* 50 个 case 的实现 */ }
```

问题：测试基于**想象的**行为，不是**真实的**。实现时发现想象错，测试全要重写。

### ✅ Vertical（tracer bullet）

```typescript
// Cycle 1: 最小 tracer
test('invalid code returns error', ...); 
// 实现 + 跑过

// Cycle 2: 加 1 个 case
test('valid code applies percentage', ...);
// 扩展 + 跑过

// Cycle 3-N: 每次加 1 个 case
```

每个 cycle 都基于上轮教你的东西。**避免承诺想象的 API**。

---

## 来源

本文示例基于 [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd/) 的 seam-driven 方法论，遵循 MIT License。