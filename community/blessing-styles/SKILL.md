# BlessingStyles Skill

## 描述
祝福语文案技能 - 生成多种风格的个性化新年祝福语

## 触发条件
用户选择风格后，结合人物特征生成

## 支持风格

### 1. 传统祝福 (traditional)
- 使用经典春节吉祥话
- 喜庆庄重的语气
- 适合传统文化元素背景
- 示例: "新年快乐，万事如意！"

### 2. 幽默搞笑 (humorous)
- 轻松幽默的段子风格
- 带梗但不过界
- 现代活泼的画面
- 示例: "新年不胖，算我输！"

### 3. 诗意古风 (poetic)
- 古诗词韵律和意境
- 文雅有文化底蕴
- 古典水墨画面
- 示例: "岁岁常欢愉，年年皆胜意！"

### 4. 现代简约 (modern)
- 简洁有力的表达
- 符合年轻人表达习惯
- 适合社交媒体
- 示例: "继续热爱，继续发光！"

### 5. 温馨祝福 (blessing)
- 真诚温暖有情感
- 表达关爱
- 温馨柔和画面
- 示例: "愿所有美好都如期而至！"

## 使用方法
```typescript
import { blessingStyles, getStyleById } from './blessingStyles';

const style = getStyleById('humorous');
const systemPrompt = style.systemPrompt;
```

## 个性化
根据人物特征（年龄、性别、表情）调整语气：
- 儿童: 可爱亲切
- 老人: 尊敬祝福
- 年轻人: 活泼有趣
