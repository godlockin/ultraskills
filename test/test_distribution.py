import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import scripts.distribute as distribute


class DistributionTests(unittest.TestCase):
    def test_copy_mode_creates_real_skill_tree(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "community" / "demo"
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text("demo", encoding="utf-8")
            index = root / "index.json"
            index.write_text(json.dumps({"skills": [{"id": "demo", "path": "./community/demo/SKILL.md"}]}), encoding="utf-8")
            destination = root / "installed"
            with patch.object(distribute, "REPO_ROOT", root), patch.object(distribute, "INDEX_FILE", index):
                skills = distribute.load_skills_from_index()
                ok, skipped = distribute.deploy_copy(skills, destination)
            self.assertEqual((ok, skipped), (1, 0))
            self.assertFalse((destination / "demo").is_symlink())
            self.assertEqual((destination / "demo" / "SKILL.md").read_text(), "demo")

    def test_invalid_index_path_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            index = root / "index.json"
            index.write_text(json.dumps({"skills": [{"id": "escape", "path": "../../etc/passwd"}]}), encoding="utf-8")
            with patch.object(distribute, "REPO_ROOT", root), patch.object(distribute, "INDEX_FILE", index):
                with self.assertRaisesRegex(ValueError, "path escapes repository"):
                    distribute.load_skills_from_index()


if __name__ == "__main__":
    unittest.main()
