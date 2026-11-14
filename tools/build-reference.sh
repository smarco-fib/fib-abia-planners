#!/bin/sh
# Build the golden-reference binaries (see golden/README.md): the upstream sources
# plus UB-1 and UB-2, exactly as in commit REF below, compiled with the upstream
# makefiles and gcc-9. Later portability patches do not affect this build, so the
# golden outputs can always be reproduced.
#   tools/build-reference.sh [OUTDIR]        default OUTDIR: build/reference
# Produces OUTDIR/ff, OUTDIR/metric-ff and OUTDIR/random_shim.so (Linux/glibc only).
# Uses at most 4 parallel make jobs.
set -eu
REF=d389fd8   # metric-ff: guard NULL ... (UB-2); golden recorded from this source tree
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT=${1:-$ROOT/build/reference}
CC=${CC:-gcc-9}
rm -rf "$OUT/src"; mkdir -p "$OUT/src"
git -C "$ROOT" archive "$REF" src/ff src/metric-ff | tar -x -C "$OUT"
for p in ff metric-ff; do
    make -C "$OUT/src/$p" -j4 CC="$CC" > "$OUT/src/$p.build.log" 2>&1
    cp "$OUT/src/$p/ff" "$OUT/$p"
done
gcc -shared -fPIC -O2 -o "$OUT/random_shim.so" "$ROOT/harness/studies/random_shim.c" -ldl
echo "built from $REF: $OUT/ff $OUT/metric-ff $OUT/random_shim.so"
