"""ABIA-Planners test harness.

  python -m harness record  --ff BIN --metric-ff BIN [-j N] MANIFEST...   # write golden/
  python -m harness check   --ff BIN --metric-ff BIN [-j N] MANIFEST...   # compare with golden/
  python -m harness repeat  --ff BIN --metric-ff BIN -n 20 MANIFEST...    # determinism
  python -m harness list    MANIFEST...

Golden files: golden/<suite>/<case-id>/<config>.json (exit code, outcome,
plan, normalised stdout/stderr).  Timings go to a separate file passed with
--timings (never compared).
"""

import argparse
import concurrent.futures as cf
import json
import os
import platform
import sys

from .cases import load_manifest
from .runner import run

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPARED = ("exit_code", "outcome", "plan", "stdout", "stderr")


def _golden_path(golden_dir, r):
    return os.path.join(golden_dir, r.suite, r.case_id, r.config + ".json")


def _load_runs(args):
    runs = []
    for m in args.manifests:
        runs += load_manifest(m)
    if args.filter:
        runs = [r for r in runs if any(f in r.run_id for f in args.filter)]
    if getattr(args, "selftest_only", False):
        runs = [r for r in runs if r.selftest]
    return runs


def _execute(runs, binaries, jobs, timeout_override=None):
    def one(r):
        return r, run(r.argv(binaries), r.cwd, timeout_override or r.timeout)
    with cf.ThreadPoolExecutor(max_workers=jobs) as ex:
        for fut in cf.as_completed([ex.submit(one, r) for r in runs]):
            yield fut.result()


def _record_of(r, res):
    return {
        "command": r.display_cmd(),
        "cwd": os.path.relpath(r.cwd, REPO).replace(os.sep, "/"),
        **{k: res[k] for k in COMPARED},
        "reason": res["reason"],
    }


def _binaries(args):
    return {"ff": os.path.abspath(args.ff), "metric-ff": os.path.abspath(args.metric_ff)}


def _host():
    return {"platform": platform.platform(), "machine": platform.machine(),
            "python": platform.python_version()}


def cmd_record(args):
    runs = _load_runs(args)
    timings = {}
    for r, res in _execute(runs, _binaries(args), args.jobs, args.timeout):
        p = _golden_path(args.golden, r)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            json.dump(_record_of(r, res), f, indent=1, ensure_ascii=False)
            f.write("\n")
        timings[r.run_id] = {"wall_s": res["wall_s"], "maxrss_kib": res["maxrss_kib"],
                             "outcome": res["outcome"],
                             "plan_length": None if res["plan"] is None else len(res["plan"])}
        print("%-60s %-18s %7.2fs" % (r.run_id, res["outcome"], res["wall_s"]), flush=True)
    if args.timings:
        _write_timings(args.timings, timings)
    return 0


def _write_timings(path, timings):
    old = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            old = json.load(f).get("runs", {})
    old.update(timings)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"host": _host(), "runs": dict(sorted(old.items()))}, f, indent=1)
        f.write("\n")


def _diff(a, b, key):
    import difflib
    if key in ("stdout", "stderr"):
        return "".join(difflib.unified_diff(
            a.splitlines(True), b.splitlines(True), "golden", "actual", n=2))[:4000]
    return "golden=%r actual=%r" % (a, b)


def cmd_check(args):
    runs = _load_runs(args)
    fails, missing, timings = 0, 0, {}
    results = []
    for r, res in _execute(runs, _binaries(args), args.jobs, args.timeout):
        p = _golden_path(args.golden, r)
        timings[r.run_id] = {"wall_s": res["wall_s"], "maxrss_kib": res["maxrss_kib"],
                             "outcome": res["outcome"]}
        if not os.path.exists(p):
            missing += 1
            print("MISSING %s" % r.run_id, flush=True)
            continue
        with open(p, encoding="utf-8") as f:
            g = json.load(f)
        bad = [k for k in COMPARED if g.get(k) != res[k]]
        status = "OK  " if not bad else "FAIL"
        results.append({"run": r.run_id, "status": status.strip(), "mismatch": bad})
        print("%s %-60s %-18s %7.2fs" % (status, r.run_id, res["outcome"], res["wall_s"]), flush=True)
        for k in bad:
            fails += 1
            print("     %s differs:\n%s" % (k, _diff(g.get(k), res[k], k)))
    if args.timings:
        _write_timings(args.timings, timings)
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"host": _host(), "results": results}, f, indent=1)
    n = len(runs)
    print("\n%d runs, %d mismatching fields, %d missing golden" % (n, fails, missing))
    return 1 if fails or missing else 0


def cmd_repeat(args):
    runs = _load_runs(args)
    reps = [r for r in runs for _ in range(args.n)]
    seen, bad = {}, set()
    for r, res in _execute(reps, _binaries(args), args.jobs, args.timeout):
        key = tuple(json.dumps(res[k]) for k in COMPARED)
        seen.setdefault(r.run_id, set()).add(key)
    for rid, s in sorted(seen.items()):
        status = "OK  " if len(s) == 1 else "VARY"
        if len(s) > 1:
            bad.add(rid)
        print("%s %-60s %d distinct output(s) over %d runs" % (status, rid, len(s), args.n))
    print("\n%d run ids, %d non-deterministic" % (len(seen), len(bad)))
    return 1 if bad else 0


def cmd_list(args):
    for r in _load_runs(args):
        print("%-60s %s  (cwd %s)" % (r.run_id, r.display_cmd(), os.path.relpath(r.cwd, REPO)))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m harness")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("record", "check", "repeat", "list"):
        sp = sub.add_parser(name)
        sp.add_argument("manifests", nargs="+")
        sp.add_argument("-k", "--filter", action="append", help="substring of run id")
        sp.add_argument("--selftest-only", action="store_true")
        if name != "list":
            sp.add_argument("--ff", required=True)
            sp.add_argument("--metric-ff", required=True)
            sp.add_argument("-j", "--jobs", type=int, default=os.cpu_count() or 2)
            sp.add_argument("--timeout", type=float, help="override per-case timeout")
            sp.add_argument("--golden", default=os.path.join(REPO, "golden"))
            sp.add_argument("--timings", help="write wall time / peak RSS here (JSON)")
        if name == "check":
            sp.add_argument("--json", help="write a machine-readable result summary")
        if name == "repeat":
            sp.add_argument("-n", type=int, default=20)
    args = ap.parse_args(argv)
    return {"record": cmd_record, "check": cmd_check, "repeat": cmd_repeat, "list": cmd_list}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
