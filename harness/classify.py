"""Outcome classifier and plan extractor for FF 2.3 / Metric-FF 2.1.

Every run maps to exactly one outcome:

  plan-found, proven-unsolvable, search-failed, parse-error, usage-error,
  limit-exceeded, timeout, crash

The decision is made from the observed output and exit code only.  The
message strings are taken verbatim from the upstream sources (grep the
quoted text in src/ff and src/metric-ff).  ``reason`` gives the matched
message so reports can explain the class.  Exit codes are recorded, never
changed; the observed mapping is documented in harness/README.md.
"""

import re

OUTCOMES = (
    "plan-found",
    "proven-unsolvable",
    "search-failed",
    "parse-error",
    "usage-error",
    "limit-exceeded",
    "timeout",
    "crash",
)

# Order matters: first match wins.
_RULES = [
    # --- plan found -------------------------------------------------------
    ("plan-found", r"ff: found legal plan as follows"),
    ("plan-found", r"ff: goal can be simplified to TRUE\. The empty plan solves it"),
    # --- unsolvable -------------------------------------------------------
    ("proven-unsolvable", r"ff: goal can be simplified to FALSE\. No plan will solve it"),
    ("proven-unsolvable", r"search space empty! problem proven unsolvable"),
    ("proven-unsolvable", r"goal accesses a fluent that will never have a defined value\. Problem unsolvable"),
    # --- capacity limits ----------------------------------------------------
    ("limit-exceeded", r"increase MAX_[A-Z_]+"),
    ("limit-exceeded", r"increase YYMAXDEPTH"),         # CAP-1 (PATCHES.md)
    ("limit-exceeded", r"too many axioms!"),
    ("limit-exceeded", r"NO MEMORY in file"),
    # --- parser / input errors --------------------------------------------
    ("parse-error", r"\*\*\*\*\* ERROR \*\*\*\*"),
    ("parse-error", r"syntax error in line \d+"),
    ("parse-error", r"undeclared predicate \S+ used in domain definition"),
    ("parse-error", r"check input files"),
    ("parse-error", r"is declared to use unknown or empty type"),
    ("parse-error", r"unknown optimization method"),
    ("parse-error", r"can't find (?:operator|fact) file"),
    ("parse-error", r"Unable to open|could not open|can't open"),
    # --- command line / configuration -------------------------------------
    ("usage-error", r"ff: unknown option"),
    ("usage-error", r"unknown search configuration"),
    ("usage-error", r"Unknown search configuration"),
    ("usage-error", r"invalid cost bound"),
    # fib-abia-planners UB-3: file argument or path + file name longer than MAX_LENGTH - 1
    ("usage-error", r"too long \(at most \d+ characters\)"),
    # Metric-FF -s 4 / -s 5 on a problem without a usable :metric
    ("usage-error", r"Optimization criterion not established"),
    ("usage-error", r"^usage of ff:"),
    # --- search gave up without proof -------------------------------------
    ("search-failed", r"Astar epsilon search space empty!\nBailing out"),
    ("search-failed", r"Enforced Hill-climbing failed !"),
]
_RULES = [(o, re.compile(p, re.M)) for o, p in _RULES]

_PLAN_HEADER = "ff: found legal plan as follows"
_STEP_RE = re.compile(r"^\s*(?:step\s+)?(\d+): (.*?)\s*$")


def extract_plan(stdout: str):
    """Return the list of plan steps (strings), [] for an empty plan, None if no plan."""
    if "ff: goal can be simplified to TRUE. The empty plan solves it" in stdout:
        return []
    idx = stdout.find(_PLAN_HEADER)
    if idx < 0:
        return None
    steps = []
    started = False
    for line in stdout[idx + len(_PLAN_HEADER):].split("\n")[1:]:
        m = _STEP_RE.match(line)
        if m:
            started = True
            if int(m.group(1)) != len(steps):
                raise ValueError("non-contiguous plan step numbering: %r" % line)
            steps.append(m.group(2))
        elif started or line.strip():
            # first non-step line after the steps (or unexpected text) ends the plan
            if started:
                break
            if not line.strip():
                continue
            break
    return steps


def classify(stdout: str, exit_code, timed_out: bool = False, stderr: str = ""):
    """Return (outcome, reason).  Parser diagnostics go to stderr, so both streams are read."""
    if timed_out:
        return "timeout", "timeout"
    if exit_code is None or exit_code < 0:
        return "crash", "signal %s" % (-exit_code if exit_code is not None else "?")
    text = (stdout + "\n" + stderr).replace("\r\n", "\n")
    for outcome, rx in _RULES:
        m = rx.search(text)
        if m:
            if outcome == "search-failed" and _PLAN_HEADER in text:
                continue
            return outcome, m.group(0).replace("\n", " ")
    # Windows: abnormal termination codes (e.g. 0xC0000005) are large positive
    if exit_code not in (0, 1):
        return "crash", "exit code %d" % exit_code
    if exit_code == 0 and "time spent:" in text:
        # Metric-FF with -i 0 prints neither plan nor success message (src/metric-ff/main.c)
        return "plan-found", "exit 0, plan not printed (-i 0)"
    return "search-failed", "no recognised message (exit %d)" % exit_code
