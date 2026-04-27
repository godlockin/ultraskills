---
name: video-transcriber
description: 视频/音频语音转录 - 使用 OpenAI Whisper 生成带时间戳的完整字幕，支持中文/多语言，用于视频内容分析的文本输入
github_url: https://github.com/openai/whisper
github_hash: 04f449b8a437f1bbd3dba5c9f826aca972e7709a
version: 20231117
created_at: 2026-04-27
tags: [whisper, transcription, speech-to-text, audio, video, chinese, subtitle, timestamps]
entry_point: scripts/transcribe.py
dependencies: ["openai-whisper", "ffmpeg"]
---

# Video Transcriber Skill

基于 OpenAI Whisper (98.5k⭐, MIT) 的视频/音频转录，生成带时间戳文本，供视频内容分析使用。

## 触发场景

- 提取视频中的所有语音内容（带精确时间戳）
- 为视频内容分析提供文本轨道（配合帧图像联合分析）
- 生成视频字幕文件（SRT/VTT格式）

## 安全审查 ✅

- 98.5k⭐，MIT协议，OpenAI 官方发布
- 模型在本地运行，音频数据不上传任何服务器
- 依赖：torch/numpy/ffmpeg — 标准学术/工程库
- 模型从 OpenAI CDN 下载（首次），后续全离线运行

## 安装

```bash
pip install openai-whisper
brew install ffmpeg  # macOS，必需
```

**模型选择**（首次自动下载）：

| 模型 | 大小 | 速度 | 中文精度 |
|------|------|------|---------|
| tiny | 39M | 最快 | 一般 |
| base | 74M | 快 | 较好 |
| small | 244M | 中 | 好 |
| **medium** | **769M** | 中慢 | **推荐** |
| large | 1.5G | 慢 | 最佳 |

## 核心用法

### 1. 带时间戳转录

```python
import whisper

def transcribe_video(
    audio_path: str,
    model_size: str = "medium",
    language: str = "zh"    # "zh"=中文, None=自动检测
) -> dict:
    """
    转录音频/视频，返回完整文本和分段时间戳
    
    Returns:
        {
            "text": "完整转录文本",
            "segments": [
                {"id": 0, "start": 0.0, "end": 2.5, "text": "大家好"},
                ...
            ],
            "language": "zh"
        }
    """
    model = whisper.load_model(model_size)
    result = model.transcribe(
        audio_path,
        language=language,
        verbose=False,
        word_timestamps=True,   # 词级时间戳
        task="transcribe"       # "transcribe"=原语言, "translate"=翻译成英文
    )
    return result


def get_text_by_timerange(
    segments: list[dict],
    start_sec: float,
    end_sec: float
) -> str:
    """从转录段落中提取指定时间范围的文本"""
    texts = [
        seg["text"].strip()
        for seg in segments
        if seg["start"] >= start_sec and seg["end"] <= end_sec
    ]
    return " ".join(texts)
```

### 2. 生成 SRT 字幕文件

```python
def to_srt(segments: list[dict], output_path: str) -> str:
    """将转录结果转为 SRT 字幕文件"""
    def fmt_time(t: float) -> str:
        h, r = divmod(int(t), 3600)
        m, s = divmod(r, 60)
        ms = int((t - int(t)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

    lines = []
    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{fmt_time(seg['start'])} --> {fmt_time(seg['end'])}")
        lines.append(seg["text"].strip())
        lines.append("")

    content = "\n".join(lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return output_path
```

### 3. 按视频段落切分转录文本

```python
def segment_transcript_by_scenes(
    segments: list[dict],
    scenes: list[dict]
) -> list[dict]:
    """
    将转录文本按场景切换点对齐
    
    Args:
        segments: whisper 转录段落
        scenes: video-scene-splitter 输出的场景列表
    
    Returns:
        每个场景对应的文本片段
    """
    result = []
    for scene in scenes:
        text = get_text_by_timerange(
            segments,
            scene["start_sec"],
            scene["end_sec"]
        )
        result.append({
            **scene,
            "transcript": text
        })
    return result
```

## Apple Silicon 加速

如使用 Mac M 系列芯片，可安装 `mlx-whisper` 获得 3-5x 速度提升：

```bash
pip install mlx-whisper
# 用法相同，替换 import 即可
```

也可直接使用已有的 `mac-whisper` skill（本库已集成优化）。

## 与其他 skill 的关系

- **输入来源**：`video-scene-splitter` 提取的 audio.wav
- **输出去向**：`video-content-analyzer` 使用转录文本+帧图像联合分析
