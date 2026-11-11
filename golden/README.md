# Golden reference

Normalised outputs of the upstream sources **plus the two approved UB fixes**
(`src/ff` pristine; `src/metric-ff` pristine + UB-1 `43003cf` + UB-2 `5c01bf3`,
see `PATCHES.md`), built with their own makefiles:

| Item | Value |
|---|---|
| Host | Ubuntu 22.04.5 LTS, x86-64, glibc 2.35 (no container runtime available; native host) |
| Compiler | `gcc-9` (Ubuntu 9.5), default `-fcommon`, so the sources link unchanged |
| Flags | upstream makefiles: FF `-Wall -g -std=gnu99 -O6`; Metric-FF `-O6 -ansi -g` |
| Parser generators | flex 2.6.4, bison 3.8.2 (makefile runs them) |
| Command | `tools/build-reference.sh` (copies each tree to `build/reference/src`, runs `make CC=gcc-9`) |

`python3 -m harness record --ff <ff> --metric-ff <metric-ff> <manifest>` writes
`golden/<suite>/<case>/<config>.json`.

Suites: `examples` (course examples, `examples/manifest.json`), `synthetic`
(`corpus/synthetic.json`), `ipc` (`corpus/ipc.json`).

Recording runs used 2 cores / 4 threads (`taskset -c 0,1,4,5`, `-j 4`).
Wall time and peak RSS per run: `timings-<suite>.json` (informational, never
compared). A run whose golden outcome is `timeout` is compared on `outcome`
only: its partial stdout is recorded for information but depends on machine
speed. Only `synthetic/unsolvable/exhaustive-wastar/mff-s3` is in this class.

**History:** the first golden (commit `acadca4`) was recorded from the
pristine sources. Pristine Metric-FF has undefined behaviour in the parser for
problems with a `:metric` (UB-1) and for some initial states (UB-2); 280 runs
crashed or misparsed. After the maintainer approved the fixes the golden was
re-recorded: 142 files changed, 138 runs that now time out were removed from the
corpus, all other files are unchanged.
