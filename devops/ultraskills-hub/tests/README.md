# hub 搜索回归测试

## 用法

```bash
# 全跑,输出准确率概要
python3 devops/ultraskills-hub/tests/regression.py

# 逐条打印命中/未命中
python3 devops/ultraskills-hub/tests/regression.py --verbose

# 保存快照(改完 aliases/search.py/index 前后各存一次,对比效果)
python3 devops/ultraskills-hub/tests/regression.py --save 我的改动

# 对比两次快照
python3 devops/ultraskills-hub/tests/regression.py --diff baseline 我的改动
```

## 结构

- `ground_truth.json` — 30 条查询用例
  - `expected_top`: 期待出现在 top 3 的 skill id 列表(命中任一算 top3_ok)
  - `must_top1`: (可选) 严格要求 top 1 必须是此 skill

- `regression.py` — 跑测,支持 --verbose / --save / --diff

- `snapshots/` — 保存的历史快照
  - `baseline.json` — v2.1.0 之前的搜索基线 (top1 63.6% · top3 73.3%)
  - `v3-final.json` — 加了 aliases + body_summary + 查询扩展 + 严格 alias 匹配后的效果 (top1 100% · top3 100%)

## 增加 ground truth

修改 `ground_truth.json` 里的 `cases`:

```json
{"query": "用户可能输的中文/英文查询", "expected_top": ["id1", "id2"], "must_top1": "id1"}
```

`must_top1` 为 null 表示不强制要求 top1(比如结果里 id1/id2/id3 都合理)。
