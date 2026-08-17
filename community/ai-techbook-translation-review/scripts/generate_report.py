#!/usr/bin/env python3
"""
合并自动扫描结果和 4 角色评审,生成综合 Translation Review Report

Usage:
    python3 generate_report.py \
      --project "Maths-CS-AI Compendium 中文版" \
      --scan-results ./scan-results/ \
      --reviews ./reviews/ \
      --output ./translation-review-report.md
"""

import argparse
import json
import os
from datetime import datetime


# 评分门槛
THRESHOLD_MUST = 9.0
THRESHOLD_BONUS = 7.0
THRESHOLD_OVERALL = 8.0

# 必须项权重 (60% 总权重内部分配；归一化后用于 0..10 评分)
MUST_WEIGHTS = {
    'terminology': 0.25,
    'technical': 0.25,
    'rendering': 0.20,
    'completeness': 0.15,
}
MUST_WEIGHT_TOTAL = sum(MUST_WEIGHTS.values())
if MUST_WEIGHT_TOTAL <= 0:
    raise ValueError('MUST_WEIGHTS must have a positive total')
NORMALIZED_MUST_WEIGHTS = {
    dim: weight / MUST_WEIGHT_TOTAL for dim, weight in MUST_WEIGHTS.items()
}

# 加分项权重 (内部权重应加和 = 1.0)
BONUS_WEIGHTS = {
    'teaching': 1.0,  # 当前只有 1 个加分维度
}

# 维度 → 中文标签
DIM_LABELS = {
    'terminology': '术语准确',
    'technical': '公式/代码/数据',
    'rendering': '渲染正确',
    'completeness': '章节/段落完整',
    'teaching': '教辅/排版/深度',
}


def load_scan_results(scan_dir):
    """Load auto-scan results from JSON files."""
    results = {}
    if not os.path.isdir(scan_dir):
        return results
    for f in sorted(os.listdir(scan_dir)):
        if f.endswith('.json'):
            try:
                with open(os.path.join(scan_dir, f)) as fp:
                    data = json.load(fp)
                key = f.replace('.json', '')
                results[key] = data
            except Exception as e:
                print(f'WARN: failed to load {f}: {e}')
    return results


def load_reviews(reviews_dir):
    """Load 4 role review markdown files."""
    reviews = []
    if not os.path.isdir(reviews_dir):
        return reviews
    for f in sorted(os.listdir(reviews_dir)):
        if f.endswith('.md'):
            with open(os.path.join(reviews_dir, f)) as fp:
                content = fp.read()
            reviews.append({'role': f.replace('.md', ''), 'content': content})
    return reviews


def calc_score(reviews, dim_name):
    """Extract score for a dimension; missing critical reviews are invalid input."""
    import re
    for review in reviews:
        if dim_name in review['role'].lower():
            match = re.search(r'评分[:\s]*(\d+\.?\d*)\s*/\s*10', review['content'])
            if not match:
                raise ValueError(f'review {review["role"]!r} has no score')
            score = float(match.group(1))
            if not 0 <= score <= 10:
                raise ValueError(f'review {review["role"]!r} score outside 0..10')
            return score, {
                'critical': review['content'].count('🔴'),
                'important': review['content'].count('🟡'),
                'minor': review['content'].count('🟢'),
            }
    raise ValueError(f'missing review for required dimension {dim_name!r}')


def scan_failures(scan_results):
    """Return scan findings that make the critical review non-passing.

    Scanner JSON formats vary, so inspect conventional failure fields while
    ignoring normal numeric statistics. Explicit critical/error findings and
    false/failed statuses are blocking; bonus results are never used here.
    """
    failures = []

    def visit(value, path='scan'):
        if isinstance(value, dict):
            for key, child in value.items():
                key_lower = str(key).lower()
                child_path = f'{path}.{key}'
                if key_lower in {'critical', 'critical_errors', 'errors', 'issues'}:
                    if child not in (None, [], {}, '', 0, False):
                        failures.append((child_path, child))
                elif key_lower in {'failed', 'failure', 'pass', 'passed', 'ok'}:
                    if child is False or (key_lower in {'failed', 'failure'} and child not in (None, [], {}, '', 0, False)):
                        failures.append((child_path, child))
                elif key_lower == 'status' and str(child).lower() in {'fail', 'failed', 'error'}:
                    failures.append((child_path, child))
                visit(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f'{path}[{index}]')

    visit(scan_results)
    return failures


def generate_report(project_name, scan_results, reviews):
    """Generate full Translation Review Report."""
    lines = []

    # Header
    lines.append('# Translation Review Report')
    lines.append('')
    lines.append(f'**项目**: {project_name}')
    lines.append(f'**评审日期**: {datetime.now().strftime("%Y-%m-%d")}')
    lines.append('')
    lines.append('---')
    lines.append('')

    # 1. 必须项评分
    must_scores = {}
    must_issues_total = {'critical': 0, 'important': 0, 'minor': 0}
    for dim in ['terminology', 'technical', 'rendering', 'completeness']:
        score, issues = calc_score(reviews, dim)
        must_scores[dim] = score
        for k, v in issues.items():
            must_issues_total[k] += v

    must_total = sum(must_scores[d] * NORMALIZED_MUST_WEIGHTS[d] for d in NORMALIZED_MUST_WEIGHTS)

    scan_issues = scan_failures(scan_results)

    # 2. 加分项评分（缺失时记 0；加分项不构成独立通过门槛）
    bonus_scores = {}
    for dim in ['teaching']:
        try:
            score, _ = calc_score(reviews, dim)
        except ValueError:
            score = 0.0
        bonus_scores[dim] = score
    bonus_total = sum(bonus_scores[d] * BONUS_WEIGHTS[d] for d in BONUS_WEIGHTS)

    # 综合分仅供报告参考；通过由必须项分数、critical review、自动扫描共同决定。
    overall = must_total * 0.6 + bonus_total * 0.4
    passed = (must_total >= THRESHOLD_MUST
              and must_issues_total['critical'] == 0
              and not scan_issues)

    # 综合评分表
    lines.append('## 📊 综合评分 (Overall Score)')
    lines.append('')
    lines.append('| 维度 | 权重 | 得分 | 门槛 | 状态 |')
    lines.append('|------|------|------|------|------|')
    lines.append(f'| **必须项** | 60% | **{must_total:.1f} / 10** | ≥ {THRESHOLD_MUST} | '
                 f'{"✅" if must_total >= THRESHOLD_MUST else "❌"} |')
    lines.append(f'| **加分项** | 40% | **{bonus_total:.1f} / 10** | ≥ {THRESHOLD_BONUS} | '
                 f'{"✅" if bonus_total >= THRESHOLD_BONUS else "❌"} |')
    lines.append(f'| **综合** | 100% | **{overall:.1f} / 10** | ≥ {THRESHOLD_OVERALL} | '
                 f'{"✅" if passed else "❌"} |')
    lines.append('')
    lines.append(f'**结论**: {"✅ **通过**" if passed else "❌ **不通过**"} '
                 f'(必须项 {must_total:.1f} {"≥" if must_total >= THRESHOLD_MUST else "<"} {THRESHOLD_MUST})')
    lines.append('')
    lines.append('---')
    lines.append('')

    # 必须项详情
    lines.append('## 🔴 必须项 (Critical, 60%)')
    lines.append('')
    lines.append('> 决定翻译是否可用,任何 critical 错误都需修复后才能通过。')
    lines.append('')

    for dim in ['terminology', 'technical', 'rendering', 'completeness']:
        label = DIM_LABELS[dim]
        score = must_scores[dim]
        lines.append(f'### {dim.title()}: {label} — {score:.1f} / 10')
        lines.append('')
        # Find review content
        review_content = None
        for r in reviews:
            if dim in r['role'].lower():
                review_content = r['content']
                break
        if review_content:
            # Extract just the issues section (skip header)
            lines.append('```markdown')
            # Truncate to relevant section
            lines.append(review_content[:3000])
            lines.append('```')
        lines.append('')

    # 必须项总分
    lines.append(f'**必须项总分**: **{must_total:.1f} / 10**')
    lines.append('')
    lines.append(f'必修 Critical: **{must_issues_total["critical"]}** 项 / '
                 f'Important: {must_issues_total["important"]} 项 / '
                 f'Minor: {must_issues_total["minor"]} 项')
    lines.append('')
    lines.append('### 自动扫描结果')
    lines.append('')
    lines.append(f'- 扫描文件: **{len(scan_results)}**')
    lines.append(f'- 阻断扫描发现: **{len(scan_issues)}**')
    if scan_issues:
        for path, finding in scan_issues:
            lines.append(f'- ❌ `{path}`: `{finding}`')
    else:
        lines.append('- ✅ 未发现 critical 扫描失败')
    lines.append('')
    lines.append('---')
    lines.append('')

    # 加分项详情
    lines.append('## 🟢 加分项 (Bonus, 40%)')
    lines.append('')
    lines.append('> 锦上添花,不决定通过,但能体现翻译深度。')
    lines.append('')

    for dim, score in bonus_scores.items():
        label = DIM_LABELS[dim]
        lines.append(f'### {dim.title()}: {label} — {score:.1f} / 10')
        lines.append('')
        for r in reviews:
            if dim in r['role'].lower():
                lines.append('```markdown')
                lines.append(r['content'][:2000])
                lines.append('```')
                break
        lines.append('')

    lines.append(f'**加分项总分**: **{bonus_total:.1f} / 10**')
    lines.append('')
    lines.append('---')
    lines.append('')

    # 修复优先级
    lines.append('## 📋 修复优先级清单')
    lines.append('')

    critical_count = must_issues_total['critical']
    important_count = must_issues_total['important']
    minor_count = must_issues_total['minor']

    lines.append(f'### 必修 (Critical) — 必须 100% 修复 ({critical_count} 项)')
    lines.append('')
    lines.append('> 详见各角色评审报告的 🔴 部分')
    lines.append('')
    lines.append(f'### 建议修 (Important) ({important_count} 项)')
    lines.append('')
    lines.append('> 详见各角色评审报告的 🟡 部分')
    lines.append('')
    lines.append(f'### 可选 (Minor) ({minor_count} 项)')
    lines.append('')
    lines.append('> 详见各角色评审报告的 🟢 部分')
    lines.append('')
    lines.append('---')
    lines.append('')

    # 总结
    lines.append('## 🎯 总结')
    lines.append('')
    lines.append('| 状态 | 项目 |')
    lines.append('|------|------|')
    crit_count = must_issues_total['critical']
    crit_str = '= 0' if crit_count == 0 else f'= {crit_count}'
    lines.append(f'| {"✅" if crit_count == 0 else "❌"} '
                 f'| 必须项 critical {crit_str} |')
    lines.append(f'| {"✅" if bonus_total >= THRESHOLD_BONUS else "❌"} '
                 f'| 加分项 ≥ {THRESHOLD_BONUS} (当前 {bonus_total:.1f}) |')
    lines.append(f'| {"✅" if passed else "❌"} '
                 f'| 综合 ≥ {THRESHOLD_OVERALL} (当前 {overall:.1f}) |')
    lines.append('')

    if passed:
        lines.append(f'**最终结论**: ✅ **翻译通过**,可进入出版阶段。')
    else:
        reasons = []
        if must_total < THRESHOLD_MUST:
            reasons.append(f'必须项 {must_total:.1f} < {THRESHOLD_MUST}')
        if must_issues_total['critical']:
            reasons.append(f'评审 critical {must_issues_total["critical"]} 项')
        if scan_issues:
            reasons.append(f'自动扫描失败 {len(scan_issues)} 项')
        lines.append(f'**最终结论**: ❌ **需修复后重新 review** ({", ".join(reasons)})')
    lines.append('')
    lines.append('---')
    lines.append('')

    # 附件
    lines.append('## 📎 附件')
    lines.append('')
    lines.append('- 渲染扫描报告: `scan-output.md`')
    lines.append('- 教辅审计报告: `companion-audit.md`')
    lines.append('- 翻译对齐报告: `translation-alignment.md`')
    lines.append('- 4 角色评审: `reviews/*.md`')
    lines.append('')

    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate Translation Review Report')
    parser.add_argument('--project', required=True, help='Project name')
    parser.add_argument('--scan-results', default='./scan-results/', help='Scan results dir')
    parser.add_argument('--reviews', default='./reviews/', help='Reviews dir')
    parser.add_argument('--output', required=True, help='Output report path')
    args = parser.parse_args()

    scan_results = load_scan_results(args.scan_results)
    reviews = load_reviews(args.reviews)

    if not reviews:
        raise ValueError('no reviews found; four required critical reviews must be supplied')

    report = generate_report(args.project, scan_results, reviews)

    with open(args.output, 'w') as fp:
        fp.write(report)

    print(f'✅ Report generated: {args.output}')
    print(f'   {len(report)} chars, {len(reviews)} reviews, {len(scan_results)} scan results')


if __name__ == '__main__':
    main()