# Step 4 Download

_从 playwright-media-sniffer v1.0 SKILL.md 抽取 (Line 233-274)_

### Step 4: 下载

```python
import subprocess

for res in best_resources:
    url = res['url']
    headers = res['headers']
    
    # 提取 cookies
    cookie_str = '; '.join([f"{k}={v}" for k, v in headers.items() if k.lower() == 'cookie'])
    
    # 构造 yt-dlp 命令
    cmd = [
        'yt-dlp',
        '--add-header', f'Referer: {target_url}',
        '--add-header', f'Cookie: {cookie_str}',
        '--add-header', f'User-Agent: {headers.get("user-agent", "")}',
        '--output', 'downloads/%(title)s.%(ext)s',
        url
    ]
    
    print(f"📥 Downloading: {url[:60]}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Success!")
    else:
        # Fallback: ffmpeg 直接下载（适用于 yt-dlp 不支持的格式）
        print(f"⚠️  yt-dlp failed, trying ffmpeg...")
        cmd_ffmpeg = [
            'ffmpeg',
            '-headers', f'Referer: {target_url}\r\nCookie: {cookie_str}',
            '-i', url,
            '-c', 'copy',
            f'downloads/video_{hash(url)}.mp4'
        ]
        subprocess.run(cmd_ffmpeg)
```

---

