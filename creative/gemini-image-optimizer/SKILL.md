---
name: "gemini-image-optimizer"
description: "Optimizes or refines images using Google's Gemini model. Invoke when user wants to improve image quality, change style, or fix artifacts using AI."
---

# Gemini Image Optimizer

This skill uses Google's Gemini Vision model to optimize, refine, or restyle images based on a text prompt.

## Capabilities

1.  **Optimize Image**: Enhance image quality, lighting, and texture.
2.  **Restyle Image**: Change the artistic style (e.g., "make it look like a sketch").
3.  **Fix Artifacts**: Remove noise, blur, or unwanted elements.

## Prerequisites

*   `google-generativeai` python package installed.
*   `GEMINI_API_KEY` environment variable set.
*   Python script: `.trae/skills/gemini-image-optimizer/optimize_image.py`

## Usage

**Tool**: `RunCommand`
**Command**:
```bash
python .trae/skills/gemini-image-optimizer/optimize_image.py --input <input_image_path> --output <output_image_path> --prompt "<optimization_prompt>"
```

*   `--input`: Path to the source image.
*   `--output`: Path to save the result.
*   `--prompt`: Instructions for Gemini (e.g., "Make this image look like a professional studio photo").

## Example

User: "Make `frame_001.png` look more cinematic."
Action:
```bash
python .trae/skills/gemini-image-optimizer/optimize_image.py --input frame_001.png --output frame_001_cinematic.png --prompt "Make this image look cinematic, with dramatic lighting and high contrast."
```
