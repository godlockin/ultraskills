#!/usr/bin/env bash
# shield-reverse-skill.sh — disable reverse-skill's global CLAUDE.md injection.
#
# Usage: bash scripts/shield-reverse-skill.sh [/path/to/external/reverse-skill]

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SUBMODULE_PATH="${1:-$REPO_ROOT/external/reverse-skill}"
RULES_FILE="$SUBMODULE_PATH/RULES.md"

if [[ ! -d "$SUBMODULE_PATH" ]]; then
  printf 'ERROR: submodule target missing: %s\n' "$SUBMODULE_PATH" >&2
  printf '       Run: git submodule update --init external/reverse-skill\n' >&2
  exit 1
fi

if [[ ! -f "$RULES_FILE" ]]; then
  printf 'ERROR: RULES.md target missing: %s\n' "$RULES_FILE" >&2
  printf '       Refusing to claim shield succeeded.\n' >&2
  exit 2
fi

RULES_FILE="$RULES_FILE" python3 - <<'PY'
import os
import re
import shutil
import tempfile
from pathlib import Path

rules_file = Path(os.environ["RULES_FILE"])
marker = "<!-- SHIELDED-BY-ULTRASKILLS -->"
backup = rules_file.with_name("RULES.md.original.bak")

pattern1 = re.compile(
    r"^## Global Injection \(MUST do on first use\).*?(?=^---\n\n## Trigger Keywords)",
    re.DOTALL | re.MULTILINE,
)
pattern2 = re.compile(
    r"^## Global Injection Content \(Compact.*?(?=^---|\Z)",
    re.DOTALL | re.MULTILINE,
)
replacement1 = """## ⚠️ Global Injection — DISABLED BY ULTRASKILLS

> **原 RULES.md 在此处要求 AI 写入用户全局配置文件 (`~/.claude/CLAUDE.md` 等) —
> 已被本仓库屏蔽**。该指令会劫持用户所有 Claude Code 会话，与 ultraskills
> 的 non-invasive skill 原则冲突。
>
> **替代方案**：用户可手动复制本 RULES.md 的核心规则到自己的 CLAUDE.md，
> 或使用 `reverse-skill-router` skill 主动调用本仓库提供的方法论。
>
> **仍可使用**：本 RULES.md 其余功能（routing / trigger keywords / 安全审计 /
> 工具 bootstrap）保持不变。

---

## Trigger Keywords"""
replacement2 = """## ⚠️ DEPRECATED: Global Injection Content (Compact) — ULTRASKILLS SHIELDED

> 该段原本用于写入全局配置；已被 ultraskills 屏蔽。如需访问原始内容，
> 请查看 `RULES.md.original.bak`。

"""

def count_matches(pattern: re.Pattern[str], text: str) -> int:
    return len(pattern.findall(text))

def assert_safe(text: str) -> None:
    if text.count(marker) != 1:
        raise RuntimeError("shield marker count is not exactly one")
    if count_matches(pattern1, text) != 0:
        raise RuntimeError("Global Injection section still present")
    if count_matches(pattern2, text) != 0:
        raise RuntimeError("Global Injection Content section still present")

text = rules_file.read_text(encoding="utf-8")
if marker in text:
    assert_safe(text)
    print("Already shielded; no changes needed.")
    raise SystemExit(0)

matches1 = count_matches(pattern1, text)
matches2 = count_matches(pattern2, text)
if matches1 != 1 or matches2 != 1:
    raise RuntimeError(
        "refusing unsafe partial patch: expected exactly one match for each "
        f"injection section (got {matches1} and {matches2})"
    )

# Build and validate complete result before touching RULES.md or creating marker.
body = pattern1.sub(replacement1, text, count=1)
body = pattern2.sub(replacement2, body, count=1)
shield_header = """<!-- SHIELDED-BY-ULTRASKILLS -->
<!--
  GLOBAL INJECTION DISABLED BY ULTRASKILLS.
  Original file is preserved in RULES.md.original.bak.
-->
<!-- END ULTRASKILLS SHIELD -->

"""
result = shield_header + body
assert_safe(result)

# Preserve original, then atomically replace RULES.md. Marker appears only in
# the replacement file, never in a partially transformed original.
if not backup.exists():
    shutil.copy2(rules_file, backup)

fd, temporary = tempfile.mkstemp(prefix=f".{rules_file.name}.", dir=rules_file.parent)
try:
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as output:
        output.write(result)
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, rules_file)
except Exception:
    try:
        os.unlink(temporary)
    except FileNotFoundError:
        pass
    raise

# Verify the on-disk result after atomic replacement.
assert_safe(rules_file.read_text(encoding="utf-8"))
print("RULES.md patched: 2 sections shielded; atomic replacement verified.")
PY

printf 'Shield complete: %s\n' "$RULES_FILE"
printf 'Original backup: %s\n' "$RULES_FILE.original.bak"
