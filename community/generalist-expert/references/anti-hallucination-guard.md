# Anti-Hallucination Guard

> 本文件原计划承载 `generalist-expert` v1 时的 anti-hallucination 完整示例。
> 由于上游模板与 reference 命名变更，最新规则已内联进 `SKILL.md` 的 5 维度评估说明。
> 本文件作为占位，避免历史引用断链；新内容请直接编辑 SKILL.md。

## 当前生效规则摘要

- **事实准确性（Dimension 1）**：必须给具体来源或标注 `[unverified]`；禁止以「通常」「一般」「业界共识」代替具体引用。
- **隐含假设（Dimension 3）**：列出 3 个或以上；每个假设必须可证伪（写出「若 X 错则结论失效」）。
- **反驳视角（Dimension 4）**：必出 1 个「strongest counter-argument」；不与初始结论相互抵消。
- **领域风险（Dimension 5）**：当领域存在合规、隐私、安全或可执行性风险时，单独列出「stop conditions」与建议转介。

## Verdict 必填字段

每次输出的末尾必须包含结构化 verdict，便于后续 reviewer 与下游 skill 接管：

```yaml
verdict:
  confidence: HIGH | MED | LOW | CONTESTED
  out_of_scope: true | false
  recommendation: proceed | refine | handoff | reject
  handoff_to: <skill-id> # recommendation 为 handoff 时必填
  next_action: <一句话下一步>
```

- `recommendation: handoff` 必须给出具体的下游 skill id；不得写 `general-purpose` 这种万能路由。
- 当用户问题更适合 `system-design` / `career-coach` / `office-hours` / `legal-risk-assessment` 等专项 skill 时，优先 handoff。
