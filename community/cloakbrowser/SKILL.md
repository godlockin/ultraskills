---
name: cloakbrowser
description: "隐身浏览器自动化 - 使用 CloakBrowser (C++ 源码级反检测) 绕过 Cloudflare、reCAPTCHA、FingerprintJS 等反爬系统，Playwright API 兼容"
version: 1.0.0
tags: [browser, automation, stealth, antibot, cloudflare, recaptcha, playwright, scraping, fingerprint]
recommended_for:
  - 绕过 Cloudflare Turnstile
  - 绕过 reCAPTCHA v3
  - 反指纹检测
  - 隐身爬虫
  - 受保护网站自动化
---

# CloakBrowser - 隐身浏览器自动化

> **58 个 C++ 源码级补丁** — 不是 JS 注入，不是配置 hack，而是真正的 Chromium 源码修改

## 核心能力

| 检测系统 | Playwright 原生 | CloakBrowser |
|---------|----------------|--------------|
| reCAPTCHA v3 分数 | 0.1 (bot) | **0.9 (human)** |
| Cloudflare Turnstile | ❌ Fail | ✅ Pass |
| FingerprintJS | ❌ Detected | ✅ Pass |
| BrowserScan | ❌ Detected | ✅ Normal |
| `navigator.webdriver` | `true` | **`false`** |
| `navigator.plugins` | 空数组 | **5 个插件** |

## 安装

```bash
pip install cloakbrowser
# 首次运行自动下载 ~200MB 的定制 Chromium 二进制
```

## 快速开始

### 基础用法 (3 行代码)

```python
from cloakbrowser import launch

browser = launch()
page = browser.new_page()
page.goto("https://protected-site.com")  # 不再被拦截
browser.close()
```

### 推荐配置 (严格反爬站点)

```python
from cloakbrowser import launch

browser = launch(
    proxy="socks5://user:pass@proxy:1080",  # 住宅代理
    geoip=True,      # 自动匹配时区/语言到代理 IP
    headless=False,  # headed 模式更隐蔽
    humanize=True,   # 模拟真人鼠标/键盘/滚动
)
page = browser.new_page()
page.goto("https://heavily-protected-site.com")
```

### 异步版本

```python
import asyncio
from cloakbrowser import launch_async

async def main():
    browser = await launch_async(humanize=True)
    page = await browser.new_page()
    await page.goto("https://example.com")
    print(await page.title())
    await browser.close()

asyncio.run(main())
```

## API 参考

### `launch()` / `launch_async()`

| 参数 | 类型 | 说明 |
|------|------|------|
| `headless` | bool | 无头模式 (默认 True，严格站点建议 False) |
| `proxy` | str | 代理地址 `http://` 或 `socks5://` |
| `geoip` | bool | 自动从代理 IP 检测时区/语言 |
| `humanize` | bool | 启用人类行为模拟 |
| `human_preset` | str | `"default"` 或 `"careful"` (更慢更谨慎) |
| `args` | list | 额外 Chrome 启动参数 |
| `timezone` | str | 时区 (如 `"America/New_York"`) |
| `locale` | str | 语言 (如 `"en-US"`) |

### `launch_persistent_context()` - 持久会话

保持 cookies/localStorage 跨会话，绕过隐身检测：

```python
from cloakbrowser import launch_persistent_context

# 首次运行 - 登录并保存状态
ctx = launch_persistent_context("./my-profile", headless=False)
page = ctx.new_page()
page.goto("https://site-requiring-login.com")
# 手动登录...
ctx.close()

# 后续运行 - 自动恢复登录状态
ctx = launch_persistent_context("./my-profile")
page = ctx.new_page()
page.goto("https://site-requiring-login.com")  # 已登录
```

### 指纹管理

```python
# 随机指纹 (每次启动不同身份)
browser = launch()

# 固定指纹 (同一身份，适合重复访问同一站点)
browser = launch(args=["--fingerprint=12345"])

# 自定义 GPU 伪装
browser = launch(args=[
    "--fingerprint-gpu-vendor=Intel Inc.",
    "--fingerprint-gpu-renderer=Intel Iris OpenGL Engine",
])
```

## 人类行为模拟 (`humanize=True`)

| 行为 | 默认 Playwright | CloakBrowser humanize |
|------|----------------|----------------------|
| 鼠标移动 | 瞬移 | 贝塞尔曲线 + 轻微超调 |
| 点击 | 即时 | 真实落点 + 按住时长 |
| 打字 | 瞬间填充 | 逐字符 + 思考停顿 + 偶尔打错自动修正 |
| 滚动 | 跳跃 | 加速→匀速→减速 |

```python
browser = launch(humanize=True, human_config={
    "mistype_chance": 0.05,        # 5% 打错率 (自动修正)
    "typing_delay": 100,           # 打字间隔 ms
    "idle_between_actions": True,  # 动作间微移动
})
```

## 与其他工具集成

### browser-use (AI Agent)

```python
from cloakbrowser import launch_async

browser = await launch_async(args=["--remote-debugging-port=9242"])
# browser-use 连接到 http://127.0.0.1:9242
```

### Crawl4AI / Scrapling

```python
from cloakbrowser.download import ensure_binary
from cloakbrowser.config import get_default_stealth_args

binary_path = ensure_binary()
stealth_args = get_default_stealth_args()
# 传给框架的 browser_executable_path 和 browser_args
```

## 常见问题

### 仍被 Cloudflare 拦截？

1. 使用 **住宅代理** (数据中心 IP 直接被拉黑)
2. 设置 `headless=False` (某些站点检测无头模式)
3. 启用 `geoip=True` (时区/语言与 IP 不匹配是 bot 信号)
4. 启用 `humanize=True` (行为检测)

### reCAPTCHA v3 分数低？

```python
# 不要用 page.wait_for_timeout() - 会发送 CDP 命令
import time
time.sleep(3)  # 用原生 sleep

# 用 page.type() 而不是 page.fill()
page.type("#email", "user@example.com", delay=50)
```

### macOS 首次运行被阻止？

```bash
xattr -cr ~/.cloakbrowser/chromium-*/Chromium.app
```

## 相关 Skills

- `playwright-media-sniffer` - 使用 Playwright 嗅探媒体资源
- `browse` (gstack) - AI 控制的浏览器自动化
- `baoyu-url-to-markdown` - URL 转 Markdown (含 CDP)

## 参考资料

- [CloakBrowser GitHub](https://github.com/CloakHQ/CloakBrowser)
- [反检测原理](references/anti-detection-explained.md)
- [测试报告](references/test-results.md)
