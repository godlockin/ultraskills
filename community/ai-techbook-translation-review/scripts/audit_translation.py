#!/usr/bin/env python3
"""
翻译与原文对齐度核查

对比源 (英文) 与译 (中文) 章节的:
- 章节标题覆盖
- 小节数量对齐
- 公式保留
- 图片数量匹配
- 链接保留

Usage:
    python3 audit_translation.py --src ./ --target ./zh/
"""

import argparse
import os
import re
from collections import Counter


def parse_chapters(root, pattern, prefix='chapter'):
    """Find chapters in root matching pattern."""
    chapters = {}
    if os.path.isdir(root):
        for entry in os.listdir(root):
            if prefix in entry:
                # English: "chapter 01 - vectors"
                m = re.match(rf'{prefix}\s*(\d+)', entry)
                if m:
                    ch_num = int(m.group(1))
                    chapters[ch_num] = os.path.join(root, entry)
    return chapters


def extract_sections(chapter_dir):
    """Extract section titles from markdown files."""
    sections = []
    if not os.path.isdir(chapter_dir):
        return sections
    for f in sorted(os.listdir(chapter_dir)):
        if not f.endswith('.md'):
            continue
        path = os.path.join(chapter_dir, f)
        with open(path) as fp:
            content = fp.read()
        # H2/H3 headers
        for m in re.finditer(r'^(#{2,3})\s+(.+)$', content, re.MULTILINE):
            sections.append((f, m.group(2).strip()))
    return sections


def extract_assets(content):
    """Extract comparable Markdown assets, preserving source payloads."""
    images = re.findall(r'!\[[^]]*\]\([^)]*\)', content)
    links = re.findall(r'(?<!!)\[[^]]*\]\([^)]*\)', content)
    code_blocks = re.findall(r'```[^\n]*\n(.*?)```', content, re.DOTALL)
    formulas = []
    formulas.extend(re.findall(r'\$\$(.*?)\$\$', content, re.DOTALL))
    formulas.extend(re.findall(r'\\\[(.*?)\\\]', content, re.DOTALL))
    formulas.extend(re.findall(r'\\\((.*?)\\\)', content, re.DOTALL))
    # Avoid treating currency as math; inline LaTeX must contain non-space content.
    formulas.extend(re.findall(r'(?<!\$)\$(?!\$)([^\n$]+?)(?<!\$)\$(?!\$)', content))
    return images, links, code_blocks, formulas


def count_assets(content):
    """Count images, fenced code blocks, and formulas."""
    images, _, code_blocks, formulas = extract_assets(content)
    return len(images), len(code_blocks), len(formulas)


def compare_assets(src_values, tgt_values, name):
    """Return an issue when target does not preserve exact asset payloads."""
    src_counter = Counter(src_values)
    tgt_counter = Counter(tgt_values)
    missing = list((src_counter - tgt_counter).elements())
    extra = list((tgt_counter - src_counter).elements())
    if not missing and not extra:
        return None
    return f'{name} mismatch: missing={len(missing)} extra={len(extra)}'


def audit_chapter(src_dir, tgt_dir, ch_num):
    """Audit a single chapter. Returns dict of stats and issues."""
    issues = []
    stats = {}

    if not os.path.isdir(src_dir):
        return {'issues': ['src not found'], 'stats': {}}
    if not os.path.isdir(tgt_dir):
        return {'issues': ['target not found'], 'stats': {}}

    src_files = sorted([f for f in os.listdir(src_dir) if f.endswith('.md')])
    tgt_files = sorted([f for f in os.listdir(tgt_dir) if f.endswith('.md')])

    stats['src_files'] = len(src_files)
    stats['tgt_files'] = len(tgt_files)

    # File count diff
    if len(src_files) != len(tgt_files):
        issues.append(f'file count mismatch: src={len(src_files)} tgt={len(tgt_files)}')

    # Aggregate stats
    src_total_lines = 0
    tgt_total_lines = 0
    src_images = 0
    tgt_images = 0
    src_code = []
    tgt_code = []
    src_formulas = []
    tgt_formulas = []
    src_links = []
    tgt_links = []

    for f in src_files:
        with open(os.path.join(src_dir, f)) as fp:
            content = fp.read()
        src_total_lines += content.count('\n')
        images, links, code, formulas = extract_assets(content)
        src_images += len(images)
        src_code.extend(code)
        src_formulas.extend(formulas)
        src_links.extend(links)

    for f in tgt_files:
        with open(os.path.join(tgt_dir, f)) as fp:
            content = fp.read()
        tgt_total_lines += content.count('\n')
        images, links, code, formulas = extract_assets(content)
        tgt_images += len(images)
        tgt_code.extend(code)
        tgt_formulas.extend(formulas)
        tgt_links.extend(links)

    stats['src_lines'] = src_total_lines
    stats['tgt_lines'] = tgt_total_lines
    stats['src_images'] = src_images
    stats['tgt_images'] = tgt_images
    stats['src_math'] = len(src_formulas)
    stats['tgt_math'] = len(tgt_formulas)
    stats['src_code'] = len(src_code)
    stats['tgt_code'] = len(tgt_code)
    stats['src_links'] = len(src_links)
    stats['tgt_links'] = len(tgt_links)

    # These are integrity checks, not approximate counts: deletion or mutation fails.
    for source, target, name in (
        (src_formulas, tgt_formulas, 'formula'),
        (src_code, tgt_code, 'code'),
        (src_links, tgt_links, 'link'),
    ):
        issue = compare_assets(source, target, name)
        if issue:
            issues.append(issue)

    # Image count (expect 1:1 or close)
    if src_images > 0 and abs(src_images - tgt_images) > 2:
        issues.append(f'image count diff: src={src_images} tgt={tgt_images}')

    # Line count (Chinese typically 1.5-2x English)
    if src_total_lines > 0 and tgt_total_lines < src_total_lines * 1.2:
        issues.append(f'tgt shorter than expected: src={src_total_lines} tgt={tgt_total_lines}')

    return {'issues': issues, 'stats': stats}


def print_audit(chapter_results, num_chapters=25):
    print('=== 翻译对齐度审计 ===\n')
    print('章 | 文件 | 行数(src→tgt) | 图片 | 公式 | 代码 | 链接 | 问题')
    print('-' * 90)

    total_issues = 0
    for ch in range(1, num_chapters + 1):
        if ch not in chapter_results:
            continue
        r = chapter_results[ch]
        s = r['stats']
        issue_str = '; '.join(r['issues']) if r['issues'] else '✅'
        print(f'{ch:02d} | {s.get("src_files", "?")}/{s.get("tgt_files", "?")} | '
              f'{s.get("src_lines", "?")}→{s.get("tgt_lines", "?")} | '
              f'{s.get("src_images", "?")}→{s.get("tgt_images", "?")} | '
              f'{s.get("src_math", "?")}→{s.get("tgt_math", "?")} | '
              f'{s.get("src_code", "?")}→{s.get("tgt_code", "?")} | '
              f'{s.get("src_links", "?")}→{s.get("tgt_links", "?")} | '
              f'{issue_str}')
        total_issues += len(r['issues'])

    print(f'\n=== TOTAL: {total_issues} issues across {num_chapters} chapters ===')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translation alignment audit')
    parser.add_argument('--src', required=True, help='Source directory (e.g. English chapters)')
    parser.add_argument('--target', required=True, help='Target directory (e.g. zh/第*章)')
    parser.add_argument('--chapters', type=int, default=25)
    args = parser.parse_args()

    # Discover chapter dirs
    src_chapters = parse_chapters(args.src, 'chapter', prefix='chapter')
    # Target: e.g. zh/第01章 - 向量
    tgt_chapters = {}
    if os.path.isdir(args.target):
        for entry in os.listdir(args.target):
            if entry.startswith('第') and '章' in entry:
                m = re.match(r'第(\d+)章', entry)
                if m:
                    ch_num = int(m.group(1))
                    tgt_chapters[ch_num] = os.path.join(args.target, entry)

    # Audit each
    results = {}
    for ch_num in range(1, args.chapters + 1):
        src_dir = src_chapters.get(ch_num)
        tgt_dir = tgt_chapters.get(ch_num)
        if src_dir and tgt_dir:
            results[ch_num] = audit_chapter(src_dir, tgt_dir, ch_num)
        else:
            results[ch_num] = {
                'issues': [f'src={"missing" if not src_dir else "ok"} tgt={"missing" if not tgt_dir else "ok"}'],
                'stats': {}
            }

    print_audit(results, args.chapters)