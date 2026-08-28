#!/usr/bin/env python3
"""
从英文原文中提取候选术语,辅助构建 GLOSSARY.md

扫描 chapter 目录,提取:
- 加粗英文术语 (**term**)
- 斜体英文术语 (*term*)
- 标题中的英文术语
- 首次出现的缩写 (NLP, LLM 等)

输出 markdown 表格,供人工校对。

Usage:
    python3 glossary_init.py --source ./chapter*/ --output ./zh/GLOSSARY.md
"""

import argparse
import os
import re
from collections import Counter, defaultdict


def extract_candidates(content):
    """Extract candidate English terms from markdown content."""
    candidates = Counter()

    # Bold terms
    for m in re.finditer(r'\*\*([A-Za-z][\w\- ]{1,40}?)\*\*', content):
        term = m.group(1).strip()
        # Skip if contains too many spaces (probably sentence)
        if term.count(' ') <= 3 and not term.endswith('.'):
            candidates[term] += 1

    # Italic terms
    for m in re.finditer(r'(?<!\*)\*([A-Za-z][\w\- ]{1,40}?)\*(?!\*)', content):
        term = m.group(1).strip()
        if term.count(' ') <= 3 and not term.endswith('.'):
            candidates[term] += 2  # italic is more likely to be a term

    # Headers
    for m in re.finditer(r'^#{2,6}\s+(.+)$', content, re.MULTILINE):
        header = m.group(1).strip()
        # Extract English parts
        for tm in re.finditer(r'\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*)\b', header):
            candidates[tm.group(1)] += 3

    # Capitalized terms (first occurrence of concept)
    for m in re.finditer(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+)\b', content):
        # CamelCase like Transformer, MultiHead
        candidates[m.group(1)] += 1

    return candidates


def is_chinese(s):
    """Check if string contains Chinese chars."""
    return bool(re.search(r'[一-鿿]', s))


def main():
    parser = argparse.ArgumentParser(description='Extract glossary candidates from English chapters')
    parser.add_argument('--source', required=True, help='Source directory (chapter*)')
    parser.add_argument('--output', default='GLOSSARY.md', help='Output path')
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(f'Error: {args.source} not a directory')
        return 1

    all_candidates = Counter()

    for entry in sorted(os.listdir(args.source)):
        if not entry.startswith('chapter'):
            continue
        ch_dir = os.path.join(args.source, entry)
        if not os.path.isdir(ch_dir):
            continue
        for f in sorted(os.listdir(ch_dir)):
            if not f.endswith('.md'):
                continue
            path = os.path.join(ch_dir, f)
            with open(path) as fp:
                content = fp.read()
            cands = extract_candidates(content)
            all_candidates.update(cands)

    # Filter: keep only terms appearing 3+ times
    filtered = {term: count for term, count in all_candidates.items()
                if count >= 3 and not is_chinese(term)}

    # Sort by frequency
    sorted_terms = sorted(filtered.items(), key=lambda x: -x[1])

    # Write output
    with open(args.output, 'w') as fp:
        fp.write('# GLOSSARY\n\n')
        fp.write('> 自动提取的候选术语 (出现 ≥3 次),请人工校对并填入中文译法。\n\n')
        fp.write('| English | 中文 | 出现次数 | 说明 |\n')
        fp.write('|---------|------|----------|------|\n')
        for term, count in sorted_terms[:200]:  # Top 200
            fp.write(f'| {term} | | {count} | |\n')
        fp.write(f'\n> 共 {len(sorted_terms)} 个候选术语 (本表显示 Top 200)\n')

    print(f'✅ Wrote {len(sorted_terms)} candidates to {args.output}')
    print(f'   Top 10:')
    for term, count in sorted_terms[:10]:
        print(f'   {count:4d}  {term}')


if __name__ == '__main__':
    main()