#!/usr/bin/env python3
"""提取高优先级重复skill对"""
import re
from pathlib import Path

def extract_high_priority_duplicates(report_file: str = "/tmp/cluster_duplicates_report.txt"):
    """提取需要立即处理的重复"""
    text = Path(report_file).read_text(encoding='utf-8')

    # 正则提取重复块
    pattern = r'\[(\d+)\] 相似度: (0\.\d+)\s+• ([\w-]+)\s+(.+?)\s+• ([\w-]+)\s+(.+?)原因: (.+?)(?=\n\n|\n   \[|\Z)'
    matches = re.findall(pattern, text, re.DOTALL)

    duplicates = []
    for match in matches:
        idx, score, id1, desc1, id2, desc2, reason = match
        score = float(score)

        # 过滤条件
        if score >= 0.7:
            duplicates.append({
                'score': score,
                'id1': id1.strip(),
                'id2': id2.strip(),
                'desc1': desc1.strip()[:100],
                'desc2': desc2.strip()[:100],
                'reason': reason.strip()
            })

    # 按相似度排序
    duplicates.sort(key=lambda x: x['score'], reverse=True)

    # 输出
    print("=" * 80)
    print(f"🔥 高优先级重复 (相似度 ≥ 0.7) - 共{len(duplicates)}组")
    print("=" * 80)
    print()

    seen_pairs = set()
    unique_count = 0

    for dup in duplicates:
        # 去重(id1+id2或id2+id1视为同一对)
        pair = tuple(sorted([dup['id1'], dup['id2']]))
        if pair in seen_pairs:
            continue
        seen_pairs.add(pair)
        unique_count += 1

        print(f"{unique_count}. [{dup['score']:.2f}] {dup['id1']} ↔ {dup['id2']}")
        print(f"   原因: {dup['reason'][:150]}")
        print()

        if unique_count >= 30:  # 只显示Top 30
            break

    print("=" * 80)
    print("💡 建议操作:")
    print("   1. 相似度0.99-1.0 (完全重复): 立即删除其中之一")
    print("   2. 相似度0.8-0.98: 比对功能,保留最完善版本")
    print("   3. 相似度0.7-0.79: 明确差异,更新描述避免混淆")
    print()
    print("   删除命令: python3 devops/skill-manager/scripts/delete_skill.py <id>")
    print("=" * 80)

if __name__ == '__main__':
    extract_high_priority_duplicates()
