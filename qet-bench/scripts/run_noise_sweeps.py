#!/usr/bin/env python3
"""Run lightweight noise sweeps for the first qet-bench deliverable."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from qet_bench.noise import binary_confusion_matrix
from qet_bench.plotting import plot_eb_vs_column, plot_eb_vs_feedforward_error
from qet_bench.sweeps import (
    sweep_amplitude_damping,
    sweep_bob_angle_miscalibration,
    sweep_dephasing,
    sweep_depolarizing,
    sweep_feedforward_error,
    sweep_readout_error,
)


def main() -> None:
    """Save first-release noise sweeps, figures, and threshold metadata."""
    data_dir = ROOT / "results" / "data"
    fig_dir = ROOT / "results" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    crossing_rows: list[dict[str, float | str]] = []

    qs = np.linspace(0.0, 1.0, 51)
    feedforward = sweep_feedforward_error(qs, h=1.0, k=0.5)
    feedforward_csv = data_dir / "feedforward_error_sweep.csv"
    feedforward_fig = fig_dir / "eb_vs_feedforward_error.png"
    _write_sweep(feedforward, feedforward_csv)
    plot_eb_vs_feedforward_error(feedforward, feedforward_fig)
    crossing_rows.append(
        _crossing_row("feedforward_error", feedforward, "feedforward_error_probability")
    )

    readout = sweep_readout_error(qs, h=1.0, k=0.5)
    readout_csv = data_dir / "readout_error_sweep.csv"
    readout_fig = fig_dir / "eb_vs_readout_error.png"
    _write_sweep(readout, readout_csv)
    plot_eb_vs_column(
        readout,
        "readout_error_probability",
        "symmetric Alice readout error probability",
        "Readout-error sweep",
        readout_fig,
    )
    crossing_rows.append(_crossing_row("readout_error", readout, "readout_error_probability"))

    ps = np.linspace(0.0, 1.0, 51)
    dephasing = sweep_dephasing(ps, h=1.0, k=0.5, qubit=1)
    dephasing_csv = data_dir / "dephasing_sweep.csv"
    dephasing_fig = fig_dir / "eb_vs_dephasing.png"
    _write_sweep(dephasing, dephasing_csv)
    plot_eb_vs_column(
        dephasing,
        "noise_strength",
        "Bob phase-flip probability",
        "Dephasing sweep",
        dephasing_fig,
    )
    crossing_rows.append(_crossing_row("dephasing", dephasing, "noise_strength"))

    depolarizing = sweep_depolarizing(ps, h=1.0, k=0.5, qubit=1)
    depolarizing_csv = data_dir / "depolarizing_sweep.csv"
    depolarizing_fig = fig_dir / "eb_vs_depolarizing.png"
    _write_sweep(depolarizing, depolarizing_csv)
    plot_eb_vs_column(
        depolarizing,
        "noise_strength",
        "Bob depolarizing probability",
        "Depolarizing sweep",
        depolarizing_fig,
    )
    crossing_rows.append(_crossing_row("depolarizing", depolarizing, "noise_strength"))

    damping = sweep_amplitude_damping(ps, h=1.0, k=0.5, qubit=1)
    damping_csv = data_dir / "amplitude_damping_sweep.csv"
    damping_fig = fig_dir / "eb_vs_amplitude_damping.png"
    _write_sweep(damping, damping_csv)
    plot_eb_vs_column(
        damping,
        "noise_strength",
        "Bob amplitude-damping probability",
        "Amplitude-damping sweep",
        damping_fig,
    )
    crossing_rows.append(_crossing_row("amplitude_damping", damping, "noise_strength"))

    angle_offsets = np.linspace(-0.35, 0.35, 71)
    angle = sweep_bob_angle_miscalibration(angle_offsets, h=1.0, k=0.5)
    angle_csv = data_dir / "bob_angle_miscalibration_sweep.csv"
    angle_fig = fig_dir / "eb_vs_bob_angle_miscalibration.png"
    _write_sweep(angle, angle_csv)
    plot_eb_vs_column(
        angle,
        "angle_offset",
        "Bob angle offset from optimum",
        "Bob-angle miscalibration sweep",
        angle_fig,
    )
    crossing_rows.append(_crossing_row("bob_angle_miscalibration", angle, "angle_offset"))

    readout_path = data_dir / "readout_confusion_example.json"
    readout_payload = {
        "description": "Columns are true bit values and rows are reported bit values.",
        "symmetric_error_probability": 0.05,
        "matrix": binary_confusion_matrix(0.05).tolist(),
    }
    readout_path.write_text(json.dumps(readout_payload, indent=2) + "\n", encoding="utf-8")

    crossings = pd.DataFrame(crossing_rows)
    crossings_path = data_dir / "noise_crossings.csv"
    crossings.to_csv(crossings_path, index=False)

    for path in (
        feedforward_csv,
        feedforward_fig,
        readout_csv,
        readout_fig,
        dephasing_csv,
        dephasing_fig,
        depolarizing_csv,
        depolarizing_fig,
        damping_csv,
        damping_fig,
        angle_csv,
        angle_fig,
        crossings_path,
    ):
        print(f"wrote {path}")
    print(f"wrote {readout_path}")


def _write_sweep(data: pd.DataFrame, path: Path) -> None:
    data.to_csv(path, index=False)


def _crossing_row(name: str, data: pd.DataFrame, x_column: str) -> dict[str, float | str]:
    ordered = data.sort_values(x_column)
    nonpositive = ordered.loc[ordered["E_B"] <= 0.0]
    first_nonpositive = (
        float(nonpositive[x_column].iloc[0]) if not nonpositive.empty else float("nan")
    )
    return {
        "sweep": name,
        "x_column": x_column,
        "first_sampled_nonpositive_x": first_nonpositive,
        "max_E_B": float(ordered["E_B"].max()),
        "min_E_B": float(ordered["E_B"].min()),
    }


if __name__ == "__main__":
    main()
