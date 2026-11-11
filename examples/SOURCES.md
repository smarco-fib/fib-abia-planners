# Course examples: provenance and changes

Maintainer documentation (students read `README.md`).

Originals are stored unmodified in `ejemplos-abia-planning/` with SHA-256
checksums. The copies here
are teaching material (CLAUDE.md rule 11): they may be corrected and commented.
Every change is a separate commit and is listed in the folder's `README.md`
("Cambios respecto al original").

| Folder | Source | Origin of the domain |
|---|---|---|
| `hanoi/`, `n-puzzle/`, `tsp/`, `logistics/`, `ascensor/`, `rovers/` | course zips (`ejemplos-abia-planning/*.zip`, files dated 2008–2011) | Hanoi: Héctor Geffner's formalisation; Logistics: IPC-1998; Miconic: IPC-2000; Rovers: IPC-2002; 8-puzzle and TSP: classic teaching examples |
| `aircargo/`, `blocks/`, `vector/` | ABIA course material (unit 5, `C5-*`) | Course examples |
| `smartbus/`, `binpacking/`, `sharebath/`, `asignaturas/` | ABIA course material | Course examples; `asignaturas` is in Catalan |

The maintainer confirmed (2026-11-11) that the material is old, freely released
and may be redistributed for academic use; author credits are kept where the
files carry them.

## Changes (summary; details in each README and commit)

| Commit subject | Files |
|---|---|
| tsp: return-against must end in the starting city | `tsp/tsp.pddl` |
| aircargo (untyped): descarga must delete (Dentro ?c ?av) | `aircargo/C5-aircargo-domain3ops.pddl` |
| sharebath: problem name must not start with a digit | `sharebath/ShareBath-problem.pddl` |
| Give example problems names that match their contents | binpacking, blocks, vector problems |
| Fix sloppy type declarations in vector and smartbus domains | `vector/C5-vector-typed-v1.{1,2}.pddl`, `smartbus/SmartBus-domain-fluents-v2.pddl` |
| blocks: add a worked solution to the STRIPS-to-PDDL exercise | `blocks/ejercicio-strips/solucion-*.pddl` (new) |

## Observations not changed

- `smartbus/SmartBus-domainv2.pddl`: `montar-movtotal` lets a passenger without
  reduced mobility take any seat, including adapted ones. Left as is and posed as
  a question in the README.
- `asignaturas/`: named "metric" but the problems have no `:metric`;
  `prova-1` and `prova-3` are unsolvable by design (credit limits).
- `binpacking/` with `v2op`: `prob2` takes about one minute.
- `blocks/` with 4 operators: problem 3 (17 blocks) is very hard for both
  planners (see manifest notes).
