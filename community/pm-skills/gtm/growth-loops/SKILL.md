---
name: growth-loops
description: "Identify growth loops (flywheels) for sustainable traction. Evaluates 5 loop types: Viral, Usage, Collaboration, User-Generated, and Referral. Use when designing growth mechanisms, building product-led traction, or understanding how growth loops work."
version: 1.0.0
tags: ['pm', 'gtm', 'growth']
---
# Growth Loops

## Overview
Identify and design growth loops (flywheels) that create sustainable traction. This skill evaluates five proven growth loop mechanisms to reduce reliance on paid acquisition and build product-led growth.

## When to Use
- Designing growth mechanisms for a product
- Building sustainable viral or referral traction
- Reducing reliance on paid acquisition
- Analyzing competitor growth strategies
- Optimizing product for product-led growth

## The 5 Growth Loop Types

### 1. Viral Loop
Product content created by users gets shared on external platforms, bringing new users back to the product.
- **Mechanism**: Users create content in-product → Share on social/external platforms → New users discover and signup
- **Example**: Figma designs shared as links, Loom videos shared in emails
- **Strength**: Exponential user acquisition if content is inherently shareable
- **Challenge**: Requires highly shareable output and strong incentive to share

### 2. Usage Loop
Users create content or value within the product, then share it, which invites new users or drives re-engagement.
- **Mechanism**: User creates → Shares creation → Others consume → Become engaged users
- **Example**: Twitter threads, Medium articles, Notion templates shared publicly
- **Strength**: Growth tied directly to product usage and network effects
- **Challenge**: Requires content creation friction to be very low

### 3. Collaboration Loop
Users invite colleagues to co-create or collaborate within the product, expanding the user base within organizations.
- **Mechanism**: User creates → Invites colleagues for collaboration → Colleagues discover product value
- **Example**: Google Docs invitations, Figma team projects, Slack channels
- **Strength**: Deep organizational penetration and high retention
- **Challenge**: Works best for collaborative/team-based products

### 4. User-Generated Loop
Users discover new content or features through other users' creations, then create and share their own content.
- **Mechanism**: User discovers content → Creates similar content → Shares creation → Others discover
- **Example**: TikTok, Pinterest, YouTube trends driving creator participation
- **Strength**: Creates content flywheel and network effects
- **Challenge**: Requires critical mass of quality content to sustain

### 5. Referral Loop
Users invite other potential users in exchange for rewards, incentives, or social recognition.
- **Mechanism**: User refers → Referred user joins → Referrer gets reward → Shares more referrals
- **Example**: Dropbox referral bonus, Uber rider referrals, PayPal signup bonuses
- **Strength**: Directly incentivizes acquisition; easy to measure ROI
- **Challenge**: Requires valuable incentive without eroding unit economics

## How It Works

### Step 1: Define Product Value
Clarify the core value users experience:
- Primary action users take in your product
- Value created per user action
- Network effects present (if any)
- Friction points in the experience

### Step 2: Evaluate Loop Fit
Assess which growth loops align with your product:
- Product type (collaborative, content-based, utility, etc.)
- Target user behavior and sharing habits
- Network effects already present
- Existing user base and engagement

### Step 3: Design Loop Mechanics
Create specific loop implementation:
- Trigger that initiates sharing or invitations
- Incentive for participation (intrinsic or extrinsic)
- Ease of sharing mechanism
- Conversion rate from invite to activation
- Frequency of loop repetition per user

### Step 4: Calculate Loop Coefficient

> ⚠️ **Loop Coefficient 必须给出可验证公式**，而不是变量列表。

**简化 K-factor（viral loop）：**

```
K = invites_per_user × conversion_rate

K > 1   → 自我增长（viral coefficient > 1, exponential）
K = 1   → 维持（self-sustaining）
K < 1   → 不可持续（需付费 / 内容补量）
```

**完整 K-factor 漏斗（referral loop）：**

```
K = (invites_sent_per_user)
  × P(signup | invite)
  × P(activation | signup)
  × P(retention_30d | activation)
```

每一步必须基于真实数据（not assumptions）；任何 P 缺失时按 `[unverified]` 标注，禁止按"行业惯例"伪造。

**Unit Economics (referral loop)：**

| 指标 | 公式 | 健康阈值 |
|---|---|---|
| 邀请 CAC | `reward_per_invite × invites_per_acquisition / conversion` | < blended CAC × 0.7 |
| Payback | `CAC_referral / (LTV × gross_margin)` | < 12 月 |
| 套利风险 | `fake_account_detection_rate / reward_loss_rate` | < 5% |

K-factor 健康但 unit economics 不健康 → loop 不可持续。

### Step 5: Build the Loop
Implement the highest-leverage loop first:
- Start with the most natural loop for your product
- Optimize messaging and friction
- Measure loop metrics and conversion rates
- Compound results over time

## ⚖️ 合规与失败模式（必读）

> 增长 loop 设计与实施前，**必须评估**以下风险与合规边界：

### Dark Pattern 反模式

- **多账号套利**：用户用虚假身份 / 临时邮箱 / 虚拟号码刷推荐奖励。**必须**设计 eligibility verification（如设备指纹、手机号绑定、KYC）才能上 referral 奖励。
- **邀请已注册用户**：奖励结构设计不当会让用户邀请已注册的"熟人"刷奖励，**而非真正获客**。设置 first-time-only 奖励 + fraud detection。
- **高额不可持续奖励**：Dropbox/Uber 早期靠 VC 补贴高额 referral bonus，但 unit economics 在补贴退坡后会崩溃。奖励金额必须 < CAC × 0.7。
- **隐私边界**："邀请好友"功能若读取通讯录 / 社交图谱，需要明确 consent（PIPL / GDPR / CCPA）。未取得同意不得上传通讯录。
- **虚假社会证明**："已有 1,000,000 用户"等声明必须有可验证来源；占位符与未经验证数字禁止用于宣传。

### 平台 ToS 合规

- **Apple App Store / Google Play**：禁止虚拟货币 / 真实货币 referral 奖励用于购买 IAP 内容（影响分成）；具体见 Apple Guideline 4.0 / Google Play Developer Policy。
- **微信 / 微博 / 抖音 / X 等社交平台**：UGC 跨平台分发受平台 ToS 限制（Spam / 诱导分享 / 内容农场），违规可封号。
- **金融 / 医疗 / 教育 / 博彩类**：referral 奖励属于营销活动，需符合当地金融营销规则（如中国《广告法》、美国 FTC Endorsement Guides、EU UCPD）。
- **数据收集合规**：跨平台追踪 / 跨设备指纹需明确 consent 与 opt-out；PIPL 跨境传输需单独评估。

### 因果推断边界

- 增长归因时区分"内容驱动"vs"平台算法驱动"vs"运气"vs"循环驱动"。同一段时间内多 loop 同时运转会 confounding。
- 推荐 A/B 测试用 cohort + 时间窗口 + 控制组同步变化；避免"saving the date"型偏倚。
- 任何"我的增长由 loop X 驱动"结论必须有 holdout / counterfactual 验证，而不是单一时间序列对比。

## Input Format
Use $ARGUMENTS to pass:
- Product description and primary user action
- Target user demographics and behavior
- Existing sharing/collaboration features
- Current growth channels and metrics
- Constraints or opportunities

## Output
A growth loops analysis including:
- Ranked evaluation of all 5 loop types for your product
- Recommended primary growth loop with implementation plan
- Secondary loops to layer over time
- Key metrics and measurement framework
- 30-60-90 day implementation roadmap
- Potential loop coefficient and growth projections

## Framework
Based on growth loops research by Ognjen Bošković. Focuses on compounding user acquisition through built-in, product-native sharing and collaboration mechanisms.

## Tips
- Start with one loop and master it before adding complexity
- Viral loops compound fastest but take time to build
- Collaboration loops create strongest retention and LTV
- Measure loop health weekly during optimization phase
- Combine loops for multiplicative effect once operating at scale

---

### Further Reading

- [Product-Led Growth 101, Part 1/2](https://www.productcompass.pm/p/product-led-growth-101-12)
- [OpenAI’s Product Leader Shares 3-Layer Distribution Framework To Win Mind & Market Share in the AI World](https://www.productcompass.pm/p/distribution-framework-ai-products)
- [How to Design a Value Proposition Customers Can't Resist?](https://www.productcompass.pm/p/how-to-design-value-proposition-template)
