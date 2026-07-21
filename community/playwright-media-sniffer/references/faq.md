# Faq

_从 playwright-media-sniffer v1.0 SKILL.md 抽取 (Line 451-487)_

## 📝 FAQ

**Q: 为什么不直接用 cat-catch？**

A: cat-catch 是浏览器扩展，需要用户手动操作。本 skill 实现了相同的嗅探逻辑，但通过 Playwright 自动化，Claude Code 可以完全自主调用。

**Q: 和 media-downloader (yt-dlp) 的区别？**

A: 
- **media-downloader**：适用于 yt-dlp 已支持的 1000+ 平台（YouTube/B站/抖音等）
- **本 skill**：适用于 yt-dlp 不支持的小众网站、自定义播放器、需登录的会员内容

两者互补，优先使用 media-downloader（更快），失败时回退到本 skill。

**Q: 支持 DRM 加密内容吗？**

A: 
- ✅ **AES-128 加密的 M3U8**：支持（yt-dlp/ffmpeg 自动解密）
- ❌ **Widevine/FairPlay DRM**：不支持（法律和技术限制）
- ⚠️ **自定义加密**：视情况，需分析 JS 解密逻辑

**Q: 下载速度如何？**

A:
- 嗅探阶段：5-10 秒（启动浏览器 + 页面加载）
- 下载阶段：取决于 yt-dlp/ffmpeg（与直接下载相同）
- **总耗时 ≈ yt-dlp + 10秒**

**Q: 能批量下载吗？**

A: 可以，但需注意：
- 每个 URL 独立会话（避免 cookie 污染）
- 建议间隔 30-60s（防止被检测）
- 可并行嗅探（多个浏览器上下文），串行下载

---

