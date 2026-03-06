---
name: "video-splitter"
description: "Splits or trims video files into segments. Invoke when user wants to cut, trim, segment, or extract parts of a video."
---

# Video Splitter

This skill helps you split video files into smaller segments, trim specific parts, or divide a video into equal chunks.

## Capabilities

1.  **Trim Video**: Extract a specific segment from a start time to an end time (or duration).
2.  **Split into Chunks**: Divide a video into multiple parts of equal duration.
3.  **Split by Scenes**: (Advanced) Split video based on scene changes (requires `ffmpeg` or `scenedetect`).

## Usage

### 1. Trimming (Cut a segment)
**Tool**: `RunCommand` with `ffmpeg`
**Command**:
```bash
ffmpeg -i <input_file> -ss <start_time> -t <duration> -c copy <output_file>
```
*   `-ss`: Start time (e.g., `00:00:10` or `10`).
*   `-t`: Duration (e.g., `00:00:20` for 20 seconds). Alternatively use `-to` for end time.
*   `-c copy`: Fast stream copy (no re-encoding). Remove if precise frame cutting is needed (may be slower).

### 2. Splitting into Equal Segments
**Tool**: `RunCommand` with `ffmpeg`
**Command**:
```bash
ffmpeg -i <input_file> -c copy -map 0 -segment_time <seconds> -f segment <output_pattern>
```
*   `-segment_time`: Duration of each segment in seconds.
*   `<output_pattern>`: E.g., `output_%03d.mp4`.

### 3. Python Implementation (if ffmpeg is not available)
Use `moviepy` or `opencv` (though slower).

## Steps

1.  **Identify Input**: Ask user for the video file path.
2.  **Determine Strategy**: Ask user if they want to trim (start/end) or split (chunks).
3.  **Check Tool**: Prefer `ffmpeg` if available.
4.  **Execute**: Run the command.

## Example

User: "Cut the first 30 seconds of video.mp4"
Action:
```bash
ffmpeg -i video.mp4 -t 30 -c copy video_part1.mp4
```
