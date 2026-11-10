# CLAUDE.md — ABIA-Planners

Project: reproducible, tested distribution of FF 2.3 and Metric-FF 2.1 (Jörg Hoffmann)
plus the ABIA course examples, installable with `pip install abia-planners` on
Windows, Linux and macOS. This is a porting and packaging project, not a
planner-improvement project.

Communicate with the maintainer in Spanish. Code, comments, commit messages and
maintainer documentation in English. Student-facing material in Spanish.

## Standing rules

1. **Semantics are frozen.** Do not change search algorithms, heuristics, default options (Metric-FF 2.1 defaults to `-s 5`: keep it), command-line interface, plan output format or exit codes. Code implementing search, heuristics and instantiation (e.g. `search.c`, `relax.c`, `inst_*.c`) may be modified only to fix a portability or undefined-behaviour problem, with written justification in `PATCHES.md`.
2. **Upstream is traceable.** Import pristine upstream sources verbatim in their own commit and record SHA-256 checksums in `UPSTREAM.md`. Apply every modification as a separate, small commit with a single purpose. List every deviation from upstream in `PATCHES.md`: file, reason, and evidence that output is unchanged.
3. **Golden equivalence is the acceptance criterion.** A change is accepted only if, on the full test corpus, normalised outputs (plans, outcome class, exit code) are identical to the golden reference. The only tolerated difference is lines that report time. For malformed-input cases, outcome class and exit code must match; any change in diagnostic text must be listed in `PATCHES.md`. If a change cannot satisfy this, stop and ask the maintainer.
4. **Fixing undefined behaviour is not free.** If removing UB changes any golden output, stop and report it: the reference behaviour depended on UB and the maintainer must decide.
5. **Capacity limits.** Do not change `MAX_*` constants or other compile-time limits unless a course domain hits them, and only after the maintainer approves. Document any such change.
6. **No substitution.** Never replace FF or Metric-FF with another planner (Ferroplan, Fast Downward, ENHSP, Planutils images, …), not even as a fallback.
7. **Evidence or "unvalidated".** A platform counts as supported only when native CI runners have built it, passed the full corpus and passed a clean-install test. Report everything else as unvalidated.
8. **Licensing.** The distribution is GPL. Keep upstream copyright notices; ship `LICENSE`, `NOTICE` and the corresponding source. Do not copy code from any repository whose licence is missing or incompatible; you may read it as a reference. Flag any licence doubt to the maintainer.
9. **Ask before irreversible or public actions:** creating public repositories, publishing to PyPI or a container registry, creating tags or releases, changing licences, rewriting history.
10. **Randomness is part of the semantics.** Both planners call `random()`. Metric-FF 2.1 breaks ties in A*-epsilon (`-s 4`, and `-s 5` when EHC fails) with an unseeded `random() % 2`. FF 2.3 seeds `random()` with the clock's milliseconds and uses it for state-hash values. Platform C libraries produce different sequences, and Windows has no `random()`. All builds must use **one portable, licence-compatible implementation that reproduces the glibc `random()` sequence**, provided in `src/compat/`. Never use the platform's `rand()`/`random()`. Any run-to-run or cross-platform difference in output is a bug to investigate, not a tolerance to widen.
11. **Course material is read-only.** Ship course examples byte-for-byte as provided, including line endings, and record their SHA-256. If you believe an example has a defect, report it to the maintainer; never fix it silently. Graded assignment material (e.g. SmartBusFluents) never goes into the public package or a public repository.
