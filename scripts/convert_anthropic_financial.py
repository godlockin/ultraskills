#!/usr/bin/env python3
"""
Convert Anthropic Financial Services skills to UltraSkills format

Usage:
    python3 convert_anthropic_financial.py --input /tmp/financial-services/plugins/vertical-plugins --output external/anthropic-financial-services
"""

import argparse
import re
import shutil
import yaml
from pathlib import Path


def extract_description_from_content(content):
    """从无frontmatter的skill中提取description"""
    lines = content.splitlines()

    # 查找 description: 行
    for i, line in enumerate(lines):
        if line.startswith('description:'):
            # 提取多行 description（直到遇到 ## 标题）
            desc_lines = [line.replace('description:', '').strip()]

            for j in range(i + 1, len(lines)):
                if lines[j].startswith('##') or lines[j].startswith('---'):
                    break
                if lines[j].strip():
                    desc_lines.append(lines[j].strip())

            return ' '.join(desc_lines)

    # 如果没找到 description:，返回第一段
    for i, line in enumerate(lines[1:], 1):  # 跳过标题
        if line.strip() and not line.startswith('#'):
            return line.strip()

    return "No description available"


def infer_tags(skill_path, vertical):
    """根据路径和内容推断tags"""
    skill_name = skill_path.parent.name

    # 基础 tags
    tags = [vertical, 'finance']

    # 添加技能名称相关tag
    tags.append(skill_name)

    # 读取内容推断额外tags
    with open(skill_path) as f:
        content = f.read().lower()

    # 关键词匹配
    keyword_tags = {
        'excel': 'excel',
        'spreadsheet': 'excel',
        'model': 'modeling',
        'valuation': 'valuation',
        'dcf': 'dcf',
        'lbo': 'lbo',
        'comps': 'comparable-analysis',
        'earnings': 'earnings',
        'research': 'research',
        'analysis': 'analysis',
        'screening': 'screening',
        'diligence': 'due-diligence',
        'portfolio': 'portfolio',
        'kyc': 'compliance',
        'reconcile': 'accounting',
    }

    for keyword, tag in keyword_tags.items():
        if keyword in content and tag not in tags:
            tags.append(tag)
            if len(tags) >= 9:  # 最多9个tags
                break

    return tags


def convert_skill(skill_path, vertical):
    """转换单个skill"""
    with open(skill_path) as f:
        content = f.read()

    # 检查是否已有 frontmatter
    fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)

    if fm_match:
        # 已有 frontmatter，补充缺失字段
        try:
            fm = yaml.safe_load(fm_match.group(1))
        except:
            fm = {}

        # 补充 version
        if 'version' not in fm:
            fm['version'] = '1.0.0'

        # 补充 tags
        if 'tags' not in fm or not fm['tags']:
            fm['tags'] = infer_tags(skill_path, vertical)
        elif 'finance' not in fm['tags']:
            fm['tags'].insert(0, 'finance')

        # 确保 name 存在
        if 'name' not in fm:
            fm['name'] = skill_path.parent.name

        # 重建 frontmatter
        new_fm = yaml.dump(fm, sort_keys=False, allow_unicode=True, width=1000)
        content = f"---\n{new_fm}---\n" + content[fm_match.end():]

    else:
        # 无 frontmatter，构造新的
        title = content.splitlines()[0].lstrip('# ').strip()
        description = extract_description_from_content(content)
        skill_name = skill_path.parent.name

        fm = {
            'name': skill_name,
            'description': description,
            'version': '1.0.0',
            'tags': infer_tags(skill_path, vertical)
        }

        new_fm = yaml.dump(fm, sort_keys=False, allow_unicode=True, width=1000)

        # 移除原 description: 行
        content = re.sub(r'^description:\s*.+?(?=\n##)', '', content, flags=re.DOTALL | re.M)

        content = f"---\n{new_fm}---\n\n{content}"

    return content


def convert_all_skills(input_dir, output_dir):
    """批量转换所有skills"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # 查找所有 vertical plugins
    verticals = [d for d in input_path.iterdir() if d.is_dir() and (d / 'skills').exists()]

    stats = {
        'total': 0,
        'converted': 0,
        'copied_as_is': 0,
        'failed': 0
    }

    for vertical_dir in verticals:
        vertical_name = vertical_dir.name
        skills_dir = vertical_dir / 'skills'

        if not skills_dir.exists():
            continue

        print(f"\n📂 Processing: {vertical_name}/")

        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / 'SKILL.md'
            if not skill_md.exists():
                continue

            stats['total'] += 1
            skill_name = skill_dir.name

            try:
                # 转换 SKILL.md
                converted_content = convert_skill(skill_md, vertical_name)

                # 创建输出目录
                out_skill_dir = output_path / skill_name
                out_skill_dir.mkdir(parents=True, exist_ok=True)

                # 写入转换后的 SKILL.md
                with open(out_skill_dir / 'SKILL.md', 'w') as f:
                    f.write(converted_content)

                # 复制 references/ 和 examples/（如果有）
                for subdir in ['references', 'examples', 'templates']:
                    src_subdir = skill_dir / subdir
                    if src_subdir.exists():
                        dst_subdir = out_skill_dir / subdir
                        if dst_subdir.exists():
                            shutil.rmtree(dst_subdir)
                        shutil.copytree(src_subdir, dst_subdir)

                stats['converted'] += 1
                print(f"  ✅ {skill_name}")

            except Exception as e:
                stats['failed'] += 1
                print(f"  ❌ {skill_name}: {e}")

    return stats


def generate_readme(output_dir, stats):
    """生成README"""
    readme = f"""# Anthropic Financial Services Skills

> 从 Anthropic 官方 financial-services 项目提取并转换为 UltraSkills 格式

**原项目**: https://github.com/anthropics/financial-services
**Stars**: 17.8k⭐
**License**: Apache-2.0
**Last Synced**: 2026-05-08

---

## 转换说明

- **原始格式**: Claude Code Plugin
- **转换格式**: UltraSkills (YAML frontmatter)
- **转换内容**: {stats['converted']} skills
- **排除内容**: MCP 连接器配置、Agents 配置、Managed Agent 模板

---

## Skills 分类

### Financial Analysis（金融分析核心）
- comps-analysis - 可比公司分析
- dcf-model - DCF 估值模型
- lbo-model - LBO 杠杆收购模型
- 3-statement-model - 三表财务模型
- audit-xls - Excel 模型审计
- competitive-analysis - 竞争分析
- ... 共13个

### Investment Banking（投资银行）
- cim-builder - CIM 文档构建
- teaser - 匿名公司简介
- buyer-list - 买方名单生成
- merger-model - 并购分析模型
- pitch-deck - 融资路演PPT
- ... 共9个

### Private Equity（私募股权）
- deal-sourcing - 交易采购
- dd-checklist - 尽调清单
- ic-memo - 投委会备忘录
- unit-economics - 单位经济学
- portfolio-monitoring - 投后监控
- ai-readiness - AI 就绪度评估
- ... 共10个

### Equity Research（股权研究）
- earnings-analysis - 财报分析
- initiating-coverage - 覆盖启动报告
- model-update - 模型更新
- sector-overview - 行业概览
- ... 共9个

### Wealth Management（财富管理）
- financial-plan - 财务规划
- portfolio-rebalance - 组合再平衡
- tax-loss-harvesting - 税损收割
- ... 共6个

### Fund Admin（基金管理）
- gl-reconciler - 总账对账
- month-end-closer - 月结
- valuation-reviewer - 估值审核
- ... 共6个

### Operations（运营合规）
- kyc-screener - KYC 筛查
- ... 共2个

---

## 使用说明

### 前置条件

大部分 skills 设计为与 MCP 数据连接器配合使用（Daloopa/FactSet/Morningstar等）。

**无MCP环境**下的使用方式：
1. 手动提供数据（CSV/Excel文件）
2. 使用公开数据源（Yahoo Finance/SEC EDGAR）
3. 聚焦方法论学习（不依赖实时数据）

### 触发示例

```
"帮我做个可比公司分析"          → comps-analysis
"DCF估值这个公司"               → dcf-model
"分析这份财报"                  → earnings-analysis
"写个投委会备忘录"              → ic-memo
"评估客户的单位经济学"          → unit-economics
```

---

## 与 UltraSkills 既有内容对比

| 类别 | Anthropic Financial | UltraSkills 既有 | 重叠度 |
|------|---------------------|------------------|--------|
| 金融建模 | 13 skills | 0 | 0% |
| 投行/PE | 19 skills | 0 | 0% |
| 股权研究 | 9 skills | 0 | 0% |
| 财富管理 | 6 skills | 0 | 0% |
| 会计/合规 | 8 skills | 0 | 0% |

**结论**: 完全填补空白，0重叠。

---

## 维护

- **上游同步**: 每月检查 anthropics/financial-services 更新
- **本地改进**: 可基于用户反馈调整（不影响上游）
- **Arena 评测**: 每次同步后重跑

---

**Converted**: {stats['converted']} skills
**Failed**: {stats['failed']} skills
**Conversion Date**: 2026-05-08
"""

    with open(Path(output_dir) / 'README.md', 'w') as f:
        f.write(readme)


def main():
    parser = argparse.ArgumentParser(description='Convert Anthropic Financial Services skills')
    parser.add_argument('--input', required=True, help='Input directory (vertical-plugins)')
    parser.add_argument('--output', required=True, help='Output directory')

    args = parser.parse_args()

    print("=" * 80)
    print("Anthropic Financial Services → UltraSkills 转换器")
    print("=" * 80)

    # 转换
    stats = convert_all_skills(args.input, args.output)

    # 生成 README
    generate_readme(args.output, stats)

    # 总结
    print("\n" + "=" * 80)
    print("转换完成")
    print("=" * 80)
    print(f"总计: {stats['total']} skills")
    print(f"✅ 成功: {stats['converted']} skills")
    print(f"❌ 失败: {stats['failed']} skills")
    print(f"\n输出目录: {args.output}")
    print(f"README: {args.output}/README.md")

    if stats['failed'] > 0:
        print(f"\n⚠️  {stats['failed']} skills 转换失败，需手动检查")

    return 0 if stats['failed'] == 0 else 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
