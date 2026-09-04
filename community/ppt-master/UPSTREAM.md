# ppt-master (ultraskills vendored snapshot)

This directory is a **snapshot import** of
[hugohe3/ppt-master](https://github.com/hugohe3/ppt-master) (MIT licensed),
tracked in the ultraskills `community/` index.

| Field | Value |
|-------|-------|
| Upstream | <https://github.com/hugohe3/ppt-master> |
| Upstream commit | `879b533` |
| Upstream version | 6.2.0 |
| Vendored at | 2026-09-04 |
| Sync cadence | monthly (via `devops/skill-sync-manager/`) |

## What's included

The full upstream `skills/ppt-master/` package:

- `SKILL.md` — workflow authority (upstream entry point)
- `workflows/` — routing, profiles, stages, governance
- `scripts/` — 80+ Python tools (SVG ↔ PPTX, image, animation, TTS, …)
- `references/` — role references, design specs, palettes (43 MB; bulk is `ai-image-comparison/`)
- `templates/` — brands / charts / decks / scaffolds / schemas / layouts / tables (binary-free)

## What's intentionally excluded

| Path | Reason | Restore |
|------|--------|---------|
| `templates/icons/` | 48 MB binary icon library | `git restore templates/icons/ && git checkout upstream/main -- templates/icons/` |
| `templates/sounds/` | 12 MB audio narration library | `git restore templates/sounds/ && git checkout upstream/main -- templates/sounds/` |

To restore, fetch the upstream tree directly:

```bash
git clone --depth 1 https://github.com/hugohe3/ppt-master.git /tmp/ppt
cp -r /tmp/ppt/skills/ppt-master/templates/icons community/ppt-master/templates/
cp -r /tmp/ppt/skills/ppt-master/templates/sounds community/ppt-master/templates/
```

The skill's own `attribution_guard.py` will still pass — vendoring marker is
recorded in the YAML frontmatter of the inner `SKILL.md` and here.

## How to invoke

ultraskills hub routes to this skill by the directory name `ppt-master`.
The workflow authority is `${SKILL_DIR}/SKILL.md` (this directory, **not** the
inner `skills/ppt-master/`). Inside the skill, the `attribution_guard.py`
gate still validates upstream provenance.

## Sync procedure (monthly)

```bash
# 1. fetch latest upstream
git fetch upstream

# 2. dry-run diff
diff -ru community/ppt-master upstream/skills/ppt-master --exclude=icons --exclude=sounds

# 3. apply (review carefully — upstream is S-tier, no Tier-1 AB review required)
rsync -a --exclude=icons --exclude=sounds \
    upstream/skills/ppt-master/ community/ppt-master/

# 4. update vendored_at + upstream_commit
$EDITOR community/ppt-master/UPSTREAM.md
$EDITOR community/ppt-master/SKILL.md  # inner frontmatter

# 5. rebuild arena index (the skill must remain indexed)
python3 scripts/arena_scan.py
python3 scripts/arena_cluster_score.py
python3 scripts/arena_build_index.py
```

## Compliance

- License: MIT — preserved (`LICENSE` file copied from upstream).
- Copyright: Hugo He 2025–2026 — preserved in vendoring metadata.
- No modifications to upstream code; this snapshot is read-only for code, write-
  only for vendoring metadata.
- Attributed via the inner SKILL.md frontmatter (which already references the
  official repository).