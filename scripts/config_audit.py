#!/usr/bin/env python3
"""
config_audit.py - 审计 Claude Code skills/plugins 配置

分析当前系统中的 skills 和 plugins：
1. 启动时必须加载的（高频使用、核心功能）
2. 可通过 ultraskills hub 动态搜索加载的
3. 建议 disable/删除的（重复、未使用、低价值）

Usage:
  python3 scripts/config_audit.py              # 完整审计报告
  python3 scripts/config_audit.py --json       # JSON 输出
  python3 scripts/config_audit.py --apply      # 生成优化命令（不执行）
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# === 配置 ===
SKILLS_DIR = Path.home() / ".claude" / "skills"
REPO_ROOT = Path(__file__).parent.parent
INDEX_FILE = REPO_ROOT / "index.json"

# 核心 skills：启动时必须加载
ESSENTIAL_SKILLS = {
    "eket",           # 任务管理框架
    "ultraskills-hub", # 动态搜索入口
    "checkpoint",     # 会话恢复
    "review",         # 代码审查
    "health",         # 代码健康检查
}

# 核心 plugins：启动时必须启用
ESSENTIAL_PLUGINS = {
    "claude-mem",           # 记忆系统
    "github",               # GitHub 集成
    "playwright",           # 浏览器自动化
    "context7",             # 文档查询
    "serena",               # LSP 代码分析
    "superpowers",          # 技能加载器
    "commit-commands",      # Git 提交
    "security-guidance",    # 安全指导
}

# 可选但有用的 plugins（按需启用）
OPTIONAL_PLUGINS = {
    "code-review",          # PR 审查
    "code-simplifier",      # 代码简化
    "feature-dev",          # 功能开发
    "frontend-design",      # 前端设计
    "huggingface-skills",   # HuggingFace
    "skill-creator",        # 技能创建
    "prompts.chat",         # 提示词管理
    "claude-md-management", # CLAUDE.md 管理
}

# 已知重复/冗余的 plugins（建议 disable）
REDUNDANT_PLUGINS = {
    "agent-architecture@context-engineering-marketplace",    # 与 ultraskills/agent-arch 重复
    "agent-development@context-engineering-marketplace",     # 与 ultraskills 重复
    "agent-evaluation@context-engineering-marketplace",      # 与 ultraskills 重复
    "cognitive-architecture@context-engineering-marketplace",# 与 ultraskills 重复
    "context-engineering-fundamentals@context-engineering-marketplace", # 与 ultraskills 重复
    "superpowers@superpowers-marketplace",                   # 与官方 superpowers 重复
    "superpowers-lab@superpowers-marketplace",               # 实验版，不稳定
    "playwright-cli@playwright-cli",                         # 与官方 playwright 重复
    "double-shot-latte@superpowers-marketplace",             # 与 superpowers 功能重叠
    "claude-session-driver@superpowers-marketplace",         # 功能已被其他工具覆盖
}

# ultraskills 已覆盖的领域（这些 plugins 可通过 hub 动态加载）
ULTRASKILLS_COVERED = {
    "creative-skills@neurofoo-agent-skills",        # ultraskills/creative/
    "learning-skills@neurofoo-agent-skills",        # ultraskills/education/
    "marketing-skills@marketingskills",             # ultraskills/marketing-*
    "prioritization-skills@neurofoo-agent-skills",  # ultraskills/productivity/
    "retrospective-skills@neurofoo-agent-skills",   # ultraskills/business-pm/
    "thinking-frameworks@neurofoo-agent-skills",    # ultraskills/persona/
    "pr-review-toolkit@claude-plugins-official",    # ultraskills/engineering-code/
}


def get_installed_skills():
    """获取已安装的 skills"""
    if not SKILLS_DIR.exists():
        return []
    return [d.name for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith('.')]


def get_plugins():
    """获取 plugins 列表（enabled/disabled）"""
    try:
        result = subprocess.run(
            ["claude", "plugins", "list"],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout
    except Exception as e:
        return {"enabled": [], "disabled": [], "error": str(e)}

    enabled = []
    disabled = []
    current_plugin = None

    for line in output.split('\n'):
        line = line.strip()
        if line.startswith('❯ '):
            current_plugin = line[2:].strip()
        elif 'enabled' in line.lower() and current_plugin:
            enabled.append(current_plugin)
            current_plugin = None
        elif 'disabled' in line.lower() and current_plugin:
            disabled.append(current_plugin)
            current_plugin = None

    return {"enabled": enabled, "disabled": disabled}


def load_ultraskills_index():
    """加载 ultraskills index"""
    if not INDEX_FILE.exists():
        return None
    with open(INDEX_FILE) as f:
        return json.load(f)


def find_ultraskills_equivalent(skill_name, index):
    """查找 ultraskills 中的等效 skill"""
    if not index:
        return None

    skill_name_lower = skill_name.lower().replace('-', '').replace('_', '')

    for s in index.get("skills", []):
        sid = s["id"].lower().replace('-', '').replace('_', '')
        if skill_name_lower in sid or sid in skill_name_lower:
            return s
    return None


def analyze_skill(skill_name, index):
    """分析单个 skill 的加载策略"""
    result = {
        "name": skill_name,
        "recommendation": "unknown",
        "reason": "",
        "ultraskills_equivalent": None,
    }

    # 核心 skill
    if skill_name in ESSENTIAL_SKILLS:
        result["recommendation"] = "keep_startup"
        result["reason"] = "核心功能，启动时必须加载"
        return result

    # 查找 ultraskills 等效
    equiv = find_ultraskills_equivalent(skill_name, index)
    if equiv:
        result["ultraskills_equivalent"] = equiv["id"]
        # 如果是 winner，建议保留
        if equiv.get("arena", {}).get("is_winner"):
            result["recommendation"] = "keep_startup"
            result["reason"] = f"Arena winner，建议保留（cluster: {equiv['arena'].get('cluster_name', '')}）"
        else:
            result["recommendation"] = "move_to_hub"
            result["reason"] = f"可通过 ultraskills-hub 搜索加载（cluster: {equiv['arena'].get('cluster', '')}）"
        return result

    # 未知 skill，建议评估
    result["recommendation"] = "evaluate"
    result["reason"] = "未在 ultraskills 索引中找到，需人工评估"
    return result


def analyze_plugin(plugin_name, index):
    """分析单个 plugin 的加载策略"""
    result = {
        "name": plugin_name,
        "recommendation": "unknown",
        "reason": "",
    }

    # 提取 plugin 基础名
    base_name = plugin_name.split('@')[0] if '@' in plugin_name else plugin_name

    # 核心 plugin
    if base_name in ESSENTIAL_PLUGINS:
        result["recommendation"] = "keep_enabled"
        result["reason"] = "核心功能，必须启用"
        return result

    # 可选但有用
    if base_name in OPTIONAL_PLUGINS:
        result["recommendation"] = "optional"
        result["reason"] = "有用但非必须，按需启用"
        return result

    # 已知冗余
    if plugin_name in REDUNDANT_PLUGINS:
        result["recommendation"] = "disable"
        result["reason"] = "与其他 plugin 或 ultraskills 功能重复"
        return result

    # ultraskills 已覆盖
    if plugin_name in ULTRASKILLS_COVERED:
        result["recommendation"] = "disable"
        result["reason"] = "功能已被 ultraskills 覆盖，可通过 hub 动态加载"
        return result

    # 未知
    result["recommendation"] = "evaluate"
    result["reason"] = "需人工评估是否有用"
    return result


def generate_report(skills_analysis, plugins_analysis):
    """生成审计报告"""
    report = []
    report.append("=" * 60)
    report.append("Claude Code 配置审计报告")
    report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 60)

    # Skills 分析
    report.append("\n## Skills 分析 (~/.claude/skills/)\n")

    by_rec = defaultdict(list)
    for s in skills_analysis:
        by_rec[s["recommendation"]].append(s)

    if by_rec["keep_startup"]:
        report.append(f"### ✅ 保留启动加载 ({len(by_rec['keep_startup'])} 个)")
        for s in by_rec["keep_startup"]:
            report.append(f"  - {s['name']}: {s['reason']}")

    if by_rec["move_to_hub"]:
        report.append(f"\n### 🔄 可移至 Hub 动态加载 ({len(by_rec['move_to_hub'])} 个)")
        for s in by_rec["move_to_hub"]:
            equiv = s.get('ultraskills_equivalent', '')
            report.append(f"  - {s['name']} → ultraskills/{equiv}")

    if by_rec["evaluate"]:
        report.append(f"\n### ❓ 需评估 ({len(by_rec['evaluate'])} 个)")
        for s in by_rec["evaluate"][:20]:  # 只显示前20个
            report.append(f"  - {s['name']}")
        if len(by_rec["evaluate"]) > 20:
            report.append(f"  ... 还有 {len(by_rec['evaluate']) - 20} 个")

    # Plugins 分析
    report.append("\n## Plugins 分析\n")

    by_rec_p = defaultdict(list)
    for p in plugins_analysis:
        by_rec_p[p["recommendation"]].append(p)

    if by_rec_p["keep_enabled"]:
        report.append(f"### ✅ 核心 Plugins ({len(by_rec_p['keep_enabled'])} 个)")
        for p in by_rec_p["keep_enabled"]:
            report.append(f"  - {p['name']}")

    if by_rec_p["optional"]:
        report.append(f"\n### 🔧 可选 Plugins ({len(by_rec_p['optional'])} 个)")
        for p in by_rec_p["optional"]:
            report.append(f"  - {p['name']}: {p['reason']}")

    if by_rec_p["disable"]:
        report.append(f"\n### ❌ 建议 Disable ({len(by_rec_p['disable'])} 个)")
        for p in by_rec_p["disable"]:
            report.append(f"  - {p['name']}: {p['reason']}")

    if by_rec_p["evaluate"]:
        report.append(f"\n### ❓ 需评估 ({len(by_rec_p['evaluate'])} 个)")
        for p in by_rec_p["evaluate"]:
            report.append(f"  - {p['name']}")

    # 优化建议
    report.append("\n## 优化建议\n")

    skills_to_remove = len(by_rec["move_to_hub"])
    plugins_to_disable = len(by_rec_p["disable"])

    report.append(f"- Skills: 可从启动加载移除 {skills_to_remove} 个，通过 hub 动态加载")
    report.append(f"- Plugins: 建议 disable {plugins_to_disable} 个冗余/重复插件")
    report.append(f"- 预计启动时间优化: 减少 {skills_to_remove + plugins_to_disable} 个加载项")

    return "\n".join(report)


def generate_commands(skills_analysis, plugins_analysis):
    """生成优化命令"""
    commands = []
    commands.append("# 优化命令（请检查后执行）\n")

    # Plugin disable 命令
    for p in plugins_analysis:
        if p["recommendation"] == "disable":
            commands.append(f"claude plugins disable {p['name']}")

    # Skills 移除命令（移到 hub 管理）
    commands.append("\n# 以下 skills 可从 ~/.claude/skills/ 移除，通过 ultraskills-hub 加载")
    for s in skills_analysis:
        if s["recommendation"] == "move_to_hub":
            commands.append(f"# rm -rf ~/.claude/skills/{s['name']}  # 等效: ultraskills/{s.get('ultraskills_equivalent', s['name'])}")

    return "\n".join(commands)


def main():
    args = sys.argv[1:]
    json_output = "--json" in args
    show_commands = "--apply" in args

    # 加载数据
    index = load_ultraskills_index()
    installed_skills = get_installed_skills()
    plugins = get_plugins()

    # 分析
    skills_analysis = [analyze_skill(s, index) for s in installed_skills]

    all_plugins = plugins.get("enabled", []) + plugins.get("disabled", [])
    plugins_analysis = [analyze_plugin(p, index) for p in all_plugins]

    # 标记当前状态
    for p in plugins_analysis:
        p["current_status"] = "enabled" if p["name"] in plugins.get("enabled", []) else "disabled"

    if json_output:
        output = {
            "timestamp": datetime.now().isoformat(),
            "skills": {
                "total": len(installed_skills),
                "analysis": skills_analysis,
            },
            "plugins": {
                "enabled": len(plugins.get("enabled", [])),
                "disabled": len(plugins.get("disabled", [])),
                "analysis": plugins_analysis,
            },
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    elif show_commands:
        print(generate_commands(skills_analysis, plugins_analysis))
    else:
        print(generate_report(skills_analysis, plugins_analysis))


if __name__ == "__main__":
    main()
