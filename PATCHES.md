# Deviations from upstream

Every change to `src/ff` or `src/metric-ff` relative to the pristine import
(commit `36a8841`) is listed here: file, reason, and evidence that output is
unchanged (golden check command and result).

## Applied

Both approved by the maintainer at Checkpoint 1 (2026-11-11), each in its own
commit. The golden reference was re-recorded as "pristine + UB-1 + UB-2".

| ID | Commit | File | Problem | Fix |
|---|---|---|---|---|
| UB-1 | `7dc96b6` | `src/metric-ff/scan-fct_pddl.y:290` | `gparse_optimization = $3;` keeps a pointer into bison's value stack (union member `char string[MAX_LENGTH]`). After `yyparse` returns the pointer dangles; on large problems the stack was heap-allocated and freed → heap-use-after-free (ASan, read in `inst_pre.c:526` `strcmp`) → SIGSEGV, or "unknown optimization method . check input files", or a wrong metric. Affects every problem with a `:metric`; small ones work by luck. | Copy the token: `gparse_optimization = new_Token( strlen($3)+1 ); strcpy( gparse_optimization, $3 );` |
| UB-2 | `7607944` | `src/metric-ff/parse.c:1039` | `make_conjunction_of_atoms`: after removing a trailing `NOT` literal `i` becomes NULL and `i->connective` is read → SIGSEGV (e.g. IPC-1998 movie). FF 2.3's version of the function does not have the bug. | Guard: `if ( i && i->connective != NOT )` (no other change of logic) |

### Evidence (2026-11-11)

Build before the commits: pristine Metric-FF plus exactly the two lines above, same compiler and
flags as the reference (`build/ubfix/metric-ff`). Command:

```sh
taskset -c 0,1,4,5 python3 -m harness check --ff build/reference/ff \
    --metric-ff build/ubfix/metric-ff -j 4 \
    examples/manifest.json corpus/synthetic.json corpus/ipc.json
```

1248 runs (per-run result: `reports/data/ubfix-check.json`). Golden outcome → outcome with the fixes:

| Golden (pristine) | With UB-1 + UB-2 | Runs |
|---|---|---|
| plan-found | identical (plan, stdout, stderr, exit code) | 618 / 618 |
| proven-unsolvable | identical | 32 / 32 |
| search-failed | identical | 15 / 15 |
| usage-error | identical | 236 / 236 |
| timeout | identical | 1 / 1 |
| parse-error (`syntax error`, malformed synthetic input) | identical | 66 / 66 |
| parse-error "unknown optimization method … check input files" (garbled metric, UB-1) | plan-found 38, timeout (120 s) 52, usage-error 14 | 104 |
| crash (SIGSEGV) | plan-found 48, timeout (120 s) 86, usage-error 42 | 176 |

Every run that did not crash or misparse is unchanged. The 280 changed runs are
all in IPC-1998 movie (UB-2) and the IPC-2002 numeric domains (UB-1). The
`usage-error` results after the fix are Metric-FF's own message "Optimization
criterion not established. A*epsilon not defined." for `-s 5` on problems whose
metric is `maximize` (satellite-hard, driverlog-hard) or absent (movie).

Under rule 4 the golden outputs of these 280 runs change; the maintainer
approved the change. After the commits:

- `tools/build-reference.sh` built from `src/` is identical in source to the
  build above; the FF binary is byte-identical to the pristine one.
- The 138 runs that now hit the 120 s limit were removed from `corpus/ipc.json`
  (see `corpus/SOURCES.md`). Re-recording changed exactly the 142 expected golden
  files (86 now plan-found, 56 now Metric-FF's own usage error) and no other.
- `python3 -m harness check` with the new reference: 1110 runs, 0 mismatching
  fields.
