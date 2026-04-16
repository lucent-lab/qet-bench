#!/usr/bin/env python3
"""Reproduce the exact benchmark ledgers and write a CSV artifact."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from qet_bench.ledgers import benchmark_ledgers


def main() -> None:
    """Print benchmark values and save ``results/data/benchmarks.csv``."""
    output = ROOT / "results" / "data" / "benchmarks.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    data = benchmark_ledgers()
    columns = ["h", "k", "E_A", "H1", "V", "E1", "E_B", "E_A_minus_E_B", "phi", "trace_final"]
    data.to_csv(output, index=False)
    print(data[columns].to_string(index=False, float_format=lambda value: f"{value:.16g}"))
    print(f"\nwrote {output}")


if __name__ == "__main__":
    main()

