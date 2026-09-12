"""wechat_mp 单测。运行: python3 -m unittest discover -s community/wechat-mp/tests -v"""
import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import wechat_mp  # noqa: E402

import tempfile, unittest.mock as mock


class TestLoadConfig(unittest.TestCase):
    def test_env_vars_win(self):
        with mock.patch.dict(os.environ, {"WECHAT_APP_ID": "id1", "WECHAT_APP_SECRET": "s1"}):
            self.assertEqual(wechat_mp.load_config(), ("id1", "s1"))

    def test_env_file_fallback(self):
        with tempfile.TemporaryDirectory() as d:
            envf = os.path.join(d, ".env")
            with open(envf, "w") as f:
                f.write("WECHAT_APP_ID=id2\n# comment\nWECHAT_APP_SECRET=s2\n")
            with mock.patch.dict(os.environ, {}, clear=False), \
                 mock.patch.object(wechat_mp.os.environ, "pop", side_effect=KeyError):
                pass  # 用下一种方式清环境更直接
            with mock.patch.object(wechat_mp, "CONFIG_DIR", d), \
                 mock.patch.dict(os.environ, {}, clear=True):
                self.assertEqual(wechat_mp.load_config(), ("id2", "s2"))

    def test_missing_returns_none(self):
        with mock.patch.object(wechat_mp, "CONFIG_DIR", "/nonexistent"), \
             mock.patch.dict(os.environ, {}, clear=True):
            self.assertEqual(wechat_mp.load_config(), (None, None))


class TestTokenCache(unittest.TestCase):
    def test_write_read_roundtrip_and_expiry(self):
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(wechat_mp, "CONFIG_DIR", d):
                wechat_mp.TOKEN_FILE = os.path.join(d, "token.json")
                wechat_mp.write_token_cache("T", 7200, now=1000)
                self.assertEqual(wechat_mp.read_token_cache(now=7000), "T")   # 1000+7200-300=7900
                self.assertIsNone(wechat_mp.read_token_cache(now=7900))      # 过期
                self.assertIsNone(wechat_mp.read_token_cache(now=100))       # 未来时间异常视为无效
