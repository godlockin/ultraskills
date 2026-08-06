import asyncio
import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).with_name("mcp_server.py")
SPEC = importlib.util.spec_from_file_location("ultraskills_hub_mcp_server", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
mcp_server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mcp_server)


class FakeProcess:
    pid = 12345


class RefreshIndexSecurityTest(unittest.TestCase):
    def test_refresh_index_passes_script_paths_as_arguments_without_shell(self):
        repo_root = Path("/tmp/repo; touch /tmp/refresh-index-injected")
        expected_scripts = repo_root / "scripts"

        with (
            patch.object(mcp_server, "REPO_ROOT", repo_root),
            patch.object(mcp_server.subprocess, "Popen", return_value=FakeProcess()) as popen,
        ):
            response = asyncio.run(mcp_server.call_tool("refresh_index", {}))

        data = json.loads(response[0].text)
        self.assertEqual(data["status"], "started")
        command = popen.call_args.args[0]
        self.assertEqual(command[:2], [mcp_server.sys.executable, "-c"])
        self.assertEqual(
            command[3:],
            [
                "--",
                str(expected_scripts / "arena_scan.py"),
                str(expected_scripts / "arena_cluster_score.py"),
                str(expected_scripts / "arena_build_index.py"),
            ],
        )
        self.assertIn("subprocess.run([sys.executable, script], check=True)", command[2])
        self.assertNotIn("bash", command)
        self.assertEqual(popen.call_args.kwargs["cwd"], repo_root)
        self.assertFalse(popen.call_args.kwargs["shell"])


if __name__ == "__main__":
    unittest.main()
