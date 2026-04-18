---
name: image-auditor
description: 图片审核技能 - 确保上传图片包含清晰人物且内容适合生成新年祝福照片
version: 1.0.0
tags: [image, audit, moderation, safety]
---

# ImageAuditor Skill

## 描述
图片审核技能 - 确保上传图片适合用于生成新年祝福照片

## 触发条件
用户上传图片后，生成祝福照片前

## 功能
1. 检测图片是否包含清晰的人物主体
2. 审核内容是否适合春节祝福场景
3. 排除不当内容（暴力、色情、政治敏感等）
4. 返回 PASS/FAIL 判定

## 使用方法
```typescript
import { ImageAuditor } from './ImageAuditor';

const auditor = new ImageAuditor(geminiClient);
const isValid = await auditor.audit(imagePart);
```

## 审核标准
- **通过条件**: 包含清晰可见的人物，内容健康正面
- **失败条件**: 无人物、人物不清晰、内容不当、多人无法识别主体

## 输出
- `true`: 审核通过
- `throw Error`: 审核失败并附带原因
