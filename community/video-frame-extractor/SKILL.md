---
name: "video-frame-extractor"
description: "Extracts image frames from video files. Invoke when user wants to convert video to images, extract frames at specific FPS, or sample video content."
---

# Video Frame Extractor

This skill extracts image frames from video files using `ffmpeg`. It allows specifying the extraction frequency (FPS).

## Capabilities

1.  **Extract at specific FPS**: Extract N frames per second (e.g., 1 frame every second).
2.  **Extract All Frames**: Convert the entire video to a sequence of images.
3.  **Extract Keyframes**: Extract only I-frames (scene changes/key points).

## Usage

### 1. Extract at Specific FPS (Most Common)
**Tool**: `RunCommand` with `ffmpeg`
**Command**:
```bash
ffmpeg -i <input_file> -vf fps=<fps_value> <output_pattern>
```
*   `<fps_value>`: Number of frames to extract per second.
    *   `1`: One frame per second.
    *   `0.5`: One frame every 2 seconds.
    *   `1/5`: One frame every 5 seconds.
*   `<output_pattern>`: E.g., `frame_%04d.png` (results in frame_0001.png, frame_0002.png...).

**Example**: Extract 2 frames per second from `video.mp4` to `frames/` folder.
```bash
mkdir -p frames
ffmpeg -i video.mp4 -vf fps=2 "frames/frame_%04d.png"
```

### 2. Extract All Frames
**Command**:
```bash
ffmpeg -i <input_file> <output_pattern>
```
*   **Warning**: This can generate a huge number of files for long videos.

### 3. Extract Keyframes (I-frames)
**Command**:
```bash
ffmpeg -i <input_file> -vf "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr <output_pattern>
```

## Steps

1.  **Identify Input**: Ask user for the video file path.
2.  **Determine FPS**: Ask user for the desired extraction rate (default to 1 fps if unsure).
3.  **Prepare Output**: Ensure the output directory exists (`mkdir -p`).
4.  **Execute**: Run the `ffmpeg` command.
