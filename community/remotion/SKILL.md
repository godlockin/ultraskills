---
name: remotion
description: 使用 React 和 Remotion 框架创建程序化视频 (Programmatic video creation with React). Generate animations, effects, data-driven personalized videos, and render to MP4/WebM/GIF. Trigger when the user mentions Remotion, programmatic video, React-based video, useCurrentFrame, interpolate, spring, Sequence, or wants to render a video from code.
github_url: https://github.com/remotion-dev/remotion
github_hash: e135efdba7d0a9385f4bed016dbe7157b639126e
version: 2.0.0
created_at: 2026-04-21
entry_point: scripts/wrapper.py
tags: [video, react, remotion, animation, creative, automation]
dependencies: ["node>=18", "npm/pnpm/bun", "ffmpeg (auto-installed by Remotion)"]
homepage: https://www.remotion.dev
docs: https://www.remotion.dev/docs
api_reference: https://www.remotion.dev/api
license_note: Remotion has a special license — a company license is required in some commercial cases. See https://github.com/remotion-dev/remotion/blob/main/LICENSE.md
supersedes: [remotion-video, remotion-video-creator]
---

# Remotion - React 程序化视频制作

> 使用 React 组件和 Web 技术 (CSS、Canvas、SVG、WebGL) 创建专业级程序化视频。告别传统视频编辑软件,用代码创作视频!

Source: https://github.com/remotion-dev/remotion (pinned to commit `e135efd`).

## ⚠️ License (must read before commercial use)

Remotion 使用**特殊许可证**。某些商业场景需获得 company license。商用上线前**务必阅读** https://github.com/remotion-dev/remotion/blob/main/LICENSE.md

## 🎯 目标 (Goal)

- 快速搭建 Remotion 视频项目
- 使用 React 组件构建视频场景
- 创建流畅的动画和过渡效果
- 实现数据驱动的批量视频生成
- 将视频渲染为 MP4/WebM/GIF 等格式

## 🧠 核心概念 (Core Concepts)

### Remotion 是什么?

Remotion 是一个用 React 创建视频的框架,核心理念:**视频是时间的函数,每一帧都是一个 React 渲染**。

```
视频 = f(帧号) → React 组件 → 图像序列 → 视频文件
```

### 核心优势

| 优势 | 说明 |
|------|------|
| **Web 技术** | 使用 CSS、Canvas、SVG、WebGL 等所有 Web 技术 |
| **编程能力** | 变量、函数、API、算法创造无限可能 |
| **React 生态** | 可复用组件、强大组合、热更新、npm 包生态 |
| **数据驱动** | 从 API/数据库生成个性化视频 |

## 🚀 快速开始 (Quick Start)

### Step 1: 创建项目

```bash
# npm
npx create-video@latest

# bun
bunx create-video@latest

# pnpm
pnpm create video
```

或使用本 skill 的 wrapper:

```bash
python scripts/wrapper.py init my-video         # 脚手架
python scripts/wrapper.py render my-video out.mp4  # 渲染
```

启动开发服务器:

```bash
cd my-video
npm run dev
```

### Step 2: 项目结构

```
my-video/
├── src/
│   ├── Root.tsx          # 注册所有 Composition
│   ├── Composition.tsx   # 视频组件
│   └── ...
├── public/               # 静态资源
├── remotion.config.ts    # Remotion 配置
└── package.json
```

### Step 3: 核心 API

```tsx
import {
  useCurrentFrame,     // 获取当前帧号
  useVideoConfig,      // 获取视频配置 (fps, width, height, durationInFrames)
  AbsoluteFill,        // 全屏容器
  Sequence,            // 序列/时间线
  spring,              // 弹簧动画
  interpolate,         // 插值函数
  Img, Video, Audio,   // 媒体组件
} from "remotion";
```

## 📐 视频属性 (Video Properties)

```tsx
<Composition
  id="MyVideo"
  component={MyVideo}
  durationInFrames={300}
  fps={30}
  width={1920}
  height={1080}
/>
```

**常用配置**:

| 用途 | 分辨率 | fps | 说明 |
|------|--------|-----|------|
| YouTube | 1920×1080 | 30 | 标准高清 |
| TikTok/Reels | 1080×1920 | 30 | 竖屏短视频 |
| Twitter | 1280×720 | 30 | 社交媒体 |
| GIF | 480×480 | 15 | 动图 |

## 🎬 动画技巧 (Animation Techniques)

### 基础: `useCurrentFrame`

```tsx
const MyAnimation = () => {
  const frame = useCurrentFrame();
  return (
    <div style={{
      transform: `translateX(${frame * 2}px)`,
      opacity: Math.min(1, frame / 30)
    }}>
      Moving Text
    </div>
  );
};
```

### 进阶: `interpolate`

```tsx
const MyAnimation = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });
  const scale   = interpolate(frame, [0, 30], [0.5, 1]);
  return <div style={{ opacity, transform: `scale(${scale})` }}>Fade In & Scale Up</div>;
};
```

### 高级: `spring` 弹簧动画

```tsx
const MyAnimation = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({
    frame, fps,
    config: { damping: 10, stiffness: 100, mass: 0.5 },
  });
  return <div style={{ transform: `scale(${scale})` }}>Bouncy</div>;
};
```

## ⏱️ 时间线管理 (Timeline)

### `<Sequence>` — 自由定位

```tsx
<AbsoluteFill>
  <Sequence from={0}   durationInFrames={60}>  <Title text="Hello!" /> </Sequence>
  <Sequence from={30}  durationInFrames={90}>  <Content />              </Sequence>
  <Sequence from={100}>                         <Ending />               </Sequence>
</AbsoluteFill>
```

### `<Series>` — 顺序播放

```tsx
import { Series } from "remotion";

<Series>
  <Series.Sequence durationInFrames={60}>  <Intro />       </Series.Sequence>
  <Series.Sequence durationInFrames={120}> <MainContent /> </Series.Sequence>
  <Series.Sequence durationInFrames={60}>  <Outro />       </Series.Sequence>
</Series>
```

## 🖼️ 媒体素材 (Media Assets)

```tsx
import { Img, Video, OffthreadVideo, Audio, staticFile } from "remotion";

<Img src={staticFile("logo.png")} />
<Img src="https://example.com/image.jpg" />

<Video src={staticFile("background.mp4")} />
<OffthreadVideo src={staticFile("background.mp4")} />  // 推荐用于长视频

<Audio src={staticFile("music.mp3")} volume={0.5} />
```

## 🎨 效果模板 (Effect Templates)

### 文字打字机

```tsx
const TypeWriter = ({ text }: { text: string }) => {
  const frame = useCurrentFrame();
  const charsToShow = Math.floor(frame / 3);
  return <span>{text.slice(0, charsToShow)}</span>;
};
```

### 淡入淡出

```tsx
const FadeInOut = ({ children }: { children: React.ReactNode }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const opacity = interpolate(
    frame,
    [0, 20, durationInFrames - 20, durationInFrames],
    [0, 1, 1, 0]
  );
  return <div style={{ opacity }}>{children}</div>;
};
```

### 缩放进入

```tsx
const ZoomIn = ({ children }: { children: React.ReactNode }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({ frame, fps, config: { damping: 12 } });
  return <div style={{ transform: `scale(${scale})` }}>{children}</div>;
};
```

## 📤 渲染输出 (Rendering)

### 命令行

```bash
# MP4
npx remotion render src/index.ts MyComposition out/video.mp4

# GIF
npx remotion render src/index.ts MyComposition out/animation.gif

# 指定帧范围
npx remotion render src/index.ts MyComposition out/clip.mp4 --frames=0-90

# 不同编码器
npx remotion render src/index.ts MyComposition out/video.webm --codec=vp8
```

### Remotion Studio

1. `npm run dev` 打开 Studio
2. 点击 "Render"
3. 选择格式和质量
4. 等待完成

### Remotion Lambda (大规模渲染)

详见 https://www.remotion.dev/docs/lambda

## 💡 最佳实践 (Best Practices)

### ✅ Do

- **组件化设计** - 将场景拆分为可复用组件
- **使用 TypeScript** - 类型安全减少运行时错误
- **预加载资源** - 使用 `delayRender` 确保资源加载完成
- **使用 `staticFile`** - 引用 public 目录中的资源
- **测试关键帧** - 在 Studio 中逐帧检查动画

### ❌ Don't

- **避免随机值** - 随机值导致每帧结果不一致
- **避免 `useEffect` 副作用** - 可能导致渲染不确定
- **避免大量 DOM 节点** - 影响渲染性能
- **避免同步获取数据** - 使用 `delayRender` 异步加载

## 📚 进阶资源

- 官方文档: https://www.remotion.dev/docs
- API 参考: https://www.remotion.dev/api
- 示例展示: https://remotion.dev/showcase
- GitHub: https://github.com/remotion-dev/remotion
- Discord: https://remotion.dev/discord

## 🔧 与其他 Skill 配合

- **gemini-image-optimizer** - 优化视频中使用的图片素材
- **prompt-engineer** - 生成视频脚本和创意文案
- **video-frame-extractor** - 从现有视频提取帧作为素材
- **image-to-video** - 单图转视频片段
- **slack-gif-creator** - 短 GIF 输出辅助

## 📜 历史与合并

本 skill 由以下来源合并而成 (2026-04-21):

| 原 skill | 贡献 |
|---|---|
| `community/remotion-video/` (name: "Remotion Video Creator") | 中文教程、API 速查、动画/时间线/效果模板、最佳实践 |
| `community/remotion/` (auto-scaffolded) | 扩展元数据 (`github_url`/`github_hash`)、license 警告、wrapper.py |
| `remotion-dev/remotion` 上游 README | 项目定位、Lambda、Discord 等链接 |

合并后:`community/remotion-video/` 已删除,统一为 `community/remotion/`。

## Update policy

`github_hash` 已锁定到 `e135efdb`。如需刷新,重新运行 `github-to-skills` 并 bump `github_hash` + `version`。
