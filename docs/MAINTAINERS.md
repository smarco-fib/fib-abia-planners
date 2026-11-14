# Maintainer guide

How to build, test, extend and release fib-abia-planners. Read `CLAUDE.md` first: its
rules (frozen semantics, traceable upstream, acceptance = validity) apply to every
change described here.

Repository: `git@github.com:smarco-fib/fib-abia-planners.git` (private), branch `main`.
CI: `.github/workflows/ci.yml` (see [CI](#ci)).

## 1. Layout

| Path | Contents |
|---|---|
| `upstream/` | Pristine upstream tarballs; SHA-256 in `UPSTREAM.md` |
| `src/ff/`, `src/metric-ff/` | Patched planner sources plus the committed flex/bison output |
| `src/compat/` | Portability layer: glibc-compatible `random()`, CPU time, clock |
| `CMakeLists.txt` | The single build for every platform |
| `python/abia_planners/` | Launchers (`ff`, `metric-ff`), `fib-abia-planners` CLI, `expected.json` |
| `examples/` | Course examples shipped to students; `manifest.json` lists every run |
| `corpus/` | Extra test cases: `synthetic.json` (CLI and error paths), `ipc.json` (IPC domains) |
| `golden/` | Reference outputs, one JSON per run: `golden/<suite>/<case>/<config>.json` |
| `harness/` | Test runner, normaliser, outcome classifier, studies (`harness/README.md`) |
| `tools/` | Maintainer scripts (parsers, reference build, generated files) |
| `PATCHES.md` | Every deviation from upstream, with justification and evidence |
| `STATUS.md` | Platform status table (rule 7) |
| `reports/` | Sanitizer, randomness and FF vs Metric-FF reports |

## 2. Build

Needs CMake ≥ 3.16 and GCC or Clang (MinGW-w64 GCC on Windows). No flex/bison needed.

```bash
cmake -S . -B build/cmake -DCMAKE_BUILD_TYPE=Release
```

```bash
cmake --build build/cmake -j 4
```

```bash
ctest --test-dir build/cmake
```

Binaries: `build/cmake/ff` and `build/cmake/metric-ff`. Options:

| Option | Effect |
|---|---|
| `-DABIA_STATIC=ON` | Static link (used for the Windows and musllinux wheels) |
| `-DABIA_SANITIZE=ON` | ASan + UBSan (with LLVM < 18 on recent kernels run under `setarch -R`; see `reports/sanitizers.md`) |
| `-DABIA_WERROR=ON` | Warnings are errors |

The ctest `compat_random_matches_glibc` compares `src/compat` with glibc's `random()`;
on other C libraries it reports "skipped".

The *reference build* (upstream makefiles, frozen sources of commit 13d2570, gcc-9)
that produced the golden outputs is rebuilt with `tools/build-reference.sh`.

## 3. Test

Every change to `src/` must pass the regression check on Linux x86-64 (CLAUDE.md rule 3):

```bash
python3 -m harness check --ff build/cmake/ff --metric-ff build/cmake/metric-ff -j 4 examples/manifest.json corpus/synthetic.json
```

It must print no differences. Add `corpus/ipc.json` for the full corpus (slow; part of
the final validation). `-k SUBSTRING` restricts the runs; `python3 -m harness list MANIFEST`
lists them.

For a change outside `src/` the course examples are enough; CI runs them on every platform.

## 4. Regenerate the parsers

Only when a `.y` or `.l` file changes. Needs the flex and bison versions recorded in
`UPSTREAM.md` (other versions produce different but equivalent C; record them if you
change them).

```bash
sh tools/regen-parsers.sh
```

Then build, run the regression check, and commit the `.y`/`.l` change and the
generated files together.

## 5. Add or change a course example

1. Never add exams, student work or third-party binaries (CLAUDE.md rule 11).
2. Put the files in `examples/<folder>/` (new folder per domain). Problem names must start with
   a letter (Metric-FF misreads `(problem 7x)`) and be unique.
3. Add one entry per problem to `examples/manifest.json`:
   `{"id": "<folder>/<problem>", "dir": "<folder>", "domain": "...", "problem": "...", "selftest": false}`.
   All three configurations (`ff`, `mff-s0`, `mff`) run by default; drop with `"configs"`
   any that does not terminate, and explain why in `"note"`. Mark at most one problem per
   folder `"selftest": true` (it must run in about a second).
4. Record its golden outputs:

   ```bash
   python3 -m harness record --ff build/cmake/ff --metric-ff build/cmake/metric-ff -k <folder>/ examples/manifest.json
   ```

5. Write `examples/<folder>/README.md` in Spanish: title, planner line, "## Qué contiene",
   "## Cómo ejecutarlo" (just the heading; it is generated), "## Cambios respecto al
   original". Copy the structure of an existing folder. Add the folder to the table in
   `examples/README.md` and its provenance to `examples/SOURCES.md`.
6. Regenerate the generated files and check that every command shown works:

   ```bash
   python3 tools/make-example-readmes.py
   ```

   ```bash
   python3 tools/make-expected.py
   ```

7. Commit. Any later correction of an example goes in its own commit, with the golden
   re-recorded (step 4), the generated files regenerated (step 6) and the change listed
   under "Cambios respecto al original".

The command shown in each README follows the course rule: no `:fluents` → `ff`;
`:fluents` without `:metric` → `metric-ff -s 0`; with `:metric minimize` → `metric-ff`.

## 6. Add a test case

Synthetic cases (malformed input, CLI errors) go in `corpus/synthetic/` and
`corpus/synthetic.json`; public benchmark cases in `corpus/ipc/` and `corpus/ipc.json`,
with their source and licence in `corpus/SOURCES.md`. Record the golden outputs with
the **reference build** (§2), not the CMake build, so that the golden stays the upstream
behaviour. The exception is a case that exercises a documented deviation (e.g. UB-3,
over-long arguments, where upstream has undefined behaviour): record it with the CMake
build and name the new cases in that `PATCHES.md` entry, as UB-3 does.

```bash
python3 -m harness record --ff build/reference/ff --metric-ff build/reference/metric-ff -k <case> corpus/synthetic.json
```

Then check that the CMake build matches it (§3).

## 7. Update upstream

Unlikely (both planners are no longer developed), but if a new upstream release appears:

1. Put the pristine tarball in `upstream/` and record its SHA-256 in `UPSTREAM.md`, in a
   commit of its own.
2. Diff it against the previous tarball, not against `src/`.
3. Re-apply each patch listed in `PATCHES.md`, one commit per patch.
4. Re-record the golden outputs with a reference build of the new release and review
   every changed golden file before committing it.

## 8. Diagnose a student's problem

Ask for the full output of `fib-abia-planners selftest --all` and `fib-abia-planners info`,
plus their `.pddl` files and the command they ran.

| Symptom | Likely cause |
|---|---|
| `fib-abia-planners: no se encuentra el ejecutable …` (exit 127) | Broken install or the antivirus removed the `.exe`: `pip install --force-reinstall fib-abia-planners` |
| `FALLO … obtenido timeout` on slow cases only | Slow or busy machine (limit 120 s per run): run again with nothing else open |
| `FALLO … obtenido crash` | Platform defect: reproduce on that OS/architecture and report it (rule 3) |
| `FALLO` on every case, `parse-error` | Examples folder of the package damaged: reinstall |
| `OK … (plan distinto del de referencia …)` | Not a failure: a different but valid plan (rule 3). Worth noting the platform |
| `selftest` passes but their own run fails | Their PDDL: see `docs/GUIA_ALUMNOS.md` §7 (FF with `:fluents`, Metric-FF without `:metric`, names starting with a digit) |

`selftest` compares outcome and exit code with `python/abia_planners/expected.json`
(generated from the golden outputs by `tools/make-expected.py`).

## 9. Release

Nothing has been published yet. Publishing to PyPI, creating tags and making the repository
public need the maintainer's explicit approval (CLAUDE.md rule 9).

1. Set the new version in `pyproject.toml`, `python/abia_planners/__init__.py` and
   `CMakeLists.txt` (`project(... VERSION ...)`).
2. Update `STATUS.md`. Commit and push; wait for a green CI run.
3. Download the artifacts of that run (`wheels-*` and `sdist`):

   ```bash
   gh run download <run-id> -D dist
   ```

4. Upload to TestPyPI first and install from there in a clean venv on at least one OS;
   then upload the same files to PyPI with `twine upload`. Tag the commit `vX.Y.Z`.

## CI

`.github/workflows/ci.yml`, on every push and pull request except those that only
change `*.md` or `docs/` (run it by hand from *Actions → ci → Run workflow*):

| Job | What it does |
|---|---|
| `regression` | Generated files up to date (`--check`); CMake build, ctest, regression check on examples and synthetic cases (Ubuntu 22.04, x86-64) |
| `wheels` | cibuildwheel on 5 native runners (Linux x86-64/ARM64, macOS Intel/Apple Silicon, Windows x64); each wheel runs `fib-abia-planners selftest --all` |
| `sdist` | Source distribution |
| `clean-install` | Each wheel in a fresh venv with Python 3.9 and 3.13, examples copied to a path with a space and "ñ", `selftest --all` |

Read the results with `gh run list` and `gh run view <run-id>`; a failing job's log:
`gh api --allow-escape-sequences repos/smarco-fib/fib-abia-planners/actions/jobs/<job-id>/logs`.
On a private repository macOS minutes count ×10 against the free quota.
