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


class TestRawCli(unittest.TestCase):
    def run_raw(self, argv, responses):
        fx = FakeUrllibRequest(responses)
        # 偏差: brief 未隔离 token 缓存,首个执行的用例会把 token 写入 cwd 的
        # .wechat-mp/token.json,导致同组后续用例缓存命中而少发一次请求
        # (exit 0!=1 / requests[1] IndexError)。改为每用例独立临时缓存,语义不变。
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(wechat_mp, "TOKEN_FILE", os.path.join(d, "token.json")), \
                 mock.patch("urllib.request.urlopen", fx), \
                 mock.patch.object(wechat_mp, "load_config", return_value=("id", "sec")):
                code = wechat_mp.main(argv)
        return code, fx

    def test_raw_get_ok(self):
        code, _ = self.run_raw(
            ["raw", "GET", "/cgi-bin/draft/count"],
            [{"access_token": "T", "expires_in": 7200}, {"errcode": 0, "total_count": 3}])
        self.assertEqual(code, 0)

    def test_raw_api_error_exit_1(self):
        code, _ = self.run_raw(
            ["raw", "GET", "/cgi-bin/draft/count"],
            [{"access_token": "T", "expires_in": 7200}, {"errcode": 40013, "errmsg": "invalid appid"}])
        self.assertEqual(code, 1)

    def test_raw_post_data_inline(self):
        code, fx = self.run_raw(
            ["raw", "POST", "/cgi-bin/draft/add", "--data", '{"title":"t"}'],
            [{"access_token": "T", "expires_in": 7200}, {"errcode": 0, "media_id": "M"}])
        self.assertEqual(code, 0)
        sent = json.loads(fx.requests[1].data.decode())
        self.assertEqual(sent["title"], "t")

    def test_raw_query_in_path(self):
        # 偏差: brief 未创建上传文件,补建并自动清理,否则 _read_file 抛 FileNotFoundError
        with open("cover.png", "wb") as f:
            f.write(b"\x89PNG")
        self.addCleanup(lambda: os.remove("cover.png"))
        code, fx = self.run_raw(
            ["raw", "POST", "/cgi-bin/material/add_material?type=image", "--file", "cover.png"],
            [{"access_token": "T", "expires_in": 7200}, {"errcode": 0, "media_id": "M"}])
        self.assertEqual(code, 0)
        self.assertIn("type=image", fx.requests[1].full_url)

    def test_network_error_exit_2(self):
        # 偏差: brief 原写法绕过 run_raw、未隔离 TOKEN_FILE,会读到 cwd 残留缓存
        # 而缓存命中(该用例自己首次运行就会写入缓存,第二次必失败)。统一走 run_raw。
        code, _ = self.run_raw(
            ["raw", "GET", "/cgi-bin/draft/count"],
            [{"access_token": "T", "expires_in": 7200}, urllib.error.URLError("boom")])
        self.assertEqual(code, 2)


class TestRegistry(unittest.TestCase):
    def test_validate_ok(self):
        self.assertEqual(wechat_mp.validate_endpoints(wechat_mp.load_endpoints()), [])

    def test_validate_catches_bad_entries(self):
        bad = {"x": {"name": "n", "method": "PUT", "path": "no-slash",
                     "category": "c", "params": [], "destructive": False},
               "draft_count": {"name": "n", "method": "GET", "path": "/p",
                     "category": "c", "params": [], "destructive": False}}
        errs = wechat_mp.validate_endpoints(bad)
        self.assertTrue(any("method" in e for e in errs))
        self.assertTrue(any("path" in e for e in errs))


class TestCallCmd(unittest.TestCase):
    def run_call(self, argv, responses):
        fx = FakeUrllibRequest(responses)
        # 与 TestRawCli 同理: 隔离 TOKEN_FILE,避免读到/写脏 cwd 的 .wechat-mp/token.json
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(wechat_mp, "TOKEN_FILE", os.path.join(d, "token.json")), \
                 mock.patch("urllib.request.urlopen", fx), \
                 mock.patch.object(wechat_mp, "load_config", return_value=("id", "sec")):
                code = wechat_mp.main(argv)
        return code, fx

    def test_call_routes_to_path(self):
        code, fx = self.run_call(
            ["call", "draft_count"],
            [{"access_token": "T", "expires_in": 7200}, {"errcode": 0, "total_count": 5}])
        self.assertEqual(code, 0)
        self.assertIn("/cgi-bin/draft/count", fx.requests[1].full_url.split("?")[0])

    def test_call_unknown_id(self):
        code, _ = self.run_call(["call", "nope"], [])
        self.assertEqual(code, 2)

    def test_call_destructive_requires_yes(self):
        code, _ = self.run_call(
            ["call", "draft_delete", "--data", '{"media_id":"M"}'], [])
        self.assertEqual(code, 2)

    def test_call_destructive_with_yes(self):
        code, _ = self.run_call(
            ["call", "draft_delete", "--data", '{"media_id":"M"}', "--yes"],
            [{"access_token": "T", "expires_in": 7200}, {"errcode": 0}])
        self.assertEqual(code, 0)

    def test_list_filters_category(self):
        import io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = wechat_mp.main(["list", "--category", "草稿管理"])
        self.assertEqual(code, 0)
        self.assertIn("draft_add", buf.getvalue())
        self.assertNotIn("stable_token", buf.getvalue())


class TestDoctor(unittest.TestCase):
    def test_doctor_all_pass(self):
        fx = FakeUrllibRequest([
            {"access_token": "T", "expires_in": 7200},
            {"errcode": 0, "quota": 100000, "used": 5}])
        with mock.patch("urllib.request.urlopen", fx), \
             mock.patch.object(wechat_mp, "load_config", return_value=("id", "sec")), \
             mock.patch.object(wechat_mp, "CONFIG_DIR", tempfile.mkdtemp()):
            wechat_mp.TOKEN_FILE = os.path.join(wechat_mp.CONFIG_DIR, "token.json")
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = wechat_mp.main(["doctor"])
        self.assertEqual(code, 0)
        self.assertIn("PASS", buf.getvalue())

    def test_doctor_whitelist_hint(self):
        fx = FakeUrllibRequest([
            {"errcode": 40164, "errmsg": "invalid ip, not in whitelist"}])
        with mock.patch("urllib.request.urlopen", fx), \
             mock.patch.object(wechat_mp, "load_config", return_value=("id", "sec")), \
             mock.patch.object(wechat_mp, "CONFIG_DIR", tempfile.mkdtemp()):
            wechat_mp.TOKEN_FILE = os.path.join(wechat_mp.CONFIG_DIR, "token.json")
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = wechat_mp.main(["doctor"])
        self.assertEqual(code, 1)
        self.assertIn("IP", buf.getvalue())

    def test_doctor_no_creds(self):
        with mock.patch.object(wechat_mp, "CONFIG_DIR", "/nonexistent"), \
             mock.patch.dict(os.environ, {}, clear=True):
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = wechat_mp.main(["doctor"])
        self.assertEqual(code, 1)


class TestConvenience(unittest.TestCase):
    def _run(self, argv, responses):
        fx = FakeUrllibRequest(responses)
        # 偏差: brief 未隔离 token 缓存,与 TestRawCli/TestCallCmd 同理 —
        # test_draft_ls 会写 cwd 缓存,导致 test_material_upload 缓存命中少发一次请求
        # (fx.requests[1] IndexError)。统一每用例独立临时缓存,语义不变。
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(wechat_mp, "TOKEN_FILE", os.path.join(d, "token.json")), \
                 mock.patch("urllib.request.urlopen", fx), \
                 mock.patch.object(wechat_mp, "load_config", return_value=("id", "sec")):
                code = wechat_mp.main(argv)
        return code, fx

    def test_draft_ls(self):
        code, fx = self._run(["draft", "ls"],
            [{"access_token": "T", "expires_in": 7200},
             {"errcode": 0, "total_count": 1, "item": []}])
        self.assertEqual(code, 0)
        sent = json.loads(fx.requests[1].data.decode())
        self.assertEqual(sent, {"offset": 0, "count": 20, "no_content": 1})

    def test_draft_del_requires_yes(self):
        code, _ = self._run(["draft", "del", "--media-id", "M"],
            [{"access_token": "T", "expires_in": 7200}])
        self.assertEqual(code, 2)

    def test_material_upload(self):
        code, fx = self._run(["material", "upload", "--file", __file__, "--type", "image"],
            [{"access_token": "T", "expires_in": 7200},
             {"errcode": 0, "media_id": "M1", "url": "http://x/1"}])
        self.assertEqual(code, 0)
        self.assertIn("type=image", fx.requests[1].full_url)

    def test_material_ls_bad_type(self):
        code, _ = self._run(["material", "ls", "--type", "doc"],
            [{"access_token": "T", "expires_in": 7200}])
        self.assertEqual(code, 2)
