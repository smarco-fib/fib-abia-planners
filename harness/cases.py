"""Test-case manifests.

A manifest is a JSON file:

{
  "suite": "examples",
  "root": ".",                          # relative to the manifest file
  "default_configs": ["ff", "mff-s0", "mff"],
  "cases": [
    {"id": "hanoi/hanoi-3", "dir": "hanoi", "domain": "hanoi.pddl",
     "problem": "hanoi-3.pddl", "selftest": true,
     "configs": ["ff", "mff-s0", "mff"],          # optional, default_configs otherwise
     "timeout": 120,                                # optional, seconds
     "note": "free text"}
  ]
}

Configs are named; see CONFIGS below.  A case may also define ad-hoc configs
as objects: {"id": "mff-b10", "planner": "metric-ff", "args": ["-b", "10"]}.
"""

import json
import os
from dataclasses import dataclass, field
from typing import List

# planner: "ff" (FF 2.3) or "metric-ff" (Metric-FF 2.1); args precede -o/-f.
CONFIGS = {
    "ff": ("ff", []),
    "mff": ("metric-ff", []),          # upstream default: -s 5
    "mff-s0": ("metric-ff", ["-s", "0"]),
    "mff-s1": ("metric-ff", ["-s", "1"]),
    "mff-s2": ("metric-ff", ["-s", "2"]),
    "mff-s3": ("metric-ff", ["-s", "3"]),
    "mff-s4": ("metric-ff", ["-s", "4"]),
}


@dataclass
class Run:
    suite: str
    case_id: str
    config: str
    planner: str
    args: List[str]
    cwd: str
    domain: str
    problem: str
    timeout: float
    selftest: bool = False
    extra: dict = field(default_factory=dict)

    @property
    def run_id(self):
        return "%s/%s/%s" % (self.suite, self.case_id, self.config)

    def argv(self, binaries):
        return [binaries[self.planner]] + self.args + ["-o", self.domain, "-f", self.problem]

    def display_cmd(self):
        name = "ff" if self.planner == "ff" else "metric-ff"
        return " ".join([name] + self.args + ["-o", self.domain, "-f", self.problem])


def load_manifest(path, default_timeout=300):
    with open(path, encoding="utf-8") as f:
        m = json.load(f)
    root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(path)), m.get("root", ".")))
    suite = m["suite"]
    runs = []
    for c in m["cases"]:
        for cfg in c.get("configs", m.get("default_configs", ["ff", "mff-s0", "mff"])):
            if isinstance(cfg, dict):
                cid, planner, args = cfg["id"], cfg["planner"], list(cfg.get("args", []))
            else:
                cid = cfg
                planner, args = CONFIGS[cfg]
                args = list(args)
            runs.append(Run(
                suite=suite, case_id=c["id"], config=cid, planner=planner, args=args,
                cwd=os.path.join(root, c.get("dir", ".")),
                domain=c["domain"], problem=c["problem"],
                timeout=c.get("timeout", m.get("timeout", default_timeout)),
                selftest=c.get("selftest", False), extra=c,
            ))
    return runs
