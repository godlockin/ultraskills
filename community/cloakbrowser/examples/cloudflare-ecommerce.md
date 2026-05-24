# 示例: 绕过 Cloudflare 保护的电商网站

## 场景

爬取受 Cloudflare 保护的电商网站商品信息。

## 错误示范 (会被拦截)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://protected-ecommerce.com")
    # 大概率触发 Cloudflare 挑战页面
```

## 正确做法

```python
from cloakbrowser import launch
import time

# 最佳配置
browser = launch(
    headless=False,                           # headed 模式
    proxy="socks5://user:pass@proxy:1080",   # 住宅代理
    geoip=True,                               # 自动匹配时区
    humanize=True,                            # 人类行为模拟
    args=["--fingerprint=ecommerce-session"], # 固定指纹
)

page = browser.new_page()

# 首次访问 - 可能需要等待 Turnstile
page.goto("https://protected-ecommerce.com")
time.sleep(5)  # 用原生 sleep，不是 page.wait_for_timeout()

# 人类行为模拟已自动启用，直接操作即可
page.locator("#search").fill("iPhone 15")  # humanize 自动逐字符输入
page.locator("button[type=submit]").click()  # humanize 自动贝塞尔曲线移动

# 滚动加载更多
for _ in range(3):
    page.mouse.wheel(0, 500)
    time.sleep(2)

# 提取数据
products = page.locator(".product-card").all()
for product in products:
    name = product.locator(".name").text_content()
    price = product.locator(".price").text_content()
    print(f"{name}: {price}")

browser.close()
```

## 关键点

1. **`headless=False`** - Cloudflare 对无头浏览器检测严格
2. **住宅代理** - 数据中心 IP 会被直接拉黑
3. **`geoip=True`** - UTC 时区 + en-US 语言但 IP 在东京 = 明显 bot
4. **`humanize=True`** - 让所有操作像人类
5. **固定 `--fingerprint`** - 重复访问同一站点用同一身份
6. **`time.sleep()` 而非 `wait_for_timeout()`** - 后者发送 CDP 命令

## 失败排查

如果仍被拦截：

```python
# 1. 检查是否卡在 Turnstile
if "challenge" in page.content().lower():
    print("需要手动解决 Turnstile")
    page.wait_for_url("**/products**", timeout=60000)  # 等待人工通过

# 2. 截图调试
page.screenshot(path="debug.png")

# 3. 检查 IP 信誉
page.goto("https://whatismyipaddress.com")
```
