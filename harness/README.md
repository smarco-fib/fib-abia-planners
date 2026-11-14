# Test harness

Python ≥ 3.9, standard library only.

```bash
python3 -m harness list   examples/manifest.json corpus/synthetic.json
python3 -m harness record --ff FF --metric-ff MFF examples/manifest.json   # (re)write golden/
python3 -m harness check  --ff FF --metric-ff MFF examples/manifest.json   # compare with golden/
python3 -m harness repeat --ff FF --metric-ff MFF -n 20 examples/manifest.json
```

- `normalize.py`: CRLF → LF, and masks only the `%7.2f` number in the
  `time spent:` block (`T.TT`). All other bytes, including the state/fact
  counts on those lines, are compared exactly.
- `classify.py`: maps each run to exactly one outcome from stdout + stderr +
  exit code. Matched message is stored as `reason`.
- `runner.py`: timeout, wall time, peak RSS (POSIX `wait4`).
- `cases.py`: manifest format and named configurations (`ff`, `mff` = Metric-FF
  default `-s 5`, `mff-s0` … `mff-s4`, plus ad-hoc per-case configs).
- `studies/`: one-off investigations (randomness study, LD_PRELOAD shim).

`check` is the **regression check** of CLAUDE.md rule 3 (byte-identical
normalised output on the reference platform, Linux x86-64 glibc). The
**validity check** used on every platform (same outcome class and exit code,
plans accepted by the plan validator, no crash or timeout) is still to be
written (Phase 1).

Golden files: `golden/<suite>/<case-id>/<config>.json`. Compared fields:
`exit_code`, `outcome`, `plan`, `stdout`, `stderr`; if the golden outcome is
`timeout`, only `outcome` (the killed run's partial output depends on machine
speed). `reason` and `command` are informational. Timings are written to a separate file with `--timings`.

## Observed upstream exit codes (pristine build, golden reference)

| Outcome | FF 2.3 | Metric-FF 2.1 | Typical message |
|---|---|---|---|
| plan-found | 0 | 0 | `ff: found legal plan as follows` / `goal can be simplified to TRUE` |
| proven-unsolvable | 0 | 0 | `goal can be simplified to FALSE`, `best first search space empty! problem proven unsolvable.` |
| search-failed | — | **0** | `Astar epsilon search space empty! Bailing out.` (A*-epsilon gives up; no proof) |
| parse-error | 1 | 1 | `syntax error in line N` (stderr), `undeclared predicate`, `check input files`, `can't find operator/fact file` (stderr) |
| usage-error | 1 | 1 | `unknown option`, `unknown search configuration`, `invalid cost bound`, **`Optimization criterion not established. A*epsilon not defined.`** |
| limit-exceeded | 1 | 1 | `increase MAX_…`, `increase YYMAXDEPTH` (PATCHES.md CAP-1) |
| timeout | — | — | harness timeout (e.g. Metric-FF `-s 3` on a finite unsolvable task without metric does not terminate) |
| crash | signal | signal | e.g. SIGSEGV (see reports/upstream-bugs in the Checkpoint 1 report) |

Notes:
- "proven-unsolvable" and "plan-found" both exit 0: callers must read the output.
- Metric-FF with `-i 0` prints neither the plan nor the success message; exit 0 with the time block is classified `plan-found` with reason `plan not printed (-i 0)`.
- Metric-FF's default configuration (`-s 5`) requires a `:metric` in the problem. Without one it prints the "Optimization criterion not established" error and exits 1 **before searching**. This affects all six course examples.
