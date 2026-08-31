# 案例:多上下文电商 —— 同名不同义不能合并

**演示重点**:`Order` 在两个上下文里都是对的。把它们合并是错的。

---

## 输入会话(节选)

> **用户**:我们的系统有点乱。财务那边说 Order 是应收账款的依据,仓库那边说 Order 是拣货单。
> 客服还会说"这个 account 有问题",有时指公司客户,有时指登录账号。
> 另外 Invoice 和 Statement 混用,Shipment 和 Delivery 也混用。

> **用户**:财务和仓库是两个团队,各自有独立的服务和数据库。

---

## 门槛判断

先过 `When this is worth it`:

| 条件 | 判定 |
|---|---|
| 领域词汇 ≥10 且存在真实歧义 | ✅ Order / Invoice / Statement / Shipment / Delivery / account / Customer / User… 且 `account` 确有一词多义 |
| ≥2 人协作或跨团队交接 | ✅ 财务与仓库两个团队 |
| 业务规则复杂度是主要难点 | ✅ 订单在两个域的生命周期不同 |
| 已因术语误解返工 | 未知,但已有认知冲突 |

满足 3 条 → **继续**。

## 上下文边界识别

用户明确说了"财务和仓库是两个团队,各自有独立的服务和数据库" —— 这命中了上下文边界的两个信号(不同团队负责、不同数据库/服务)。

**结论:两个 bounded context — `billing` 与 `fulfillment`。**

## 关键判断:`Order` 怎么处理

这是本案例的核心。三种做法里只有一种对:

| 做法 | 对错 | 为什么 |
|---|---|---|
| 合并成一个定义:"Order = 客户的购买请求" | ❌ | 抹掉了两个域各自关心的属性,两边都不认这个定义 |
| 选财务的定义,把仓库的列进 "Aliases to avoid" | ❌ | 仓库的用法不是"该避免的别名",它在自己上下文里是正确的 |
| **各上下文独立成表,标注 same term, different context** | ✅ | 两个定义都保留,并明确跨界对话时要说清是哪个 |

同理 `Invoice`/`Statement`:需要先确认它们是**同义词**还是**两个概念**。会话里没说清 → 归入 Unverified,不武断裁决。

---

## 产出的 `UBIQUITOUS_LANGUAGE.md`

```md
# Ubiquitous Language

**Last verified:** 2026-08-30
**Contexts covered:** billing, fulfillment

> 本文件是**意图**的记录;代码是**事实**。两者不一致时见文末 Suspected drift。

## Context: billing

| Term | Definition | Aliases to avoid | Code anchor |
|---|---|---|---|
| **Order** | 一笔应收账款的依据,含金额、税率与账期 | Purchase, transaction | `src/billing/order.ts` |
| **Invoice** | 交付确认后向客户发出的付款请求 | Bill, payment request | `src/billing/invoice.ts` |

## Context: fulfillment

| Term | Definition | Aliases to avoid | Code anchor |
|---|---|---|---|
| **Order** | 一批待拣货发运的商品,含库存占用与收货地址 | Job, picking task | `src/fulfillment/order.ts` |
| **Shipment** | 一次实际发运动作 | Delivery, dispatch | `src/fulfillment/shipment.ts` |

> ⚠️ **`Order` — same term, different context,不合并。**
> billing 的 Order 关心钱,fulfillment 的 Order 关心货。
> 跨团队对话时必须说明是 billing Order 还是 fulfillment Order。

## People(跨上下文共享)

| Term | Definition | Aliases to avoid | Code anchor |
|---|---|---|---|
| **Customer** | 下单的个人或组织 | Client, buyer, account | `src/shared/customer.ts` |
| **User** | 系统中的一个认证身份 | Login, account | `src/auth/user.ts` |

## Relationships

- 一个 billing **Order** 产生一或多个 **Invoice**
- 一个 fulfillment **Order** 产生一或多个 **Shipment**
- 一个 **Invoice** 恰属于一个 **Customer**
- 一个 **Customer** 可对应零到多个 **User**

## Example dialogue

> **Dev:** "客户取消了,我要把 **Order** 标成 cancelled — 哪个 Order?"
> **Domain expert:** "两个都要动,但顺序有讲究。先取消 fulfillment **Order**,释放库存占用;
> 只有还没生成 **Invoice** 时才能取消 billing **Order**。"
> **Dev:** "那如果 **Invoice** 已经发出去了?"
> **Domain expert:** "那就不是取消,是退款流程 —— billing **Order** 保留,另开一笔冲销。
> 这也是为什么两边不能共用一个 Order 状态机。"

## Flagged ambiguities

- **"account"** 在会话中同时指 **Customer**(公司客户)与 **User**(登录账号)。
  这是同一上下文内的一词多义,必须消歧:
  谈商务关系用 **Customer**,谈登录/权限用 **User**。「account」一词建议弃用。

## Unverified

- **Statement** *(unverified — needs domain expert confirmation)* —
  会话中与 **Invoice** 混用,但无法判断是同义词还是不同概念
  (可能是"对账单"= 多张 Invoice 的汇总)。需财务确认。
- **Delivery** *(unverified — needs domain expert confirmation)* —
  与 **Shipment** 混用。若指"送达这一事件"而非"发运动作",则是独立概念而非别名。

## Suspected drift

*(首次生成,留空)*
```

---

## 三个月后重跑:Drift check 起作用

> **用户**:更新一下术语表。

按 `Re-running`,先跑 Drift check:

```bash
grep -rn "Invoice" src/billing/     # 无命中
ls src/billing/invoice.ts           # 文件不存在
grep -rn "Statement" src/billing/   # 12 处命中
```

产出:

```md
## Suspected drift

- **Invoice** — 术语表定义为「交付确认后的付款请求」,但 `src/billing/` 已无 `Invoice`,
  code anchor `src/billing/invoice.ts` 不存在。同时出现了 `Statement`(12 处)。
  **是重命名吗?** 若是,术语表该把 Invoice 改为 Statement;
  若 Statement 是新概念(对账单),该新增条目并说明与 Invoice 的关系。
  **未裁决前不改动任一侧。**
```

这正是 Drift check 的价值:**没有它,新人会按"Invoice"去代码里找,找不到,然后自己猜。**

---

## 本例演示了什么

| 要点 | 体现在哪 |
|---|---|
| 门槛判断先行 | 满足 3 条才继续,不是无条件生成 |
| 上下文边界靠信号识别 | "两个团队 + 独立数据库" → 两个 context |
| 同名不同义不合并 | `Order` 分表 + 显式标注 |
| 同上下文一词多义要消歧 | `account` 进 Flagged ambiguities |
| 不确定的不武断 | `Statement` / `Delivery` 进 Unverified |
| code anchor 使漂移可检测 | 三个月后 grep 发现 Invoice 消失 |
| 漂移不静默修 | 列出交用户裁决 |
