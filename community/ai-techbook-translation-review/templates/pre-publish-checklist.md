# 出版前检查清单 (Pre-Publish Checklist)

> 用于技术图书出版前的 30 项强制检查。

## 📋 翻译质量 (10 项)

- [ ] **T1**: 25/25 章节翻译完成
- [ ] **T2**: 公式 100% 保留 (原文 `$...$` `$$...$$` 内 LaTeX 源码未改)
- [ ] **T3**: 图片路径正确 (相对路径或绝对路径)
- [ ] **T4**: 链接保留 (内部链接 / 外部 URL)
- [ ] **T5**: 代码块语法高亮正确
- [ ] **T6**: 术语一致 (跨章术语统一,无混用)
- [ ] **T7**: 数据时效 (2024-2026 模型/数据)
- [ ] **T8**: 中文标点规范 (全角标点正确使用)
- [ ] **T9**: 段落对齐 (避免过长/过短段落)
- [ ] **T10**: 中文语法通顺

## 🎨 渲染质量 (8 项)

- [ ] **R1**: 0 mermaid 裸 label (含 () % <> 等特殊字符未加引号)
- [ ] **R2**: 0 mermaid 子图不匹配 (subgraph/end 配对)
- [ ] **R3**: 0 mermaid 含 `$` 字符 (mermaid 不渲染 KaTeX)
- [ ] **R4**: 0 KaTeX 函数名下标无 `{}` (e.g. `f_\max` 必须 `f_{\max}`)
- [ ] **R5**: 0 KaTeX 大括号不平衡
- [ ] **R6**: 0 inline `\(...\)` LaTeX 原生语法 (用 `$...$`)
- [ ] **R7**: 0 inline `\begin{pmatrix}` (用块级 `$$...$$`)
- [ ] **R8**: 0 `\[...\]` 块级 (用 `$$...$$`)

## 📚 教辅完整性 (4 项)

- [ ] **C1**: 25/25 章节单页 proposal
- [ ] **C2**: 25/25 章节闪卡
- [ ] **C3**: 25/25 章节阶段测试题 + 答案
- [ ] **C4**: 25/25 章节思维导图 + 信息图 + 复习大纲

## 🏛️ 出版就绪 (8 项)

- [ ] **P1**: 前言 (Preface) 齐备
- [ ] **P2**: 致谢 (Acknowledgments) 齐备
- [ ] **P3**: 勘误表 (Errata) 维护中
- [ ] **P4**: 参考文献 (150+ 条)
- [ ] **P5**: 索引 (主题索引)
- [ ] **P6**: Pandoc 编译通过 (xelatex)
- [ ] **P7**: 中文字体嵌入 (XeCJK + Source Han Serif)
- [ ] **P8**: PDF 文件大小合理 (< 100 MB)

## 执行检查

```bash
# 1. 渲染扫描 (R1-R8)
python3 scripts/scan_render.py --root ./zh/ --fix

# 2. 教辅审计 (C1-C4)
python3 scripts/audit_companion.py --root ./zh/教辅 --chapters 25

# 3. 翻译对齐 (T1-T10)
python3 scripts/audit_translation.py --src ./ --target ./zh/

# 4. Pandoc 编译 (P6-P8)
pandoc zh/前言.md zh/第*章/*.md zh/致谢.md \
  -o build/book.pdf \
  --pdf-engine=xelatex \
  --template=zh/templates/zh-book.tex \
  --toc --toc-depth=3
```

## 通过门槛

- 30 项全部 ✅ 才能进入出版阶段
- 任何 Critical 问题 (R1-R8 任一) 必须 100% 解决
- Important 问题 (T1-T10, C1-C4) 可保留 1-2 项,但需在勘误表中标注