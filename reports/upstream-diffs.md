# Third-party forks of FF 2.3 / Metric-FF 2.1: annotated diff analysis

Status: analysis only. Nothing in this report has been applied to `src/`.
Baseline: pristine upstream trees in `src/ff/` (FF 2.3) and `src/metric-ff/`
(Metric-FF 2.1), commit `a9e3d7c`. All `file:line` references without a fork
prefix point into `src/`.

## Method and limits

- Each fork was inspected commit by commit with `git show <hash>`. Trees were
  compared with the baseline using `git archive <hash> | tar -x` and `diff -r`.
- Fork code was **read, not built or run**. Statements that a fork build
  "would fail" are inferences from reading the code and the system headers,
  and are marked as such.
- The pristine trees were built in a scratch copy, with GCC 11.4, flex 2.6.4,
  bison and glibc 2.35, to list link errors and warnings. Section 2 relies on
  that build.
- Classification of hunks:
  - **build**: makefile, flags, generated-file handling.
  - **portability**: needed to compile, link or run on some platform or compiler, with no intended behaviour change.
  - **semantic**: can change plans, search behaviour, stdout/stderr content, defaults or exit codes.
  - **cosmetic**: whitespace, comments, README.
- The licence rule (CLAUDE.md rule 8) is applied per fork. For the forks whose
  licence is unclear, changes are described in words, with excerpts of a few
  lines at most.

| Fork | Remote | HEAD | Licence | Use |
|---|---|---|---|---|
| Vidminas | github.com/Vidminas/metric-ff-crossplatform | `12175ca` | GPL-2.0 `LICENSE` | may copy, but see verdicts |
| tranchis | github.com/tranchis/metric-ff-macos | `c12256f` | `LICENSE` is GPL-3.0; README says GPL-2+ | reference only |
| ronuchit | github.com/ronuchit/FF | `e5176df` | no licence file | reference only |
| mokhtarivahid | github.com/mokhtarivahid/pddl-solvers | `13272d1` | no top-level licence; README defers to each planner | reference only |

---

## 0. Summary tables

### 0.1 Vidminas/metric-ff-crossplatform (Metric-FF 2.1 base)

Base `b0ba55e` (2022-04-04) has the same bytes as `src/metric-ff`, apart from
`.gitignore`, `LICENSE` and `README`. This was verified earlier and accepted
here.

| Commit | Files | Class | Verdict |
|---|---|---|---|
| `ab96497` sys/times.h compat | `ff.h`, new `times.c`, `times.h` | portability (time lines only) | **adopt idea**, own implementation |
| `92d7adb` makefile | `makefile` | build | irrelevant (we use our own build) |
| `7ee379c` prototypes fcterr/opserr | `scan-*.y`, `.gitignore` | portability | **adopt idea**, but rename the `errno` parameter |
| `c517363` random()→rand() | `inst_final.c`, `search.c` | **SEMANTIC** | **avoid** |
| `212b887` extern globals | `main.c`, `relax.c` | portability (link) | **adopt idea** for `gbracket_count`; handle `lF` differently (type mismatch) |
| `3aa57c6` makefile | `makefile` | build | irrelevant |
| `c76cb05` README | `README.md` | cosmetic | irrelevant |
| `5673be8` format all code | all `.c`/`.h`, `README.md` | cosmetic (verified, see 1.1) | **avoid** (destroys diffability against upstream) |
| `8c73f65` MinGW fixes | `makefile`, `times.h` | portability/build | adopt idea (MinGW already defines `struct timeval`) |
| `9ad30f9` README | `README.md` | cosmetic | irrelevant |
| `c1e1d53` move into `v2.1/` | renames, `makefile` output paths | build | irrelevant |
| `390c1c2`, `aca44a0`, `c9c9bf9`, `4c55e4a`, `12175ca` | `v1.0/*`, README | Metric-FF 1.0 port | irrelevant (not our version) |

### 0.2 tranchis/metric-ff-macos

`10d7ede` has the same bytes as `src/metric-ff` (`diff -r` shows only the added
`LICENSE`), so it is Metric-FF 2.1.

| Commit | Files | Class | Verdict |
|---|---|---|---|
| `4591827` initial commit | `LICENSE` (GPL-3.0 text) | licence | note the inconsistency (see 1.2) |
| `10d7ede` "Original codebase" | 27 files | none (pristine Metric-FF 2.1) | n/a |
| `f37ce43` macOS compilation | `scan-fct_pddl.y`, `scan-ops_pddl.y`, `search.h` | portability | **adopt idea** (reimplement; do not copy) |
| `d368605` README | `README.md` | cosmetic | irrelevant |
| `c12256f` "Rollback to 1.0" | 27 files, adds `llparse.c`, `parse.c.patch` | replaces 2.1 with Metric-FF 1.0 | **avoid** (wrong version; probably does not compile, see 1.2) |

### 0.3 ronuchit/FF (FF 2.3 base, modified)

| Commit | Files | Class | Verdict |
|---|---|---|---|
| `3d9691d` "original planner that causes errors" | 28 files | older FF 2.3 plus Siddharth Srivastava's state-printing edits: **semantic** (output) | **avoid** |
| `bfed732` "patch" | 12 files | brings the tree to the same bytes as official `src/ff`, except `scan-*.y` and README; the `scan-*.y` change is portability | irrelevant (we already have the official tree); the scan-*.y idea is superseded |
| `e5176df` "suppress a warning" | `makefile` (`-Wno-implicit`) | build | **avoid** (hides the warning instead of fixing the cause) |

### 0.4 mokhtarivahid/pddl-solvers

| Item | Class | Verdict |
|---|---|---|
| `planners/ff` (modified FF 2.3) | semantic (grammar recursion, `MAX_*` limits, output file) + portability (`extern`) | **avoid**; the `extern` idea is already listed above |
| `planners/metric-ff` (Metric-FF **1.0** + `extern` edits) | portability | irrelevant (wrong version) |

---

## 1. Per-fork analysis

### 1.1 Vidminas/metric-ff-crossplatform

#### `ab96497` "Add sys/times.h compat replacement" (portability)

- `ff.h`: replaces the three includes `sys/types.h`, `sys/timeb.h` and
  `sys/times.h` (`src/metric-ff/ff.h:50-52`) with `#include "times.h"`.
- New `times.h`: on non-Windows it includes `<sys/times.h>`. On `_WIN32` it
  declares its own `struct timeval`, `gettimeofday()`, a copy of glibc's
  `struct tms` and `times()`, and also defines `__need_clock_t` (a
  glibc-internal reserved name).
- New `times.c` defines `times()` as `clock()` written into `tms_utime`, with
  `tms_stime = 0`. It also defines `gettimeofday()` on top of `_ftime()`.
- **`times.c` has no `#ifdef _WIN32` guard.** It uses `struct _timeb` and
  `_ftime`, which exist only in the Microsoft CRT. glibc's `<sys/timeb.h>`
  declares only `struct timeb` and `ftime`
  (`/usr/include/x86_64-linux-gnu/sys/timeb.h:25,29`). This was not built, but
  from reading the code the tree should not compile unchanged on Linux or
  macOS. If it did compile, it would also replace libc's `times()` there.
- Effect on output: `TIME()` (`src/metric-ff/ff.h:312-313`) divides tick
  deltas by a hard-coded `100.0`. On Windows `clock()` counts in
  `CLOCKS_PER_SEC` = 1000 units and measures wall time, not CPU time. The
  reported times would therefore be about 10× too large and would not be CPU
  times. Only time lines change, which the golden rule tolerates. Still, our
  implementation should scale correctly.
- `gettimeofday()` is never called by Metric-FF, so that part is dead code.
- Verdict: adopt the idea of a small Windows shim for `times()`/`struct tms`.
  Implement it ourselves in `src/compat/`, with a `_WIN32` guard and CPU time
  from `GetProcessTimes`, in units of 1/100 s, so that `TIME()` stays correct.

#### `92d7adb` "Update makefile" (build)

- `CC = clang`; `-O6 -ansi … -g` becomes `-O3 -ansi … -g`. GCC treats `-O6` as
  `-O3`, so code generation does not change.
- Windows branch: `LIBS` empty, `FLEX=./win_flex --wincompat`,
  `BISON=./win_bison`.
- Adds `times.c` to `SOURCES`. Irrelevant to us; `--wincompat` is worth knowing
  (it makes flex emit `<io.h>` instead of `<unistd.h>`).

#### `7ee379c` "Uncomment forward prototype fcterr and opserr declarations" (portability)

- `scan-fct_pddl.y:101` and `scan-ops_pddl.y:94`: removes the comment markers
  around `void fcterr( int errno, char *par );` and the `opserr` equivalent.
- Upstream commented these out because `errno` is a macro: glibc expands it to
  `(*__errno_location ())`, macOS to `(*__error())`, MSVC to `(*_errno())`.
  The parameter therefore turns into a function-pointer parameter. GCC reports
  the pristine definition as `void(int * (*)(), char *)`
  (`src/metric-ff/scan-fct_pddl.y:878`, `scan-ops_pddl.y:997`).
- This "works" only because prototype and definition expand the same way.
- Better fix: rename the parameter, as tranchis `f37ce43` does. The function
  bodies are entirely commented out upstream (`src/metric-ff/scan-fct_pddl.y:878-892`,
  `scan-ops_pddl.y:997-1011`, the same in FF), so the change has no runtime
  effect.
- `.gitignore`: ignores generated lexers/parsers and `data/`.

#### `c517363` "Replace random() calls with standard rand()" — **SEMANTIC**

Three live calls change (`inst_final.c:1950`, `inst_final.c:1962`,
`search.c:1371` in `src/metric-ff`), and two commented-out ones
(`search.c:1391,1400`):

```c
-    gft_conn[i].rand = random() % BIG_INT;
+    gft_conn[i].rand = rand() % BIG_INT;
...
-      coin = random() % 2;
+      coin = rand() % 2;
```

- `search.c:1371` is the A*-epsilon tie-break coin in
  `Astar_epsilon_select_first`, used by `-s 4` and by `-s 5` (the default,
  `src/metric-ff/main.c:671`) when EHC fails. The plan can therefore depend
  on it.
- `inst_final.c:1950/1962` feed the state-hash values (`state_sum`,
  `src/metric-ff/search.c:1829,1839,1855`). They also consume the generator
  before the search starts, so they shift the coin sequence.
- On glibc, `rand()` and `random()` share one generator. A check with a test
  program gave the same first five values, and `RAND_MAX` = 2147483647. **So
  the change does nothing on Linux.**
- On macOS, `rand()` is a different generator. On Windows (MSVC, MinGW/msvcrt)
  `rand()` is an LCG with `RAND_MAX` = 32767. Coin sequences and hash values
  then differ between platforms, which breaks CLAUDE.md rule 10.
- Verdict: **avoid**. Use the portable glibc-`random()`-compatible generator in
  `src/compat/`.

#### `212b887` "Declare globals extern where needed" (portability, link)

- `main.c:124`: `int gbracket_count;` becomes `extern int gbracket_count;`.
  Correct: the definition lives in `lex-fct_pddl.l:30`, which is `#include`d
  into `scan-fct_pddl.tab.c` (`src/metric-ff/scan-fct_pddl.y:867`).
- `relax.c:72-73`: `int *lF; int lnum_F;` become `extern`. **Caveat:** the
  only remaining definition is `int lF[MAX_LNF_F];` in
  `src/metric-ff/expressions.c:460`, an array of 25 ints. Declaring
  `extern int *lF` against an `int[25]` definition is a type mismatch and
  undefined behaviour (C11 6.2.7).
- It reproduces what `-fcommon` did upstream: both tentative definitions merge
  into one common symbol, and `relax.c:804` writes its `calloc` pointer into
  the first bytes of `expressions.c`'s array. This is harmless in practice only
  because `expressions.c` uses `lF`/`lnum_F` only during the LNF phase
  (`normalize_expressions`, `encode_lfns_as_artificial_fluents`, …), before
  `relax.c` initialises its own.
- Recommended fix: make both pairs `static` in their files, so there are two
  separate objects. Justify it in `PATCHES.md` with the disjoint-lifetime
  argument and confirm it with the golden corpus.

#### `3aa57c6` "Update makefile" (build)

`-ansi` becomes `-std=c89` (the same mode under another name). Drops `TYPE`,
`ADDONS` and `-g`, and adds `OUT_FILE` (`ff.exe` on Windows). Irrelevant.

#### `5673be8` "Format all code": verified cosmetic

- Check: for every `.c`/`.h` file, compare the parent and child after deleting
  all whitespace, and again after `gcc -fpreprocessed -dD -E -P` (comments
  stripped).
- All files except `ff.h` are identical at token level under both checks.
- `ff.h` differs only because the formatter split macro bodies with added
  `\`-newline continuations (`CHECK_PTR`, `TIME`). After also deleting
  backslash-newline, `ff.h` is identical too: same md5 for parent and child.
- Limit: deleting whitespace would not catch a change inside a string literal
  that only adds or removes spaces. clang-format does not touch string
  contents, so this is accepted.
- The `README.md` part only removes blank lines.
- Conclusion: **no non-whitespace change**. Still avoid it: it makes all later
  Vidminas commits impossible to diff against upstream, and it would break our
  "small upstream-traceable deltas" rule.

#### `8c73f65` "MinGW GCC compat fixes" (portability/build)

- `times.h`: wraps the private `struct timeval` in `#ifndef __MINGW32__`,
  because MinGW already defines it. Converts `//` comments to `/* */`
  (needed for `-std=c89`).
- `makefile`: `CC = gcc`.
- Idea worth keeping: a Windows shim must not redefine types that MinGW
  headers already provide.

#### `9ad30f9`, `c76cb05` (README, cosmetic); `c1e1d53` (moves files into `v2.1/`, build)

- `c1e1d53`: pure renames, except `v2.1/makefile`, which changes four lines
  (output to `../ff-v2.1[.exe]`, tools in `../`).

#### v1.0 commits (`390c1c2`, `aca44a0`, `c9c9bf9`, `4c55e4a`, `12175ca`)

- They add and port Metric-FF 1.0 under `v1.0/` and touch no file under
  `v2.1/`.
- `aca44a0` repeats the 2.1 changes on 1.0. `c9c9bf9` deletes `llparse.c` and
  `parse.c.patch` from `v1.0/`.
- Not analysed further.

### 1.2 tranchis/metric-ff-macos

- **Version:** `10d7ede` "Original codebase" has the same bytes as
  `src/metric-ff` (Metric-FF 2.1). `c12256f` "Rollback to 1.0" replaces the
  tree with Metric-FF 1.0: apart from the `.y` files, `LICENSE` and the
  README, it matches Vidminas `577aa9e` "Add Metric-FF 1.0 code".
- **Licence:** `4591827` adds a GPL-3.0 `LICENSE` (the GitHub template).
  `README.md` (`d368605`) quotes the GPL-2-or-later notice, and so do all
  source headers. The GPL-3.0 file therefore contradicts the README and the
  headers. Ownership of the author's own small edits is unclear, so treat the
  fork as reference only and reimplement independently.
- **`parse.c.patch`:** yes, present from `c12256f`, together with
  `llparse.c`.
  - It is a context diff from 2011, `Metric-FF/parse.c` against
    `Metric-FF-FTK/parse.c`.
  - It adds type-name collection and `make_either_ty` for
    `gparse_functions` arguments, so that `either` types work in function
    declarations.
  - It is not applied to the tree. It belongs to the 1.0 code base.
  - It would be semantic (it changes the parser/typing). Not relevant to 2.1.

#### `f37ce43` "Modifications to allow compilation in recent versions of MacOS" (portability)

- `scan-fct_pddl.y` / `scan-ops_pddl.y`:
  - Replace the commented-out `fcterr`/`opserr` prototype with prototypes
    using an unnamed `int`.
  - Add prototypes for `fct_pddllex(void)`, `fct_pddlerror(char *)`,
    `fct_pddlparse(void)` and the `ops_` equivalents.
  - Change `yyerror();` to `yyerror("");` (3 call sites;
    `src/metric-ff/scan-fct_pddl.y:221`, `scan-ops_pddl.y:371,386`).
  - Rename the definitions' parameter from `errno` to `errnum`.
- This addresses the implicit-declaration warnings our own build shows
  (`fct_pddllex`, `fct_pddlerror`, `fcterr`, `opserr`). Those become **hard
  errors** with GCC ≥ 14 and Clang ≥ 16 in C99+ modes.
- Calling `yyerror()` with no argument against the definition
  `int yyerror( char *msg )` (`src/metric-ff/scan-fct_pddl.y:896`) is
  undefined behaviour. It is harmless because `msg` is never read.
  `yyerror("")` changes no output: `yyerror` prints `gact_filename`,
  `lineno`, `yytext` and `serrmsg[sact_err]`, then `exit(1)`, so the exit code
  is unchanged.
- `search.h`: adds `void do_Astar_epsilon(void);`. That function is defined
  at `src/metric-ff/search.c:1250` but has no prototype. `main.c:979,1004`
  call it through an implicit `int` declaration (undefined behaviour, and an
  error on new compilers).
- Verdict: adopt the idea and write our own equivalent patch. All hunks are
  header or parser glue, with no change to search or output.

#### `c12256f` "Rollback to 1.0"

- Replaces the code base with Metric-FF 1.0.
- `makefile`: `-O6 -Wall -g -ansi`.
- Re-applies the f37ce43-style edits to the 1.0 `.y` files, with a slip: in
  `scan-ops_pddl.y` the prototype is `void opserr( int errno, char *par );`
  while the definition uses `int errnum`.
- With `errno` defined as a macro, those two declarations conflict. A
  self-written reproduction gives "conflicting types for 'opserr'" with both
  GCC and Clang. So this tree **probably does not compile** (not built).
- Wrong version for us: **avoid**.

### 1.3 ronuchit/FF

#### Base `3d9691d` "original planner that causes errors"

Compared with official `src/ff`, the differences fall into two groups.
Upstream file dates in our tarball are given in brackets.

*A. Older upstream FF 2.3, before Hoffmann's and rpg's 2015/2016 edits.*

`3d9691d` lacks the following:

- `ff.h`: `#include <string.h>` (`src/ff/ff.h:70`) and the
  `#endif /* __FF_H */` fix. The fork has `#endif __FF_H`, which is not
  valid C. [2016-10-04]
- `inst_final.h`: `#include <stdlib.h> /* for random functions [2016/09/28:rpg] */`
  (`src/ff/inst_final.h:67`). [2016-10-04]
- `lex-*.l`: `#define YY_NO_INPUT` and `%option nounput`
  (`src/ff/lex-fct_pddl.l:4,13`). Warnings only. [2016-10-04]
- `makefile`: rpg's `-ansi` → `-std=gnu99` change with OS switch
  (`src/ff/makefile:13-29`); the fork has `-O6 -Wall -g -ansi`. [2016-10-04]
- `search.c`/`main.c`: `fflush(stdout)` after progress lines
  (`src/ff/search.c:229,238,856,860`; `src/ff/main.c:706`).
  - This changes interleaving with stderr only, not stdout content. [2015-11-05]
- `inst_hard.c` (**instantiation**) [2016-04-07]:
  - The fork sizes the initial-state lookup table `lini` as
    `gnum_constants^arity`, and `instantiated_fact_adress` indexes it with raw
    constant numbers.
  - Official code (`src/ff/inst_hard.c:127`, `:753-754`) uses per-type sizes
    and `gmember_nr[...][type]`.
  - This is a memory and indexing change inside `inst_hard.c`. In principle it
    should not change results, but we already have the official version, so
    nothing to do.

*B. Edits by Siddharth Srivastava (README credit). All semantic, output format:*

- `main.c` / `output_planner_info`:
  - Calls `print_official_result()` *before* `exit(0)`. In the official tree
    the call comes *after* `exit(0)` and is dead code (`src/ff/main.c:768-770`).
  - The function writes `<fct-file>.soln`; the official function is at
    `src/ff/main.c:784-797`.
  - It also prints `*** States ***` and every plan state to stdout.
  - Its loop runs to `gnum_plan_ops+1`, so it reads one entry past the plan
    in `gplan_ops`.
- Usage text gains "Also prints states."
- `output.c` `print_plan`: the commented-out debugging block differs only
  inside comments (cosmetic).
- `README`: credit note.

Two independent derivatives call `print_official_result()` before `exit(0)`:
this fork, and mokhtarivahid's FF (1.4), which renames the output file to
`.ff`. That suggests that older FF 2.3 releases wrote a solution file and that
the 2015 tarball turned this off. This is an inference; it cannot be checked
from these sources.

#### `bfed732` "patch"

- README points to `jsk-ros-pkg/jsk_3rdparty/3rdparty/ff/ff.patch` as the
  source of the patch.
- After this commit the tree matches official `src/ff` (`diff -r`) **except**
  `README` and `scan-*.y`. Every hunk in ff.h, inst_final.h, inst_hard.c,
  lex-*.l, main.c, makefile, output.c and search.c is exactly the A/B
  difference above.
- Hunks touching `search.c` (flush only), `inst_hard.c` (indexing) and output
  (removal of the state printing) only *restore* the official code. So the
  commit is irrelevant to us.
- `scan-fct_pddl.y` / `scan-ops_pddl.y` (portability):
  - Comments out the real `fcterr`/`opserr` definitions.
  - Turns the prototype into an empty inline definition,
    `void fcterr( int errno, char *par ){};`, still with the `errno`
    parameter name.
  - Behaviour is the same, because the upstream bodies are empty.
  - Superseded by the parameter rename (1.2). **Do not adopt.**

#### `e5176df` "suppress a warning" (build)

Adds `-Wno-implicit` to `CFLAGS`. This hides the implicit-declaration
diagnostics (`fct_pddllex`, `fct_pddlerror`, `fcterr`, `opserr`) instead of
declaring the functions. **Avoid.**

### 1.4 mokhtarivahid/pddl-solvers (brief)

- A collection of planners with a Python runner (`run_planner.py`) and
  `build_all.sh`, which runs plain `make` in `planners/ff` and
  `planners/metric-ff`.
- There is no separate FF or Metric-FF patch script. The two `scripts/patch_*.sh`
  files are for VHPOP and NextFLAP.
- The FF sources were committed already modified in `7a028c4` (2026-02-23),
  together with generated `lex.*.c` and `*.tab.c`.
- `planners/ff` is an FF 2.3 variant. Compared with `src/ff`:
  - **`MAX_*` limits raised**, marked "MS: increased from …":
    `MAX_CONSTANTS` 2500, `MAX_PREDICATES` 20000, `MAX_TYPE` 2500,
    `MAX_OPERATORS` 350000. Upstream values are at `src/ff/ff.h:211-221`.
  - **Bison grammar** in `scan-*.y` changed from right recursion to left
    recursion (domain defs, predicates, requirements, problem defs). This
    changes the order in which semantic actions run, so possibly the order of
    operators and facts. Semantic.
  - `fcterr`/`opserr` calls removed.
  - `extern` added to `gbracket_count` (`main.c`) and `lcurrent_goals`
    (`search.c`).
  - `print_official_result()` moved before `exit(0)`, writing
    `<path><fct>.ff`.
  - Older `makefile` (`-O6 -ansi`) and lexers.
- `planners/metric-ff` is **Metric-FF 1.0** (it matches Vidminas `577aa9e`,
  plus a `.svn` directory). The only edits are the `extern` lines for
  `gbracket_count` (`main.c`) and `lF`/`lnum_F` (`relax.c`).
- Licence: no top-level licence. The README (line ~881) says each planner keeps
  its own licence. Upstream GPL headers are kept in the files.
- Reference only. Nothing to adopt beyond the `extern` idea, which is already
  covered above.

---

## 2. FF 2.3 vs Metric-FF 2.1: file-level comparison and shared portability hotspots

### 2.1 File inventory and similarity

- Only in FF: `orderings.c`, `orderings.h`, `README`.
- Only in Metric-FF: `expressions.c`, `expressions.h`.
- How the table was computed: "diff lines" counts the added plus removed lines
  of `diff -U0`. "ratio" is `difflib.SequenceMatcher` on lines, where 1.0
  means the files are identical.

| File | FF lines | MFF lines | diff lines | ratio |
|---|---:|---:|---:|---:|
| `ff.h` | 1478 | 2044 | 760 | 0.79 |
| `inst_easy.c` | 1354 | 1220 | 326 | 0.87 |
| `inst_easy.h` | 103 | 73 | 30 | 0.83 |
| `inst_final.c` | 1512 | 2797 | 1873 | 0.58 |
| `inst_final.h` | 88 | 69 | 43 | 0.73 |
| `inst_hard.c` | 992 | 1306 | 550 | 0.76 |
| `inst_hard.h` | 97 | 71 | 34 | 0.80 |
| `inst_pre.c` | 2725 | 3854 | 1507 | 0.77 |
| `inst_pre.h` | 144 | 123 | 37 | 0.86 |
| `lex-fct_pddl.l` | 125 | 161 | 52 | 0.82 |
| `lex-ops_pddl.l` | 124 | 171 | 67 | 0.77 |
| `main.c` | 935 | 1230 | 747 | 0.68 |
| `makefile` | 107 | 89 | 22 | 0.89 |
| `memory.c` | 1007 | 1278 | 417 | 0.83 |
| `memory.h` | 121 | 109 | 40 | 0.83 |
| `output.c` | 780 | 1482 | 810 | 0.65 |
| `output.h` | 87 | 68 | 35 | 0.77 |
| `parse.c` | 1245 | 1339 | 146 | 0.94 |
| `parse.h` | 88 | 63 | 25 | 0.83 |
| `relax.c` | 980 | 2756 | 2450 | 0.36 |
| `relax.h` | 104 | 93 | 71 | 0.64 |
| `scan-fct_pddl.y` | 654 | 939 | 309 | 0.81 |
| `scan-ops_pddl.y` | 807 | 1060 | 285 | 0.85 |
| `search.c` | 1225 | 2372 | 1797 | 0.53 |
| `search.h` | 120 | 105 | 77 | 0.66 |

- The parser, lexers, memory, `parse.c` and `inst_easy/pre` are close
  relatives, so portability fixes there can be shared in spirit.
- `relax.c`, `search.c`, `inst_final.c` and `output.c` diverge strongly.
- Each tree still needs its own patch, because the line numbers differ.

### 2.2 Link errors under `-fno-common` (GCC ≥ 10 and Clang ≥ 11 default)

Verified by building the pristine trees with GCC 11.4. **Neither upstream tree
links with default flags.** `nm` over all objects, built with `-fcommon`, lists
every multiply-defined data symbol:

| Planner | Symbol | Definitions | Notes |
|---|---|---|---|
| FF | `gbracket_count` | `src/ff/main.c:147` (tentative), `src/ff/lex-fct_pddl.l:9` (`= 0`) | same type; `extern` in `main.c` is exact (`ff.h:1187` already declares it `extern`) |
| FF | `lcurrent_goals` (`State`) | `src/ff/relax.c:111`, `src/ff/search.c:110` | same type; `extern` in `search.c` keeps the merged-object semantics exactly. Under `-fcommon`, `get_1P` called with `&ggoal_state` (`search.c:898`) also overwrites search's copy; `extern` keeps that. |
| Metric-FF | `gbracket_count` | `src/metric-ff/main.c:124`, `src/metric-ff/lex-fct_pddl.l:30` | as in FF (`ff.h:1595`) |
| Metric-FF | `lF` | `src/metric-ff/expressions.c:460` **`int lF[25]`**, `src/metric-ff/relax.c:72` **`int *lF`** | **type mismatch**: two unrelated variables that `-fcommon` merged by accident. Use `static` in both files (disjoint lifetimes, see 1.1) |
| Metric-FF | `lnum_F` | `src/metric-ff/expressions.c:462`, `src/metric-ff/relax.c:73` | same reasoning: `static` in both |

**No header defines a non-`extern` global.** All the collisions come from
`.c` files and from the `.l` files that are `#include`d into `scan-*.tab.c`
(`src/ff/scan-fct_pddl.y:582`, `src/metric-ff/scan-fct_pddl.y:867`). The
`gbracket_count` defined in `lex-fct_pddl.l` ends up in `scan-fct_pddl.tab.o`.

Adding `-fcommon` would also work around all of this on GCC and Clang. MSVC
has no equivalent, and it hides the `lF` type mismatch, so source fixes are
preferable.

### 2.3 Time functions

- `<sys/times.h>` and `<sys/timeb.h>`: `src/ff/ff.h:73-74`,
  `src/metric-ff/ff.h:51-52`. `sys/times.h` does not exist on Windows (MSVC or
  MinGW). `sys/timeb.h` exists there, with `_ftime`/`ftime`.
- `times()` calls: `src/ff/main.c:504,542,627,630,637,640,647,650,656,665,710,791`;
  `src/metric-ff/main.c:662,713,796,799,806,809,816,823,828,831,844,943,1012`.
- `TIME()` macro hard-codes 100 ticks/s: `src/ff/ff.h:314-315`,
  `src/metric-ff/ff.h:312-313`. That is correct where
  `sysconf(_SC_CLK_TCK)` = 100, the usual value on Linux and macOS. Elsewhere
  only time lines are affected.
- FF's (dead) `print_official_result` uses `* 10.0` (`src/ff/main.c:792-793`).
- `ftime()`: FF only, `src/ff/inst_final.c:1121-1124` (`struct timeb tp;
  ftime(&tp); srandom(tp.millitm);`). Deprecated in glibc ≥ 2.33 (warning
  seen in our build).

### 2.4 Random numbers

| Site | Code | Role |
|---|---|---|
| `src/ff/inst_final.c:1124` | `srandom( tp.millitm )` | FF seeds from the clock's milliseconds (0–999), so it differs from run to run |
| `src/ff/inst_final.c:1141` | `gft_conn[i].rand = random() % BIG_INT` | fact hash values; used in `state_sum` `src/ff/search.c:562`, then `& EHC/PLAN/BFS_HASH_BITS` (`search.c:446,508,678,721,989,1018`) |
| `src/metric-ff/inst_final.c:1950,1962` | `random() % BIG_INT` (facts, fluents) | hash values (`src/metric-ff/search.c:1829,1839,1855`); unseeded, so the glibc default seed applies |
| `src/metric-ff/search.c:1371` | `coin = random() % 2` | A*-epsilon tie-break; **decides plans** with `-s 4` and with `-s 5` after EHC fails |

Other notes on randomness:

- Metric-FF never calls `srandom`. Its usage text advertises
  `-r <int> Random seed` (`src/metric-ff/main.c:1087`), but
  `process_command_line` has no `case 'r'` (`src/metric-ff/main.c:1146-1200`).
  So `-r` is rejected with the usage message. This is an upstream quirk and
  is frozen.
- `random()` returns `long`, assigned to `int`. This is the only
  `long → int` narrowing reported by `-Wconversion` (4 sites). It is safe
  because the values are `< BIG_INT` = 1 500 000 or `< 2`.
- Undefined behaviour to keep in mind for rule 4:
  - `state_sum` adds up to `num_F` values `< 1.5e6` in a signed `int`
    (`src/ff/search.c:562`, `src/metric-ff/search.c:1829`). It overflows once
    a state has more than about 1431 true facts.
  - `gfl_conn[i].rand * (int) S->f_V[i]` (`src/metric-ff/search.c:1839`)
    can overflow, and the float-to-int conversion is undefined for large
    values.
  - Today's results rely on two's-complement wrap. Do not "fix" this without
    golden evidence; consider `-fwrapv` as a guard.

### 2.5 Lexer / parser portability

- Generated lexers `#include <unistd.h>` and call `isatty(fileno(file))`.
  Flex 2.6.4 output, seen in our generated `lex.fct_pddl.c:865,1960`.
  - MSVC needs `flex --nounistd` (or `--wincompat`) plus `<io.h>`.
  - Under `-ansi`, `fileno` is implicitly declared on glibc (our `-ansi`
    build: `lex.fct_pddl.c:1960`).
- `yywrap` is defined as K&R `int fct_pddlwrap() { return 1; }`
  (`src/ff/lex-fct_pddl.l:7`, `src/metric-ff/lex-fct_pddl.l:26`;
  `ops_` likewise). It gives the warning "prototype follows non-prototype".
  Under C23 (GCC 15 defaults to gnu23) `()` means `(void)`, which is still
  compatible.
- Implicit declarations (errors on GCC ≥ 14 and Clang ≥ 16):
  - `fct_pddllex`, `fct_pddlerror`, `ops_*`: generated `*.tab.c:69-70`.
  - `fcterr`: `src/ff/scan-fct_pddl.y:156`, `src/metric-ff/scan-fct_pddl.y:193`.
  - `opserr`: `src/ff/scan-ops_pddl.y:164`, `src/metric-ff/scan-ops_pddl.y:205`.
  - `do_Astar_epsilon`: `src/metric-ff/main.c:979`.
  - Under `-ansi`, also `random`: `src/metric-ff/inst_final.c:1950`,
    `search.c:1371`.
- `errno` as a parameter name: `src/ff/scan-fct_pddl.y:593`,
  `src/ff/scan-ops_pddl.y:744`, `src/metric-ff/scan-fct_pddl.y:878`,
  `src/metric-ff/scan-ops_pddl.y:997` (see 1.1 `7ee379c`).
- `yyerror()` is called with no argument but defined as `int yyerror(char*)`:
  - FF: `src/ff/scan-fct_pddl.y:184` (definition `:611`),
    `src/ff/scan-ops_pddl.y:262,277` (definition `:764`).
  - Metric-FF: `src/metric-ff/scan-fct_pddl.y:221` (definition `:896`),
    `scan-ops_pddl.y:371,386` (definition `:1017`).
- CRLF input: the catch-all rule `. {}` (`src/ff/lex-ops_pddl.l:123`,
  `src/ff/lex-fct_pddl.l:124`, `src/metric-ff/lex-ops_pddl.l:170`,
  `src/metric-ff/lex-fct_pddl.l:160`) silently skips `\r`. Comment rules
  `\;(.)*\n` also match through `\r`. So CRLF PDDL files parse the same on
  POSIX (binary) and Windows (text-mode `fopen(…, "r")`). One course example
  is CRLF: `examples/logistics/log-3-2.pddl`.

### 2.6 `-ansi` and compiler modes

- `src/metric-ff/makefile:12`: `-O6 -ansi`.
  - On glibc, `-ansi` hides `random()` and `fileno()`, which are then
    implicitly declared as `int`. `random()` returns `long`, so the call is
    undefined behaviour on LP64, though it works on x86-64.
  - On macOS `-ansi` does not hide them (rpg's comment, `src/ff/makefile:13-15`).
  - Apple clang rejects `-O6` (`src/ff/makefile:28`).
- `src/ff/makefile:16`: `-std=gnu99`, and it refuses to build on Windows
  (`src/ff/makefile:21`).
- `src/ff/makefile:40` lists a non-existent `scan-probname.tab.c` in
  `PDDL_PARSER_SRC`; Metric-FF does the same at `src/metric-ff/makefile:22`.
  It is used only by `clean` and harmless.

### 2.7 Other non-portable spots

- **`<strings.h>`**: `src/ff/ff.h:69` (FF only). MSVC does not have it, and
  no BSD string function (`bzero`, `strcasecmp`, `index`, …) is used, so it
  can be removed or guarded.
- **`long`/LLP64 (Win64)**:
  - No `long`, `%ld` or pointer↔int cast in either code base (grep, plus
    `-Wpointer-to-int-cast -Wint-to-pointer-cast` warning-free).
  - The only narrowing is `size_t → int` from `strlen` (41 sites in FF,
    54 in Metric-FF, `-Wconversion`). It is harmless at these sizes.
- **`char` signedness**:
  - `strupcase` calls `toupper((int) tmp)` on a plain `char`
    (`src/ff/parse.c:128`, `src/metric-ff/parse.c:104`). It is undefined for
    negative values, and MSVC debug CRT asserts.
  - Callers pass only `yytext` from rules limited to `[a-zA-Z0-9\-_\[\]]`,
    so in practice the input is ASCII.
  - `char option` in `process_command_line` (`src/ff/main.c:889`,
    `src/metric-ff/main.c:1146`) is only compared with ASCII letters.
- **Fixed 256-byte path buffers** (`MAX_LENGTH`, `src/ff/ff.h:155`):
  - `strncpy(…, *argv, MAX_LENGTH)` can leave the buffer without a
    terminating NUL (`src/ff/main.c:908-914`, `src/metric-ff/main.c:1168-1174`).
  - `sprintf(ops_file, "%s%s", path, name)` into 256 bytes
    (`src/ff/main.c:533-534`, `src/metric-ff/main.c:704-705`; GCC
    `-Wformat-overflow`) can overflow.
  - Long Windows paths (pip temp dirs) can reach this. A wrapper that
    `chdir`s and passes short relative names avoids touching the C code.
- **`sprintf("%s%s%4d", …)`**: `src/ff/memory.c:233` writes into a buffer
  sized for 4 digits. This is safe because `count < 10000` is enforced at
  `memory.c:228`.
- **`ENCODE_VAR` / `DECODE_VAR`** are not parenthesised (`src/ff/ff.h:300`;
  `-Wint-in-bool-context`). Do not touch.
- **Floating point (Metric-FF)**:
  - Costs and fluents are `float`, for example
    `e->cost += glnf_metric.pC[k] * e->lnf_effects_rh[j]->c`
    (`src/metric-ff/expressions.c:2357`).
  - GCC in GNU modes and Clang (≥ 14) may fuse such expressions into FMA on
    targets that have FMA (arm64 macOS and Linux, x86-64 with `-march`
    supporting FMA). The results then differ from x86-64 baseline builds.
  - Pin `-ffp-contract=off` (MSVC: `/fp:precise`, no `/fp:contract`). Avoid
    32-bit x87 builds and never use `-ffast-math`.
- **Windows stdout text mode**: `printf("\n")` produces CRLF on Windows.
  Either normalise line endings in the golden comparison (and document it),
  or set stdout to binary mode in a `main()` wrapper.
- **Uninitialised-use warnings** (Metric-FF, `-Wmaybe-uninitialized`):
  `relax.c:2229` (`min_ownlevel`), `search.c:998` (`goal_distance`). These may
  be potential undefined behaviour, so investigate under rule 4 before any
  change.
- **Exit codes**:
  - Both planners `exit(0)` after search whether or not a plan is found
    (`src/ff/main.c:720`, `src/metric-ff/main.c:1020`).
  - Errors give `exit(1)` (≈ 300 sites), including `yyerror`.
  - None of the fork hunks reviewed changes exit codes. ronuchit `3d9691d`
    adds an extra `.soln` file write before the existing `exit(0)`.

---

## 3. Implications for this project

### Portability fixes we will need (both planners unless noted)

- **Globals for `-fno-common`:**
  - `extern` for `gbracket_count` in `main.c` (FF `main.c:147`, MFF
    `main.c:124`).
  - FF: `extern` for `lcurrent_goals` in `search.c:110`; same type, keeps
    the merged-object behaviour.
  - Metric-FF: make `lF`/`lnum_F` `static` in `expressions.c:460-462` *and*
    `relax.c:72-73`, not `extern` (type mismatch).
  - Document all of these in `PATCHES.md` with the golden evidence.
- **Time shim** in `src/compat/`:
  - `struct tms` and `times()` for Windows, giving CPU time in 1/100 s so
    that `TIME()` stays right.
  - FF only: an `ftime` replacement (or `_ftime`) for the seed call at
    `src/ff/inst_final.c:1121-1124`.
  - Keep `<sys/timeb.h>`/`<sys/times.h>` behind `#ifndef _WIN32`. Do not
    redefine `struct timeval` on MinGW (the lesson of Vidminas `8c73f65`).
- **Random numbers:** route every `random()`/`srandom()` call
  (`src/ff/inst_final.c:1124,1141`; `src/metric-ff/inst_final.c:1950,1962`;
  `src/metric-ff/search.c:1371`) to the glibc-compatible generator in
  `src/compat/`, unseeded for Metric-FF. FF's clock-ms seed is a separate
  maintainer decision (rule 10): output may not depend on it, but this has to
  be shown.
- **Prototypes and declarations** (needed for GCC ≥ 14 / Clang ≥ 16):
  - `fct_pddllex`, `fct_pddlerror`, `ops_pddllex`, `ops_pddlerror`.
  - `fcterr`/`opserr`, with the parameter renamed from `errno`.
  - `do_Astar_epsilon` in `src/metric-ff/search.h`.
  - Optionally `yyerror("")` at the no-argument call sites; output is
    unchanged because `msg` is unused.
  - Pin an explicit `-std=gnu99` (or `gnu89`) in both builds, so that
    `random`/`fileno` are declared and C23 defaults do not apply.
- **Headers:** guard or remove `<strings.h>` (`src/ff/ff.h:69`). Generate
  lexers with `--nounistd` (or provide `isatty`/`fileno` via `<io.h>`) on
  MSVC.
- **Build flags:**
  - `-ffp-contract=off` everywhere (Metric-FF float costs); no
    `-ffast-math`; 64-bit SSE/NEON targets only.
  - `-O3`, not `-O6` (same code on GCC; required by Apple clang).
  - Consider `-fwrapv` to make today's signed-overflow wrap in `state_sum`
    explicit.
- **Wrapper level (not C changes):** decide how Windows CRLF stdout is
  handled, and avoid paths longer than 255 bytes, for example by `chdir` plus
  relative names.

### What NOT to adopt from the forks

- Vidminas `c517363` (`random()` → `rand()`): **semantic**. A no-op on glibc,
  but a different sequence on macOS, and `RAND_MAX` = 32767 on Windows.
- Vidminas `5673be8` (reformat everything): whitespace-only, as verified, but
  it destroys traceability.
- Vidminas `212b887` `extern int *lF` against `int lF[25]`: works only by the
  same accident as `-fcommon`. Use `static` instead.
- Vidminas `times.c` as written: no `_WIN32` guard, and `clock()` wall time in
  1/1000 s fed to a `/100.0` macro.
- tranchis `c12256f` (Metric-FF 1.0, `parse.c.patch`, `llparse.c`): wrong
  version, parser semantics change, probably does not compile. Do not copy any
  tranchis code (licence inconsistency); reimplement the `f37ce43` ideas
  independently.
- ronuchit `3d9691d` (state printing, `.soln` writing, off-by-one): output
  format change. `bfed732`'s empty inline `fcterr`/`opserr` stubs and
  `e5176df`'s `-Wno-implicit`: they hide problems instead of fixing them. No
  licence: reference only.
- mokhtarivahid FF: `MAX_*` increases (rule 5), left-recursive grammar
  (possible change in operator and fact order), `.ff` solution-file output.
  Its Metric-FF is version 1.0.
- `-Wno-implicit` and `-fcommon` as substitutes for source fixes, where we
  target MSVC.
