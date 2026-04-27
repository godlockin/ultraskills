---
name: video-scene-splitter
description: 视频镜头切割与帧提取 - 自动检测场景切换点、切割视频片段、按时间区间抽帧，为视频内容分析提供素材
github_url: https://github.com/Breakthrough/PySceneDetect
github_hash: 009281557bf198d0ebe366699ceb7429e3e222a2
version: 0.6.7
created_at: 2026-04-27
tags: [video, ffmpeg, scene-detection, frame-extraction, video-processing, opencv]
entry_point: scripts/split.py
dependencies: ["scenedetect[opencv]", "ffmpeg"]
---

# Video Scene Splitter Skill

基于 PySceneDetect (4.8k⭐, BSD-3) 的视频镜头切割与帧提取，为视频内容分析 pipeline 提供素材。

## 触发场景

- 将视频切割成场景片段（用于后续逐段分析）
- 从视频指定时间区间抽取代表帧（前10秒/中段/结尾5秒）
- 检测视频中的镜头切换点，获得场景时间轴

## 安全审查 ✅

- 4.8k⭐，BSD-3协议，作者 Brandon Castellano
- 依赖：click/numpy/opencv-python/tqdm — 全部低风险纯计算库
- 无网络请求，无外部API，无混淆代码

## 安装

```bash
pip install "scenedetect[opencv]"
# ffmpeg 必需（用于视频切割输出）
brew install ffmpeg  # macOS
```

## 核心用法

### 1. 自动检测场景切换点

```python
from scenedetect import open_video, SceneManager
from scenedetect.detectors import ContentDetector

def detect_scenes(video_path: str, threshold: float = 27.0) -> list[dict]:
    """
    检测视频场景切换点
    返回：[{scene_num, start_sec, end_sec, duration_sec}, ...]
    """
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold))
    scene_manager.detect_scenes(video)

    scenes = scene_manager.get_scene_list()
    return [
        {
            "scene_num": i + 1,
            "start_sec": round(s[0].get_seconds(), 2),
            "end_sec": round(s[1].get_seconds(), 2),
            "duration_sec": round(s[1].get_seconds() - s[0].get_seconds(), 2),
        }
        for i, s in enumerate(scenes)
    ]
```

### 2. 按时间区间抽帧（核心：前10s/中段/结尾5s）

```python
import subprocess
import os

def extract_frames_by_range(
    video_path: str,
    output_dir: str,
    start_sec: float,
    end_sec: float,
    fps: float = 1.0,   # 每秒抽几帧，1.0=每秒1帧
    prefix: str = "frame"
) -> list[str]:
    """
    从视频指定时间段抽帧
    返回：抽出的帧文件路径列表
    """
    os.makedirs(output_dir, exist_ok=True)
    duration = end_sec - start_sec
    output_pattern = os.path.join(output_dir, f"{prefix}_%04d.jpg")

    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_sec),
        "-i", video_path,
        "-t", str(duration),
        "-vf", f"fps={fps}",
        "-q:v", "2",    # 高质量JPEG
        output_pattern
    ]
    subprocess.run(cmd, capture_output=True, check=True)

    frames = sorted([
        os.path.join(output_dir, f)
        for f in os.listdir(output_dir)
        if f.startswith(prefix) and f.endswith(".jpg")
    ])
    return frames


def extract_audio(video_path: str, output_path: str) -> str:
    """提取音频轨道为 wav 文件"""
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",                    # 无视频
        "-acodec", "pcm_s16le",   # 16-bit PCM
        "-ar", "16000",           # 16kHz（Whisper推荐）
        "-ac", "1",               # 单声道
        output_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    return output_path


def get_video_duration(video_path: str) -> float:
    """获取视频总时长（秒）"""
    import json
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])
```

### 3. 完整素材准备（为视频内容分析器准备输入）

```python
def prepare_video_materials(
    video_path: str,
    work_dir: str,
    intro_secs: float = 10.0,
    outro_secs: float = 5.0,
    mid_fps: float = 0.5,   # 中段每2秒1帧
    intro_fps: float = 2.0, # 开头每0.5秒1帧（密集）
) -> dict:
    """
    一键准备视频分析所需的全部素材：
    - 前10秒帧（密集）
    - 中段帧（稀疏）
    - 结尾5秒帧（密集）
    - 音频文件
    - 场景切换时间轴
    """
    duration = get_video_duration(video_path)
    mid_start = intro_secs
    mid_end = max(intro_secs, duration - outro_secs)

    return {
        "duration": duration,
        "intro_frames": extract_frames_by_range(
            video_path, f"{work_dir}/intro", 0, min(intro_secs, duration),
            fps=intro_fps, prefix="intro"
        ),
        "mid_frames": extract_frames_by_range(
            video_path, f"{work_dir}/mid", mid_start, mid_end,
            fps=mid_fps, prefix="mid"
        ),
        "outro_frames": extract_frames_by_range(
            video_path, f"{work_dir}/outro", max(0, duration - outro_secs), duration,
            fps=intro_fps, prefix="outro"
        ),
        "audio_path": extract_audio(video_path, f"{work_dir}/audio.wav"),
        "scenes": detect_scenes(video_path),
    }
```

## CLI 用法

```bash
# 检测场景并保存每场景首帧
scenedetect -i video.mp4 detect-content save-images

# 按场景切割视频片段
scenedetect -i video.mp4 detect-content split-video

# 跳过前10秒分析（可用于跳过片头）
scenedetect -i video.mp4 time -s 10s detect-content save-images
```

## 与 video-content-analyzer 的关系

本 skill 只负责**机械操作**（切割/抽帧/提取音频）。
分析工作（理解内容/结构/情感）由 `video-content-analyzer` skill 完成。
