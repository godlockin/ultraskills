# Step 1 Browser State

_从 playwright-media-sniffer v1.0 SKILL.md 抽取 (Line 119-158)_

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

