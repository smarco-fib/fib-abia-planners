# Sanitizers and compiler diagnostics (Phase 1)

Host: Ubuntu 22.04, x86-64, kernel 6.8, glibc 2.35. Compilers: GCC 12.3, Clang 14.0.
All runs on 2 cores / 4 threads (`taskset -c 0,1,4,5`, `-j 4`).

## 1. AddressSanitizer + UndefinedBehaviorSanitizer over the corpus

Build and run:

```sh
CC=clang-14 cmake -S . -B build/cmake-asan-clang -DCMAKE_BUILD_TYPE=RelWithDebInfo -DABIA_SANITIZE=ON
cmake --build build/cmake-asan-clang -j 4
python3 -m harness.studies.sanitize --no-aslr --ff build/cmake-asan-clang/ff \
    --metric-ff build/cmake-asan-clang/metric-ff -j 4 --json out.json \
    examples/manifest.json corpus/synthetic.json corpus/ipc.json
```

`ASAN_OPTIONS=detect_leaks=0` (the planners never free their memory before
exiting; leaks are by design), `UBSAN_OPTIONS=halt_on_error=0`; case timeouts ×3.

### Results

| Pass | Sources | Runs | Runs with findings | Distinct findings | Outcome differs from golden |
|---|---|---|---|---|---|
| 1 | after P-BUILD-1 | 1281 | 69 | 2 (both `metric-ff/search.c:1839`) | 0 |
| 2 | after UB-4 | 1281 | **0** | **0** | 0 |

Findings of pass 1:

| Tool | Location | Finding | Runs | Fixed by |
|---|---|---|---|---|
| UBSan | `src/metric-ff/search.c:1839` (`state_sum`) | signed integer overflow: `N + N` | 69 | UB-4 |
| UBSan | `src/metric-ff/search.c:1839` (`state_sum`) | signed integer overflow: `N * N` | 38 (subset of the 69) | UB-4 |

AddressSanitizer reported nothing: no out-of-bounds access, use-after-free or
stack overflow on any of the 1281 runs. (UB-1, the use-after-free in the
Metric-FF parser, and UB-2, a NULL dereference, were found and fixed in Phase 0;
UB-3, the path-length overflow, by a compiler warning and a targeted test.)

### Tool artefact: random SIGSEGV of ASan on this kernel

An initial run without `--no-aslr` reported 307 crashes (SIGSEGV, exit −11, no ASan
report, after about 0.1 s). They are not planner bugs: the ASan runtime of
LLVM < 18 can crash at start-up on Linux kernels with high mmap randomisation
(`vm.mmap_rnd_bits = 32`, default on recent Ubuntu kernels). Evidence: `hanoi-4`
with the sanitized FF crashed 13 times out of 40 normally and 0 out of 40 under
`setarch -R` (address-space randomisation disabled for that process); of the 307
crashed runs, 234 did not crash when simply repeated (73 crashed again, at
random); under `setarch -R` none crashed (passes 1 and 2 in the table above). `harness.studies.sanitize --no-aslr`
runs every planner under `setarch -R`. CI should use a recent Clang (≥ 18) or
the same option.

## 2. Compiler diagnostics

`-Wall -Wextra`, CMake Release build. Before Phase 1 the sources did not build
with GCC ≥ 10 or Clang ≥ 11 (multiple definitions without `-fcommon`; Clang:
conflicting types for `fcterr`/`opserr`), and had 63 implicit function
declarations (errors in GCC ≥ 14 and Clang ≥ 16). After Phase 1: both compilers
build; 0 implicit declarations.

Remaining warnings (GCC 12: 46, Clang 14: 35) and their triage:

| Warning | Where | Verdict |
|---|---|---|
| `-Wunused-parameter`, `-Wunused-variable`, `-Wunused-but-set-variable`, `-Wunused-function`, `-Wunneeded-internal-declaration` | various; flex output | harmless |
| `-Wcomment` (`/*` within comment) | FF `relax.c` | harmless |
| `-Waddress` / `-Wpointer-bool-conversion`: `!gcmd_line.ops_file_name` is always false | `main.c` (both) | **upstream logic bug, not fixed** (rule 1): the "two input files needed" check never fires; a missing `-o`/`-f` ends in "can't find … file" instead. Harmless. |
| `-Wint-in-bool-context` in `DECODE_VAR` | `inst_easy.c` (FF 1084, Metric-FF 917) | **upstream logic bug, not fixed** (rule 1): `DECODE_VAR( args[j] < lo->num_vars )` misplaces a parenthesis; the condition reduces to `args[j] < 0`. Fixing it would change instantiation, so it is reported to the maintainer instead. |
| `-Wformat-overflow` on `sprintf(ops_file, "%s%s", path, file)` | `main.c` (both) | real, fixed by UB-3 (length check before the `sprintf`; the compiler cannot see it) |
| `-Wformat-overflow` on `"%s.soln"` | FF `main.c` | unreachable code (`print_official_result()` is called after `exit(0)`) |
| `-Wformat-overflow` on `"%4d"` into 5 bytes | `memory.c` (both) | false positive: the counter is < 10000 (the program exits at 10000) |
| `prototype for 'fct_pddlwrap' follows non-prototype definition` | flex output | harmless |

## 3. Floating point and other build choices

`-ffp-contract=off` on every target, no `-ffast-math`, no `-march=native`.
x86-64 uses SSE2 for `float`, so there is no excess precision either.
`-fwrapv` was considered for the hash sums and not needed: UB-4 removes the
overflow in the source.
