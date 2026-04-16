#!/usr/bin/env python3
"""Run null-test diagnostics and generate a comparison figure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from qet_bench.exact import qet_ledger
from qet_bench.null_tests import (
    k_zero_scan,
    product_state_null,
    random_bob_only_unitary_scan,
    scrambled_bit_scan,
    wrong_angle_scan,
)
from qet_bench.plotting import plot_null_comparison, plot_wrong_angle_scan


def main() -> None:
    """Save null-test data, a JSON summary, and a comparison figure."""
    data_dir = ROOT / "results" / "data"
    fig_dir = ROOT / "results" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    baseline = qet_ledger(h=1.0, k=0.5)
    k_scan = k_zero_scan(h=1.0)
    q_scan = scrambled_bit_scan(h=1.0, k=0.5)
    product = product_state_null(h=1.0, k=0.5)
    bob_only = random_bob_only_unitary_scan(h=1.0, k=0.5, n=1000, seed=0)
    angle_scan = wrong_angle_scan(h=1.0, k=0.5)

    k_scan_path = data_dir / "k_zero_scan.csv"
    q_scan_path = data_dir / "scrambled_bit_scan.csv"
    bob_only_path = data_dir / "bob_only_random_scan.csv"
    angle_scan_path = data_dir / "wrong_angle_scan.csv"
    k_scan.to_csv(k_scan_path, index=False)
    q_scan.to_csv(q_scan_path, index=False)
    bob_only.to_csv(bob_only_path, index=False)
    angle_scan.to_csv(angle_scan_path, index=False)

    q_half = q_scan.loc[(q_scan["feedforward_error_probability"] - 0.5).abs().idxmin()]
    angle_max = angle_scan.loc[angle_scan["E_B"].idxmax()]
    summary = {
        "baseline_E_B": float(baseline["E_B"]),
        "k_zero_E_B": float(k_scan.loc[k_scan["k"].idxmin(), "E_B"]),
        "scrambled_q_half_E_B": float(q_half["E_B"]),
        "product_00_E_B": float(product["E_B"]),
        "bob_only_max_E_B": float(bob_only["E_B"].max()),
        "wrong_angle_max_E_B": float(angle_max["E_B"]),
        "wrong_angle_phi_at_max_E_B": float(angle_max["phi"]),
        "wrong_angle_phi_optimal": float(angle_max["phi_optimal"]),
        "bob_only_diagnostic": bob_only.attrs.get("limitation", ""),
    }
    summary_path = data_dir / "null_tests_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    figure_data = pd.DataFrame(
        [
            {"label": "QET q=0", "E_B": summary["baseline_E_B"]},
            {"label": "k=0", "E_B": summary["k_zero_E_B"]},
            {"label": "q=0.5", "E_B": summary["scrambled_q_half_E_B"]},
            {"label": "|00>", "E_B": summary["product_00_E_B"]},
            {"label": "Bob-only max", "E_B": summary["bob_only_max_E_B"]},
        ]
    )
    fig_path = fig_dir / "null_test_comparison.png"
    plot_null_comparison(figure_data, fig_path)
    angle_fig_path = fig_dir / "wrong_angle_scan.png"
    plot_wrong_angle_scan(angle_scan, angle_fig_path)

    print(f"wrote {k_scan_path}")
    print(f"wrote {q_scan_path}")
    print(f"wrote {bob_only_path}")
    print(f"wrote {angle_scan_path}")
    print(f"wrote {summary_path}")
    print(f"wrote {fig_path}")
    print(f"wrote {angle_fig_path}")


if __name__ == "__main__":
    main()
