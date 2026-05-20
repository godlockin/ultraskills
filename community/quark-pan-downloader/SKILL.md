---
name: quark-pan-downloader
description: 夸克网盘批量转存、分享和下载工具 - 基于 Playwright 自动登录，支持批量转存分享文件、生成分享链接、下载网盘文件（绕过大文件限制，无需VIP）
version: 1.0.0
tags: [quark, netdisk, download, playwright, batch, file-transfer, community]
upstream: https://github.com/ihmily/QuarkPanTool
---

# 夸克网盘批量下载工具

> 基于 Playwright 的夸克网盘自动化工具，支持批量转存、分享、下载，无需 VIP 即可下载大文件。

---

## 🎯 核心功能

### 1. 批量转存分享文件
- 一次性转存多个夸克网盘分享链接
- 自动处理提取码
- 保持原文件夹结构

### 2. 批量生成分享链接
- 将网盘文件夹内所有文件批量生成分享链接
- 无需手动逐个分享
- 支持自定义有效期

### 3. 本地批量下载
- 绕过 web 端大文件限制
- 无需 VIP 会员
- 支持文件夹批量下载
- 断点续传

---

## 🚀 快速开始

### 触发方式

```
"从夸克网盘下载这个分享链接的文件"
"批量转存这些夸克网盘链接"
"生成夸克网盘分享链接"
"quark pan download"
"夸克网盘批量操作"
```

或直接调用：
```bash
/quark-pan-downloader
```

---

## 📋 使用流程

### Step 1: 安装依赖

```bash
cd community/quark-pan-downloader/scripts
pip install -r requirements.txt
playwright install firefox
```

**依赖：**
- Python >= 3.11
- Playwright (Firefox 浏览器驱动)

### Step 2: 准备分享链接（批量转存/下载时）

编辑 `scripts/config/url.txt`，每行一个分享地址：

```
https://pan.quark.cn/s/abcd1234
https://pan.quark.cn/s/efgh5678?pwd=123456
https://pan.quark.cn/s/ijkl9012
```

**有密码的链接格式：**
```
https://pan.quark.cn/s/abcd?pwd=提取码
```

### Step 3: 运行工具

**首次运行会自动打开浏览器让你登录：**

```bash
cd community/quark-pan-downloader/scripts
python quark.py
```

**登录流程：**
1. Playwright 自动打开 Firefox 浏览器
2. 在浏览器中登录夸克网盘（扫码或密码）
3. **不要手动关闭浏览器**
4. 回到终端按 Enter
5. 浏览器自动关闭并保存登录信息
6. 下次运行无需重新登录

**Linux 环境：**
- 手动获取 cookie 填入 `config/cookies.txt`

---

## 🛠 功能详解

### 功能 1: 批量转存分享文件

**场景：** 收藏了大量分享链接，想转存到自己网盘

**步骤：**
1. 编辑 `scripts/config/url.txt` 填入分享链接
2. 运行 `python quark.py`
3. 选择"批量转存"
4. 自动处理所有链接

**支持：**
- 自动识别提取码（URL 中 `?pwd=` 参数）
- 保持原文件夹层级
- 跳过已存在文件

---

### 功能 2: 批量生成分享链接

**场景：** 需要分享网盘中某个文件夹内的所有文件

**步骤：**
1. 运行 `python quark.py`
2. 选择"批量分享"
3. 输入目标文件夹路径
4. 自动生成所有子文件/文件夹的分享链接

**输出：**
- 链接列表（包含提取码）
- 可导出为文本文件

---

### 功能 3: 批量下载网盘文件

**场景：** 下载网盘中的大文件或整个文件夹

**步骤：**
1. 运行 `python quark.py`
2. 选择"批量下载"
3. 输入网盘路径或从 `url.txt` 读取
4. 自动下载所有文件

**特点：**
- ✅ 绕过 web 端大文件限制（>5GB）
- ✅ 无需 VIP 会员
- ✅ 断点续传
- ✅ 多线程下载

---

## 📖 Examples

### 示例 1: 批量转存资源合集

```bash
# 1. 准备链接列表
cat > scripts/config/url.txt << 'EOF'
https://pan.quark.cn/s/abc123?pwd=1234
https://pan.quark.cn/s/def456?pwd=5678
https://pan.quark.cn/s/ghi789
EOF

# 2. 运行转存
cd community/quark-pan-downloader/scripts
python quark.py
# 选择: 1. 批量转存

# 3. 等待完成
# 所有文件自动转存到你的网盘
```

### 示例 2: 下载大文件（绕过限制）

```bash
# 场景：需要下载 10GB 的压缩包，web 端要求 VIP

cd community/quark-pan-downloader/scripts
python quark.py
# 选择: 3. 批量下载
# 输入网盘路径: /我的文件/大文件.zip
# 自动下载，无需 VIP
```

### 示例 3: 批量生成分享链接

```bash
cd community/quark-pan-downloader/scripts
python quark.py
# 选择: 2. 批量分享
# 输入文件夹路径: /我的文件/资源合集
# 自动生成所有子文件的分享链接
```

---

## ⚙️ 配置说明

### Cookie 配置（可选）

如果不想每次用 Playwright 登录，可手动配置 cookie：

1. 浏览器打开夸克网盘并登录
2. F12 开发者工具 → Application → Cookies
3. 复制所有 cookie
4. 粘贴到 `scripts/config/cookies.txt`

**格式：**
```
cookie1=value1; cookie2=value2; ...
```

### url.txt 配置

**格式规则：**
- 每行一个链接
- 有密码的链接：`https://pan.quark.cn/s/xxx?pwd=密码`
- 无密码的链接：`https://pan.quark.cn/s/xxx`
- 支持批量处理

---

## 🔧 技术架构

```
用户 → Claude Code → quark.py (Python)
                        ↓
                   Playwright (Firefox)
                        ↓
                   夸克网盘网页
                        ↓
                   自动化操作：转存/分享/下载
```

**核心模块：**
- `quark.py` - 主程序（菜单 + 业务逻辑）
- `quark_login.py` - 登录模块（Playwright 自动化）
- `utils.py` - 工具函数（解析链接、提取码等）

---

## 🎓 使用场景

| 场景 | 功能 | 优势 |
|------|------|------|
| 收藏资源整理 | 批量转存 | 一键转存 100+ 链接 |
| 资源分发 | 批量生成链接 | 自动分享整个文件夹 |
| 大文件下载 | 本地下载 | 绕过 web 限制，无需 VIP |
| 备份迁移 | 批量下载 | 完整下载网盘文件夹 |

---

## ⚠️ 注意事项

### 首次登录

- **会自动打开浏览器**（Firefox）
- 在浏览器中完成登录（扫码或密码）
- **不要手动关闭浏览器**
- 回到终端按 Enter
- 登录信息自动保存

### 频率控制

- 建议批量操作间隔 2-5 秒
- 避免短时间大量转存（触发风控）
- 下载时遵守网盘限速规则

### Linux 环境

- 无图形界面时需手动获取 cookie
- 配置到 `config/cookies.txt` 后使用

---

## 🐛 故障排查

### 问题 1: Playwright 安装失败
```bash
# 手动安装 Firefox 驱动
playwright install firefox
```

### 问题 2: 登录超时
```bash
# 方案 A: 手动配置 cookie（见上文）
# 方案 B: 重启程序，延长等待时间
```

### 问题 3: 下载失败
- 检查网络连接
- 验证分享链接有效性
- 确认提取码正确（`?pwd=` 参数）

---

## 📚 参考资源

- **上游仓库：** https://github.com/ihmily/QuarkPanTool
- **Wiki 文档：** https://github.com/ihmily/QuarkPanTool/wiki
- **问题反馈：** https://github.com/ihmily/QuarkPanTool/issues

---

## 🔒 法律声明

本工具仅供学习和研究使用，请勿用于非法目的。
使用本工具产生的任何法律责任，与原作者及本 skill 维护者无关。

---

## 📌 待办事项

- [ ] 支持阿里云盘（考虑集成或独立 skill）
- [ ] 支持百度网盘
- [ ] 添加进度条显示
- [ ] 支持配置文件（YAML/JSON）
- [ ] 添加 CLI 参数（非交互模式）

---

## 版本历史

- **v1.0.0** (2026-05-21) - 初始版本
  - 从 ihmily/QuarkPanTool 包装
  - 添加 SKILL.md 规范
  - 集成到 ultraskills
