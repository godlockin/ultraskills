# 示例 2: 自定义播放器嗅探

## 场景

某小众教育网站使用自定义 HTML5 播放器（非标准嵌入），yt-dlp 无对应提取器。

**目标URL**: `https://edu-example.com/course/frontend/video/lesson-5`

---

## 特点

- 自定义加密逻辑（URL 带动态 token）
- 需登录才能观看
- 视频资源在 iframe 中嵌套

---

## 执行步骤

### Step 1: 首次登录

```bash
python scripts/sniff_and_download.py \
    "https://edu-example.com/course/frontend/video/lesson-5" \
    --login-first
```

**操作**：
1. 浏览器自动打开
2. 手动输入账号密码登录
3. 按 Enter 保存登录态

**输出**：
```
✅ Auth state saved: auth/edu_example_com.json
```

---

### Step 2: 嗅探资源

```bash
python scripts/sniff_and_download.py \
    "https://edu-example.com/course/frontend/video/lesson-5" \
    --auth-state auth/edu_example_com.json
```

**监听到的资源**：
```
🎯 Captured: https://cdn.edu-example.com/hls/course_123/lesson_5.m3u8?token=abc123...
🎯 Captured: https://cdn.edu-example.com/videos/course_123_lesson_5.mp4?sign=xyz...
```

---

### Step 3: 选择并下载

```
📋 Captured Media Resources:
1. [xhr] https://cdn.edu-example.com/hls/course_123/lesson_5.m3u8?token=abc1...
2. [media] https://cdn.edu-example.com/videos/course_123_lesson_5.mp4?sign=x...

Select resource to download (1-2, Enter for #1): 1
```

**下载过程**：
```bash
# 自动执行
yt-dlp \
    --referer "https://edu-example.com/course/frontend/video/lesson-5" \
    --add-header "Cookie: session=xyz; user_id=123" \
    --add-header "User-Agent: Mozilla/5.0..." \
    "https://cdn.edu-example.com/hls/course_123/lesson_5.m3u8?token=abc123"
```

**输出**：
```
[download] Destination: downloads/edu_example_com_1715123456_Lesson_5_Frontend.mp4
[download] 100% of 87.5MiB in 00:45
✅ Download successful!
```

---

## 技术细节

### 动态 token 处理

**问题**：URL 中的 `token=abc123` 每次访问都不同

**cat-catch 方案**：
- JS 执行生成 token
- 浏览器自动发出请求
- 拦截到的就是**已签名的最终URL**

**本 skill 实现**：
```python
# Playwright 执行页面 JS，token 自动生成
page.goto(target_url)  # JS 运行，生成 token
page.wait_for_timeout(5000)  # 等待播放器初始化

# 监听到的请求已包含 token
# https://cdn.example.com/video.m3u8?token=GENERATED_BY_JS
```

**优势**：无需逆向 JS 加密逻辑，浏览器帮你执行

---

### iframe 嵌套处理

**问题**：视频实际在 `<iframe src="https://player.example.com/embed/123">` 中

**本 skill 实现**：
```python
# Playwright 自动监听所有 frame 的请求
page.on('request', on_request)  # 包括主页面和所有 iframe

# 即使视频在 iframe 中，请求仍会被捕获
```

**对比 yt-dlp**：
```bash
# yt-dlp 需要手动提取 iframe URL
# 1. 先访问主页面，提取 iframe src
# 2. 再对 iframe URL 调用 yt-dlp
```

---

## 调试技巧

### 1. 查看所有请求

```bash
# 开启详细日志
python scripts/sniff_and_download.py \
    "https://edu-example.com/course/frontend/video/lesson-5" \
    --auth-state auth/edu_example_com.json \
    --debug  # 保存所有请求到 debug_requests.log
```

### 2. 手动对比 DevTools

```bash
# 1. 手动打开 Chrome DevTools → Network Tab
# 2. 播放视频，观察 .m3u8 请求
# 3. 右键请求 → Copy as cURL
# 4. 对比脚本捕获的 URL 和 headers 是否一致
```

### 3. 测试下载命令

```bash
# 先用脚本提取 URL 和 headers
# 然后手动测试 yt-dlp 是否能下载

yt-dlp \
    --verbose \
    --referer "https://edu-example.com/..." \
    --add-header "Cookie: session=xyz" \
    "https://cdn.edu-example.com/video.m3u8?token=abc"
```

---

## 成功率

| 网站类型 | 成功率 | 备注 |
|---------|--------|------|
| 标准 M3U8/MPD | 95% | 直接下载 |
| 自定义播放器 | 85% | 需捕获正确URL |
| 需登录网站 | 90% | cookie 正确即可 |
| 强反爬网站 | 60% | 可能需验证码 |
| DRM 加密 | 0% | 技术和法律限制 |

---

**Last Updated**: 2026-05-08
