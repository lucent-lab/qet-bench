#!/usr/bin/env python3
"""Run the pure-Python reference branch cross-check."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from qet_bench.reference_branch import reference_branch_audit, reference_qet_ledger


def main() -> None:
    """Print and save the independent reference benchmark outputs."""
    data_dir = ROOT / "results" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    ledgers = [
        {"h": 1.0, "k": 0.5, **reference_qet_ledger(h=1.0, k=0.5)},
        {"h": 1.0, "k": 1.0, **reference_qet_ledger(h=1.0, k=1.0)},
    ]
    ledger_path = data_dir / "reference_branch_benchmarks.csv"
    _write_csv(ledger_path, ledgers)

    audit = reference_branch_audit(h=1.0, k=0.5)
    audit_path = data_dir / "reference_branch_audit_h1_k0p5.csv"
    _write_csv(audit_path, audit)

    columns = ["h", "k", "E_A", "H1", "V", "E1", "E_B", "trace_final"]
    print(_format_table(ledgers, columns))
    print(f"\nwrote {ledger_path}")
    print(f"wrote {audit_path}")


def _write_csv(path: Path, rows: list[dict[str, float | int]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _format_table(rows: list[dict[str, float | int]], columns: list[str]) -> str:
    lines = [" ".join(f"{column:>18}" for column in columns)]
    for row in rows:
        lines.append(" ".join(_format_value(row[column]) for column in columns))
    return "\n".join(lines)


def _format_value(value: float | int) -> str:
    if isinstance(value, int):
        return f"{value:18d}"
    return f"{value:18.16g}"


if __name__ == "__main__":
    main()

