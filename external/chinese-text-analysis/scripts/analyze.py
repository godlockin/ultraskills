#!/usr/bin/env python3
"""
chinese-text-analysis entry point
=================================

CLI wrapper for the four NLP capabilities declared in SKILL.md:
  - sentiment (SnowNLP)
  - keyword extraction (jieba.analyse)
  - semantic topic clustering (BERTopic + multilingual MiniLM)
  - full pipeline (analyze_crawl_results) against MediaCrawler SQLite

Usage:
  python scripts/analyze.py sentiment  --text "..."
  python scripts/analyze.py keywords  --text "..." --top-k 30
  python scripts/analyze.py cluster   --input texts.jsonl
  python scripts/analyze.py pipeline  --db data/xhs.db --platform xhs --output report.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from typing import Iterable

import pandas as pd

# Reuse the module-level code blocks from SKILL.md.
# They are duplicated here rather than imported because SKILL.md is the
# canonical source for the team and we want a single-file CLI.
import jieba
import jieba.analyse
from snownlp import SnowNLP


# ---------------------------------------------------------------------------
# Sentiment
# ---------------------------------------------------------------------------

_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "️"
    "]+",
    flags=re.UNICODE,
)


def _strip_emoji(text: str) -> str:
    return _EMOJI_RE.sub("", text or "").strip()


def sentiment_score(text: str) -> float:
    """Return SnowNLP sentiment in [0, 1]; 0.5 when input is empty/emoji-only."""
    cleaned = _strip_emoji(text)
    if not cleaned:
        return 0.5
    try:
        return float(SnowNLP(cleaned).sentiments)
    except Exception:  # noqa: BLE001
        return 0.5


def sentiment_label(score: float) -> str:
    if score > 0.6:
        return "正面"
    if score < 0.4:
        return "负面"
    return "中性"


# ---------------------------------------------------------------------------
# Keywords
# ---------------------------------------------------------------------------


def extract_keywords(text: str, top_k: int = 30) -> list[tuple[str, float]]:
    cleaned = _strip_emoji(text)
    if not cleaned:
        return []
    return jieba.analyse.extract_tags(cleaned, topK=top_k, withWeight=True)


# ---------------------------------------------------------------------------
# Topic clustering
# ---------------------------------------------------------------------------


def cluster_topics(texts: Iterable[str], min_samples: int = 10) -> dict:
    cleaned = [_strip_emoji(t) for t in texts if t and _strip_emoji(t)]
    if len(cleaned) < min_samples:
        return {"note": f"样本量不足 {min_samples} 条，跳过聚类", "assignments": [], "topic_words": {}}

    # Lazy import — heavy deps.
    from bertopic import BERTopic
    from sentence_transformers import SentenceTransformer

    embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    topic_model = BERTopic(embedding_model=embedding_model, verbose=False)
    topics, _probs = topic_model.fit_transform(cleaned)
    topic_info = topic_model.get_topic_info()

    topic_words: dict[int, list[str]] = {}
    for _, row in topic_info.iterrows():
        if row["Topic"] == -1:
            continue
        topic_words[int(row["Topic"])] = list(row["Representation"])

    return {
        "note": "ok",
        "assignments": [int(t) for t in topics],
        "topic_words": topic_words,
        "topic_info": topic_info.to_dict("records"),
    }


# ---------------------------------------------------------------------------
# Full pipeline (MediaCrawler SQLite)
# ---------------------------------------------------------------------------

# Table names by platform. Keep explicit; do NOT build SQL with f-string
# interpolation of user input — restrict to this whitelist.
_PLATFORM_TABLES = {
    "xhs": ("xhs_note", "xhs_note_comment"),
    "douyin": ("douyin_note", "douyin_note_comment"),
    "kuaishou": ("kuaishou_video", "kuaishou_video_comment"),
    "bilibili": ("bilibili_video", "bilibili_video_comment"),
    "weibo": ("weibo_note", "weibo_note_comment"),
}


def analyze_crawl_results(db_path: str, platform: str = "xhs") -> dict:
    if platform not in _PLATFORM_TABLES:
        raise ValueError(f"unsupported platform: {platform!r}; allowed: {list(_PLATFORM_TABLES)}")
    note_table, comment_table = _PLATFORM_TABLES[platform]

    if not os.path.isfile(db_path):
        raise FileNotFoundError(db_path)

    conn = sqlite3.connect(db_path)
    try:
        # Validate table exists before reading — fails loudly instead of
        # silently returning an empty DataFrame.
        existing = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        if note_table not in existing:
            raise RuntimeError(f"table '{note_table}' not found in {db_path}")
        if comment_table not in existing:
            raise RuntimeError(f"table '{comment_table}' not found in {db_path}")

        posts = pd.read_sql(
            f"SELECT note_id, title, desc, liked_count, collected_count, "
            f"comment_count FROM {note_table}",
            conn,
        )
        comments = pd.read_sql(
            f"SELECT comment_id, note_id, content, liked_count FROM {comment_table}",
            conn,
        )
    finally:
        conn.close()

    # Sentiment
    posts["sentiment_score"] = posts["desc"].apply(sentiment_score)
    posts["sentiment_label"] = posts["sentiment_score"].apply(sentiment_label)
    comments["sentiment_score"] = comments["content"].apply(sentiment_score)
    comments["sentiment_label"] = comments["sentiment_score"].apply(sentiment_label)

    # Drop direct identifiers before returning — callers should never see
    # raw user ids / nicknames from the source DB.
    drop_cols = [c for c in ("user_id", "nickname", "avatar") if c in posts.columns]
    posts_out = posts.drop(columns=drop_cols)
    drop_cols_c = [c for c in ("user_id", "nickname") if c in comments.columns]
    comments_out = comments.drop(columns=drop_cols_c)

    # Keywords
    all_text = " ".join(posts["desc"].dropna().astype(str).tolist())
    top_keywords = extract_keywords(all_text, top_k=30)

    # Topic clustering
    texts_for_cluster = (
        posts["title"].fillna("").astype(str) + " " + posts["desc"].fillna("").astype(str)
    ).tolist()
    cluster_result = cluster_topics(texts_for_cluster)

    return {
        "post_sentiments": posts_out[
            ["note_id", "title", "sentiment_score", "sentiment_label"]
        ],
        "comment_sentiments": comments_out[
            ["comment_id", "note_id", "sentiment_score", "sentiment_label"]
        ],
        "top_keywords": top_keywords,
        "topic_clusters": cluster_result,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _read_jsonl(path: str) -> list[str]:
    out: list[str] = []
    with open(path, "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if line:
                out.append(line)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="chinese-text-analysis CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_sent = sub.add_parser("sentiment", help="single-text sentiment")
    p_sent.add_argument("--text", required=True)

    p_kw = sub.add_parser("keywords", help="keyword extraction")
    p_kw.add_argument("--text", required=True)
    p_kw.add_argument("--top-k", type=int, default=30)

    p_clu = sub.add_parser("cluster", help="topic clustering from JSONL")
    p_clu.add_argument("--input", required=True, help="path to texts.jsonl")

    p_pipe = sub.add_parser("pipeline", help="full pipeline against MediaCrawler SQLite")
    p_pipe.add_argument("--db", required=True)
    p_pipe.add_argument("--platform", default="xhs")
    p_pipe.add_argument("--output", required=True)

    args = parser.parse_args(argv)

    if args.cmd == "sentiment":
        score = sentiment_score(args.text)
        print(json.dumps({"score": score, "label": sentiment_label(score)}, ensure_ascii=False))
        return 0

    if args.cmd == "keywords":
        print(json.dumps(extract_keywords(args.text, top_k=args.top_k), ensure_ascii=False))
        return 0

    if args.cmd == "cluster":
        result = cluster_topics(_read_jsonl(args.input))
        # Drop heavy topic_info when serialising.
        result.pop("topic_info", None)
        print(json.dumps(result, ensure_ascii=False, default=str))
        return 0

    if args.cmd == "pipeline":
        result = analyze_crawl_results(args.db, args.platform)
        summary = {
            "total_posts": int(len(result["post_sentiments"])),
            "total_comments": int(len(result["comment_sentiments"])),
            "positive_ratio": float(
                (result["post_sentiments"]["sentiment_label"] == "正面").mean()
            )
            if len(result["post_sentiments"])
            else 0.0,
            "negative_ratio": float(
                (result["post_sentiments"]["sentiment_label"] == "负面").mean()
            )
            if len(result["post_sentiments"])
            else 0.0,
            "neutral_ratio": float(
                (result["post_sentiments"]["sentiment_label"] == "中性").mean()
            )
            if len(result["post_sentiments"])
            else 0.0,
        }
        payload = {
            "summary": summary,
            "top_keywords": result["top_keywords"],
            "topic_clusters": {
                str(k): v for k, v in result["topic_clusters"].get("topic_words", {}).items()
            },
            "post_sentiments": result["post_sentiments"].to_dict(orient="records"),
            "comment_sentiments": result["comment_sentiments"].to_dict(orient="records"),
        }
        with open(args.output, "w", encoding="utf-8") as fp:
            json.dump(payload, fp, ensure_ascii=False, indent=2)
        print(f"wrote {args.output}")
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
