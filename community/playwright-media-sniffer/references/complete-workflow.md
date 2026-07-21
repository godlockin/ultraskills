# Complete Workflow

_从 playwright-media-sniffer v1.0 SKILL.md 抽取 (Line 363-414)_

## 🚀 完整工作流

### 调用示例

```
User: "从这个网站下载视频，需要登录: https://example.com/video/abc123"

Claude:
1. 检测目标网站域名: example.com
2. 查找已保存的登录态: auth/example_com.json
3. 若无 → 引导用户首次登录
4. 启动 Playwright 嗅探器
5. 监听 5-10 秒，捕获媒体资源
6. 列出候选资源，用户选择
7. 调用 yt-dlp 下载（自动注入 cookies）
8. 输出：downloads/video_title.mp4
```

### 输出结构

```
downloads/
├── example_com_video_abc123.mp4       # 最终视频
├── example_com_video_abc123.m3u8      # 原始清单（调试用）
└── metadata.json                       # 资源信息
    {
      "url": "https://cdn.example.com/hls/video.m3u8",
      "captured_at": "2026-05-08T10:45:00Z",
      "resource_type": "xhr",
      "size_estimate": "150MB",
      "format": "HLS",
      "resolution": "1920x1080"
    }
```

---

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

