"""Generate corpus/synthetic/capacity/: test cases for the capacity limits (PATCHES.md, CAP-1).

Each family has a case just above the upstream limit (must now be solved), one at the
new limit (solved) and one just above it (limit-exceeded). The files are committed;
rerun this script only to change them, then re-record their golden outputs.

  python3 tools/make-capacity-cases.py

The parser stack limit (YYMAXDEPTH = 1000000) is not covered here: a problem that
exceeds it is several MB. PATCHES.md (CAP-1) records how it was tested.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "corpus", "synthetic", "capacity")

# Classical: one action per object, no precondition. Every object is a constant of the
# single (implicit) type, so this exercises MAX_CONSTANTS and MAX_TYPE.
OBJECTS_DOMAIN = """\
(define (domain capacity-objects)
  (:requirements :strips)
  (:predicates (visited ?x) (pair ?x ?y))
  (:action visit
    :parameters (?x)
    :effect (visited ?x)))
"""

# Classical: a chain o0 -> o1 -> ... -> oN; the only plan has N steps (MAX_PLAN_LENGTH).
CHAIN_DOMAIN = """\
(define (domain capacity-chain)
  (:requirements :strips)
  (:predicates (at ?x) (next ?x ?y))
  (:action move
    :parameters (?x ?y)
    :precondition (and (at ?x) (next ?x ?y))
    :effect (and (at ?y) (not (at ?x)))))
"""

# Numeric: every object has a fluent (level ?x) that an action can change, so each one
# is a relevant (dynamic) fluent (MAX_RELEVANT_FLUENTS). Metric-FF also adds an internal
# fluent for -(level ?x), used by the "<" comparison, so N objects give 2N+1 relevant
# fluents (with (total-cost)). One raise reaches the goal.
FLUENTS_DOMAIN = """\
(define (domain capacity-fluents)
  (:requirements :strips :fluents)
  (:predicates (obj ?x))
  (:functions (level ?x) (total-cost))
  (:action raise
    :parameters (?x)
    :precondition (and (obj ?x) (< (level ?x) 1))
    :effect (and (increase (level ?x) 1) (increase (total-cost) 1))))
"""


def objs(n, start=1):
    names = ["o%d" % i for i in range(start, start + n)]
    return "\n".join(" ".join(names[i:i + 20]) for i in range(0, len(names), 20))


def objects_problem(n):
    return ("(define (problem objects-%d)\n  (:domain capacity-objects)\n  (:objects\n%s)\n"
            "  (:init (pair o1 o1))\n  (:goal (visited o1)))\n" % (n, objs(n)))


def init_problem(n):
    # n*n (pair ...) facts in :init; static and unused, but every one is parsed
    pairs = "\n".join("   " + " ".join("(pair o%d o%d)" % (i, j) for j in range(1, n + 1))
                      for i in range(1, n + 1))
    return ("(define (problem init-%d)\n  (:domain capacity-objects)\n  (:objects\n%s)\n"
            "  (:init\n%s)\n  (:goal (visited o1)))\n" % (n * n, objs(n), pairs))


def chain_problem(n):
    nxt = "\n".join("   (next o%d o%d)" % (i, i + 1) for i in range(n))
    return ("(define (problem chain-%d)\n  (:domain capacity-chain)\n  (:objects\n%s)\n"
            "  (:init\n   (at o0)\n%s)\n  (:goal (at o%d)))\n" % (n, objs(n + 1, 0), nxt, n))


def fluents_problem(n):
    init = "\n".join("   (obj o%d) (= (level o%d) 0)" % (i, i) for i in range(1, n + 1))
    return ("(define (problem fluents-%d)\n  (:domain capacity-fluents)\n  (:objects\n%s)\n"
            "  (:init\n   (= (total-cost) 0)\n%s)\n  (:goal (>= (level o1) 1))\n"
            "  (:metric minimize (total-cost)))\n" % (n, objs(n), init))


FILES = {
    "objects-domain.pddl": OBJECTS_DOMAIN,
    "chain-domain.pddl": CHAIN_DOMAIN,
    "fluents-domain.pddl": FLUENTS_DOMAIN,
    # MAX_CONSTANTS / MAX_TYPE: upstream 2000, now 20000
    "objects-2001.pddl": objects_problem(2001),
    "objects-20000.pddl": objects_problem(20000),
    "objects-20001.pddl": objects_problem(20001),
    # :init with more than 10000 elements (bison's default YYMAXDEPTH, now 1000000)
    "init-10201.pddl": init_problem(101),
    # MAX_PLAN_LENGTH: Metric-FF upstream 500, now 2000 (FF: 2000, unchanged)
    "chain-501.pddl": chain_problem(501),
    "chain-2000.pddl": chain_problem(2000),
    "chain-2001.pddl": chain_problem(2001),
    # MAX_RELEVANT_FLUENTS: Metric-FF upstream 1000, now 10000 (2N+1 fluents, see above)
    "fluents-500.pddl": fluents_problem(500),
    "fluents-4999.pddl": fluents_problem(4999),
    "fluents-5000.pddl": fluents_problem(5000),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, text in FILES.items():
        with open(os.path.join(OUT, name), "w", encoding="ascii", newline="\n") as f:
            f.write(text)
        print("wrote corpus/synthetic/capacity/" + name)


if __name__ == "__main__":
    main()
