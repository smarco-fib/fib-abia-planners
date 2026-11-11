"""Collect AddressSanitizer / UndefinedBehaviorSanitizer findings over a corpus.

Build the sanitized binaries first:

  CC=clang cmake -S . -B build/asan -DCMAKE_BUILD_TYPE=RelWithDebInfo -DABIA_SANITIZE=ON
  cmake --build build/asan

then:

  python3 -m harness.studies.sanitize --ff build/asan/ff --metric-ff build/asan/metric-ff \
      [-k FILTER] [-j N] --json out.json MANIFEST...

Every run is executed once with ASAN_OPTIONS=detect_leaks=0 (the planners never free
memory before exiting) and UBSAN_OPTIONS=halt_on_error=0. Findings are grouped by
(kind, source location); for each group the script reports how many runs hit it and
one example run. The outcome of each run is also compared with the golden outcome,
to see whether a finding coincides with a changed result.
"""
import argparse
import collections
import concurrent.futures as cf
import json
import os
import re
import sys

from ..cases import load_manifest
from ..runner import run

UBSAN_RE = re.compile(r"^(?P<loc>[^\s:]+:\d+:\d+): runtime error: (?P<msg>.*)$", re.M)
ASAN_RE = re.compile(r"ERROR: AddressSanitizer: (?P<kind>[\w-]+)")
ASAN_FRAME_RE = re.compile(r"#\d+ 0x[0-9a-f]+ in (?P<fn>\S+) (?P<loc>\S+:\d+)")


def findings(stderr):
    out = []
    for m in UBSAN_RE.finditer(stderr):
        msg = re.sub(r"-?\d+", "N", m.group("msg"))      # group values of the same kind
        out.append(("ubsan", os.path.basename(m.group("loc").rsplit(":", 1)[0]), msg))
    m = ASAN_RE.search(stderr)
    if m:
        frame = ASAN_FRAME_RE.search(stderr[m.end():])
        loc = "%s (%s)" % (os.path.basename(frame.group("loc")), frame.group("fn")) if frame else "?"
        out.append(("asan", loc, m.group("kind")))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifests", nargs="+")
    ap.add_argument("--ff", required=True)
    ap.add_argument("--metric-ff", required=True)
    ap.add_argument("--golden", default="golden")
    ap.add_argument("-k", "--filter", action="append")
    ap.add_argument("-j", type=int, default=min(4, os.cpu_count() or 1))
    ap.add_argument("--timeout-factor", type=float, default=3.0,
                    help="sanitized binaries are slower; multiply case timeouts")
    ap.add_argument("--ids", help="file with exact run ids to include (one per line)")
    ap.add_argument("--no-aslr", action="store_true",
                    help="run under 'setarch -R': ASan from LLVM < 18 crashes at random on Linux "
                         "kernels with vm.mmap_rnd_bits=32 (SIGSEGV with no report)")
    ap.add_argument("--json")
    a = ap.parse_args()
    bins = {"ff": os.path.abspath(a.ff), "metric-ff": os.path.abspath(a.metric_ff)}
    env = dict(os.environ, ASAN_OPTIONS="detect_leaks=0", UBSAN_OPTIONS="print_stacktrace=1:halt_on_error=0")
    runs = [r for m in a.manifests for r in load_manifest(m)]
    if a.filter:
        runs = [r for r in runs if any(f in r.run_id for f in a.filter)]
    if a.ids:
        want = {l.split()[0] for l in open(a.ids) if l.strip()}
        runs = [r for r in runs if r.run_id in want]

    def go(r):
        argv = (["setarch", "-R"] if a.no_aslr else []) + r.argv(bins)
        res = run(argv, r.cwd, r.timeout * a.timeout_factor, env)
        gpath = os.path.join(a.golden, r.run_id + ".json")
        golden = json.load(open(gpath)) if os.path.exists(gpath) else {}
        return r, res, golden

    groups = collections.OrderedDict()
    per_run = {}
    with cf.ThreadPoolExecutor(a.j) as ex:
        for r, res, golden in ex.map(go, runs):
            fs = findings(res["stderr"])
            same = golden.get("outcome") == res["outcome"] if golden else None
            per_run[r.run_id] = {"outcome": res["outcome"], "golden_outcome": golden.get("outcome"),
                                 "findings": [list(f) for f in fs]}
            for f in sorted(set(fs)):
                g = groups.setdefault(f, {"runs": 0, "example": r.run_id, "outcome_changed": 0})
                g["runs"] += 1
                if same is False:
                    g["outcome_changed"] += 1
    print("%d runs, %d with findings, %d distinct findings" %
          (len(runs), sum(1 for v in per_run.values() if v["findings"]), len(groups)))
    for (tool, loc, msg), g in sorted(groups.items(), key=lambda kv: -kv[1]["runs"]):
        print("%-5s %-34s %-60s runs=%-4d outcome_changed=%-3d e.g. %s" %
              (tool, loc, msg[:60], g["runs"], g["outcome_changed"], g["example"]))
    if a.json:
        json.dump({"groups": [{"tool": t, "location": l, "message": m, **g} for (t, l, m), g in groups.items()],
                   "runs": per_run}, open(a.json, "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
