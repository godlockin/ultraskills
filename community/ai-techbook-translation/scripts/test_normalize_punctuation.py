import importlib.util
from pathlib import Path
import unittest


SCRIPT = Path(__file__).with_name("normalize_punctuation.py")
SPEC = importlib.util.spec_from_file_location("normalize_punctuation", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class NormalizePunctuationTests(unittest.TestCase):
    def test_normalizes_ordinary_chinese_text(self):
        self.assertEqual(
            MODULE.normalize_line_punctuation("这是中文,需要规范化:确定吗? 是"),
            "这是中文，需要规范化：确定吗？ 是",
        )

    def test_preserves_fenced_code(self):
        content = "说明,如下:\n```python\nprint(中文,测试?)\n```\n结束,"
        expected = "说明，如下：\n```python\nprint(中文,测试?)\n```\n结束，"
        self.assertEqual(MODULE.normalize_content(content), expected)

    def test_preserves_inline_code(self):
        content = "调用,然后 `函数(中文,测试?)`，继续。"
        expected = "调用，然后 `函数(中文,测试?)`，继续。"
        self.assertEqual(MODULE.normalize_content(content), expected)

    def test_preserves_dollar_math(self):
        content = "公式 $f(x)=中文,测试?$，然后说明,结束。"
        expected = "公式 $f(x)=中文,测试?$，然后说明，结束。"
        self.assertEqual(MODULE.normalize_content(content), expected)

    def test_preserves_display_math(self):
        content = "$$中文,测试?$$\n\\(中文,测试?\\)\n\\[中文,测试?\\]"
        self.assertEqual(MODULE.normalize_content(content), content)

    def test_preserves_url_literal(self):
        content = "链接,请访问 https://example.com/中文?x=1&y=中文,测试，然后说明,结束。"
        expected = "链接，请访问 https://example.com/中文?x=1&y=中文,测试，然后说明，结束。"
        self.assertEqual(MODULE.normalize_content(content), expected)


if __name__ == "__main__":
    unittest.main()
