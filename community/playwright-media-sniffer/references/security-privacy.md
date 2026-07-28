# Security Privacy

_从 playwright-media-sniffer v1.0 SKILL.md 抽取 (Line 415-430)_

## 🛡️ 安全与隐私

### Cookie 安全

- ✅ **本地存储**：`auth/*.json` 仅保存在本地
- ✅ **加密可选**：可使用 `cryptography` 加密 storage_state
- ⚠️ **敏感提示**：提醒用户不要分享 auth/ 目录

### 反爬风险

- **正常使用**：模拟人类行为，风险极低
- **高频调用**：避免短时间大量请求（建议间隔 ≥ 30s）
- **账号安全**：建议使用小号测试，避免主账号被封

---

