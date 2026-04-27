---
name: mediacrawler
description: 多平台自媒体数据采集 - 小红书/抖音/微博/B站/知乎等关键词搜索、帖子详情、评论爬取、创作者主页，支持CSV/JSON/SQLite/MySQL多种存储
github_url: https://github.com/NanmiCoder/MediaCrawler
github_hash: 1572b643346e539047b6347bd90c26130d0a03f8
version: 0.1.0
created_at: 2026-04-27
tags: [scraping, social-media, xiaohongshu, douyin, tiktok, weibo, bilibili, crawler, data-collection]
entry_point: scripts/wrapper.sh
dependencies: ["uv", "node>=16", "chrome>=144", "playwright"]
---

# MediaCrawler Skill

多平台自媒体数据采集工具（小红书 · 抖音 · 快手 · B站 · 微博 · 贴吧 · 知乎）

## ⚠️ 使用前必读

**法律免责**：本工具仅限学习研究，禁止商用。爬取行为可能违反平台ToS，使用风险自负。

**安全注意事项（已审查）**：
- 依赖从清华PyPI镜像拉取，引入时已改为官方PyPI源
- `xhshow` 包用于小红书签名，功能特殊，版本已pin
- CDP模式直连用户Chrome，不注入代码，登录态复用安全
- SSL验证默认开启（需在config中手动关闭才会禁用）

## 触发场景

- 搜索小红书/抖音关键词，批量采集帖子和评论
- 根据帖子ID列表下载详情（图片URL、视频URL、统计数据、文字内容）
- 采集创作者主页所有帖子
- 需要结构化保存社媒数据到数据库

## 安装

```bash
# 1. 克隆项目（首次）
git clone https://github.com/NanmiCoder/MediaCrawler.git /tmp/MediaCrawler
cd /tmp/MediaCrawler

# 2. 安装依赖（使用官方PyPI，覆盖清华镜像）
uv sync --index-url https://pypi.org/simple/

# 3. 安装浏览器驱动（仅非CDP模式需要）
uv run playwright install chromium
```

## Chrome CDP 配置（推荐）

```
在Chrome地址栏打开：chrome://inspect/#remote-debugging
勾选 "Allow remote debugging for this browser instance"
确认显示：Server running at: 127.0.0.1:9222
```

## 使用方式

### 关键词搜索采集（Step 1-5 of workflow）

```bash
# 小红书关键词搜索
uv run main.py --platform xhs --lt qrcode --type search

# 抖音关键词搜索
uv run main.py --platform douyin --lt qrcode --type search

# 配置文件设置关键词、数量
# config/base_config.py:
#   KEYWORDS = "你的关键词"
#   CRAWLER_MAX_NOTES_COUNT = 50  # 采集前50条
#   ENABLE_GET_COMMENTS = True    # 开启评论采集
#   MAX_COMMENTS_PER_POST = 50    # 每帖最多50条评论
```

### 指定帖子ID采集

```bash
# 从配置文件读取帖子ID列表
uv run main.py --platform xhs --lt qrcode --type detail
```

### 数据存储模式

```bash
# SQLite（推荐本地使用）
# config/base_config.py: SAVE_DATA_OPTION = "db"

# CSV
# SAVE_DATA_OPTION = "csv"

# MySQL
# SAVE_DATA_OPTION = "mysql"
```

## 采集数据结构

### 小红书帖子字段

| 字段 | 说明 |
|------|------|
| note_id | 帖子ID |
| title | 标题 |
| desc | 正文 |
| type | 类型（video/normal） |
| liked_count | 点赞数 |
| collected_count | 收藏数 |
| comment_count | 评论数 |
| share_count | 转发数 |
| image_list | 图片URL列表（JSON） |
| video_url | 视频URL |
| tag_list | hashtag列表 |
| last_modify_ts | 最后修改时间 |
| nickname | 作者昵称 |
| user_id | 作者ID |

### 评论字段

| 字段 | 说明 |
|------|------|
| comment_id | 评论ID |
| note_id | 所属帖子ID |
| content | 评论内容 |
| user_id | 评论者ID |
| nickname | 评论者昵称 |
| liked_count | 评论点赞数 |
| create_time | 发布时间 |
| parent_comment_id | 父评论ID（二级评论） |

## 与 web-access skill 协作

MediaCrawler 处理**批量结构化采集**（搜索→URL列表→详情→评论→存库）。

若需要**单次交互式浏览**（登录后手动导航、截图确认）→ 使用 `web-access` skill。

## 工作流映射（7步小红书采集）

| 步骤 | 工具 |
|------|------|
| 1. 打开小红书 | MediaCrawler CDP模式（自动） |
| 2. 搜索关键词 | `KEYWORDS` 配置 + `--type search` |
| 3. 记录前50帖子URL | `CRAWLER_MAX_NOTES_COUNT=50` 自动采集 |
| 4. 随机等待+逐个打开 | 内置 `CRAWLER_SLEEP_TIME`（随机延迟） |
| 5. 下载内容 | 自动采集所有字段（见上方数据结构） |
| 6. 存入数据库 | `SAVE_DATA_OPTION=db`（SQLite/MySQL） |
| 7. NLP分析 | → 交给 `chinese-text-analysis` skill |

## config/base_config.py 关键配置

```python
# 平台
PLATFORM = "xhs"          # xhs / douyin / weibo / bilibili

# 登录方式
LOGIN_TYPE = "qrcode"      # qrcode / cookie / phone

# 采集控制
CRAWLER_MAX_NOTES_COUNT = 50
ENABLE_GET_COMMENTS = True
MAX_COMMENTS_PER_POST = 50
CRAWLER_SLEEP_TIME = 5     # 每次请求随机等待基础秒数（anti-detection）

# 存储
SAVE_DATA_OPTION = "db"    # csv / json / db

# CDP模式（推荐）
ENABLE_CDP_MODE = True
CDP_SERVER_PORT = 9222
```

## References

- [完整配置文档](https://github.com/NanmiCoder/MediaCrawler/blob/main/config/base_config.py)
- [数据存储说明](https://github.com/NanmiCoder/MediaCrawler/blob/main/store/README.md)
- 抖音平台参数同小红书，`--platform douyin`
