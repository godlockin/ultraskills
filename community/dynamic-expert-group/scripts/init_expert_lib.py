#!/usr/bin/env python3
"""
初始化专家库脚本

扫描 references/experts/ 目录下的所有专家定义，
生成索引文件供后续使用。
"""

import os
import re
import json
import yaml
from pathlib import Path

SKILL_ROOT = Path(__file__).parent.parent
EXPERTS_DIR = SKILL_ROOT / "references" / "experts"
OUTPUT_FILE = SKILL_ROOT / "references" / "experts" / "all_experts.json"

def parse_expert_from_markdown(content: str, file_path: Path) -> dict | None:
    """从 markdown 文件中解析专家定义"""
    # 提取 yaml 代码块
    yaml_match = re.search(r"```yaml\n(.*?)```", content, re.DOTALL)
    if not yaml_match:
        return None

    try:
        expert = yaml.safe_load(yaml_match.group(1))
        expert['_source_file'] = str(file_path.relative_to(SKILL_ROOT))
        return expert
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None


def scan_experts() -> list[dict]:
    """扫描所有专家文件"""
    experts = []

    for md_file in EXPERTS_DIR.rglob("*.md"):
        # 跳过索引文件
        if md_file.stem in ['index_by_domain', 'index_by_level']:
            continue

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 支持多专家文件（目录下的 index.md）
        # 也支持单专家文件（直接 .md 文件）

        # 查找所有 yaml 代码块
        yaml_blocks = re.findall(r"```yaml\n(.*?)```", content, re.DOTALL)

        for yaml_block in yaml_blocks:
            try:
                expert = yaml.safe_load(yaml_block)
                if expert and 'id' in expert:
                    expert['_source_file'] = str(md_file.relative_to(SKILL_ROOT))
                    experts.append(expert)
            except Exception as e:
                print(f"Error parsing yaml in {md_file}: {e}")

    return experts


def build_indexes(experts: list[dict]) -> dict:
    """构建索引"""
    by_domain = {}
    by_level = {}
    by_keyword = {}
    by_id = {}

    for expert in experts:
        # by_id
        by_id[expert['id']] = expert

        # by_domain
        domain = expert.get('domain', 'unknown')
        if domain not in by_domain:
            by_domain[domain] = []
        by_domain[domain].append({
            'id': expert['id'],
            'name': expert.get('name', ''),
            'name_cn': expert.get('name_cn', ''),
            'subdomain': expert.get('subdomain', ''),
            'level': expert.get('level', ''),
            'avatar': expert.get('avatar', '')
        })

        # by_level
        level = expert.get('level', 'unknown')
        if level not in by_level:
            by_level[level] = []
        by_level[level].append({
            'id': expert['id'],
            'name': expert.get('name', ''),
            'domain': domain,
            'avatar': expert.get('avatar', '')
        })

        # by_keyword
        for keyword in expert.get('trigger_keywords', []):
            keyword = keyword.lower().strip()
            if keyword not in by_keyword:
                by_keyword[keyword] = []
            by_keyword[keyword].append(expert['id'])

    return {
        'experts': experts,
        'by_domain': by_domain,
        'by_level': by_level,
        'by_keyword': by_keyword,
        'by_id': by_id
    }


def main():
    print("🔍 Scanning experts...")
    experts = scan_experts()
    print(f"   Found {len(experts)} experts")

    print("📚 Building indexes...")
    indexes = build_indexes(experts)

    print("💾 Saving to", OUTPUT_FILE)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(indexes, f, ensure_ascii=False, indent=2)

    print("✅ Expert library initialized!")
    print(f"   - {len(experts)} experts")
    print(f"   - {len(indexes['by_domain'])} domains")
    print(f"   - {len(indexes['by_keyword'])} keywords")


if __name__ == "__main__":
    main()