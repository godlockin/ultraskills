---
name: "image-to-video"
description: "Combines a sequence of images into a video file. Invoke when user wants to create a video from frames, timelapse, or image sequence."
---

# Image to Video Converter

This skill converts a sequence of images into a video file using `ffmpeg`. It allows specifying the frame rate (FPS) and video encoding parameters.

## Capabilities

1.  **Combine Images to Video**: Convert numbered images (e.g., `frame_001.png`, `frame_002.png`) into an MP4 video.
2.  **Set Frame Rate**: Define how many images are shown per second.
3.  **Control Quality**: Adjust bitrate and codec (e.g., H.264).

## Usage

### 1. Basic Conversion
**Tool**: `RunCommand` with `ffmpeg`
**Command**:
```bash
ffmpeg -framerate <fps> -i <input_pattern> -c:v libx264 -pix_fmt yuv420p <output_file>
```
*   `-framerate <fps>`: Input frame rate (e.g., `30` for 30 fps, `1` for 1 fps).
*   `-i <input_pattern>`: Pattern for input files (e.g., `frame_%04d.png` for frame_0001.png, frame_0002.png).
*   `-c:v libx264`: Video codec (H.264 is widely supported).
*   `-pix_fmt yuv420p`: Pixel format (ensures compatibility with most players).
*   `<output_file>`: Output video filename (e.g., `output.mp4`).

**Example**: Convert 30 frames per second from `frames/img_*.png` to `video.mp4`.
```bash
ffmpeg -framerate 30 -i frames/img_%04d.png -c:v libx264 -pix_fmt yuv420p video.mp4
```

### 2. High Quality / Lossless
**Command**:
```bash
ffmpeg -framerate <fps> -i <input_pattern> -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p <output_file>
```
*   `-crf 18`: Constant Rate Factor (lower is better quality, 18 is near visual lossless).

## Steps

1.  **Identify Input**: Ask user for the image folder and filename pattern.
2.  **Determine FPS**: Ask user for the desired frame rate.
3.  **Execute**: Run the `ffmpeg` command.
