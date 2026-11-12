"""Regenerate the "## Cómo ejecutarlo" section of every examples/<folder>/README.md.

The section lists, for every problem in examples/manifest.json, the command a student
should copy and the reference result (plan length or outcome) from golden/examples.
Everything else in the README (title, description, "Cambios respecto al original") is
hand-written and left untouched.

Which command is shown follows the course rule (examples/README.md):
  domain without :fluents                -> ff
  :fluents, problem without :metric      -> metric-ff -s 0
  :fluents, problem with :metric         -> metric-ff

  python3 tools/make-example-readmes.py           rewrite the sections
  python3 tools/make-example-readmes.py --check   exit 1 if any README is out of date
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "examples")
HEADER = "## Cómo ejecutarlo\n"
INTRO = ("Desde esta carpeta (el número de pasos puede variar un poco según el sistema; "
         "lo importante es que el plan sea válido):\n")
COMMAND = {"ff": "ff", "mff-s0": "metric-ff -s 0", "mff": "metric-ff"}


def _text(path):
    with open(path, "rb") as f:
        s = f.read().decode("latin-1").lower()
    return re.sub(r";[^\n]*", "", s)            # drop PDDL comments


def config_for(case):
    """The configuration shown to students for this case (see module docstring)."""
    d = os.path.join(EX, *case["dir"].split("/"))
    if ":fluents" not in _text(os.path.join(d, case["domain"])):
        return "ff"
    return "mff" if re.search(r":metric\s+minimize", _text(os.path.join(d, case["problem"]))) else "mff-s0"


def result_line(case, cfg):
    golden = os.path.join(ROOT, "golden", "examples", case["id"], cfg + ".json")
    if not os.path.exists(golden):
        # the config was removed from the manifest because it does not terminate
        return "**no encuentra plan en 10 minutos** (ver arriba)"
    with open(golden, encoding="utf-8") as f:
        g = json.load(f)
    if g["outcome"] == "plan-found":
        return "plan de %d pasos" % len(g["plan"])
    if g["outcome"] == "proven-unsolvable":
        return "sin solución (el planificador demuestra que no hay plan)"
    raise SystemExit("%s/%s: outcome %r has no README wording; add it to result_line()"
                     % (case["id"], cfg, g["outcome"]))


def section(top, cases):
    out = [HEADER, "\n", INTRO]
    domain = None
    for c in cases:
        if c["domain"] != domain:
            out.append("%s#### Dominio `%s`\n" % ("\n" if domain is None else "\n\n", c["domain"]))
            domain = c["domain"]
        cfg = config_for(c)
        sub = c["dir"][len(top):].lstrip("/")
        cmd = "%s -o %s -f %s" % (COMMAND[cfg], c["domain"], c["problem"])
        if sub:
            cmd = "cd %s && %s" % (sub, cmd)
        out.append("\n`%s` — %s:\n\n```bash\n%s\n```\n" % (c["problem"], result_line(c, cfg), cmd))
    return "".join(out)


def main():
    check = "--check" in sys.argv[1:]
    with open(os.path.join(EX, "manifest.json"), encoding="utf-8") as f:
        cases = json.load(f)["cases"]
    folders = {}
    for c in cases:
        folders.setdefault(c["dir"].split("/")[0], []).append(c)
    stale = []
    for top, cs in folders.items():
        path = os.path.join(EX, top, "README.md")
        with open(path, encoding="utf-8") as f:
            old = f.read()
        start = old.index(HEADER)
        nxt = old.find("\n## ", start + len(HEADER))
        end = len(old) if nxt < 0 else nxt + 1
        new = old[:start] + section(top, cs) + ("\n" if nxt >= 0 else "") + old[end:]
        if new != old:
            stale.append(path)
            if not check:
                with open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(new)
    for p in stale:
        print(("out of date: " if check else "rewrote: ") + os.path.relpath(p, ROOT))
    if check and stale:
        print("Run: python3 tools/make-example-readmes.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
