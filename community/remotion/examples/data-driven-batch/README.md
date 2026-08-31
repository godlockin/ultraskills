# 案例:数据驱动批量生成个性化视频

从一份 CSV 生成 N 条个性化 MP4 —— Remotion 相对传统视频工具的核心优势就在这里。

**场景**:给 200 位课程学员各生成一条 15 秒结业视频,含姓名、完成率、徽章。

**验证环境**:Remotion 4.x / Node 20

---

## 项目结构

```
data-driven-batch/
├── package.json
├── src/
│   ├── index.ts          # registerRoot
│   ├── Root.tsx          # Composition 定义 + schema
│   └── Certificate.tsx   # 视频组件
├── data/
│   └── students.csv      # 数据源
├── public/
│   └── fonts/Inter.woff2
└── scripts/
    └── batch-render.mjs  # 批量渲染驱动
```

## 1. 数据源

`data/students.csv`:

```csv
id,name,completion,badge
1,张明,100,gold
2,李婷,87,silver
3,王强,95,gold
```

## 2. Composition 定义(带 schema 校验)

`src/Root.tsx`:

```tsx
import { Composition } from "remotion";
import { z } from "zod";
import { Certificate } from "./Certificate";

// schema 让 props 有类型校验 — 批量渲染时能提前发现脏数据
export const certificateSchema = z.object({
  name: z.string().min(1),
  completion: z.number().min(0).max(100),
  badge: z.enum(["gold", "silver", "bronze"]),
});

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="Certificate"
      component={Certificate}
      durationInFrames={450}   // 15s @ 30fps
      fps={30}
      width={1920}
      height={1080}
      schema={certificateSchema}
      defaultProps={{
        name: "示例学员",
        completion: 100,
        badge: "gold" as const,
      }}
    />
  );
};
```

`src/index.ts`:

```tsx
import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";

registerRoot(RemotionRoot);
```

## 3. 视频组件

`src/Certificate.tsx`:

```tsx
import {
  AbsoluteFill, useCurrentFrame, useVideoConfig,
  interpolate, spring, Easing, Sequence,
} from "remotion";
import { loadFont } from "@remotion/google-fonts/Inter";
import { z } from "zod";
import type { certificateSchema } from "./Root";

const { fontFamily, waitUntilDone } = loadFont();
// 关键:让 Remotion 等字体加载完再截帧,否则渲出来是 fallback 字体
await waitUntilDone();

const BADGE_COLOR = {
  gold: "#F5B700",
  silver: "#9CA3AF",
  bronze: "#B45309",
} as const;

export const Certificate: React.FC<z.infer<typeof certificateSchema>> = ({
  name, completion, badge,
}) => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();

  // 标题缓出淡入 — 加 easing 与 clamp
  const titleOpacity = interpolate(frame, [0, 20], [0, 1], {
    easing: Easing.out(Easing.cubic),
    extrapolateRight: "clamp",
  });

  // 姓名弹入
  const nameScale = spring({ frame: frame - 20, fps, config: { damping: 12 } });

  // 完成率数字从 0 递增到实际值 — 由帧号派生,保证确定性
  const shownCompletion = Math.round(
    interpolate(frame, [40, 100], [0, completion], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    })
  );

  // 进度条宽度
  const barWidth = interpolate(frame, [40, 100], [0, completion / 100], {
    easing: Easing.inOut(Easing.ease),
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#0B1120", fontFamily }}>
      <AbsoluteFill
        style={{
          justifyContent: "center",
          alignItems: "center",
          gap: 40,
          color: "white",
        }}
      >
        <div style={{ fontSize: 44, opacity: titleOpacity, letterSpacing: 4 }}>
          课程结业证明
        </div>

        <div
          style={{
            fontSize: 96,
            fontWeight: 700,
            transform: `scale(${nameScale})`,
          }}
        >
          {name}
        </div>

        <Sequence from={40}>
          <div style={{ alignItems: "center", display: "flex", flexDirection: "column", gap: 16 }}>
            <div style={{ fontSize: 64, color: BADGE_COLOR[badge] }}>
              {shownCompletion}%
            </div>
            <div
              style={{
                width: width * 0.4,
                height: 12,
                borderRadius: 6,
                backgroundColor: "#1E293B",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${barWidth * 100}%`,
                  height: "100%",
                  backgroundColor: BADGE_COLOR[badge],
                }}
              />
            </div>
          </div>
        </Sequence>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

## 4. 批量渲染

`scripts/batch-render.mjs`:

```js
import { readFileSync, mkdirSync } from "node:fs";
import { execFileSync } from "node:child_process";

const rows = readFileSync("data/students.csv", "utf8")
  .trim().split("\n").slice(1)
  .map((line) => {
    const [id, name, completion, badge] = line.split(",");
    return { id, name, completion: Number(completion), badge };
  });

mkdirSync("out", { recursive: true });

// 串行渲染:每次渲染内部已经并发到多核,外层再并行会争抢内存
for (const row of rows) {
  const props = JSON.stringify({
    name: row.name,
    completion: row.completion,
    badge: row.badge,
  });
  console.log(`[${row.id}] ${row.name} ...`);
  execFileSync(
    "npx",
    [
      "remotion", "render", "Certificate", `out/cert-${row.id}.mp4`,
      "--props", props,
      "--concurrency", "4",
    ],
    { stdio: "inherit" }
  );
}
console.log(`完成 ${rows.length} 条`);
```

运行:

```bash
# 先渲一条确认没问题(字体/布局)
npx remotion render Certificate out/test.mp4 --props '{"name":"测试","completion":88,"badge":"silver"}' --frames=0-0

# 确认无误后批量
node scripts/batch-render.mjs
```

## 5. 实测数据

| 项 | 数值 |
|---|---|
| 单条时长 | 15s (450 帧 @ 30fps) |
| 单条渲染耗时 | 约 25s(1080p,`--concurrency=4`,M 系列芯片) |
| 200 条串行总耗时 | 约 85 min |
| 峰值内存 | 约 6GB(4 worker × 1.5GB) |
| 输出体积 | 单条约 2.8MB |

**若需更快**:改用 `@remotion/lambda` 云端 fan-out,200 条可压到几分钟。

## 6. 踩过的坑

| 问题 | 原因 | 解法 |
|---|---|---|
| 首次批量渲染字体全是宋体 | `waitUntilDone()` 漏了 | 加上,并先用 `--frames=0-0` 验证 |
| 第 47 条崩了,前 46 条白跑 | 脚本没有断点续跑 | 渲染前检查 `out/cert-${id}.mp4` 是否已存在则跳过 |
| 外层并行 4 个 render 反而更慢 | 内存争抢 + swap | 外层串行,靠 `--concurrency` 吃多核 |
| CSV 有空姓名导致渲出空白视频 | 没有数据校验 | 用 `schema` + zod,脏数据在渲染前就报错 |

## 7. 断点续跑补丁

```js
import { existsSync } from "node:fs";

for (const row of rows) {
  const out = `out/cert-${row.id}.mp4`;
  if (existsSync(out)) {
    console.log(`[${row.id}] 已存在,跳过`);
    continue;
  }
  // ... 渲染
}
```
