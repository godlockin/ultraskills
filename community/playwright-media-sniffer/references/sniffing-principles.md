# Sniffing Principles

_从 playwright-media-sniffer v1.0 SKILL.md 抽取 (Line 31-102)_

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

