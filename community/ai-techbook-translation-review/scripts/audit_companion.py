#!/usr/bin/env python3
"""
教辅 7 件套完整性审计

检查每章是否齐备 7 类教辅文件:
- 单页 proposal (单页proposal/第{NN}章.md)
- 闪卡 (闪卡/第{NN}章.md)
- 阶段测试题 (阶段测试题/第{NN}章.md)
- 测试题答案 (阶段测试题答案/第{NN}章.md)
- 思维导图 (思维导图/第{NN}章.md)
- 信息图 (信息图/第{NN}章.md)
- 复习大纲 (复习大纲/第{NN}章.md)

Usage:
    python3 audit_companion.py --root ./zh/教辅 --chapters 25
"""

import argparse
import os
import sys


COMPANION_TYPES = [
    ('单页proposal', '单页 proposal (500-800 字)'),
    ('闪卡', '闪卡 (15-25 张)'),
    ('阶段测试题', '阶段测试题 (15-20 题 × 4 类)'),
    ('阶段测试题答案', '测试题答案 (含评分标准)'),
    ('思维导图', '思维导图 (60-100 节点)'),
    ('信息图', '信息图 (5-8 mermaid)'),
    ('复习大纲', '复习大纲 (60-90 分钟复习)'),
]


def pad(n):
    """Zero-pad chapter number: 1 -> 01, 25 -> 25."""
    return str(n).zfill(2)


def audit(root, num_chapters=25):
    """Audit companion completeness. Returns dict of {chapter: {type: (exists, size)}}."""
    result = {}
    for ch in range(1, num_chapters + 1):
        cn = pad(ch)
        result[cn] = {}
        for dirname, desc in COMPANION_TYPES:
            path = os.path.join(root, dirname, f'第{cn}章.md')
            if os.path.exists(path):
                size = os.path.getsize(path)
                line_count = sum(1 for _ in open(path))
                result[cn][dirname] = (True, line_count)
            else:
                result[cn][dirname] = (False, 0)

    return result


def print_audit(result, num_chapters=25):
    """Print formatted audit table."""
    print('=== 教辅 7 件套审计 ===\n')

    # Header
    header = '章 | ' + ' | '.join([c[0][:8] for c in COMPANION_TYPES]) + ' | 总计'
    print(header)
    print('-' * len(header))

    total_files = 0
    expected = num_chapters * len(COMPANION_TYPES)

    for ch in range(1, num_chapters + 1):
        cn = pad(ch)
        row = [cn]
        ch_total = 0
        for dirname, _ in COMPANION_TYPES:
            exists, lines = result[cn][dirname]
            status = '✅' if exists and lines > 50 else ('⚠️' if exists else '❌')
            row.append(f'{status}{lines}')
            if exists:
                total_files += 1
        ch_count = sum(1 for exists, _ in result[cn].values() if exists)
        row.append(f'{ch_count}/{len(COMPANION_TYPES)}')
        print(' | '.join(row))

    print('-' * len(header))

    # By type stats
    print('\n=== BY TYPE ===')
    for dirname, desc in COMPANION_TYPES:
        ok = sum(1 for ch in result.values() if ch[dirname][0])
        print(f'  {ok}/{num_chapters}  {desc}')

    print(f'\n=== TOTAL ===')
    print(f'  {total_files}/{expected}  ({total_files/expected*100:.1f}%)')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Audit companion 7-piece completeness')
    parser.add_argument('--root', required=True, help='教辅 root directory')
    parser.add_argument('--chapters', type=int, default=25, help='Total chapter count')
    args = parser.parse_args()

    result = audit(args.root, args.chapters)
    print_audit(result, args.chapters)