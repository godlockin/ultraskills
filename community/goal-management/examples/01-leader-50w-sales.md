# Example 01 · 主公原用例 · 下周 50 万业绩

> **主公原话**:「今天领导给我布置的工作是下周做到 50 万业绩,你给我做一个方案,用 HTML 格式生成。」

---

## 情境背景

```
主公:某 ToB SaaS 公司销售负责人
场景:老板口头布置下周业绩冲刺
原话:"下周做到 50 万业绩"
隐含信息:
  - 时间:2026-07-27 ~ 2026-07-31(7 天)
  - 量化:50 万(未说回款还是合同)
  - 范围:全产品/全团队
```

---

## HTML 完整方案

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>下周 50 万业绩冲刺方案 · 2026-07-27~07-31</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
    background: #f5f7fa;
    color: #1f2937;
    line-height: 1.6;
    padding: 24px;
  }
  .container { max-width: 1100px; margin: 0 auto; }
  h1 {
    font-size: 28px;
    color: #1e3a8a;
    border-bottom: 3px solid #3b82f6;
    padding-bottom: 12px;
    margin-bottom: 24px;
  }
  h2 {
    font-size: 20px;
    color: #1e40af;
    margin: 32px 0 12px;
    padding-left: 12px;
    border-left: 4px solid #3b82f6;
  }
  h3 { font-size: 16px; color: #374151; margin: 16px 0 8px; }
  .card {
    background: #fff;
    border-radius: 8px;
    padding: 20px;
    margin: 16px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,.08);
  }
  .meta {
    background: #eff6ff;
    border-left: 4px solid #3b82f6;
    padding: 12px 16px;
    margin: 16px 0;
    border-radius: 4px;
    font-size: 14px;
  }
  .meta b { color: #1e40af; }
  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }
  .kpi {
    background: linear-gradient(135deg, #3b82f6, #1e40af);
    color: #fff;
    padding: 16px;
    border-radius: 8px;
    text-align: center;
  }
  .kpi .num { font-size: 32px; font-weight: 700; }
  .kpi .label { font-size: 13px; opacity: 0.9; margin-top: 4px; }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0;
    background: #fff;
    border-radius: 6px;
    overflow: hidden;
  }
  th, td { padding: 10px 14px; text-align: left; border-bottom: 1px solid #e5e7eb; font-size: 14px; }
  th { background: #f3f4f6; font-weight: 600; color: #374151; }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: #f9fafb; }
  .green { background: #dcfce7; color: #166534; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
  .yellow { background: #fef3c7; color: #92400e; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
  .red { background: #fee2e2; color: #991b1b; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
  .blue { background: #dbeafe; color: #1e40af; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
  ol, ul { padding-left: 24px; margin: 8px 0; }
  li { margin: 4px 0; }
  .alert {
    background: #fef2f2;
    border-left: 4px solid #ef4444;
    padding: 12px 16px;
    margin: 16px 0;
    border-radius: 4px;
  }
  .success {
    background: #f0fdf4;
    border-left: 4px solid #22c55e;
    padding: 12px 16px;
    margin: 16px 0;
    border-radius: 4px;
  }
  .warning {
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
    padding: 12px 16px;
    margin: 16px 0;
    border-radius: 4px;
  }
  .plan-box {
    background: #fafafa;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    padding: 16px;
    margin: 12px 0;
  }
  .plan-box h4 { color: #1e40af; margin-bottom: 8px; font-size: 15px; }
  .checklist { list-style: none; padding-left: 0; }
  .checklist li { padding: 6px 0; }
  .checklist li::before {
    content: "□ ";
    color: #3b82f6;
    font-weight: 700;
    margin-right: 6px;
  }
  .timeline {
    position: relative;
    padding-left: 24px;
    border-left: 2px solid #e5e7eb;
    margin: 16px 0;
  }
  .timeline-item {
    margin: 16px 0;
    padding-left: 8px;
    position: relative;
  }
  .timeline-item::before {
    content: "";
    position: absolute;
    left: -28px;
    top: 6px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #3b82f6;
  }
  .timeline-item .date {
    color: #6b7280;
    font-size: 12px;
    font-weight: 600;
  }
  .tri-card {
    background: #fff;
    border-radius: 8px;
    padding: 16px;
    border: 1px solid #e5e7eb;
  }
  .tri-card.recommended {
    border: 2px solid #3b82f6;
    background: #eff6ff;
  }
  .tri-card h4 {
    color: #1e40af;
    margin-bottom: 8px;
  }
  .footer {
    margin-top: 32px;
    padding-top: 16px;
    border-top: 1px solid #e5e7eb;
    color: #6b7280;
    font-size: 13px;
    text-align: center;
  }
</style>
</head>
<body>
<div class="container">

<h1>📊 下周 50 万业绩冲刺方案</h1>

<div class="meta">
  <b>周期:</b> 2026-07-27 ~ 2026-07-31(周一-周五,5 个工作日)<br>
  <b>目标:</b> 销售总额 50 万(回款口径)<br>
  <b>团队:</b> 销售 5 人 + 借调 2 BD + 设计支援 1 人<br>
  <b>当前进度:</b> 0 / 50 万(尚未开始)<br>
  <b>历史峰值:</b> 35 万 / 周(2026-06 第 2 周)
</div>

<h2>一、目标 SMART 检查</h2>
<div class="card">
<table>
  <tr><th>维度</th><th>检查</th><th>状态</th></tr>
  <tr><td><b>S</b> 具体</td><td>50 万 = 新客 30 万 + 老客 20 万(已显化拆解)</td><td><span class="green">✓</span></td></tr>
  <tr><td><b>M</b> 可衡量</td><td>每日 7 万进度,周累计 50 万</td><td><span class="green">✓</span></td></tr>
  <tr><td><b>A</b> 可达成</td><td>历史峰值 35 万,挑战 = 1.43x;<br>但加上资源追加(2 BD + 5 万 SEM) → 可达成</td><td><span class="yellow">挑战</span></td></tr>
  <tr><td><b>R</b> 相关性</td><td>关联 Q3 OKR1(年目标 1500 万 = 周均 30 万)<br>本周 = 1.67x 周均,服务 Q3 冲刺节奏</td><td><span class="green">✓</span></td></tr>
  <tr><td><b>T</b> 时限</td><td>截止 2026-07-31 24:00,精确到日</td><td><span class="green">✓</span></td></tr>
</table>
</div>

<h2>二、5 Why 根因分析</h2>
<div class="card">
<p>为什么本周要 50 万?(主公追问)</p>
<ol>
  <li>因为 <b>Q3 冲刺压力大,目前月进度落后</b></li>
  <li>为什么压力大?→ <b>集团对 Q3 营收有硬指标,资本市场关注</b></li>
  <li>为什么关注?→ <b>10 月有新一轮融资计划,需要 Q3 数据</b></li>
</ol>
<p style="margin-top:12px;color:#1e40af;font-weight:600;">
  根因:本周 50 万不是孤立目标,是融资节奏需要 → <b>本周是死线,不可延期</b>
</p>
</div>

<h2>三、隐藏目标识别</h2>
<div class="card">
<table>
  <tr><th>隐藏维度</th><th>领导的真实目标</th><th>动作调整</th></tr>
  <tr><td>现金流 vs 利润</td><td><b>回款</b>(融资需要现金流)<br>合同不算</td><td>聚焦已签约未回款客户催回款</td></tr>
  <tr><td>新客 vs 老客</td><td>新客为底,老客为辅<br>新客 ≥ 60%</td><td>BD 重点拓新客,客服跟进老客</td></tr>
  <tr><td>核心产品</td><td>主力产品 X 占 70%<br>其他产品辅助</td><td>BD 主推 X 产品</td></tr>
  <tr><td>时间窗口</td><td>周三有内部投资人预沟通<br>需周三前完成 ≥ 50%</td><td>周一周二发力,周三达成 25 万</td></tr>
</table>
</div>

<h2>四、OKR + KPI 拆解</h2>
<div class="card">
<h3>O:完成下周业绩冲刺,达成回款 50 万</h3>
<table>
  <tr><th>KR</th><th>指标</th><th>基线</th><th>目标</th><th>截止</th><th>状态</th></tr>
  <tr>
    <td>KR1 新客回款</td>
    <td>新客合同回款</td>
    <td>15 万/周</td>
    <td><b>30 万</b></td>
    <td>07-31</td>
    <td><span class="blue">主攻</span></td>
  </tr>
  <tr>
    <td>KR2 老客复购</td>
    <td>老客加购回款</td>
    <td>10 万/周</td>
    <td><b>20 万</b></td>
    <td>07-31</td>
    <td><span class="blue">辅助</span></td>
  </tr>
  <tr>
    <td>KR3 日均进度</td>
    <td>日均回款</td>
    <td>—</td>
    <td><b>10 万/天</b></td>
    <td>07-31</td>
    <td><span class="blue">监控</span></td>
  </tr>
</table>
</div>

<h2>五、关键动作清单</h2>

<h3>KR1 行动 — 新客 30 万</h3>
<div class="card">
<table>
  <tr><th>#</th><th>动作</th><th>Owner</th><th>截止</th><th>预期</th></tr>
  <tr><td>1.1</td><td>SEO 5 篇深度内容(获长尾流量)</td><td>张三</td><td>07-29</td><td>20 个线索</td></tr>
  <tr><td>1.2</td><td>BD 陌生拜访 50 家目标客户</td><td>借调 BD ×2</td><td>07-29</td><td>15 个意向</td></tr>
  <tr><td>1.3</td><td>SEM 投 5 万(主推 X 产品)</td><td>市场部</td><td>07-27 起</td><td>50 个点击,5 个转化</td></tr>
  <tr><td>1.4</td><td>直播 2 场(周三 + 周五)</td><td>李四</td><td>07-29/31</td><td>10 个订单</td></tr>
</table>
</div>

<h3>KR2 行动 — 老客 20 万</h3>
<div class="card">
<table>
  <tr><th>#</th><th>动作</th><th>Owner</th><th>截止</th><th>预期</th></tr>
  <tr><td>2.1</td><td>短信群发 8 万老客(限时优惠)</td><td>运营</td><td>07-27</td><td>500 个响应</td></tr>
  <tr><td>2.2</td><td>电话跟进 100 个高价值老客</td><td>客服</td><td>07-30</td><td>30 个加购</td></tr>
  <tr><td>2.3</td><td>私域推送限时套餐</td><td>运营</td><td>07-28</td><td>50 个购买</td></tr>
</table>
</div>

<h3>KR3 行动 — 日均 10 万进度</h3>
<div class="card">
<table>
  <tr><th>日</th><th>目标进度</th><th>关键动作</th><th>复盘点</th></tr>
  <tr><td>周一 07-27</td><td>10 万(20%)</td><td>SEM 上线 + BD 出动</td><td>18:00 当面</td></tr>
  <tr><td>周二 07-28</td><td>20 万(40%)</td><td>BD 转化 + 私域推送</td><td>18:00 当面</td></tr>
  <tr><td>周三 07-29</td><td>30 万(60%) ⭐</td><td>直播 + SEO 内容</td><td>投资人预沟通</td></tr>
  <tr><td>周四 07-30</td><td>40 万(80%)</td><td>电话跟进 + 二次转化</td><td>18:00 邮件</td></tr>
  <tr><td>周五 07-31</td><td><b>50 万(100%)</b></td><td>收尾 + 报数据</td><td>17:00 当面</td></tr>
</table>
</div>

<h2>六、ART 不可能三角方案</h2>
<div class="warning">
<p><b>当前三角:</b> A=50 万 / R=现有团队 5 人 / T=5 天</p>
<p>瓶颈分析:历史峰值 35 万,要做到 50 万需 1.43x 突破,仅靠现有资源难达成。</p>
</div>

<div class="grid">
  <div class="tri-card recommended">
    <h4>方案 A · 动 R(资源追加) ⭐ 推荐</h4>
    <ul>
      <li><b>借调:</b> 2 BD 支援 3 天</li>
      <li><b>预算:</b> 加 5 万 SEM</li>
      <li><b>设计:</b> 1 素材加班</li>
      <li><b>投入:</b> ~7-8 万</li>
      <li><b>产出:</b> 50 万达成(置信 85%)</li>
      <li><b>回收:</b> 当周回款即覆盖</li>
    </ul>
  </div>
  <div class="tri-card">
    <h4>方案 B · 动 T(时间)</h4>
    <ul>
      <li>延后到 8 天(到下周三)</li>
      <li>目标 50 万不变</li>
      <li>代价:错过投资人预沟通</li>
      <li><b>不推荐</b>(融资节奏不能动)</li>
    </ul>
  </div>
  <div class="tri-card">
    <h4>方案 C · 动 A(目标降级)</h4>
    <ul>
      <li>目标降到 35 万(历史峰值)</li>
      <li>时间不变</li>
      <li>代价:目标未达,被谈话</li>
      <li><b>不推荐</b>(背锅风险)</li>
    </ul>
  </div>
</div>

<h2>七、汇报节奏表</h2>
<div class="card">
<table>
  <tr><th>时点</th><th>形式</th><th>内容</th><th>收件人</th></tr>
  <tr><td>周一 09:00</td><td>当面 + 邮件</td><td>目标确认 + 3 方案请领导选</td><td>领导</td></tr>
  <tr><td>每日 18:00</td><td>微信群</td><td>当日进度 + 风险</td><td>领导 + 团队</td></tr>
  <tr><td>周三 12:00</td><td>邮件</td><td>中期进度汇报</td><td>领导 + 财务</td></tr>
  <tr><td>周五 17:00</td><td>当面 + 周报</td><td>完成情况 + 下周计划</td><td>领导 + 关键人</td></tr>
</table>
</div>

<h2>八、风险登记表</h2>
<div class="card">
<table>
  <tr><th>ID</th><th>风险</th><th>影响</th><th>概率</th><th>应对</th></tr>
  <tr>
    <td>R1</td>
    <td>BD 借调被拒</td>
    <td>KR1 难达成</td>
    <td><span class="yellow">中</span></td>
    <td>周一 9:00 即提交申请;备选 = 现有团队延长工时</td>
  </tr>
  <tr>
    <td>R2</td>
    <td>SEM ROI 差</td>
    <td>5 万预算浪费</td>
    <td><span class="yellow">中</span></td>
    <td>每日监控 ROI,< 1.5 立即停</td>
  </tr>
  <tr>
    <td>R3</td>
    <td>关键客户回款延迟</td>
    <td>KR2 难达成</td>
    <td><span class="red">高</span></td>
    <td>提前 3 天催款 + 备选客户 3 个</td>
  </tr>
  <tr>
    <td>R4</td>
    <td>团队加班超 60h</td>
    <td>不可持续</td>
    <td><span class="yellow">中</span></td>
    <td>周三检查工时,超过立即申请资源</td>
  </tr>
</table>
</div>

<h2>九、防甩锅协议</h2>
<div class="alert">
<p><b>本任务关键留痕点:</b></p>
<ul class="checklist">
  <li>周一 09:00 邮件确认 50 万目标(原话复述)</li>
  <li>领导选定方案 A 后,邮件确认资源支持</li>
  <li>每日进度微信群同步 + 邮件备份</li>
  <li>周三投资人预沟通结果邮件给领导</li>
  <li>周五完成结果邮件 + 周报抄送财务/HR</li>
  <li>所有口头决策 24h 内邮件化</li>
</ul>
</div>

<h2>十、本周 5 天时间线</h2>
<div class="timeline">

  <div class="timeline-item">
    <div class="date">周一 07-27</div>
    <p><b>09:00</b> 找领导确认目标 + 3 方案 → 邮件留痕</p>
    <p><b>10:00</b> BD 团队 + 借调 BD 启动</p>
    <p><b>14:00</b> SEM 上线,5 篇 SEO 内容开写</p>
    <p><b>18:00</b> 当日进度同步(目标 10 万)</p>
  </div>

  <div class="timeline-item">
    <div class="date">周二 07-28</div>
    <p><b>全天</b> BD 转化(15 个意向 → 5 个签约)</p>
    <p><b>10:00</b> 短信群发老客</p>
    <p><b>14:00</b> 私域推送套餐</p>
    <p><b>18:00</b> 当日进度同步(目标累计 20 万)</p>
  </div>

  <div class="timeline-item">
    <div class="date">周三 07-29 ⭐ 关键日</div>
    <p><b>10:00</b> 第一场直播</p>
    <p><b>12:00</b> 中期进度汇报邮件</p>
    <p><b>15:00</b> 投资人预沟通(已完成 ≥ 30 万)</p>
    <p><b>18:00</b> 当日进度同步</p>
  </div>

  <div class="timeline-item">
    <div class="date">周四 07-30</div>
    <p><b>全天</b> 电话跟进老客 + BD 二次跟进</p>
    <p><b>10:00</b> SEO 内容 5 篇全部上线</p>
    <p><b>18:00</b> 当日进度同步(目标累计 40 万)</p>
  </div>

  <div class="timeline-item">
    <div class="date">周五 07-31</div>
    <p><b>14:00</b> 收尾 + 二次转化冲刺</p>
    <p><b>17:00</b> 当面向领导汇报 + 周报</p>
    <p><b>18:00</b> 邮件抄送财务/HR(留痕)</p>
  </div>

</div>

<h2>十一、KPI 仪表板</h2>
<div class="grid">
  <div class="kpi">
    <div class="num">50万</div>
    <div class="label">周目标</div>
  </div>
  <div class="kpi">
    <div class="num">30万</div>
    <div class="label">新客 KR</div>
  </div>
  <div class="kpi">
    <div class="num">20万</div>
    <div class="label">老客 KR</div>
  </div>
  <div class="kpi">
    <div class="num">10万</div>
    <div class="label">日均目标</div>
  </div>
  <div class="kpi">
    <div class="num">7人</div>
    <div class="label">团队规模</div>
  </div>
  <div class="kpi">
    <div class="num">7-8万</div>
    <div class="label">资源追加</div>
  </div>
</div>

<h2>十二、沟通话术(找领导用)</h2>
<div class="success">
<p><b>开场(周一 09:00):</b></p>
<blockquote style="margin:8px 0;padding:8px 12px;background:#fff;border-left:3px solid #22c55e;">
老板,关于下周 50 万业绩,我整理了 3 个方案请您定夺:
<ul>
  <li><b>方案 A(推荐):</b>追加资源(借调 2 BD + 5 万 SEM + 设计支援),达成 50 万</li>
  <li><b>方案 B:</b>延后到 8 天,达成 50 万(但错过周三投资人预沟通)</li>
  <li><b>方案 C:</b>现有资源,达成 35 万(历史峰值)</li>
</ul>
按公司融资节奏,我建议方案 A。具体动作我已发您邮箱,您看是否可行?
</blockquote>
</div>

<h2>十三、方案总结</h2>
<div class="card">
<p><b>如果资源到位(方案 A),本方案置信度 85%。</b></p>
<p><b>关键里程碑:</b> 周三投资人预沟通前达成 30 万(60%)</p>
<p><b>最大风险:</b> 关键客户回款延迟(已备 3 个备选客户)</p>
<p><b>必出物:</b> 周五 17:00 完整周报 + 数据邮件给领导</p>
</div>

<div class="footer">
方案生成时间:2026-07-26 · 基于主公提示词 + 目标管理 skill v1.0<br>
涉及模型:SMART + OKR + KPI + Sprint + ART + PDCA<br>
下次更新:周一 09:00 后(基于领导选定方案调整)
</div>

</div>
</body>
</html>
```

---

## 方案要点回顾(给人看版)

### 1. SMART 化

模糊"下周 50 万"→"下周回款 50 万(新客 30 + 老客 20),2026-07-31 前"

### 2. 5 Why + 隐藏目标

- 根因:融资节奏需要,本周是死线
- 隐藏目标:回款(不是合同)、新客为主、周三前完成 50%

### 3. OKR + KPI 拆解

- O:完成 50 万冲刺
- KR1:新客 30 万 / KR2:老客 20 万 / KR3:日均 10 万

### 4. ART 三角(关键)

3 方案让领导选,推荐方案 A(资源追加 7-8 万,产出 50 万)

### 5. 汇报节奏

- 周一当面 + 邮件
- 每日 18:00 同步
- 周三邮件 + 投资人沟通
- 周五当面 + 周报

### 6. 防甩锅

6 个关键留痕点,口头决策 24h 内邮件化

---

## 复盘节点

- **周三 12:00**:中期复盘(达成 30 万?否则启动应急)
- **周五 17:00**:完成复盘 + GRAI 启动
- **下周一**:月度报告素材积累