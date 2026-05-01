# zero-debt-lint

> Automated quality gates that catch what human eyes miss — spelling, paths, placeholders, silence.

## Why This Exists

Sensory debt compounds. One typo is a detail. Five issues = "this team is unprofessional." Lint catches them all before submission.

## What's Inside

- **`lint_text.sh`** — scans HTML for absolute paths, placeholder text, common misspellings, empty content
- **`lint_audio.sh`** — checks WAV files for duration (5–40s), silence ratio (≤8%), sample rate (≥16kHz)
- **Audio recipes** — trim silence, detect boundaries, measure loudness, normalize to -16 LUFS
- **CI integration** — pre-commit hooks and build pipeline patterns

## When to Use

- Before any presentation submission
- After exporting HTML/PNG composites
- After generating TTS audio
- As a pre-commit hook for deck repos

## Quick Start

```bash
bash lint_text.sh v10/deck
bash lint_audio.sh v10/voice/clones/v3_indextts2
```

Both must pass 0 errors before submission.

## Dependencies

- `ffmpeg` + `ffprobe` (`brew install ffmpeg`)
- `aspell` (`brew install aspell`)
- `bc` (pre-installed on macOS/Linux)
