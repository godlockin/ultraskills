# Example 1 — Read-only scan

Use `--summary` to inventory all repos and see which need updates, without touching anything.

## Command

```bash
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/working/sourcecode --summary
```

## Output

```
=== git-batch-sync ===
ROOT          : /Users/chenchen/working/sourcecode
SUMMARY       : yes
TOOLS         : fd=1 rg=1 eza=1 bat=1 delta=1 dust=1 tokei=1 hyperfine=1 just=1
----------------------------------------
▶ Repos found: 42
----------------------------------------

[1/42] research/LLM/transformers
  branch=main ahead=0 behind=0
  ✓ up-to-date

[2/42] my_projects/api-server
  branch=main ahead=2 behind=5
  ⚠ needs update (behind=5)

[3/42] my_projects/fork-of-lib
  ⊟ fork upstream: https://github.com/original/lib.git
  branch=main ahead=0 behind=12
  ⚠ needs update (behind=12)
  ...

========================================
Summary
========================================
Total          : 42
Forks          : 3 (synced=0)
Up-to-date     : 28
Updated        : 0
Pushed         : 0
Dirty          : 1
Conflicts      : 0
Skipped        : 2
Errors         : 0
Elapsed        : 1s
Log            : /tmp/claude-tasks/git-batch-sync-20260908-233715.log
```

## Notes

- Detects forks via `remote.upstream.url` (output shows `⊟ fork`)
- Skips detached HEAD and repos with no upstream
- Fast (1s for 42 repos with fd)
- Safe — read-only, no fetch/pull
