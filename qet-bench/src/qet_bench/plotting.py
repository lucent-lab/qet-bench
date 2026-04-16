"""Matplotlib figure helpers for qet-bench."""

from __future__ import annotations

import math
from collections.abc import Mapping
from pathlib import Path

import matplotlib

matplotlib.use("Agg", force=True)

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

_SURVIVAL_LABELS = {
    "feedforward_error": "feedforward",
    "alice_bit_readout_error": "readout",
    "bob_dephasing": "dephasing",
    "bob_depolarizing": "depolarizing",
    "bob_amplitude_damping": "amplitude damping",
}


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
    if "anchor_label" in data.columns:
        return _plot_survival_summary_by_anchor(data, output_path)

    labels = [_survival_display_label(value) for value in data["survival_model"]]
    fig_width = max(8.0, 0.45 * len(labels))
    fig, ax = plt.subplots(figsize=(fig_width, 4.0), dpi=150)
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


def _plot_survival_summary_by_anchor(
    data: pd.DataFrame,
    output_path: str | Path | None = None,
) -> Figure:
    anchors = data[["anchor_index", "anchor_label", "h", "k"]].drop_duplicates()
    anchors = anchors.sort_values("anchor_index")
    n_panels = len(anchors)
    n_cols = 2 if n_panels > 1 else 1
    n_rows = math.ceil(n_panels / n_cols)
    fig, _axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(6.2 * n_cols, 3.5 * n_rows),
        dpi=150,
        sharey=True,
    )
    axes = fig.axes
    width = 0.36
    for axis, (_row_index, anchor) in zip(axes, anchors.iterrows(), strict=False):
        anchor_data = data[data["anchor_label"] == anchor["anchor_label"]]
        labels = [_survival_display_label(value) for value in anchor_data["survival_model"]]
        x_positions = list(range(len(labels)))
        axis.bar(
            [x - width / 2.0 for x in x_positions],
            anchor_data["lambda_ratio_cutoff"].astype(float),
            width=width,
            label="R=0.5 crossing",
        )
        axis.bar(
            [x + width / 2.0 for x in x_positions],
            anchor_data["lambda_zero_crossing"].astype(float),
            width=width,
            label="E_B=0 crossing",
        )
        axis.set_xticks(x_positions, labels, rotation=20, ha="right")
        axis.set_title(f"h={float(anchor['h']):g}, k={float(anchor['k']):g}")
        axis.grid(True, axis="y", alpha=0.3)
    for axis in axes[n_panels:]:
        axis.set_visible(False)
    for row_start in range(0, n_panels, n_cols):
        axes[row_start].set_ylabel("scan coordinate")
    axes[0].legend(fontsize="small")
    _save(fig, output_path)
    return fig


def plot_survival_curves_by_anchor(
    data: pd.DataFrame,
    output_path: str | Path | None = None,
) -> Figure:
    """Plot fixed-protocol survival-ratio curves as one panel per anchor."""
    if data.empty:
        raise ValueError("data must not be empty")
    required = {
        "anchor_index",
        "anchor_label",
        "survival_model",
        "scan_coordinate",
        "survival_ratio",
        "h",
        "k",
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"missing survival curve columns: {sorted(missing)}")

    anchors = data[["anchor_index", "anchor_label", "h", "k"]].drop_duplicates()
    anchors = anchors.sort_values("anchor_index")
    n_panels = len(anchors)
    n_cols = 2 if n_panels > 1 else 1
    n_rows = math.ceil(n_panels / n_cols)
    fig, _axes = plt.subplots(
        n_rows,
        n_cols,
        figsize=(6.0 * n_cols, 3.4 * n_rows),
        dpi=150,
        sharex=True,
        sharey=True,
    )
    axes = fig.axes
    for axis, (_row_index, anchor) in zip(axes, anchors.iterrows(), strict=False):
        anchor_data = data[data["anchor_label"] == anchor["anchor_label"]]
        for model_name, model_data in anchor_data.groupby("survival_model", sort=False):
            axis.plot(
                model_data["scan_coordinate"],
                model_data["survival_ratio"],
                marker="o",
                markersize=2.5,
                linewidth=1.0,
                label=_survival_display_label(model_name),
            )
        axis.axhline(0.0, linewidth=1.0)
        axis.axhline(0.5, linestyle="--", linewidth=1.0)
        axis.set_title(f"h={float(anchor['h']):g}, k={float(anchor['k']):g}")
        axis.grid(True, alpha=0.3)
    for axis in axes[n_panels:]:
        axis.set_visible(False)
    for axis in axes[-n_cols:]:
        axis.set_xlabel("scan coordinate")
    for row_start in range(0, n_panels, n_cols):
        axes[row_start].set_ylabel("R(lambda)")
    axes[0].legend(fontsize="small")
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


def _survival_display_label(value: object) -> str:
    text = str(value)
    return _SURVIVAL_LABELS.get(text, text.replace("_", " "))
