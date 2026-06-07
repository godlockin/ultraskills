# CodeGraph Benchmark 对比数据

> 数据来源: [CodeGraph官方README](https://github.com/colbymchenry/codegraph)
> 测试方法: Claude Opus 4.7 headless模式,每个任务4次运行取中位数

## 完整测试结果

### 大型项目 (>5k文件)

#### VS Code (TypeScript, ~10k文件)
| 指标 | 启用CodeGraph | 不启用 | 优化幅度 |
|-----|-------------|--------|---------|
| 成本 | $0.42 | $0.64 | **35% ↓** |
| Token | 393k | 1.4M | **73% ↓** |
| 时间 | 1m 0s | 1m 43s | **41% ↓** |
| 工具调用 | 7 | 23 | **72% ↓** |

**测试问题**: "How does the extension host communicate with the main process?"

---

### 中型项目 (600-3k文件)

#### Excalidraw (TypeScript, ~600文件)
| 指标 | 启用CodeGraph | 不启用 | 优化幅度 |
|-----|-------------|--------|---------|
| 成本 | $0.54 | $1.02 | **47% ↓** |
| Token | 851k | 3.2M | **73% ↓** |
| 时间 | 1m 17s | 3m 14s | **60% ↓** |
| 工具调用 | 12 | 83 | **86% ↓** |

**测试问题**: "How does Excalidraw render and update canvas elements?"

---

#### Django (Python, ~2.7k文件)
| 指标 | 启用CodeGraph | 不启用 | 优化幅度 |
|-----|-------------|--------|---------|
| 成本 | $0.41 | $0.62 | **34% ↓** |
| Token | 499k | 1.4M | **64% ↓** |
| 时间 | 1m 0s | 2m 25s | **59% ↓** |
| 工具调用 | 9 | 48 | **81% ↓** |

**测试问题**: "How does Django's ORM build and execute a query from a QuerySet?"

---

#### Tokio (Rust, ~700文件)
| 指标 | 启用CodeGraph | 不启用 | 优化幅度 |
|-----|-------------|--------|---------|
| 成本 | $0.50 | $1.04 | **52% ↓** |
| Token | 657k | 3.4M | **81% ↓** |
| 时间 | 1m 5s | 2m 56s | **63% ↓** |
| 工具调用 | 9 | 75 | **89% ↓** |

**测试问题**: "How does tokio schedule and run async tasks on its runtime?"

---

#### OkHttp (Java, ~640文件)
| 指标 | 启用CodeGraph | 不启用 | 优化幅度 |
|-----|-------------|--------|---------|
| 成本 | $0.36 | $0.44 | **17% ↓** |
| Token | 352k | 596k | **41% ↓** |
| 时间 | 45s | 1m 11s | **36% ↓** |
| 工具调用 | 5 | 14 | **64% ↓** |

**测试问题**: "How does OkHttp process a request through its interceptor chain?"

---

### 小型项目 (<200文件)

#### Gin (Go, ~150文件)
| 指标 | 启用CodeGraph | 不启用 | 优化幅度 |
|-----|-------------|--------|---------|
| 成本 | $0.36 | $0.46 | **22% ↓** |
| Token | 431k | 562k | **23% ↓** |
| 时间 | 47s | 1m 11s | **34% ↓** |
| 工具调用 | 7 | 8 | **19% ↓** ⚠️ |

**测试问题**: "How does gin route requests through its middleware chain?"

**⚠️ 注意**: 工具调用优化仅19%,说明小项目原生搜索已足够高效

---

#### Alamofire (Swift, ~100文件)
| 指标 | 启用CodeGraph | 不启用 | 优化幅度 |
|-----|-------------|--------|---------|
| 成本 | $0.61 | $0.99 | **38% ↓** |
| Token | 1.1M | 2.6M | **59% ↓** |
| 时间 | 1m 19s | 2m 41s | **51% ↓** |
| 工具调用 | 15 | 64 | **77% ↓** |

**测试问题**: "How does Alamofire build, send, and validate a request?"

---

## 关键洞察

### 1. 规模效应明显

```
项目文件数 vs 工具调用削减率:
10k+ 文件:  72-86% ↓
600-3k 文件: 64-89% ↓
<200 文件:   19-77% ↓
```

**结论**: 越大项目收益越高,CodeGraph将O(N)搜索变O(1)图查询

### 2. 为何小项目收益较低

**Gin (150文件)** 案例:
- 原生搜索: grep全仓库仅需几百ms,工具调用8次
- CodeGraph: 减少到7次,边际收益<20%
- **初始化成本**: 首次`codegraph init -i`需1-2分钟

**阈值建议**: 500文件以下跳过CodeGraph

### 3. Agent行为差异

#### 启用CodeGraph:
```
User问题 → codegraph_explore(1次) → 返回完整源码 → 直接回答
总工具调用: 5-15次
```

#### 不启用:
```
User问题 → spawn Explore agent → grep(多次) → read(多次) → 
  可能spawn更多sub-agent → 持续读文件 → 最终回答
总工具调用: 20-80次
```

### 4. Token节省来源

- **缓存未命中**: 不用CodeGraph时,agent持续读文件 → 新token
- **重复读取**: 多个sub-agent可能读相同文件
- **探索开销**: grep返回大量匹配 → 逐一read → token爆炸

CodeGraph一次返回精准上下文,避免探索税

---

## 决策矩阵

| 场景 | 推荐 | 原因 |
|-----|-----|-----|
| 首次探索10k+文件项目 | ✅ 必用 | 70%+工具调用削减 |
| 频繁架构问答(任意规模) | ✅ 必用 | 持续ROI |
| 单次快速查询 | ❌ 跳过 | 初始化成本>收益 |
| <500文件小项目 | ❌ 跳过 | 原生工具够快 |
| CI环境中使用Agent | ✅ 考虑 | 预构建索引可复用 |
