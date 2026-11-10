# Course examples: provenance

The files under `examples/` are byte-for-byte copies of the ABIA course archives
in `ejemplos-abia-planning/` (rule 11: read-only; checksums in `SHA256SUMS`).
Nothing here has been edited, re-encoded or re-wrapped. `logistics/log-3-2.pddl`
has CRLF line endings, as provided.

| Archive | SHA-256 | Member dates |
|---|---|---|
| `ascensor.zip` | `9694e7d680c17f1440c0dd5d06f4d24e818b511def132bacb80104586be85d0e` | 2011-12-02 |
| `hanoi.zip` | `a7bb83eb7d02106f5be849c28ea55d2c73c541fa04861a77ec180a739879c6a0` | 2011-12-02 |
| `logistics.zip` | `c0881a5b0864c39a6f8ca5d97b66a825953a101b17721dc12a0c5b9d826fbd32` | 2011-11-24 / 2011-12-02 |
| `n-puzzle.zip` | `0d90f9fffe1320e0d8be02d149a2e50cc0fb47702fe700e861c1823744828db3` | 2011-11-24 |
| `rovers.zip` | `356d188796fcafe5549db2bb7ac3ab91c26bfbb2b89b4506b976620df9c5c2c9` | 2008-01-29 |
| `tsp.zip` | `ec07a85abf70ea6d687ef6ee1a597ec24f94b15599ac1cd3f28f06064f42691c` | 2011-12-02 |

## Origin of each domain

Attributions are **inferred from file contents** (comments, domain names,
instance names). None comes with an explicit licence. **To be confirmed by the
maintainer before any public release** (Checkpoint 1, question on provenance and
redistribution).

| Directory | Content | Evidence | Probable origin |
|---|---|---|---|
| `hanoi/` | Towers of Hanoi, 3–8 discs | header comment "formalisation by Hector Geffner" | Geffner's formalisation; teaching set in the style of the Linköping TDDC17 / Haslum PDDL examples |
| `n-puzzle/` | sliding-tile domain, `eight01.pddl` | comments reference Reinefeld's hardest 8-puzzle instances (31 steps) | same teaching set |
| `tsp/` | STRIPS TSP, 10 cities | comment style identical to `hanoi/`, `n-puzzle/` | same teaching set |
| `logistics/` | STRIPS Logistics, `log-3-2` | "plain STRIPS formulation of the standard Logistics domain" | IPC-1998 Logistics, reformulated for teaching |
| `ascensor/` | Miconic (elevator), `miconic01`–`05` | domain/predicate names of IPC-2000 Miconic STRIPS | IPC-2000 Miconic-10 (Koehler, Schindler), course instances |
| `rovers/` | Rovers STRIPS, `pfile01`–`20` | `(domain Rover)`, `roverprob1234`, 2008 file dates | IPC-2002 Rovers (Long, Fox), STRIPS track instances |

## Observations reported to the maintainer (not fixed)

- `tsp/tsp.pddl`, action `return-against`: the precondition is
  `(not-visited ?y)`, whereas the symmetric `return-along` uses `(starting ?y)`.
  As written, `return-against` can only "return" to an unvisited city, which
  then never becomes visited, so it is never part of a valid plan. The tour can
  only close via `return-along`, i.e. along an arc `(connected ?x c1)`.
  Both planners solve `tsp-10` (10 steps).
- `n-puzzle/eight01.pddl`: both planners find a plan (FF 63 steps, Metric-FF
  `-s 0` 57 steps; optimum 31). The plans use actions with repeated arguments
  (e.g. `MOVE-RIGHT T1 P2 P1 P1`); neither planner rejects repeated objects.
  `eight01x.pddl`, mentioned in the project brief, is **not** in the archives.
- None of the examples declares a `:metric`. Metric-FF's default configuration
  (`-s 5`) therefore stops with "Optimization criterion not established" on every
  example; `metric-ff -s 0` (or plain `ff`) is needed.
