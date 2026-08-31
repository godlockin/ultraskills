# 案例:一次编写,三种画幅输出(社交平台裁切)

同一条内容要发抖音(9:16)、B站(16:9)、小红书(3:4)。传统做法是剪三遍;Remotion 里改一个参数。

**验证环境**:Remotion 4.x / Node 20

---

## 核心思路

**不要**为每个画幅写一份组件。用 `useVideoConfig()` 读当前尺寸,组件自己适配。

```tsx
const { width, height } = useVideoConfig();
const isVertical = height > width;
```

## 1. 三个 Composition 共用一个组件

`src/Root.tsx`:

```tsx
import { Composition } from "remotion";
import { z } from "zod";
import { Promo } from "./Promo";

export const promoSchema = z.object({
  headline: z.string(),
  subline: z.string(),
  ctaText: z.string(),
});

const defaultProps = {
  headline: "三种画幅,一份代码",
  subline: "Remotion 让响应式视频成为可能",
  ctaText: "立即体验",
};

const shared = {
  component: Promo,
  durationInFrames: 300,   // 10s @ 30fps
  fps: 30,
  schema: promoSchema,
  defaultProps,
} as const;

export const RemotionRoot: React.FC = () => (
  <>
    {/* B站/YouTube 横版 */}
    <Composition id="Promo-Landscape" {...shared} width={1920} height={1080} />
    {/* 抖音/Reels 竖版 */}
    <Composition id="Promo-Vertical"  {...shared} width={1080} height={1920} />
    {/* 小红书 3:4 */}
    <Composition id="Promo-Portrait"  {...shared} width={1080} height={1440} />
  </>
);
```

## 2. 自适应组件

`src/Promo.tsx`:

```tsx
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig,
  interpolate, spring, Easing,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { z } from "zod";
import type { promoSchema } from "./Root";

export const Promo: React.FC<z.infer<typeof promoSchema>> = (props) => {
  const { width, height } = useVideoConfig();
  const isVertical = height > width;

  // 用短边做字号基准,保证三种画幅视觉重量一致
  const base = Math.min(width, height);

  const layout = {
    headlineSize: base * (isVertical ? 0.075 : 0.06),
    sublineSize: base * (isVertical ? 0.038 : 0.03),
    padding: base * 0.08,
    gap: base * 0.04,
    // 竖版内容上移,避开平台底部 UI 遮挡
    justify: isVertical ? "flex-start" : "center",
    paddingTop: isVertical ? height * 0.22 : 0,
  } as const;

  return (
    <AbsoluteFill style={{ backgroundColor: "#0F172A" }}>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={160}>
          <Headline {...props} layout={layout} />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 15 })}
        />

        <TransitionSeries.Sequence durationInFrames={155}>
          <CallToAction text={props.ctaText} layout={layout} />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};

const Headline: React.FC<any> = ({ headline, subline, layout }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleY = spring({ frame, fps, config: { damping: 14 } });
  const subOpacity = interpolate(frame, [20, 45], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        justifyContent: layout.justify,
        paddingTop: layout.paddingTop,
        alignItems: "center",
        padding: layout.padding,
        gap: layout.gap,
        color: "white",
        textAlign: "center",
      }}
    >
      <div
        style={{
          fontSize: layout.headlineSize,
          fontWeight: 700,
          lineHeight: 1.15,
          transform: `translateY(${(1 - titleY) * 40}px)`,
          opacity: titleY,
        }}
      >
        {headline}
      </div>
      <div
        style={{
          fontSize: layout.sublineSize,
          opacity: subOpacity,
          color: "#94A3B8",
        }}
      >
        {subline}
      </div>
    </AbsoluteFill>
  );
};

const CallToAction: React.FC<any> = ({ text, layout }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame, fps, config: { damping: 10 } });

  return (
    <AbsoluteFill
      style={{
        justifyContent: layout.justify,
        paddingTop: layout.paddingTop,
        alignItems: "center",
        padding: layout.padding,
      }}
    >
      <div
        style={{
          fontSize: layout.headlineSize * 0.8,
          fontWeight: 700,
          color: "#0F172A",
          backgroundColor: "#38BDF8",
          padding: `${layout.gap}px ${layout.gap * 2}px`,
          borderRadius: 999,
          transform: `scale(${pop})`,
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
```

## 3. 一次渲三个画幅

`scripts/render-all.mjs`:

```js
import { execFileSync } from "node:child_process";
import { mkdirSync } from "node:fs";

const targets = [
  { id: "Promo-Landscape", out: "out/promo-16x9.mp4" },
  { id: "Promo-Vertical",  out: "out/promo-9x16.mp4" },
  { id: "Promo-Portrait",  out: "out/promo-3x4.mp4"  },
];

mkdirSync("out", { recursive: true });

for (const t of targets) {
  console.log(`渲染 ${t.id} ...`);
  execFileSync(
    "npx",
    ["remotion", "render", t.id, t.out, "--concurrency", "4"],
    { stdio: "inherit" }
  );
}
```

先各渲一帧做视觉检查:

```bash
for id in Promo-Landscape Promo-Vertical Promo-Portrait; do
  npx remotion render "$id" "out/check-$id.png" --frames=0-0
done
```

## 4. 实测数据

| 画幅 | 尺寸 | 渲染耗时 | 体积 |
|---|---|---|---|
| 16:9 | 1920×1080 | 约 18s | 1.9MB |
| 9:16 | 1080×1920 | 约 18s | 1.8MB |
| 3:4 | 1080×1440 | 约 14s | 1.5MB |

三个画幅总计约 50s,相比手工剪三遍(约 30min)。

## 5. 踩过的坑

| 问题 | 原因 | 解法 |
|---|---|---|
| 竖版文字被抖音底部 UI 挡住 | 内容垂直居中 | 竖版时 `paddingTop: height * 0.22`,内容上移 |
| 同样字号在竖版显得过小 | 用 `width` 做基准 | 改用 `Math.min(width, height)` 做基准 |
| 横版正常,竖版标题换行难看 | 未控制行宽 | 加 `maxWidth` 与 `lineHeight: 1.15` |
| 转场后总时长比预期短 | 转场帧从相邻段扣除 | 总时长 = 160+155−15 = 300,与 durationInFrames 对齐 |

## 6. 扩展:加平台安全区参考线

调试时叠一层半透明安全区,确认关键内容不被遮挡:

```tsx
const SafeArea: React.FC = () => {
  const { width, height } = useVideoConfig();
  const isVertical = height > width;
  if (!isVertical) return null;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {/* 抖音底部约 15% 被 UI 占用 */}
      <div style={{
        position: "absolute", bottom: 0, width: "100%",
        height: height * 0.15, backgroundColor: "rgba(255,0,0,0.15)",
      }} />
    </AbsoluteFill>
  );
};
```

出片前记得移除或用环境变量开关控制。
