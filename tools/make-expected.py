"""Generate python/abia_planners/expected.json from examples/manifest.json and golden/examples.

The installed package uses it for `fib-abia-planners selftest`: for every example run, the
expected outcome, exit code and plan of the reference build. Rerun after re-recording
the golden outputs of the examples. With --check, only report (exit 1) if the file
is out of date.
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from harness.cases import load_manifest

out = []
for r in load_manifest(os.path.join(ROOT, "examples", "manifest.json")):
    g = json.load(open(os.path.join(ROOT, "golden", r.run_id + ".json")))
    case_dir = os.path.relpath(r.cwd, os.path.join(ROOT, "examples")).replace(os.sep, "/")
    out.append({
        "id": r.run_id.split("/", 1)[1],
        "dir": case_dir,
        "planner": r.planner,
        "args": r.args,
        "domain": r.domain,
        "problem": r.problem,
        "selftest": r.selftest,
        "timeout": r.timeout,
        "outcome": g["outcome"],
        "exit_code": g["exit_code"],
        "plan": g["plan"],
    })
dst = os.path.join(ROOT, "python", "abia_planners", "expected.json")
text = json.dumps(out, indent=0, ensure_ascii=False) + "\n"
if "--check" in sys.argv[1:]:
    with open(dst, encoding="utf-8") as f:
        if f.read() != text:
            sys.exit("out of date: %s\nRun: python3 tools/make-expected.py" % os.path.relpath(dst, ROOT))
    print("up to date: %s (%d runs)" % (os.path.relpath(dst, ROOT), len(out)))
else:
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote %s: %d runs" % (dst, len(out)))
