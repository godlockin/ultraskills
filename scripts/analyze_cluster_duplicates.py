#!/usr/bin/env python3
"""
Cluster重复分析器 - 识别功能重叠的skills
"""
import json
from collections import defaultdict
from pathlib import Path
from typing import List, Dict, Set, Tuple

def load_clusters(path: str = "devops/skill-arena/clusters.json") -> dict:
    """加载clusters数据"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_similarity(skill1: dict, skill2: dict) -> Tuple[float, List[str]]:
    """
    计算两个skill的相似度
    返回: (相似度分数 0-1, 重叠特征列表)
    """
    reasons = []
    score = 0.0

    # 1. 关键词重叠 (权重50%)
    kw1 = set(skill1.get('keywords', []))
    kw2 = set(skill2.get('keywords', []))
    if kw1 and kw2:
        overlap = kw1 & kw2
        if overlap:
            ratio = len(overlap) / min(len(kw1), len(kw2))
            score += ratio * 0.5
            if ratio > 0.3:
                reasons.append(f"关键词重叠{len(overlap)}个: {', '.join(list(overlap)[:5])}")

    # 2. Tag重叠 (权重30%)
    tags1 = set(skill1.get('tags', []))
    tags2 = set(skill2.get('tags', []))
    if tags1 and tags2:
        overlap = tags1 & tags2
        if overlap and 'community' not in overlap:  # 排除泛用tag
            ratio = len(overlap) / min(len(tags1), len(tags2))
            score += ratio * 0.3
            if ratio > 0.5:
                reasons.append(f"Tag重叠: {', '.join(overlap)}")

    # 3. 描述相似度 (简单词频,权重20%)
    desc1_words = set(skill1.get('description', '').lower().split())
    desc2_words = set(skill2.get('description', '').lower().split())
    if desc1_words and desc2_words:
        overlap = desc1_words & desc2_words
        # 过滤停用词
        stopwords = {'a', 'an', 'the', 'in', 'on', 'at', 'to', 'for', 'with', 'from', 'use', 'when'}
        overlap = overlap - stopwords
        if len(overlap) > 3:
            ratio = len(overlap) / min(len(desc1_words), len(desc2_words))
            score += ratio * 0.2
            if ratio > 0.3:
                reasons.append(f"描述相似: {len(overlap)}个共同词")

    return score, reasons

def analyze_cluster_duplicates(cluster: dict, threshold: float = 0.4) -> List[dict]:
    """
    分析单个cluster内的重复
    threshold: 相似度阈值(0-1),超过视为重复
    """
    skills = cluster['skills']
    duplicates = []

    for i, skill1 in enumerate(skills):
        for skill2 in skills[i+1:]:
            score, reasons = calculate_similarity(skill1, skill2)

            if score >= threshold:
                duplicates.append({
                    'skill1': {
                        'id': skill1['id'],
                        'name': skill1['name'],
                        'desc': skill1.get('description', '')[:80] + '...'
                    },
                    'skill2': {
                        'id': skill2['id'],
                        'name': skill2['name'],
                        'desc': skill2.get('description', '')[:80] + '...'
                    },
                    'similarity': round(score, 2),
                    'reasons': reasons
                })

    return duplicates

def generate_report(data: dict, output_file: str = None):
    """生成重复分析报告"""
    clusters = data['clusters']

    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("🔍 Cluster 重复分析报告")
    report_lines.append("=" * 80)
    report_lines.append(f"分析时间: {data.get('updated_at', 'N/A')}")
    report_lines.append(f"总cluster数: {len(clusters)}")
    report_lines.append("")

    total_duplicates = 0
    high_risk_clusters = []

    for cluster in clusters:
        cluster_id = cluster['id']
        cluster_name = cluster['name']
        skill_count = len(cluster['skills'])

        # 分析重复
        duplicates = analyze_cluster_duplicates(cluster, threshold=0.4)

        if duplicates:
            total_duplicates += len(duplicates)

            report_lines.append("-" * 80)
            report_lines.append(f"📦 Cluster: {cluster_name} ({cluster_id})")
            report_lines.append(f"   描述: {cluster['description']}")
            report_lines.append(f"   技能数: {skill_count}")
            report_lines.append(f"   🔴 发现 {len(duplicates)} 组重复")
            report_lines.append("")

            # 记录高风险cluster
            if len(duplicates) >= 3:
                high_risk_clusters.append({
                    'name': cluster_name,
                    'count': len(duplicates),
                    'total_skills': skill_count
                })

            # 输出每组重复
            for idx, dup in enumerate(duplicates, 1):
                report_lines.append(f"   [{idx}] 相似度: {dup['similarity']}")
                report_lines.append(f"       • {dup['skill1']['id']}")
                report_lines.append(f"         {dup['skill1']['desc']}")
                report_lines.append(f"       • {dup['skill2']['id']}")
                report_lines.append(f"         {dup['skill2']['desc']}")
                if dup['reasons']:
                    report_lines.append(f"       原因: {'; '.join(dup['reasons'])}")
                report_lines.append("")

    # 汇总
    report_lines.append("=" * 80)
    report_lines.append("📊 汇总")
    report_lines.append("=" * 80)
    report_lines.append(f"总重复组数: {total_duplicates}")
    report_lines.append(f"高风险cluster (≥3组重复): {len(high_risk_clusters)}")
    report_lines.append("")

    if high_risk_clusters:
        report_lines.append("⚠️  高风险Cluster排名:")
        for item in sorted(high_risk_clusters, key=lambda x: x['count'], reverse=True):
            report_lines.append(f"   • {item['name']}: {item['count']}组重复 (共{item['total_skills']}个skill)")
        report_lines.append("")

    # 建议
    report_lines.append("💡 Consolidation建议:")
    report_lines.append("   1. 优先处理高风险cluster")
    report_lines.append("   2. 相似度>0.7: 考虑合并为单个skill")
    report_lines.append("   3. 相似度0.4-0.7: 明确差异化,更新描述")
    report_lines.append("   4. 使用命令删除: python3 devops/skill-manager/scripts/delete_skill.py <id>")
    report_lines.append("=" * 80)

    report_text = "\n".join(report_lines)

    # 输出到文件或stdout
    if output_file:
        Path(output_file).write_text(report_text, encoding='utf-8')
        print(f"✅ 报告已保存: {output_file}")
    else:
        print(report_text)

    return report_text

def main():
    import sys

    # 加载数据
    clusters_file = sys.argv[1] if len(sys.argv) > 1 else "devops/skill-arena/clusters.json"
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"📂 加载: {clusters_file}")
    data = load_clusters(clusters_file)

    # 生成报告
    generate_report(data, output_file)

if __name__ == '__main__':
    main()
