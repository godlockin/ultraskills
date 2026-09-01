---
name: ai-techbook-translation
description: 英文→中文 AI/技术书籍翻译执行 skill — 配套 ai-techbook-translation-review 使用。从英文 Markdown 章节生成中文译稿,严守公式保留、术语一致、代码完整、链接保留 4 大铁律。包含分章翻译 SOP、术语表维护 (GLOSSARY.md)、标点规范化、风格指南、并行多 agent 协作翻译。触发场景: AI/技术书籍翻译、技术文档中文化、章节级英中翻译、术语库维护、译文初稿生成。
version: 1.0.0
tags: [translation, ai-techbook, technical-book, terminology, markdown, glossary, parallel-agents]
---

# AI Techbook Translation — AI/技术书籍翻译执行

> 配套 `ai-techbook-translation-review` 使用:本 skill 生成译稿,review skill 验收译稿。沉淀自《The Mathematics, Computer Science, and AI Compendium》中文版翻译项目 (25 章 × ~241 万字)。

## 🎯 定位 (Positioning)

**核心目标**: 将英文 Markdown 技术书籍翻译为高质量中文译稿。
**配套**: `ai-techbook-translation-review` 验证译文是否正确/完整/可靠。

## 🔄 翻译流程 (Workflow)

```
原文章节 (chapter 01 - vectors/01. vector spaces.md)
       ↓
[1] 术语检查 → GLOSSARY.md 锁定关键译法
       ↓
[2] 风格指南 → TRANSLATION_GUIDE.md 锁定风格
       ↓
[3] 翻译 agent → 章节级中文译稿
       ↓
[4] 自检 → 公式/代码/链接 100% 保留
       ↓
[5] 标点规范化 → 全角标点
       ↓
[6] 输出: zh/第01章 - 向量/01. 向量空间.md
       ↓
[7] review skill 验收 → 必须项 ≥ 9.0
```

## 📐 4 大铁律 (4 Iron Rules)

### 1. 公式 100% 保留

**绝对禁止**: 修改 `$...$` `$$...$$` `\(...\)` `\[...\]` 内的任何字符。

```markdown
原文: $f_\theta(x) = Wx + b$
译文: $f_\theta(x) = Wx + b$    # ← 完全一致
```

**例外**: 文档示例(反引号内)不视为公式。

### 2. 术语严格一致

**所有专有名词** 必须在 `GLOSSARY.md` 中定义,并在翻译前查表。

```
LLM → 大语言模型 (LLM)
RLHF → 人类反馈强化学习 (RLHF)
MoE → 混合专家 (MoE)
```

**同一本书中**同一术语必须用同一译法。

### 3. 代码完整

**代码块内** 所有字符(包括缩进、变量名、注释)必须**完全保留**。
**代码块外的**代码引用(如 `x_train.shape`)必须用反引号包裹。

```markdown
原文:
```python
def train(x, y):
    return model.fit(x, y)
```

译文:
```python
def train(x, y):
    return model.fit(x, y)
```
```

### 4. 链接保留

**所有链接** 必须保留,包括:
- 内部链接 `[text](chapter 02/...)`
- 外部 URL `[text](https://...)`
- 图片引用 `![alt](../images/...)`

**图片路径**: 通常 `../images/...` 不变 (或根据目录结构调整)。

## 📋 翻译 SOP (Standard Operating Procedure)

### Step 1: 准备 (Preparation)

```bash
# 1. 读原文 (整章,不是逐节)
cat "chapter 01 - vectors/01. vector spaces.md"

# 2. 查术语表
grep -A 1 "Vector Space" zh/GLOSSARY.md

# 3. 查风格指南
cat zh/TRANSLATION_GUIDE.md

# 4. 确认目录结构
ls zh/第01章 - 向量/    # 已存在 → 翻译到对应文件
```

### Step 2: 翻译 (Translation)

按**节**翻译,每节一次完成:

```markdown
## §01 Vector Spaces (向量空间)

### Definition 1.1
[定义 1.1 翻译]

### Example 1.1
[例 1.1 翻译]

[代码块原样保留]
```

**翻译要点**:
- ✅ 标题双译: `## Vector Spaces (向量空间)`
- ✅ 段落: 流畅中文,避免翻译腔
- ✅ 公式: 100% 原样
- ✅ 代码: 100% 原样
- ✅ 图片: 路径正确
- ✅ 表格: 行/列对齐保留

### Step 3: 自检 (Self-Check)

```bash
# 1. 公式完整性
diff <(grep -oP '\$\$.*?\$\$' src.md) \
     <(grep -oP '\$\$.*?\$\$' tgt.md)

# 2. 代码块数量
src_count=$(grep -c '^```' src.md)
tgt_count=$(grep -c '^```' tgt.md)
[ "$src_count" = "$tgt_count" ] || echo "代码块数量不一致!"

# 3. 图片数量
[ "$(grep -c '!\[' src.md)" = "$(grep -c '!\[' tgt.md)" ] || echo "图片数量不一致!"
```

### Step 4: 标点规范化

```python
# 自动规范化 (scripts/normalize_punctuation.py)
import re
content = open('zh/第01章/01. 向量空间.md').read()
content = re.sub(r'(?<=[a-zA-Z0-9])"(?=[a-zA-Z0-9])', '"', content)  # "..."
# ... etc
```

### Step 5: 输出

```
zh/第01章 - 向量/
├── 01. 向量空间.md        # 翻译完成
├── 02. 向量性质.md        # 待翻译
└── ...
```

## 🎯 翻译风格指南

### 语言风格

| 原英文 | 推荐中译 | 避免 |
|--------|----------|------|
| "we will see" | "我们会看到" | "我们将看到" |
| "let's consider" | "让我们考虑" | "假设" |
| "Note that" | "注意" / "需要指出" | "请注意" |
| "It's worth noting" | "值得说明" | "值得注意的是" |

### 标点

- 中文用全角: `,。;:!?()""''`
- 英文/数字旁用半角: `Git, Python, 2024`
- 引号: 中文 `"..."` , 英文代码内 `"..."`

### 数字与单位

- 数字保留原样: `100, 3.14, 1e-10`
- 单位中英对照: `1 GB (1 吉字节)` 或 `100 million (1 亿)`

### 长句处理

英文长句 → 中文拆短句,用句号/分号断开:

```markdown
原文: The transformer architecture, which was introduced in 2017
by Vaswani et al. in the seminal paper "Attention is All You Need",
has become the foundation of modern NLP systems, replacing earlier
recurrent and convolutional approaches.

译文: Transformer 架构由 Vaswani 等人于 2017 年在开创性论文
《Attention is All You Need》中提出。该架构已成为现代 NLP 系统
的基础,取代了早期的循环和卷积方法。
```

## 🛠 工具集 (Toolbox)

> 部分脚本 / 模板仅作占位描述；本仓库**实际仅包含** `glossary_init.py` / `normalize_punctuation.py` / `test_normalize_punctuation.py` / `glossary-template.md` / `translation-guide-template.md` / `good-translation.md`。其它文件（`parallel_translate.py` / `markdown_clean.py` / `chapter-template.md` / `glossary-sample.md`）**未实现**，使用时按需创建或删除对应条目。

### scripts/（已实现）

| 文件 | 用途 |
|------|------|
| `normalize_punctuation.py` | 全角标点规范化（含 URL 保护、emoji 跳过） |
| `glossary_init.py` | 从原文提取候选术语 |
| `test_normalize_punctuation.py` | normalize 的最小回归 |

### scripts/（占位 — 尚未实现）

| 文件 | 状态 |
|------|------|
| `parallel_translate.py` | **TBD** — 并行多 agent 翻译协调器 |
| `markdown_clean.py` | **TBD** — 译文清理 |

### templates/（已实现）

| 文件 | 用途 |
|------|------|
| `translation-guide-template.md` | 翻译风格指南模板 |
| `glossary-template.md` | 术语表模板 |

### templates/（占位）

| 文件 | 状态 |
|------|------|
| `chapter-template.md` | **TBD** — 章节翻译模板 |

### examples/

| 文件 | 用途 | 状态 |
|------|------|------|
| `good-translation.md` | 优秀翻译案例对比 | 已实现 |
| `glossary-sample.md` | 典型术语表示例 | **TBD** |

## ⚖️ 版权与翻译授权（必读）

> 本 skill 输出之前，**用户必须自行确认**：
>
> 1. **原书授权状态**：原书是闭源 / CC BY / 公有领域？翻译 25 章 × 241 万字前必须有合法授权（作者书面授权 / 出版社许可 / 公有领域声明 / CC BY-SA 等开放许可）。
> 2. **译文归属**：译文版权归译者 / 团队 / 机构；不得仅因翻译行为取得原作者权利。
> 3. **商用边界**：闭源或非 CC-BY 授权书籍的译文**禁止商用**；仅可作为个人学习、研究、内部使用。
> 4. **多国法规**：翻译 / 复制 / 传播受原书司法管辖地（DMCA / 中国著作权法 / EU 著作权指令）约束。
>
> 若不确定授权状态，**先停下来确认授权**，再开始翻译。

## 🤝 并行多 Agent 协作

**25 章书可分 5 个 agent 并行翻译**:

```
Agent 1: Ch01-05 (数学基础)
Agent 2: Ch06-10 (机器学习 + 视觉/语音)
Agent 3: Ch11-15 (系统/工程)
Agent 4: Ch16-20 (GPU + 推理 + 应用)
Agent 5: Ch21-25 (对齐 + Eval + Agent + 面试)
```

**每个 agent 加载**:
- `GLOSSARY.md` (术语表)
- `TRANSLATION_GUIDE.md` (风格指南)
- 自己负责的章节原文

**冲突解决**:
- 术语冲突 → 查 `GLOSSARY.md`
- 风格冲突 → 查 `TRANSLATION_GUIDE.md`
- 翻译策略冲突 → 主 agent 决策

## 📊 翻译质量自检清单

每章翻译完成后:

- [ ] 标题双译 (英文+中文)
- [ ] 所有公式 100% 保留
- [ ] 所有代码块 100% 保留
- [ ] 所有图片引用保留
- [ ] 所有链接保留
- [ ] 术语与 GLOSSARY.md 一致
- [ ] 中文标点规范
- [ ] 无翻译腔 (避免"我们将看到")
- [ ] 长句合理拆分
- [ ] 中文字符占比 ≥ 60%

## 🎓 案例研究

**项目**: maths-cs-ai-compendium 中文版 (25 章)

| 阶段 | 工作量 | 工具 |
|------|--------|------|
| 术语表 | 156 词条 | `glossary_init.py` + 手工 |
| 风格指南 | 50 条规范 | `translation-guide-template.md` |
| 翻译 | ~241 万字 | 5 agent 并行 |
| 自检 | 25 章 | `parallel_translate.py` |
| **review** | **0 critical 错误** | `ai-techbook-translation-review` |

## 🔗 与 review skill 配合

```
[翻译 skill] 生成译稿
       ↓
[review skill] 验收 (必须项 ≥ 9.0)
       ↓
不通过 → 回到翻译 skill 修复
       ↓
通过 → 进入排版/Pandoc 阶段
```

## 📝 更新日志

**v1.0.0 (2026-07-31)**
- 初版: 翻译执行 skill
- 4 大铁律 (公式/术语/代码/链接)
- 翻译 SOP 5 步
- 并行多 agent 协作框架
- 配套 ai-techbook-translation-review