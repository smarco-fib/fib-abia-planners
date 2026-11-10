# Test corpus: provenance and licences

The corpus is test data only. It is **not** shipped in wheels or release archives.

| Path | Origin | Revision | Licence |
|---|---|---|---|
| `ipc/ipc-1998/…`, `ipc/ipc-2000/…`, `ipc/ipc-2002/…` | International Planning Competition benchmarks, as collected in https://github.com/potassco/pddl-instances | `cf19edf7c53d1540ddbb396c642595e0926ee552` (2017-11-28) | **No licence file in the collection.** IPC benchmarks are widely redistributed for research, but no explicit permission is recorded. **To be confirmed by the maintainer before the repository is made public.** |
| `synthetic/` | Written for this project | — | GPL-2.0-or-later (same as the project) |
| `private/` | Graded course material (e.g. SmartBusFluents). Git-ignored; never public. | — | Course material, UPC |

## Selection

- `ipc.json` was generated from an exploration run of the pristine reference
  build (instances 1–12 of each classical/ADL domain and 1–20 of each IPC-2002
  numeric domain; per-run limit 30 s on an 8-core x86-64 workstation).
- A configuration was dropped from a case when it timed out in that
  exploration, to keep CI time bounded. Crashing runs were **kept**:
  they are evidence of upstream defects (see the Checkpoint 1 report).
- Files are byte-identical copies of the collection (rule 11 applies by analogy).

Domains:

- Classical STRIPS: gripper (1998), blocks, logistics, freecell (2000), depots,
  driverlog, satellite, zenotravel (2002, STRIPS).
- ADL: gripper-adl, assembly, movie, mystery (1998), elevator full/simple ADL,
  schedule (2000).
- Numeric (IPC-2002, `:fluents`, `:metric`): depots, driverlog, rovers,
  satellite, zenotravel, settlers (also conditional effects), driverlog-hard,
  satellite-hard.
