# Known Limits

_从 playwright-media-sniffer v1.0 SKILL.md 抽取 (Line 577-596)_

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
