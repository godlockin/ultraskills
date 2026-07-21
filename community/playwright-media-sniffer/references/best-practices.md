# Best Practices

_从 playwright-media-sniffer v1.0 SKILL.md 抽取 (Line 275-327)_

## 💡 最佳实践 (Best Practices)

### Do ✅

1. **首次运行手动登录**
   ```python
   # 保存登录态供后续使用
   context.storage_state(path='auth/site_name.json')
   ```

2. **使用 stealth 模式**
   ```python
   # 安装：pip install playwright-stealth
   from playwright_stealth import stealth_sync
   stealth_sync(page)
   ```

3. **检查资源完整性**
   ```python
   # M3U8 验证
   if '.m3u8' in url:
       resp = requests.get(url, headers=headers)
       if '#EXTM3U' not in resp.text:
           print("⚠️  Invalid M3U8 file")
   ```

4. **处理多个候选资源**
   ```python
   # 让用户选择（如检测到多个视频）
   for i, res in enumerate(best_resources, 1):
       print(f"{i}. {res['url'][:60]}...")
   choice = input("选择要下载的资源编号: ")
   ```

### Don't ❌

1. **不要在 headless 模式下处理强反爬网站**
   - 使用 `headless=False`（可见浏览器）
   - 或使用 `--stealth` 插件

2. **不要忽略 Referer 和 User-Agent**
   - 某些 CDN 强制校验
   - 必须传递给 yt-dlp/ffmpeg

3. **不要下载所有 .ts 分片**
   - 只下载主 M3U8 清单
   - 让 yt-dlp/ffmpeg 自动处理分片

4. **不要长时间停留在页面**
   - 嗅探完立即关闭，避免被检测

---

