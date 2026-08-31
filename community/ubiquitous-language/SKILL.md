---
name: ubiquitous-language
description: Extract a DDD-style ubiquitous language glossary from the current conversation, flagging ambiguities and proposing canonical terms. Saves to UBIQUITOUS_LANGUAGE.md. Use when user wants to define domain terms, build a glossary, harden terminology, create a ubiquitous language, or mentions "domain model" or "DDD". NOT-FOR: 单人 CRUD 小项目(过度工程)/ 术语已无争议 / 需要持续演进的领域模型(用 domain-modeling 写 CONTEXT.md)。
disable-model-invocation: true
github_url: https://github.com/mattpocock/skills
github_hash: 60aa99c0230fbac087514ba5fca2ae6e519965fe
version: 1.1.0
created_at: 2026-04-26T00:00:00Z
last_verified: 2026-08-30
entry_point: SKILL.md
dependencies: []
tags: [ddd, domain-model, glossary, terminology, documentation, bounded-context]
---

# Ubiquitous Language

Extract and formalize domain terminology from the current conversation into a consistent glossary, saved to a local file.

## When this is worth it

术语表是**有维护成本的资产**。不值得建的时候建了,团队背上一份收益为零的负担。

**先过这道门槛 — 满足 ≥2 条才继续:**

- [ ] 领域词汇 ≥10 个,且**存在真实歧义**(同一词被用于不同概念,或不同词指同一概念)
- [ ] ≥2 人协作,或存在跨团队/跨职能交接
- [ ] 业务规则复杂度是项目的主要难点(不是技术实现)
- [ ] 已经因为术语误解产生过实际返工

**明确不值得做 — 命中任一条,直接回复"这个项目不值得建术语表"并停止:**

| 情况 | 为什么不值得 |
|---|---|
| 单人项目且无交接计划 | 语言在你脑子里就够了,写下来只是多一处要同步 |
| 以 CRUD 为主,领域逻辑薄 | Task/Item/List 这类词没有歧义可消 |
| 术语已经稳定且无争议 | 没有要解决的问题 |
| 会话中领域名词 < 5 个 | 输入不足,产出的会是一份看起来权威但内容空洞的文档 |

> 被拒绝时给出替代建议:"如果之后出现了术语争议,或者有人要接手这个项目,再回来做。"

## Bounded context — 语言只在上下文内统一

这是本 skill 最容易做错的地方。Evans 原著中 ubiquitous language 与 bounded context 是**配对概念**:

**同一个词在不同上下文里有不同的合法含义,这不是歧义,不能强行统一。**

```
billing 上下文的 Order    = 一笔应收账款的依据(关心金额、税、账期)
fulfillment 上下文的 Order = 一批要拣货发运的商品(关心库存、地址、时效)
```

这两个 `Order` 都是对的。把它们合并成一个定义,或把其中一个列进 "Aliases to avoid",都是错的。

**处理规则:**

| 情形 | 归类到哪 | 怎么写 |
|---|---|---|
| 同一上下文内,一词多义 | **Flagged ambiguities** | 必须消歧,给出推荐用法 |
| 同一上下文内,多词一义 | **Aliases to avoid** | 选定一个,其余列为别名 |
| **不同上下文**,同名不同义 | **各上下文独立成表** | 标注 `same term, different context`,**不合并** |

判断上下文边界的信号:不同团队负责、不同数据库/服务、不同业务节奏、术语在跨界对话时需要翻译。

## Process

1. **过 "When this is worth it" 门槛** — 不满足则停止,不要产出文件
2. **确认输入充分性** — 会话中领域名词 < 5 个时,先做其中一件:
   - 向用户提问补足
   - 读 `src/` 与既有 `README.md` / `docs/` 抽取候选术语
   - 两者都不可行 → 明确告知"输入不足,暂不生成",停止
3. **识别上下文边界** — 是单一上下文还是多个?多个则按上下文分表
4. **Scan the conversation** for domain-relevant nouns, verbs, and concepts
5. **Identify problems**:
   - Same word used for different concepts **within one context** (ambiguity)
   - Different words used for the same concept (synonyms)
   - Vague or overloaded terms
   - Same term across contexts (**not** an ambiguity — see Bounded context)
6. **Propose a canonical glossary** with opinionated term choices
7. **检查是否已有竞争文件** — 见 Boundaries;有 `CONTEXT.md` / `CONTEXT-MAP.md` 时不新建
8. **Write to `UBIQUITOUS_LANGUAGE.md`** in the working directory using the format below
9. **Output a summary** inline in the conversation

## Output Format

Write a `UBIQUITOUS_LANGUAGE.md` file with this structure:

```md
# Ubiquitous Language

**Last verified:** 2026-08-30
**Contexts covered:** billing, fulfillment

> 本文件是**意图**的记录;代码是**事实**。两者不一致时见文末 Suspected drift。

## Context: billing

| Term        | Definition                                              | Aliases to avoid      | Code anchor |
| ----------- | ------------------------------------------------------- | --------------------- | ----------- |
| **Order**   | 一笔应收账款的依据,含金额、税与账期                     | Purchase, transaction | `src/billing/order.ts` |
| **Invoice** | A request for payment sent to a customer after delivery | Bill, payment request | `src/billing/invoice.ts` |

## Context: fulfillment

| Term      | Definition                              | Aliases to avoid | Code anchor |
| --------- | --------------------------------------- | ---------------- | ----------- |
| **Order** | 一批待拣货发运的商品,含库存与收货地址   | Job, task        | `src/fulfillment/order.ts` |
| **Shipment** | 一次实际发运                          | Delivery         | `src/fulfillment/shipment.ts` |

> ⚠️ `Order` 在 billing 与 fulfillment 中含义不同 — **same term, different context**,不合并。
> 跨上下文对话时必须说明是哪个 Order。

## People

| Term         | Definition                                  | Aliases to avoid       | Code anchor |
| ------------ | ------------------------------------------- | ---------------------- | ----------- |
| **Customer** | A person or organization that places orders | Client, buyer, account | `src/shared/customer.ts` |
| **User**     | An authentication identity in the system    | Login, account         | `src/auth/user.ts` |

## Relationships

- An **Invoice** belongs to exactly one **Customer**
- A billing **Order** produces one or more **Invoices**
- A fulfillment **Order** produces one or more **Shipments**

## Example dialogue

> **Dev:** "When a **Customer** places an **Order**, do we create the **Invoice** immediately?"
> **Domain expert:** "No — an **Invoice** is only generated once a **Fulfillment** is confirmed. A single **Order** can produce multiple **Invoices** if items ship in separate **Shipments**."
> **Dev:** "So if a **Shipment** is cancelled before dispatch, no **Invoice** exists for it?"
> **Domain expert:** "Exactly. The **Invoice** lifecycle is tied to the **Fulfillment**, not the **Order**."

## Flagged ambiguities

- "account" was used to mean both **Customer** and **User** — these are distinct concepts: a **Customer** places orders, while a **User** is an authentication identity that may or may not represent a **Customer**.

## Unverified

以下定义无法从会话确认,需领域专家确认:

- **Settlement** *(unverified — needs domain expert confirmation)* — 推测指账期结束后的对账动作

## Suspected drift

*(重跑时填写;首次生成留空)*
```

## Rules

- **Be opinionated.** When multiple words exist for the same concept, pick the best one and list the others as aliases to avoid.
- **但要标注不确定。** 无法从会话判定的词,标 `(unverified — needs domain expert confirmation)` 并归入 Unverified 段。领域专家不在场时,武断裁决不应被当成权威结论固化。
- **Flag conflicts explicitly.** If a term is used ambiguously **within one context**, call it out in the "Flagged ambiguities" section with a clear recommendation.
- **不要跨上下文强行统一。** 同名不同义时分表并标注,见 Bounded context 段。
- **Only include terms relevant for domain experts.** Skip the names of modules or classes unless they have meaning in the domain language.
- **Keep definitions tight.** One sentence max. Define what it IS, not what it does.
- **Show relationships.** Use bold term names and express cardinality where obvious.
- **Only include domain terms.** Skip generic programming concepts (array, function, endpoint) unless they have domain-specific meaning.
- **Group terms by context first, then by natural clusters.** 单一上下文时不必强加 `## Context:` 标题。
- **给每个词加 code anchor**(定义该概念的文件/类型),便于后续漂移检测。无法定位时留空并说明。
- **Write an example dialogue.** A short conversation (3-5 exchanges) between a dev and a domain expert that demonstrates how the terms interact naturally. The dialogue should clarify boundaries between related concepts and show terms being used precisely.

<example>

## Example dialogue

> **Dev:** "How do I test the **sync service** without Docker?"

> **Domain expert:** "Provide the **filesystem layer** instead of the **Docker layer**. It implements the same **Sandbox service** interface but uses a local directory as the **sandbox**."

> **Dev:** "So **sync-in** still creates a **bundle** and unpacks it?"

> **Domain expert:** "Exactly. The **sync service** doesn't know which layer it's talking to. It calls `exec` and `copyIn` — the **filesystem layer** just runs those as local shell commands."

</example>

## Re-running

**任何时候 `UBIQUITOUS_LANGUAGE.md` 已存在**(不限于同一会话):

1. Read the existing `UBIQUITOUS_LANGUAGE.md`
2. **先跑 Drift check**(见下)—— 在合并新术语之前
3. Incorporate any new terms from subsequent discussion
4. Update definitions if understanding has evolved
5. Re-flag any new ambiguities
6. Rewrite the example dialogue to incorporate new terms
7. 更新 `Last verified` 日期

> **不要整体重写抹掉人工修订。** 已有文件里的人工调整(定义措辞、别名选择、上下文划分)优先于本次推断,除非有明确证据它已过期。

### Drift check

术语表最常见的死法不是写得不好,是**写完就过期**。代码里 `Invoice` 早已改名 `Statement`,而术语表仍是新人理解系统的权威文档。

重跑时对每个术语做:

1. `grep` 代码中的术语名(优先查 code anchor 指向的文件)
2. 记录三类不一致:

| 类型 | 判定 | 写入 Suspected drift |
|---|---|---|
| **术语在代码中消失** | grep 无命中,且 code anchor 文件已不存在 | `Invoice — 术语表有,代码无。已重命名?已删除?` |
| **代码出现未登记的同义词** | 代码里有 `Statement` 且语义近似 `Invoice` | `Statement — 代码中使用但术语表未登记,是否为 Invoice 的新名?` |
| **code anchor 失效** | 文件存在但不再定义该概念 | `Order — anchor 指向的文件已不含该定义` |

3. **不静默改任一侧。** 列出 Suspected drift 交用户裁决 —— 代码是事实,术语表是意图,可能是代码改错了名,也可能是术语表该更新。

```md
## Suspected drift

- **Invoice** — 术语表定义为「交付后发出的付款请求」,但 `src/billing/` 中已无 `Invoice`,
  出现了 `Statement`。是重命名吗?若是,术语表该改;若 `Statement` 是新概念,该新增条目。
```

## Boundaries

本 skill 与同上游的 `domain-modeling` 职责不同,**不要同时产出两份术语表**:

| 用本 skill(`ubiquitous-language`) | 用 `domain-modeling` |
|---|---|
| 一次性从会话抽取术语快照 | 持续演进领域模型 |
| 产出 `UBIQUITOUS_LANGUAGE.md` | 产出 `CONTEXT.md` / `CONTEXT-MAP.md` + ADR |
| 只做术语澄清 | 主动挑战术语、构造边界场景、记录决策 |

**冲突处理:**

- 仓库已有 `CONTEXT.md` 或 `CONTEXT-MAP.md` → **不要新建 `UBIQUITOUS_LANGUAGE.md`**,改为更新既有文件。下游 skill(如 `improve-codebase-architecture`)消费的是 `CONTEXT.md`,新建竞争文件会破坏单一真相来源。
- 两个文件都已存在 → 提示用户合并,并建议保留 `CONTEXT.md` 作为权威。

其他相关:

- 需要判断**概念本身**是否成立(而非命名)→ `deep-concept-analyzer`
- 需要改架构而非改语言 → `improve-codebase-architecture`

## Examples

- [01 · 多上下文电商](examples/01-multi-context-ecommerce.md) — 同名不同义不能合并;三个月后 Drift check 发现术语已改名
- [02 · 何时该拒绝](examples/02-when-to-refuse.md) — 小型 CRUD 项目正确的做法是不生成,并给出理由与回来的时机

## 变更记录

### v1.1.0 (2026-08-30)

经 AB 双轴 review 后修复(2 P0 + 5 P1):

**P0**
- 新增 `## When this is worth it` 门槛与明确的 skip 条件 —— 原先无任何规模判断,3 文件的 Todo CLI 也会照常产出正式术语表 + 关系图 + 专家对话,是教科书级 DDD 过度工程
- `Re-running` 去掉 `in the same conversation` 限制;新增 `### Drift check` 代码漂移检测(术语消失 / 未登记同义词 / anchor 失效三类),规定不一致时由用户裁决而非静默改动;输出格式加 `Last verified` 与每词 `Code anchor`

**P1**
- 新增 `## Bounded context` 段 —— 原先 `bounded context` 全文零出现,而它是 Evans 原著中与 ubiquitous language 配对的概念。缺失导致跨上下文同名不同义(billing 的 `Order` ≠ fulfillment 的 `Order`)被误判为歧义强行统一。输出格式改为按上下文分表
- Process 新增输入充分性门槛:领域名词 < 5 个时先提问或读代码补足,不足则明确拒绝生成
- 新增 `## Boundaries` —— 与同上游 `domain-modeling` 职责划分。后者产出 `CONTEXT.md` 且下游 `improve-codebase-architecture` 消费的是它;检测到既有 `CONTEXT.md` / `CONTEXT-MAP.md` 时改为更新而非新建,避免双术语表竞争
- description 补 NOT-FOR,使边界在路由阶段可见

**P2**
- `Be opinionated` 加逃生阀:无法从会话判定的词标 `(unverified — needs domain expert confirmation)` 并归入新增的 `Unverified` 段,避免 LLM 武断裁决被当成权威结论固化
