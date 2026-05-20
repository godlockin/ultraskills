# 夸克网盘下载工具 - 快速参考

## 一键下载命令

```bash
# 1. 配置链接
echo "https://pan.quark.cn/s/ce476b55ec2a?pwd=7efe3YeNNj" > config/url.txt

# 2. 运行工具
cd ~/working/sourcecode/tools/llm_apps/ultraskills/community/quark-pan-downloader/scripts
python quark.py

# 3. 选择功能:
# → 输入 3 (批量下载)
# → 或输入 1 (先转存到网盘再下载)
```

## 当前任务

**下载目标:**
- 分享链接: https://pan.quark.cn/s/ce476b55ec2a
- 提取码: 7efe3YeNNj
- 内容: 沈弈斐合集
- 保存到: ~/Documents/00_文档/02_doc/videos/沈弈斐/

**状态:**
- ✅ 链接已配置 (config/url.txt)
- ✅ 目标目录已创建
- 🔄 工具运行中（后台）
- ⏳ 等待浏览器登录完成

## 首次登录流程

1. **Playwright 会自动打开 Firefox 浏览器**
2. **在浏览器中登录夸克网盘**（扫码或密码）
3. **不要关闭浏览器**
4. **回到终端按 Enter**
5. Cookie 自动保存，下次无需登录

## 下载完成后

文件默认下载到:
```
scripts/downloads/
```

然后需要手动移动到目标目录:
```bash
mv scripts/downloads/* ~/Documents/00_文档/02_doc/videos/沈弈斐/
```

或修改 quark.py 中的下载路径配置。
