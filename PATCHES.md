# Deviations from upstream

Every change to `src/ff` or `src/metric-ff` relative to the pristine import
(commit `678eb18`) is listed here: file, reason, and evidence that output is
unchanged (golden check command and result).

## Applied

Both approved by the maintainer at Checkpoint 1 (2026-11-11), each in its own
commit. The golden reference was re-recorded as "pristine + UB-1 + UB-2".

| ID | Commit | File | Problem | Fix |
|---|---|---|---|---|
| UB-1 | `5a2b30f` | `src/metric-ff/scan-fct_pddl.y:290` | `gparse_optimization = $3;` keeps a pointer into bison's value stack (union member `char string[MAX_LENGTH]`). After `yyparse` returns the pointer dangles; on large problems the stack was heap-allocated and freed → heap-use-after-free (ASan, read in `inst_pre.c:526` `strcmp`) → SIGSEGV, or "unknown optimization method . check input files", or a wrong metric. Affects every problem with a `:metric`; small ones work by luck. | Copy the token: `gparse_optimization = new_Token( strlen($3)+1 ); strcpy( gparse_optimization, $3 );` |
| UB-2 | `d389fd8` | `src/metric-ff/parse.c:1039` | `make_conjunction_of_atoms`: after removing a trailing `NOT` literal `i` becomes NULL and `i->connective` is read → SIGSEGV (e.g. IPC-1998 movie). FF 2.3's version of the function does not have the bug. | Guard: `if ( i && i->connective != NOT )` (no other change of logic) |

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

## Phase 1: portability (Linux x86-64)

Evidence for every entry: the regression check of CLAUDE.md rule 3 on the full
corpus (`examples/manifest.json corpus/synthetic.json corpus/ipc.json`,
1275 runs), comparing against `golden/` with the binaries named in the entry.
"Identical" means 0 mismatching fields.

| ID | Files | Problem | Change | Evidence |
|---|---|---|---|---|
| P-GLOB-1 | FF `main.c`, `search.c`; Metric-FF `main.c`, `expressions.c`, `relax.c` | Tentative definitions of the same global in two files (`gbracket_count`, FF `lcurrent_goals`, Metric-FF `lnum_F` and `lF`) only link with `-fcommon`, which merges each pair into one object. GCC ≥ 10 and Clang ≥ 11 default to `-fno-common`. Metric-FF's `lF` is even declared with two types (`int lF[25]` in `expressions.c`, `int *lF` in `relax.c`), so the merged object was used as both. | `gbracket_count`, `lcurrent_goals`, `lnum_F`: one definition, `extern` elsewhere (keeps the sharing exactly). `lF`: `static` in each file; equivalent because every use of the array is inside `transform_to_LNF()` and `relax.c` assigns its pointer in `initialize_fixpoint()` before reading it, during search. | gcc-12 `-fno-common`: identical (1275 runs) |
| P-PARSE-1 | `scan-fct_pddl.y`, `scan-ops_pddl.y` (both planners) | `fcterr`/`opserr`, `yyerror` and `yylex` were used without a declaration; Clang rejects the resulting conflicting types for `fcterr`/`opserr`, and implicit declarations are errors in GCC ≥ 14 and Clang ≥ 16. `yyerror()` was called with no argument although it is defined with one (UB; the argument is unused). The parameter name `errno` breaks wherever `<errno.h>` defines `errno` as a macro. | Prototypes in the grammar prologue; `yyerror()` → `yyerror( NULL )`; parameter `errno` → `err` (both functions have empty bodies upstream). | gcc-12 and clang-14: identical (1275 runs each) |
| P-DECL-1 | Metric-FF `search.h` | `main.c` calls `do_Astar_epsilon()` without a prototype (implicit `int` function, defined `void`); `search.h` instead declares a `do_Astar_epsilon_repairing` that does not exist. | Add the prototype `void do_Astar_epsilon( void );`. | gcc-12 and clang-14: identical (1275 runs each) |
| P-COMPAT-1 | `ff.h` (both), FF `inst_final.c`, Metric-FF `inst_final.c`, `search.c`; new `src/compat/compat.h`, `compat_random.c`, `tests/compat/test_random.c` | Both planners take state-hash values and Metric-FF its A*-epsilon tie-break coin from the C library's `random()`. Its sequence differs between C libraries and Windows has none (CLAUDE.md rule 10). | `random()`/`srandom()` → `compat_random()`/`compat_srandom()`: an independent implementation of glibc's default (TYPE_3) generator. `tests/compat/test_random.c` compares it with glibc: unseeded and 9 seeds × 10 000 values, seeds 0–999 × 1 000 values, re-seeding: identical. The binaries no longer import `random`/`srandom` (`nm -u`). | gcc-12 and clang-14: identical (1275 runs each, including the `-s 4` cases whose plans depend on the coin) |
| P-COMPAT-2 | `ff.h`, `main.c` (both), FF `inst_final.c`; new `src/compat/compat_time.c` | CPU times come from POSIX `times()`/`struct tms` and FF's seed from `ftime()` (`<sys/times.h>`, `<sys/timeb.h>`): not available on Windows; `ftime` is deprecated. | `compat_times()` fills the same two fields in 1/100 s (`getrusage` on POSIX, `GetProcessTimes` on Windows); `compat_clock_millis()` returns the wall clock's milliseconds (`gettimeofday` / `GetSystemTime`), still used as FF's seed. Only the reported times can change, and they are masked by the normaliser. | gcc-12 and clang-14: identical (1275 runs each) |
| UB-3 | `main.c` (both) | `-p`, `-o` and `-f` arguments were copied with `strncpy(dst, arg, 256)` into 256-byte buffers (no terminator if the argument has ≥ 256 characters), then `sprintf(ops_file, "%s%s", path, file)` into another 256-byte buffer. A long path overflowed the stack: the reference build aborts with `*** buffer overflow detected ***` (exit 134, `_FORTIFY_SOURCE`); elsewhere it is silent memory corruption. Realistic for students with deep folders, especially on Windows. | Arguments longer than 255 characters are rejected: "ff: argument of option -X is too long (at most 255 characters)" followed by the usage text, exit 1; a path plus file name longer than 255: "ff: path and file name too long (at most 255 characters)", exit 1. `MAX_LENGTH` unchanged (rule 5). New synthetic cases `cli/long-argument`, `cli/long-path` (before: crash, now `usage-error`) and `cli/path-near-limit` (253 characters, still `plan-found`); new classifier rule. **Diagnostic text added** (rule 3). | gcc-12 and clang-14: identical on the 1275 existing runs; the 6 new runs recorded with this build |
| P-GEN-1 | generated `lex.*.c`, `*.tab.c` (both); `tools/regen-parsers.sh` | The flex scanners included `<unistd.h>` and called `isatty(fileno(...))`, absent on Windows; under `-ansi` `fileno` was implicitly declared. | Generated parsers are committed (bison 3.8.2, flex 2.6.4; UPSTREAM.md). flex runs with `--nounistd --never-interactive`: no `<unistd.h>`, no `isatty`/`fileno`. For the regular files the planners read, flex already chose the non-interactive code path. | CMake build, gcc-12 and clang-14: identical (1281 runs each) |
| P-BUILD-1 | new `CMakeLists.txt`; upstream makefiles kept but unused | Upstream makefiles need flex/bison, use `-O6` and do not build on Windows. | One CMake build for both planners and `src/compat`: FF as C99 with GNU extensions (upstream `-std=gnu99`), Metric-FF as strict C90 (upstream `-ansi`), `-O3` (Release), `-ffp-contract=off`, `-Wall -Wextra`; `ctest` runs the `random()` test. `tools/build-reference.sh` now builds the golden-reference binaries from the frozen sources of commit `d389fd8` (byte-identical to before). | gcc-12 and clang-14: identical (1281 runs each); 0 implicit declarations |
| UB-4 | `search.c` (both): `state_sum`, Metric-FF `logical_state_sum` | UBSan: signed `int` overflow in Metric-FF `state_sum` (`sum += rand * (int) fluent_value`, `search.c:1839`) in 69 runs of the corpus (IPC-2002 numeric domains); the hash key is meant to wrap. FF's sum over facts can overflow likewise for states with more than ~1430 true facts (not reached by the corpus). | Accumulate in `unsigned int` (modulo 2³²) and convert back to `int`: the same value two's-complement wrap-around produced, without undefined behaviour. | gcc-12 and clang-14: identical (1281 runs each); ASan+UBSan on the 69 runs: 0 findings |

## Capacity limits (release 0.2.0)

Exception to CLAUDE.md rule 5, approved by the maintainer on 2026-11-14 for the
ABIA planning assignment, whose travel catalogues (Spain, Europe) exceed the
upstream limits. Measured upstream limits (Metric-FF 2.1 / FF 2.3 as distributed in 0.1.0):
about 10 000 elements in one list (`:init`, `:objects`; bison's default stack depth,
reported as a misleading "syntax error"), 2000 objects, 1000 relevant fluents
(Metric-FF), plans of 500 steps (Metric-FF; FF already 2000).

| ID | Files | Problem | Change | Evidence |
|---|---|---|---|---|
| CAP-1 | `ff.h`, `scan-fct_pddl.y`, `scan-ops_pddl.y` (both) and the regenerated `*.tab.c` | Fixed capacity limits too small for course problems. The parser stack limit is bison's default `YYMAXDEPTH` 10 000, and lists are right-recursive (one stack entry per element), so a longer list stopped with "syntax error in line N", which students read as an error in their PDDL. | `YYMAXDEPTH` 10 000 → 1 000 000 (defined in the grammar prologue; the stack is `malloc`ed and grows by doubling, so only problems that need it pay for it). `MAX_CONSTANTS` and `MAX_TYPE` 2000 → 20 000, `MAX_RELEVANT_FACTS` 100 000 (FF) / 150 000 (Metric-FF) → 1 000 000; Metric-FF only: `MAX_RELEVANT_FLUENTS` 1000 → 10 000, `MAX_PLAN_LENGTH` 500 → 2000. A parser stack overflow now prints "FILE: problem too large in line N: too many list elements or too deep nesting! increase YYMAXDEPTH (currently 1000000)", exit 1 as before; new classifier rule (`limit-exceeded`). **Diagnostic text added** (rule 3); the other limits keep their upstream messages ("too many constants! increase MAX_CONSTANTS …"). The grammar stays right-recursive (no change in the order of facts or in any output); every other limit is unchanged. Cost: all tables are static arrays, none quadratic in a raised limit; BSS grows from 4.1 to 33.9 MB (FF) and 5.7 to 34.8 MB (Metric-FF), virtual and zero-filled, so it costs memory only when touched: peak RSS on `examples/hanoi` grows from about 3 MB to 7.7 MB (the `gis_member`/`gmember_nr` tables, 20 000 × 50, are initialised at start-up). | See below |
| CAP-2 | `memory.c` (both): `free_PlNode` | With longer lists, freeing the parse tree of `:init` recursed once per element along `next` and overflowed the C stack: SIGSEGV from about 150 000 facts with an 8 MB stack (Linux, macOS) and from about 30 000 with 1 MB (Windows' default). | Loop over `next` instead of recursing (recursion on `sons` kept). Only the order in which nodes are `free`d changes. With CAP-1 and CAP-2: 998 001 facts in `:init` run to the end with a 1 MB stack. | See below |
| CAP-3 | `memory.c`, `memory.h`, `inst_pre.c`, `inst_hard.c`, `inst_final.c` (both) | The instantiation phase builds dense tables with one entry per possible fact or fluent: FF multiplies the sizes of the argument types; Metric-FF does the same for its reachability tables but uses the **total number of objects** for every argument of its initial-state table (`inst_hard.c`) and of its fluent tables (`inst_final.c`). The product is computed in `int`: above 2³¹−1 entries it overflowed (undefined behaviour) and the planner crashed (SIGSEGV; ASan: `calloc parameters overflow`). Already in upstream (Metric-FF with an arity-3 predicate and more than 1290 objects), but CAP-1 makes it much easier to reach (reported from the planning assignment: about 3700 objects and `(trayecto ?t ?o ?d)`). The `calloc` results were not checked. | Before each table is computed, its number of entries is computed in `double` and, above `INT_MAX`, the planner stops: "too many objects for predicate P of arity k: its instantiation table would need N entries (X GB), more than 2147483647! use fewer objects", exit 1 (`limit-exceeded`, new classifier rule). Tables below that size are computed exactly as before; a failed `calloc` now stops with upstream's own `NO MEMORY in file …` message (`CHECK_PTR`). The tables are not made sparse (that would change the instantiation code). **Diagnostic text added** (rule 3). Memory is still the practical limit: Metric-FF's initial-state table needs 4 bytes × objects^arity per predicate (20 000 objects and arity 2: 1.6 GB). | Full corpus identical (see below); new cases `capacity/dense-1291` (initial-state and reachability tables), `capacity/dense-negated-1291` (the `NOT-` predicate created for a negative precondition, `inst_pre.c`) and `capacity/dense-fluent-1291` (Metric-FF fluent table): 0.1.0 crashes with SIGSEGV on all of them, now `limit-exceeded`. A case just below the bound is not in the corpus: 1290³ entries need about 8.6 GB. |

Evidence for CAP-1, CAP-2 and CAP-3 (2026-11-15, CMake build, GCC, Linux x86-64):

- Regression check on the full corpus (`examples/manifest.json corpus/synthetic.json
  corpus/ipc.json`): 1281 runs, 0 mismatching fields. No case of the corpus was near the
  old limits.
- New synthetic cases `corpus/synthetic/capacity/` (generated by
  `tools/make-capacity-cases.py`), recorded with this build. For each limit, one case just
  above the upstream limit (upstream: limit-exceeded or "syntax error"; now plan-found), one
  at the new limit (plan-found) and one just above it (limit-exceeded): `objects-2001`,
  `objects-20000`, `objects-20001`; `init-10201`; `chain-501`, `chain-2000`, `chain-2001`;
  `fluents-500`, `fluents-4999`, `fluents-5000` (N objects give 2N+1 relevant fluents).
- The parser stack limit itself is not in the corpus (a problem above it is about 16 MB).
  Tested by hand: 1 002 001 facts in `:init` gives the new message after 0.9 s with both
  planners; 998 001 facts parse and run to the end (FF: about 5 s, 600 MB peak RSS).
  Metric-FF's preprocessing is slow on huge static `:init` sections (upstream behaviour,
  not changed): 200 000 facts about 19 s, 500 000 about 150 s.
- A 50 000-conjunct goal and 50 000 `:init` facts with a 1 MB stack: plan-found, no crash.
- ASan + UBSan (clang-14, `harness.studies.sanitize --no-aslr`) on the full corpus plus the
  new cases: 1301 runs, 0 findings, every outcome equal to the golden.
