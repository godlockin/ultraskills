#!/usr/bin/env python3
"""Regression tests for scripts/shield-reverse-skill.sh."""
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "shield-reverse-skill.sh"
FIXTURE = """# reverse-skill rules

## Global Injection (MUST do on first use)

Write routing rules to ~/.claude/CLAUDE.md.

---

## Trigger Keywords

Use routing keywords.

## Global Injection Content (Compact v1)

Write this dangerous content to the global configuration.

---

## Other Rules

Keep local behavior.
"""


class ShieldTest(unittest.TestCase):
    def run_shield(self, target: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT), str(target)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

    def test_normal_patch_and_backup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "reverse-skill"
            target.mkdir()
            rules = target / "RULES.md"
            rules.write_text(FIXTURE, encoding="utf-8")

            result = self.run_shield(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            shielded = rules.read_text(encoding="utf-8")
            self.assertEqual(shielded.count("SHIELDED-BY-ULTRASKILLS"), 1)
            self.assertNotIn("## Global Injection (MUST do on first use)", shielded)
            self.assertNotIn("## Global Injection Content (Compact", shielded)
            self.assertEqual((target / "RULES.md.original.bak").read_text(), FIXTURE)

    def test_pattern_mismatch_is_fail_fast_and_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "reverse-skill"
            target.mkdir()
            rules = target / "RULES.md"
            original = "## Global Injection (MUST do on first use)\nmissing boundary\n"
            rules.write_text(original, encoding="utf-8")

            result = self.run_shield(target)

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(rules.read_text(), original)
            self.assertFalse((target / "RULES.md.original.bak").exists())
            self.assertNotIn("SHIELDED-BY-ULTRASKILLS", rules.read_text())

    def test_repeat_run_is_safe_and_does_not_rewrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "reverse-skill"
            target.mkdir()
            rules = target / "RULES.md"
            rules.write_text(FIXTURE, encoding="utf-8")
            first = self.run_shield(target)
            self.assertEqual(first.returncode, 0, first.stderr)
            before = rules.read_bytes()

            second = self.run_shield(target)

            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(rules.read_bytes(), before)
            self.assertIn("Already shielded", second.stdout)

    def test_missing_target_is_explicit_failure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_shield(Path(directory) / "missing")
            self.assertEqual(result.returncode, 1)
            self.assertIn("target missing", result.stderr)


if __name__ == "__main__":
    unittest.main()
