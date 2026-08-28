# UltraSkills 安全与一致性修复 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 消除已确认的路径穿越、命令注入、CLI 安装生命周期故障、Arena 发布竞争与索引/安装语义漂移。

**Architecture:** 将不可信 skill ID 与 index path 的校验收敛为可复用的边界函数；Node CLI 使用单一版本化 manifest 契约。Arena 仅通过 scan→score→build 发布，所有 JSON 采用临时文件原子替换并由可靠锁串行化。安装器按 index 的 `SKILL.md` 文件路径契约工作。

**Tech Stack:** Node.js ESM、Node test runner、Python 3、shell、JSON。

## Global Constraints

- 不接受含 `/`、`\\`、`.`、`..` 或控制字符的 skill ID；仅接受 `/^[A-Za-z0-9][A-Za-z0-9._-]*$/`。
- 所有由索引派生的文件路径须 `resolve()` 后验证包含在预期根目录内。
- 所有生成 JSON 先写同目录临时文件，完成 `fsync` 后原子替换。
- index 更新唯一真相来源为 `arena_scan.py → arena_cluster_score.py → arena_build_index.py`。
- 不引入 `any`、`@ts-ignore` 或未固定的远程可执行脚本。
- 每项变更先写失败测试；测试命令后台执行并保存日志。

---

### Task 1: 共享路径边界与破坏性删除防护

**Files:**
- Create: `lib/path-safety.js`
- Create: `test/path-safety.test.js`
- Modify: `lib/install.js`
- Modify: `lib/uninstall.js`
- Modify: `scripts/deploy_skills.py`
- Modify: `scripts/distribute.py`
- Modify: `devops/skill-manager/scripts/delete_skill.py`

**Interfaces:**
- Produces Node `assertSafeSkillId(id: string): string` 和 `resolveWithin(root: string, ...segments: string[]): string`。
- Python 入口分别实现同等的 ID 与 containment 检查；所有删除默认拒绝非安全目标。

- [ ] **Step 1: 写 Node 路径安全失败测试**

```js
import assert from 'node:assert/strict';
import test from 'node:test';
import { assertSafeSkillId, resolveWithin } from '../lib/path-safety.js';

test('rejects traversal and separators in a skill id', () => {
  for (const id of ['..', '.', '../victim', 'a/b', 'a\\b', '']) {
    assert.throws(() => assertSafeSkillId(id), /Invalid skill ID/);
  }
});

test('resolves only inside root', () => {
  assert.throws(() => resolveWithin('/tmp/skills', '..', 'victim'), /escapes root/);
});
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `node --test test/path-safety.test.js`
Expected: FAIL，因为模块不存在。

- [ ] **Step 3: 实现最小 Node 边界模块**

```js
import { resolve, relative } from 'node:path';
const SKILL_ID = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;
export function assertSafeSkillId(id) {
  if (typeof id !== 'string' || !SKILL_ID.test(id)) throw new Error(`Invalid skill ID: ${id}`);
  return id;
}
export function resolveWithin(root, ...segments) {
  const base = resolve(root);
  const candidate = resolve(base, ...segments);
  if (candidate !== base && !relative(base, candidate).split('/').every(part => part && part !== '..')) {
    throw new Error(`Resolved path escapes root: ${candidate}`);
  }
  return candidate;
}
```

- [ ] **Step 4: 在 Node 安装、更新、卸载使用边界模块**

`writeSkill`、update 写入和 uninstall 删除前调用 `assertSafeSkillId`，目标统一以 `resolveWithin(join(cwd, '.claude', 'skills'), id)` 生成。删除必须拒绝 skills root 本身。

- [ ] **Step 5: 在 Python 部署与删除入口添加等价检查**

在 `deploy_skills.py`、`distribute.py` 读取 index 后拒绝不安全 `id`，并验证 source path 位于 `REPO_ROOT`。在 `delete_skill.py` 使用 `Path.resolve()` 验证 `target.parent == skills_root.resolve()`，默认询问 `input('Type skill ID to confirm: ')`，仅 `--yes` 可跳过确认。

- [ ] **Step 6: 运行安全回归测试**

Run: `node --test test/path-safety.test.js test/install.test.js test/uninstall.test.js && python3 -m unittest discover -s scripts -p '*test*.py'`
Expected: PASS；若 Python 测试目录不存在，新增针对 delete/deploy 的 `unittest` 文件并运行。

- [ ] **Step 7: Commit**

```bash
git add lib/path-safety.js test/path-safety.test.js lib/install.js lib/uninstall.js scripts/deploy_skills.py scripts/distribute.py devops/skill-manager/scripts/delete_skill.py
git commit -m "fix(security): validate skill paths before writes and deletes"
```

### Task 2: MCP 无 shell 的 Arena 刷新

**Files:**
- Modify: `devops/ultraskills-hub/mcp_server.py`
- Create: `devops/ultraskills-hub/tests/test_mcp_refresh.py`

**Interfaces:**
- `refresh_index` 以 Python 参数数组依次启动 scan、score、build，不得传递 `shell=True` 或 `bash -c`。

- [ ] **Step 1: 写命令构造失败测试**

```python
def test_refresh_uses_argument_vectors(monkeypatch):
    calls = []
    monkeypatch.setattr(module.subprocess, "Popen", lambda args, **kw: calls.append((args, kw)))
    module.start_refresh(Path("/tmp/repo;touch /tmp/pwned"))
    assert all(isinstance(args, list) for args, _ in calls)
    assert all(kw.get("shell", False) is False for _, kw in calls)
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python3 -m unittest devops.ultraskills-hub.tests.test_mcp_refresh`
Expected: FAIL，当前实现拼接 shell 字符串。

- [ ] **Step 3: 实现安全顺序执行**

使用 `[sys.executable, str(script)]` 参数数组。后台工作线程依次 `subprocess.run(..., check=True, cwd=repo_root)` 执行三个 Python 脚本，并记录结构化失败状态；不再拼接 shell 管道或 `bash -c`。

- [ ] **Step 4: 运行 MCP 回归测试**

Run: `python3 -m unittest discover -s devops/ultraskills-hub/tests -p 'test_*.py'`
Expected: PASS。

- [ ] **Step 5: Commit**

```bash
git add devops/ultraskills-hub/mcp_server.py devops/ultraskills-hub/tests/test_mcp_refresh.py
git commit -m "fix(mcp): run index refresh without shell evaluation"
```

### Task 3: 修复 CLI 下载路径、manifest 与卸载命令

**Files:**
- Modify: `lib/install.js`
- Modify: `lib/update.js`
- Modify: `lib/uninstall.js`
- Modify: `bin/ultraskills.js`
- Modify: `test/install.test.js`
- Modify: `test/update.test.js`
- Create: `test/cli-lifecycle.test.js`

**Interfaces:**
- Index `skill.path` 是相对仓库根的 `SKILL.md` 文件路径。
- Manifest 为 `{ "version": 1, "skills": [{ "id", "path", "installedAt", "score" }] }`。
- `uninstall(id, cwd, opts)` 是唯一卸载导出。

- [ ] **Step 1: 写失败测试**

```js
test('buildRawUrl preserves an index SKILL.md path', () => {
  assert.equal(buildRawUrl('./community/foo/SKILL.md'),
    'https://raw.githubusercontent.com/godlockin/ultraskills/main/community/foo/SKILL.md');
});

test('lifecycle manifest is readable by update and uninstall', async () => {
  await writeManifest(cwd, skill);
  assert.deepEqual(await readManifest(cwd), { version: 1, skills: [expectedEntry] });
});
```

- [ ] **Step 2: 运行目标测试确认失败**

Run: `node --test test/install.test.js test/update.test.js test/cli-lifecycle.test.js`
Expected: FAIL，URL 有重复 `/SKILL.md` 且 schema 不同。

- [ ] **Step 3: 实现稳定 URL 与版本化 manifest**

`buildRawUrl()` 仅移除前导 `./` 并编码路径，不追加文件名。新增 shared `readManifest` / `writeManifest`；读取旧对象格式时转换为 v1 并在下次写入迁移。所有 lifecycle 操作通过该模块读写。

- [ ] **Step 4: 修复 CLI 命令绑定与交互输入**

从 `lib/uninstall.js` 导入 `uninstall`，调用 `await uninstall(skillId, process.cwd(), { yes })`。交互选择必须使用 `Number.parseInt`、`Number.isInteger` 与范围校验；无效输入重新提示或取消，绝不选择 `undefined`。

- [ ] **Step 5: 加入真实生命周期集成测试**

在临时 cwd 中 stub 下载，验证 install 写 manifest、update 读取同一 skill、uninstall 同时删除目录和 manifest entry；验证 `uninstall ../../x` 拒绝且没有删除目标。

- [ ] **Step 6: 运行 Node 全套测试**

Run: `npm test -- --runInBand`
Expected: PASS。

- [ ] **Step 7: Commit**

```bash
git add lib/install.js lib/update.js lib/uninstall.js bin/ultraskills.js test/install.test.js test/update.test.js test/cli-lifecycle.test.js
git commit -m "fix(cli): unify skill lifecycle paths and manifest"
```

### Task 4: Arena 互斥、原子发布与唯一构建链

**Files:**
- Modify: `scripts/pipeline_lock.py`
- Create: `scripts/atomic_json.py`
- Modify: `scripts/arena_scan.py`
- Modify: `scripts/arena_cluster_score.py`
- Modify: `scripts/arena_build_index.py`
- Modify: `scripts/deploy_skills.py`
- Modify: `scripts/sync_skills.py`
- Create: `scripts/tests/test_pipeline_publish.py`

**Interfaces:**
- `atomic_write_json(path: Path, value: object) -> None`。
- `PipelineLock` 使用排他原子创建；只删除自身创建的 lock。
- deploy/sync 不得直接写 `index.json`，仅调用完整 Arena pipeline。

- [ ] **Step 1: 写失败测试**

```python
def test_atomic_write_never_exposes_partial_json(tmp_path):
    target = tmp_path / "index.json"
    atomic_write_json(target, {"skills": [{"id": "x"}]})
    assert json.loads(target.read_text())["skills"][0]["id"] == "x"

def test_second_lock_owner_is_rejected(tmp_path):
    with PipelineLock(tmp_path / ".lock"):
        with pytest.raises(LockHeldError):
            PipelineLock(tmp_path / ".lock").acquire()
```

- [ ] **Step 2: 运行并确认失败**

Run: `python3 -m pytest scripts/tests/test_pipeline_publish.py -q`
Expected: FAIL，因为尚无 `atomic_json` 或排他锁。

- [ ] **Step 3: 实现原子 JSON 发布与锁**

同目录 `NamedTemporaryFile(delete=False)` 写入 JSON，`flush()`、`os.fsync()` 后 `os.replace()`；目录文件描述符同样 `fsync`。锁使用 `os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)`，记录 nonce/PID；release 仅在 nonce 匹配时 unlink。

- [ ] **Step 4: 删除 legacy index writers**

`deploy_skills.py scan` 与 `sync_skills.py` 不再直接写 index；成功完成完整 pipeline 后才接受新 index。同步失败必须检查 `git pull` 返回码并停止导入，记录 cache 的 commit SHA。

- [ ] **Step 5: 修复 winner 参赛集一致性**

`arena_cluster_score.py` 中 `runner_up` 与 `defeated` 必须从已过滤的 `eligible` 排序结果派生，禁止重新使用全量成员。

- [ ] **Step 6: 运行发布与 Arena 回归测试**

Run: `python3 -m pytest scripts/tests -q && python3 scripts/arena_scan.py && python3 scripts/arena_cluster_score.py && python3 scripts/arena_build_index.py`
Expected: PASS；生成 index 可由 `python3 -m json.tool index.json` 解析。

- [ ] **Step 7: Commit**

```bash
git add scripts
git commit -m "fix(arena): publish consistent index data atomically"
```

### Task 5: 安装模式、索引门禁、文档索引与供应链固定

**Files:**
- Modify: `setup.sh`
- Modify: `scripts/distribute.py`
- Modify: `scripts/arena_scan.py`
- Modify: `scripts/arena_build_index.py`
- Modify: `SKILLS_INDEX.md` 或其生成器
- Modify: `devops/codegraph-booster/scripts/setup.sh`
- Modify: `scripts/sync_skills.py`
- Modify: `devops/ultraskills-hub/requirements.txt`
- Create: 对应脚本测试。

**Interfaces:**
- `--top --mode copy` 必须复制而非 symlink。
- index 中每个 `path` 都是仓库内存在的 `SKILL.md`。
- `SKILLS_INDEX.md` 从同一 build 输入生成。
- 远程可执行来源必须是固定版本及校验值；依赖必须锁定。

- [ ] **Step 1: 写安装模式与索引路径失败测试**

```python
def test_all_published_paths_exist_and_are_skill_files(index):
    for skill in index["skills"]:
        path = (REPO_ROOT / skill["path"]).resolve()
        assert path.is_relative_to(REPO_ROOT.resolve())
        assert path.name == "SKILL.md" and path.is_file()
```

Shell 集成测试调用 `./setup.sh --top --mode copy --tool claude-code`，断言安装目标是普通目录而不是 symlink，且归档 skill 不在 top 清单。

- [ ] **Step 2: 运行测试确认失败**

Run: `python3 -m pytest scripts/tests/test_index_paths.py -q`
Expected: FAIL，现有 index 含悬空路径。

- [ ] **Step 3: 修复 setup 与索引生成**

删除已归档 `design-an-interface` 的 top 项；统一 top 安装走 `distribute.py --mode "$LINK_MODE"`；记录成功/跳过，必选项缺失时 exit 1。scan/build 过滤/拒绝不存在 path，并生成 `SKILLS_INDEX.md` 元数据总数、cluster、日期。

- [ ] **Step 4: 固定供应链来源**

`codegraph-booster` 不得 `curl | sh` 追踪 `main`：使用固定 release URL、固定 SHA-256，下载到临时文件、哈希匹配后执行。`sync_skills.py` 的 source 配置须固定 commit SHA；clone 后验证 `HEAD` 等于 allowlist SHA。MCP requirements 使用由受审查锁文件导出的精确版本与 hashes。

- [ ] **Step 5: 全量重建与一致性校验**

Run: `python3 scripts/arena_scan.py && python3 scripts/arena_cluster_score.py && python3 scripts/arena_build_index.py && python3 -m pytest scripts/tests/test_index_paths.py -q`
Expected: PASS；不存在悬空 index path，`SKILLS_INDEX.md` 与 index 统计一致。

- [ ] **Step 6: Commit**

```bash
git add setup.sh scripts SKILLS_INDEX.md devops/codegraph-booster/scripts/setup.sh devops/ultraskills-hub/requirements.txt
git commit -m "fix(distribution): verify index paths and installation modes"
```

### Task 6: 整体验证与安全复审

**Files:**
- Modify: 必要的测试和文档文件。

- [ ] **Step 1: 运行 Node、Python、shell 静态检查**

Run: `npm test -- --runInBand && python3 -m pytest scripts/tests devops/ultraskills-hub/tests -q && bash -n setup.sh devops/codegraph-booster/scripts/setup.sh`
Expected: 全部 PASS。

- [ ] **Step 2: 运行完整 Arena pipeline**

Run: `python3 scripts/arena_scan.py && python3 scripts/arena_cluster_score.py && python3 scripts/arena_build_index.py && python3 -m json.tool index.json >/dev/null`
Expected: 全部 exit 0。

- [ ] **Step 3: 安全回归**

验证以下命令全部拒绝且不修改根目录外文件：

```bash
node bin/ultraskills.js uninstall ../../sentinel --yes
python3 devops/skill-manager/scripts/delete_skill.py ../../sentinel /tmp/skills --yes
```

验证 `refresh_index` 在含 `;` 的临时工作区路径下仍把路径作为参数而非 shell 源码。

- [ ] **Step 4: 请求独立代码复审**

使用 `/code-review` 或安全审查 skill，重点复核任意删除、`subprocess`、`os.replace`、manifest migration 与 generated index。

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "test: verify hardened skill lifecycle and arena pipeline"
```
