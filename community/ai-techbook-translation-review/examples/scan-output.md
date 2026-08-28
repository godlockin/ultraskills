# 扫描输出示例 (Typical Scan Output)

下面是典型的 `scan_render.py` 输出,来自 maths-cs-ai-compendium 项目实战。

## 案例 1: 完整中文版扫描 (修复模式)

```bash
$ python3 scripts/scan_render.py --root ./zh/ --fix

=== SUMMARY ===
Total files scanned: 169
Files with issues: 32

=== BY TYPE ===
    936  inline_dollar_with_begin    (跨文件,合并修复)
    279  inline_\(\)                (单行 LaTeX 原生)
     23  block_\[\]                 (LaTeX 块级)
      4  mermaid_naked_special      (含 () % <>) 

TOTAL ISSUES: 1242
```

**修复后**:
```bash
$ python3 scripts/scan_render.py --root ./zh/

=== SUMMARY ===
Total files scanned: 169
Files with issues: 0

TOTAL ISSUES: 0
```

## 案例 2: 英文原文扫描 (只读)

```bash
$ python3 scripts/scan_render.py --root ./chapter*/ --target en --read-only

=== SUMMARY ===
Total files scanned: 104
Total md lines: 29528
Mermaid blocks: 0
Files with issues: 0

TOTAL ISSUES: 0
```

**解读**: 英文原版 100% 使用标准 Markdown math 语法,无 mermaid 块。

## 案例 3: 教辅 7 件套审计

```bash
$ python3 scripts/audit_companion.py --root ./zh/教辅 --chapters 25

=== 教辅 7 件套审计 ===

章 | 单页 | 闪卡 | 测试 | 答案 | 思维导图 | 信息图 | 复习大纲 | 总计
01 | ✅62 | ✅18 | ✅19 | ✅85 | ✅145 | ✅6 | ✅160 | 7/7
02 | ✅65 | ✅20 | ✅19 | ✅80 | ✅155 | ✅6 | ✅165 | 7/7
...
25 | ✅70 | ✅25 | ✅19 | ✅100 | ✅200 | ✅7 | ✅190 | 7/7

=== BY TYPE ===
  25/25  单页 proposal (500-800 字)
  25/25  闪卡 (15-25 张)
  25/25  阶段测试题 (15-20 题 × 4 类)
  25/25  测试题答案 (含评分标准)
  25/25  思维导图 (60-100 节点)
  25/25  信息图 (5-8 mermaid)
  25/25  复习大纲 (60-90 分钟复习)

=== TOTAL ===
  175/175  (100.0%)
```

## 案例 4: 翻译对齐度

```bash
$ python3 scripts/audit_translation.py --src ./ --target ./zh/

=== 翻译对齐度审计 ===

章 | 文件 | 行数(src→tgt) | 图片 | 公式 | 问题
01 | 8/8 | 1240→1856 | 35→35 | 124→124 | ✅
02 | 7/7 | 980→1470 | 28→28 | 86→86 | ✅
...
25 | 4/4 | 520→780 | 12→12 | 38→38 | ✅

=== TOTAL: 0 issues across 25 chapters ===
```

## 关键经验

1. **先扫后修**: 不要肉眼检查,扫描器能发现 100+ 隐藏问题
2. **英文作为基线**: 英文版通常 0 错误,可作为质量标准
3. **批量修复**: 同类问题用 `sed`/Python 批量修复,效率 10×
4. **修复后验证**: 必须 re-scan 确认 0 残留
5. **commit 分批**: mermaid / KaTeX / inline / block 4 类分别 commit,便于回溯