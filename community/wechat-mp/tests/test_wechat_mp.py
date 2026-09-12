"""wechat_mp 单测。运行: python3 -m unittest discover -s community/wechat-mp/tests -v"""
import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import wechat_mp  # noqa: E402

import tempfile, unittest.mock as mock
import json, time
import urllib.request, urllib.error


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


class FakeResp:
    def __init__(self, body): self._b = body.encode() if isinstance(body, str) else body
    def read(self): return self._b
    def __enter__(self): return self
    def __exit__(self, *a): return False


def urlopen_200(payload):
    return mock.patch("urllib.request.urlopen", return_value=FakeResp(json.dumps(payload)))


class TestTokenFetch(unittest.TestCase):
    def test_fetch_stable_token(self):
        with urlopen_200({"access_token": "T1", "expires_in": 7200}) as m:
            tok, exp = wechat_mp.fetch_stable_token("id", "sec")
            self.assertEqual((tok, exp), ("T1", 7200))
            req = m.call_args[0][0]
            self.assertIn("/cgi-bin/stable_token", req.full_url)
            self.assertEqual(req.get_method(), "POST")

    def test_fetch_error_raises_for_caller(self):
        with urlopen_200({"errcode": 40125, "errmsg": "invalid secret"}):
            with self.assertRaises(wechat_mp.WechatApiError) as cm:
                wechat_mp.fetch_stable_token("id", "bad")
            self.assertEqual(cm.exception.payload["errcode"], 40125)

    def test_get_access_token_uses_cache(self):
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(wechat_mp, "CONFIG_DIR", d):
                wechat_mp.TOKEN_FILE = os.path.join(d, "token.json")
                wechat_mp.write_token_cache("Cached", 7200, now=time.time())
                with mock.patch.object(wechat_mp, "fetch_stable_token") as fs:
                    self.assertEqual(wechat_mp.get_access_token(), "Cached")
                    fs.assert_not_called()


class TestMultipart(unittest.TestCase):
    def test_build_contains_fields_and_file(self):
        body, ctype = wechat_mp.build_multipart(
            {"type": "image", "description": "封面"}, "media", "cover.png", b"\x89PNG...")
        self.assertIn("multipart/form-data", ctype)
        self.assertIn(b'name="type"', body)
        self.assertIn(b"image", body)
        self.assertIn(b'name="media"; filename="cover.png"', body)
        self.assertIn(b"\x89PNG...", body)
        # boundary 在 ctype 与 body 一致
        b = ctype.split("boundary=")[1].encode()
        self.assertIn(b, body)


class FakeUrllibRequest:
    """捕获 urlopen 的 Request,按脚本顺序回放响应。"""
    def __init__(self, responses):
        self.responses = list(responses)
        self.requests = []
    def __call__(self, req, timeout=None):
        self.requests.append(req)
        r = self.responses.pop(0)
        if isinstance(r, Exception):
            raise r
        return FakeResp(json.dumps(r))


class TestApiCall(unittest.TestCase):
    def setUp(self):
        self.fx = FakeUrllibRequest([{"access_token": "T0", "expires_in": 7200}])
        # 偏差: brief 原值 "/nonexistent/token.json" 在 macOS 只读根卷上 write_token_cache
        # 的 makedirs 会 PermissionError,故改用真实临时目录,语义不变(读缓存必 miss)
        self._t = mock.patch.object(wechat_mp, "TOKEN_FILE",
                                    os.path.join(tempfile.mkdtemp(), "token.json"))
        self._t.start(); self.addCleanup(self._t.stop)
        self._c = mock.patch.object(wechat_mp, "load_config", return_value=("id", "sec"))
        self._c.start(); self.addCleanup(self._c.stop)

    def test_token_attached(self):
        fx = FakeUrllibRequest([{"access_token": "T0", "expires_in": 7200},
                                {"errcode": 0, "data": "ok"}])
        with mock.patch("urllib.request.urlopen", fx):
            out = wechat_mp.api_call("GET", "/cgi-bin/draft/count")
        self.assertEqual(out["data"], "ok")
        self.assertIn("access_token=T0", fx.requests[1].full_url)

    def test_retry_once_on_40001(self):
        fx = FakeUrllibRequest([{"access_token": "T0", "expires_in": 7200},
                                {"errcode": 40001, "errmsg": "invalid"},
                                {"access_token": "T1", "expires_in": 7200},
                                {"errcode": 0}])
        with mock.patch("urllib.request.urlopen", fx), \
             mock.patch.object(wechat_mp, "CONFIG_DIR", tempfile.mkdtemp()):
            wechat_mp.TOKEN_FILE = os.path.join(wechat_mp.CONFIG_DIR, "token.json")
            out = wechat_mp.api_call("GET", "/cgi-bin/draft/count")
        self.assertEqual(out["errcode"], 0)
        self.assertEqual(len(fx.requests), 4)  # 取token + 失败 + 强刷token + 重试

    def test_no_retry_twice(self):
        fx = FakeUrllibRequest([{"access_token": "T0", "expires_in": 7200},
                                {"errcode": 40001, "errmsg": "invalid"},
                                {"access_token": "T1", "expires_in": 7200},
                                {"errcode": 40001, "errmsg": "still invalid"}])
        with mock.patch("urllib.request.urlopen", fx):
            out = wechat_mp.api_call("GET", "/cgi-bin/draft/count")
        self.assertEqual(out["errcode"], 40001)
        self.assertEqual(len(fx.requests), 4)

    def test_multipart_upload(self):
        fx = FakeUrllibRequest([{"access_token": "T0", "expires_in": 7200},
                                {"errcode": 0, "media_id": "M1"}])
        with mock.patch("urllib.request.urlopen", fx):
            out = wechat_mp.api_call("POST", "/cgi-bin/material/add_material",
                                     extra_query={"type": "image"},
                                     file=("cover.png", b"\x89PNG"))
        self.assertEqual(out["media_id"], "M1")
        req = fx.requests[1]
        self.assertIn("multipart/form-data", req.headers.get("Content-type", ""))
