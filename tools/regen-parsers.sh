#!/bin/sh
# Maintainer-only: regenerate the committed flex/bison output of both planners.
# A normal build needs only CMake and a C compiler (the generated files are committed).
# Versions used for the committed files are recorded in UPSTREAM.md.
#
#   --nounistd          the scanner must not include <unistd.h> (absent on Windows)
#   --never-interactive the scanner never calls isatty()/fileno(); the planners only
#                       read regular files, for which flex chooses the same code path
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
for p in ff metric-ff; do
  cd "$ROOT/src/$p"
  bison -pfct_pddl -bscan-fct_pddl scan-fct_pddl.y
  bison -pops_pddl -bscan-ops_pddl scan-ops_pddl.y
  flex --nounistd --never-interactive -Pfct_pddl lex-fct_pddl.l
  flex --nounistd --never-interactive -Pops_pddl lex-ops_pddl.l
done
echo "regenerated with $(flex --version) and $(bison --version | head -1)"
