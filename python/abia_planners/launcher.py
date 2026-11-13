"""Console commands ``ff`` and ``metric-ff``.

They run the bundled executable with the same arguments, standard input, output
and error, and exit with the planner's exit code. The planners' behaviour is not
changed (CLAUDE.md rule 1).

The only addition: when Metric-FF stops with "Optimization criterion not
established" because the problem has no usable ``:metric``, a short hint in
Spanish is written to standard error *after* the planner's own output.
"""
import os
import re
import signal
import subprocess
import sys

from . import binary

HINT = (
    "\n[fib-abia-planners] Si el error es \"Optimization criterion not established\": el problema\n"
    "[fib-abia-planners] no tiene una métrica que minimizar ((:metric minimize ...)), y las\n"
    "[fib-abia-planners] configuraciones -s 4 y -s 5 (la de por defecto) la necesitan.\n"
    "[fib-abia-planners] Para buscar un plan sin optimizar, usa -s 0:\n"
    "[fib-abia-planners]     metric-ff -s 0 %s\n"
)


def _missing(name):
    sys.stderr.write("fib-abia-planners: no se encuentra el ejecutable %s.\n"
                     "Reinstala el paquete: pip install --force-reinstall fib-abia-planners\n" % binary(name))
    return 127


def _run(name, args):
    exe = binary(name)
    if not os.path.exists(exe):
        return _missing(name)
    # The child gets Ctrl-C directly (same process group); the launcher just waits.
    old = signal.signal(signal.SIGINT, signal.SIG_IGN)
    try:
        rc = subprocess.call([exe] + args)
    finally:
        signal.signal(signal.SIGINT, old)
    return rc


def _exit_like(rc):
    """Exit with the child's status; re-raise a terminating signal on POSIX."""
    if rc < 0 and hasattr(signal, "SIGKILL"):
        sig = -rc
        try:
            signal.signal(sig, signal.SIG_DFL)
            os.kill(os.getpid(), sig)
        except (OSError, ValueError):
            pass
        sys.exit(128 + sig)
    sys.exit(rc)


def _search_config(args):
    """Metric-FF's -s value (default 5), or None if it cannot be read."""
    for i, a in enumerate(args):
        if a == "-s" and i + 1 < len(args):
            try:
                return int(args[i + 1])
            except ValueError:
                return None
    return 5


def _problem_path(args):
    path, problem = "", None
    for i, a in enumerate(args[:-1]):
        if a == "-p":
            path = args[i + 1]
        elif a == "-f":
            problem = args[i + 1]
    return None if problem is None else path + problem


def _needs_hint(args, rc):
    if rc != 1 or _search_config(args) not in (4, 5):
        return False
    problem = _problem_path(args)
    if not problem or not os.path.isfile(problem):
        return False
    try:
        with open(problem, "rb") as f:
            text = f.read().decode("latin-1").lower()
    except OSError:
        return False
    text = re.sub(r";[^\n]*", "", text)       # ignore PDDL comments
    return not re.search(r":metric\s+minimize", text)


def ff():
    _exit_like(_run("ff", sys.argv[1:]))


def metric_ff():
    args = sys.argv[1:]
    rc = _run("metric-ff", args)
    if _needs_hint(args, rc):
        rest = []
        skip = False
        for i, a in enumerate(args):          # repeat the user's arguments without -s N
            if skip:
                skip = False
                continue
            if a == "-s":
                skip = True
                continue
            rest.append(a)
        sys.stderr.write(HINT % " ".join(rest))
    _exit_like(rc)
