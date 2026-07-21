# Test Checklist

_从 playwright-media-sniffer v1.0 SKILL.md 抽取 (Line 562-596)_

## 🧪 测试清单

开发新网站支持时的测试步骤：

- [ ] 手动打开目标页面，确认视频能播放
- [ ] Chrome DevTools → Network Tab 查看实际请求
- [ ] 确认资源格式（M3U8/MPD/MP4）
- [ ] 检查是否需要特定 headers（Referer/Cookie/token）
- [ ] 运行 sniffer，验证能否捕获
- [ ] 测试 yt-dlp 下载（传递 headers）
- [ ] 若失败，回退到 ffmpeg
- [ ] 验证输出视频可播放

---

## 🔄 持续改进

### 已知限制

- **无法处理 DRM**：Widevine/FairPlay 加密内容无法下载
- **部分反爬强的网站**：可能需要验证码/滑块（需人工介入）
- **WebSocket 流**：当前仅监听 HTTP 请求，不支持 WebSocket 推送的视频流

### 未来增强

- [ ] 支持 WebSocket 监听（`page.on('websocket')`)
- [ ] 集成验证码识别（2captcha/手动）
- [ ] 多浏览器并行嗅探（提高效率）
- [ ] 自动清单质量检测（选择最高清版本）

---

**Version**: 1.0.0  
**Last Updated**: 2026-05-08  
**Dependencies**: playwright, yt-dlp, ffmpeg, browser-cookie3
