# Example 5 — When NOT to use this skill (monorepo boundary)

This skill treats each `.git/` as a unit. Some directory layouts look like "many repos" but are actually one. Use the right tool.

## Decision

```bash
find ~/code -maxdepth 3 -name '.git' -type d | wc -l
# ≥ 3 → git-batch-sync.sh is appropriate
# < 3 → just use `git pull` directly
```

## NOT a use case — pnpm/lerna/yarn workspaces

```
my-app/                    # ONE git repo
├── .git/
├── package.json           # workspaces config
├── apps/
│   ├── web/package.json
│   └── mobile/package.json
└── packages/
    ├── ui/package.json
    └── api/package.json
```

**Why not**: This is one repo. `git pull` updates everything atomically. Using `git-batch-sync.sh` here would find only `my-app/.git/` (since packages/ have no `.git`) — script would do nothing useful.

```bash
cd my-app && git pull              # ← right tool
# or
pnpm -r update                     # ← for package deps
```

## NOT a use case — Cargo workspace

```
rust-project/              # ONE git repo
├── .git/
├── Cargo.toml             # [workspace] members = [...]
├── crates/
│   ├── core/Cargo.toml
│   └── cli/Cargo.toml
```

**Why not**: Same as above. One repo, one `.git/`.

## NOT a use case — Submodules

```
parent-repo/               # ONE git repo, with submodules
├── .git/
├── .gitmodules            # lists submodules
└── vendor/
    ├── lib-a/             # git submodule (own .git/)
    └── lib-b/             # git submodule
```

`git-batch-sync.sh` would try to sync `lib-a/` and `lib-b/` as independent repos, but they're tracked by the parent. The right tool:

```bash
cd parent-repo
git submodule update --init --recursive   # ← right tool
git pull                                  # parent first
git submodule update --remote             # then submodules
```

## YES a use case — Multiple unrelated OSS clones

```
~/work/
├── kubernetes/.git/
├── terraform/.git/
├── prometheus/.git/
└── grafana/.git/
```

4 separate projects, each is its own repo with its own origin. Perfect fit.

```bash
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/work --summary
```

## YES a use case — Mix of own + forks

```
~/code/
├── my-saas/.git/                  # own project (no upstream)
├── fork-of-postgres/.git/         # fork (remote.upstream = postgres/postgres)
├── fork-of-redis/.git/            # fork
└── oss-clone/.git/                # plain clone
```

Perfect fit. Use `--sync-upstream` to keep forks current with their upstream.

```bash
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/code --sync-upstream --skiplist=~/internal.txt
```

## Yes, but with caveat — nested repos with submodules

```
parent-repo/
├── .git/
└── vendor/
    └── lib/                       # submodule, has its own .git/
```

Script will:
- Sync `parent-repo/` (origin pull)
- Sync `vendor/lib/` as if independent (fetch + pull against its origin, not parent)

This may diverge from parent's tracked submodule SHA. **Solution**: After running this skill, also run `git submodule update --recursive` in the parent.

## Edge case — repos inside `.git/info/`

Some workflows (e.g. worktrees) put nested `.git` files (not directories). fd/find only match directories. These are skipped automatically.

## When in doubt

```bash
# Check what the skill would see
bash $SKILL_DIR/scripts/git-batch-sync.sh --summary
```

If `Repos found: N` matches what you expect, proceed. If not, restructure first.
