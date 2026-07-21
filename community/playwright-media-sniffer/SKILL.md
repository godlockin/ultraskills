---
name: playwright-media-sniffer
description: Browser automation-based media sniffer using Playwright to inherit login state, capture M3U8/MPD/MP4 resources from any website (including custom players), and download via yt-dlp/ffmpeg with full cookie support. Use when user wants to "download video from site", "抓取视频", "下载 M3U8", "M3U8 下载", "video sniffer", "抓包下载", "登录态下载视频", "B站大会员视频下载", "登录后下视频", "继承 cookie 下视频", "嗅探网页视频", "抓包 m3u8", "继承登录态抓视频", "video download with login", or needs to bypass anti-bot for download.
version: 2.0.0
tags: [community]
---

# Playwright Media Sniffer

> 用 Playwright 继承登录态 → 嗅探 M3U8/MPD/MP4 → 用 yt-dlp/ffmpeg 下载。
> 主体只保留:触发 + 4 步索引 + 硬约束。详细机制 → references/。

## 📌 何时该用

| 触发 | 例句 |
|---|---|
| **下载网站视频** | "这个网站的视频怎么下 / 帮我下这个视频 / 抓 M3U8" |
| **登录后下载** | "我登录了但 yt-dlp 下不了 / 带 cookie 下 / 继承登录态" |
| **自定义播放器** | "这个网站是自研播放器 / 不是 YouTube 类站点 / yt-dlp 不支持" |
| **反爬绕过** | "有指纹检测 / 触发 Cloudflare / yt-dlp 直接 403" |

---

## 🚀 4 步工作流索引

按需读 references/:

| Step | 任务 | references/ |
|---|---|---|
| Step 1 | 准备浏览器状态(launch + login state) | [`step-1-browser-state.md`](references/step-1-browser-state.md) |
| Step 2 | 嗅探媒体资源(network capture) | [`step-2-sniff-media.md`](references/step-2-sniff-media.md) |
| Step 3 | 智能筛选(M3U8 / MPD / MP4 优先级) | [`step-3-filter-strategy.md`](references/step-3-filter-strategy.md) |
| Step 4 | 下载(yt-dlp / ffmpeg + cookie 注入) | [`step-4-download.md`](references/step-4-download.md) |

---

## 🧠 核心机制速览

> **3 个机制** 决定了为什么 Playwright 比 yt-dlp 强。

### 1. **嗅探原理**
浏览器自动加载所有 `<video>` / `<source>` / 加密流,Playwright 通过 `page.on("request")` 拦截所有 `.m3u8` / `.mpd` / `.mp4` 请求。

### 2. **登录态继承**
Playwright `context.add_cookies()` 注入 yt-dlp 后续使用的 cookies → 等于在已登录的浏览器里下载。

### 3. **反爬绕过**
真实 Chromium 跑在用户态,JS 引擎完整 → Cloudflare / 指纹检测看不到 bot 特征。

→ 完整机制说明: [`references/sniffing-principles.md`](references/sniffing-principles.md)
→ Playwright network API: [`references/playwright-network-api.md`](references/playwright-network-api.md)(已存在)

---

## 🚨 必守 6 条 Hard Rules

| # | Rule | 违反即停 |
|---|---|---|
| R1 | **总是先嗅探,再下载** — 不要从源码里硬猜 m3u8 URL(经常被签名 + 时效) | ✋ |
| R2 | **用 page.on("request") 不是 page.on("response")** — request 才能拿到完整 URL | ✋ |
| R3 | **cookie 必须从 Playwright context 导出到 Netscape 格式** — yt-dlp 不认 JSON | ✋ |
| R4 | **反爬站点必须真实 Chromium** — 不要用 headless flag(被识别) | ✋ |
| R5 | **M3U8 优先 MP4** — M3U8 可切片下载,失败可重试;MP4 一次下载 | ✋ |
| R6 | **下载后清理临时文件** — 不在用户机器留残留 cookie 文件 | ✋ |

---

## 💡 最佳实践速览(详细见 references/best-practices.md)

**Do**:
- ✅ 先让用户登录,导出 cookies 再下载
- ✅ 用 `playwright install chromium` 确保版本一致
- ✅ 超时设置合理(嗅探 30s / 下载 5min)
- ✅ 大文件用 M3U8 + 并发切片下载
- ✅ 失败时保留 cookie,可重试

**Don't**:
- ❌ 不要用 `--no-sandbox`(Chromium 在 root 环境失效)
- ❌ 不要在 cookie 里塞密码字段(暴露风险)
- ❌ 不要绕过付费墙(法律风险)
- ❌ 不要对同一 URL 重试超过 3 次(可能触发 ban)

→ 完整 Do/Don't: [`references/best-practices.md`](references/best-practices.md)

---

## 🔧 技术栈速览

```
Python 3.9+
├── playwright        # 浏览器自动化
├── yt-dlp            # 下载引擎
├── ffmpeg            # 切片合并
├── m3u8 / m3u8-to-mp4  # M3U8 解析
└── requests          # 兜底下载
```

→ 详细版本/依赖: [`references/tech-stack.md`](references/tech-stack.md)

---

## 🛡️ 安全与隐私(核心约束)

| 风险 | 缓解 |
|---|---|
| Cookie 文件残留 | 下载完立刻删除,不让文件活过 session |
| 反爬指纹检测 | 用真实 Chromium,不要 headless flag |
| 绕过付费墙 | **不接** — 法律风险,见 R7(虚规则,但必守) |
| 用户密码泄露 | cookie 文件加密存,只导出 netscape 标准字段 |

→ 完整安全规则: [`references/security-privacy.md`](references/security-privacy.md)

---

## 📚 资源引用

| references | 内容 |
|---|---|
| [`sniffing-principles.md`](references/sniffing-principles.md) | 嗅探原理 + 登录态继承 + 反爬绕过 完整说明 |
| [`step-1-browser-state.md`](references/step-1-browser-state.md) | 准备浏览器状态(含 login flow) |
| [`step-2-sniff-media.md`](references/step-2-sniff-media.md) | 嗅探 M3U8/MPD/MP4 资源 |
| [`step-3-filter-strategy.md`](references/step-3-filter-strategy.md) | 智能筛选(类型 + 清晰度优先级) |
| [`step-4-download.md`](references/step-4-download.md) | yt-dlp / ffmpeg + cookie 注入 |
| [`best-practices.md`](references/best-practices.md) | Do/Don't 完整清单 |
| [`tech-stack.md`](references/tech-stack.md) | 依赖 + 版本 |
| [`security-privacy.md`](references/security-privacy.md) | 安全 + 隐私 + 合规 |
| [`debug-mode.md`](references/debug-mode.md) | 调试模式 + 故障排查 |
| [`faq.md`](references/faq.md) | 13+ FAQ 问题解答 |
| [`comparison.md`](references/comparison.md) | vs yt-dlp / browser-ext / IDM 对比 |
| [`complete-workflow.md`](references/complete-workflow.md) | 完整调用示例 + 输出结构 |
| [`test-checklist.md`](references/test-checklist.md) | 30 项测试清单 |
| [`known-limits.md`](references/known-limits.md) | 已知限制 + 未来增强 |
| [`cookie-extraction.md`](references/cookie-extraction.md)(已有) | Cookie 提取细节 |
| [`playwright-network-api.md`](references/playwright-network-api.md)(已有) | Playwright network API |

| examples | 内容 |
|---|---|
| [`examples/`](examples/) | 3 个完整场景(B站大会员 / 小众教育平台 / 企业培训) |

---

## 🛠 主体自检 Checklist(每次跑前)

- [ ] Chromium 浏览器已安装(`playwright install chromium`)?
- [ ] 用户已登录(cookie 已导出到 netscape 格式)?
- [ ] M3U8 URL 是嗅探出来的(非硬编码)?
- [ ] 反爬站点用了真实 Chromium(非 headless)?
- [ ] 下载完临时文件已清理?
- [ ] 输出结构符合 examples/ 范式?
- [ ] R1-R6 全遵守?

**主公记住**:**Playwright 嗅探 + yt-dlp 下载 = 黄金组合**。纯 yt-dlp 搞不定的(自定义播放器 / 反爬)走这条链路。