---
name: image-reviewer
description: 图片质量审核技能 - 审核AI生成的图片是否符合主题、无畸变、质量达标
version: 1.0.0
tags: [image, review, quality, ai-generated]
---

# ImageReviewer Skill

## 描述
图片质量审核技能 - 确保AI生成的祝福照片质量合格

## 触发条件
AI生成图片后，返回给用户前

## 功能
1. 检查是否符合"中国新年祝福"主题
2. 识别人物畸变、扭曲等问题
3. 检查画面质量（模糊、噪点等）
4. 验证背景元素是否恰当

## 使用方法
```typescript
import { ImageReviewer } from './ImageReviewer';

const reviewer = new ImageReviewer(geminiClient);
const isGoodQuality = await reviewer.review(generatedImageBase64);
```

## 审核标准
- **通过**: 符合新年主题，无明显畸变，质量可接受
- **警告**: 小问题但可接受（记录日志）
- **失败**: 严重畸变或质量问题（考虑重试）

## 策略
当前采用宽松策略，允许小问题但记录警告，确保用户体验流畅。
