#!/usr/bin/env python3
"""
术语一致性检查 — 跨章术语翻译是否一致

读取 GLOSSARY.md 中定义的术语,检查译文中是否一致使用。

Usage:
    python3 term_check.py --glossary ./zh/GLOSSARY.md --target ./zh/
"""

import argparse
import os
import re
from collections import defaultdict


def load_glossary(path):
    """Load GLOSSARY.md. Expected format: | 中文 | English | 说明 |"""
    glossary = {}  # english -> chinese
    if not os.path.exists(path):
        return glossary
    with open(path) as fp:
        for line in fp:
            line = line.strip()
            # Match table row: | 中文 | English | 说明 |
            m = re.match(r'\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|', line)
            if m:
                chinese, english, _ = m.groups()
                if english and chinese and not english.startswith('-'):  # skip separator
                    glossary[english.strip().lower()] = chinese.strip()
    return glossary


def scan_file(path, glossary):
    """Scan a single file. Returns list of (term, expected, found) issues."""
    issues = []
    if not glossary:
        return issues
    with open(path) as fp:
        content = fp.read()
    for english, expected_chinese in glossary.items():
        # Skip very short terms (false positives)
        if len(english) < 3:
            continue
        # Check if English term appears in file
        # Use word boundary for multi-word, lowercase for case-insensitive
        pattern = re.compile(r'\b' + re.escape(english) + r'\b', re.IGNORECASE)
        if pattern.search(content):
            # Find all Chinese candidates near this English
            # Heuristic: search for common alternative translations within 200 chars
            for m in pattern.finditer(content):
                start = max(0, m.start() - 200)
                end = min(len(content), m.end() + 200)
                context = content[start:end]
                # Extract Chinese strings (3+ chars)
                chinese_matches = re.findall(r'[一-鿿]{2,}', context)
                for cm in chinese_matches:
                    if cm != expected_chinese and len(cm) >= 3:
                        # Heuristic: if alternative Chinese appears 3+ times near this term
                        if chinese_matches.count(cm) >= 2:
                            issues.append({
                                'term': english,
                                'expected': expected_chinese,
                                'found': cm,
                                'count': chinese_matches.count(cm)
                            })
                            break
    return issues


def scan_root(root, glossary):
    """Scan all .md files under root."""
    all_issues = defaultdict(list)
    for dirpath, _, files in os.walk(root):
        for f in files:
            if not f.endswith('.md'):
                continue
            path = os.path.join(dirpath, f)
            issues = scan_file(path, glossary)
            for issue in issues:
                key = (issue['term'], issue['expected'], issue['found'])
                all_issues[key].append(path)
    return all_issues


def print_report(all_issues):
    print('=== 术语一致性检查报告 ===\n')
    print(f'发现不一致术语组合: {len(all_issues)}\n')

    if not all_issues:
        print('✅ 所有术语翻译一致')
        return

    print('| 英文术语 | 标准译法 | 发现译法 | 出现文件数 |')
    print('|----------|----------|----------|------------|')
    for (term, expected, found), paths in sorted(all_issues.items(), key=lambda x: -len(x[1])):
        print(f'| {term} | {expected} | {found} | {len(paths)} |')

    print('\n=== 详细位置 (Top 5) ===')
    for (term, expected, found), paths in sorted(all_issues.items(), key=lambda x: -len(x[1]))[:5]:
        print(f'\n**{term}** 标准: {expected}, 发现: {found}')
        for p in paths[:3]:
            print(f'  - {p}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Terminology consistency check')
    parser.add_argument('--glossary', required=True, help='GLOSSARY.md path')
    parser.add_argument('--target', required=True, help='Target directory to scan')
    args = parser.parse_args()

    glossary = load_glossary(args.glossary)
    print(f'Loaded {len(glossary)} terms from glossary\n')

    all_issues = scan_root(args.target, glossary)
    print_report(all_issues)