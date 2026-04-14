# Example: Extracting Audio

**Scenario**: User wants to listen to a conference talk on their phone (audio only).

## Input

"Get me the MP3 of this talk: <https://www.bilibili.com/video/BV1xx411c7mD>"

## Process

### 1. Command Generation

- **Tool**: `yt-dlp`
- **Arguments**:
  - `-x` (Extract audio)
  - `--audio-format mp3` (Convert to MP3)
  - `--audio-quality 0` (Best quality, VBR ~256k)

### 2. Execution

```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 "https://www.bilibili.com/video/BV1xx411c7mD"
```

## Output

- File saved: `Awesome Talk [BV1xx411c7mD].mp3`
