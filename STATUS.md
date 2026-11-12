# Platform status

Legend: ✅ CI evidence (link) · ❌ fails (link) · ⏳ not yet run · unvalidated

| Platform | Built | Course examples | Valid on full corpus (rule 3) | Plans validated | Clean install | Real-hardware pilot | Notes |
|---|---|---|---|---|---|---|---|
| Linux x86-64 (glibc) | local only | local only | local only | ⏳ | ⏳ | unvalidated | Phase 1 (2026-11-12, local, no CI): CMake build with GCC 12 and Clang 14 byte-identical to golden on the full corpus (1281 runs); ASan+UBSan 0 findings; examples deterministic over 5 runs each. Reference platform for the regression check (rule 3). |
| Linux x86-64 (musl) | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | unvalidated | |
| Linux aarch64 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | unvalidated | |
| macOS x86-64 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | unvalidated | |
| macOS arm64 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | unvalidated | |
| Windows x64 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | unvalidated | |
| Windows arm64 | — | — | — | — | — | out of scope | excluded by the maintainer (Checkpoint 1) |

Phase 0 (2026-11-10): no CI yet; no platform is supported.

Phase 1 (2026-11-12): portable build on Linux x86-64 done locally (see
PATCHES.md P-*/UB-3/UB-4 and reports/sanitizers.md). Determinism: every course
example run 5 times with the CMake GCC 12 build gave identical output; one
apparent variation (binpacking v2op prob2, ~50 s) was a timeout caused by
running 4 copies in parallel on 4 threads and disappeared when run alone.
