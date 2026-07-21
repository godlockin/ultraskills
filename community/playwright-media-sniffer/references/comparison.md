# Comparison

_从 playwright-media-sniffer v1.0 SKILL.md 抽取 (Line 400-414)_

## 📊 vs 其他方案对比

| 方案 | 覆盖率 | AI调用 | 登录态 | 效率 |
|------|--------|--------|--------|------|
| **playwright-media-sniffer** | 100%（任意网站） | ✅ 自动化 | ✅ 继承 | 中（需启动浏览器） |
| **cat-catch** | 100% | ❌ 手动 | ✅ 自动 | 高（原生浏览器） |
| **yt-dlp** | 90%（1000+平台） | ✅ 完美 | ⚠️ 手动导出 | 高（无浏览器） |

**推荐策略**：
- 主流平台（YouTube/B站） → 优先 yt-dlp（已有 media-downloader skill）
- 小众/自定义播放器 → 使用本 skill
- 会员内容 → 本 skill（自动继承登录态）

---

