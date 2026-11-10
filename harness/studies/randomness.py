"""Randomness study (Linux/glibc only; uses LD_PRELOAD).

  gcc -shared -fPIC -O2 -o shim.so harness/studies/random_shim.c -ldl
  python3 -m harness.studies.randomness --shim shim.so --ff FF --metric-ff MFF \
      --seeds 0-999 [--alt-seeds 2,3,42] MANIFEST...

For every run in the manifests:
  * ff runs: FORCE_SEED=s for every s in --seeds (FF seeds srandom() with
    ftime().millitm, i.e. 0..999), compare all outputs.
  * metric-ff runs: unseeded (= glibc seed 1), FORCE_SEED=s for --alt-seeds,
    and RAND15=1 (15-bit values, models rand() with RAND_MAX=32767).
Prints, per run id, the number of distinct normalised outputs.
"""
import argparse, concurrent.futures as cf, json, os, sys
from ..cases import load_manifest
from ..runner import run

KEYS = ("exit_code", "outcome", "plan", "stdout", "stderr")

def parse_range(s):
    out = []
    for part in s.split(","):
        if "-" in part:
            a, b = part.split("-"); out += range(int(a), int(b) + 1)
        elif part:
            out.append(int(part))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifests", nargs="+")
    ap.add_argument("--shim", required=True); ap.add_argument("--ff", required=True)
    ap.add_argument("--metric-ff", required=True)
    ap.add_argument("--seeds", default="0-999"); ap.add_argument("--alt-seeds", default="0,2,3,42,12345")
    ap.add_argument("-k", "--filter", action="append"); ap.add_argument("-j", type=int, default=min(4, os.cpu_count() or 1))
    ap.add_argument("--ids", help="file with exact run ids to include (one per line)")
    ap.add_argument("--json")
    a = ap.parse_args()
    bins = {"ff": os.path.abspath(a.ff), "metric-ff": os.path.abspath(a.metric_ff)}
    shim = os.path.abspath(a.shim)
    runs = [r for m in a.manifests for r in load_manifest(m)]
    if a.filter:
        runs = [r for r in runs if any(f in r.run_id for f in a.filter)]
    if a.ids:
        want = {l.split()[0] for l in open(a.ids) if l.strip()}
        runs = [r for r in runs if r.run_id in want]
    jobs = []
    for r in runs:
        if r.planner == "ff":
            variants = [("seed=%d" % s, {"FORCE_SEED": str(s)}) for s in parse_range(a.seeds)]
        else:
            variants = [("unseeded", {})] + [("seed=%d" % s, {"FORCE_SEED": str(s)}) for s in parse_range(a.alt_seeds)] \
                       + [("rand15", {"RAND15": "1"})]
        for name, env in variants:
            jobs.append((r, name, dict(env, LD_PRELOAD=shim)))
    res, detail = {}, {}
    with cf.ThreadPoolExecutor(a.j) as ex:
        futs = {ex.submit(run, r.argv(bins), r.cwd, r.timeout, env): (r, n) for r, n, env in jobs}
        for f in cf.as_completed(futs):
            r, n = futs[f]; out = f.result()
            key = json.dumps([out[k] for k in KEYS])
            res.setdefault(r.run_id, {}).setdefault(key, []).append(n)
            detail.setdefault(r.run_id, {})[n] = {
                "outcome": out["outcome"], "timed_out": out["timed_out"],
                "plan_len": None if out["plan"] is None else len(out["plan"]),
                "wall_s": round(out["wall_s"], 2), "group": key}
    summary = {}
    for rid in sorted(res):
        groups = res[rid]
        gid = {k: i for i, k in enumerate(groups)}
        summary[rid] = {"groups": [sorted(v) for v in groups.values()],
                        "variants": {n: dict(d, group=gid[d["group"]]) for n, d in sorted(detail[rid].items())}}
        print("%-4s %-60s %d distinct output(s) over %d variants" %
              ("OK" if len(groups) == 1 else "VARY", rid, len(groups), sum(map(len, groups.values()))))
    if a.json:
        json.dump(summary, open(a.json, "w"), indent=1)
    return 0

if __name__ == "__main__":
    sys.exit(main())
