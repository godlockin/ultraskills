---
name: face-beautification
description: 端到端AI新年祝福照片生成系统，含美颜策略（年龄/性别/肤色维度）、Prompt生成、质量审核
version: 1.0.0
tags: [image, face, beauty, photo, new-year, ai]
---

# 新年祝福图片生成器 - 技能体系

## 项目能力概览

本项目是一个基于 AI 的端到端新年祝福照片生成系统，包含以下核心能力：

### 1. 图片审核技能 (ImageAuditor)
**文件**: `src/lib/ImageAuditor.ts`
**功能**: 
- 审核上传图片是否包含清晰人物
- 确保内容适合生成新年祝福照片
- 输出 PASS/FAIL 判定

### 2. 特征分析技能 (ImageAnalyzer)
**文件**: `src/lib/ImageAnalyzer.ts`
**功能**:
- 分析人物性别、年龄、表情
- 识别发型、衣着特征
- 输出结构化特征描述

### 3. Prompt生成技能 (PromptGenerator)
**文件**: `src/lib/PromptGenerator.ts`
**功能**:
- 根据特征生成AI绘图Prompt
- 集成美颜策略
- 生成英文专业Prompt

### 4. 图片质量审核技能 (ImageReviewer)
**文件**: `src/lib/ImageReviewer.ts`
**功能**:
- 审核生成结果是否符合主题
- 检查畸变和质量问题
- 确保最终输出质量

### 5. 祝福语文案技能 (BlessingStyles)
**文件**: `src/constants/blessingStyles.ts`
**功能**:
- 提供5种风格祝福语：传统、幽默、诗意、现代、温馨
- 根据人物特征定制文案
- 支持风格切换

### 6. 智能美颜技能 (FaceBeautifier)
**文件**: `src/lib/Beautifier.ts`
**功能**:
- 多维度美颜策略（见下方详细说明）
- 年龄/性别/肤色/面部特征智能识别
- 自然美颜，保持可识别性

---

## 智能美颜技能详细设计

### 美颜维度

#### 1. 年龄维度 (Age-based)
```typescript
interface AgeStrategy {
  group: 'child' | 'teenager' | 'young_adult' | 'adult' | 'middle_aged' | 'elderly';
  range: [number, number];
  focus: string[];
  intensity: number; // 0-1
}
```

| 年龄段 | 范围 | 美颜重点 | 强度 |
|--------|------|----------|------|
| 儿童 | 0-12 | 保持天真，柔光，健康肤色 | 0.3 |
| 青少年 | 13-19 | 青春活力，祛痘，提亮 | 0.4 |
| 青年 | 20-35 | 大眼瘦脸，去细纹，气色 | 0.7 |
| 中年 | 36-59 | 去皱纹，紧致，减龄 | 0.8 |
| 老年 | 60+ | 温和除皱，保留尊严，健康气色 | 0.5 |

#### 2. 性别维度 (Gender-based)
```typescript
interface GenderStrategy {
  gender: 'male' | 'female' | 'unknown';
  features: {
    eyes: string;
    face: string;
    skin: string;
    makeup: string;
  };
}
```

**女性策略**:
- 眼睛: 放大有神，自然眼妆
- 脸型: 瓜子脸/V脸，柔和轮廓
- 皮肤: 磨皮美白，去瑕疵
- 妆容: 淡妆提亮，好气色

**男性策略**:
- 眼睛: 明亮有神，去疲态
- 脸型: 轮廓分明，适度瘦脸
- 皮肤: 去油光皱纹，健康肤色
- 妆容: 自然无妆感，阳刚气质

#### 3. 肤色维度 (SkinTone-based)
```typescript
type SkinTone = 'fair' | 'light' | 'medium' | 'olive' | 'tan' | 'dark';

interface SkinToneStrategy {
  tone: SkinTone;
  enhancement: string[];
  colorCorrection: string[];
}
```

| 肤色 | 优化策略 |
|------|----------|
| 白皙 | 增加血色，避免苍白，提升光泽 |
| 偏白 | 均匀肤色，提亮，自然红润 |
| 中等 | 提亮一个色阶，增加光泽感 |
| 橄榄 | 去黄提亮，均匀肤色 |
| 偏黄 | 提亮美白，去除暗沉 |
| 深色 | 提亮光泽，均匀肤色，保持自然 |

#### 4. 面部特征维度 (FacialFeatures)
```typescript
interface FacialFeatures {
  faceShape: 'oval' | 'round' | 'square' | 'heart' | 'long' | 'diamond';
  eyeSize: 'small' | 'medium' | 'large';
  skinIssues: ('acne' | 'wrinkles' | 'spots' | 'dark_circles' | 'pores')[];
  specialFeatures: string[]; // 痣、酒窝、眼镜等
}
```

**脸型优化**:
- 圆脸 → 微V脸，拉长线条
- 方脸 → 柔和轮廓，减少棱角
- 长脸 → 缩短中庭，增加宽度感
- 心形脸 → 平衡额头下巴比例

**眼部问题**:
- 小眼 → 放大1.2-1.5倍，有神
- 眼袋/黑眼圈 → 消除疲态
- 细纹 → 平滑眼周

**皮肤问题**:
- 痘痘/痘印 → 磨皮去除
- 皱纹 → 根据年龄适度减少
- 色斑 → 均匀肤色
- 毛孔 → 细腻肤质

---

## 美颜Prompt模板

### 通用美颜基础
```
Professional photo retouching with the following enhancements:
- Maintain original identity and recognizable features
- Natural-looking improvements without over-processing
- High-definition skin texture preservation
```

### 分年龄段模板

#### 儿童 (0-12岁)
```
Gentle enhancements for child:
- Soft natural lighting, rosy healthy cheeks
- Clear bright eyes full of innocence
- Smooth baby-soft skin texture
- Keep adorable childlike appearance
- Maintain all natural features
```

#### 青少年 (13-19岁)
```
Youth enhancement:
- Bright clear eyes with natural spark
- Smooth skin reducing acne/blemishes
- Fresh and energetic appearance
- Natural healthy glow
- Preserve youthful characteristics
```

#### 青年 (20-35岁)
```
Beauty enhancement:
- Big bright eyes with natural makeup effect
- Slim V-shaped face, refined jawline
- Smooth flawless skin, minimize fine lines
- Rosy healthy complexion
- Well-proportioned facial features
- Camera-ready polished look
```

#### 中年 (36-59岁)
```
Age-defying enhancement:
- Lifted eye area, reduce wrinkles
- Slimmer face contour, reduce sagging
- Smooth skin minimizing age spots and deep lines
- Youthful radiant glow
- Refreshed energetic appearance
- Maintain wisdom and maturity
```

#### 老年 (60岁+)
```
Dignified enhancement:
- Gentle softening of deep wrinkles
- Natural healthy color restoration
- Subtle face lift maintaining character
- Dignified graceful appearance
- Warm approachable expression
- Keep natural age marks with elegance
```

### 分性别调整

#### 女性附加
```
Feminine touches:
- Soft and delicate features
- Natural makeup look
- Elegant and graceful appearance
```

#### 男性附加
```
Masculine refinement:
- Defined jawline and features
- Strong but approachable look
- No makeup appearance
- Keep masculine characteristics
```

---

## 使用方式

在 `process-image.ts` 的 Prompt 生成步骤中：

```typescript
import { beautify, detectAgeGroup, detectGender, detectSkinTone, analyzeFacialFeatures } from './Beautifier';

// 分析阶段获取详细信息
const analysis = await analyzeImage(image);
const ageGroup = detectAgeGroup(analysis);
const gender = detectGender(analysis);
const skinTone = detectSkinTone(analysis);
const features = analyzeFacialFeatures(analysis);

// 生成美颜增强的prompt
const beautifyPrompt = generateComprehensiveBeautifyPrompt({
  ageGroup,
  gender,
  skinTone,
  features,
  originalAnalysis: analysis
});
```

---

## 质量保证

1. **可识别性**: 始终保留关键识别特征（痣、疤痕、眼镜等）
2. **自然度**: 避免过度美颜，保持真实感
3. **适度性**: 根据年龄调整强度，尊重每个年龄段的美
4. **一致性**: 批量处理时保持风格统一
