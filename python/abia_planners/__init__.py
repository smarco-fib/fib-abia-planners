"""fib-abia-planners: FF 2.3 and Metric-FF 2.1 with the ABIA course examples.

Console commands: ``ff``, ``metric-ff`` and ``fib-abia-planners`` (``examples``, ``selftest``).
"""
import os
import sys

__version__ = "0.2.0"

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
BIN_DIR = os.path.join(PACKAGE_DIR, "bin")
EXAMPLES_DIR = os.path.join(PACKAGE_DIR, "examples")


def binary(name):
    """Absolute path of the bundled planner executable ``name`` ('ff' or 'metric-ff')."""
    exe = name + (".exe" if sys.platform == "win32" else "")
    return os.path.join(BIN_DIR, exe)
