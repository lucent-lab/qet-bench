#!/usr/bin/env python3
"""Run the h/k parameter sweep and generate its figure."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from qet_bench.plotting import plot_energy_ledger_vs_ratio
from qet_bench.sweeps import sweep_h_over_k


def main() -> None:
    """Save the h/k sweep CSV and figure."""
    data_dir = ROOT / "results" / "data"
    fig_dir = ROOT / "results" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    ratios = np.linspace(0.2, 5.0, 49)
    data = sweep_h_over_k(ratios, k=1.0)
    csv_path = data_dir / "h_over_k_sweep.csv"
    fig_path = fig_dir / "energy_ledger_vs_h_over_k.png"
    data.to_csv(csv_path, index=False)
    plot_energy_ledger_vs_ratio(data, fig_path)
    print(f"wrote {csv_path}")
    print(f"wrote {fig_path}")


if __name__ == "__main__":
    main()

