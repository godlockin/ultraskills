# Step 2 Sniff Media

_从 playwright-media-sniffer v1.0 SKILL.md 抽取 (Line 159-197)_

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

