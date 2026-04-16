"""Noise-survival metrics for fixed-protocol two-qubit QET sweeps."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from qet_bench.sweeps import (
    sweep_amplitude_damping,
    sweep_dephasing,
    sweep_depolarizing,
    sweep_feedforward_error,
    sweep_readout_error,
)


def add_survival_columns(
    data: pd.DataFrame,
    x_column: str,
    model_name: str,
    accounting_tolerance: float = 1.0e-10,
) -> pd.DataFrame:
    """Add survival diagnostics to one fixed-protocol sweep.

    ``survival_ratio`` is ``E_B(lambda) / E_B(0)``. A sampled point is marked as
    ``survives_positive`` only when Bob extraction is positive and the reported
    model accounting gap is nonnegative within ``accounting_tolerance``.
    """
    if data.empty:
        raise ValueError("data must not be empty")
    if x_column not in data.columns:
        raise ValueError(f"missing x_column: {x_column}")

    ordered = data.sort_values(x_column).reset_index(drop=True).copy()
    baseline = float(ordered["E_B"].iloc[0])
    if baseline <= 0.0:
        raise ValueError("baseline E_B must be positive")

    ordered["survival_model"] = model_name
    ordered["survival_x_column"] = x_column
    ordered["survival_ratio"] = ordered["E_B"] / baseline
    ordered["survives_positive"] = (ordered["E_B"] > 0.0) & (
        ordered["E_A_minus_E_B"] >= -accounting_tolerance
    )
    ordered["survives_half"] = ordered["survives_positive"] & (
        ordered["survival_ratio"] >= 0.5
    )
    return ordered


def survival_summary(
    data: pd.DataFrame,
    x_column: str,
    model_name: str,
    ratio_cutoff: float = 0.5,
) -> dict[str, float | str]:
    """Return compact sampled/interpolated survival metrics for one sweep."""
    if ratio_cutoff <= 0.0:
        raise ValueError("ratio_cutoff must be positive")
    enriched = add_survival_columns(data, x_column=x_column, model_name=model_name)
    x = enriched[x_column].astype(float).to_numpy()
    eb = enriched["E_B"].astype(float).to_numpy()
    ratio = enriched["survival_ratio"].astype(float).to_numpy()

    first_nonpositive = enriched.loc[enriched["E_B"] <= 0.0]
    first_sampled_nonpositive = (
        float(first_nonpositive[x_column].iloc[0]) if not first_nonpositive.empty else float("nan")
    )

    return {
        "survival_model": model_name,
        "x_column": x_column,
        "x_min": float(x.min()),
        "x_max": float(x.max()),
        "baseline_E_B": float(eb[0]),
        "min_E_B": float(eb.min()),
        "min_survival_ratio": float(ratio.min()),
        "lambda_ratio_cutoff": _first_crossing(x, ratio, ratio_cutoff),
        "lambda_zero_crossing": _first_crossing(x, eb, 0.0),
        "first_sampled_nonpositive_x": first_sampled_nonpositive,
        "ratio_cutoff": float(ratio_cutoff),
    }


def survival_atlas(
    strengths: Iterable[float],
    h: float = 1.0,
    k: float = 0.5,
    ratio_cutoff: float = 0.5,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return survival curves and summaries for the release channel families."""
    sweep_specs = [
        (
            "feedforward_error",
            "feedforward_error_probability",
            sweep_feedforward_error(strengths, h=h, k=k),
        ),
        (
            "alice_bit_readout_error",
            "readout_error_probability",
            sweep_readout_error(strengths, h=h, k=k),
        ),
        ("bob_dephasing", "noise_strength", sweep_dephasing(strengths, h=h, k=k, qubit=1)),
        (
            "bob_depolarizing",
            "noise_strength",
            sweep_depolarizing(strengths, h=h, k=k, qubit=1),
        ),
        (
            "bob_amplitude_damping",
            "noise_strength",
            sweep_amplitude_damping(strengths, h=h, k=k, qubit=1),
        ),
    ]

    curves: list[pd.DataFrame] = []
    summaries: list[dict[str, float | str]] = []
    for model_name, x_column, data in sweep_specs:
        enriched = add_survival_columns(data, x_column=x_column, model_name=model_name)
        curves.append(enriched)
        summaries.append(
            survival_summary(
                data,
                x_column=x_column,
                model_name=model_name,
                ratio_cutoff=ratio_cutoff,
            )
        )
    return pd.concat(curves, ignore_index=True), pd.DataFrame(summaries)


def _first_crossing(x: np.ndarray, y: np.ndarray, target: float) -> float:
    """Return the first linearly interpolated ``x`` where ``y <= target``."""
    if y[0] <= target:
        return float(x[0])
    for index in range(1, len(y)):
        if y[index] <= target:
            x0 = float(x[index - 1])
            x1 = float(x[index])
            y0 = float(y[index - 1])
            y1 = float(y[index])
            if y1 == y0:
                return x1
            fraction = (target - y0) / (y1 - y0)
            return x0 + fraction * (x1 - x0)
    return float("nan")

