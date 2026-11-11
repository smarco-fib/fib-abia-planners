#!/bin/sh
# Build the golden-reference binaries from the pristine sources (see golden/README.md).
#   tools/build-reference.sh [OUTDIR]        default OUTDIR: build/reference
# Produces OUTDIR/ff, OUTDIR/metric-ff and OUTDIR/random_shim.so (Linux/glibc only).
# Uses at most 4 parallel make jobs.
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
OUT=${1:-$ROOT/build/reference}
CC=${CC:-gcc-9}
mkdir -p "$OUT/src"
for p in ff metric-ff; do
    rm -rf "$OUT/src/$p"
    cp -r "$ROOT/src/$p" "$OUT/src/$p"
    make -C "$OUT/src/$p" -j4 CC="$CC" > "$OUT/src/$p.build.log" 2>&1
    cp "$OUT/src/$p/ff" "$OUT/$p"
done
gcc -shared -fPIC -O2 -o "$OUT/random_shim.so" "$ROOT/harness/studies/random_shim.c" -ldl
echo "built: $OUT/ff $OUT/metric-ff $OUT/random_shim.so"
