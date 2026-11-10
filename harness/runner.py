"""Run one planner invocation with a timeout; record exit code, wall time, peak RSS."""

import os
import subprocess
import sys
import time

from .classify import classify, extract_plan
from .normalize import normalize


class _Popen(subprocess.Popen):
    """Popen that keeps the child's rusage (POSIX) so we get per-run peak RSS."""

    rusage = None

    def _try_wait(self, wait_flags):  # CPython private hook, stable 3.6-3.13
        if hasattr(os, "wait4"):
            try:
                pid, sts, ru = os.wait4(self.pid, wait_flags)
            except ChildProcessError:
                pid, sts = self.pid, 0
                ru = None
            if pid == self.pid and ru is not None:
                self.rusage = ru
            return (pid, sts)
        return super()._try_wait(wait_flags)


def _maxrss_kib(ru):
    if ru is None:
        return None
    # Linux: KiB; macOS: bytes
    return ru.ru_maxrss // 1024 if sys.platform == "darwin" else ru.ru_maxrss


def run(argv, cwd, timeout, env=None):
    """Run argv in cwd. Returns a dict with raw and normalised results."""
    t0 = time.monotonic()
    timed_out = False
    if env is not None:
        env = {**os.environ, **env}
    p = _Popen(argv, cwd=cwd, stdin=subprocess.DEVNULL, env=env,
               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        out, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        p.kill()
        out, err = p.communicate()
    wall = time.monotonic() - t0
    out_s = out.decode("latin-1")  # upstream output is byte-oriented; keep bytes 1:1
    err_s = err.decode("latin-1")
    outcome, reason = classify(out_s, p.returncode, timed_out, err_s)
    try:
        plan = extract_plan(normalize(out_s)) if outcome == "plan-found" else None
    except ValueError as e:
        plan, reason = None, "plan extraction failed: %s" % e
    return {
        "exit_code": p.returncode,
        "timed_out": timed_out,
        "outcome": outcome,
        "reason": reason,
        "plan": plan,
        "stdout": normalize(out_s),
        "stderr": normalize(err_s),
        "wall_s": round(wall, 3),
        "maxrss_kib": _maxrss_kib(p.rusage),
    }
