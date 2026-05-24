# 示例: reCAPTCHA v3 高分通过

## 目标

在带有 reCAPTCHA v3 保护的登录页面获得 0.9 分 (人类级别)。

## 错误示范 (得分 0.1)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://site-with-recaptcha.com/login")
    
    # 瞬间填充 - reCAPTCHA 检测到无人类行为
    page.fill("#email", "user@example.com")
    page.fill("#password", "password123")
    
    # 立即点击 - 无思考时间
    page.click("button[type=submit]")
    
    # 结果: reCAPTCHA 分数 0.1，被标记为 bot
```

## 正确做法 (得分 0.9)

```python
from cloakbrowser import launch
import time
import random

browser = launch(
    humanize=True,
    human_preset="careful",  # 更慢更谨慎
    args=["--fingerprint=my-login-session"],  # 固定身份
)

page = browser.new_page()

# 1. 访问首页先，建立正常浏览历史
page.goto("https://site-with-recaptcha.com")
time.sleep(random.uniform(2, 4))

# 2. 像人类一样点击导航到登录页
page.locator("a[href*='login']").click()
time.sleep(random.uniform(1, 2))

# 3. "阅读" 页面一会儿
time.sleep(random.uniform(3, 5))

# 4. 用 type() 而不是 fill() - humanize 自动加延迟和偶尔打错
page.type("#email", "user@example.com")
time.sleep(random.uniform(0.5, 1))

page.type("#password", "password123")
time.sleep(random.uniform(1, 2))

# 5. "思考" 一下再提交
time.sleep(random.uniform(1, 3))
page.click("button[type=submit]")

# 结果: reCAPTCHA 分数 0.9，通过验证

browser.close()
```

## 关键技巧

### 1. 绝不使用 `page.wait_for_timeout()`

```python
# ❌ 错误 - 发送 CDP 命令，reCAPTCHA 检测到
page.wait_for_timeout(3000)

# ✅ 正确 - 原生 Python sleep，对浏览器不可见
import time
time.sleep(3)
```

### 2. 用 `type()` 代替 `fill()`

```python
# ❌ fill() 瞬间设置值，无键盘事件
page.fill("#email", "user@example.com")

# ✅ type() 逐字符输入，有键盘事件
page.type("#email", "user@example.com", delay=50)

# ✅✅ humanize 模式下自动变速 + 偶尔打错
page.type("#email", "user@example.com")  # delay 自动添加
```

### 3. 固定指纹跨会话

```python
# 每次新指纹 - 对 reCAPTCHA 来说是"新设备"
browser = launch()  # ❌

# 固定指纹 - 像"老用户回访"
browser = launch(args=["--fingerprint=my-fixed-id"])  # ✅
```

### 4. 花时间在页面上

reCAPTCHA v3 评估的是**整体会话行为**，不只是提交时刻：

```python
# 好的行为模式
1. 访问首页 (2-4秒)
2. 导航到登录页 (1-2秒)  
3. "阅读" 登录页 (3-5秒)
4. 填写表单 (带停顿)
5. "思考" 后提交 (1-3秒)

# 坏的行为模式
1. 直接访问登录页
2. 瞬间填写
3. 立即提交
```

### 5. 减少 `page.evaluate()` 调用

```python
# 每次 evaluate() 都发送 CDP 流量
for i in range(10):
    await page.evaluate("...")  # ❌ 10 次 CDP 调用

# 合并为一次
await page.evaluate("""
    // 所有逻辑放一起
""")  # ✅ 1 次 CDP 调用
```

## 调试分数

```python
# 检查 reCAPTCHA 分数 (如果网站返回)
response_text = page.locator("#recaptcha-response").text_content()
print(f"reCAPTCHA 响应: {response_text}")

# 或者访问测试站点
page.goto("https://recaptcha-demo.appspot.com/recaptcha-v3-request-scores.php")
```
