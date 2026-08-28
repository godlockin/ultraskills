# 优秀翻译案例对比

> 5 个典型翻译案例,展示"优秀翻译"的标准。

---

## 案例 1: 公式保留

**原文** (chapter 03/02. derivatives.md):

> The derivative of a function $f(x)$ at a point $x = a$ is defined as:
>
> $$f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$$

**❌ 错误译文**:

> 函数 $f(x)$ 在点 $x = a$ 处的导数定义为:
>
> $$f'(a) = lim_{h→0} [f(a+h) - f(a)] / h$$

(问题: lim → lim(不标准),→ 变字符,/ 变字符)

**✅ 正确译文**:

> 函数 $f(x)$ 在点 $x = a$ 处的导数定义为:
>
> $$f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$$

(公式 100% 一致,中文翻译流畅)

---

## 案例 2: 术语一致性

**原文**:

> Use **gradient descent** to optimize the loss function. Compared to **stochastic gradient descent (SGD)**, **Adam** achieves faster convergence.

**❌ 错误译文**:

> 使用**梯度下降法**优化损失函数。相比**随机梯度下降 (SGD)**, **Adam** 收敛更快。

(Ch07 又写"梯度下降算法",不一致)

**✅ 正确译文 (统一术语)**:

> 使用**梯度下降**优化损失函数。相比**随机梯度下降 (SGD)**, **Adam** 收敛更快。

(查 GLOSSARY.md,所有章节统一用"梯度下降")

---

## 案例 3: 代码块保留

**原文**:

> ```python
> def train_step(x, y):
>     """Single training step."""
>     y_pred = model(x)
>     loss = criterion(y_pred, y)
>     optimizer.zero_grad()
>     loss.backward()
>     optimizer.step()
>     return loss.item()
> ```

**❌ 错误译文**:

> ```python
> def train_step(x, y):
>     """单步训练。"""     # ← 注释被翻译了
>     y_pred = model(x)
>     loss = criterion(y_pred, y)
>     optimizer.zero_grad()
>     loss.backward()
>     optimizer.step()
>     return loss.item()  # 返回
> ```

(问题: 代码注释被翻译,违反铁律)

**✅ 正确译文**:

> ```python
> def train_step(x, y):
>     """Single training step."""
>     y_pred = model(x)
>     loss = criterion(y_pred, y)
>     optimizer.zero_grad()
>     loss.backward()
>     optimizer.step()
>     return loss.item()
> ```

(代码 100% 一致)

---

## 案例 4: 翻译腔

**原文**:

> The transformer architecture, which was introduced in 2017 by Vaswani et al. in their seminal paper "Attention is All You Need", has become the foundation of modern NLP systems, replacing earlier recurrent and convolutional approaches.

**❌ 错误译文 (翻译腔)**:

> Transformer 架构,这是由 Vaswani 等人在 2017 年在他们开创性的论文《Attention is All You Need》中所提出的,已经成为了现代 NLP 系统的基础,取代了早期的循环和卷积方法。

**✅ 正确译文 (流畅中文)**:

> Transformer 架构由 Vaswani 等人于 2017 年在开创性论文《Attention is All You Need》中提出。该架构现已成为现代 NLP 系统的基础,取代了早期的循环和卷积方法。

(拆长句,避免"这是...的"翻译腔)

---

## 案例 5: 链接 + 图片保留

**原文**:

> As shown in [Figure 1.1](../images/attention_diagram.svg), the attention mechanism computes:
>
> ![Attention Diagram](../images/attention_diagram.svg)
>
> See [Chapter 2](../chapter 02 - matrices/01. matrix basics.md) for matrix operations.

**❌ 错误译文**:

> 如图 [1.1] 所示,注意力机制计算:
>
> (图片丢失)
>
> 见第 2 章矩阵运算。

(图片和链接丢失)

**✅ 正确译文**:

> 如图 [1.1](../images/attention_diagram.svg) 所示,注意力机制计算:
>
> ![Attention Diagram](../images/attention_diagram.svg)
>
> 矩阵运算见 [第 02 章](../chapter 02 - matrices/01. matrix basics.md)。

(图片/链接全部保留,中文加注"第 02 章")

---

## 经验总结

| 维度 | 标准 |
|------|------|
| 公式 | 一字符不差 |
| 术语 | 全书一致 |
| 代码 | 一字符不差 |
| 链接 | 100% 保留 |
| 中文 | 流畅自然 |
| 标点 | 全角规范 |