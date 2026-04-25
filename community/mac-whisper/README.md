# mac-whisper

Apple Silicon 本地 SOTA 语音转文字。基于 MLX-Whisper（Apple 官方框架），M2 上 10–20× 实时。

## Install

```bash
bash scripts/install.sh
```

会装：`mlx-whisper`、`ffmpeg`，可选 `whisper.cpp`。

## Use

```bash
bash scripts/transcribe.sh audio.mp3 --lang zh --format srt
```

完整选项见 `scripts/transcribe.sh --help` 或 `SKILL.md`。
