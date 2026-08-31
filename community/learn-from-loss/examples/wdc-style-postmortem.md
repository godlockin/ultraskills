# 示例：WDC 风格比赛复盘（脱敏）

> **Synthetic example only — not empirical evidence。**
> 本案例所有数字、团队名、比赛名为脱敏虚构；用于演示 8 维度打分、Gap 分析、Panel findings、Iron Rules 与 Day-0 Checklist 的填写方式。任何对外引用前必须替换为真实数据。

---

## 1. Result Summary

- 项目：`Kestrel Bay Dashboard`
- 比赛：`DataFive Demo Jam APAC 2026`（虚构）
- 自评综合：72 / 100
- 排名：12 / 31
- 顶档 Gap：Carrier（-5）、Memorability（-6）

## 2. Winner Analysis（虚构）

| Rank | Team | Carrier | Hook | Score | What they did differently |
|------|------|---------|------|-------|---------------------------|
| 1 | Data Five | HTML | "五行缺数据" | 92 | Cultural team name + hover interactions |
| 2 | Vikings | Video | "came for data, stayed for insights" | 89 | Multi-voice + quotable closing |
| 3 | Insights Fund | QR → App | Scan to use | 87 | Zero-friction adoption |
| ... | Kestrel Bay | PPT | "Plan A" | 72 | Strong content, poor delivery |

## 3. 8-Dimension Self vs Winners

| # | 维度 | 自评 | Data Five | Gap | 根因 | 修复 |
|---|---|---:|---:|---:|---|---|
| 1 | Carrier convenience | 4 | 9 | -5 | 默认 PPT，未挑战 | Day-0 carrier workshop |
| 2 | Memorability | 3 | 9 | -6 | 团队名抽象，无 hook | 双关团队名 + origin story |
| 3 | Actionability | 7 | 8 | -1 | 行动建议已列 | 强化 CTA |
| 4 | Market coverage | 5 | 8 | -3 | 单市场 80% | 5 国对称骨架 |
| 5 | Methodology rigor | 8 | 8 | 0 | 持平 | 维持 |
| 6 | Visual consistency | 6 | 9 | -3 | 模板混用 | Design token 单一来源 |
| 7 | Sensory quality | 7 | 8 | -1 | 拼写有零星错误 | Lint 关卡 |
| 8 | Story arc | 8 | 8 | 0 | 持平 | 维持 |

## 4. Expert Panel Review（虚构）

### 4.1 Content Accuracy

- P0：1 处引用与脚注不符，已修
- P1：图表缺单位，已补

### 4.2 Design System

- P1：2 个页面使用了非 token 颜色，已迁回 token
- P2：移动端断点不一致，记录下一轮处理

### 4.3 Audio & Pipeline

- P0：1 段静音 > 5s，已重录
- P1：导出参数不一致，统一为同规格

## 5. Iron Rules（本轮新增 L7、L8、L9）

| # | Rule | Pass Criteria |
|---|---|---|
| L7 | 默认载体 ≠ PPT | 必须先证伪 PPT 优势 |
| L8 | 双关团队名 + 1 个 metaphor | 团队成员外的人能复述 |
| L9 | 5 国对称骨架 | 每国 ≥ 1 页，锁定后才能改 |

## 6. Day-0 Checklist

- [ ] 评委画像 workshop
- [ ] 团队名 + origin story + 1 metaphor（4h 内）
- [ ] 默认载体 ≠ PPT（先证伪）
- [ ] Pre-mortem：列 5 个可能输因
- [ ] 5 国对称骨架
- [ ] 外部冷读（时间末段前）
- [ ] Lint 全过
- [ ] Day-0 起手前运行本 skill

## 7. 复盘使用边界（必填）

- 本次复盘用于流程/系统/交付物改进，不用于个人绩效归因：□ 是
- 引用数据已标注来源、日期、口径：□ 是
- 如任何一项为否：停止本流程，转 `learn-from-loss` 边界说明
