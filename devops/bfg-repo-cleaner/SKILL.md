---
name: bfg-repo-cleaner
description: Git 仓库历史清理工具。使用 BFG Repo-Cleaner 移除大文件、敏感数据（密码、密钥）、凭证等私密信息。10-720x 比 git-filter-branch 更快。触发词：清理 git 历史、删除大文件、移除敏感数据、bfg、git 仓库净化
---

# BFG Repo-Cleaner

Git 仓库历史清理工具 - 移除大文件和敏感数据，比 git-filter-branch 快 10-720 倍。

## 何时使用

使用此技能清理 Git 仓库历史中的：

1. **大文件** - 误提交的大文件（>100MB 的二进制文件、视频、数据集等）
2. **敏感数据** - 密码、API 密钥、凭证、私钥（id_rsa、id_dsa）
3. **不需要的文件** - 特定名称的文件或目录（.git、node_modules 等）
4. **批量替换** - 替换历史中的所有出现的敏感文本

## 快速开始

### 1. 准备环境

```bash
# 安装 BFG（macOS）
brew install bfg

# 安装 BFG（其他方式）
# 下载 jar 文件：https://repo1.maven.org/maven2/com/madgag/bfg/1.15.0/bfg-1.15.0.jar
# 需要 Java 11 或更高版本

# 验证安装
bfg --version
```

### 2. 克隆仓库（镜像模式）

```bash
# 重要：使用 --mirror 克隆完整仓库数据库
git clone --mirror <repo-url>
cd <repo-name>.git

# ⚠️ 操作前务必备份！
```

### 3. 运行 BFG

```bash
# 删除大于 100MB 的文件
bfg --strip-blobs-bigger-than 100M .

# 删除指定名称的文件
bfg --delete-files "id_rsa|id_dsa" .

# 删除指定目录
bfg --delete-folders ".git" .

# 替换敏感文本
bfg --replace-text banned.txt .
```

### 4. 清理并推送

```bash
# 清理 Git 垃圾
git reflog expire --expire=now --all && git gc --prune=now --aggressive

# 验证清理结果
git log --stat

# 强制推送到远程
git push --force
```

## 常用命令

### 删除大文件

```bash
# 删除大于指定大小的文件
bfg --strip-blobs-bigger-than 50M repo.git
bfg --strip-blobs-bigger-than 1G repo.git

# 删除最大的 N 个文件
bfg --strip-biggest-blobs 100 repo.git

# 删除特定扩展名的大文件
bfg --delete-files "*.mp4|*.mov|*.zip" repo.git
```

### 删除敏感文件

```bash
# 删除私钥文件
bfg --delete-files "id_rsa|id_dsa" repo.git

# 删除密码文件
bfg --delete-files "*.kdbx|*.key|passwords.txt" repo.git

# 删除 .git 目录（从其他 VCS 迁移时常见）
bfg --delete-folders .git --delete-files .git --no-blob-protection repo.git
```

### 替换敏感文本

创建 `banned.txt` 文件，每行一个需要替换的敏感字符串：

```text
# banned.txt 示例
password123
AKIAIOSFODNN7EXAMPLE
-----BEGIN RSA PRIVATE KEY-----
```

运行替换：

```bash
bfg --replace-text banned.txt repo.git
```

替换为自定义文本：

```text
# 使用 regex: 前缀进行正则匹配
regex:AKIA[0-9A-Z]{16}
glob:*password*
```

### 高级选项

```bash
# 关闭最新提交保护（默认保护 master/HEAD 分支的最新提交）
bfg --no-blob-protection --delete-files secret.txt repo.git

# 仅清理特定分支
bfg --delete-files secret.txt --branch-filter feature/* repo.git

# 显示详细信息
bfg --delete-files secret.txt --log-to-file repo.git
```

## 完整工作流程示例

### 场景 1：移除 500MB 视频文件

```bash
# 1. 镜像克隆
git clone --mirror https://github.com/user/repo.git
cd repo.git

# 2. 运行 BFG
bfg --strip-blobs-bigger-than 100M .

# 3. 清理
git reflog expire --expire=now --all && git gc --prune=now --aggressive

# 4. 验证
du -sh .  # 检查仓库大小

# 5. 推送
git push --force
```

### 场景 2：移除泄露的 API 密钥

```bash
# 1. 创建 banned.txt
cat > banned.txt << 'EOF'
AKIAIOSFODNN7EXAMPLE
wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
EOF

# 2. 镜像克隆
git clone --mirror https://github.com/user/repo.git
cd repo.git

# 3. 运行 BFG
bfg --replace-text banned.txt .

# 4. 清理并提交（如果需要修复最新提交）
# 如果最新提交包含密钥，先手动修复
git reset --hard HEAD~1
# 编辑文件移除密钥
git commit -am "Remove exposed credentials"

# 5. 重新运行 BFG
bfg --replace-text banned.txt .

# 6. 清理并推送
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force
```

## 重要注意事项

### ⚠️ 警告

1. **备份第一** - 操作前务必备份原始仓库
2. **破坏性操作** - 会重写 Git 历史，影响所有协作者
3. **通知团队** - 清理后所有人需要重新克隆
4. **最新提交保护** - 默认不修改 master/HEAD 的最新提交

### 受保护的提交

BFG 默认不修改最新提交（HEAD/master）的内容：

- 如果敏感数据在最新提交中，需要先修复提交
- 或者使用 `--no-blob-protection` 关闭保护（不推荐）
- 受保护提交中的文件不会被删除，但 commit SHA 会变

### 限制

- **不支持** - 修改提交信息、作者信息（用 git-filter-branch）
- **不支持** - 复杂的重命名或文件移动
- **支持** - 删除文件、替换文本、删除大文件

## 故障排除

### "File still exists in HEAD"

```bash
# 文件在当前 HEAD 中存在，需要先删除
git rm --cached path/to/file
git commit -m "Remove sensitive file"

# 然后运行 BFG
bfg --delete-files filename repo.git
```

### 仓库大小没有减少

```bash
# 需要运行 git gc 清理
cd repo.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 检查实际大小
du -sh .
```

### 清理后无法推送

```bash
# 需要强制推送（会重写历史）
git push --force

# 如果是受保护分支，可能需要
git push --force --no-verify
```

## 资源

### scripts/

包含自动化脚本：

- `cleanup_repo.sh` - 完整的清理流程脚本
- `check_secrets.sh` - 检查仓库是否包含常见密钥模式

### references/

- `common_patterns.md` - 常见敏感数据模式（正则表达式）
- `migration_guide.md` - 从 git-filter-branch 迁移指南

## 替代方案对比

| 功能 | BFG | git-filter-branch |
|------|-----|-------------------|
| 删除大文件 | ✅ 快速 | ⚠️ 慢 |
| 替换文本 | ✅ 简单 | ⚠️ 复杂 |
| 修改提交信息 | ❌ | ✅ |
| 修改作者 | ❌ | ✅ |
| 复杂过滤 | ⚠️ 有限 | ✅ 灵活 |
| 性能 | ⭐⭐⭐⭐⭐ | ⭐⭐ |

**推荐**：优先使用 BFG，除非需要修改提交元数据。

---

*基于 [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/) - 一个由 Roberto Tyley 开发的 Scala 工具*
