---
name: zero-debt-lint
description: Automated quality gate for presentation decks — text lint (spelling, paths, placeholders) and audio lint (silence ratio, WPM, sample rate) with shell scripts and ffmpeg
version: 1.0.0
tags: [lint, quality, audio, video, ffmpeg, presentation, automation]
---

# Presentation Lint — Zero Sensory Debt

## Overview

"Sensory debt" is what happens when individually minor issues (a typo, a placeholder, a long silence) accumulate into a single impression: "this team is unprofessional." This skill provides two lint scripts — `lint_text.sh` for content and `lint_audio.sh` for voice — that catch these issues before submission.

## When to Use

- Before any presentation submission (competition, executive review, board deck)
- After exporting HTML/PNG composites (catch absolute paths, broken references)
- After generating TTS audio (catch silence spikes, wrong sample rates)
- As a CI/pre-commit hook for deck repositories

## Text Lint (`lint_text.sh`)

### What It Checks

| Check | Pattern | Why |
|-------|---------|-----|
| Absolute paths | `/Users/`, `C:\`, `file:///` | Exposes local filesystem, breaks portability |
| Placeholder text | `PLACEHOLDER`, `TODO`, `FIXME`, `XXX` | Signals incomplete content |
| Common misspellings | `Spakling`, `Seperate`, `Occured`, etc. | Instant credibility killer |
| Empty content | `class="..."> </div>` with only whitespace | Dead space in exported slides |
| Broken image refs | `<img src="...">` pointing to nonexistent files | Visual holes in the deck |

### Implementation Pattern

```bash
#!/usr/bin/env bash
# lint_text.sh — check HTML/text files for quality issues
set -euo pipefail
ROOT="${1:-.}"
ERRORS=0

echo "=== Text Lint: $ROOT ==="

# Absolute paths
while IFS= read -r -d '' file; do
  if grep -n '/Users/\|C:\\\\|file:///' "$file" >/dev/null 2>&1; then
    echo "❌ ABSOLUTE PATH in $file"
    grep -n '/Users/\|C:\\\\|file:///' "$file"
    ERRORS=$((ERRORS+1))
  fi
done < <(find "$ROOT" -name '*.html' -print0)

# Placeholder text
while IFS= read -r -d '' file; do
  if grep -ni 'PLACEHOLDER\|TODO\|FIXME\|XXX' "$file" >/dev/null 2>&1; then
    echo "❌ PLACEHOLDER in $file"
    grep -ni 'PLACEHOLDER\|TODO\|FIXME\|XXX' "$file"
    ERRORS=$((ERRORS+1))
  fi
done < <(find "$ROOT" -name '*.html' -print0)

# Spell check (add project-specific terms to dictionary)
while IFS= read -r -d '' file; do
  # Use aspell or hunspell with custom wordlist
  misspelled=$(aspell list --lang=en --mode=html < "$file" | sort -u)
  if [ -n "$misspelled" ]; then
    echo "⚠️  MISSPELLINGS in $file: $misspelled"
    ERRORS=$((ERRORS+1))
  fi
done < <(find "$ROOT" -name '*.html' -print0)

if [ "$ERRORS" -eq 0 ]; then
  echo "✅ All checks passed"
else
  echo "❌ $ERRORS issue(s) found"
  exit 1
fi
```

### Usage

```bash
bash lint_text.sh v10/deck          # Check all HTML slides
bash lint_text.sh v10/deck/export   # Check exported composites
```

## Audio Lint (`lint_audio.sh`)

### What It Checks

| Check | Threshold | Tool | Why |
|-------|-----------|------|-----|
| Duration | 5s ≤ d ≤ 40s | `ffprobe` | Too short = incomplete; too long = rambles |
| Silence ratio | ≤ 8% | `ffmpeg silencedetect` | Long silences kill pacing |
| Sample rate | ≥ 16000 Hz | `ffprobe` | Below 16kHz sounds robotic |
| Clipping | 0 clips | `ffmpeg volumedetect` | Audio distortion |

### Implementation Pattern

```bash
#!/usr/bin/env bash
# lint_audio.sh — check WAV files for quality thresholds
set -euo pipefail
ROOT="${1:-.}"
FFPROBE=/opt/homebrew/bin/ffprobe
FFMPEG=/opt/homebrew/bin/ffmpeg
ERRORS=0

echo "=== Audio Lint: $ROOT ==="

check_silence() {
  local file="$1"
  local duration
  duration=$($FFPROBE -v error -show_entries format=duration \
    -of default=nw=1:nk=1 "$file")

  # Detect silence below -30dB for 0.5s+
  local silence_output
  silence_output=$($FFMPEG -i "$file" -af silencedetect=noise=-30dB:d=0.5 \
    -f null - 2>&1 | grep 'silence_')

  local total_silence=0
  while IFS= read -r line; do
    if [[ "$line" =~ silence_duration:([0-9.]+) ]]; then
      total_silence=$(echo "$total_silence + ${BASH_REMATCH[1]}" | bc)
    fi
  done <<< "$silence_output"

  local ratio
  ratio=$(echo "scale=4; $total_silence / $duration" | bc)
  echo "$ratio"
}

for wav in $(find "$ROOT" -name '*_30s.wav' -type f | sort); do
  name=$(basename "$wav")
  echo -n "$name: "

  # Duration check
  dur=$($FFPROBE -v error -show_entries format=duration \
    -of default=nw=1:nk=1 "$wav")
  if (( $(echo "$dur < 5" | bc -l) )) || (( $(echo "$dur > 40" | bc -l) )); then
    echo "❌ duration=${dur}s (need 5–40s)"
    ERRORS=$((ERRORS+1))
    continue
  fi

  # Sample rate check
  sr=$($FFPROBE -v error -show_entries stream=sample_rate \
    -of default=nw=1:nk=1 "$wav")
  if [ "$sr" -lt 16000 ]; then
    echo "❌ sample_rate=${sr}Hz (need ≥16000)"
    ERRORS=$((ERRORS+1))
    continue
  fi

  # Silence check
  silence_ratio=$(check_silence "$wav")
  if (( $(echo "$silence_ratio > 0.08" | bc -l) )); then
    echo "❌ silence=$(echo "scale=1; $silence_ratio*100" | bc)% (need ≤8%)"
    ERRORS=$((ERRORS+1))
    continue
  fi

  echo "✅ dur=$(printf '%.1f' "$dur")s sr=${sr}Hz silence=$(echo "scale=1; $silence_ratio*100" | bc)%"
done

echo
if [ "$ERRORS" -eq 0 ]; then
  echo "✅ All audio checks passed"
else
  echo "❌ $ERRORS file(s) failed"
  exit 1
fi
```

### Usage

```bash
bash lint_audio.sh v10/voice/clones/v3_indextts2
```

## Audio Post-Production Recipes

### Trim Head/Tail Silence

```bash
ffmpeg -i input.wav -af areverse,silenceremove=start_periods=1:start_silence=0.1:start_threshold=-30dB,areverse output.wav
```

### Detect Silence Boundaries

```bash
ffmpeg -i input.wav -af silencedetect=noise=-30dB:d=0.5 -f null - 2>&1 | grep silence_
```

### Measure Loudness (EBU R128)

```bash
ffmpeg -i input.wav -af ebur128=peak=true -f null - 2>&1 | tail -20
```

### Adjust Loudness to -16 LUFS

```bash
ffmpeg -i input.wav -af loudnorm=I=-16:TP=-1.5:LRA=11 output.wav
```

## Integration with Build Pipeline

### Pre-Submission Checklist

```bash
# 1. Text lint
bash lint_text.sh v10/deck || { echo "BLOCKED: text lint failed"; exit 1; }

# 2. Audio lint
bash lint_audio.sh v10/voice/clones/v3_indextts2 || { echo "BLOCKED: audio lint failed"; exit 1; }

# 3. Build video
bash v10/voice/build_video_v3.sh

# 4. Final text lint on exports
bash lint_text.sh v10/deck/export || { echo "BLOCKED: export lint failed"; exit 1; }
```

### CI Hook (pre-commit)

```bash
# .git/hooks/pre-commit
#!/bin/bash
bash lint_text.sh v10/deck
bash lint_audio.sh v10/voice/clones/v3_indextts2
```

## Common Failure Patterns and Fixes

| Failure | Root Cause | Fix |
|---------|-----------|-----|
| Absolute path in HTML | Hardcoded `file:///Users/...` in src/href | Use relative paths: `../assets/chart.png` |
| Silence > 8% | TTS output has long pauses | `ffmpeg silencedetect` → trim with `areverse,silenceremove,areverse` |
| Placeholder text | Copy-paste from template | Search-replace before export |
| Misspelling | "Spakling" instead of "Sparkling" | Add project terms to aspell dictionary |
| Low sample rate | Exported at 8000 Hz | Re-export TTS at ≥ 16000 Hz |

## Dependencies

- `ffmpeg` + `ffprobe` (install: `brew install ffmpeg`)
- `aspell` (install: `brew install aspell`)
- `bc` (pre-installed on macOS/Linux)
