# Playwright Network API Reference

## 网络监听 API

### page.on('request')

监听所有HTTP请求（包括 iframe）

```python
def on_request(request):
    print(f"URL: {request.url}")
    print(f"Method: {request.method}")
    print(f"Type: {request.resource_type}")  # xhr, media, document, script...
    print(f"Headers: {request.headers}")

page.on('request', on_request)
```

**Resource Types**:
- `document` - HTML 页面
- `xhr` - AJAX 请求（M3U8 通常在此）
- `media` - `<video>/<audio>` 标签
- `fetch` - fetch API 调用
- `websocket` - WebSocket 连接（不在 request 中）

---

### page.on('response')

监听响应（可获取内容）

```python
def on_response(response):
    if '.m3u8' in response.url:
        # 读取 M3U8 内容
        try:
            content = response.text()
            print(f"M3U8 Content:\n{content}")
        except:
            pass

page.on('response', on_response)
```

**注意**：
- 只能读取文本响应（JSON/M3U8/MPD）
- 二进制流（视频分片）无法读取完整内容

---

### route.continue_() - 修改请求

```python
def handle_route(route):
    # 修改 headers
    headers = route.request.headers
    headers['X-Custom-Token'] = 'my-token'
    route.continue_(headers=headers)

# 拦截所有 .m3u8 请求并修改
page.route('**/*.m3u8', handle_route)
```

---

## Cookie 管理

### 从浏览器导入

```python
import browser_cookie3

# Chrome
cookies = browser_cookie3.chrome(domain_name='example.com')

# 转换为 Playwright 格式
playwright_cookies = []
for cookie in cookies:
    playwright_cookies.append({
        'name': cookie.name,
        'value': cookie.value,
        'domain': cookie.domain,
        'path': cookie.path,
        'expires': cookie.expires,
        'httpOnly': cookie.has_nonstandard_attr('HttpOnly'),
        'secure': cookie.secure,
        'sameSite': cookie.get_nonstandard_attr('SameSite', 'Lax')
    })

context.add_cookies(playwright_cookies)
```

---

### 保存/加载登录态

```python
# 保存（包含 cookies + localStorage + sessionStorage）
context.storage_state(path='auth_state.json')

# 加载
context = browser.new_context(storage_state='auth_state.json')
```

**storage_state.json 结构**：
```json
{
  "cookies": [
    {
      "name": "session",
      "value": "abc123",
      "domain": ".example.com",
      "path": "/",
      "expires": 1748975999,
      "httpOnly": true,
      "secure": true,
      "sameSite": "Lax"
    }
  ],
  "origins": [
    {
      "origin": "https://example.com",
      "localStorage": [
        {"name": "user_id", "value": "12345"}
      ]
    }
  ]
}
```

---

## Stealth 模式

### playwright-stealth 插件

```bash
pip install playwright-stealth
```

```python
from playwright_stealth import stealth_sync

page = context.new_page()
stealth_sync(page)  # 隐藏自动化特征
page.goto(url)
```

**隐藏特征**：
- `navigator.webdriver` → `undefined`
- `window.chrome` → 真实对象
- Canvas/WebGL 指纹随机化
- Permissions API 正常化

---

### 手动 Stealth 配置

```python
context = browser.new_context(
    # User-Agent（使用真实浏览器的）
    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    
    # 视口（常见分辨率）
    viewport={'width': 1920, 'height': 1080},
    
    # 语言和时区
    locale='zh-CN',
    timezone_id='Asia/Shanghai',
    
    # Permissions
    permissions=['geolocation', 'notifications'],
    
    # Geolocation（如果网站检测位置）
    geolocation={'latitude': 39.9, 'longitude': 116.4},  # 北京
    
    # HTTP Headers
    extra_http_headers={
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    },
    
    # 设备特征
    is_mobile=False,
    has_touch=False,
    device_scale_factor=2.0,  # Retina 屏幕
)

# 隐藏 webdriver 标志
context.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
""")
```

---

## 等待策略

### 智能等待

```python
# 等待网络空闲
page.goto(url, wait_until='networkidle')  # 500ms 无网络活动

# 等待特定请求
with page.expect_request(re.compile(r'.*\.m3u8'), timeout=10000) as request_info:
    page.click('.play-button')
m3u8_request = request_info.value

# 等待元素出现
page.wait_for_selector('video', state='attached', timeout=10000)

# 等待 JS 执行完成
page.wait_for_function('window.videoPlayer !== undefined')
```

---

## 人类行为模拟

```python
import random

# 随机延迟
async def random_delay(min_ms=500, max_ms=2000):
    await page.wait_for_timeout(random.randint(min_ms, max_ms))

# 鼠标移动
async def move_mouse_randomly():
    x = random.randint(100, 1800)
    y = random.randint(100, 900)
    await page.mouse.move(x, y, steps=random.randint(5, 15))

# 滚动
async def scroll_randomly():
    delta_y = random.randint(100, 500)
    await page.mouse.wheel(0, delta_y)

# 完整人类行为序列
async def simulate_human():
    await random_delay(1000, 2000)
    await move_mouse_randomly()
    await random_delay(500, 1500)
    await scroll_randomly()
    await random_delay(800, 1800)
```

---

## 常见模式

### 模式 1: VideoJS 播放器

```python
# 等待 VideoJS 初始化
page.wait_for_function('typeof videojs !== "undefined"')

# 提取播放源
sources = page.evaluate('''
    () => {
        const player = videojs('my-video');
        return player.currentSources();
    }
''')

print(f"Video sources: {sources}")
# [{"src": "https://cdn.example.com/video.m3u8", "type": "application/x-mpegURL"}]
```

---

### 模式 2: JWPlayer

```python
# 提取 JWPlayer 配置
config = page.evaluate('''
    () => {
        const player = jwplayer('player');
        return player.getPlaylistItem();
    }
''')

print(f"JWPlayer source: {config['file']}")
```

---

### 模式 3: 原生 `<video>` 标签

```python
# 提取 video.src
video_src = page.evaluate('''
    () => {
        const video = document.querySelector('video');
        return video ? video.src : null;
    }
''')

if video_src:
    print(f"Video source: {video_src}")
```

---

## 错误处理

```python
try:
    page.goto(url, timeout=30000)
except TimeoutError:
    print("⚠️  Page load timeout, but continuing...")
    # 某些网站页面不会完全加载，但视频已开始请求

try:
    page.click('.play-button', timeout=5000)
except:
    print("ℹ️  No play button found, video might auto-play")

# 即使没找到播放按钮，监听也会捕获自动播放的请求
```

---

## 性能优化

### 阻止无关资源加载

```python
def block_resource(route):
    if route.request.resource_type in ['image', 'stylesheet', 'font']:
        route.abort()
    else:
        route.continue_()

page.route('**/*', block_resource)

# 效果：页面加载速度提升 3-5 倍
```

---

## 调试命令

```python
# 截图当前页面
page.screenshot(path='debug.png', full_page=True)

# 打印页面 HTML
html = page.content()
with open('debug.html', 'w') as f:
    f.write(html)

# 执行 JS 调试
result = page.evaluate('console.log(window.videoConfig); return window.videoConfig;')
print(result)

# 暂停等待手动检查
page.pause()  # 打开 Playwright Inspector
```

---

**官方文档**: https://playwright.dev/python/docs/api/class-page#page-event-request

**Last Updated**: 2026-05-08
