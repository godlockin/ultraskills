---
name: image-analyzer
description: 图片分析技能 - 提取人物性别/年龄/面部特征/发型/穿着等多维度信息
version: 1.0.0
tags: [image, analysis, face, feature-extraction]
---

# ImageAnalyzer Skill

## 描述
图片分析技能 - 提取人物的多维度特征信息

## 触发条件
图片审核通过后，Prompt生成前

## 功能
分析并提取以下人物特征：
- **基本信息**: 性别、年龄（大致范围）
- **面部特征**: 表情、眼睛大小、脸型
- **发型特征**: 发色、发型、长度
- **穿着特征**: 服装类型、颜色、风格
- **皮肤问题**: 痘痘、皱纹、黑眼圈等（用于美颜参考）
- **特殊标记**: 眼镜、胡须、痣、酒窝等

## 使用方法
```typescript
import { ImageAnalyzer } from './ImageAnalyzer';

const analyzer = new ImageAnalyzer(geminiClient);
const analysis = await analyzer.analyze(imagePart);
// 返回: "女性，大约30岁，长发，戴眼镜，微笑，穿着休闲..."
```

## 输出格式
返回简洁的文本描述，包含所有可识别的特征，用于后续：
1. Prompt生成
2. 美颜策略选择
3. 祝福语个性化

## 注意事项
- 描述应简洁但信息完整
- 包含年龄、性别等关键信息用于美颜
- 记录特殊特征以保持可识别性
