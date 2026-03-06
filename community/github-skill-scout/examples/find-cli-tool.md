# Example: Finding a CLI Tool

**Scenario**: User needs a tool to upscale images using AI, running locally.

## Input

"I need a CLI tool to upscale images 4x locally without sending them to the cloud."

## Process

### 1. Search Strategy

**Query**: `"image upscaler" language:python topic:ai topic:cli sort:stars`

### 2. Candidate Selection

Found `upscayl/upscayl` (Electron, heavy) and `xinntao/Real-ESRGAN` (Python, model-based).
Selected **`Real-ESRGAN`** for better CLI integration potential.

### 3. Audit Result

- **Stars**: 15k+
- **License**: BSD-3-Clause
- **Last Update**: 3 months ago
- **Security Check**: Clean `setup.py`.

## Output (Recommendation)

> **Candidate Found**: `Real-ESRGAN`
>
> - **Why**: High performance, pure CLI support, widely used industry standard.
> - **Command**: `realesrgan-ncnn-vulkan -i input.jpg -o output.png -s 4`
> - **Status**: ✅ Safe to wrap.
