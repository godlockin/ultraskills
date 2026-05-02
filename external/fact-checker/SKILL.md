---
name: fact-checker
description: |
  系统性事实核查与内容风险评估。识别逻辑谬误、评估信息可信度、标注证据等级、量化内容风险。
  当用户提到"事实核查"、"逻辑谬误"、"验证声明"、"CRAAP测试"、"内容风险"时使用。
version: 1.0.0
tags: [external, journalism, critical-thinking]
source: video_intelligent_analyzer/src/skills/critic
---

# Fact Checker — 系统性内容验证框架

## 核心能力

- CRAAP 信息可信度测试（5维度量化评分）
- 13类逻辑谬误识别与分类
- 5级证据等级评估
- 4级风险分级与处理建议

---

## 1. CRAAP Test (信息可信度评估)

对每个关键声明进行 5 维度评估，每项 1-5 分：

| 维度 | 评分标准 |
|------|----------|
| **Currency (时效性)** | 5=最近6个月，4=1年内，3=2-3年，2=3-5年，1=>5年或未知 |
| **Relevance (相关性)** | 5=直接相关且充分，4=相关，3=部分相关，2=边缘相关，1=不相关 |
| **Authority (权威性)** | 5=领域权威专家/期刊，4=专业人士，3=有经验人士，2=普通来源，1=匿名/不可靠 |
| **Accuracy (准确性)** | 5=有数据支持且可验证，4=有引用但需核实，3=合理但无数据，2=存疑，1=明显错误 |
| **Purpose (目的性)** | 5=中立客观，4=轻微倾向，3=有明显立场，2=宣传性质，1=恶意误导 |

**综合判定**:
- **20-25 分**: 高可信度 (High Credibility)
- **15-19 分**: 中等可信度 (Medium Credibility)
- **<15 分**: 低可信度 (Low Credibility)

---

## 2. Logical Fallacies Taxonomy (逻辑谬误分类)

### 形式谬误 (Formal Fallacies)

| 谬误名称 | 定义 | 案例 |
|----------|------|------|
| **Ad Hominem (人身攻击)** | 攻击人而非论点 | "他是骗子，所以他的观点不对" |
| **Straw Man (稻草人)** | 曲解对方论点后攻击 | "你说要减少军费，你就是不爱国" |
| **False Cause (虚假因果)** | 将相关性误认为因果 | "冰淇淋销量和溺水率正相关，所以冰淇淋导致溺水" |
| **Appeal to Authority (诉诸权威)** | 仅因权威身份认定正确 | "诺贝尔奖得主说的，肯定对" |
| **Bandwagon (从众谬误)** | 因为多数人就对 | "大家都在买，所以是好的" |

### 非形式谬误 (Informal Fallacies)

| 谬误名称 | 定义 | 案例 |
|----------|------|------|
| **Hasty Generalization (轻率概括)** | 样本不足就下结论 | "我认识的几个人都这样，所以都这样" |
| **False Dilemma (虚假两难)** | 只给两个极端选项 | "要么支持我，要么就是敌人" |
| **Slippery Slope (滑坡谬误)** | 夸大因果链条 | "今天允许 A，明天就会 Z" |
| **Appeal to Emotion (诉诸情感)** | 用情感替代理性 | "想想可怜的孩子，所以政策必须通过" |
| **Cherry Picking (选择性引证)** | 只选支持自己的证据 | 只引用支持自己观点的研究 |

### 统计谬误 (Statistical Fallacies)

| 谬误名称 | 定义 | 案例 |
|----------|------|------|
| **Gambler's Fallacy (赌徒谬误)** | 认为独立事件有关联 | "连续5次正面，下次肯定是反面" |
| **Survivorship Bias (幸存者偏差)** | 只看成功者忽略失败者 | "成功者都早起，所以早起导致成功" |
| **Regression to Mean (回归均值)** | 将自然波动归因于干预 | "训练后成绩提高，所以训练有效" |

---

## 3. Evidence Hierarchy (证据等级)

| 等级 | 类型 | 可信度 |
|------|------|--------|
| **Level 1** | 同行评审/Meta分析/系统综述 | 最高 |
| **Level 2** | 随机对照试验 (RCT) | 高 |
| **Level 3** | 队列研究/病例对照研究 | 中等 |
| **Level 4** | 专家意见/案例报告 | 低 |
| **Level 5** | 个人经验/传闻/个案 | 最低 |

---

## 4. Risk Classification (风险分级)

| 风险等级 | 判定标准 | 处理建议 |
|----------|----------|----------|
| **High Risk** | 含投资/医疗/法律建议且无证据；煽动性言论；明显虚假信息 | 必须添加警告，建议删除或大幅修改 |
| **Medium Risk** | 有争议但有一定依据；片面观点；统计谬误 | 需要平衡观点，添加反方论点 |
| **Low Risk** | 轻微夸大；证据不足但不危害 | 建议补充来源，可保留 |
| **Pass** | 无明显问题 | 无需处理 |

---

## Output Schema (输出格式)

```json
{
  "claims_analysis": [
    {
      "claim": "<原文声明>",
      "timestamp": "<时间戳或位置>",
      "craap_score": {
        "currency": 1-5,
        "relevance": 1-5,
        "authority": 1-5,
        "accuracy": 1-5,
        "purpose": 1-5,
        "total": 5-25
      },
      "craap_verdict": "High/Medium/Low Credibility",
      "fallacies": [
        {
          "type": "形式/非形式/统计",
          "name": "<谬误名称>",
          "explanation": "<为什么这是谬误>"
        }
      ],
      "evidence_level": "Level 1-5",
      "risk_level": "High/Medium/Low/Pass",
      "counter_argument": "<反方观点>",
      "recommendation": "<处理建议>"
    }
  ],
  "overall_risk": "High/Medium/Low/Pass",
  "summary": "<整体内容风险摘要>"
}
```

---

## 反谬误规则

在输出声明评估时：
- **Never fabricate counter-evidence** — 没有相反证据时，明确说明而非编造
- **All fallacy identifications must cite** — 标注谬误时必须引用原文中的具体表述
- **Distinguish correlation vs causation** — 任何因果声明都需要标注是否有实验设计支撑
- **Confidence tagging** — `[CONTESTED]` = 领域内有争议，`[EVOLVING]` = 最新研究可能改变结论

---

## 内容类型阈值

不同内容类型的风险容忍度不同：

| 内容类型 | 最低可接受 CRAAP 分 | 原因 |
|---------|-------------------|------|
| 医疗/健康建议 | ≥18 | 错误信息直接危害健康 |
| 金融/投资建议 | ≥18 | 错误信息导致财务损失 |
| 法律建议 | ≥17 | 错误信息导致法律后果 |
| 科学/技术 | ≥15 | 需要证据支持 |
| 娱乐/观点 | ≥10 | 低风险，主观内容可接受 |
