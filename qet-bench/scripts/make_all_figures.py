#!/usr/bin/env python3
"""Generate all first-deliverable figures."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.run_noise_sweeps import main as run_noise_sweeps
from scripts.run_null_tests import main as run_null_tests
from scripts.run_parameter_sweep import main as run_parameter_sweep


def main() -> None:
    """Run every deterministic figure-generation script."""
    run_parameter_sweep()
    run_noise_sweeps()
    run_null_tests()


if __name__ == "__main__":
    main()

