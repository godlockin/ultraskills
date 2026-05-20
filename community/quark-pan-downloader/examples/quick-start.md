# 快速开始

## 5 分钟上手指南

### 第一步：安装（2 分钟）

```bash
cd community/quark-pan-downloader/scripts
pip install -r requirements.txt
playwright install firefox
```

### 第二步：首次登录（1 分钟）

```bash
python quark.py
```

**会自动发生：**
1. 打开 Firefox 浏览器
2. 跳转到夸克网盘登录页
3. 你在浏览器中登录（扫码或密n
### 第三步：使用（2 分钟）

**场景 A: 转存分享链接**
```bash
# 1. 编辑 url.txt
echo "https://pan.quark.cn/s/abc123?pwd=1234" > config/url.txt

# 2. 运行
python quark.py
# 选择: 1  [批量转存]

# 完成！
```

**场景 B: 下载文件**
```bash
python quark.py
# 选择: 3  [批量下载]
# 输入路径: /我的文件/大文件.zip

# 开始下载（无需 VIP）
```

---

## 常用命令速查

```bash
# 批量转存
echo "链接1\n链接2" > config/url.txt
python quark.py  # 选择 1

# 批量分享
python quark.py  # 选择 2 → 输入目录路径

# 批量下载
python quark.py  # 选择 3 → 输入文件路径

# 重新登录
rm config/cookies.txt
python quark.py  # 自动打开浏览器
```

---

## 第一次使用推荐流程

1. **测试单个链接转存**
   ```bash
   echo "https://pan.quark.cn/s/test" > config/url.txt
   python quark.py → 选择 1
   ```

2. **验证网盘中已转存**
   - 打开夸克网盘 web 端
   - 查看 "转存文件" 目录

3. **测试下载**
   ```bash
   python quark.py → 选择 3
   # 输入刚转存的文件路径
   ```

4. **批量使用**
   - url.txt 填入多个链接
   - 重复步骤 1

---

## 终端输出示例

```
=================================
夸克网盘批量工具
=================================

请选择功能:
1. 批量转存
2. 批量分享
3. 批量下载
0. 退出

请输入选项 (0-3): 1

读取 url.txt ... 发现 3 个链接
开始批量转存...

[1/3] https://pan.quark.cn/s/abc123
  → 正在获取文件列表...
  → 发现 15 个文件
  → 转存中... [████████████] 100%
  ✓ 转存完成: /转存文件/资料包1

[2/3] https://pan.quark.cn/s/def456?pwd=1234
  → 正在验证提取码...
  → 发现 8 个文件
  → 转存中... [████████████] 100%
  ✓ 转存完成: /转存文件/资料包2

[3/3] https://pan.quark.cn/s/ghi789
  → 正在获取文件列表...
  → 发现 1 个文件
  → 转存中... [████████████] 100%
  ✓ 转存完成: /转存文件/单个文件.pdf

=================================
✅ 全部完成！
   成功: 3 个链接
   失败: 0 个
   共转存: 24 个文件
=================================
```
