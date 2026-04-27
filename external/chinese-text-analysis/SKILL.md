---
name: chinese-text-analysis
description: 中文文本NLP分析管道 - 情感正负面判断、关键词提取、语义主题聚类，适用于小红书/抖音帖子和评论批量分析
github_url: https://github.com/fxsjy/jieba https://github.com/isnowfy/snownlp https://github.com/MaartenGr/BERTopic
github_hash: jieba:67fa2e36 snownlp:fad6ae77 bertopic:b2ce0842
version: 1.0.0
created_at: 2026-04-27
tags: [nlp, sentiment-analysis, keyword-extraction, semantic-clustering, chinese, text-analysis, social-media]
entry_point: scripts/analyze.py
dependencies: ["jieba==0.42.1", "snownlp", "bertopic", "sentence-transformers"]
---

# Chinese Text Analysis Skill

中文文本NLP分析管道，专为社媒帖子/评论批量分析设计（Step 7 of 小红书/抖音采集工作流）。

## 触发场景

- 对帖子/评论做情感分析（正面/负面/中性）
- 提取帖子主要关键词和高频词
- 对大量帖子/评论做语义聚类，发现主题群
- 从 MediaCrawler 采集结果做二次分析

## 安装

```bash
pip install jieba snownlp bertopic sentence-transformers pandas
# 或
uv add jieba snownlp bertopic sentence-transformers pandas
```

## 分析能力

### 1. 情感分析（snownlp）

```python
from snownlp import SnowNLP

def analyze_sentiment(text: str) -> dict:
    """返回情感得分和标签"""
    s = SnowNLP(text)
    score = s.sentiments  # 0.0~1.0，越高越正面
    label = "正面" if score > 0.6 else ("负面" if score < 0.4 else "中性")
    return {"score": round(score, 3), "label": label}

# 批量分析评论
def batch_sentiment(texts: list[str]) -> list[dict]:
    return [analyze_sentiment(t) for t in texts]
```

**精度说明**：snownlp基于朴素贝叶斯，在购物评论语料上训练，社媒文本精度约70-80%。
如需更高精度，可替换为 `transformers` + `IDEA-CCNL/Erlangshen-Roberta-110M-Sentiment`（中文情感分类微调模型）。

### 2. 关键词提取（jieba）

```python
import jieba
import jieba.analyse

def extract_keywords(text: str, topk: int = 10) -> list[tuple]:
    """TF-IDF关键词提取"""
    keywords = jieba.analyse.extract_tags(text, topK=topk, withWeight=True)
    return keywords  # [(词, 权重), ...]

def extract_keywords_textrank(text: str, topk: int = 10) -> list[tuple]:
    """TextRank关键词提取（更适合长文本）"""
    return jieba.analyse.textrank(text, topK=topk, withWeight=True)

# 合并多篇文章提取高频词
def corpus_keywords(texts: list[str], topk: int = 20) -> list[tuple]:
    combined = " ".join(texts)
    return extract_keywords(combined, topk=topk)
```

### 3. 语义聚类（BERTopic）

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import jieba

def cluster_topics(texts: list[str], n_topics: int = 10) -> dict:
    """
    对文本列表做语义主题聚类
    返回：每条文本所属主题 + 主题关键词
    """
    # 中文分词预处理
    tokenized = [" ".join(jieba.cut(t)) for t in texts]

    # 使用多语言模型（支持中文）
    embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    topic_model = BERTopic(
        embedding_model=embedding_model,
        language="chinese (simplified)",
        nr_topics=n_topics,
        verbose=False
    )

    topics, probs = topic_model.fit_transform(tokenized)

    topic_info = topic_model.get_topic_info()
    topic_words = {
        row["Topic"]: row["Representation"]
        for _, row in topic_info.iterrows()
        if row["Topic"] != -1
    }

    return {
        "assignments": topics,       # 每条文本的主题ID列表
        "topic_words": topic_words,  # 每个主题的代表词
        "topic_info": topic_info.to_dict("records")
    }
```

**首次运行**：自动从HuggingFace下载 `paraphrase-multilingual-MiniLM-L12-v2`（约120MB）。
如无法访问HuggingFace，可本地镜像：`HF_ENDPOINT=https://hf-mirror.com python analyze.py`

### 4. 完整分析管道（对接 MediaCrawler 输出）

```python
import sqlite3
import pandas as pd
import jieba.analyse
from snownlp import SnowNLP
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

def analyze_crawl_results(db_path: str, platform: str = "xhs") -> dict:
    """
    从 MediaCrawler SQLite 数据库读取数据并执行完整NLP分析
    
    Args:
        db_path: MediaCrawler生成的SQLite路径（如 data/xhs.db）
        platform: 平台名称
    
    Returns:
        {
          "post_sentiments": DataFrame,   # 帖子情感
          "comment_sentiments": DataFrame, # 评论情感
          "top_keywords": list,            # 全局关键词
          "topic_clusters": dict           # 语义聚类结果
        }
    """
    conn = sqlite3.connect(db_path)

    # 读取帖子
    posts = pd.read_sql("SELECT note_id, title, desc, liked_count, collected_count, comment_count FROM xhs_note", conn)

    # 读取评论
    comments = pd.read_sql("SELECT comment_id, note_id, content, liked_count FROM xhs_note_comment", conn)
    conn.close()

    # 1. 帖子情感
    posts["sentiment_score"] = posts["desc"].apply(
        lambda x: SnowNLP(str(x)).sentiments if pd.notna(x) and x else 0.5
    )
    posts["sentiment_label"] = posts["sentiment_score"].apply(
        lambda s: "正面" if s > 0.6 else ("负面" if s < 0.4 else "中性")
    )

    # 2. 评论情感
    comments["sentiment_score"] = comments["content"].apply(
        lambda x: SnowNLP(str(x)).sentiments if pd.notna(x) and x else 0.5
    )
    comments["sentiment_label"] = comments["sentiment_score"].apply(
        lambda s: "正面" if s > 0.6 else ("负面" if s < 0.4 else "中性")
    )

    # 3. 关键词（合并所有帖子正文）
    all_text = " ".join(posts["desc"].dropna().tolist())
    top_keywords = jieba.analyse.extract_tags(all_text, topK=30, withWeight=True)

    # 4. 语义聚类（帖子标题+正文）
    texts_for_cluster = (posts["title"].fillna("") + " " + posts["desc"].fillna("")).tolist()
    if len(texts_for_cluster) >= 10:
        cluster_result = cluster_topics(texts_for_cluster)
    else:
        cluster_result = {"note": "样本量不足10条，跳过聚类"}

    return {
        "post_sentiments": posts[["note_id", "title", "sentiment_score", "sentiment_label"]],
        "comment_sentiments": comments[["comment_id", "note_id", "sentiment_score", "sentiment_label"]],
        "top_keywords": top_keywords,
        "topic_clusters": cluster_result
    }
```

## 使用示例（完整工作流）

```bash
# Step 1-6: 用 MediaCrawler 采集（见 mediacrawler skill）
cd /tmp/MediaCrawler
uv run main.py --platform xhs --lt qrcode --type search
# 数据保存到 data/xhs.db

# Step 7: NLP分析
python scripts/analyze.py --db /tmp/MediaCrawler/data/xhs.db --platform xhs --output report.json
```

## 输出报告结构

```json
{
  "summary": {
    "total_posts": 50,
    "positive_ratio": 0.72,
    "negative_ratio": 0.18,
    "neutral_ratio": 0.10,
    "comment_positive_ratio": 0.65
  },
  "top_keywords": [["好用", 0.32], ["推荐", 0.28], ...],
  "topic_clusters": {
    "0": ["护肤", "精华", "保湿"],
    "1": ["平价", "学生", "性价比"],
    ...
  },
  "post_sentiments": [...],
  "comment_sentiments": [...]
}
```

## 精度升级路径

| 层级 | 工具 | 精度 | 成本 |
|------|------|------|------|
| 基础 | snownlp | ~70% | 极轻量 |
| 进阶 | HuggingFace中文情感模型 | ~88% | 需GPU/内存 |
| 最佳 | Claude API分析 | ~95% | 按token计费 |

## References

- [jieba文档](https://github.com/fxsjy/jieba#readme)
- [snownlp API](https://github.com/isnowfy/snownlp#readme)  
- [BERTopic文档](https://maartengr.github.io/BERTopic/)
- [中文情感模型列表（HuggingFace）](https://huggingface.co/models?language=zh&pipeline_tag=text-classification)
