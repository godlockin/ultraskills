# Example 4 — Benchmark + LOC stats

`--bench` runs `hyperfine fd vs find`, `--stats` runs `tokei` for language stats.

## Combined

```bash
bash $SKILL_DIR/scripts/git-batch-sync.sh ~/working/sourcecode --bench --stats --summary
```

## Output (excerpt)

```
=== git-batch-sync ===
TOOLS         : fd=1 rg=1 tokei=1 hyperfine=1
----------------------------------------
▶ Repos found: 42
----------------------------------------

── hyperfine: fd vs find ──
Benchmark 1: fd --type=dir --hidden --no-ignore --max-depth=8 --glob '.git' /Users/chenchen/working/sourcecode >/dev/null
  Time (abs ≡):         52.4 ms               ┌──┐
                        [6.13 ms .. 58.1 ms]   │██│
  User time (abs ≡):    33.7 ms
  System time (abs ≡):  39.5 ms

Benchmark 2: find /Users/chenchen/working/sourcecode -maxdepth 8 -type d -name .git >/dev/null
  Time (abs ≡):         587.3 ms              ┌────┐
                        [567 ms .. 612 ms]    │████│
  User time (abs ≡):    274.1 ms
  System time (abs ≡):  312.7 ms

Summary
  'fd' ran
    11.21 ± 1.05 times faster than 'find'

── tokei: language stats ──
===============================================================================
 Language            Files        Lines         Code     Comments       Blanks
===============================================================================
 Python               1245      412338       298445        58234        55659
 Rust                   342      187221       152443         8921        25857
 TypeScript             891      156443       128993        11234        16216
 Go                     234      112998        91234        10234        11530
 Markdown               567       45321            0        38021         7300
 ...

───────────────────────────────────────────────────────────────────────────────
 Total                4789     1284593      1053292       123452       107849
===============================================================================
```

## Just recipes

```bash
just bench     # fd vs find benchmark only
just stats     # tokei LOC only
just all       # bench + stats + summary combined
```

## Interpreting

- `fd` typically 10-30x faster than `find` on repo trees (multi-threaded, respects `.gitignore`)
- `tokei` excludes `node_modules` `dist` `build` `.venv` `target` etc. — see `--exclude` flags
- Both tools are optional — if missing, the script prints a `brew install X` hint and continues
