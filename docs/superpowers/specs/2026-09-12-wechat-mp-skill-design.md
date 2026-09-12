# wechat-mp Skill 设计文档

- 日期: 2026-09-12
- 状态: 已获用户批准设计,待 spec 审阅
- 目标路径: `community/wechat-mp/`

## 1. 目标与范围

构建一个完整覆盖微信公众号服务端 API 的 ultraskills skill。

- **范围: 目标 C(全量 ~116 端点 / 22 模块)**,但**分层实现、基础优先**——底层做成通用 API 网关,任意端点一条命令直达;高频流程再叠便利命令。
- 现有 `community/baoyu-skills/baoyu-post-to-wechat` 只覆盖发文链路(draft/add),本 skill 与其共存,不替代。

### API 模块清单(来自官方文档 `/doc/subscription/api/`)

| 模块组 | 模块 | 端点数(约) |
|---|---|---|
| 基础 | 接口调用凭据(token/stable_token)、网络检测、服务器 IP | 5 |
| openApi 管理 | quota 查询/重置、rid 查询 | 5 |
| 自定义菜单 | 创建/查询/删除/个性化菜单 | 7 |
| 群发消息 | 上传图片、群发(标签)、预览、速度控制、删除 | 8 |
| 一次性订阅消息 | 发送订阅模板消息 | 1 |
| 自动回复 | 获取规则 | 1 |
| 素材管理 | 永久素材增删查、临时素材、uploadimg | 9 |
| 草稿管理 | 开关、增删改查、计数 | 7 |
| 商品卡片 | 获取 DOM 结构 | 1 |
| 留言管理 | 开/关评论、列表、精选、回复、删除 | 8 |
| 发布能力 | 提交发布、状态查询、列表、删除、获取图文 | 5 |
| 用户标签 | 增删改查、批量打/取消标签、粉丝列表 | 8 |
| 用户信息 | 基本信息、批量、关注列表、黑名单、备注 | 7 |
| openid 转换 | changeopenid | 1 |
| 客服管理 | 账号增删改、在线列表、头像 | 7 |
| 客服会话 | 创建/关闭/查询会话 | 5 |
| 客服消息 | 发送、typing、聊天记录 | 3 |
| 数据统计 | 用户/图文/消息/接口数据 | 21 |
| JS-SDK | getticket | 1 |
| 智能接口 | 语音翻译、OCR×7、图像处理×2 | 12 |
| 微信门店 | 门店小程序管理 | 12 |
| 就医助手 | 消息推送 | 1 |

合计 ~116。以 `scripts/` 实际注册数为准,文档差异在 Phase 4 对账。

## 2. 技术决策

| 决策 | 选择 | 理由 |
|---|---|---|
| 运行时 | Python 3 纯标准库(urllib + json + argparse) | 仓库惯例、零依赖、部署即用 |
| 形态 | CLI 单入口 + SKILL.md 路由 | 与 ultraskills 结构标准一致;未来可包 MCP 薄壳 |
| 凭证 | env(`WECHAT_APP_ID`/`WECHAT_APP_SECRET`)+ 项目 `.wechat-mp/.env` 回退 | 简单起步;格式预留 `accounts:` 多账号扩展 |
| token | `POST /cgi-bin/stable_token` | 官方推荐,支持 force_refresh |

## 3. 目录结构

```
community/wechat-mp/
├── SKILL.md              # frontmatter + 触发词 + 用法 + 安全规则
├── scripts/
│   ├── wechat_mp.py      # 单入口 CLI
│   └── endpoints.json    # 端点注册表
├── references/
│   ├── api-catalog.md    # 全接口清单(中文名 + path + 分类)
│   └── errors.md         # errcode 速查表
└── examples/
    ├── publish-article.md
    └── manage-drafts.md
```

## 4. 架构: 4 层

```
Layer 3  便利命令   doctor / publish / draft / material / comment
Layer 2  端点注册表 endpoints.json(116 端点元数据)
Layer 1  通用网关   wechat_mp.py raw GET|POST <path> [...]
Layer 0  认证层     stable_token 获取 + 缓存 + 自动续期
```

### 4.1 Layer 0 — 认证

- `POST https://api.weixin.qq.com/cgi-bin/stable_token`,body `{"grant_type":"client_credential","appid":...,"secret":...,"force_refresh":false}`
- 缓存 `.wechat-mp/token.json`:`{"token":..., "expires_at": <unix秒>}`,写入时 `expires_at = now + expires_in - 300`
- 读取: 文件存在且未过期 → 直接用;否则刷新
- 运行中遇 `40001`(credential 失效)/`42001`(token 过期) → `force_refresh:true` 重取一次并重试原请求,只重试一次
- Secret 只出现在请求体内,永不打印到 stdout/日志/错误信息

### 4.2 Layer 1 — 通用网关

```
python3 wechat_mp.py raw GET /cgi-bin/draft/count
python3 wechat_mp.py raw POST /cgi-bin/draft/add --data @article.json
python3 wechat_mp.py raw POST /cgi-bin/material/add_material?type=image --file cover.png
python3 wechat_mp.py raw POST /datacube/getusersummary --data '{"begin_date":"2026-09-01","end_date":"2026-09-07"}'
```

- 自动附 access_token(query 参数 `?access_token=`)
- `--data @file.json` 或内联 JSON;`--file` 触发 multipart/form-data
- 输出: 服务端原始 JSON,pretty-print(含 errcode/errmsg/rid)
- exit code: `0` 成功 / `1` API 返回错误(errcode 见 JSON 输出;errcode 如 40001 超出 POSIX 0-255 不能直接作 exit code) / `2` 网络异常
- 网络异常输出 `{"errcode":-2,"errmsg":"network error: ...","rid":null}` exit 2

### 4.3 Layer 2 — 端点注册表 `endpoints.json`

Schema:

```json
{
  "draft_add": {
    "name": "新增草稿",
    "method": "POST",
    "path": "/cgi-bin/draft/add",
    "category": "草稿管理",
    "params": ["articles"],
    "destructive": false,
    "notes": "thumb_media_id 需先经 material/add_material 获取"
  }
}
```

- `wechat_mp.py list [--category 素材] [--search 草稿]` — 列端点
- `wechat_mp.py call draft_add --data @a.json` — 按名调用(等价 raw,带参数提示)
- 全 116 端点逐条录入,字段以官方文档目录为准

### 4.4 Layer 3 — 便利命令

| 命令 | 功能 |
|---|---|
| `doctor` | 自检: env/.env 凭证存在 → 调 stable_token → 调 `openapi/quota/get` 报 quota;40164 时提示 IP 白名单设置路径 |
| `publish <md|json>` | 完整链: 封面图 upload(`material/add_material`)→ 正文图片 uploadimg → `draft/add` → `freepublish/submit` → 轮询 `freepublish/get` 直到 success/fail,打印 article_url。JSON 输入为标准 draft articles 结构;md 输入做图片占位替换后组 articles |
| `draft ls/get/del/count` | 草稿箱管理(del 强制 --yes) |
| `material ls/upload/del` | 永久素材管理(del 强制 --yes) |
| `comment ls/reply/elect` | 留言管理 |

未覆盖流程一律走 `raw`/`call`,即已全量可达。

## 5. SKILL.md

- frontmatter: `name: wechat-mp`,触发词含 微信公众号、公众号接口、素材、草稿、发布、留言、菜单、群发、数据统计
- 正文: 快速开始(doctor) → 4 层用法 → 破坏性操作规则 → 常见 errcode
- 不重复 endpoints 全量内容,链接 references/api-catalog.md(单一真相源)

## 6. 安全规则

1. **destructive 端点**(注册表 `destructive:true`:`freepublish/delete`、`draft/delete`、`del_material`、`comment/delete`、`comment/reply/delete`、`mass/delete`、`menu/delete`、tags 删除类、黑名单类等)CLI 层强制 `--yes`,缺省拒绝并列出将执行的操作
2. Secret 永不输出;`--verbose` 调试模式对 token/secret 做 `****` 脱敏
3. `45009`(reach max api daily quota)错误提示 `clear_quota` 用法
4. 速率遵从服务端限制,不做客户端主动限流(YAGNI),错误码透传

## 7. 测试

- **无需真实凭证的单元测试**(`test/test_wechat_mp.py`):
  - endpoints.json schema 校验(必填字段、method 合法、path 以 / 开头、无重复 key)
  - CLI 参数解析(argparse 各子命令)
  - multipart body 构造(纯函数,校验 boundary/字段)
  - token 缓存读写与过期判断(注入 fake clock)
  - raw 层 HTTP 交互(mock urlopen):成功、errcode 透传、40001 重试一次
- **真实凭证验收**(用户提供账号):`doctor` 通过、publish 链路端到端、draft/material/comment 各走一条
- 运行: `python3 -m pytest test/` 或 `python3 test/test_wechat_mp.py`(unittest 兼容两种)

## 8. 验收标准

- [ ] endpoints.json 注册 ≥ 官方目录全部端点(以 references/api-catalog.md 对账)
- [ ] `doctor` 真实账号通过
- [ ] `publish` 真实账号端到端发文成功
- [ ] destructive 防误删:无 `--yes` 时拒绝
- [ ] `scan_and_check.py community/wechat-mp/` 结构合规
- [ ] arena pipeline 重建,`search.py 微信公众号` 能命中
- [ ] 单测全绿

## 9. 实施阶段

| Phase | 内容 | 交付 |
|---|---|---|
| 1 基础 | L0 token + L1 raw 网关 + doctor + 单测骨架 | 基础可用,任意 GET/POST 可达 |
| 2 注册表 | endpoints.json 全量 116 + list/call + schema 单测 | 全量覆盖 |
| 3 便利命令 | publish 链路 → draft/material/comment | 高频流程一键化 |
| 4 收尾 | references/examples + scan_and_check + arena 重建 + 真实账号验收 | 入库完成 |

## 10. 非目标(本期不做)

- 多账号切换(格式预留,不实现)
- MCP server 化(留作后续薄壳)
- 浏览器自动化发文(baoyu-post-to-wechat 已覆盖该场景)
- 门店小程序/就医助手之外的微信小程序 API(那是另一套 doc)
