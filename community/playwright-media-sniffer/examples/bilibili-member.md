# 示例 1: B站大会员视频下载

## 场景

下载B站番剧《某部需要大会员才能观看的动画》

**目标URL**: `https://www.bilibili.com/bangumi/play/ep123456`

---

## 前提条件

- 已在 Chrome 中登录 B站大会员账号
- 已安装 `yt-dlp` 和 `browser-cookie3`

---

## 执行步骤

### Step 1: 首次使用 - 保存登录态

```bash
python scripts/sniff_and_download.py \
    "https://www.bilibili.com/bangumi/play/ep123456" \
    --login-first
```

**流程**：
1. Playwright 打开浏览器
2. 加载目标页面
3. **暂停**，提示："⏸️  Press Enter after you've logged in..."
4. 用户在浏览器中登录（或已登录则直接）
5. 按 Enter 继续
6. 保存登录态到 `auth/bilibili_com.json`

**输出**：
```
✅ Auth state saved: auth/bilibili_com.json
💡 Next time, use: --auth-state auth/bilibili_com.json
```

---

### Step 2: 后续使用 - 自动嗅探

```bash
python scripts/sniff_and_download.py \
    "https://www.bilibili.com/bangumi/play/ep123456" \
    --auth-state auth/bilibili_com.json
```

**流程**：
1. 加载保存的登录态（自动以会员身份访问）
2. 打开番剧页面
3. 自动点击播放按钮
4. 监听网络请求 5-10 秒
5. 捕获 M3U8 资源

**捕获示例**：
```
🎯 Captured: https://upos-sz-estgoss.bilivideo.com/...master.m3u8?token=abc...
🎯 Captured: https://upos-sz-estgoss.bilivideo.com/...video.m3u8
```

---

### Step 3: 下载

脚本自动调用：
```bash
yt-dlp \
    --referer "https://www.bilibili.com/bangumi/play/ep123456" \
    --add-header "Cookie: SESSDATA=xyz; bili_jct=abc" \
    --output "downloads/bilibili_com_某番剧名_EP1.mp4" \
    "https://upos-sz-estgoss.bilivideo.com/...master.m3u8"
```

**输出**：
```
✅ Download successful!
📄 Metadata saved: downloads/metadata_1234567890.json
```

---

## 预期结果

```
downloads/
├── bilibili_com_1715123456_某番剧名_EP1.mp4    # 视频文件
└── metadata_1715123456.json                     # 元数据
    {
      "target_url": "https://www.bilibili.com/bangumi/play/ep123456",
      "captured_at": "2026-05-08 10:45:00",
      "resource_url": "https://upos-sz-estgoss.bilivideo.com/...master.m3u8",
      "resource_type": "xhr",
      "total_candidates": 3
    }
```

---

## 常见问题

### Q: 提示 "No media resources found"

**原因**：页面可能有反爬或需要更多交互

**解决**：
```bash
# 使用非 headless 模式（可见浏览器）
python scripts/sniff_and_download.py \
    "https://www.bilibili.com/bangumi/play/ep123456" \
    --auth-state auth/bilibili_com.json \
    --no-headless  # 改为可见模式

# 手动播放视频，观察 Network Tab
```

### Q: 下载失败 "403 Forbidden"

**原因**：Cookie 过期或缺少必要 headers

**解决**：
1. 重新运行 `--login-first` 刷新登录态
2. 检查是否需要额外 headers（查看 DevTools）

### Q: 视频画质不是最高清

**原因**：yt-dlp 默认选择 "best" 格式，但某些网站有多个清晰度

**解决**：
```bash
# 列出所有格式
yt-dlp -F "https://upos-sz-estgoss.bilivideo.com/...master.m3u8"

# 手动选择格式
yt-dlp -f 401+30280 "..."  # 1080P 视频 + 高音质音频
```

---

**Last Updated**: 2026-05-08
