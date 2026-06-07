# Example: 隐私 / 离线 / Air-gapped

## 场景
医疗 / 法律 / 金融 / 政府项目：
- 数据不能出本地 (HIPAA/GDPR/合规)
- 必须 open_weights 自部署
- 网络可能断 (现场作业)
- 性能次要，安全第一

## 推荐命令

```bash
python3 <skill-path>/scripts/recommend.py \
    --task any \
    --context 128k \
    --privacy open_weights \
    --top 10
```

## 实际输出 (示例)

| Rank | Score | Provider | Model | Context | $in/M | Open Weights | Hardware |
|------|-------|----------|-------|---------|-------|--------------|----------|
| 1 | ~88 | meta | llama-3.3-70b | 128k | self-host | ✓ | 2× A100 80G |
| 2 | ~85 | mistral | mistral-large-2 | 128k | self-host | ✓ | 2× A100 |
| 3 | ~84 | qwen | qwen-2.5-72b | 128k | self-host | ✓ | 2× A100 |
| 4 | ~80 | deepseek | deepseek-v3 | 64k | self-host | ✓ | 2× A100 |
| 5 | ~78 | google | gemma-2-27b | 8k | self-host | ✓ | 1× A100 |

## 决策说明

**Primary: Llama 3.3 70B** (业界最成熟的 open-weight)
- 70B = 质量接近 GPT-4 class
- 完全本地，数据不出防火墙
- 生态最广 (Ollama / vLLM / TGI 都支持)

**Fallback 链**:
- `mistral-large-2` — 欧洲合规
- `qwen-2.5-72b` — 中文场景
- `deepseek-v3` — 推理强
- `gemma-2-27b` — 小模型快速

## 部署架构

```yaml
# docker-compose.yml 概念
services:
  llm-primary:
    image: vllm/vllm-openai:latest
    command: --model meta-llama/Llama-3.3-70B-Instruct
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
              count: 2  # 2× A100 80G
    network_mode: "none"  # 彻底断网

  llm-fallback:
    image: ollama/ollama
    # 小模型 fallback, 资源不足时用
```

## 实战代码示例

```python
# OpenAI-compatible 本地 endpoint
import openai

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",  # vLLM
    api_key="not-needed",
)

# 完整审计 trail
response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct",
    messages=[{"role": "user", "content": prompt}],
    # 数据从未离开 localhost
)
```

## 关键陷阱

- **70B 是甜点** — 7B/13B 质量不够，405B 部署太贵
- **必须用推理加速框架** (vLLM / TGI / SGLang) — 否则 5 tokens/s
- **数据分类** — `open_weights` ≠ `air-gapped`. 还要确认无 telemetry 上报 (Ollama 默认有)
- **合规审计** — 部署后需第三方审计 (模型权重 + 推理日志)
- **断网验证** — 部署完 `iptables -A OUTPUT -d 0.0.0.0/0 -j DROP` 测一遍
