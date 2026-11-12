"""Command ``abia-planners``: copy the course examples and run the self-test.

  abia-planners examples [CARPETA]     copia los ejemplos (por defecto ./abia-ejemplos)
  abia-planners selftest [--all]       comprueba que los planificadores funcionan
  abia-planners info                   versión, plataforma y rutas
"""
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time

from . import EXAMPLES_DIR, PACKAGE_DIR, __version__, binary
from ._classify import classify, extract_plan

DEFAULT_EXAMPLES = "abia-ejemplos"
SKIP_FILES = ("manifest.json", "SOURCES.md")   # maintainer files, not for students


def cmd_examples(args):
    dst = os.path.abspath(args.dir)
    if os.path.exists(dst) and (not os.path.isdir(dst) or os.listdir(dst)):
        print("No copio nada: '%s' ya existe y no está vacía.\n"
              "Elige otra carpeta, por ejemplo:  abia-planners examples otra-carpeta" % dst)
        return 1
    shutil.copytree(EXAMPLES_DIR, dst, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(*SKIP_FILES))
    folders = sorted(d for d in os.listdir(dst) if os.path.isdir(os.path.join(dst, d)))
    print("Ejemplos copiados en: %s" % dst)
    print("Carpetas: %s" % ", ".join(folders))
    print("\nPara empezar:")
    print("  cd \"%s\"" % os.path.join(dst, "hanoi"))
    print("  ff -o hanoi.pddl -f hanoi-3.pddl")
    print("\nCada carpeta tiene un README.md con los comandos de todos sus problemas.")
    return 0


def _decode(b):
    return b.decode("utf-8", "replace").replace("\r\n", "\n")


def _run_one(case, root):
    argv = [binary(case["planner"])] + case["args"] + ["-o", case["domain"], "-f", case["problem"]]
    cwd = os.path.join(root, *case["dir"].split("/"))
    t0 = time.time()
    try:
        p = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           timeout=case["timeout"])
        rc, out, err, timed_out = p.returncode, _decode(p.stdout), _decode(p.stderr), False
    except subprocess.TimeoutExpired as e:
        rc, out, err, timed_out = None, _decode(e.stdout or b""), _decode(e.stderr or b""), True
    outcome, _ = classify(out, rc, timed_out, err)
    plan = extract_plan(out) if outcome == "plan-found" else None
    return outcome, rc, plan, time.time() - t0


def cmd_selftest(args):
    with open(os.path.join(PACKAGE_DIR, "expected.json"), encoding="utf-8") as f:
        expected = json.load(f)
    cases = expected if args.all else [c for c in expected if c["selftest"]]
    print("abia-planners %s — %s %s, Python %s" % (
        __version__, platform.system(), platform.machine(), platform.python_version()))
    print("ff:        %s" % binary("ff"))
    print("metric-ff: %s" % binary("metric-ff"))
    print("%d ejecuciones%s\n" % (len(cases), " (todos los ejemplos)" if args.all else ""))
    fails = 0
    for c in cases:
        cmd = ("ff" if c["planner"] == "ff" else "metric-ff") + "".join(" " + a for a in c["args"])
        label = "%-58s %-16s" % (c["id"], cmd)
        outcome, rc, plan, secs = _run_one(c, EXAMPLES_DIR)
        if outcome != c["outcome"] or rc != c["exit_code"]:
            fails += 1
            print("FALLO %s esperado %s (código %s), obtenido %s (código %s)" % (
                label, c["outcome"], c["exit_code"], outcome, rc))
            continue
        note = ""
        if outcome == "plan-found" and plan != c["plan"]:
            note = "  (plan distinto del de referencia: %d pasos frente a %d)" % (len(plan), len(c["plan"]))
        print("OK    %s %-17s %6.2fs%s" % (label, outcome, secs, note))
    print("\n%s: %d de %d correctas." % ("TODO CORRECTO" if not fails else "HAY FALLOS",
                                         len(cases) - fails, len(cases)))
    if fails:
        print("Envía esta salida completa al profesorado de la asignatura.")
    return 1 if fails else 0


def cmd_info(args):
    print("abia-planners %s" % __version__)
    print("Plataforma: %s %s (%s)" % (platform.system(), platform.release(), platform.machine()))
    print("Python:     %s (%s)" % (platform.python_version(), sys.executable))
    print("ff:         %s" % binary("ff"))
    print("metric-ff:  %s" % binary("metric-ff"))
    print("Ejemplos:   %s" % EXAMPLES_DIR)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="abia-planners",
                                 description="FF 2.3 y Metric-FF 2.1 con los ejemplos de ABIA.")
    sub = ap.add_subparsers(dest="cmd")
    sp = sub.add_parser("examples", help="copia los ejemplos de la asignatura a una carpeta")
    sp.add_argument("dir", nargs="?", default=DEFAULT_EXAMPLES,
                    help="carpeta de destino (por defecto: %s)" % DEFAULT_EXAMPLES)
    sp = sub.add_parser("selftest", help="comprueba que los planificadores funcionan")
    sp.add_argument("--all", action="store_true", help="prueba todos los ejemplos (tarda unos minutos)")
    sub.add_parser("info", help="muestra versión, plataforma y rutas")
    a = ap.parse_args(argv)
    if a.cmd is None:
        ap.print_help()
        return 0
    return {"examples": cmd_examples, "selftest": cmd_selftest, "info": cmd_info}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
