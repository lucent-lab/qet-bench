#!/usr/bin/env python3
"""Run the optional branch-resolved Qiskit/Aer interoperability check."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from qet_bench.qiskit_bridge import is_qiskit_aer_available, run_aer_branches


def main() -> None:
    """Run the optional Aer smoke check when Qiskit/Aer is installed."""
    if not is_qiskit_aer_available():
        print(
            "Qiskit/Aer optional dependencies are not installed; "
            'install with: pip install -e ".[qiskit]"'
        )
        return

    data_dir = ROOT / "results" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    rows = [
        {"h": 1.0, "k": 0.5, **run_aer_branches(h=1.0, k=0.5, shots=8192, seed=0)},
        {"h": 1.0, "k": 1.0, **run_aer_branches(h=1.0, k=1.0, shots=8192, seed=1)},
    ]
    output_path = data_dir / "qiskit_bridge_benchmarks.csv"
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    columns = ["h", "k", "E_B", "exact_E_B", "absolute_E_B_error"]
    print(_format_table(rows, columns))
    print(f"\nwrote {output_path}")


def _format_table(rows: list[dict[str, float]], columns: list[str]) -> str:
    lines = [" ".join(f"{column:>18}" for column in columns)]
    for row in rows:
        lines.append(" ".join(f"{float(row[column]):18.12g}" for column in columns))
    return "\n".join(lines)


if __name__ == "__main__":
    main()
