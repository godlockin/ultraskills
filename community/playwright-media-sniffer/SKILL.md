---
name: playwright-media-sniffer
description: Browser automation-based media sniffer using Playwright to inherit login state, capture M3U8/MPD/MP4 resources from any website (including custom players), and download via yt-dlp/ffmpeg with full cookie support
version: 1.0.0
tags: [media, download, playwright, browser-automation, m3u8, mpd, sniffer, login-state, cookie-injection]
---

# Playwright Media Sniffer

> 模拟人类操作，继承浏览器登录态，自动嗅探并下载任意网站的媒体资源（包括会员内容）

---

## 🎯 目标 (Goal)

- **浏览器层嗅探**：监听所有网络请求，捕获 M3U8/MPD/MP4/音频资源
- **登录态继承**：从用户已登录的浏览器复用 cookies/localStorage
- **人类行为模拟**：随机延迟、鼠标移动、滚动，绕过反爬检测
- **智能下载**：资源URL提取后，调用 yt-dlp/ffmpeg 高效下载合并
- **全格式支持**：HLS (M3U8)、DASH (MPD)、直接MP4、音频流

**适用场景**：
- yt-dlp 不支持的小众视频网站
- 自定义播放器（非标准嵌入）
- 需登录才能观看的会员内容
- 动态加密/签名的视频URL
- iframe 多层嵌套的资源

---

## 🧠 核心理念 (Core Concepts)

### 嗅探原理

```
用户 → Claude Code → Playwright 打开浏览器
                          ↓
                   加载目标页面（继承登录态）
                          ↓
                   page.on('request') 监听所有网络请求
                          ↓
                   筛选：.m3u8 / .mpd / .mp4 / audio/*
                          ↓
                   提取：URL + headers + cookies
                          ↓
                   下载：yt-dlp --cookies / ffmpeg
```

### 登录态继承方式

**方法 1**：从本地浏览器导入 cookies（推荐）
```python
from playwright.sync_api import sync_playwright

# 从 Chrome/Edge/Firefox 读取 cookies
context = browser.new_context(storage_state='chrome://cookies')
```

**方法 2**：手动登录后保存状态
```python
# 首次登录
page.goto('https://example.com/login')
# ... 用户手动登录 ...
context.storage_state(path='auth_state.json')

# 后续复用
context = browser.new_context(storage_state='auth_state.json')
```

**方法 3**：接管已打开的浏览器（CDP）
```python
# 连接用户正在使用的浏览器
browser = playwright.chromium.connect_over_cdp('http://localhost:9222')
```

### 反爬绕过

```python
# Stealth 模式
context = browser.new_context(
    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
    viewport={'width': 1920, 'height': 1080},
    locale='zh-CN',
    timezone_id='Asia/Shanghai',
    permissions=['geolocation'],
    geolocation={'latitude': 31.23, 'longitude': 121.47},  # 上海
    extra_http_headers={
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
)

# 随机延迟
import random
await page.wait_for_timeout(random.randint(1000, 3000))

# 模拟人类行为
await page.mouse.move(random.randint(100, 800), random.randint(100, 600))
await page.mouse.wheel(0, random.randint(100, 500))
```

---

## 🚀 使用流程 (Workflow)

### 触发方式

```
"从这个网站下载视频: https://example.com/video/123"
"这个会员视频帮我下载"
"嗅探这个页面的媒体资源"
"download video from login-required site"
```

或直接：
```bash
/playwright-media-sniffer https://example.com/video/123
```

### Step 1: 准备浏览器状态

**选项 A**：使用已登录的浏览器（推荐）

```python
# scripts/sniff_and_download.py
from playwright.sync_api import sync_playwright
import browser_cookie3  # pip install browser-cookie3

# 从本地浏览器提取 cookies
cookies = browser_cookie3.chrome(domain_name='example.com')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # 可见模式便于调试
    context = browser.new_context()
    
    # 注入 cookies
    for cookie in cookies:
        context.add_cookies([{
            'name': cookie.name,
            'value': cookie.value,
            'domain': cookie.domain,
            'path': cookie.path,
        }])
```

**选项 B**：首次手动登录

```python
# 交互式登录（首次）
page = context.new_page()
page.goto('https://example.com/login')

print("⏸️  请在浏览器中登录，完成后按 Enter...")
input()

# 保存登录态
context.storage_state(path='auth/example_com.json')
```

### Step 2: 嗅探媒体资源

```python
# 监听网络请求
captured_resources = []

def on_request(request):
    url = request.url
    # 筛选媒体资源
    if any(ext in url.lower() for ext in ['.m3u8', '.mpd', '.mp4', '.ts', '.m4s']):
        captured_resources.append({
            'url': url,
            'type': request.resource_type,
            'method': request.method,
            'headers': request.headers
        })
        print(f"🎯 Captured: {url[:80]}...")

page.on('request', on_request)

# 打开目标页面
page.goto(target_url, wait_until='networkidle')

# 等待视频播放器加载（触发资源请求）
page.wait_for_timeout(5000)

# 尝试播放（触发更多请求）
try:
    # 查找播放按钮
    play_button = page.locator('button:has-text("播放"), button[aria-label*="play"], .video-play-btn').first
    if play_button.is_visible():
        play_button.click()
        page.wait_for_timeout(3000)
except:
    pass

print(f"\n✅ Captured {len(captured_resources)} media resources")
```

### Step 3: 智能筛选

```python
# 优先级排序
def prioritize_resources(resources):
    scored = []
    for r in resources:
        url = r['url']
        score = 0
        
        # M3U8/MPD 高优先级（主清单）
        if '.m3u8' in url and 'index' in url:
            score += 10
        elif '.mpd' in url:
            score += 10
        elif '.m3u8' in url:
            score += 5
        
        # 分片文件低优先级（只下载主清单）
        if '.ts' in url or '.m4s' in url:
            score -= 5
        
        # 直接 MP4 中优先级
        if '.mp4' in url and 'playlist' not in url:
            score += 7
        
        scored.append((score, r))
    
    # 按分数排序，返回前3个
    scored.sort(reverse=True, key=lambda x: x[0])
    return [r for _, r in scored[:3]]

best_resources = prioritize_resources(captured_resources)
```

### Step 4: 下载

```python
import subprocess

for res in best_resources:
    url = res['url']
    headers = res['headers']
    
    # 提取 cookies
    cookie_str = '; '.join([f"{k}={v}" for k, v in headers.items() if k.lower() == 'cookie'])
    
    # 构造 yt-dlp 命令
    cmd = [
        'yt-dlp',
        '--add-header', f'Referer: {target_url}',
        '--add-header', f'Cookie: {cookie_str}',
        '--add-header', f'User-Agent: {headers.get("user-agent", "")}',
        '--output', 'downloads/%(title)s.%(ext)s',
        url
    ]
    
    print(f"📥 Downloading: {url[:60]}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Success!")
    else:
        # Fallback: ffmpeg 直接下载（适用于 yt-dlp 不支持的格式）
        print(f"⚠️  yt-dlp failed, trying ffmpeg...")
        cmd_ffmpeg = [
            'ffmpeg',
            '-headers', f'Referer: {target_url}\r\nCookie: {cookie_str}',
            '-i', url,
            '-c', 'copy',
            f'downloads/video_{hash(url)}.mp4'
        ]
        subprocess.run(cmd_ffmpeg)
```

---

## 💡 最佳实践 (Best Practices)

### Do ✅

1. **首次运行手动登录**
   ```python
   # 保存登录态供后续使用
   context.storage_state(path='auth/site_name.json')
   ```

2. **使用 stealth 模式**
   ```python
   # 安装：pip install playwright-stealth
   from playwright_stealth import stealth_sync
   stealth_sync(page)
   ```

3. **检查资源完整性**
   ```python
   # M3U8 验证
   if '.m3u8' in url:
       resp = requests.get(url, headers=headers)
       if '#EXTM3U' not in resp.text:
           print("⚠️  Invalid M3U8 file")
   ```

4. **处理多个候选资源**
   ```python
   # 让用户选择（如检测到多个视频）
   for i, res in enumerate(best_resources, 1):
       print(f"{i}. {res['url'][:60]}...")
   choice = input("选择要下载的资源编号: ")
   ```

### Don't ❌

1. **不要在 headless 模式下处理强反爬网站**
   - 使用 `headless=False`（可见浏览器）
   - 或使用 `--stealth` 插件

2. **不要忽略 Referer 和 User-Agent**
   - 某些 CDN 强制校验
   - 必须传递给 yt-dlp/ffmpeg

3. **不要下载所有 .ts 分片**
   - 只下载主 M3U8 清单
   - 让 yt-dlp/ffmpeg 自动处理分片

4. **不要长时间停留在页面**
   - 嗅探完立即关闭，避免被检测

---

## 📚 资源引用

- [examples/bilibili-member.md](./examples/bilibili-member.md) — B站大会员视频下载
- [examples/custom-player.md](./examples/custom-player.md) — 自定义播放器嗅探
- [scripts/sniff_and_download.py](./scripts/sniff_and_download.py) — 完整实现
- [references/playwright-network-api.md](./references/playwright-network-api.md) — Playwright 网络监听API参考
- [references/cookie-extraction.md](./references/cookie-extraction.md) — 跨浏览器 cookie 提取方法

---

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

## 🚀 完整工作流

### 调用示例

```
User: "从这个网站下载视频，需要登录: https://example.com/video/abc123"

Claude:
1. 检测目标网站域名: example.com
2. 查找已保存的登录态: auth/example_com.json
3. 若无 → 引导用户首次登录
4. 启动 Playwright 嗅探器
5. 监听 5-10 秒，捕获媒体资源
6. 列出候选资源，用户选择
7. 调用 yt-dlp 下载（自动注入 cookies）
8. 输出：downloads/video_title.mp4
```

### 输出结构

```
downloads/
├── example_com_video_abc123.mp4       # 最终视频
├── example_com_video_abc123.m3u8      # 原始清单（调试用）
└── metadata.json                       # 资源信息
    {
      "url": "https://cdn.example.com/hls/video.m3u8",
      "captured_at": "2026-05-08T10:45:00Z",
      "resource_type": "xhr",
      "size_estimate": "150MB",
      "format": "HLS",
      "resolution": "1920x1080"
    }
```

---

## 📊 vs 其他方案对比

| 方案 | 覆盖率 | AI调用 | 登录态 | 效率 |
|------|--------|--------|--------|------|
| **playwright-media-sniffer** | 100%（任意网站） | ✅ 自动化 | ✅ 继承 | 中（需启动浏览器） |
| **cat-catch** | 100% | ❌ 手动 | ✅ 自动 | 高（原生浏览器） |
| **yt-dlp** | 90%（1000+平台） | ✅ 完美 | ⚠️ 手动导出 | 高（无浏览器） |

**推荐策略**：
- 主流平台（YouTube/B站） → 优先 yt-dlp（已有 media-downloader skill）
- 小众/自定义播放器 → 使用本 skill
- 会员内容 → 本 skill（自动继承登录态）

---

## 🛡️ 安全与隐私

### Cookie 安全

- ✅ **本地存储**：`auth/*.json` 仅保存在本地
- ✅ **加密可选**：可使用 `cryptography` 加密 storage_state
- ⚠️ **敏感提示**：提醒用户不要分享 auth/ 目录

### 反爬风险

- **正常使用**：模拟人类行为，风险极低
- **高频调用**：避免短时间大量请求（建议间隔 ≥ 30s）
- **账号安全**：建议使用小号测试，避免主账号被封

---

## 🔍 调试模式

```python
# 开启调试输出
DEBUG = True

if DEBUG:
    # 可见浏览器
    browser = p.chromium.launch(headless=False, slow_mo=500)
    
    # 保存所有请求日志
    with open('debug_requests.log', 'w') as f:
        page.on('request', lambda req: f.write(f"{req.url}\n"))
    
    # 截图保存
    page.screenshot(path='debug_page.png', full_page=True)
```

---

## 📝 FAQ

**Q: 为什么不直接用 cat-catch？**

A: cat-catch 是浏览器扩展，需要用户手动操作。本 skill 实现了相同的嗅探逻辑，但通过 Playwright 自动化，Claude Code 可以完全自主调用。

**Q: 和 media-downloader (yt-dlp) 的区别？**

A: 
- **media-downloader**：适用于 yt-dlp 已支持的 1000+ 平台（YouTube/B站/抖音等）
- **本 skill**：适用于 yt-dlp 不支持的小众网站、自定义播放器、需登录的会员内容

两者互补，优先使用 media-downloader（更快），失败时回退到本 skill。

**Q: 支持 DRM 加密内容吗？**

A: 
- ✅ **AES-128 加密的 M3U8**：支持（yt-dlp/ffmpeg 自动解密）
- ❌ **Widevine/FairPlay DRM**：不支持（法律和技术限制）
- ⚠️ **自定义加密**：视情况，需分析 JS 解密逻辑

**Q: 下载速度如何？**

A:
- 嗅探阶段：5-10 秒（启动浏览器 + 页面加载）
- 下载阶段：取决于 yt-dlp/ffmpeg（与直接下载相同）
- **总耗时 ≈ yt-dlp + 10秒**

**Q: 能批量下载吗？**

A: 可以，但需注意：
- 每个 URL 独立会话（避免 cookie 污染）
- 建议间隔 30-60s（防止被检测）
- 可并行嗅探（多个浏览器上下文），串行下载

---

## 🎬 示例场景

### 场景 1: B站大会员视频

**需求**：下载需要大会员权限的番剧

**步骤**：
```python
# 1. 从本地 Chrome 提取 B站 cookies
cookies = browser_cookie3.chrome(domain_name='bilibili.com')

# 2. 嗅探
page.goto('https://www.bilibili.com/bangumi/play/ep123456')
# ... 监听网络请求 ...

# 3. 捕获 M3U8
# https://upos-sz-estgoss.bilivideo.com/...master.m3u8

# 4. 下载（自动注入 cookies）
yt-dlp --cookies-from-browser chrome \
       --referer https://www.bilibili.com/bangumi/play/ep123456 \
       "https://upos-sz-estgoss.bilivideo.com/...master.m3u8"
```

### 场景 2: 小众教育平台

**需求**：某在线课程平台（yt-dlp 不支持）

**步骤**：
```python
# 1. 首次手动登录
son')

# 2. 后续自动复用
context = browser.new_context(storage_state='auth/edu_platform.json')
page.goto('https://edu-platform.com/course/123/video/5')

# 3. 触发播放
page.click('.play-button')
page.wait_for_timeout(5000)

# 4. 捕获自定义播放器的 M3U8
# https://cdn.edu-platform.com/enc/abc123.m3u8?token=xyz

# 5. 下载
ffmpeg -headers "Referer: https://edu-platform.com/course/123/video/5" \
       -headers "Cookie: session=abc; token=xyz" \
       -i "https://cdn.edu-platform.com/enc/abc123.m3u8" \
       -c copy \
       course_video_5.mp4
```

### 场景 3: 企业培训视频

**需求**：公司内部培训平台（需 SSO 登录）

**步骤**：
```python
# 1. 连接用户已登录的浏览器（CDP）
# 用户先启动 Chrome: chrome --remote-debugging-port=9222
browser = playwright.chromium.connect_over_cdp('http://localhost:9222')

# 2. 无需登录，直接使用当前会话
page = browser.contexts[0].pages[0]
page.goto('https://training.company.com/video/onboarding')

# 3. 嗅探内网 CDN 资源
# https://internal-cdn.company.com/videos/onboarding.mp4

# 4. 下载（自动携带所有 cookies）
```

---

## 🧪 测试清单

开发新网站支持时的测试步骤：

- [ ] 手动打开目标页面，确认视频能播放
- [ ] Chrome DevTools → Network Tab 查看实际请求
- [ ] 确认资源格式（M3U8/MPD/MP4）
- [ ] 检查是否需要特定 headers（Referer/Cookie/token）
- [ ] 运行 sniffer，验证能否捕获
- [ ] 测试 yt-dlp 下载（传递 headers）
- [ ] 若失败，回退到 ffmpeg
- [ ] 验证输出视频可播放

---

## 🔄 持续改进

### 已知限制

- **无法处理 DRM**：Widevine/FairPlay 加密内容无法下载
- **部分反爬强的网站**：可能需要验证码/滑块（需人工介入）
- **WebSocket 流**：当前仅监听 HTTP 请求，不支持 WebSocket 推送的视频流

### 未来增强

- [ ] 支持 WebSocket 监听（`page.on('websocket')`)
- [ ] 集成验证码识别（2captcha/手动）
- [ ] 多浏览器并行嗅探（提高效率）
- [ ] 自动清单质量检测（选择最高清版本）

---

**Version**: 1.0.0  
**Last Updated**: 2026-05-08  
**Dependencies**: playwright, yt-dlp, ffmpeg, browser-cookie3
