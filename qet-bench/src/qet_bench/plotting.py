"""Matplotlib figure helpers for qet-bench."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

import matplotlib

matplotlib.use("Agg", force=True)

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def plot_energy_ledger_vs_ratio(
    data: pd.DataFrame,
    output_path: str | Path | None = None,
) -> Figure:
    """Plot Alice input, Bob extraction, and the accounting gap versus ``h/k``."""
    fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=150)
    ax.plot(data["h_over_k"], data["E_A"], marker="o", label="E_A")
    ax.plot(data["h_over_k"], data["E_B"], marker="s", label="E_B")
    ax.plot(data["h_over_k"], data["E_A_minus_E_B"], marker="^", label="E_A - E_B")
    ax.set_xlabel("h/k")
    ax.set_ylabel("energy")
    ax.set_title("QET energy ledger")
    ax.legend()
    ax.grid(True, alpha=0.3)
    _save(fig, output_path)
    return fig


def plot_eb_vs_feedforward_error(
    data: pd.DataFrame,
    output_path: str | Path | None = None,
) -> Figure:
    """Plot Bob extraction versus classical feedforward sign-flip probability."""
    xcol = "feedforward_error_probability"
    fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=150)
    ax.plot(data[xcol], data["E_B"], marker="o", label="E_B")
    ax.axhline(0.0, linewidth=1.0)
    ax.set_xlabel("feedforward sign-flip probability q")
    ax.set_ylabel("E_B")
    ax.set_title("Feedforward-error sweep")
    ax.grid(True, alpha=0.3)
    ax.legend()
    _save(fig, output_path)
    return fig


def plot_eb_vs_column(
    data: pd.DataFrame,
    x_column: str,
    xlabel: str,
    title: str,
    output_path: str | Path | None = None,
) -> Figure:
    """Plot Bob extraction versus a scalar sweep column."""
    fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=150)
    ax.plot(data[x_column], data["E_B"], marker="o", label="E_B")
    ax.axhline(0.0, linewidth=1.0)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("E_B")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend()
    _save(fig, output_path)
    return fig


def plot_wrong_angle_scan(
    data: pd.DataFrame,
    output_path: str | Path | None = None,
) -> Figure:
    """Plot Bob extraction over candidate Bob rotation angles."""
    fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=150)
    ax.plot(data["phi"], data["E_B"], marker="o", label="E_B")
    ax.axhline(0.0, linewidth=1.0)
    ax.axvline(float(data["phi_optimal"].iloc[0]), linestyle="--", linewidth=1.0, label="optimal phi")
    ax.set_xlabel("Bob rotation angle phi")
    ax.set_ylabel("E_B")
    ax.set_title("Wrong-angle diagnostic")
    ax.grid(True, alpha=0.3)
    ax.legend()
    _save(fig, output_path)
    return fig


def plot_null_comparison(
    values: Mapping[str, float] | pd.DataFrame,
    output_path: str | Path | None = None,
) -> Figure:
    """Plot a bar-chart comparison of selected null-test ``E_B`` values."""
    if isinstance(values, pd.DataFrame):
        labels = values["label"].astype(str).tolist()
        heights = values["E_B"].astype(float).tolist()
    else:
        labels = list(values.keys())
        heights = [float(value) for value in values.values()]

    fig, ax = plt.subplots(figsize=(7.0, 4.0), dpi=150)
    ax.bar(labels, heights)
    ax.axhline(0.0, linewidth=1.0)
    ax.set_ylabel("E_B")
    ax.set_title("Null-test diagnostics")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    _save(fig, output_path)
    return fig


def plot_survival_summary(
    data: pd.DataFrame,
    output_path: str | Path | None = None,
) -> Figure:
    """Plot half-survival and zero-crossing estimates for survival diagnostics."""
    fig, ax = plt.subplots(figsize=(8.0, 4.0), dpi=150)
    labels = data["survival_model"].astype(str).tolist()
    x_positions = range(len(labels))
    width = 0.36
    ax.bar(
        [x - width / 2.0 for x in x_positions],
        data["lambda_ratio_cutoff"].astype(float),
        width=width,
        label="R=0.5 crossing",
    )
    ax.bar(
        [x + width / 2.0 for x in x_positions],
        data["lambda_zero_crossing"].astype(float),
        width=width,
        label="E_B=0 crossing",
    )
    ax.set_xticks(list(x_positions), labels, rotation=20, ha="right")
    ax.set_ylabel("scan coordinate")
    ax.set_title("Noise-survival diagnostics")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    _save(fig, output_path)
    return fig


def _save(fig: Figure, output_path: str | Path | None) -> None:
    if output_path is None:
        fig.tight_layout()
        return
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(path)
