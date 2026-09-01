#!/usr/bin/env python3
"""
中文全角标点规范化

将英文标点 (在中文上下文中) 转为全角:
- , → ,
- . → 。
- : → :
- ; → ;
- ! → !
- ? → ?
- ( ) → ( )
- " " → " "
- ' ' → ' '

注意: 保留:
- 代码块内 (`code`)
- 数学公式内 ($...$)
- 英文/数字旁的半角标点
- URL/邮箱
"""

import argparse
import os
import re
import sys


_PROTECTED_SPAN_PATTERN = re.compile(
    r"```[^\n]*\n.*?```"
    r"|```.*?```"
    r"|`[^`\n]*`"
    r"|\$\$.*?\$\$"
    r"|\$(?!\$)[^\n$]*\$(?!\$)"
    r"|\\\(.*?\\\)"
    r"|\\\[.*?\\\]"
    r"|https?://[^\s<>，。！？；：]+",
    re.DOTALL,
)


def iter_protected_spans(content):
    """Yield code, math, and URL spans that must not be normalized."""
    return _PROTECTED_SPAN_PATTERN.finditer(content)


def normalize_content(content):
    """Normalize ordinary text while preserving protected spans verbatim."""
    parts = []
    last_end = 0
    for match in iter_protected_spans(content):
        plain_text = content[last_end : match.start()]
        parts.append(normalize_plain_text(plain_text))
        parts.append(match.group(0))
        last_end = match.end()
    parts.append(normalize_plain_text(content[last_end:]))
    return ''.join(parts)


def normalize_plain_text(content):
    """Normalize each line in an unprotected text segment."""
    return ''.join(
        normalize_line_punctuation(line)
        for line in content.splitlines(keepends=True)
    ) if content else content
def normalize_line_punctuation(line):
    """Normalize punctuation in a single line (heuristic).

    Strategy:
    - If line is >50% Chinese chars, treat as Chinese context → full-width
    - Skip code/math regions
    """
    # Skip if line is in code block (handled by caller)
    # Skip if line is purely URL/email/english

    # Count Chinese chars
    chinese_count = len(re.findall(r'[一-鿿]', line))
    total_chars = len(re.findall(r'\S', line))
    if total_chars == 0:
        return line

    # If >50% Chinese, apply full-width rules
    if chinese_count / total_chars < 0.3:
        return line

    # Apply rules
    # Quote pairs
    line = re.sub(r'(?<=[\s一-鿿])"([^"]*?)"(?=[\s一-鿿，。、！？])', r'"\1"', line)
    line = re.sub(r'(?<=[\s一-鿿])\'([^\']*?)\'(?=[\s一-鿿，。、！？])', r"'\1'", line)

    # Comma + Chinese context
    line = re.sub(r'(?<=[一-鿿]),', '，', line)
    # Period + Chinese context (but not after digit/letter or in math)
    line = re.sub(r'(?<=[一-鿿])\.(?=[一-鿿\s，。、！？])', '。', line)
    # Colon + Chinese
    line = re.sub(r'(?<=[一-鿿]):(?=[一-鿿\s])', '：', line)
    # Semicolon
    line = re.sub(r'(?<=[一-鿿]);(?=[一-鿿\s])', '；', line)
    # Exclamation
    line = re.sub(r'(?<=[一-鿿])!(?=[一-鿿\s])', '！', line)
    # Question
    line = re.sub(r'(?<=[一-鿿])\?(?=[一-鿿\s])', '？', line)
    # Parentheses
    line = re.sub(r'(?<=[一-�（])\(', '（', line)
    line = re.sub(r'\)(?=[一-鿿）\s，。、！？])', '）', line)

    return line


def normalize_file(path, dry_run=False):
    """Normalize a single markdown file."""
    with open(path) as fp:
        content = fp.read()

    new_content = normalize_content(content)

    # In dry_run mode, just count differences
    if dry_run:
        return content != new_content, new_content

    with open(path, 'w') as fp:
        fp.write(new_content)
    return True, new_content


def main():
    parser = argparse.ArgumentParser(description='Normalize Chinese punctuation')
    parser.add_argument('paths', nargs='+', help='Files or directories to normalize')
    parser.add_argument('--dry-run', action='store_true', help='Only show what would change')
    args = parser.parse_args()

    total_files = 0
    total_changed = 0

    for path_arg in args.paths:
        if os.path.isfile(path_arg):
            files = [path_arg]
        elif os.path.isdir(path_arg):
            files = []
            for root, _, fs in os.walk(path_arg):
                for f in fs:
                    if f.endswith('.md'):
                        files.append(os.path.join(root, f))
        else:
            print(f'Skip {path_arg} (not found)')
            continue

        for f in files:
            total_files += 1
            try:
                changed, _ = normalize_file(f, dry_run=args.dry_run)
                if changed:
                    total_changed += 1
                    status = 'would change' if args.dry_run else 'normalized'
                    print(f'  [{status}] {f}')
            except Exception as e:
                print(f'  [ERROR] {f}: {e}')

    print(f'\nTotal: {total_changed}/{total_files} files {"would change" if args.dry_run else "changed"}')


if __name__ == '__main__':
    main()