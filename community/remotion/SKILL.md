---
name: remotion
description: 使用 React 和 Remotion 框架创建程序化视频 (Programmatic video creation with React). Generate animations, effects, data-driven personalized videos, and render to MP4/WebM/GIF. Trigger when the user mentions Remotion, programmatic video, React-based video, useCurrentFrame, interpolate, spring, Sequence, or wants to render a video from code. NOTE: Remotion 使用受限许可证,部分商业场景需 company license。NOT-FOR: 剪辑/拼接/裁剪已有素材(用 ffmpeg)、单纯抽帧、长片非线性编辑。
github_url: https://github.com/remotion-dev/remotion
github_hash: e135efdba7d0a9385f4bed016dbe7157b639126e
version: 2.1.0
created_at: 2026-04-21
entry_point: scripts/wrapper.py
remotion_version: "^4.0"
last_verified: 2026-08-30
tags: [video, react, remotion, animation, creative, automation, license-restricted]
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

## 📌 版本基线

本 skill 的所有 API 示例基于 **Remotion 4.x** 验证(`last_verified: 2026-08-30`)。

```bash
# 若要与本文档完全一致,安装时锁定 major 版本
npm i remotion@^4.0 @remotion/cli@^4.0
```

`npx create-video@latest` 总是拉取**最新 major**。若 Remotion 已发布 5.x 而你需要按本文档操作,先锁 4.x;或对照 https://www.remotion.dev/docs/migration 自行迁移。

> 出现 `X is not exported from 'remotion'` 类错误,基本可判定为 major 版本不匹配。

## 🚫 何时不该用 Remotion

Remotion 的强项是**用代码生成**视频。以下场景用它是绕远路:

| 需求 | 该用什么 | 为什么不用 Remotion |
|---|---|---|
| 剪辑/拼接/裁剪已有视频 | `ffmpeg` 两行命令 | Remotion 会逐帧重渲染,慢百倍且有损重编码 |
| 从视频里抽某几帧图 | `ffmpeg -ss ... -vframes 1` | 无需搭 React 项目 |
| 小体积循环 GIF / 表情包 | 专用 GIF 工具 | Remotion 渲 GIF 需额外调参才能控体积 |
| 长片非线性编辑(多轨、调色) | Premiere / DaVinci / FCP | Remotion 无时间线 UI,不适合手工剪辑 |
| 单张图加平移缩放 | ffmpeg zoompan 滤镜 | 一条滤镜就够 |

**该用 Remotion 的信号**:数据驱动批量生成、需要 React 组件复用、需要程序化控制每一帧、需要 CI 里自动出片。

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

或使用本 skill 的 wrapper(会先做环境预检,并给出并发建议):

```bash
python3 scripts/wrapper.py preflight                          # 检查 node/ffmpeg/磁盘
python3 scripts/wrapper.py init my-video                      # 脚手架
python3 scripts/wrapper.py studio --dir my-video              # 启动 Studio
python3 scripts/wrapper.py render MyComp out.mp4 --dir my-video
python3 scripts/wrapper.py render MyComp out.mp4 --dir my-video \
        --concurrency 4 --scale 0.5 --props data.json
```

wrapper 只是官方 CLI 的薄封装,额外做三件事:渲染前预检环境、自动设置合理并发、GIF 输出自动补 `--codec=gif --every-nth-frame`。

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

### `<TransitionSeries>` — 带转场的顺序播放

需要 `@remotion/transitions`。转场帧数从相邻两段中**扣除**,不是额外增加。

```tsx
import { TransitionSeries, linearTiming, springTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";
import { wipe } from "@remotion/transitions/wipe";

<TransitionSeries>
  <TransitionSeries.Sequence durationInFrames={60}>
    <Intro />
  </TransitionSeries.Sequence>

  <TransitionSeries.Transition
    presentation={fade()}
    timing={linearTiming({ durationInFrames: 15 })}
  />

  <TransitionSeries.Sequence durationInFrames={120}>
    <MainContent />
  </TransitionSeries.Sequence>

  <TransitionSeries.Transition
    presentation={slide({ direction: "from-right" })}
    timing={springTiming({ config: { damping: 200 } })}
  />

  <TransitionSeries.Sequence durationInFrames={60}>
    <Outro />
  </TransitionSeries.Sequence>
</TransitionSeries>
```

| 转场 | 导入 | 适用 |
|---|---|---|
| `fade()` | `@remotion/transitions/fade` | 通用,最安全 |
| `slide({direction})` | `.../slide` | 场景推进感 |
| `wipe({direction})` | `.../wipe` | 板块切换 |
| `flip()` | `.../flip` | 强调转折 |
| `clockWipe({width,height})` | `.../clock-wipe` | 计时/进度感 |

**时长换算**:`总时长 = Σ段时长 − Σ转场时长`。上例为 60+120+60−15−(spring 实际帧数)。

### Easing — 别让动画都是线性的

`interpolate` 默认线性,观感生硬。加 `easing` 立刻显得专业:

```tsx
import { interpolate, Easing } from "remotion";

// 线性(默认)— 机械感
const linear = interpolate(frame, [0, 30], [0, 1]);

// 缓出 — 最常用,快进慢停,自然
const easeOut = interpolate(frame, [0, 30], [0, 1], {
  easing: Easing.out(Easing.cubic),
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});

// 缓入缓出 — 适合位移
const easeInOut = interpolate(frame, [0, 30], [0, 1], {
  easing: Easing.inOut(Easing.ease),
  extrapolateRight: "clamp",
});

// 自定义贝塞尔 — 对齐设计稿的曲线
const custom = interpolate(frame, [0, 30], [0, 1], {
  easing: Easing.bezier(0.25, 0.1, 0.25, 1),
  extrapolateRight: "clamp",
});
```

| 场景 | 推荐 easing |
|---|---|
| 淡入淡出 | `Easing.out(Easing.cubic)` |
| 位移/滑入 | `Easing.inOut(Easing.ease)` |
| 弹性出现 | 直接用 `spring()`,不用 interpolate |
| 匀速滚动/字幕 | 保持线性 |

> **务必加 `extrapolateRight: "clamp"`** — 否则动画结束后数值会继续外推,造成元素飞出画面。

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

# GIF — 必须显式指定 codec 与抽帧,否则体积失控
npx remotion render src/index.ts MyComposition out/animation.gif \
    --codec=gif --every-nth-frame=2 --fps=15

# 指定帧范围
npx remotion render src/index.ts MyComposition out/clip.mp4 --frames=0-90

# 不同编码器
npx remotion render src/index.ts MyComposition out/video.webm --codec=vp8
```

### 性能参数(长渲染必调)

视频渲染是重计算步骤 — 每个 worker 是一个 Chrome 实例。

| 参数 | 作用 | 建议 |
|---|---|---|
| `--concurrency=N` | 并发 worker 数 | **≈ CPU 核数 / 2**;1080p 时每 worker 约占 1.5GB RAM。OOM 就下调 |
| `--scale=0.5` | 分辨率缩放 | 预览/草稿用 0.5,成片用 1 |
| `--jpeg-quality=80` | 中间帧质量 | 默认 80;调低加快但画质降 |
| `--timeout=60000` | 单帧超时(ms) | 默认 30000;有网络请求的合成需调高 |
| `--frames=A-B` | 只渲部分帧 | 调试动画时只渲关键段 |
| `--gl=angle` | 渲染后端 | Chrome 崩溃或 WebGL 异常时尝试 |

**内存估算**:`并发数 × 1.5GB ≈ 峰值 RAM`(1080p)。4K 约翻 3-4 倍。

**长视频策略**:

| 时长 | 做法 |
|---|---|
| < 2 min | 直接单次渲染 |
| 2-10 min | 分段渲染 `--frames=0-3599`、`--frames=3600-7199`,再用 `ffmpeg -f concat` 合并 |
| > 10 min 或需批量 | `@remotion/lambda` 云端并行 fan-out |

分段的好处:第 15000 帧崩了只需重渲那一段,不是从头开始。嵌入长素材时**必须**用 `<OffthreadVideo>` 而非 `<Video>`。

### Remotion Studio

1. `npm run dev` 打开 Studio
2. 点击 "Render"
3. 选择格式和质量
4. 等待完成

### Remotion Lambda (大规模渲染)

详见 https://www.remotion.dev/docs/lambda

## ⏳ 异步资源加载 (delayRender / continueRender)

`delayRender()` 告诉 Remotion「先别截这一帧」,**必须**配对调用 `continueRender(handle)` 释放。忘了释放会让渲染卡到超时。

```tsx
import { delayRender, continueRender } from "remotion";
import { useEffect, useState } from "react";

export const DataDriven: React.FC = () => {
  // 带 label 便于超时时定位是哪一处没释放
  const [handle] = useState(() => delayRender("fetching-chart-data"));
  const [data, setData] = useState<Item[] | null>(null);

  useEffect(() => {
    fetch("https://api.example.com/data")
      .then((r) => r.json())
      .then((d) => {
        setData(d);
        continueRender(handle);   // ← 成功路径必须释放
      })
      .catch((e) => {
        cancelRender(e);          // ← 失败路径:让渲染带错误退出,而不是挂住
      });
  }, [handle]);

  if (!data) return null;
  return <Chart data={data} />;
};
```

**三条铁律**:
1. 每个 `delayRender()` 都有恰好一个 `continueRender()`
2. 失败路径用 `cancelRender(err)`,不要静默 catch — 否则渲染挂到超时才失败
3. 默认超时 30s,慢接口需 `--timeout` 调高

## 🔤 字体加载(最常见的踩坑)

在 Studio 里字体正常,渲出来变成 Times/fallback —— 因为渲染在字体加载完成前就截帧了。

```tsx
// 方案 A:Google Fonts(推荐)
import { loadFont } from "@remotion/google-fonts/Inter";
const { fontFamily, waitUntilDone } = loadFont();

// 在组件外触发,并让 Remotion 等它完成
await waitUntilDone();

export const Title = () => <div style={{ fontFamily }}>标题</div>;
```

```tsx
// 方案 B:本地字体 + delayRender 门控
import { delayRender, continueRender, staticFile } from "remotion";

const handle = delayRender("load-custom-font");
const font = new FontFace(
  "MyFont",
  `url(${staticFile("fonts/MyFont.woff2")})`
);
font.load().then(() => {
  document.fonts.add(font);
  continueRender(handle);
});
```

**自查**:渲一帧成图(`--frames=0-0`)确认字体正确,再跑全片。

## 🚨 故障排查 (Troubleshooting)

| 症状 | 根因 | 处理 |
|---|---|---|
| 渲染中途 OOM / 进程被杀 | 并发 × Chrome 内存超出物理内存 | 降 `--concurrency`(先减半),或 `--scale=0.5` |
| `Target closed` / Chrome 崩溃 | 渲染后端或 headless shell 异常 | 试 `--gl=angle`;`npx remotion browser ensure` 重装 |
| 渲染卡住直到超时 | `delayRender` 没有对应 `continueRender` | 给每个 delayRender 加 label,看超时报的是哪个;检查 catch 分支是否漏了释放 |
| 字体变成 fallback | 字体未加载完就截帧 | 用 `loadFont()` + `waitUntilDone()`,见「字体加载」 |
| 视频素材卡顿/花屏 | 用了 `<Video>` 处理长素材 | 改用 `<OffthreadVideo>` |
| `ENOSPC` / 磁盘写满 | 帧序列临时文件占满磁盘 | 清理临时目录;确保剩余空间 > 输出体积 × 3 |
| 每次渲染结果不同 | 用了 `Math.random()` / `Date.now()` / `useEffect` 副作用 | 改为由 `useCurrentFrame()` 或 props 派生 |
| `X is not exported from 'remotion'` | 安装的 major 版本与文档不符 | 锁 `remotion@^4.0`,见「版本基线」 |
| 音频不同步 | fps 与音频采样处理不匹配 | 检查 Composition 的 `fps` 与源素材一致 |

**长渲染前的 5 项预检**(或直接跑 `python3 scripts/wrapper.py preflight`):

- [ ] `node --version` ≥ 18
- [ ] 磁盘剩余 > 预估输出体积 × 3
- [ ] 已用 `--frames=0-0` 试渲一帧确认字体/素材正常
- [ ] 并发数已按内存设置
- [ ] 长片已决定分段或走 Lambda

## 💡 最佳实践 (Best Practices)

### ✅ Do

- **组件化设计** - 将场景拆分为可复用组件
- **使用 TypeScript** - 类型安全减少运行时错误
- **预加载资源** - `delayRender` + `continueRender` 配对,见上文
- **使用 `staticFile`** - 引用 public 目录中的资源
- **测试关键帧** - 在 Studio 中逐帧检查动画
- **先渲一帧再渲全片** - `--frames=0-0` 花 5 秒,能省几小时

### ❌ Don't

- **避免随机值** - 随机值导致每帧结果不一致;需要随机感用 `random(seed)` 或由帧号派生
- **避免 `useEffect` 副作用** - 可能导致渲染不确定
- **避免大量 DOM 节点** - 影响渲染性能
- **避免同步获取数据** - 使用 `delayRender` 异步加载
- **不要忘记 `continueRender`** - 这是卡住渲染的第一原因
- **长素材不要用 `<Video>`** - 用 `<OffthreadVideo>`

## 📚 进阶资源

- 官方文档: https://www.remotion.dev/docs
- API 参考: https://www.remotion.dev/api
- 示例展示: https://remotion.dev/showcase
- GitHub: https://github.com/remotion-dev/remotion
- Discord: https://remotion.dev/discord

## 📖 本 skill 的示例

| 示例 | 演示什么 |
|---|---|
| [data-driven-batch](examples/data-driven-batch/README.md) | CSV → N 条个性化 MP4;schema 校验、断点续跑、批量渲染实测数据 |
| [social-cutdown](examples/social-cutdown/README.md) | 一份组件输出 16:9 / 9:16 / 3:4 三种画幅;响应式布局、转场、安全区 |

两个示例都含**实测耗时/内存/体积**与踩坑记录。

## 🔧 与其他 Skill 配合

- **gemini-image-optimizer** - 优化视频中使用的图片素材
- **prompt-engineer** - 生成视频脚本和创意文案
- **video-frame-extractor** - 从现有视频提取帧作为素材
- **image-to-video** - 单图转视频片段
- **slack-gif-creator** - 短 GIF 输出辅助

### 与 hyperframes 的边界

`external/hyperframes` 自称视频创作的默认入口。两者分工:

| 选 Remotion | 选 hyperframes |
|---|---|
| 用户明确点名 Remotion / React / 程序化视频 | HTML 优先的一次性合成 |
| 需要类型化 React 组件复用 | 不需要构建工程 |
| 数据驱动批量出片 | 单条快速产出 |
| 需要 Lambda 规模化渲染 | 本地一次性渲染 |

冲突时以**用户是否点名框架**为先;都没点名且需求是批量/组件化 → Remotion。

## 📜 历史与合并

本 skill 由以下来源合并而成 (2026-04-21):

| 原 skill | 贡献 |
|---|---|
| `community/remotion-video/` (name: "Remotion Video Creator") | 中文教程、API 速查、动画/时间线/效果模板、最佳实践 |
| `community/remotion/` (auto-scaffolded) | 扩展元数据 (`github_url`/`github_hash`)、license 警告、wrapper.py |
| `remotion-dev/remotion` 上游 README | 项目定位、Lambda、Discord 等链接 |

合并后:`community/remotion-video/` 已删除,统一为 `community/remotion/`。

## Update policy

`github_hash` 已锁定到 `e135efdb`,npm 版本基线 `remotion_version: ^4.0`。

刷新流程:

1. 重新运行 `github-to-skills`,bump `github_hash` + `version`
2. **验证 API 示例仍能编译** — 至少跑通 `examples/social-cutdown` 的一帧渲染
3. 若上游发布了新 major,更新 `remotion_version` 并检查所有代码块
4. 更新 frontmatter 的 `last_verified: <日期>`

> 只 bump hash 不验证示例 = 文档腐烂不可见。第 2 步不可省。

## 变更记录

### v2.1.0 (2026-08-30)

经 AB 双轴 review 后修复:

- `scripts/wrapper.py` 从 10 行占位 stub 改为**可运行**的 CLI 薄封装(preflight/init/studio/render),并修正 SKILL.md 里对应的命令示例
- 新增 `remotion_version: ^4.0` + `last_verified` 版本基线,补 major 不匹配的排查指引
- 新增「⏳ 异步资源加载」:`delayRender` 必须配对 `continueRender`,失败路径用 `cancelRender`
- 新增「🔤 字体加载」:`loadFont()` + `waitUntilDone()`,解决渲出 fallback 字体
- 新增「🚨 故障排查」9 类症状 → 根因 → 处理,含 OOM / Chrome crash / ENOSPC
- 新增「性能参数」表与内存估算公式;长视频分段与 Lambda 决策规则
- 新增「🚫 何时不该用」:剪辑/抽帧/GIF/NLE 场景转交 ffmpeg 等
- 新增 `<TransitionSeries>` 转场与 `Easing` 章节(原先所有 interpolate 都是线性)
- GIF 渲染补齐 `--codec=gif --every-nth-frame --fps`
- 新增 2 个 examples(此前为 0,不符 S-Tier)
- 补 `license-restricted` tag 与 description 中的 NOT-FOR,使约束在路由阶段可见

