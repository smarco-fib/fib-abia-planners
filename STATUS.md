# Platform status

Legend: ✅ CI evidence (link) · ❌ fails (link) · ⏳ not yet run · unvalidated

| Platform | Built | Course examples | Valid on full corpus (rule 3) | Plans validated | Clean install | Real-hardware pilot | Notes |
|---|---|---|---|---|---|---|---|
| Linux x86-64 (glibc) | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) 267/267 | local only | ⏳ | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) | unvalidated | Phase 1 (2026-11-12, local, no CI): CMake build with GCC 12 and Clang 14 byte-identical to golden on the full corpus (1281 runs); ASan+UBSan 0 findings; examples deterministic over 5 runs each. Reference platform for the regression check (rule 3). |
| Linux x86-64 (musl) | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) 267/267 | ⏳ | ⏳ | ⏳ | unvalidated | static binaries |
| Linux aarch64 | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) 267/267 | ⏳ | ⏳ | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) | unvalidated | glibc; the musl wheel also passes 267/267, without clean-install test |
| macOS x86-64 | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) 267/267 | ⏳ | ⏳ | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) | unvalidated | runner macos-15-intel; deployment target 11.0; links only libSystem |
| macOS arm64 | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) 267/267 | ⏳ | ⏳ | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) | unvalidated | runner macos-15; deployment target 11.0; links only libSystem |
| Windows x64 | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) 267/267 | ⏳ | ⏳ | [✅](https://github.com/smarco-fib/fib-abia-planners/actions/runs/43210321175) | unvalidated | MinGW-w64 GCC, static: imports only KERNEL32 and the Universal CRT (part of Windows 10+), no MinGW DLLs |
| Windows arm64 | — | — | — | — | — | out of scope | excluded by the maintainer (Checkpoint 1) |

Phase 0 (2026-11-10): no CI yet; no platform is supported.

Phase 1 (2026-11-12): portable build on Linux x86-64 done locally (see
PATCHES.md P-*/UB-3/UB-4 and reports/sanitizers.md). Determinism: every course
example run 5 times with the CMake GCC 12 build gave identical output; one
apparent variation (binpacking v2op prob2, ~50 s) was a timeout caused by
running 4 copies in parallel on 4 threads and disappeared when run alone.

First CI run (2026-11-12, run 43210321175): wheels built natively on all five
runners; each ran `fib-abia-planners selftest --all` (267 example runs) with
outcome and exit code matching the golden and every plan identical to the
Linux reference. Clean install (fresh venv, Python 3.9 and 3.13, examples
copied to a path with a space and "ñ") passed everywhere. Still missing for
"supported" (rule 7): the full corpus and VAL plan validation on each
platform (final validation phase).
