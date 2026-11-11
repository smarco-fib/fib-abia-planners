# Randomness study (Phase 0)

Question: how much do FF 2.3 and Metric-FF 2.1 depend on the `random()`
sequence of the C library? The answer decides how the portable `random()` in
`src/compat/` must behave (rule 10) and how FF's clock-based seed is treated.

## 1. Where `random()` is used

| Planner | Site | Use |
|---|---|---|
| FF 2.3 | `src/ff/inst_final.c:1123-1124` | `ftime(&tp); srandom(tp.millitm);` → seed is 0…999, varies run to run |
| FF 2.3 | `src/ff/inst_final.c:1141` | `gft_conn[i].rand = random() % BIG_INT;` one value per fact |
| FF 2.3 | `src/ff/search.c:562` | `state_sum` adds the fact values → hash key of a state |
| Metric-FF 2.1 | — | **never seeded**: glibc default sequence (= `srandom(1)`) |
| Metric-FF 2.1 | `src/metric-ff/inst_final.c:1950,1962` | one value per fact and per fluent |
| Metric-FF 2.1 | `src/metric-ff/search.c:1822-1846` | `state_sum` = Σ fact values + Σ fluent value × `(int)` fluent; `logical_state_sum` = facts only |
| Metric-FF 2.1 | `src/metric-ff/search.c:1371` | `coin = random() % 2;` tie-break between equal `goal_distance` in A*-epsilon (`-s 4`; `-s 5` when EHC fails) |

The hash values are **not only** a lookup key. The dominance tests
`superior_ehc_state_hashed` (`search.c:525-549`, EHC) and the analogous BFS
function (`search.c:1798-1816`) compare a new state only with states in the
**same bucket** (`sum & *_HASH_BITS`) whose `sum` is not smaller. Which states
are pruned as dominated therefore depends on the random values, and with it the
number of evaluated states and, potentially, the plan.

Metric-FF's usage text advertises `-r <int> Random seed` (`main.c:1087`), but
the option parser rejects `-r` ("unknown option"); there is no way to seed it.

`state_sum` accumulates in `int`; overflow there is signed-integer UB
(see the fork analysis in `reports/upstream-diffs.md`, suggestion `-fwrapv`).

## 2. Method

`harness/studies/random_shim.c` (LD_PRELOAD, Linux/glibc only):

- `FORCE_SEED=s`: calls `srandom(s)` at start-up and replaces any later
  `srandom()` argument with `s` (forces FF's clock seed).
- `RAND15=1`: masks every value to 15 bits (models a `rand()` with
  `RAND_MAX = 32767`, as on Windows).
- `LOG_RANDOM=1`: prints the number of `random()` calls.

`python3 -m harness.studies.randomness` runs each selected run under every
variant and compares the normalised outputs (exit code, outcome, plan, stdout,
stderr; time numbers masked). Variants:

- FF: `FORCE_SEED` = 0 … 999, i.e. **every** seed `ftime().millitm` can produce.
- Metric-FF: unseeded, `FORCE_SEED` ∈ {0, 2, 3, 42, 12345}, `RAND15`.
  (glibc treats `srandom(0)` as `srandom(1)`, so unseeded ≡ seed 0: a built-in
  consistency check.)

Binaries: `tools/build-reference.sh` (gcc-9, upstream makefiles). Metric-FF
was run with the two proposed UB fixes (`build/ubfix`, see `PATCHES.md`),
because pristine Metric-FF crashes or misparses most `:metric` problems
(UB-1), which would hide any effect of randomness. Both fixes are in the
parser; neither touches `random()` or search.

Host: Ubuntu 22.04, x86-64, glibc 2.35. All runs pinned to 2 cores / 4 threads
(`taskset -c 0,1,4,5`, `-j 4`) except run 1 (below).

## 3. FF 2.3

All 240 FF runs of the three suites (examples 34, synthetic 29, IPC 177), each
under **all 1000 seeds** FF can draw (0–999), pristine build. 240 000
executions, 2026-11-11, 1 h 44 min on 2 cores / 4 threads.

Outcomes of the 240 runs: 213 plan-found, 24 parse-error, 2 proven-unsolvable,
1 usage-error (longest run 14.6 s; no timeouts).

**Result: 240/240 runs produce byte-identical normalised output for all 1000
seeds** (plan, statistics, exit code). Data: `reports/data/randomness-ff.json` (per run: distinct outputs, variants).

Why, from the code: FF uses the random values only as hash keys of states
(`state_sum`, `src/ff/search.c:555-566`). Every lookup in a bucket
(`search.c:516, 682, 725, 1025`) tests exact equality with `same_state`, so the
values change which bucket is searched, never the answer. There is no
tie-breaking coin and no dominance test as in Metric-FF. The measurement and the
code agree: FF's output does not depend on the seed.

## 4. Metric-FF 2.1

### Run 1 — screening

All Metric-FF runs whose id contains `numeric/` (synthetic numeric cases and
IPC-2002 numeric domains): 943 runs × 7 variants, `-j 8` on 8 threads.
Result: 871 identical, 72 varying. By configuration:

| Config | varying / runs |
|---|---|
| `mff-s4` (A*-epsilon) | 56 / 118 |
| `mff-s0` | 9 / 347 |
| `mff` (default `-s 5`) | 4 / 348 |
| `mff-s3` | 2 / 103 |
| `mff-s4-b8` | 1 / 1 |
| all others (`-s 1`, `-s 2`, `-w 1`, `-C`, `-b`, …) | 0 |

The raw per-run output of run 1 was lost with a scratch directory; only this
summary survived. It is used solely to select the runs for run 2.

### Run 2 — detail (reproducible)

The 72 varying runs (80 ids, 8 neighbours added because two ids of the list
were lost), 7 variants each, 2 cores / 4 threads. Data:
`reports/data/randomness-metric-ff.json` (per run: groups of variants with
identical output; per variant: outcome, plan length, timed out, wall time) and
`reports/data/randomness-metric-ff-ids.txt` (the run ids).

| Config | identical | all variants time out (partial output differs) | timeout in some variants only | plan differs (length) | plan differs, same length | same outcome, only search statistics differ |
|---|---|---|---|---|---|---|
| `mff-s4` | 0 | 30 | 3 | 15 | 4 (3 with different plans) | 4 (zenotravel, `search-failed`) |
| `mff-s4-b8` | 0 | 0 | 0 | 1 | 0 | 0 |
| `mff` | 4 | 1 | 0 | 0 | 1 (statistics only) | 0 |
| `mff-s0` | 9 | 2 | 0 | 0 | 1 (statistics only) | 0 |
| `mff-s3` | 5 | 0 | 0 | 0 | 0 | 0 |

Interpretation:

1. **`-s 4` (A*-epsilon) depends strongly on the sequence.** Plan lengths over
   the 7 variants, examples:
   depots-03 {57, 65, 67, 71, 123}, driverlog-11 {26, 27, 33, 39, 49},
   driverlog-13 {63, 65, 68, 78}, depots-01 {10, 11, 17, 18};
   synthetic `ties-tour` {14, 16, 18, 20}. Three runs change between "plan
   found" and "timeout" depending on the sequence (e.g. depots-10: plans of
   39 or 60 steps, or no plan within 120 s).
2. **`-s 0`, `-s 3` and the default `-s 5` are much less sensitive, but not
   immune.** satellite-11 (`mff` and `mff-s0`): same 44-step plan for every
   variant, but with seed 12345 EHC evaluates 968 instead of 971 states. This is
   the bucket-dependent dominance pruning of §1 (`-s 0` calls `random()` only
   for the hash values: 235 calls for every seed). The other `-s 0`/`-s 3`/`mff`
   variations of run 1 disappear under the lower load of run 2: they were
   timeouts whose partial output depended on how far the run got.
3. **"All variants time out" (33 runs)** carries no information about
   randomness: each run printed a different amount of progress output before
   the harness killed it.
4. **unseeded ≡ seed 0** in every run of run 2 except two that time out
   (driverlog-20 `-s 4`, rovers-17 `-s 0`; partial output). Consistent with
   glibc.
5. **`RAND15` grouped with the unseeded glibc sequence in 76 of 80 runs.**
   Masking glibc's own sequence to 15 bits changes little because the values are
   reduced `% BIG_INT` and the coin uses the lowest bit. This does **not** model
   Windows: the MSVC `rand()` sequence itself is different (an LCG), and the
   seed variants show what a different sequence does.

### Consequences

- A build that uses the platform `rand()`/`random()` (Windows, macOS, musl)
  would produce **different plans** for Metric-FF `-s 4` and, more rarely,
  different search statistics for `-s 0`/`-s 5`. Golden equivalence across
  platforms is only possible with one implementation of the glibc `random()`
  algorithm (TYPE_3 additive feedback, default state from `srandom(1)`),
  as rule 10 requires.
- The implementation must reproduce the sequence **bit-exactly** from the
  first call, including `srandom(0)` ≡ `srandom(1)`; reproducing only the low
  bit (coin) is not enough because the hash values use the full 31 bits.

## 5. FF 2.3 seed: recommendation

**Keep the upstream code unchanged** (`ftime` + `srandom(millitm)` →
`compat_srandom`). Measured effect on output: none, over every possible seed
and the whole corpus. Changing it to a fixed seed would be a semantic change
with no observable benefit; keeping it costs nothing because golden tests
already cover all 1000 seeds. If the maintainer prefers bit-for-bit
determinism of internal state anyway, the alternative is a fixed seed (e.g. 0),
recorded in `PATCHES.md`; outputs would not change.

## Reproduce

```sh
tools/build-reference.sh                         # build/reference/{ff,metric-ff,random_shim.so}
# Metric-FF with the proposed UB fixes: see PATCHES.md (UB-1, UB-2) → build/ubfix/metric-ff
taskset -c 0,1,4,5 python3 -m harness.studies.randomness \
    --shim build/reference/random_shim.so --ff build/reference/ff \
    --metric-ff build/ubfix/metric-ff --ids reports/data/randomness-metric-ff-ids.txt -j 4 \
    --log build/studies/rand-vary.jsonl --json build/studies/rand-vary.json \
    corpus/synthetic.json corpus/ipc.json
```
