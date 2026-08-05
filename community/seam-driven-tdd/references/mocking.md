# When to Mock — Mock 时机

仅在**系统边界** mock：

- 外部 API（支付、邮件等）
- 数据库（有时——优先测试 DB）
- 时间/随机性
- 文件系统（有时）

不 mock：

- 你自己的类/module
- 内部协作者
- 你控制的任何东西

---

## 为可 Mock 性设计

在系统边界，设计易 mock 的接口：

**1. 用依赖注入**

传外部依赖进去，不要内部创建：

```typescript
// Easy to mock
function processPayment(order, paymentClient) {
  return paymentClient.charge(order.total);
}

// Hard to mock
function processPayment(order) {
  const client = new StripeClient(process.env.STRIPE_KEY);
  return client.charge(order.total);
}
```

**2. 优先 SDK 风格接口而非通用 fetcher**

为每个外部操作创建具体函数，而非一个带条件逻辑的通用函数：

```typescript
// GOOD: Each function is independently mockable
const api = {
  getUser: (id) => fetch(`/users/${id}`),
  getOrders: (userId) => fetch(`/users/${userId}/orders`),
  createOrder: (data) => fetch('/orders', { method: 'POST', body: data }),
};

// BAD: Mocking requires conditional logic inside the mock
const api = {
  fetch: (endpoint, options) => fetch(endpoint, options),
};
```

SDK 方式意味着：

- 每个 mock 返回一个具体 shape
- 测试 setup 中无条件逻辑
- 更易看出测试触及哪些端点
- 每端点类型安全

---

## 与 seam-driven-tdd 的协同

mock 时机 = **何时需要 adapter** = deep-module-design 里的 "one adapter = hypothetical seam, two adapters = real seam"：

- 单 mock（生产 + 单元测试）= **真实 seam** —— 应有 port interface
- 仅测试用 mock（生产直接 `new HttpClient()`）= **假设 seam** —— 直接传 mock 实例即可，不需要 interface

mock 设计应反映真实 seam 设计，不要为 mock 而造抽象。

---

## 来源

本文档改编自 [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd/mocking.md)，遵循 MIT License。