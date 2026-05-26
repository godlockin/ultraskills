#!/usr/bin/env python3
"""
audit.py - Audit user's Claude Code plugins and skills configuration.

Detects:
1. Plugin redundancy with ultraskills
2. Low-quality skills (score < 5.0, broken descriptions)
3. Context overhead (niche skills, translations)
4. Duplicate skills

Usage:
    python3 audit.py           # Summary report
    python3 audit.py --full    # Detailed report
    python3 audit.py --json    # JSON output
    python3 audit.py --fix     # Auto-fix redundant plugins
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Paths
HOME = Path.home()
CLAUDE_DIR = HOME / ".claude"
SETTINGS_FILE = CLAUDE_DIR / "settings.json"
PLUGINS_CACHE = CLAUDE_DIR / "plugins" / "installed_plugins.json"
SKILLS_DIR = CLAUDE_DIR / "skills"

# Ultraskills paths (relative to script location)
SCRIPT_DIR = Path(__file__).parent
ULTRASKILLS_ROOT = SCRIPT_DIR.parent.parent.parent
INDEX_FILE = ULTRASKILLS_ROOT / "index.json"


def load_json(path: Path) -> Optional[dict]:
    """Load JSON file, return None if not found."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return None


def get_enabled_plugins(settings: dict) -> List[str]:
    """Extract enabled plugin names from settings."""
    plugins = settings.get("enabledPlugins", {})
    return [name for name, enabled in plugins.items() if enabled]


def get_plugin_skills(plugin_cache: dict, plugin_name: str) -> List[str]:
    """Get skill IDs from a plugin's cache directory."""
    plugins_info = plugin_cache.get("plugins", {})
    plugin_data = plugins_info.get(plugin_name, [])

    if not plugin_data:
        return []

    # Get install path from first entry
    install_path = plugin_data[0].get("installPath", "")
    if not install_path:
        return []

    skills_dir = Path(install_path) / "skills"
    if not skills_dir.exists():
        return []

    return [d.name for d in skills_dir.iterdir() if d.is_dir()]


def find_redundant_plugins(
    enabled_plugins: List[str],
    plugin_cache: dict,
    ultraskills_index: dict
) -> List[Dict]:
    """Find plugins whose skills are already in ultraskills."""
    redundant = []

    # Build set of ultraskills IDs
    ultraskills_ids = {s["id"] for s in ultraskills_index.get("skills", [])}

    # Known plugin -> ultraskills mapping
    KNOWN_MAPPINGS = {
        "superpowers@claude-plugins-official": [
            "brainstorming", "dispatching-parallel-agents", "executing-plans",
            "finishing-a-development-branch", "receiving-code-review",
            "requesting-code-review", "subagent-driven-development",
            "systematic-debugging", "test-driven-development",
            "using-git-worktrees", "using-superpowers",
            "verification-before-completion", "writing-plans", "writing-skills"
        ],
        "fullstack-dev-skills@fullstack-dev-skills": "external/fullstack-dev-skills",
        "planning-with-files@community": ["planning-with-files"],
        "frontend-design@claude-plugins-official": ["frontend-design"],
    }

    for plugin in enabled_plugins:
        # Skip non-skill plugins
        if "lsp" in plugin.lower():
            continue

        overlap = []
        source = None

        if plugin in KNOWN_MAPPINGS:
            mapping = KNOWN_MAPPINGS[plugin]
            if isinstance(mapping, list):
                overlap = [s for s in mapping if s in ultraskills_ids]
            else:
                # It's a path reference
                source = mapping
                # Count skills in that external path
                for s in ultraskills_index.get("skills", []):
                    if mapping in s.get("path", ""):
                        overlap.append(s["id"])
        else:
            # Try to detect from plugin cache
            plugin_skills = get_plugin_skills(plugin_cache, plugin)
            overlap = [s for s in plugin_skills if s in ultraskills_ids]

        if overlap:
            redundant.append({
                "plugin": plugin,
                "overlap_count": len(overlap),
                "overlap_skills": overlap[:10],  # First 10
                "source": source or "community/",
            })

    return redundant


def find_low_quality_skills(ultraskills_index: dict) -> List[Dict]:
    """Find skills with quality issues."""
    issues = []

    for skill in ultraskills_index.get("skills", []):
        problems = []
        arena = skill.get("arena", {})
        score = arena.get("score", 0)
        desc = skill.get("description", "")

        if score < 5.0 and score > 0:
            problems.append(f"low score ({score:.1f})")

        if desc in [">", "|", "", None]:
            problems.append("broken description")

        if skill.get("auxiliary"):
            problems.append("auxiliary (not standalone)")

        if problems:
            issues.append({
                "id": skill["id"],
                "score": score,
                "problems": problems,
                "path": skill.get("path", ""),
            })

    return sorted(issues, key=lambda x: x["score"])


def find_niche_skills(ultraskills_index: dict) -> Dict[str, List[str]]:
    """Categorize niche/specialized skills that could be lazy-loaded."""
    categories = {
        "scientific": [],
        "financial": [],
        "translations": [],
        "deprecated": [],
    }

    SCIENTIFIC_KEYWORDS = [
        "scanpy", "rdkit", "qiskit", "biopython", "deepchem", "cellxgene",
        "opentrons", "benchling", "genomic", "phylogenetic", "molecular",
        "quantum", "neuropixels", "dicom", "histolab", "pathml"
    ]

    FINANCIAL_KEYWORDS = [
        "dcf", "lbo", "comps", "pitch-deck", "ic-memo", "dd-", "kyc",
        "teaser", "cim-builder", "merger-model", "earnings"
    ]

    for skill in ultraskills_index.get("skills", []):
        sid = skill["id"].lower()
        path = skill.get("path", "").lower()

        # Scientific
        if any(kw in sid or kw in path for kw in SCIENTIFIC_KEYWORDS):
            categories["scientific"].append(skill["id"])
            continue

        # Financial
        if any(kw in sid for kw in FINANCIAL_KEYWORDS):
            categories["financial"].append(skill["id"])
            continue

        # Translation variants
        if any(sid.endswith(suf) for suf in ["-ar", "-de", "-es", "-zht", "-ja"]):
            categories["translations"].append(skill["id"])
            continue

    return {k: v for k, v in categories.items() if v}


def estimate_token_savings(redundant_plugins: List[Dict]) -> int:
    """Estimate tokens saved by disabling redundant plugins."""
    # Rough estimate: ~500 tokens per skill loaded
    total_skills = sum(p["overlap_count"] for p in redundant_plugins)
    return total_skills * 500


def fix_redundant_plugins(settings_path: Path, redundant: List[str]) -> bool:
    """Disable redundant plugins in settings.json."""
    settings = load_json(settings_path)
    if not settings:
        return False

    modified = False
    plugins = settings.get("enabledPlugins", {})

    for plugin in redundant:
        if plugins.get(plugin):
            plugins[plugin] = False
            modified = True

    if modified:
        settings_path.write_text(json.dumps(settings, indent=2))

    return modified


def print_report(
    redundant: List[Dict],
    low_quality: List[Dict],
    niche: Dict[str, List[str]],
    token_savings: int,
    full: bool = False
):
    """Print human-readable audit report."""
    total_skills = sum(len(v) for v in niche.values())

    print("╔" + "═" * 62 + "╗")
    print("║" + "SKILLS AUDIT REPORT".center(62) + "║")
    print("╠" + "═" * 62 + "╣")
    print(f"║ Redundant plugins:   {len(redundant):<40} ║")
    print(f"║ Low-quality skills:  {len(low_quality):<40} ║")
    print(f"║ Niche skills:        {total_skills:<40} ║")
    print(f"║ Est. token savings:  ~{token_savings:,} tokens/session{' ' * 20} ║")
    print("╚" + "═" * 62 + "╝")

    if redundant:
        print("\n⚠️  REDUNDANT PLUGINS")
        for p in redundant:
            print(f"   {p['plugin']}")
            print(f"     → {p['overlap_count']} skills already in ultraskills")
            if full and p['overlap_skills']:
                skills_str = ", ".join(p['overlap_skills'][:5])
                if p['overlap_count'] > 5:
                    skills_str += f", ... (+{p['overlap_count'] - 5} more)"
                print(f"       Examples: {skills_str}")
            print(f"     💡 Disable plugin, use ultraskills-hub instead")
            print()

    if low_quality and full:
        print("\n⚠️  LOW-QUALITY SKILLS")
        for s in low_quality[:10]:
            problems = ", ".join(s["problems"])
            print(f"   {s['id']:30} score={s['score']:.1f}  [{problems}]")
        if len(low_quality) > 10:
            print(f"   ... +{len(low_quality) - 10} more")
        print()

    if niche and full:
        print("\n📦 NICHE SKILLS (candidates for lazy-load)")
        for category, skills in niche.items():
            print(f"   {category}: {len(skills)} skills")
            if len(skills) <= 5:
                print(f"     {', '.join(skills)}")
            else:
                print(f"     {', '.join(skills[:5])}, ... (+{len(skills) - 5} more)")
        print()

    print("\n💡 RECOMMENDATIONS:")
    rec_num = 1
    if redundant:
        print(f"   {rec_num}. Disable {len(redundant)} redundant plugins (run with --fix)")
        rec_num += 1
    if niche.get("scientific"):
        print(f"   {rec_num}. Consider lazy-loading {len(niche['scientific'])} scientific skills")
        rec_num += 1
    if niche.get("translations"):
        print(f"   {rec_num}. Remove {len(niche['translations'])} translation variants (use i18n)")
        rec_num += 1
    if not redundant and not niche:
        print("   ✅ Configuration looks good!")


def main():
    parser = argparse.ArgumentParser(description="Audit Claude Code skills configuration")
    parser.add_argument("--full", action="store_true", help="Show detailed report")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--fix", action="store_true", help="Auto-fix redundant plugins")
    args = parser.parse_args()

    # Load data
    settings = load_json(SETTINGS_FILE) or {}
    plugin_cache = load_json(PLUGINS_CACHE) or {}
    ultraskills_index = load_json(INDEX_FILE)

    if not ultraskills_index:
        print(f"❌ Could not load ultraskills index: {INDEX_FILE}")
        sys.exit(1)

    # Analysis
    enabled_plugins = get_enabled_plugins(settings)
    redundant = find_redundant_plugins(enabled_plugins, plugin_cache, ultraskills_index)
    low_quality = find_low_quality_skills(ultraskills_index)
    niche = find_niche_skills(ultraskills_index)
    token_savings = estimate_token_savings(redundant)

    # Fix mode
    if args.fix:
        if not redundant:
            print("✅ No redundant plugins to fix")
            return

        plugins_to_disable = [p["plugin"] for p in redundant]
        if fix_redundant_plugins(SETTINGS_FILE, plugins_to_disable):
            print(f"✅ Disabled {len(plugins_to_disable)} redundant plugins:")
            for p in plugins_to_disable:
                print(f"   - {p}")
            print("\nRestart Claude Code for changes to take effect.")
        else:
            print("❌ Could not update settings.json")
        return

    # Output
    if args.json:
        result = {
            "redundant_plugins": redundant,
            "low_quality_skills": low_quality[:20],
            "niche_skills": niche,
            "token_savings": token_savings,
        }
        print(json.dumps(result, indent=2))
    else:
        print_report(redundant, low_quality, niche, token_savings, full=args.full)


if __name__ == "__main__":
    main()
