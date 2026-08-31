#!/usr/bin/env python3
"""
check-skill-refs.py — 校验 SKILL.md 中引用的下游 skill id 是否真实存在

用于 orchestrator 类 skill:它们的核心正确性就是"路由指向的 skill 真的在"。
`check-skill-links.sh` 只查文件路径,查不出 skill id 不解析 —— 那是语义断链。

Usage:
    python3 scripts/check-skill-refs.py community/content-orchestrator
    python3 scripts/check-skill-refs.py community/*-orchestrator
    python3 scripts/check-skill-refs.py --list-ids        # 打印 index.json 里所有 id

Exit codes:
    0 = 全部引用可解析
    1 = 存在不可解析的引用
    2 = 参数/环境错误
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INDEX = REPO_ROOT / "index.json"

# 反引号里形如 skill-id 的 token(小写字母数字连字符,≥2 段)
BACKTICK_ID_RE = re.compile(r"`([a-z0-9]+(?:-[a-z0-9]+){1,})`")

# 裸 token 形式的 skill id — orchestrator 的路由表常这样写:
#   | content-presentation | 6 | **C2** | deck-that-wins, spreadsheet-formula, to-prd |
# 只在表格单元格与列表项里找,避免把正文里的连字符词都当 id
BARE_ID_RE = re.compile(r"(?<![\w`/.-])([a-z0-9]+(?:-[a-z0-9]+){1,})(?![\w`/.-])")

# 明显不是 skill id 的 token — 命令、文件名、技术词
NOT_SKILL_ID = {
    # 命令与工具
    "npm-install", "npx-create", "pip-install", "git-clone", "git-commit",
    "py-compile", "run-in-background", "exit-code", "check-done",
    # 常见技术词
    "best-practice", "best-practices", "step-by-step", "top-level",
    "read-only", "up-to-date", "end-to-end", "one-shot", "1-shot",
    "real-time", "long-form", "short-form", "high-fidelity", "low-fidelity",
    "open-source", "third-party", "front-end", "back-end", "full-stack",
    "use-case", "use-cases", "trade-off", "trade-offs", "follow-up",
    "drop-in", "opt-in", "opt-out", "built-in", "hands-on", "case-study",
    "case-studies", "self-hosted", "cross-platform", "multi-context",
    "single-source", "source-of-truth", "code-anchor", "last-verified",
    "bounded-context", "human-in-the-loop", "out-of-scope", "so-called",
    "well-known", "so-far", "day-to-day", "side-by-side", "on-demand",
    "fine-tune", "fine-tuning", "state-of-the-art", "must-have",
    "nice-to-have", "off-the-shelf", "plug-and-play", "zero-shot",
    "few-shot", "chain-of-thought", "text-to-speech", "speech-to-text",
    "click-through", "sign-up", "drop-off", "break-even", "go-to-market",
    "product-market", "time-to-value", "b2b-saas", "9-16", "16-9", "3-4",
    # 文件与格式
    "package-json", "tsconfig-json", "index-json", "skill-md", "readme-md",
    "routing-table", "case-studies-md", "requirements-txt",
    # 本仓库的目录/概念名(非 skill)
    "skill-arena", "ultraskills-hub", "skill-manager", "skill-loader",
    "arena-scan", "arena-build-index", "arena-cluster-score",
    # sub-cluster 名前缀(engineering-orchestrator 的表格里是 sub-cluster 而非 skill)
    "engineering-qa", "engineering-devops", "engineering-debug",
    "engineering-lang", "engineering-arch", "engineering-security",
    "business-finance", "business-legal", "business-clevel",
    "business-product", "business-operations", "business-pm",
    "business-strategy", "business-hr", "business-marketing",
    "sales-marketing", "small-business-ops", "finance-accounting",
    "hr-talent", "legal-compliance", "content-writing", "content-doc",
    "content-presentation", "content-video", "content-image",
    "content-social", "content-seo", "social-media-cn", "video-production",
}


def load_index_ids() -> set[str]:
    if not INDEX.exists():
        print(f"错误: 找不到 {INDEX}", file=sys.stderr)
        sys.exit(2)
    try:
        data = json.loads(INDEX.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误: index.json 解析失败: {e}", file=sys.stderr)
        sys.exit(2)
    ids: set[str] = set()
    for s in data.get("skills", []):
        sid = s.get("id")
        if isinstance(sid, str):
            # index.json 里存在带转义引号的脏 id,一并归一化
            ids.add(sid.strip().strip('"').strip("'"))
    if not ids:
        print("错误: index.json 中没有 skills", file=sys.stderr)
        sys.exit(2)
    return ids


def extract_candidates(line: str) -> set[str]:
    """从一行 markdown 里提取疑似 skill id 引用。

    两种来源:
      1. 反引号包裹 —— 任何位置都算
      2. 裸 token —— 只在表格单元格或列表项里算,避免把正文的连字符词误判
    """
    out: set[str] = set()

    def keep(tok: str) -> bool:
        if tok in NOT_SKILL_ID:
            return False
        if re.fullmatch(r"[\d.-]+", tok):  # 纯数字/版本号
            return False
        if len(tok) < 5:  # 太短的不像 skill id
            return False
        return True

    for m in BACKTICK_ID_RE.finditer(line):
        if keep(m.group(1)):
            out.add(m.group(1))

    stripped = line.strip()
    is_table_row = stripped.startswith("|")
    is_list_item = bool(re.match(r"^[-*+]\s|^\d+\.\s", stripped))
    if not (is_table_row or is_list_item):
        return out

    # 表格行:只扫单元格内容;列表项:扫整行
    segments: list[str] = []
    if is_table_row:
        segments = [c.strip() for c in stripped.strip("|").split("|")]
    else:
        segments = [stripped]

    for seg in segments:
        # 去掉 markdown 强调与链接文本,只留可能的 id
        seg = re.sub(r"\*\*|__|\*|_", "", seg)
        seg = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", seg)
        # 反引号内容已在上面处理过,这里移除以免重复
        seg = re.sub(r"`[^`]*`", " ", seg)
        # 引号内是用户原话/查询词/示例文本,不是 skill 引用
        seg = re.sub(r'"[^"]*"', " ", seg)
        seg = re.sub(r"[“][^”]*[”]", " ", seg)
        seg = re.sub(r"[「][^」]*[」]", " ", seg)
        for m in BARE_ID_RE.finditer(seg):
            if keep(m.group(1)):
                out.add(m.group(1))

    return out


def nearest(tok: str, ids: set[str], limit: int = 3) -> list[str]:
    """给不可解析的 id 找最接近的候选。

    只认「一方是另一方的前缀」这类强关系,避免 `content-writing` 因为
    子串包含匹配到一堆无关 skill,产生噪声。
    """
    cands: list[str] = []
    for i in ids:
        if i.startswith(tok + "-") or tok.startswith(i + "-"):
            cands.append(i)          # spreadsheet-formula → spreadsheet-formula-helper
        elif i.endswith("-" + tok) or tok.endswith("-" + i):
            cands.append(i)          # markdown-to-html → baoyu-markdown-to-html
    return sorted(cands, key=len)[:limit]


def check_skill(
    skill_dir: Path, ids: set[str], strict: bool
) -> tuple[list[tuple[str, int, str, list[str]]], int]:
    """校验一个 skill。

    返回 (确信的问题, 被忽略的疑似项数)。

    默认只报**有近似候选**的 token —— 那说明作者确实想引用某个 skill 但写错了,
    是真断链。没有近似候选的 token 大多是 cluster 名、章节名或普通连字符词,
    报出来只会淹没真问题。`--strict` 可查看全部疑似项。
    """
    confirmed: list[tuple[str, int, str, list[str]]] = []
    ignored = 0
    for md in sorted(skill_dir.rglob("*.md")):
        try:
            lines = md.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        rel = str(md.relative_to(skill_dir.parent))
        for lineno, line in enumerate(lines, 1):
            for tok in sorted(extract_candidates(line)):
                if tok in ids or tok == skill_dir.name:
                    continue
                sugg = nearest(tok, ids)
                if sugg or strict:
                    confirmed.append((rel, lineno, tok, sugg))
                else:
                    ignored += 1
    return confirmed, ignored


def main() -> int:
    parser = argparse.ArgumentParser(
        description="校验 SKILL.md 中引用的下游 skill id 是否存在于 index.json"
    )
    parser.add_argument("skill_dirs", nargs="*", help="skill 目录")
    parser.add_argument(
        "--list-ids", action="store_true", help="打印 index.json 中所有 skill id"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="报告所有疑似项(含无近似候选的),噪声较多但覆盖全",
    )
    args = parser.parse_args()

    ids = load_index_ids()

    if args.list_ids:
        for i in sorted(ids):
            print(i)
        return 0

    if not args.skill_dirs:
        parser.print_help()
        return 2

    total_problems = 0
    total_ignored = 0
    for d in args.skill_dirs:
        path = Path(d)
        if not path.is_dir():
            print(f"SKIP  {d} (不存在)")
            continue
        problems, ignored = check_skill(path.resolve(), ids, args.strict)
        total_ignored += ignored
        if problems:
            print(f"\n{path.name}: {len(problems)} 处疑似断链")
            for rel, lineno, tok, sugg in problems:
                hint = f"  → 是否想写: {', '.join(sugg)}" if sugg else ""
                print(f"  UNRESOLVED  {rel}:{lineno}  {tok}{hint}")
            total_problems += len(problems)
        else:
            print(f"{path.name}: 未发现疑似断链")

    print("---")
    if total_ignored and not args.strict:
        print(
            f"(已忽略 {total_ignored} 个无近似候选的 token —— 多为 cluster 名/普通词;"
            f"用 --strict 查看)"
        )
    if total_problems == 0:
        print(f"skill ref check: 通过(index 共 {len(ids)} 个 skill)")
        return 0
    print(f"skill ref check: {total_problems} 处疑似断链")
    return 1


if __name__ == "__main__":
    sys.exit(main())
