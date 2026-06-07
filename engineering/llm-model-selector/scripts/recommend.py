#!/usr/bin/env python3
"""
recommend.py - 5 维度评分推荐 LLM model

权重 (质量+速度优先, 价格次要):
  Task affinity   35%   任务匹配度
  Quality         25%   模型质量 (provider tier + family tier + recency)
  Speed           20%   推理速度 (latency proxy)
  Context         10%   上下文 headroom
  Cost            10%   成本效率

Usage:
    python3 recommend.py --task code --context 128k --budget 3 --top 3
    python3 recommend.py --task reasoning --context 1M --privacy open_weights
    python3 recommend.py --task vision --latency realtime

数据源: <skill>/.cache/models.json (由 fetch_models.py 维护)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
CACHE_FILE = SKILL_DIR / ".cache" / "models.json"

# ---------- 评分参数 ----------
# 各任务对应的 TOP_TIER 模型 (质量 S/A 级)
TOP_TIER = {
    "code":         ["gpt-5", "claude-opus-4", "claude-sonnet-4", "qwen2.5-coder-32b", "deepseek-coder", "codestral-25", "grok-code"],
    "reasoning":    ["o1", "o3", "claude-opus-4", "deepseek-r1", "qwq", "gemini-2.5-pro-thinking"],
    "creative":     ["claude-opus-4", "gpt-5", "gemini-2.5-pro"],
    "vision":       ["gpt-5", "claude-sonnet-4", "gemini-2.5-pro", "qwen2-vl-72b", "pixtral-large", "llama-3.2-90b-vision"],
    "audio":        ["gpt-4o-audio", "gemini-2.0-flash", "ultravox"],
    "long-context": ["gemini-2.5-pro", "claude-sonnet-4", "gpt-4.1", "qwen-long", "llama-4-scout"],
    "multilingual": ["qwen-2.5", "gpt-5", "claude-sonnet-4", "gemini-2.5-pro", "aya"],
    "embedding":    ["text-embedding-3", "bge-m3", "bge-large", "e5-large", "cohere-embed-v3", "voyage-3"],
    "chat":         ["gpt-5", "claude-sonnet-4", "gemini-2.5-pro", "llama-3.3-70b"],
}

# Tier 1: 顶级实验室 (OpenAI / Anthropic / Google / xAI / DeepSeek / Meta / Mistral / Alibaba)
# Tier 2: 可靠中型 (Snowflake / Groq / Together / Fireworks / DeepInfra)
# Tier 3: 聚合/小厂 (others)
TIER1_PROVIDERS = {"openai", "anthropic", "google", "xai", "deepseek", "meta", "mistral", "alibaba", "qwen"}
TIER2_PROVIDERS = {"groq", "together", "fireworks", "deepinfra", "snowflake-cortex", "amazon-bedrock", "microsoft-azure", "cloudflare-ai-gateway"}

# 速度 proxy: 模型名含这些 → 快
FAST_PATTERNS = ("mini", "flash", "nano", "haiku", "instant", "lite", "small", "turbo", "fast")
# 速度 proxy: 模型名含这些 → 慢
SLOW_PATTERNS = ("opus", "ultra", "max", "thinking", "pro", "preview", "experimental")

# ---------- 评分参数 ----------
TASK_FAMILIES = {
    "code":          ["gpt-5", "claude", "qwen-coder", "deepseek-coder", "codestral", "grok-code"],
    "reasoning":     ["o1", "o3", "claude-opus-thinking", "deepseek-r1", "qwq", "gemini-thinking"],
    "creative":      ["claude-opus", "gpt-5", "gemini-ultra", "claude"],
    "vision":        ["gpt-4o", "claude", "gemini", "qwen-vl", "llava", "pixtral"],
    "audio":         ["gpt-4o-audio", "gemini", "ultravox"],
    "long-context":  ["gemini-1.5", "claude", "gpt-4.1", "qwen-long"],
    "multilingual":  ["qwen", "gemma", "aya", "claude", "gpt"],
    "embedding":     ["text-embedding", "bge", "e5", "cohere-embed", "voyage"],
    "chat":          ["gpt-4o-mini", "claude-haiku", "gemini-flash", "llama-3"],
}

CONTEXT_THRESHOLDS = {
    "8k":   8000,
    "32k":  32000,
    "128k": 128000,
    "256k": 256000,
    "512k": 512000,
    "1m":   1000000,
    "2m":   2000000,
}

COST_BUDGETS = {
    "free":     0.0,
    "low":      1.0,
    "medium":   3.0,
    "high":     10.0,
    "any":      100.0,
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="LLM model recommender")
    p.add_argument("--task", default="code",
                   choices=list(TASK_FAMILIES.keys()),
                   help="任务类型 (default: code)")
    p.add_argument("--context", default="32k",
                   choices=list(CONTEXT_THRESHOLDS.keys()),
                   help="最低 context window (default: 32k)")
    p.add_argument("--budget", default="medium",
                   choices=list(COST_BUDGETS.keys()),
                   help="成本预算 per M tokens (default: medium=$3)")
    p.add_argument("--latency", default="interactive",
                   choices=["realtime", "interactive", "batch"],
                   help="延迟要求 (default: interactive)")
    p.add_argument("--privacy", default="any",
                   choices=["any", "open_weights", "on-prem"],
                   help="隐私约束 (default: any)")
    p.add_argument("--top", type=int, default=3,
                   help="返回 top N 推荐 (default: 3)")
    p.add_argument("--json", action="store_true",
                   help="只输出 JSON (无 markdown 表格)")
    return p.parse_args()


# ---------- 数据加载 ----------
def load_models() -> dict:
    if not CACHE_FILE.exists():
        print(f"✗ Cache not found: {CACHE_FILE}", file=sys.stderr)
        print(f"  Run fetch_models.py first.", file=sys.stderr)
        sys.exit(1)
    return json.loads(CACHE_FILE.read_text(encoding="utf-8"))


# ---------- 硬性过滤 ----------
def passes_hard_filters(model: dict, model_id: str, provider: dict, args: argparse.Namespace) -> bool:
    # Context window 下限
    ctx = (model.get("limit") or {}).get("context", 0)
    if ctx < CONTEXT_THRESHOLDS[args.context]:
        return False

    # 成本上限 (用 input cost 作 proxy)
    cost_in = (model.get("cost") or {}).get("input", 0) or 0
    if cost_in > COST_BUDGETS[args.budget]:
        return False

    # 隐私约束
    if args.privacy == "open_weights" and not model.get("open_weights"):
        return False

    # 排除 deprecated/alpha 状态
    status = model.get("status", "")
    if status in ("deprecated", "alpha"):
        return False

    return True


# ---------- 软性评分 ----------
def task_affinity(model_id: str, model: dict, task: str) -> float:
    """任务匹配: 0-100. 在 TOP_TIER 列表里加权最高"""
    score = 50.0
    fid = (model.get("family") or model_id).lower()
    name = model_id.lower()

    # Tier A: TOP_TIER 精确匹配 (+30)
    if any(kw in fid or kw in name for kw in TOP_TIER.get(task, [])):
        score += 30
    # Tier B: TASK_FAMILIES 兜底匹配 (+15)
    elif any(kw in fid or kw in name for kw in TASK_FAMILIES.get(task, [])):
        score += 15

    # 能力加分
    caps = model
    if task == "code" and caps.get("tool_call"):
        score += 10
    if task == "reasoning" and caps.get("reasoning"):
        score += 15
    if task == "vision" and "image" in (model.get("modalities", {}).get("input", [])):
        score += 15
    if task == "long-context" and (model.get("limit") or {}).get("context", 0) >= 500000:
        score += 10
    if task == "embedding":
        score += 5  # embedding 模型默认 OK

    return min(score, 100)


def quality_score(model_id: str, model: dict, provider_id: str, task: str) -> float:
    """模型质量: 0-100. 基于 provider tier + family tier + recency."""
    score = 50.0
    pid = provider_id.lower()
    name = model_id.lower()
    family = (model.get("family") or "").lower()

    # Provider tier (40 分封顶)
    if pid in TIER1_PROVIDERS:
        score += 40
    elif pid in TIER2_PROVIDERS:
        score += 25
    else:
        score += 10  # 聚合器/小厂

    # Family tier — 是否在 TOP_TIER (20 分)
    if any(kw in family or kw in name for kw in TOP_TIER.get(task, [])):
        score += 20
    elif any(kw in family or kw in name for kw in TASK_FAMILIES.get(task, [])):
        score += 10

    # Recency — release_date 越近越好 (+/- 10 分)
    release = (model.get("release_date") or "2024-01")[:7]  # YYYY-MM
    try:
        from datetime import datetime
        rel_months = (datetime.now().year - int(release[:4])) * 12 + (datetime.now().month - int(release[5:7]))
        if rel_months <= 6:
            score += 10  # 半年内
        elif rel_months <= 12:
            score += 5   # 一年内
        elif rel_months > 24:
            score -= 10  # 两年以上
    except (ValueError, IndexError):
        pass

    return max(0, min(score, 100))


def speed_score(model_id: str, model: dict, latency: str) -> float:
    """速度评分: 0-100. 基于模型名 + provider 路由能力."""
    score = 70.0
    mid = model_id.lower()
    provider_id = (model.get("_provider_id") or "").lower() if False else ""  # placeholder

    # 模型名 pattern
    is_fast = any(p in mid for p in FAST_PATTERNS)
    is_slow = any(p in mid for p in SLOW_PATTERNS)

    if is_fast and not is_slow:
        score = 95
    elif is_slow and not is_fast:
        score = 50
    elif is_fast and is_slow:
        score = 70  # 冲突, 中性
    else:
        score = 75  # unknown

    # provider 加速加成 (Groq / Together / Fireworks 路由快)
    # 通过 model_id 路径推断或不在此处处理

    # 根据 latency 要求微调
    if latency == "realtime":
        if score < 80:
            score = max(30, score - 20)  # realtime 要求高, 不够快的扣分
    elif latency == "batch":
        if score > 60:
            score = min(100, score + 10)  # batch 不在意速度, 慢点加分 (说明是大模型)

    return max(0, min(score, 100))


def cost_efficiency(model: dict, budget: str) -> float:
    """成本效率: 0-100. 预算内即可, 不再主导."""
    cost_in = (model.get("cost") or {}).get("input", 0) or 0
    cap = COST_BUDGETS[budget]

    # 已经通过硬性 cap 过滤, 这里只做"在预算内得基础分"
    if cap <= 0:
        return 100 if cost_in == 0 else 0

    # 线性: 0 cost → 100, 预算上限 → 50
    if cost_in == 0:
        return 100
    ratio = cost_in / cap
    return max(50, 100 - ratio * 50)  # 50-100 区间


def context_headroom(model: dict) -> float:
    """context 富余度: 越大越好 (0-100)"""
    ctx = (model.get("limit") or {}).get("context", 0)
    if ctx >= 1_000_000:
        return 100
    if ctx >= 500_000:
        return 80
    if ctx >= 128_000:
        return 60
    if ctx >= 32_000:
        return 40
    return 20


def score_model(model: dict, model_id: str, provider: dict, provider_id: str, args: argparse.Namespace) -> dict:
    """返回 dict 含总分 + 5 维度明细, 便于输出展示"""
    if not passes_hard_filters(model, model_id, provider, args):
        return {"total": 0.0}
    breakdown = {
        "task":     round(task_affinity(model_id, model, args.task), 1),
        "quality":  round(quality_score(model_id, model, provider_id, args.task), 1),
        "speed":    round(speed_score(model_id, model, args.latency), 1),
        "context":  round(context_headroom(model), 1),
        "cost":     round(cost_efficiency(model, args.budget), 1),
    }
    # 质量+速度优先, 价格次要
    total = (
        breakdown["task"]    * 0.35
      + breakdown["quality"] * 0.25
      + breakdown["speed"]   * 0.20
      + breakdown["context"] * 0.10
      + breakdown["cost"]    * 0.10
    )
    return {"total": round(total, 2), "breakdown": breakdown}


# ---------- 主流程 ----------
def main():
    args = parse_args()
    data = load_models()

    candidates = []
    for prov_id, prov in data.items():
        for model_id, model in prov.get("models", {}).items():
            sc = score_model(model, model_id, prov, prov_id, args)
            if sc["total"] > 0:
                candidates.append({
                    "provider": prov_id,
                    "provider_name": prov.get("name", prov_id),
                    "model": model_id,
                    "model_name": model.get("name", model_id),
                    "score": sc["total"],
                    "breakdown": sc["breakdown"],
                    "context": (model.get("limit") or {}).get("context", 0),
                    "cost_in": (model.get("cost") or {}).get("input", 0) or 0,
                    "cost_out": (model.get("cost") or {}).get("output", 0) or 0,
                    "capabilities": {
                        k: v for k, v in {
                            "tool_call": model.get("tool_call"),
                            "reasoning": model.get("reasoning"),
                            "attachment": model.get("attachment"),
                            "structured_output": model.get("structured_output"),
                            "open_weights": model.get("open_weights"),
                        }.items() if v
                    },
                })

    candidates.sort(key=lambda x: x["score"], reverse=True)
    top = candidates[:args.top]

    if args.json:
        print(json.dumps(top, ensure_ascii=False, indent=2))
        return 0

    # Markdown 表格输出
    print(f"# LLM Model Recommendations")
    print(f"")
    print(f"**Task:** {args.task} | **Context:** ≥{args.context} | **Budget:** {args.budget} (${COST_BUDGETS[args.budget]}/M) | **Latency:** {args.latency} | **Privacy:** {args.privacy}")
    print(f"")
    print(f"**Weights:** task 35% | quality 25% | speed 20% | context 10% | cost 10%")
    print(f"")
    print(f"| Rank | Score | Task | Qual | Speed | Ctx | Cost | Provider | Model |")
    print(f"|------|-------|------|------|-------|-----|------|----------|-------|")

    for i, c in enumerate(top, 1):
        b = c["breakdown"]
        print(f"| {i} | {c['score']} | {b['task']:.0f} | {b['quality']:.0f} | {b['speed']:.0f} | {b['context']:.0f} | {b['cost']:.0f} | {c['provider']} | {c['model']} |")

    # Fallback chain (同 task 类别不同 provider)
    if len(top) >= 1:
        primary_provider = top[0]["provider"]
        fallbacks = [c for c in candidates[args.top:args.top*3] if c["provider"] != primary_provider][:2]
        if fallbacks:
            print(f"\n## Fallback Chain")
            for fb in fallbacks:
                print(f"- {fb['provider']}/{fb['model']} (score {fb['score']})")

    return 0


if __name__ == "__main__":
    sys.exit(main())
