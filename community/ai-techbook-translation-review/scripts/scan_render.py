#!/usr/bin/env python3
"""
图书 Markdown 渲染报错扫描器

扫描 mermaid / KaTeX / Markdown math 语法错误,支持自动修复模式。

Usage:
    # Read-only scan
    python3 scan_render.py --root ./zh/ --target zh

    # Auto-fix mode
    python3 scan_render.py --root ./zh/ --target zh --fix

    # Scan English original (read-only)
    python3 scan_render.py --root ./chapter*/ --target en --read-only
"""

import argparse
import os
import re
import sys
from collections import Counter


def scan_inline_math(content):
    """Find LaTeX-native inline \\( ... \\) that Markdown doesn't render."""
    return re.findall(r'\\\((.*?)\\\)', content, re.DOTALL)


def scan_block_math(content):
    """Find LaTeX-native block \\[ ... \\] that Markdown doesn't render."""
    return re.findall(r'\\\[(.*?)\\\]', content, re.DOTALL)


def scan_inline_dollar_with_begin(content):
    """Find $...\\begin{...}...$ that partial renderers don't support."""
    return re.findall(r'(?<!\\)(?<!\$)\$([^$\n]*\\begin\{[^}]+\}[^$]*)\$(?!\$)', content)


def scan_katex_func_subscript(content):
    """Find _\\func without {} that KaTeX rejects."""
    funcs = ['max', 'min', 'arg', 'inf', 'sup', 'lim', 'log', 'ln', 'exp',
             'sin', 'cos', 'tan', 'det', 'gcd', 'deg', 'dim', 'ker', 'hom', 'Pr']
    issues = []
    for fn in funcs:
        pattern = r'_\\' + fn + r'(?![a-zA-Z{])'
        for m in re.finditer(pattern, content):
            issues.append((fn, m.group(0)[:50]))
    return issues


def scan_unbalanced_braces(content):
    """Find single-line $...$ with unbalanced { }."""
    issues = []
    for m in re.finditer(r'(?<!\\)(?<!\$)\$([^$\n]+)\$(?!\$)', content):
        math = m.group(1)
        if math.count('{') != math.count('}'):
            issues.append(math[:60])
    return issues


def scan_mermaid_blocks(content):
    """Scan mermaid blocks for naked labels with special chars and other issues."""
    issues = []
    blocks = re.findall(r'```mermaid\n(.*?)\n```', content, re.DOTALL)
    for bi, block in enumerate(blocks):
        # naked [label] with special chars
        for m in re.finditer(r'(?<!\\")(?<!\\\')\[([^\[\]"\']+)\]', block):
            label = m.group(1)
            if any(c in label for c in ['(', ')', '%', '<', '>']):
                issues.append(('mermaid_naked', label[:50]))
        # $ in mermaid
        if '$' in block:
            issues.append(('mermaid_dollar', ''))
        # subgraph/end mismatch
        sub = len(re.findall(r'^\s*subgraph\b', block, re.MULTILINE))
        end = len(re.findall(r'^\s*end\s*$', block, re.MULTILINE))
        if sub != end:
            issues.append((f'mermaid_subgraph sub={sub} end={end}', ''))
    return issues


def fix_inline_math(content):
    """Convert \\( ... \\) to $ ... $."""
    def replace(m):
        inner = m.group(1)
        if '$$' in inner:
            return m.group(0)
        return '$' + inner.replace('$', '\\$') + '$'
    return re.sub(r'\\\((.*?)\\\)', replace, content, flags=re.DOTALL)


def fix_block_math(content):
    """Convert \\[ ... \\] to $$ ... $$."""
    return re.sub(r'\\\[(.*?)\\\]', lambda m: '$$\n' + m.group(1).strip() + '\n$$',
                  content, flags=re.DOTALL)


def fix_inline_dollar_with_begin(content):
    """Convert $...\\begin{...}...$ to $$...$$."""
    def replace(m):
        return '$$\n' + m.group(1).strip() + '\n$$'
    return re.sub(r'(?<!\\)(?<!\$)\$([^$\n]*\\begin\{[^}]+\}[^$]*)\$(?!\$)',
                  replace, content)


def fix_katex_func_subscript(content):
    """Convert _\\func to _{\\func}."""
    funcs = ['max', 'min', 'arg', 'inf', 'sup', 'lim', 'log', 'ln', 'exp',
             'sin', 'cos', 'tan', 'det', 'gcd', 'deg', 'dim', 'ker', 'hom', 'Pr']
    for fn in funcs:
        pattern = r'_\\' + fn + r'(?![a-zA-Z{])'
        content = re.sub(pattern, r'_{\\' + fn + '}', content)
    return content


def scan_path(path, fix=False):
    """Scan a single file, optionally fix it. Returns list of issue tuples."""
    with open(path) as fp:
        content = fp.read()
    issues = []

    # Inline math
    inline = scan_inline_math(content)
    if inline:
        issues.append(('inline_\\(\\)', len(inline)))
        if fix:
            content = fix_inline_math(content)

    # Block math
    block = scan_block_math(content)
    if block:
        issues.append(('block_\\[\\]', len(block)))
        if fix:
            content = fix_block_math(content)

    # Inline dollar with begin
    inline_begin = scan_inline_dollar_with_begin(content)
    if inline_begin:
        issues.append(('inline_dollar_with_begin', len(inline_begin)))
        if fix:
            content = fix_inline_dollar_with_begin(content)

    # KaTeX function subscript
    katex_func = scan_katex_func_subscript(content)
    if katex_func:
        issues.append(('katex_func_no_brace', len(katex_func)))
        if fix:
            content = fix_katex_func_subscript(content)

    # Unbalanced braces
    unbalanced = scan_unbalanced_braces(content)
    if unbalanced:
        issues.append(('unbalanced_braces', len(unbalanced)))

    # mermaid
    mermaid_issues = scan_mermaid_blocks(content)
    if mermaid_issues:
        for issue in mermaid_issues:
            issues.append(('mermaid_' + issue[0].split()[0], 1))

    if fix:
        with open(path, 'w') as fp:
            fp.write(content)

    return issues


def scan_root(root, fix=False, verbose=True):
    """Scan all .md files under root. Returns Counter of issue types."""
    total_issues = Counter()
    files_with_issues = 0
    total_files = 0

    for dirpath, dirs, files in os.walk(root):
        for f in files:
            if not f.endswith('.md'):
                continue
            total_files += 1
            path = os.path.join(dirpath, f)
            issues = scan_path(path, fix=fix)
            if issues:
                files_with_issues += 1
                total_issues.update([i[0] for i in issues])
                if verbose and not fix:
                    print(f'\n{path}')
                    for issue_type, count in issues:
                        print(f'  {issue_type}: {count}')

    print(f'\n=== SUMMARY ===')
    print(f'Total files scanned: {total_files}')
    print(f'Files with issues: {files_with_issues}')
    print(f'\n=== BY TYPE ===')
    for itype, count in total_issues.most_common():
        print(f'  {count:5d}  {itype}')
    print(f'\nTOTAL ISSUES: {sum(total_issues.values())}')
    return total_issues


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Book markdown render scanner')
    parser.add_argument('--root', required=True, help='Root directory to scan')
    parser.add_argument('--target', choices=['zh', 'en'], default='zh',
                        help='Target language: zh (will auto-fix) or en (read-only)')
    parser.add_argument('--fix', action='store_true', help='Auto-fix issues')
    parser.add_argument('--read-only', action='store_true', help='Read-only mode')
    args = parser.parse_args()

    fix = args.fix and not args.read_only
    if args.target == 'en':
        fix = False  # English: never auto-fix

    scan_root(args.root, fix=fix, verbose=True)