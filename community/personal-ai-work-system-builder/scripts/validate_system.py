#!/usr/bin/env python3
"""
validate_system.py — 校验 personal-ai-work-system-builder 的结构完整性与完成标准

Usage:
    # 校验 skill 自身结构
    python3 validate_system.py [SKILL_ROOT]

    # 校验用户项目是否满足完成标准 8 条(仅文件存在性)
    python3 validate_system.py --check-done PROJECT_ROOT

    # 严格模式:额外校验档案内容(必填字段/状态枚举/日期新鲜度)
    python3 validate_system.py --check-done PROJECT_ROOT --strict

Exit codes:
    0 = PASS
    1 = FAIL (存在 error)
    2 = 参数错误
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- skill 结构

REQUIRED_REFS = [
    "interview-and-diagnosis.md",
    "interview-questions.md",
    "maturity-and-metrics.md",
    "tool-routing.md",
    "automation-and-safety.md",
    "data-classification.md",
    "output-blueprint.md",
    "build-and-maintain.md",
    "anti-patterns.md",
]

REQUIRED_ASSETS = [
    "SYSTEM-BLUEPRINT.template.md",
    "SYSTEM-STATE.template.md",
    "ASSET-REGISTRY.template.md",
    "AUTOMATION-REGISTRY.template.md",
    "WEEKLY-REVIEW.template.md",
    "STEP-COMPRESSION.template.md",
]

REQUIRED_FRONTMATTER = ["name", "description", "version", "tags"]

# ---------------------------------------------------------------- 完成标准

# (完成标准编号, 说明, 文件名)
DONE_FILES = [
    (1, "入口可达", "00_项目说明与目标.md"),
    (2, "权威来源与主责明确", "01_权威资料与数据口径.md"),
    (3, "SOP 沉淀", "02_SOP与判断规则.md"),
    (3, "模板归档", "03_话术、模板与Skill.md"),
    (8, "执行记录", "04_执行记录与案例.md"),
    (7, "复盘机制", "05_复盘、指标与迭代版本.md"),
    (1, "系统蓝图", "SYSTEM-BLUEPRINT.md"),
    (7, "运行状态", "SYSTEM-STATE.md"),
    (3, "资产登记", "ASSET-REGISTRY.md"),
    (4, "自动化登记", "AUTOMATION-REGISTRY.md"),
    (6, "步骤压缩", "STEP-COMPRESSION.md"),
]

AUTOMATION_STATES = {"手动", "AI辅助", "半自动", "全自动", "规划中"}

CAPABILITY_STATES = {
    "已连接可执行",
    "已连接只读",
    "可生成草稿",
    "需登录",
    "需授权",
    "需插件或API",
    "规划中",
    "不可用",
}

HIGH_RISK_KEYWORDS = (
    "付款",
    "退款",
    "转账",
    "支付",
    "审批",
    "删除",
    "权限",
    "解雇",
    "录用",
    "批量",
    "群发",
    "触达",
)

NO_REVIEW_MARKERS = ("无", "不需要", "none", "n/a", "-", "—", "")

DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
# 量化指标必须是非零数值 + 单位
METRIC_RE = re.compile(r"(?<!\d)[1-9]\d*(?:\.\d+)?\s*(?:min|分钟|h|小时|%|次|元|天|人)")
SECRET_RE = re.compile(
    r"(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[A-Z0-9]{16}"
    r"|(?:password|passwd|secret|token|api[_-]?key)\s*[:=]\s*[\"']?[A-Za-z0-9/_+\-]{12,})",
    re.IGNORECASE,
)

PLACEHOLDER_MARKERS = ("{{", "____", "<!-- TODO")
# 行首示例前缀(只在行首生效,防止被用来隐藏违规行)
EXAMPLE_PREFIXES = ("例:", "例：", "示例:", "示例：", "e.g.")
# 空值/占位标记
EMPTY_MARKERS = {
    "",
    "-",
    "—",
    "–",
    "n/a",
    "na",
    "tbd",
    "todo",
    "待补充",
    "待填",
    "待定",
    "无",
    "暂无",
    "?",
    "??",
    "x",
    "xx",
    "xxx",
}

# 每份档案的最小实质内容量(字符数,去空白)
MIN_ARCHIVE_CHARS = 80


# ---------------------------------------------------------------- 工具函数


def _normalize_state(cell: str) -> str:
    """去掉 emoji / 标点 / 空白,只留中英文与数字,用于状态枚举匹配"""
    return re.sub(r"[^一-鿿A-Za-z0-9]", "", cell)


def _match_state(cells: list[str], valid: set[str]) -> str | None:
    """在一行单元格里找出命中的状态值(容忍装饰字符)"""
    for c in cells:
        norm = _normalize_state(c)
        if not norm:
            continue
        if norm in valid:
            return norm
        # 装饰后仍包含完整状态词(如 "全自动✅" -> "全自动")
        for v in valid:
            if norm == v or (v in norm and len(norm) <= len(v) + 4):
                return v
    return None


def _is_empty_cell(cell: str) -> bool:
    return cell.strip().lower() in EMPTY_MARKERS


def _field_value(text: str, field: str) -> str | None:
    """取 `字段名: 值` 或表格中该字段列的值。返回 None 表示字段不存在。"""
    m = re.search(
        rf"{re.escape(field)}\s*[^\n\S]*[：:]\s*([^\n|]*)",
        text,
    )
    if m:
        return m.group(1).strip().strip("`*_ ←")
    return None


def parse_frontmatter(skill_md: Path) -> dict[str, str]:
    """简易 YAML frontmatter 解析(单行 key: value / 单行 [list])"""
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    block = text[3:end].strip()
    out: dict[str, str] = {}
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("- "):
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def _today() -> _dt.date:
    return _dt.date.today()


def _latest_date(text: str) -> _dt.date | None:
    """取文本中最新的 YYYY-MM-DD 日期"""
    dates: list[_dt.date] = []
    for y, m, d in DATE_RE.findall(text):
        try:
            dates.append(_dt.date(int(y), int(m), int(d)))
        except ValueError:
            continue
    return max(dates) if dates else None


def _field_date(text: str, field: str) -> _dt.date | None:
    """只取指定字段同一行上的日期,防止用别处的近期日期冒充新鲜度"""
    m = re.search(rf"{re.escape(field)}[^\n]*?(\d{{4}}-\d{{2}}-\d{{2}})", text)
    if not m:
        return None
    try:
        return _dt.date(*(int(x) for x in m.group(1).split("-")))
    except ValueError:
        return None


def _table_rows(
    text: str, min_cols: int = 2, min_filled_ratio: float = 0.6
) -> tuple[list[list[str]], list[list[str]]]:
    """提取 markdown 表格数据行。

    返回 (有效数据行, 被示例前缀过滤掉的行)。

    有效行要求:列数 ≥ min_cols,且非空单元格占比 ≥ min_filled_ratio。
    示例行只在**行首**出现 例:/示例:/e.g. 时才过滤,并单独返回以便检测
    "用示例前缀隐藏违规行" 的规避手法。
    """
    rows: list[list[str]] = []
    filtered: list[list[str]] = []
    prev_was_header = False
    in_table = False
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            in_table = False  # 表格结束,下一个 | 行是新表的表头
            prev_was_header = False
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if not cells:
            continue
        if all(set(c) <= set("-: ") for c in cells):
            # 分隔行 → 确认上一行是表头,后续为数据
            in_table = True
            prev_was_header = False
            continue
        if not in_table and not prev_was_header:
            prev_was_header = True
            continue  # 表头行(等待分隔行)
        if not in_table:
            continue  # 尚未见到分隔行,仍在表头区
        first = cells[0].lstrip("*` ")
        if any(first.startswith(p) for p in EXAMPLE_PREFIXES):
            filtered.append(cells)
            continue
        joined = " ".join(cells)
        if any(marker in joined for marker in PLACEHOLDER_MARKERS):
            filtered.append(cells)
            continue
        if len(cells) < min_cols:
            continue
        filled = sum(1 for c in cells if not _is_empty_cell(c))
        if filled / len(cells) < min_filled_ratio:
            continue
        rows.append(cells)
    return rows, filtered


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _substantive(text: str) -> bool:
    """档案是否有实质内容(去空白后 ≥ MIN_ARCHIVE_CHARS 字符)"""
    return len(re.sub(r"\s", "", text)) >= MIN_ARCHIVE_CHARS


# ---------------------------------------------------------------- skill 校验


def check_skill(root: Path) -> list[str]:
    errors: list[str] = []
    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        return ["SKILL.md 缺失"]

    fm = parse_frontmatter(skill_md)
    for key in REQUIRED_FRONTMATTER:
        if key not in fm:
            errors.append(f"SKILL.md frontmatter 缺 {key}")
        elif not fm[key]:
            errors.append(f"SKILL.md frontmatter {key} 为空")
    tags = fm.get("tags", "")
    if tags and not (tags.startswith("[") and tags.endswith("]") and len(tags) > 2):
        errors.append("SKILL.md frontmatter tags 不是非空列表")

    refs_dir = root / "references"
    if not refs_dir.is_dir():
        errors.append("references/ 目录缺失")
    else:
        for name in REQUIRED_REFS:
            if not (refs_dir / name).exists():
                errors.append(f"references/{name} 缺失")

    assets_dir = root / "assets"
    if not assets_dir.is_dir():
        errors.append("assets/ 目录缺失")
    else:
        for name in REQUIRED_ASSETS:
            if not (assets_dir / name).exists():
                errors.append(f"assets/{name} 缺失")

    examples_dir = root / "examples"
    if not examples_dir.is_dir():
        errors.append("examples/ 目录缺失")
    elif not list(examples_dir.glob("case-*.md")):
        errors.append("examples/ 无 case study (需 ≥1 个 case-*.md)")

    return errors


# ---------------------------------------------------------------- 完成标准校验


def check_done_files(project_root: Path) -> list[str]:
    """基础:文件存在性"""
    if not project_root.is_dir():
        return [f"项目根目录不存在: {project_root}"]
    errors: list[str] = []
    for num, label, filename in DONE_FILES:
        if not (project_root / filename).exists():
            errors.append(f"[完成标准 {num}] {label} 缺失: {filename}")
    return errors


def check_done_strict(project_root: Path) -> tuple[list[str], list[str]]:
    """严格模式:校验档案内容。返回 (errors, warnings)

    设计原则:**空文件不得静默跳过**。每个档案先检查实质内容量,
    再检查具体字段,避免"清空文件即免检"的绕过。
    """
    errors: list[str] = []
    warnings: list[str] = []

    # --- 所有档案的最小实质内容门槛(堵住"清空即免检") ---
    for num, label, filename in DONE_FILES:
        path = project_root / filename
        if not path.exists():
            continue  # 存在性已由 check_done_files 报告
        text = _read(path)
        if not _substantive(text):
            errors.append(
                f"[完成标准 {num}] {filename} 内容不足"
                f"(去空白后 <{MIN_ARCHIVE_CHARS} 字符),不构成有效证据"
            )

    # --- 完成标准 1 + 5: 入口可达 / 下一条工作流 ---
    bp_text = _read(project_root / "SYSTEM-BLUEPRINT.md")
    for field, num in (("入口位置", 1), ("示例指令", 1), ("下一条待接通流程", 5)):
        value = _field_value(bp_text, field)
        if value is None:
            errors.append(f"[完成标准 {num}] SYSTEM-BLUEPRINT.md 缺「{field}」字段")
        elif _is_empty_cell(value) or len(value.strip()) < 2:
            errors.append(
                f"[完成标准 {num}] SYSTEM-BLUEPRINT.md「{field}」未填写实质内容(当前: {value!r})"
            )
    if SECRET_RE.search(bp_text):
        errors.append("[安全] SYSTEM-BLUEPRINT.md 疑似包含明文密钥/token,必须移除并轮换")

    # --- 完成标准 2: 资料源/主责/人审/输出(必须是表格里的非空值,不是提到字段名) ---
    src_text = _read(project_root / "01_权威资料与数据口径.md")
    src_rows, _ = _table_rows(src_text, min_cols=4)
    if not src_rows:
        errors.append(
            "[完成标准 2] 01_权威资料与数据口径.md 无有效数据行"
            "(需 ≥1 行含 权威来源/主责/人工确认/输出 四列且均非空)"
        )
    else:
        header_ok = all(
            f in src_text for f in ("权威来源", "主责", "人工确认", "输出")
        )
        if not header_ok:
            errors.append(
                "[完成标准 2] 01_权威资料与数据口径.md 表头缺 权威来源/主责/人工确认/输出"
            )
        if not any(
            sum(1 for c in cells if not _is_empty_cell(c)) >= 4 for cells in src_rows
        ):
            errors.append(
                "[完成标准 2] 01_权威资料与数据口径.md 无任何行的四个字段同时非空"
            )

    # --- 完成标准 3: 资产登记(路径 + 版本 + 责任人) ---
    asset_text = _read(project_root / "ASSET-REGISTRY.md")
    asset_rows, asset_filtered = _table_rows(asset_text, min_cols=3)
    if not asset_rows:
        errors.append("[完成标准 3] ASSET-REGISTRY.md 无有效资产行(需 ≥1 条真实数据)")
    elif not any(
        DATE_RE.search(" ".join(cells)) or re.search(r"v\d", " ".join(cells))
        for cells in asset_rows
    ):
        errors.append("[完成标准 3] ASSET-REGISTRY.md 无任何资产带版本号或日期,无法追溯")
    if asset_filtered:
        warnings.append(
            f"ASSET-REGISTRY.md 有 {len(asset_filtered)} 行被识别为示例/占位并跳过"
        )

    # --- 完成标准 4: 自动化状态 ---
    auto_text = _read(project_root / "AUTOMATION-REGISTRY.md")
    auto_rows, auto_filtered = _table_rows(auto_text, min_cols=4)
    if not auto_rows:
        errors.append("[完成标准 4] AUTOMATION-REGISTRY.md 无有效自动化行")
    # 检测"用示例前缀隐藏违规行"
    for cells in auto_filtered:
        row_text = " ".join(cells)
        hidden_state = _match_state(cells, AUTOMATION_STATES)
        if hidden_state or any(kw in row_text for kw in HIGH_RISK_KEYWORDS):
            errors.append(
                f"[安全] AUTOMATION-REGISTRY.md 疑似用示例前缀规避校验: "
                f"被跳过的行含真实状态或高风险动作 — {cells[0][:40]!r}"
            )

    stateful_rows = 0
    active_rows = 0
    # 只有含状态值的行属于主登记表;其他表(异常与停止条件/测试记录等)不做状态校验
    registry_rows = [c for c in auto_rows if _match_state(c, AUTOMATION_STATES)]
    if auto_rows and not registry_rows:
        errors.append(
            f"[完成标准 4] AUTOMATION-REGISTRY.md 无任何行的状态命中 5 状态枚举 "
            f"{sorted(AUTOMATION_STATES)}(不得用装饰字符或自定义措辞)"
        )
    for cells in registry_rows:
        row_text = " ".join(cells)
        state = _match_state(cells, AUTOMATION_STATES)
        stateful_rows += 1
        if state != "规划中":
            active_rows += 1
            # 非"规划中"的自动化必须有测试日期
            if not DATE_RE.search(row_text):
                errors.append(
                    f"[完成标准 4] AUTOMATION-REGISTRY.md「{cells[0][:30]}」状态为「{state}」"
                    f"但无「最后测试」日期"
                )
        if state == "全自动":
            latest = _latest_date(row_text)
            if latest is None:
                errors.append(
                    f"[完成标准 4] AUTOMATION-REGISTRY.md 标注「全自动」但无「最后测试」日期: {cells[0][:30]}"
                )
            else:
                age = (_today() - latest).days
                if age > 30:
                    errors.append(
                        f"[完成标准 4] 「全自动」测试记录已过期 {age} 天(>30),必须降级为「规划中」: {cells[0][:30]}"
                    )
                elif age > 7:
                    errors.append(
                        f"[完成标准 4] 「全自动」测试记录已 {age} 天(>7),必须降级为「半自动」: {cells[0][:30]}"
                    )
        # --- 高风险动作 ---
        if any(kw in row_text for kw in HIGH_RISK_KEYWORDS):
            if not _has_review(cells):
                errors.append(
                    f"[安全] AUTOMATION-REGISTRY.md 高风险动作「{cells[0][:30]}」人审点为空或缺失,"
                    f"高风险动作不得无人审自动执行"
                )
            if state == "全自动":
                errors.append(
                    f"[安全] AUTOMATION-REGISTRY.md 高风险动作「{cells[0][:30]}」标注「全自动」,"
                    f"付款/退款/删除/权限变更/批量触达类动作最高只能是「半自动」"
                )
    if registry_rows and active_rows == 0:
        errors.append(
            "[完成标准 4/8] AUTOMATION-REGISTRY.md 所有行都是「规划中」— "
            "与完成标准 8「第一闭环已经真实输入验证」矛盾,需至少 1 条 AI辅助/半自动/全自动"
        )

    # --- 完成标准 6: 步骤压缩 + 量化指标 + 压缩率 ---
    comp_text = _read(project_root / "STEP-COMPRESSION.md")
    comp_rows, _ = _table_rows(comp_text, min_cols=3)
    if not comp_rows:
        errors.append("[完成标准 6] STEP-COMPRESSION.md 无有效数据行(需 ≥1 条真实压缩记录)")
    else:
        if not any(METRIC_RE.search(" ".join(cells)) for cells in comp_rows):
            errors.append(
                "[完成标准 6] STEP-COMPRESSION.md 无有效量化指标"
                "(需非零数字+单位,如 90min / 60% / 3次;0min 不算)"
            )
        best_ratio = None
        for cells in comp_rows:
            nums = [
                int(c)
                for c in cells
                if re.fullmatch(r"\d+", c.strip()) and int(c) >= 0
            ]
            if len(nums) >= 2:
                before, after = nums[0], nums[1]
                if before > 0:
                    ratio = (before - after) / before
                    best_ratio = ratio if best_ratio is None else max(best_ratio, ratio)
        if best_ratio is not None:
            if best_ratio <= 0:
                errors.append(
                    f"[完成标准 6] STEP-COMPRESSION.md 最优压缩率 {best_ratio:.0%} ≤ 0 — "
                    f"步骤未被消除或合并,不构成系统升级"
                )
            elif best_ratio < 0.30:
                warnings.append(
                    f"STEP-COMPRESSION.md 最优压缩率仅 {best_ratio:.0%}(<30%),"
                    f"按 SKILL.md 标准属微优化,不构成「系统升级」"
                )

    # --- 完成标准 7: 状态新鲜度(定向取「最后验证」同行日期) ---
    state_text = _read(project_root / "SYSTEM-STATE.md")
    if "最后验证" not in state_text:
        errors.append("[完成标准 7] SYSTEM-STATE.md 缺「最后验证」字段")
    else:
        verified = _field_date(state_text, "最后验证")
        if verified is None:
            errors.append(
                "[完成标准 7] SYSTEM-STATE.md「最后验证」同一行上无有效日期(YYYY-MM-DD)"
            )
        else:
            age = (_today() - verified).days
            if age < 0:
                errors.append(
                    f"[完成标准 7] SYSTEM-STATE.md「最后验证」是未来日期 {verified},无效"
                )
            elif age > 30:
                errors.append(
                    f"[完成标准 7] SYSTEM-STATE.md 最后验证已过期 {age} 天(>30),不可作为「系统可续」证据"
                )
            elif age > 14:
                warnings.append(f"SYSTEM-STATE.md 最后验证 {age} 天前,建议尽快复验")
    state_rows, _ = _table_rows(state_text, min_cols=3)
    for cells in state_rows:
        if _match_state(cells, CAPABILITY_STATES) is None:
            suspicious = [c for c in cells if _looks_like_state(c)]
            if suspicious:
                warnings.append(
                    f"SYSTEM-STATE.md 状态值疑似不在值域内: {suspicious}"
                )

    # --- 完成标准 8: 执行记录四要素(表头 + 数据行都要有实质内容) ---
    rec_text = _read(project_root / "04_执行记录与案例.md")
    missing = [f for f in ("输入", "输出", "耗时", "异常") if f not in rec_text]
    if missing:
        errors.append(
            f"[完成标准 8] 04_执行记录与案例.md 缺四要素: {missing}(需 输入版本/输出位置/耗时/异常)"
        )
    rec_rows, _ = _table_rows(rec_text, min_cols=4)
    if not rec_rows:
        errors.append(
            "[完成标准 8] 04_执行记录与案例.md 无有效运行记录行"
            "(需 ≥1 行四列以上且均非空)"
        )
    else:
        dated = [c for c in rec_rows if DATE_RE.search(" ".join(c))]
        if not dated:
            errors.append("[完成标准 8] 04_执行记录与案例.md 无任何带日期的运行记录")
        elif not any(METRIC_RE.search(" ".join(c)) for c in dated):
            errors.append(
                "[完成标准 8] 04_执行记录与案例.md 运行记录无有效耗时"
                "(需非零数字+单位,如 4min)"
            )

    # --- 全局密钥扫描 ---
    for path in sorted(project_root.glob("*.md")):
        if path.name == "SYSTEM-BLUEPRINT.md":
            continue  # 已单独检查
        if SECRET_RE.search(_read(path)):
            errors.append(f"[安全] {path.name} 疑似包含明文密钥/token,必须移除并轮换")

    return errors, warnings


def _looks_like_state(cell: str) -> bool:
    """粗略判断一个单元格是否想表达"状态"。

    只在单元格与某个合法状态值高度相似时才判定为"状态列",避免把
    「接自动解析」这类下一步描述误判成状态值。
    """
    text = cell.strip()
    if not text or len(text) > 8:
        return False
    for valid in CAPABILITY_STATES:
        # 与合法状态共享 ≥3 个连续字符,视为想写该状态但写错
        for size in range(len(valid), 2, -1):
            for start in range(len(valid) - size + 1):
                if valid[start : start + size] in text:
                    return True
    return False


def _has_review(cells: list[str]) -> bool:
    """判断该行是否存在实质的人审描述"""
    review_hints = ("人审", "人工", "确认", "审批", "复核", "双人", "GO-YES")
    for c in cells:
        stripped = c.strip().lower()
        if stripped in NO_REVIEW_MARKERS:
            continue
        if any(h in c for h in review_hints):
            return True
    return False


# ---------------------------------------------------------------- main


def main() -> int:
    parser = argparse.ArgumentParser(
        description="personal-ai-work-system-builder 结构与完成标准校验"
    )
    parser.add_argument(
        "skill_root", nargs="?", default=".", help="skill 根目录(含 SKILL.md)"
    )
    parser.add_argument(
        "--check-done", metavar="PROJECT_ROOT", help="校验用户项目的完成标准"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="(默认已开启)严格模式:校验档案内容",
    )
    parser.add_argument(
        "--lenient",
        action="store_true",
        help="仅检查文件存在性,不校验内容 — 结果不构成完成标准证据",
    )
    args = parser.parse_args()

    if (args.strict or args.lenient) and not args.check_done:
        print(
            "Result: ERROR — --strict / --lenient 必须与 --check-done 一起使用",
            file=sys.stderr,
        )
        return 2
    if args.strict and args.lenient:
        print("Result: ERROR — --strict 与 --lenient 互斥", file=sys.stderr)
        return 2

    # 默认严格
    strict = not args.lenient

    errors: list[str] = []
    warnings: list[str] = []

    skill_root = Path(args.skill_root).resolve()
    errors.extend(check_skill(skill_root))

    checked_done = False
    if args.check_done:
        project = Path(args.check_done).resolve()
        errors.extend(check_done_files(project))
        checked_done = True
        if strict:
            strict_errors, strict_warnings = check_done_strict(project)
            errors.extend(strict_errors)
            warnings.extend(strict_warnings)
        else:
            warnings.append(
                "已用 --lenient:仅验证文件存在性,不构成完成标准证据。"
                "正式验收请去掉 --lenient。"
            )

    for w in warnings:
        print(f"  ⚠️  {w}")

    if errors:
        print("Result: FAIL")
        for e in errors:
            print(f"  ❌ {e}")
        return 1

    print("Result: PASS")
    print("  ✓ SKILL.md frontmatter 完整")
    print(f"  ✓ {len(REQUIRED_REFS)} 个 references 齐备")
    print(f"  ✓ {len(REQUIRED_ASSETS)} 个 assets 模板齐备")
    print("  ✓ examples/ ≥1 个 case study")
    if checked_done:
        print("  ✓ 完成标准档案文件齐备")
        if strict:
            print(
                "  ✓ 严格模式:内容量 / 必填字段 / 状态枚举 / 压缩率 / "
                "日期新鲜度 / 密钥扫描 全部通过"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())