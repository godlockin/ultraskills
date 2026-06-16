#!/usr/bin/env python3
"""
Health gate parser — converts SkillSpector JSON output into a list of warnings
suitable for the UltraSkills health-check pipeline.

Used by the skill-manager check (Stage 2.5).

Decision bands (matches SKILL.md matrix):
  - score < 30, no criticals  -> SAFE       -> 0 warnings
  - score 30-69, no criticals -> CAUTION    -> 1 warning
  - score >= 70 OR any critical pattern -> DO NOT INSTALL -> 2+ warnings

Returns:
  List[str] of human-readable warnings. Empty list = clean.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

REPO_ROOT = Path(__file__).resolve().parents[3]
WRAPPER = REPO_ROOT / "devops" / "skill-security-scan" / "scripts" / "run_skillspector.py"

CAUTION_THRESHOLD = 30
BLOCK_THRESHOLD = 70


def skillspector_available() -> bool:
    """True if the skillspector CLI is installed and importable."""
    if shutil.which("skillspector"):
        return True
    candidate = REPO_ROOT / "external" / "skillspector" / ".venv" / "bin" / "skillspector"
    return candidate.exists()


def run_scan(skill_dir: str, timeout: int = 120) -> Optional[dict]:
    """Run SkillSpector on a skill, return parsed JSON or None on failure."""
    try:
        result = subprocess.run(
            [
                sys.executable, str(WRAPPER),
                skill_dir,
                "--no-llm",
                "--format", "json",
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0 and not result.stdout:
            return None
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return None


def classify(report: dict) -> tuple[str, int, list[str]]:
    """
    Return (band, score, critical_patterns).
    band in {"SAFE", "CAUTION", "DO_NOT_INSTALL"}.
    """
    score = int(report.get("risk_score", 0))
    findings = report.get("findings", [])
    critical = [f.get("pattern", "?") for f in findings
                if f.get("severity", "").lower() in ("critical", "high")]

    if score >= BLOCK_THRESHOLD or critical:
        band = "DO_NOT_INSTALL"
    elif score >= CAUTION_THRESHOLD:
        band = "CAUTION"
    else:
        band = "SAFE"
    return band, score, critical


def check_security_scan(skill_dir: str) -> List[str]:
    """
    Scan a single skill via SkillSpector and return warnings.

    Drop-in helper for the skill-manager health-check pipeline.
    Returns [] if scan passes (SAFE) or skill is not a community/external skill.
    """
    skill_name = Path(skill_dir).name
    warnings: List[str] = []

    if not skillspector_available():
        return [
            f"WARN: [{skill_name}] security scan skipped: skillspector CLI not found",
            f"WARN:        install with: pip install -e external/skillspector/",
        ]

    report = run_scan(skill_dir)
    if report is None:
        return [
            f"WARN: [{skill_name}] security scan failed (scan error or invalid JSON)"
        ]

    band, score, critical = classify(report)

    if band == "SAFE":
        return []

    prefix = "ERROR" if band == "DO_NOT_INSTALL" else "WARN"
    warnings.append(
        f"{prefix}: [{skill_name}] security scan: {band} (risk score: {score})"
    )

    if critical:
        warnings.append(
            f"{prefix}: [{skill_name}] critical patterns detected: {', '.join(critical)}"
        )

    findings = report.get("findings", [])
    for f in findings[:5]:  # surface up to 5 findings inline
        pattern = f.get("pattern", "?")
        severity = f.get("severity", "?")
        warnings.append(
            f"{prefix}: [{skill_name}]   - [{severity}] {pattern}"
        )

    return warnings


if __name__ == "__main__":
    # Manual test: python3 health_gate.py <skill-path>
    if len(sys.argv) < 2:
        print("Usage: health_gate.py <skill-path>", file=sys.stderr)
        sys.exit(1)
    for w in check_security_scan(sys.argv[1]):
        print(w)
