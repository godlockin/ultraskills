# patent-disclosure-skill (ultraskills vendored snapshot)

This directory is a **snapshot import** of
[handsomestWei/patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill)
(MIT licensed), tracked in the ultraskills `community/` index.

| Field | Value |
|-------|-------|
| Upstream | <https://github.com/handsomestWei/patent-disclosure-skill> |
| Upstream commit | `49d529f` |
| Upstream version | 4.1.0 |
| Vendored at | 2026-09-04 |
| Sync cadence | monthly (via `devops/skill-sync-manager/`) |

## What's included

The full upstream repo (minus exclusions below):

- `SKILL.md` — router entry (5 sub-skill routing)
- `skills/patent-disclosure/` — 交底书 (disclosure drafting, largest sub-package)
- `skills/patent-search/` — CNIPA 著录检索
- `skills/patent-reader/` — 专利通俗解读
- `skills/patent-oa/` — 审查答复 (office action)
- `skills/patent-exam-policy/` — 政策简报
- `scripts/`, `INSTALL.md`, `requirements.txt`, `LICENSE`

## What's intentionally excluded

| Path | Reason | Restore |
|------|--------|---------|
| `docs/` | 3.5 MB demo screenshots (效果例-*.png/jpg) — pure marketing visuals | `git clone` upstream; see its `docs/` |

## Local modification (ultraskills-only)

- Added `tags:` to root `SKILL.md` frontmatter — required by ultraskills
  pre-commit skill validation. No other upstream code modified.

## Dependencies (user-side)

Python 3.9+ / Playwright — see upstream `INSTALL.md`.

## Sync procedure (monthly)

```bash
git clone --depth 1 https://github.com/handsomestWei/patent-disclosure-skill.git /tmp/patent
rm -rf /tmp/patent/.git /tmp/patent/docs
rsync -a --delete /tmp/patent/ community/patent-disclosure-skill/
# re-add ultraskills tags to SKILL.md frontmatter, update UPSTREAM.md commit/version
python3 scripts/arena_scan.py
python3 scripts/arena_cluster_score.py
python3 scripts/arena_build_index.py
```

## Compliance

- License: MIT — preserved (`LICENSE`).
- Upstream already mandates human review before submitting OA responses
  (审查答复输出须人工审核), consistent with ultraskills compliance standards.
- No modification to upstream logic; only frontmatter `tags` added.
