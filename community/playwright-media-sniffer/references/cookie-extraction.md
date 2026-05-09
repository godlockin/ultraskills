# Cookie Extraction Methods

## 跨浏览器 Cookie 提取

### 方法 1: browser-cookie3 (推荐)

**安装**:
```bash
pip install browser-cookie3
```

**支持浏览器**: Chrome, Firefox, Edge, Safari, Opera, Brave

**使用**:
```python
import browser_cookie3

# Chrome
cookies = browser_cookie3.chrome(domain_name='example.com')

# Firefox
cookies = browser_cookie3.firefox(domain_name='example.com')

# Edge
cookies = browser_cookie3.edge(domain_name='example.com')

# 自动检测
cookies = browser_cookie3.load(domain_name='example.com')

# 转换为字典
cookie_dict = {c.name: c.value for c in cookies}
print(cookie_dict)
```

---

### 方法 2: Chrome DevTools 手动导出

**步骤**:
1. 打开 Chrome DevTools (F12)
2. Application → Cookies → 选择域名
3. 右键 → "Show Cookies" → 复制所有行
4. 或使用扩展: "EditThisCookie" / "Cookie Editor"

**格式转换**:
```python
# Netscape cookie 格式 (适用于 curl/wget/yt-dlp)
# domain    flag    path    secure    expiration    name    value
.example.com    TRUE    /    TRUE    1748975999    session    abc123xyz

# 保存为 cookies.txt
# 使用: yt-dlp --cookies cookies.txt <url>
```

---

### 方法 3: Playwright CDP (Chrome DevTools Protocol)

**连接已打开的浏览器**:

```bash
# 1. 启动 Chrome 并开启远程调试
chrome --remote-debugging-port=9222

# 或 Edge
msedge --remote-debugging-port=9222
```

```python
# 2. Playwright 连接
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://localhost:9222')
    
    # 使用当前已打开的页面
    context = browser.contexts[0]
    page = context.pages[0]
    
    # 直接使用，无需登录！
    page.goto('https://example.com/video')
    
    # 提取 cookies
    cookies = context.cookies()
    print(cookies)
```

**优势**:
- ✅ 无需导出 cookie 文件
- ✅ 实时使用当前登录态
- ✅ 支持多账号切换（不同 Chrome Profile）

---

## Cookie 注入到下载工具

### yt-dlp

**方法 A: Cookie 文件**
```bash
# 1. 导出 cookies 为 Netscape 格式
python -c "
import browser_cookie3
import http.cookiejar

cookies = browser_cookie3.chrome(domain_name='example.com')
jar = http.cookiejar.MozillaCookieJar('cookies.txt')
jar._cookies = cookies
jar.save(ignore_discard=True, ignore_expires=True)
"

# 2. 使用
yt-dlp --cookies cookies.txt <url>
```

**方法 B: 直接从浏览器读取**
```bash
# yt-dlp 内置支持（推荐）
yt-dlp --cookies-from-browser chrome <url>

# 指定浏览器 Profile
yt-dlp --cookies-from-browser "chrome:Profile 1" <url>
```

**方法 C: Header 注入**
```bash
# 手动拼接 Cookie header
yt-dlp --add-header "Cookie: session=abc; token=xyz" <url>
```

---

### ffmpeg

```bash
# Headers 参数（多个 header 用 \r\n 分隔）
ffmpeg \
    -headers "Cookie: session=abc123; user_id=456\r\nReferer: https://example.com/" \
    -i "https://cdn.example.com/video.m3u8" \
    -c copy \
    output.mp4
```

---

## 特殊场景

### Chrome 108+ Cookie 加密

Chrome 108+ 使用系统密钥加密 cookies，`browser-cookie3` 可能失败。

**解决方案**:

**方案 A**: 降级到 `--cookies-from-browser`
```bash
yt-dlp --cookies-from-browser chrome <url>
# yt-dlp 内置解密逻辑，支持最新 Chrome
```

**方案 B**: 使用 Chrome Profile 路径
```python
from playwright.sync_api import sync_playwright

# 指定 Chrome Profile
profile_path = Path.home() / 'Library/Application Support/Google/Chrome/Default'

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=str(profile_path),
        headless=False
    )
    # 自动继承所有登录态
```

---

### Firefox Container Tabs

Firefox 支持多账号隔离（Container Tabs）：

```python
# 提取特定 Container 的 cookies
import browser_cookie3

# Firefox 需指定 profile
firefox_profile = Path.home() / '.mozilla/firefox/abc123.default-release'
cookies = browser_cookie3.firefox(
    domain_name='example.com',
    cookie_file=firefox_profile / 'cookies.sqlite'
)
```

---

### Safari Cookies

Safari cookies 存储在加密的 keychain 中，提取复杂：

```python
# 需要 macOS keychain 访问
import keyring

# 或使用 Playwright 直接接管 Safari
with sync_playwright() as p:
    browser = p.webkit.launch()
    # ... Safari 不支持 storage_state，需手动登录
```

**推荐**: Safari 场景使用 Chrome/Edge 替代

---

## Cookie 过期处理

### 自动刷新

```python
import json
from datetime import datetime

def is_cookie_expired(auth_state_path):
    with open(auth_state_path) as f:
        state = json.load(f)
    
    for cookie in state['cookies']:
        expires = cookie.get('expires', -1)
        if expires != -1 and expires < datetime.now().timestamp():
            return True
    return False

# 检查并刷新
if is_cookie_expired('auth/example_com.json'):
    print("🔄 Cookies expired, re-login required")
    # 触发重新登录流程
```

---

### Cookie 存活时间

| 网站类型 | 典型过期时间 | 建议刷新频率 |
|---------|-------------|-------------|
| 短视频平台 | 7-30 天 | 每月 |
| 会员网站 | 14-90 天 | 每季度 |
| 教育平台 | 30-180 天 | 半年 |
| 企业内网 | 1-7 天 | 每周 |

---

## 安全最佳实践

### 存储

```python
# ❌ 不要明文存储
# auth/example_com.json 直接保存在 git 仓库

# ✅ 加密存储
from cryptography.fernet import Fernet

key = Fernet.generate_key()  # 保存在 .env
cipher = Fernet(key)

# 加密
with open('auth_state.json', 'rb') as f:
    encrypted = cipher.encrypt(f.read())
    
with open('auth_state.enc', 'wb') as f:
    f.write(encrypted)

# 解密
with open('auth_state.enc', 'rb') as f:
    decrypted = cipher.decrypt(f.read())
    
import json
state = json.loads(decrypted)
```

### .gitignore

```gitignore
# 必须忽略
auth/*.json
auth/*.enc
cookies.txt
*.cookie
storage_state*.json
```

---

**Last Updated**: 2026-05-08
