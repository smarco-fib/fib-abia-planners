"""FF vs Metric-FF study (data for reports/ff-vs-metricff.md).

  python3 -m harness.studies.compare --ff FF --metric-ff MFF -j 2 --repeat 3 \
      --json build/studies/compare.json examples/manifest.json
  python3 -m harness.studies.compare --report build/studies/compare.json

Runs every (case, config) of the manifests --repeat times and keeps, per run:
outcome, exit code, plan, median wall time and the largest peak RSS. Configs
removed from a manifest (non-terminating runs) are reported as "not run".
For stable timings use -j no larger than the number of physical cores.
"""
import argparse
import concurrent.futures as cf
import json
import os
import statistics
import sys

from ..cases import load_manifest
from ..runner import run

CONFIGS = ("ff", "mff-s0", "mff")


def measure(a):
    bins = {"ff": os.path.abspath(a.ff), "metric-ff": os.path.abspath(a.metric_ff)}
    runs = [r for m in a.manifests for r in load_manifest(m) if r.config in CONFIGS]
    if a.filter:
        runs = [r for r in runs if any(f in r.run_id for f in a.filter)]

    def one(r):
        reps = [run(r.argv(bins), r.cwd, r.timeout) for _ in range(a.repeat)]
        first = reps[0]
        same = all(x["outcome"] == first["outcome"] and x["plan"] == first["plan"] for x in reps)
        rss = [x["maxrss_kib"] for x in reps if x["maxrss_kib"] is not None]
        return r, {
            "outcome": first["outcome"], "exit_code": first["exit_code"], "plan": first["plan"],
            "wall_s": round(statistics.median(x["wall_s"] for x in reps), 3),
            "maxrss_kib": max(rss) if rss else None, "repeats_agree": same,
        }

    cases = {}
    with cf.ThreadPoolExecutor(a.j) as ex:
        for i, (r, res) in enumerate(ex.map(one, runs), 1):
            c = cases.setdefault(r.case_id, {"id": r.case_id, "domain": r.domain,
                                             "configs_in_manifest": [], "runs": {}})
            c["configs_in_manifest"].append(r.config)
            c["runs"][r.config] = res
            print("[%d/%d] %s %s %.2fs" % (i, len(runs), r.run_id, res["outcome"], res["wall_s"]),
                  file=sys.stderr, flush=True)
    with open(a.json, "w", encoding="utf-8") as f:
        json.dump({"repeat": a.repeat, "cases": list(cases.values())}, f, indent=1)


def _fmt_t(s):
    return "%.2f" % s


def report(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    rows = []
    for c in data["cases"]:
        rs = c["runs"]
        cells = [c["id"]]
        for cfg in CONFIGS:
            r = rs.get(cfg)
            if r is None:
                cells += ["not run", "", ""]
            elif r["outcome"] == "plan-found":
                cells += [str(len(r["plan"])), _fmt_t(r["wall_s"]),
                          "%.1f" % (r["maxrss_kib"] / 1024) if r["maxrss_kib"] else ""]
            else:
                cells += [r["outcome"], _fmt_t(r["wall_s"]), ""]
        plans = {cfg: tuple(rs[cfg]["plan"]) for cfg in CONFIGS
                 if cfg in rs and rs[cfg]["outcome"] == "plan-found"}
        def same(x, y):
            if x in plans and y in plans:
                return "yes" if plans[x] == plans[y] else "no"
            return ""
        cells += [same("ff", "mff-s0"), same("mff-s0", "mff")]
        rows.append(cells)
    head = ["case", "ff len", "ff s", "ff MiB", "s0 len", "s0 s", "s0 MiB", "s5 len", "s5 s", "s5 MiB",
            "ff = s0", "s0 = s5"]
    print("| " + " | ".join(head) + " |")
    print("|" + "---|" * len(head))
    for r in rows:
        print("| " + " | ".join(r) + " |")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifests", nargs="*")
    ap.add_argument("--ff"); ap.add_argument("--metric-ff")
    ap.add_argument("-j", type=int, default=2); ap.add_argument("--repeat", type=int, default=3)
    ap.add_argument("-k", "--filter", action="append")
    ap.add_argument("--json"); ap.add_argument("--report")
    a = ap.parse_args()
    if a.report:
        report(a.report)
    else:
        measure(a)


if __name__ == "__main__":
    main()
