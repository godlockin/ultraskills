# Git Commit 最佳实践示例

## 示例 1: 新功能 (Feature)

### Before (❌ Bad)

```text
added login button
```

### After (✅ Good)

```text
feat(auth): add login button to navigation bar

This adds a login button component to the main navigation bar.
It triggers the auth modal when clicked.

Part of #123
```

---

## 示例 2: Bug 修复 (Fix)

### Before (❌ Bad)

```text
fix crash
```

### After (✅ Good)

```text
fix(user-profile): resolve null pointer exception when avatar is missing

Previously, accessing the profile page without an avatar would cause a crash.
This commit adds a null check and renders a default placeholder.

Fixes #456
```

---

## 示例 3: 重构 (Refactor)

### Before (❌ Bad)

```text
clean up code
```

### After (✅ Good)

```text
refactor(api): extract validation logic to standalone service

Moved validation logic from the UserContoller to a new ValidationService.
This improves testability and reduces code duplication.
```

---

## 示例 4: 破坏性变更 (Breaking Change)

### Before (❌ Bad)

```text
change api url
```

### After (✅ Good)

```text
feat(api): migrate to v2 endpoints

BREAKING CHANGE: The base URL has changed from /api/v1 to /api/v2.
All clients must update their configuration.
```
