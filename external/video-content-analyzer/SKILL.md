---
name: video-content-analyzer
description: 短视频内容深度分析 - 分析前10秒钩子、中段内容簇、结尾5秒，输出完整结构/情感曲线/传达方式报告。配合 video-scene-splitter + video-transcriber 使用
version: 1.0.0
created_at: 2026-04-27
tags: [video-analysis, content-strategy, short-video, douyin, xiaohongshu, vision, multimodal, claude]
entry_point: scripts/analyze.py
dependencies: ["anthropic", "Pillow", "base64"]
---

# Video Content Analyzer Skill

短视频内容深度分析，回答"这条视频在干什么、怎么干的、效果如何"。

**本 skill 是分析层**，依赖 `video-scene-splitter`（抽帧）和 `video-transcriber`（转录）提供素材。

## 触发场景

- 分析小红书/抖音短视频的内容结构和表达策略
- 理解前10秒如何吸引注意力、用什么钩子
- 拆解视频中段的内容主题分布
- 分析结尾5秒的行动号召/情感收尾方式
- 生成视频完整结构报告（含情感曲线）
- 竞品视频内容拆解

## Pipeline（完整工作流）

```
视频文件 (MP4/MOV)
    │
    ├── video-scene-splitter.prepare_video_materials()
    │       ├── intro_frames[]   前10秒帧
    │       ├── mid_frames[]     中段帧
    │       ├── outro_frames[]   结尾5秒帧
    │       ├── audio.wav        音频
    │       └── scenes[]        场景时间轴
    │
    ├── video-transcriber.transcribe_video()
    │       └── segments[]      带时间戳文字
    │
    └── video-content-analyzer.analyze()  ← 本 skill
            └── 结构化分析报告
```

## 分析框架

### 前10秒（钩子分析）

分析维度：
1. **视觉钩子**：封面画面/开场镜头是什么，用什么视觉方式抓住眼球
2. **音频钩子**：开场台词/音乐/音效，传递什么核心信号
3. **传达方式**：口播直叙 / 悬念设置 / 冲突展示 / 结果前置 / 痛点戳中
4. **关键信息点**：前10秒承诺给观众"看完你会得到什么"

### 中段内容簇（主体分析）

分析维度：
1. **内容分段**：自动识别N个内容簇（每簇对应一个话题/场景）
2. **每簇主题**：在讲什么，核心信息是什么
3. **过渡方式**：簇间如何衔接（硬切/转场/口播过渡）
4. **信息密度**：各段落信息量分布

### 结尾5秒（收尾分析）

分析维度：
1. **情感收尾**：留下什么情绪（期待/满足/共鸣/惊喜）
2. **行动号召**：是否有CTA（关注/点赞/评论/购买）
3. **记忆点**：最后强化的核心信息是什么

### 整体结构报告

1. **叙事结构**：悬念式/列举式/故事式/教程式/对比式
2. **内容分布**：各主题占比饼图（文字描述）
3. **情感曲线**：全片情绪高低走势（低→高→高/低→高→低等）
4. **节奏评估**：信息密度节奏，快/慢/变化点

## 核心实现

```python
import anthropic
import base64
import json
from pathlib import Path


def encode_image(image_path: str) -> str:
    """图片转 base64"""
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")


def build_frame_content(frame_paths: list[str], label: str) -> list[dict]:
    """将帧列表转为 Claude Vision 消息格式"""
    content = [{"type": "text", "text": f"以下是{label}的截帧："}]
    for i, path in enumerate(frame_paths[:8]):  # 最多8帧避免超token
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": encode_image(path)
            }
        })
    return content


def analyze_video(
    materials: dict,       # video-scene-splitter 输出
    transcript: dict,      # video-transcriber 输出
    video_title: str = "", # 可选：视频标题/描述
) -> dict:
    """
    完整视频内容分析
    
    Args:
        materials: prepare_video_materials() 返回值
        transcript: transcribe_video() 返回值
        video_title: 视频标题（辅助分析）
    
    Returns:
        结构化分析报告
    """
    client = anthropic.Anthropic()
    duration = materials["duration"]

    # 获取各段文字
    from video_transcriber import get_text_by_timerange
    segs = transcript.get("segments", [])
    intro_text = get_text_by_timerange(segs, 0, min(10, duration))
    mid_text = get_text_by_timerange(segs, 10, max(10, duration - 5))
    outro_text = get_text_by_timerange(segs, max(0, duration - 5), duration)
    full_text = transcript.get("text", "")

    # 构建分析消息
    messages_content = []

    # 1. 前10秒
    messages_content.extend(build_frame_content(materials["intro_frames"], "视频前10秒"))
    messages_content.append({"type": "text", "text": f"前10秒语音内容：{intro_text}"})

    # 2. 中段
    messages_content.extend(build_frame_content(materials["mid_frames"], "视频中段"))
    messages_content.append({"type": "text", "text": f"中段语音内容：{mid_text}"})

    # 3. 结尾5秒
    messages_content.extend(build_frame_content(materials["outro_frames"], "视频结尾5秒"))
    messages_content.append({"type": "text", "text": f"结尾语音内容：{outro_text}"})

    # 4. 元信息
    scene_info = json.dumps(materials["scenes"], ensure_ascii=False)
    messages_content.append({"type": "text", "text": f"""
视频基本信息：
- 总时长：{duration:.1f}秒
- 场景切换点：{scene_info}
- 标题/描述：{video_title}
- 完整转录：{full_text[:2000]}
"""})

    # 5. 分析指令
    messages_content.append({"type": "text", "text": ANALYSIS_PROMPT})

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": messages_content}]
    )

    raw = response.content[0].text

    # 尝试解析JSON，失败则返回原文
    try:
        return json.loads(raw[raw.index("{"):raw.rindex("}") + 1])
    except Exception:
        return {"raw_analysis": raw}


ANALYSIS_PROMPT = """
请对这段短视频进行深度内容分析，按以下结构输出 JSON：

{
  "intro_analysis": {
    "visual_hook": "开场视觉钩子描述",
    "audio_hook": "开场音频/台词钩子",
    "delivery_method": "传达方式：口播直叙/悬念设置/冲突展示/结果前置/痛点戳中/其他",
    "key_promise": "前10秒给观众的核心承诺",
    "hook_strength": "强/中/弱",
    "hook_reason": "判断理由"
  },
  "mid_content_clusters": [
    {
      "cluster_id": 1,
      "time_range": "10s-30s",
      "topic": "主题描述",
      "key_points": ["核心信息1", "核心信息2"],
      "visual_style": "视觉风格"
    }
  ],
  "outro_analysis": {
    "emotional_close": "情感收尾方式",
    "cta": "行动号召内容（无则填null）",
    "memory_anchor": "最后强化的记忆点"
  },
  "overall_structure": {
    "narrative_type": "叙事类型：悬念式/列举式/故事式/教程式/对比式/其他",
    "content_distribution": {"主题1": "占比%", "主题2": "占比%"},
    "emotion_curve": "情感曲线描述，如：低开高走/起伏型/持续高能/先抑后扬",
    "rhythm": "节奏特点：快节奏/慢节奏/张弛有度",
    "core_message": "整体视频最想传达的一句话",
    "target_audience": "目标受众判断",
    "effectiveness_score": 1-10,
    "effectiveness_reason": "评分理由"
  }
}
"""
```

## 完整使用示例

```python
# 步骤1：准备素材（调用 video-scene-splitter）
from video_scene_splitter import prepare_video_materials
materials = prepare_video_materials(
    video_path="/tmp/douyin_video.mp4",
    work_dir="/tmp/analysis_work"
)

# 步骤2：转录（调用 video-transcriber）
from video_transcriber import transcribe_video
transcript = transcribe_video(
    audio_path=materials["audio_path"],
    language="zh"
)

# 步骤3：分析（本 skill）
from video_content_analyzer import analyze_video
report = analyze_video(
    materials=materials,
    transcript=transcript,
    video_title="这款面霜真的绝了！用了一周皮肤变化太大了"
)

# 输出报告
import json
print(json.dumps(report, ensure_ascii=False, indent=2))
```

## 与 MediaCrawler 完整集成

```python
# 从 MediaCrawler 采集的视频 URL 到完整分析报告
import subprocess

def analyze_from_url(video_url: str, work_dir: str) -> dict:
    """从视频 URL 直接分析（需 yt-dlp 或 media-downloader skill）"""
    video_path = f"{work_dir}/input.mp4"

    # 下载（使用 media-downloader skill 中的 yt-dlp）
    subprocess.run(["yt-dlp", "-o", video_path, video_url], check=True)

    materials = prepare_video_materials(video_path, f"{work_dir}/frames")
    transcript = transcribe_video(materials["audio_path"], language="zh")
    return analyze_video(materials, transcript)
```

## 输出报告示例

```json
{
  "intro_analysis": {
    "visual_hook": "主播手持产品特写，背景整洁白色，前景有明显反光效果",
    "audio_hook": "开口第一句：'用了三年护肤品，这是我见过最有效的'",
    "delivery_method": "结果前置",
    "key_promise": "观看后会知道一款改变皮肤状态的护肤品",
    "hook_strength": "强",
    "hook_reason": "结果前置+产品特写组合，制造好奇心驱动完播"
  },
  "mid_content_clusters": [
    {"cluster_id": 1, "time_range": "10s-25s", "topic": "使用前后对比", "key_points": ["皮肤暗沉改善", "毛孔收缩"], "visual_style": "对比截图"},
    {"cluster_id": 2, "time_range": "25s-45s", "topic": "成分讲解", "key_points": ["玻尿酸浓度", "无酒精"], "visual_style": "产品背标特写"}
  ],
  "outro_analysis": {
    "emotional_close": "满足感+期待感",
    "cta": "评论区回复'想要'发购买链接",
    "memory_anchor": "三年测试背书的可信度"
  },
  "overall_structure": {
    "narrative_type": "结果前置式",
    "content_distribution": {"产品展示": "40%", "使用效果": "35%", "成分科普": "25%"},
    "emotion_curve": "高开持续高能",
    "rhythm": "快节奏",
    "core_message": "这款面霜是护肤界的隐藏冠军",
    "effectiveness_score": 8,
    "effectiveness_reason": "结果前置钩子强，但中段成分讲解偏专业可能流失普通用户"
  }
}
```
