# Tech Stack

_从 playwright-media-sniffer v1.0 SKILL.md 抽取 (Line 338-362)_

## 🔧 技术栈

### 依赖项

```bash
# Python 依赖
pip install playwright playwright-stealth browser-cookie3 requests

# 初始化 Playwright 浏览器
playwright install chromium

# 下载工具（二选一或都装）
pip install yt-dlp         # 推荐，支持更多格式
brew install ffmpeg        # 或 apt install ffmpeg
```

### 浏览器支持

- ✅ Chromium/Chrome（推荐，cookie提取最简单）
- ✅ Edge（同 Chromium 内核）
- ✅ Firefox（需 firefox-cookie3）
- ⚠️ Safari（cookie 提取复杂，不推荐）

---

