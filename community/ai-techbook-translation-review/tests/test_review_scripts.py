import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


generate_report = load_script("generate_report")
audit_translation = load_script("audit_translation")


class AuditTranslationTests(unittest.TestCase):
    def make_chapters(self, target_text):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        source = root / "chapter 01"
        target = root / "第01章"
        source.mkdir()
        target.mkdir()
        (source / "lesson.md").write_text(
            "## Source\n\nFormula $x+y$ and:\n```python\nprint('ok')\n```\n"
            "See [docs](https://example.com/docs).\n",
            encoding="utf-8",
        )
        (target / "lesson.md").write_text(target_text, encoding="utf-8")
        return temp, source, target

    def test_formula_code_and_link_deletions_fail(self):
        target_text = "## 译文\n\n中文说明\n"
        temp, source, target = self.make_chapters(target_text)
        self.addCleanup(temp.cleanup)
        result = audit_translation.audit_chapter(str(source), str(target), 1)
        self.assertTrue(any("formula mismatch" in issue for issue in result["issues"]))
        self.assertTrue(any("code mismatch" in issue for issue in result["issues"]))
        self.assertTrue(any("link mismatch" in issue for issue in result["issues"]))

    def test_unchanged_assets_pass_integrity_checks(self):
        target_text = (
            "## 译文\n\n中文说明\n\n公式 $x+y$：\n"
            "```python\nprint('ok')\n```\n参考 [docs](https://example.com/docs)。\n"
        )
        temp, source, target = self.make_chapters(target_text)
        self.addCleanup(temp.cleanup)
        result = audit_translation.audit_chapter(str(source), str(target), 1)
        self.assertFalse(any("mismatch" in issue for issue in result["issues"]))


class GenerateReportTests(unittest.TestCase):
    def reviews(self, score="10.0"):
        return [
            {"role": role, "content": f"评分: {score} / 10\n"}
            for role in ("terminology", "technical", "rendering", "completeness")
        ]

    def test_empty_reviews_fail_fast(self):
        with self.assertRaises(ValueError):
            generate_report.generate_report("p", {}, [])

    def test_full_critical_reviews_can_pass_without_bonus_review(self):
        report = generate_report.generate_report("p", {}, self.reviews())
        self.assertIn("最终结论**: ✅ **翻译通过", report)
        self.assertIn("必须项总分**: **10.0 / 10", report)

    def test_critical_scan_failure_blocks_pass(self):
        report = generate_report.generate_report(
            "p", {"audit": {"critical": ["missing formula"]}}, self.reviews()
        )
        self.assertIn("最终结论**: ❌", report)
        self.assertIn("自动扫描失败 1 项", report)


if __name__ == "__main__":
    unittest.main()
