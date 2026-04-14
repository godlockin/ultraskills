# Example: Downloading a Video

**Scenario**: User wants to archive a tech tutorial from YouTube in the best quality.

## Input

"Download this video: <https://www.youtube.com/watch?v=dQw4w9WgXcQ>"

## Process

### 1. Command Generation

- **Tool**: `yt-dlp`
- **Arguments**:
  - `"https://www.youtube.com/watch?v=dQw4w9WgXcQ"` (Quoted URL)
  - `-f "bv+ba/b"` (Best video + Best audio)
  - `--merge-output-format mp4` (Ensure standard MP4 container)

### 2. Execution

```bash
yt-dlp -f "bv+ba/b" --merge-output-format mp4 "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

## Output

- File saved: `Rick Astley - Never Gonna Give You Up [dQw4w9WgXcQ].mp4`
- Resolution: 1080p (or 4K if available)
