---
name: baoyu-danger-x-to-markdown
description: Converts X (Twitter) tweets and articles to markdown with YAML front matter. Uses reverse-engineered API requiring user consent. Use when user mentions "X to markdown", "tweet to markdown", "save tweet", or provides x.com/twitter.com URLs for conversion.
version: 1.56.1
tags: ['baoyu', 'content', 'social', 'danger', 'community']
metadata:
  openclaw:
    homepage: https://github.com/JimLiu/baoyu-skills#baoyu-danger-x-to-markdown
    requires:
      anyBins:
        - bun
        - npx
---

# X to Markdown

Converts X content to markdown:
- Tweets/threads → Markdown with YAML front matter
- X Articles → Full content extraction

> ⚠️ **重要合规与风险声明**
>
> 1. **ToS 边界**：本 skill 使用 reverse-engineered API 直接访问 X / Twitter，违反 X Terms of Service §4 (no scraping, no automated access without written permission)。用户对使用本 skill 产生的账户封禁、法律追责承担全部责任。
> 2. **内容版权**：归档的 tweet / 文章版权仍归原作者；本工具不授予任何再分发或商用权利。仅供个人学习、研究、备份使用；商用前必须取得作者书面授权。
> 3. **数据留存**：建议用户自行管理归档内容保留期限；原内容被原作者删除后应同步删除本地归档；多国版权法（DMCA / GDPR / 中国著作权法）适用。
> 4. **敏感内容过滤**：归档内容未经内容审核即保存，违规（暴力 / 色情 / 非法）内容可能被一同存入本地。用户应自行加内容过滤或人工复核。
> 5. **认证 token**：使用用户 cookie / `X_AUTH_TOKEN` / `X_CT0` 长期会话 token，存在 token 泄露 / 跨账号串用 / CDP 端口复用等风险。建议使用专用 browser profile 与最小权限 cookie，并定期轮换。

## User Input Tools

When this skill prompts the user, follow this tool-selection rule (priority order):

1. **Prefer built-in user-input tools** exposed by the current agent runtime — e.g., `AskUserQuestion`, `request_user_input`, `clarify`, `ask_user`, or any equivalent.
2. **Fallback**: if no such tool exists, emit a numbered plain-text message and ask the user to reply with the chosen number/answer for each question.
3. **Batching**: if the tool supports multiple questions per call, combine all applicable questions into a single call; if only single-question, ask them one at a time in priority order.

Concrete `AskUserQuestion` references below are examples — substitute the local equivalent in other runtimes.

## Script Directory

Scripts located in `scripts/` subdirectory.

**Path Resolution**:
1. `{baseDir}` = this SKILL.md's directory
2. Script path = `{baseDir}/scripts/main.ts`
3. Resolve `${BUN_X}` runtime: if `bun` installed → `bun`; if `npx` available → `npx -y bun`; else suggest installing bun

## Consent Requirement

**Before any conversion**, check and obtain consent.

### Consent Flow

**Step 1**: Check consent file

```bash
# macOS
cat ~/Library/Application\ Support/baoyu-skills/x-to-markdown/consent.json

# Linux
cat ~/.local/share/baoyu-skills/x-to-markdown/consent.json
```

**Step 2**: If `accepted: true` and `disclaimerVersion: "1.0"` → print warning and proceed:
```
Warning: Using reverse-engineered X API. Accepted on: <acceptedAt>
```

**Step 3**: If missing or version mismatch → display disclaimer:
```
DISCLAIMER

This tool uses a reverse-engineered X API, NOT official.

Risks:
- May break if X changes API
- No guarantees or support
- Possible account restrictions
- Use at your own risk

Accept terms and continue?
```

Use `AskUserQuestion` with options: "Yes, I accept" | "No, I decline"

**Step 4**: On accept → create consent file:
```json
{
  "version": 1,
  "accepted": true,
  "acceptedAt": "<ISO timestamp>",
  "disclaimerVersion": "1.0"
}
```

**Step 5**: On decline → output "User declined. Exiting." and stop.

## Preferences (EXTEND.md)

Check EXTEND.md in priority order — the first one found wins:

| Priority | Path | Scope |
|----------|------|-------|
| 1 | `.baoyu-skills/baoyu-danger-x-to-markdown/EXTEND.md` | Project |
| 2 | `${XDG_CONFIG_HOME:-$HOME/.config}/baoyu-skills/baoyu-danger-x-to-markdown/EXTEND.md` | XDG |
| 3 | `$HOME/.baoyu-skills/baoyu-danger-x-to-markdown/EXTEND.md` | User home |

| Result | Action |
|--------|--------|
| Found | Read, parse, apply settings |
| Not found | **MUST** run first-time setup (see below) — do NOT silently create defaults |

**EXTEND.md supports**: Download media by default, default output directory.

### First-Time Setup (BLOCKING)

**CRITICAL**: When EXTEND.md is not found, you **MUST use `AskUserQuestion`** to ask the user for their preferences before creating EXTEND.md. **NEVER** create EXTEND.md with defaults without asking. This is a **BLOCKING** operation — do NOT proceed with any conversion until setup is complete.

Use `AskUserQuestion` with ALL questions in ONE call:

**Question 1** — header: "Media", question: "How to handle images and videos in tweets?"
- "Ask each time (Recommended)" — After saving markdown, ask whether to download media
- "Always download" — Always download media to local imgs/ and videos/ directories
- "Never download" — Keep original remote URLs in markdown

**Question 2** — header: "Output", question: "Default output directory?"
- "x-to-markdown (Recommended)" — Save to ./x-to-markdown/{username}/{tweet-id}.md
- (User may choose "Other" to type a custom path)

**Question 3** — header: "Save", question: "Where to save preferences?"
- "User (Recommended)" — ~/.baoyu-skills/ (all projects)
- "Project" — .baoyu-skills/ (this project only)

After user answers, create EXTEND.md at the chosen location, confirm "Preferences saved to [path]", then continue.

Full reference: [references/config/first-time-setup.md](references/config/first-time-setup.md)

### Supported Keys

| Key | Default | Values | Description |
|-----|---------|--------|-------------|
| `download_media` | `ask` | `ask` / `1` / `0` | `ask` = prompt each time, `1` = always download, `0` = never |
| `default_output_dir` | empty | path or empty | Default output directory (empty = `./x-to-markdown/`) |

**Value priority**:
1. CLI arguments (`--download-media`, `-o`)
2. EXTEND.md
3. Skill defaults

## Usage

```bash
${BUN_X} {baseDir}/scripts/main.ts <url>
${BUN_X} {baseDir}/scripts/main.ts <url> -o output.md
${BUN_X} {baseDir}/scripts/main.ts <url> --download-media
${BUN_X} {baseDir}/scripts/main.ts <url> --json
```

## Options

| Option | Description |
|--------|-------------|
| `<url>` | Tweet or article URL |
| `-o <path>` | Output path |
| `--json` | JSON output |
| `--download-media` | Download image/video assets to local `imgs/` and `videos/`, and rewrite markdown links to local relative paths |
| `--login` | Refresh cookies only |

## Supported URLs

- `https://x.com/<user>/status/<id>`
- `https://twitter.com/<user>/status/<id>`
- `https://x.com/i/article/<id>`

## Output

```markdown
---
url: "https://x.com/user/status/123"
author: "Name (@user)"
tweetCount: 3
coverImage: "https://pbs.twimg.com/media/example.jpg"
---

Content...
```

**File structure**: `x-to-markdown/{username}/{tweet-id}/{content-slug}.md`

When `--download-media` is enabled:
- Images are saved to `imgs/` next to the markdown file
- Videos are saved to `videos/` next to the markdown file
- Markdown media links are rewritten to local relative paths

## Media Download Workflow

Based on `download_media` setting in EXTEND.md:

| Setting | Behavior |
|---------|----------|
| `1` (always) | Run script with `--download-media` flag |
| `0` (never) | Run script without `--download-media` flag |
| `ask` (default) | Follow the ask-each-time flow below |

### Ask-Each-Time Flow

1. Run script **without** `--download-media` → markdown saved
2. Check saved markdown for remote media URLs (`https://` in image/video links)
3. **If no remote media found** → done, no prompt needed
4. **If remote media found** → use `AskUserQuestion`:
   - header: "Media", question: "Download N images/videos to local files?"
   - "Yes" — Download to local directories
   - "No" — Keep remote URLs
5. If user confirms → run script **again** with `--download-media` (overwrites markdown with localized links)

## Authentication

1. **Environment variables** (preferred): `X_AUTH_TOKEN`, `X_CT0`
2. **Chrome login** (fallback): Auto-opens Chrome, caches cookies locally

## Extension Support

Custom configurations via EXTEND.md. See **Preferences** section for paths and supported options.
