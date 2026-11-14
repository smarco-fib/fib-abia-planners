# FF 2.3 vs Metric-FF 2.1 on the course examples

**Question.** For each course example, what do the three commands a student might
type give: `ff`, `metric-ff -s 0` and `metric-ff` (default, `-s 5`)? Compared on
outcome, plan length, whether the plans are identical, time and memory. Only what
the data shows is concluded.

**Scope.** The 90 problems of `examples/manifest.json` (course examples only; the
IPC corpus is left for the final validation). Plan validity is not checked here
(VAL is not integrated yet); every plan below is one the planner reported as legal.

**Method.** CMake build at commit 75c86c4 of `src/` (GCC 11.4, Linux x86-64,
Intel i7-1165G7), `python3 -m harness.studies.compare -j 2 --repeat 3` pinned to
two physical cores. Each run was repeated 3 times: outcome and plan were the same in
all 3 for every run; times are the median wall-clock time, memory the peak resident
set size. Configurations removed from the manifest because they do not terminate
within 10 minutes are shown as "not run". Raw data:
`reports/data/ff-vs-metricff-examples.json`.

## Summary

Problems are grouped by what the domain and problem use:

| Group | Problems | `ff` | `metric-ff -s 0` | `metric-ff` (default) |
|---|---|---|---|---|
| Classical (no `:fluents`) | 74 | 73 plan, 1 not run | 72 plan, 2 not run | 74 usage error |
| `:fluents`, no `:metric` | 6 | 6 parse error | 4 plan, 2 proven unsolvable | 6 usage error |
| `:fluents` and `:metric minimize` | 10 | 10 parse error | 10 plan | 10 plan |

- "usage error" is Metric-FF's `Optimization criterion not established`: the default
  configuration needs a `:metric`, and stops before searching (exit 1). The launcher
  prints the Spanish hint to use `-s 0`.
- "parse error" is FF rejecting `:fluents` (`syntax error in line 2, ':FLUENTS'`).
- The 2 unsolvable problems (`asignaturas` prova-1 and prova-3) are unsolvable on
  purpose; Metric-FF proves it.

## Classical problems: `ff` vs `metric-ff -s 0`

72 problems where both found a plan (the other 2 are the 4-operator blocks domain,
below).

| | Count |
|---|---|
| Same outcome | 72 of 72 |
| Identical plan | 22 |
| Same length, different plan | 17 |
| `ff` plan shorter | 21 |
| `metric-ff -s 0` plan shorter | 12 |

Largest length differences: blocks 4-operator problem1 (20 vs 12) and problemslides
(6 vs 10), vector v2-10val (24 vs 40), blocks 6-operator problem5 (22 vs 33),
SmartBus v2 (77 vs 86), n-puzzle eight01 (63 vs 57; the optimum is 31).

**Time.** Every problem took under 1.2 s with either planner. Total over the 72:
`ff` 1.7 s, `metric-ff -s 0` 3.5 s. Slowest: vector v2-10val (0.29 s vs 1.15 s),
blocks 6-operator problem3 (0.70 s vs 0.19 s), rovers pfile20 (0.19 s vs 0.63 s).

**Memory.** Median peak 16.2 MiB for both. Maximum 30.2 MiB (`ff`) and 68.2 MiB
(`metric-ff -s 0`); the ratio `-s 0`/`ff` ranges from 0.55 to 4.1, median 1.0.

**4-operator blocks domain.** problem3: neither `ff` nor `metric-ff -s 0` finds a
plan within 10 minutes. problem5: `ff` finds a plan of 40 steps in 0.01 s;
`metric-ff -s 0` does not within 10 minutes. Both are documented for students in
`examples/blocks/README.md`.

## Problems with `:metric`: `metric-ff -s 0` vs `metric-ff`

The 10 BinPacking problems (two domains × five problems).

- Same outcome and same plan length in all 10; identical plans in 7.
- With the default configuration, Enforced Hill-Climbing found the plan in 7 problems;
  in 3 (v1 prob2, v1 prob3, v2op prob2) it failed and A\*-epsilon found it.
- Metric value (`contenedoresOcupados`): in the v1 domain, where the only action is
  `colocar_paquete`, it equals the number of distinct containers in the plan, and is
  the same with both configurations in all 5 problems (4, 3, 6, 6, 6). For the v2op
  domain it needs simulating the plan; left for the VAL integration.
- Times are similar (largest: v2op prob2, 41 s with `-s 0` and 43 s with the default).

## What the data shows

1. For classical course problems, `ff` and `metric-ff -s 0` agree on the outcome in
   every case where both terminate, but usually return different plans (50 of 72);
   `ff`'s plan was shorter in 21 and `-s 0`'s in 12, so neither is shorter in every case.
2. `ff` was faster in total on these problems, but both answer in about a second or
   less, except in the 4-operator blocks domain, where `-s 0` finds no plan for
   problem5 (`ff` does) and neither finds one for problem3.
3. The default `metric-ff` does not run on any problem without `:metric` (80 of the 90
   course problems); `-s 0` is needed there.
4. On the problems with `:metric`, the default configuration did not give a better
   metric value than `-s 0` where it was measured (v1 domain).

Limits: one machine and one platform; course examples only; wall-clock times of
short runs (a few milliseconds) are dominated by process start-up; plan validity and
v2op metric values are pending the VAL integration.

## Per-problem data

Plan length (`len`), median time in seconds (`s`) and peak memory in MiB; `s0` is
`metric-ff -s 0`, `s5` the default `metric-ff`. The last two columns say whether the
plans are identical.

| case | ff len | ff s | ff MiB | s0 len | s0 s | s0 MiB | s5 len | s5 s | s5 MiB | ff = s0 | s0 = s5 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hanoi/hanoi-3 | 7 | 0.01 | 15.4 | 7 | 0.01 | 15.4 | usage-error | 0.00 |  | yes |  |
| hanoi/hanoi-4 | 15 | 0.01 | 15.4 | 15 | 0.01 | 15.4 | usage-error | 0.00 |  | yes |  |
| hanoi/hanoi-5 | 31 | 0.01 | 15.4 | 31 | 0.01 | 15.5 | usage-error | 0.01 |  | yes |  |
| hanoi/hanoi-6 | 63 | 0.01 | 15.5 | 64 | 0.01 | 15.5 | usage-error | 0.00 |  | no |  |
| hanoi/hanoi-7 | 127 | 0.01 | 15.5 | 127 | 0.03 | 15.5 | usage-error | 0.00 |  | yes |  |
| hanoi/hanoi-8 | 255 | 0.04 | 15.5 | 261 | 0.08 | 15.7 | usage-error | 0.00 |  | no |  |
| ascensor/miconic01 | 11 | 0.00 | 15.6 | 11 | 0.00 | 15.6 | usage-error | 0.00 |  | yes |  |
| ascensor/miconic02 | 16 | 0.00 | 15.6 | 16 | 0.00 | 15.6 | usage-error | 0.00 |  | yes |  |
| ascensor/miconic03 | 21 | 0.00 | 15.6 | 21 | 0.00 | 15.6 | usage-error | 0.00 |  | yes |  |
| ascensor/miconic04 | 34 | 0.00 | 15.7 | 34 | 0.01 | 15.7 | usage-error | 0.00 |  | yes |  |
| ascensor/miconic05 | 46 | 0.01 | 15.7 | 47 | 0.02 | 15.7 | usage-error | 0.01 |  | no |  |
| logistics/log-3-2 | 18 | 0.00 | 15.7 | 18 | 0.00 | 15.7 | usage-error | 0.00 |  | yes |  |
| n-puzzle/eight01 | 63 | 0.01 | 15.7 | 57 | 0.02 | 15.7 | usage-error | 0.00 |  | no |  |
| rovers/pfile01 | 10 | 0.00 | 15.7 | 10 | 0.00 | 15.7 | usage-error | 0.00 |  | no |  |
| rovers/pfile02 | 8 | 0.00 | 15.7 | 8 | 0.00 | 15.7 | usage-error | 0.00 |  | no |  |
| rovers/pfile03 | 13 | 0.00 | 15.7 | 11 | 0.00 | 15.7 | usage-error | 0.00 |  | no |  |
| rovers/pfile04 | 8 | 0.00 | 15.7 | 8 | 0.00 | 15.7 | usage-error | 0.00 |  | no |  |
| rovers/pfile05 | 22 | 0.00 | 15.7 | 23 | 0.00 | 15.7 | usage-error | 0.00 |  | no |  |
| rovers/pfile06 | 38 | 0.01 | 15.9 | 38 | 0.01 | 15.9 | usage-error | 0.00 |  | no |  |
| rovers/pfile07 | 18 | 0.00 | 15.9 | 18 | 0.00 | 15.9 | usage-error | 0.00 |  | no |  |
| rovers/pfile08 | 28 | 0.00 | 15.9 | 27 | 0.01 | 15.9 | usage-error | 0.00 |  | no |  |
| rovers/pfile09 | 33 | 0.01 | 15.9 | 34 | 0.01 | 15.9 | usage-error | 0.00 |  | no |  |
| rovers/pfile10 | 37 | 0.01 | 15.9 | 38 | 0.01 | 15.9 | usage-error | 0.00 |  | no |  |
| rovers/pfile11 | 37 | 0.01 | 15.9 | 38 | 0.01 | 15.9 | usage-error | 0.00 |  | no |  |
| rovers/pfile12 | 19 | 0.00 | 15.9 | 21 | 0.01 | 15.9 | usage-error | 0.00 |  | no |  |
| rovers/pfile13 | 46 | 0.01 | 15.9 | 47 | 0.04 | 15.9 | usage-error | 0.01 |  | no |  |
| rovers/pfile14 | 28 | 0.01 | 15.9 | 32 | 0.01 | 16.0 | usage-error | 0.01 |  | no |  |
| rovers/pfile15 | 42 | 0.01 | 16.0 | 41 | 0.02 | 16.0 | usage-error | 0.01 |  | no |  |
| rovers/pfile16 | 46 | 0.01 | 16.0 | 45 | 0.03 | 16.0 | usage-error | 0.01 |  | no |  |
| rovers/pfile17 | 49 | 0.01 | 16.0 | 50 | 0.04 | 16.1 | usage-error | 0.01 |  | no |  |
| rovers/pfile18 | 42 | 0.02 | 16.1 | 41 | 0.06 | 16.1 | usage-error | 0.01 |  | no |  |
| rovers/pfile19 | 74 | 0.08 | 16.1 | 72 | 0.41 | 20.5 | usage-error | 0.01 |  | no |  |
| rovers/pfile20 | 96 | 0.19 | 16.2 | 94 | 0.63 | 27.6 | usage-error | 0.02 |  | no |  |
| tsp/tsp-10 | 10 | 0.00 | 16.2 | 10 | 0.00 | 16.2 | usage-error | 0.00 |  | no |  |
| aircargo/C5-aircargo-problem1 | 6 | 0.00 | 16.2 | 6 | 0.00 | 16.2 | usage-error | 0.00 |  | no |  |
| aircargo/C5-aircargo-problem2 | 6 | 0.00 | 16.2 | 6 | 0.00 | 16.2 | usage-error | 0.00 |  | yes |  |
| aircargo/C5-aircargo-problem3 | 31 | 0.00 | 16.2 | 30 | 0.01 | 16.2 | usage-error | 0.00 |  | no |  |
| aircargo/C5-aircargo-problem4 | 27 | 0.00 | 16.2 | 27 | 0.00 | 16.2 | usage-error | 0.00 |  | yes |  |
| aircargo/C5-aircargo-problem1-typed | 6 | 0.00 | 16.2 | 6 | 0.00 | 16.2 | usage-error | 0.00 |  | no |  |
| aircargo/C5-aircargo-problem3-typed | 30 | 0.00 | 16.2 | 32 | 0.01 | 16.2 | usage-error | 0.00 |  | no |  |
| blocks/domain2ops--C5-blocks-problem1 | 11 | 0.00 | 16.2 | 9 | 0.00 | 16.2 | usage-error | 0.00 |  | no |  |
| blocks/domain2ops--C5-blocks-problem2 | 3 | 0.00 | 16.2 | 3 | 0.00 | 16.2 | usage-error | 0.00 |  | yes |  |
| blocks/domain2ops--C5-blocks-problem2b | 6 | 0.00 | 16.2 | 6 | 0.00 | 16.2 | usage-error | 0.00 |  | yes |  |
| blocks/domain2ops--C5-blocks-problem3 | 34 | 0.01 | 16.2 | 28 | 0.02 | 16.2 | usage-error | 0.00 |  | no |  |
| blocks/domain2ops--C5-blocks-problem4 | 3 | 0.00 | 16.2 | 3 | 0.00 | 16.2 | usage-error | 0.00 |  | yes |  |
| blocks/domain2ops--C5-blocks-problem5 | 22 | 0.00 | 16.2 | 22 | 0.01 | 16.2 | usage-error | 0.00 |  | no |  |
| blocks/domain2ops--C5-blocks-problemslides | 3 | 0.00 | 16.2 | 3 | 0.00 | 16.2 | usage-error | 0.00 |  | yes |  |
| blocks/domain4ops--C5-blocks-problem1 | 20 | 0.00 | 16.2 | 12 | 0.00 | 16.2 | usage-error | 0.00 |  | no |  |
| blocks/domain4ops--C5-blocks-problem2 | 6 | 0.00 | 16.2 | 6 | 0.00 | 16.2 | usage-error | 0.00 |  | yes |  |
| blocks/domain4ops--C5-blocks-problem2b | 10 | 0.00 | 16.2 | 16 | 0.00 | 16.2 | usage-error | 0.00 |  | no |  |
| blocks/domain4ops--C5-blocks-problem3 | not run |  |  | not run |  |  | usage-error | 0.01 |  |  |  |
| blocks/domain4ops--C5-blocks-problem4 | 6 | 0.00 | 16.4 | 8 | 0.00 | 16.4 | usage-error | 0.00 |  | no |  |
| blocks/domain4ops--C5-blocks-problem5 | 40 | 0.01 | 16.4 | not run |  |  | usage-error | 0.00 |  |  |  |
| blocks/domain4ops--C5-blocks-problemslides | 6 | 0.00 | 16.4 | 10 | 0.00 | 16.4 | usage-error | 0.00 |  | no |  |
| blocks/domain6ops--C5-blocks-problem1 | 11 | 0.00 | 16.4 | 12 | 0.00 | 16.4 | usage-error | 0.00 |  | no |  |
| blocks/domain6ops--C5-blocks-problem2 | 3 | 0.00 | 16.4 | 3 | 0.00 | 16.4 | usage-error | 0.00 |  | yes |  |
| blocks/domain6ops--C5-blocks-problem2b | 6 | 0.00 | 16.4 | 6 | 0.00 | 16.4 | usage-error | 0.00 |  | no |  |
| blocks/domain6ops--C5-blocks-problem3 | 34 | 0.70 | 30.2 | 41 | 0.19 | 16.5 | usage-error | 0.01 |  | no |  |
| blocks/domain6ops--C5-blocks-problem4 | 3 | 0.00 | 16.5 | 3 | 0.00 | 16.5 | usage-error | 0.00 |  | yes |  |
| blocks/domain6ops--C5-blocks-problem5 | 22 | 0.01 | 16.5 | 33 | 0.04 | 16.5 | usage-error | 0.01 |  | no |  |
| blocks/domain6ops--C5-blocks-problemslides | 3 | 0.00 | 16.5 | 3 | 0.00 | 16.5 | usage-error | 0.00 |  | yes |  |
| vector/C5-prob-vector-v1 | 2 | 0.00 | 16.5 | 2 | 0.00 | 16.5 | usage-error | 0.00 |  | yes |  |
| vector/C5-prob-vector-v1-10val | 22 | 0.01 | 16.5 | 22 | 0.01 | 16.5 | usage-error | 0.01 |  | no |  |
| vector/C5-prob-vector-Typed-v1.1 | 2 | 0.00 | 16.5 | 2 | 0.00 | 16.5 | usage-error | 0.00 |  | yes |  |
| vector/C5-prob-vector-Typed-v1.1-10val | 22 | 0.01 | 16.5 | 22 | 0.01 | 16.5 | usage-error | 0.01 |  | no |  |
| vector/C5-prob-vector-Typed-v1.2 | 2 | 0.00 | 16.5 | 2 | 0.00 | 16.5 | usage-error | 0.00 |  | no |  |
| vector/C5-prob-vector-Typed-v1.2-10val | 8 | 0.00 | 16.5 | 8 | 0.00 | 16.5 | usage-error | 0.00 |  | no |  |
| vector/C5-prob-vector-v2 | 2 | 0.00 | 16.5 | 2 | 0.00 | 16.5 | usage-error | 0.00 |  | yes |  |
| vector/C5-prob-vector-v2-5val | 8 | 0.01 | 16.5 | 8 | 0.01 | 16.5 | usage-error | 0.01 |  | no |  |
| vector/C5-prob-vector-v2-10val | 24 | 0.29 | 16.5 | 40 | 1.15 | 68.2 | usage-error | 0.05 |  | no |  |
| smartbus/SmartBus-prob1 | 55 | 0.01 | 16.5 | 55 | 0.01 | 16.5 | usage-error | 0.01 |  | no |  |
| smartbus/SmartBus-prob1v2 | 77 | 0.07 | 16.5 | 86 | 0.45 | 36.4 | usage-error | 0.02 |  | no |  |
| smartbus/SmartBus-prob1-fluents-v0 | parse-error | 0.00 |  | 55 | 0.01 | 16.6 | usage-error | 0.00 |  |  |  |
| smartbus/SmartBus-prob1-fluents-v1 | parse-error | 0.00 |  | 55 | 0.01 | 16.6 | usage-error | 0.00 |  |  |  |
| smartbus/SmartBus-prob1-fluents-v2 | parse-error | 0.00 |  | 55 | 0.01 | 16.6 | usage-error | 0.00 |  |  |  |
| binpacking/v1--BinPacking-prob1-fluents-v1-20p | parse-error | 0.00 |  | 20 | 0.01 | 16.6 | 20 | 0.01 | 16.6 |  | yes |
| binpacking/v1--BinPacking-prob1-fluents-v2-10p | parse-error | 0.00 |  | 10 | 0.00 | 16.6 | 10 | 0.00 | 16.6 |  | yes |
| binpacking/v1--BinPacking-prob2-fluents-v1 | parse-error | 0.00 |  | 20 | 0.02 | 16.6 | 20 | 0.03 | 16.6 |  | no |
| binpacking/v1--BinPacking-prob3-fluents-v1 | parse-error | 0.00 |  | 20 | 0.02 | 16.6 | 20 | 0.03 | 16.6 |  | no |
| binpacking/v1--BinPacking-prob4-fluents-v1-16p | parse-error | 0.00 |  | 16 | 0.01 | 16.6 | 16 | 0.01 | 16.6 |  | yes |
| binpacking/v2op--BinPacking-prob1-fluents-v1-20p | parse-error | 0.00 |  | 20 | 0.88 | 144.0 | 20 | 0.89 | 143.9 |  | yes |
| binpacking/v2op--BinPacking-prob1-fluents-v2-10p | parse-error | 0.00 |  | 10 | 0.01 | 16.6 | 10 | 0.01 | 16.6 |  | yes |
| binpacking/v2op--BinPacking-prob2-fluents-v1 | parse-error | 0.00 |  | 20 | 41.16 | 144.5 | 20 | 42.56 | 144.4 |  | no |
| binpacking/v2op--BinPacking-prob3-fluents-v1 | parse-error | 0.00 |  | 21 | 0.94 | 144.0 | 21 | 0.83 | 143.9 |  | yes |
| binpacking/v2op--BinPacking-prob4-fluents-v1-16p | parse-error | 0.00 |  | 16 | 0.31 | 93.4 | 16 | 0.33 | 93.2 |  | yes |
| asignaturas/assigs-metric-prova-1 | parse-error | 0.00 |  | proven-unsolvable | 0.01 |  | usage-error | 0.01 |  |  |  |
| asignaturas/assigs-metric-prova-2 | parse-error | 0.00 |  | 4 | 0.01 | 16.7 | usage-error | 0.00 |  |  |  |
| asignaturas/assigs-metric-prova-3 | parse-error | 0.00 |  | proven-unsolvable | 0.00 |  | usage-error | 0.00 |  |  |  |
| sharebath/ShareBath-problem | 76 | 0.02 | 16.7 | 76 | 0.04 | 16.7 | usage-error | 0.00 |  | no |  |
| blocks/ejercicio-strips/solucion-problem2 | 10 | 0.00 | 16.7 | 16 | 0.00 | 16.7 | usage-error | 0.00 |  | no |  |
