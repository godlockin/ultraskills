# 术语表模板 (GLOSSARY Template)

> 所有专有名词的标准译法表。所有译者必须遵守。

## 使用说明

1. **新术语**: 在 `glossary_init.py` 提取候选 → 人工校对 → 加入本表
2. **术语更新**: 在 PR 中讨论 → 主 maintainer 决策 → 同步全章
3. **冲突解决**: 同一概念已有译法,不得擅自修改

---

## 1. AI / 机器学习核心术语

| English | 中文 | 说明 |
|---------|------|------|
| Artificial Intelligence (AI) | 人工智能 | |
| Machine Learning (ML) | 机器学习 | |
| Deep Learning (DL) | 深度学习 | |
| Neural Network (NN) | 神经网络 | |
| Transformer | Transformer | 保留英文 |
| Large Language Model (LLM) | 大语言模型 | |
| Foundation Model | 基础模型 | |
| Reinforcement Learning (RL) | 强化学习 | |
| Supervised Learning | 监督学习 | |
| Unsupervised Learning | 无监督学习 | |
| Self-Supervised Learning | 自监督学习 | |
| Pre-training | 预训练 | |
| Fine-tuning | 微调 | |
| Transfer Learning | 迁移学习 | |
| Few-shot Learning | 小样本学习 | |
| Zero-shot Learning | 零样本学习 | |
| In-context Learning | 上下文学习 | |

## 2. LLM 训练与对齐

| English | 中文 | 说明 |
|---------|------|------|
| Pre-training | 预训练 | |
| SFT (Supervised Fine-Tuning) | 监督微调 | |
| RLHF (Reinforcement Learning from Human Feedback) | 人类反馈强化学习 | |
| DPO (Direct Preference Optimization) | 直接偏好优化 | |
| GRPO (Group Relative Policy Optimization) | 组相对策略优化 | |
| Constitutional AI (CAI) | 宪法 AI | |
| Reward Model (RM) | 奖励模型 | |
| Process Reward Model (PRM) | 过程奖励模型 | |
| Outcome Reward Model (ORM) | 结果奖励模型 | |
| KL Penalty | KL 惩罚 | |
| KL Divergence | KL 散度 | |

## 3. 模型架构

| English | 中文 | 说明 |
|---------|------|------|
| Attention | 注意力 | |
| Self-Attention | 自注意力 | |
| Multi-Head Attention | 多头注意力 | |
| Cross-Attention | 交叉注意力 | |
| MoE (Mixture of Experts) | 混合专家 | |
| KV Cache | KV 缓存 | |
| PagedAttention | 分页注意力 | |
| Flash Attention | 快速注意力 | |
| Mamba | Mamba | 保留英文 (选择性状态空间模型) |
| State Space Model (SSM) | 状态空间模型 | |
| LoRA (Low-Rank Adaptation) | 低秩适配 | |
| Quantization | 量化 | |
| Distillation | 蒸馏 | |

## 4. AI Agent

| English | 中文 | 说明 |
|---------|------|------|
| Agent | 智能体 / Agent | 首次出现双译 |
| Tool | 工具 | |
| Function Calling | 函数调用 | |
| ReAct | ReAct | 保留英文 (Reason + Act) |
| Chain of Thought (CoT) | 思维链 | |
| Tree of Thoughts (ToT) | 思维树 | |
| Reflexion | Reflexion | 保留英文 |
| Multi-Agent | 多智能体 | |
| MCP (Model Context Protocol) | 模型上下文协议 | |
| Computer Use | Computer Use | 保留英文 |
| Operator | Operator | OpenAI Operator |
| Browser-Use | Browser-Use | 保留英文 |

## 5. RAG 与检索

| English | 中文 | 说明 |
|---------|------|------|
| RAG (Retrieval-Augmented Generation) | 检索增强生成 | |
| Vector Database | 向量数据库 | |
| Embedding | 嵌入向量 / Embedding | 首次双译 |
| Chunking | 分块 | |
| Hybrid Search | 混合检索 | |
| Re-ranking | 重排序 | |
| BM25 | BM25 | 保留 |

## 6. 评测与安全

| English | 中文 | 说明 |
|---------|------|------|
| Benchmark | 基准 / 基准测试 | |
| MMLU | MMLU | 保留 |
| HumanEval | HumanEval | 保留 |
| GSM8K | GSM8K | 保留 |
| LMSYS Arena / Chatbot Arena | LMSYS 竞技场 / Chatbot Arena | 首次双译 |
| Elo Rating | Elo 评分 | |
| LLM-as-Judge | LLM 当裁判 | |
| Jailbreak | 越狱 | |
| Prompt Injection | 提示注入 | |
| Alignment | 对齐 | |
| Mechanistic Interpretability | 机制可解释性 | |
| Sparse Autoencoder (SAE) | 稀疏自编码器 | |
| Circuit | 电路 | |
| Mesa-Optimizer | 元优化器 | |

## 7. 分布式与系统

| English | 中文 | 说明 |
|---------|------|------|
| Data Parallel (DP) | 数据并行 | |
| Model Parallel (MP) | 模型并行 | |
| Tensor Parallel (TP) | 张量并行 | |
| Pipeline Parallel (PP) | 流水线并行 | |
| AllReduce | AllReduce | 保留 |
| Ring AllReduce | 环形 AllReduce | |
| ZeRO | ZeRO | 保留 |
| FSDP | FSDP | 保留 |
| Mixed Precision | 混合精度 | |
| BF16 | BF16 | 保留 |
| FP8 | FP8 | 保留 |

## 8. 数据与统计

| English | 中文 | 说明 |
|---------|------|------|
| Token | Token | 保留 |
| Vocabulary | 词表 | |
| Byte Pair Encoding (BPE) | 字节对编码 | |
| WordPiece | WordPiece | 保留 |
| Perplexity (PPL) | 困惑度 | |
| Tokenizer | 分词器 | |

---

## 修订日志

| 日期 | 修改 | 修改人 |
|------|------|--------|
| 2026-07-31 | 初版 156 词条 | @maintainer |