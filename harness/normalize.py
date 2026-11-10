"""Output normaliser for FF 2.3 / Metric-FF 2.1.

Only two transformations are applied (CLAUDE.md, rule 3):

1. Line endings are normalised to LF.
2. The CPU-time figures in the final "time spent:" block are masked.

The time block lines also carry counts (facts, actions, evaluated states,
search depth).  Those counts are deterministic and are kept: only the
"%7.2f seconds" number is replaced by a fixed token, so the line structure
is compared byte for byte.

Source of the format: src/ff/main.c:753-764, src/metric-ff/main.c:1053-1066
("time spent: %7.2f seconds ..." followed by "            %7.2f seconds ...").
"""

import re

TIME_MASK = "T.TT"

# "time spent:    0.00 seconds instantiating ..."  and
# "               0.00 seconds reachability analysis ..."
_TIME_RE = re.compile(r"^(time spent: |            )( *)(\d+\.\d\d)( seconds )", re.M)


def _mask(m):
    # Keep total width of the %7.2f field so alignment is unchanged.
    width = len(m.group(2)) + len(m.group(3))
    return m.group(1) + TIME_MASK.rjust(width) + m.group(4)


def normalize(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return _TIME_RE.sub(_mask, text)
