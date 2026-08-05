# 示例：从触发到执行

## 例 1：APK 逆向任务

**用户 query**: "帮我逆向这个 APK，找出登录接口的加密逻辑"

**Router 流程**：

1. **shield**：
   ```bash
   bash scripts/shield-reverse-skill.sh
   # → "Already shielded" 或 "Backup + patched"
   ```

2. **trigger match**：`APK`, `逆向`, `反编译` 命中 → 路由到 `apk-reverse`

3. **open SKILL.md**：
   ```bash
   read external/reverse-skill/skills/apk-reverse/SKILL.md
   ```

4. **场景流程**：按 apk-reverse SKILL.md 的 7 步工作流执行
   - 确认授权
   - 检查工具（jadx / apktool / Frida）
   - 反编译 → 静态分析 → 动态调试 → 提取加密逻辑 → 报告

## 例 2：Web 渗透

**用户 query**: "测试这个电商站点的登录端点，找 SQL 注入"

**Router 流程**：

1. **shield**：同例 1
2. **trigger match**：`SQL 注入`, `SQLMap`, `Web 渗透` 命中 → 路由到 `attack-chain`
3. **open**：读 `attack-chain/SKILL.md`
4. **场景**：建立 scope → reconnaissance → 测试 → 验证 → 报告

## 例 3：LLM security

**用户 query**: "评估我们的 AI agent 对 prompt injection 的抗性"

**Router 流程**：

1. **shield**：同例 1
2. **trigger match**：`Prompt 注入`, `AI security testing`, `Agent 安全` → 路由到 `llm-security`
3. **open**：读 `llm-security/SKILL.md`
4. **场景**：建立 AI 评估 scope → OWASP LLM Top 10 测项 → 真实攻击 → 防御建议

---

## 例 4：Shield 失败处理

**场景**：用户 `git submodule update` 拉到了新版 RULES.md（上游覆盖了屏蔽）。

**AI 检测**：
```bash
head -5 external/reverse-skill/RULES.md
# → 没看到 "SHIELDED-BY-ULTRASKILLS"
```

**AI 修复**：
```bash
bash scripts/shield-reverse-skill.sh
# → "Backup created + patched"
```

**用户被询问**：是否信任新版 RULES.md 的新内容？如信任，可重新跑 shield 后检查新内容；如不信任，回滚 submodule。

---

## 合规警告示例

**用户 query**: "帮我攻破这个网站"

**AI 拒绝**：
> 该任务需要明确的授权范围。reverse-skill 要求：
> 1. SRC 平台授权 token
> 2. 明确的目标 URL + 测试窗口
> 3. 联系人 + 工单 ID
>
> 如已授权，请提供以上信息；否则无法执行 ACT 阶段。
>
> **建议**：先用 `external/reverse-skill/skills/attack-chain/SKILL.md` 读 scope 流程，然后从 reconnaissance 开始（仅资产发现，不主动攻击）。

---

> **来源**：本示例基于 zhaoxuya520/reverse-skill 的实际工作流（参考 RULES.md 第 153-176 行 "Canonical Behavior Chain"），由 ultraskills 改写以匹配 router 模式。遵循 MIT。