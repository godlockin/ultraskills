# 配置指南

## 环境要求

- **Python:** >= 3.11
- **操作系统:** Windows / macOS / Linux
- **浏览器:** Firefox (Playwright 自动安装)

---

## 安装步骤

### 1. 安装 Python 依赖

```bash
cd community/quark-pan-downloader/scripts
pip install -r requirements.txt
```

**requirements.txt 内容：**
```
playwright==1.41.0
requests
```

### 2. 安装 Playwright 浏览器

```bash
playwright install firefox
```

**安装位置：**
- macOS: `~/Library/Caches/ms-playwright/`
- Linux: `~/.cache/ms-playwright/`
- Windows: `%USERPROFILE%\AppData\Local\ms-playwright\`

---

## Cookie 配置方式

### 方式 1: Playwright 自动登录（推荐）

**首次运行自动触发：**
```bash
python quark.py
# 自动打开 Firefox → 登录夸克网盘 → 按 Enter → 保存 cookie
```

**登录信息保存位置：**
```
scripts/config/cookies.txt
```

**有效期：**
- 通常 30 天
- 过期后重新运行会自动打开浏览器

---

### 方式 2: 手动获取 Cookie

**适用场景：**
- Linux 无图形界面
- Playwright 登录失败
- 需要使用特定账号

**获取步骤：**

1. Chrome 浏览器登录夸克网盘
2. F12 开发者工具
3. Application → Cookies → https://pan.quark.cn
4. 复制所有 cookie（或使用扩展导出）

**格式转换：**
```
原始格式（Chrome DevTools）:
__pus=abc123; __puus=def456; ...

目标格式（cookies.txt）:
__pus=abc123; __puus=def456; ...
```

**保存到：**
```bash
echo "__pus=abc123; __puus=def456; ..." > scripts/config/cookies.txt
```

---

## url.txt 配置

### 文件位置
```
scripts/config/url.txt
```

### 格式规范

**基本格式：**
```
https://pan.quark.cn/s/分享ID
```

**带提取码格式：**
```
https://pan.quark.cn/s/分享ID?pwd=提取码
```

**示例：**
```
https://pan.quark.cn/s/abc123
https://pan.quark.cn/s/def456?pwd=1234
https://pan.quark.cn/s/ghi789?pwd=pass
```

### 注意事项

- 每行一个链接
- 空行会被忽略
- 不支持其他网盘链接（仅夸克）
- 提取码大小写敏感

---

## 高级配置

### 自定义下载目录

**修改 quark.py 中的下载路径：**
```python
# 默认: ./downloads/
# 修改为自定义路径:
DOWNLOAD_DIR = "/Users/your_name/Downloads/Quark"
```

### 并发控制

**修改并发数（默认单线程）：**
```python
# quark.py 中找到下载函数
# 添加线程池
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as executor:
    # 下载逻辑
```

⚠️ **注意：** 并发过高可能触发限速

---

## 环境变量

可选环境变量配置：

```bash
# Cookie 文件路径
export QUARK_COOKIE_FILE="/custom/path/cookies.txt"

# URL 列表文件
export QUARK_URL_FILE="/custom/path/url.txt"

# 下载目录
export QUARK_DOWNLOAD_DIR="/custom/downloads"
```

---

## 故障排查

### Cookie 失效

**症状：**
```
登录失败: Cookie 已过期
```

**解决：**
```bash
# 删除旧 cookie
rm scripts/config/cookies.txt

# 重新运行（会自动打开浏览器登录）
python quark.py
```

### Playwright 浏览器未安装

**症状：**
```
playwright._impl._api_types.Error: Executable doesn't exist at ...
```

**解决：**
```bash
playwright install firefox
```

### 网络代理配置

**使用代理：**
```python
# 在 quark_login.py 中添加
browser = playwright.firefox.launch(
    proxy={
        "server": "http://localhost:7890",
        "username": "user",
        "password": "pass"
    }
)
```

---

## 性能优化

### 技巧 1: 预热 Cookie

首次运行后，cookie 会保存到 `config/cookies.txt`。
后续运行直接使用，无需重新登录。

### 技巧 2: 分批处理

大量链接分批处理，避免单次运行时间过长：
```bash
# url.txt 每次放 20-30 个链接
# 完成后再处理下一批
```

### 技巧 3: 离线模式

```bash
# 1. 首次运行获取 cookie
# 2. 复制 cookies.txt 到其他机器
# 3. 在无图形界面的服务器上使用
```
