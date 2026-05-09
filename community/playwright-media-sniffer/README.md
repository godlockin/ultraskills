# Playwright Media Sniffer

> 模拟人类操作，继承浏览器登录态，自动嗅探并下载任意网站的媒体资源

---

## Quick Start

```bash
# 安装依赖
pip install playwright playwright-stealth browser-cookie3
playwright install chromium

# 首次使用 - 保存登录态
python scripts/sniff_and_download.py \
    "https://example.com/video/123" \
    --login-first

# 后续使用 - 自动嗅探下载
python scripts/sniff_and_download.py \
    "https://example.com/video/123" \
    --auth-state auth/example_com.json
```

---

## What's Inside

- **SKILL.md** — 完整工作流（登录态继承 → 嗅探 → 下载）
- **scripts/**
  - `sniff_and_download.py` — 主程序（Playwright 嗅探 + yt-dlp 下载）
- **examples/**
  - `bilibili-member.md` — B站大会员视频下载
  - `custom-player.md` — 自定义播放器嗅探
- **references/**
  - `playwright-network-api.md` — Playwright 网络监听API
  - `cookie-extraction.md` — 跨浏览器 cookie 提取方法

---

## Core Features

### 1. 浏览器层嗅探（模拟 cat-catch）

```python
# 监听所有网络请求
page.on('request', lambda req: capture_if_media(req))

# 捕获格式
- M3U8 (HLS 流)
- MPD (DASH 流)
- 直接 MP4/WebM
- 音频流
```

### 2. 登录态继承

**方法 A**: 从本地浏览器导入
```python
import browser_cookie3
cookies = browser_cookie3.chrome(domain_name='bilibili.com')
context.add_cookies(cookies)
```

**方法 B**: 手动登录保存
```python
# 首次登录
page.goto('https://example.com/login')
input("Login then press Enter...")
context.storage_state(path='auth/example_com.json')

# 后续复用
context = browser.new_context(storage_state='auth/example_com.json')
```

**方法 C**: 接管已打开的浏览器（CDP）
```bash
chrome --remote-debugging-port=9222
```
```python
browser = playwright.chromium.connect_over_cdp('http://localhost:9222')
```

### 3. 智能下载

```python
# 优先 yt-dlp（支持更多格式）
yt-dlp --cookies-from-browser chrome \
       --referer "https://example.com/" \
       "https://cdn.example.com/video.m3u8"

# Fallback: ffmpeg（直接下载）
ffmpeg -headers "Cookie: session=abc\r\nReferer: https://example.com/" \
       -i "https://cdn.example.com/video.m3u8" \
       -c copy output.mp4
```

### 4. 反爬绕过

- Stealth 模式（隐藏自动化特征）
- 随机延迟（模拟人类行为）
- 真实 User-Agent 和浏览器指纹

---

## vs 其他方案

| 方案 | 覆盖率 | AI调用 | 登录态 | 速度 | 适用场景 |
|------|--------|--------|--------|------|----------|
| **playwright-media-sniffer** | 100% | ✅ | ✅ 自动 | 中 | 小众网站、会员内容、自定义播放器 |
| **cat-catch** | 100% | ❌ | ✅ 自动 | 快 | 手动浏览器操作 |
| **yt-dlp** | 90% | ✅ | ⚠️ 手动 | 快 | 主流平台（YouTube/B站/1000+） |

**推荐策略**:
1. 优先使用 **media-downloader** (yt-dlp) - 主流平台
2. 失败时使用 **本 skill** - 小众/自定义播放器
3. 需手动操作时使用 **cat-catch** - 复杂反爬场景

---

## Examples

### 示例 1: B站大会员番剧

```bash
# 首次：保存登录态
python scripts/sniff_and_download.py \
    "https://www.bilibili.com/bangumi/play/ep123456" \
    --login-first

# 后续：自动下载
python scripts/sniff_and_download.py \
    "https://www.bilibili.com/bangumi/play/ep123456" \
    --auth-state auth/bilibili_com.json
```

**输出**: `downloads/bilibili_com_某番剧名_EP1.mp4`

---

### 示例 2: 小众教育平台

```bash
python scripts/sniff_and_download.py \
    "https://edu-platform.com/course/123/video/5" \
    --login-first

# 捕获自定义播放器的 M3U8
# https://cdn.edu-platform.com/enc/course123.m3u8?token=dynamic_generated
```

---

### 示例 3: 企业内网视频（SSO登录）

```bash
# 1. 先在 Chrome 中手动 SSO 登录
# 2. 启动 Chrome 远程调试
chrome --remote-debugging-port=9222

# 3. 连接并嗅探（无需再次登录）
python scripts/sniff_and_download.py \
    "https://training.company.com/video/onboarding" \
    --cdp http://localhost:9222
```

---

## Workflow

```
用户请求下载 URL
    ↓
检查是否有保存的登录态 (auth/*.json)
    ↓
    无 → --login-first 模式（手动登录）
    有 → 加载 storage_state
    ↓
Playwright 打开浏览器
    ↓
page.on('request') 监听网络
    ↓
page.goto(url) + 触发播放
    ↓
捕获所有 .m3u8/.mpd/.mp4 资源
    ↓
智能排序（主清单优先，分片过滤）
    ↓
用户选择资源（或自动选最佳）
    ↓
调用 yt-dlp/ffmpeg 下载（注入 cookies + headers）
    ↓
输出：downloads/video.mp4 + metadata.json
```

---

## Dependencies

```bash
# Python packages
playwright>=1.40.0
playwright-stealth>=1.0.0
browser-cookie3>=0.19.0
requests>=2.31.0

# System tools
yt-dlp>=2023.11.0
ffmpeg>=6.0
```

---

## Limitations

- ❌ **DRM 内容**: Widevine/FairPlay 加密无法下载（法律和技术限制）
- ⚠️ **强反爬网站**: 可能需要验证码/滑块（需人工介入）
- ⚠️ **WebSocket 流**: 当前不支持（未来可能添加）
- ⚠️ **直播流**: 实时流需要持续录制（未实现）

---

## FAQ

**Q: 和 media-downloader (yt-dlp) 什么关系？**

A: 互补关系
- **media-downloader**: 主流平台（YouTube/B站），优先使用
- **本 skill**: 小众网站/会员内容，回退方案

**Q: 合法吗？**

A: 
- ✅ 下载自己购买的会员内容 - 合法（个人备份）
- ❌ 传播/售卖版权内容 - 违法
- ⚠️ 绕过技术保护措施（DRM）- 某些地区违法

**Q: 会被封号吗？**

A:
- 正常使用（模拟人类）- 风险极低
- 高频爬取（短时间大量） - 可能触发风控
- 建议：使用小号测试，间隔 ≥ 30s

**Q: 性能如何？**

A:
- 嗅探: 5-10s（启动浏览器 + 页面加载）
- 下载: 与 yt-dlp 相同（网速决定）
- **总耗时 ≈ yt-dlp + 10s**

---

## Version History

**v1.0.0** (2026-05-08)
- Initial release
- Playwright network monitoring
- Browser cookie injection
- yt-dlp/ffmpeg download
- Stealth mode support

---

**License**: MIT  
**Author**: UltraSkills Community  
**Last Updated**: 2026-05-08
