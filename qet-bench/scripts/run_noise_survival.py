#!/usr/bin/env python3
"""Generate fixed-protocol noise-survival diagnostics."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from qet_bench.plotting import plot_survival_curves_by_anchor, plot_survival_summary
from qet_bench.survival import DEFAULT_SURVIVAL_ANCHORS, survival_atlas


def main() -> None:
    """Save survival curves, summary metrics, and summary figure."""
    data_dir = ROOT / "results" / "data"
    fig_dir = ROOT / "results" / "figures"
    data_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    strengths = np.linspace(0.0, 1.0, 101)
    curves, summary = survival_atlas(
        strengths,
        ratio_cutoff=0.5,
        parameter_anchors=DEFAULT_SURVIVAL_ANCHORS,
    )

    curves_path = data_dir / "noise_survival_curves.csv"
    summary_path = data_dir / "noise_survival_summary.csv"
    json_path = data_dir / "noise_survival_summary.json"
    fig_path = fig_dir / "noise_survival_summary.png"
    atlas_fig_path = fig_dir / "noise_survival_atlas.png"

    curves.to_csv(curves_path, index=False)
    summary.to_csv(summary_path, index=False)
    json_path.write_text(
        json.dumps(summary.to_dict(orient="records"), indent=2) + "\n",
        encoding="utf-8",
    )
    plot_survival_summary(summary, fig_path)
    plot_survival_curves_by_anchor(curves, atlas_fig_path)

    print(f"wrote {curves_path}")
    print(f"wrote {summary_path}")
    print(f"wrote {json_path}")
    print(f"wrote {fig_path}")
    print(f"wrote {atlas_fig_path}")


if __name__ == "__main__":
    main()
