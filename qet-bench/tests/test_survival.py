import math

import numpy as np

from qet_bench.plotting import plot_survival_curves_by_anchor
from qet_bench.survival import add_survival_columns, survival_atlas, survival_summary
from qet_bench.sweeps import sweep_feedforward_error


def test_survival_ratio_starts_at_one() -> None:
    data = sweep_feedforward_error([0.0, 0.5, 1.0])
    enriched = add_survival_columns(data, "feedforward_error_probability", "feedforward")
    assert abs(float(enriched["survival_ratio"].iloc[0]) - 1.0) < 1.0e-12
    assert bool(enriched["survives_positive"].iloc[0])


def test_survival_summary_reports_crossings() -> None:
    data = sweep_feedforward_error(np.linspace(0.0, 1.0, 101))
    summary = survival_summary(data, "feedforward_error_probability", "feedforward")
    assert summary["baseline_E_B"] > 0.0
    assert summary["min_survival_ratio"] < 0.0
    assert math.isfinite(float(summary["interval_mean_survival_ratio"]))
    assert 0.0 < summary["lambda_ratio_cutoff"] < 1.0
    assert 0.0 < summary["lambda_zero_crossing"] < 1.0


def test_survival_atlas_outputs_expected_models() -> None:
    anchors = [(1.0, 0.5), (1.0, 1.0)]
    curves, summary = survival_atlas([0.0, 0.5, 1.0], parameter_anchors=anchors)
    assert set(summary["survival_model"]) == {
        "feedforward_error",
        "alice_bit_readout_error",
        "bob_dephasing",
        "bob_depolarizing",
        "bob_amplitude_damping",
    }
    assert list(summary["anchor_label"].drop_duplicates()) == ["h1_k0p5", "h1_k1"]
    assert len(curves) == 30
    assert len(summary) == 10
    assert not any(math.isnan(value) for value in summary["baseline_E_B"])
    assert not any(math.isnan(value) for value in summary["interval_mean_survival_ratio"])

    grouped = curves.groupby(["anchor_label", "survival_model"], sort=False)
    for (_anchor_label, _model_name), group in grouped:
        assert abs(float(group["survival_ratio"].iloc[0]) - 1.0) < 1.0e-12
        assert bool(group["survives_positive"].iloc[0])


def test_survival_atlas_rejects_zero_coupling_anchor() -> None:
    with np.testing.assert_raises(ValueError):
        survival_atlas([0.0, 0.5], parameter_anchors=[(1.0, 0.0)])


def test_survival_atlas_plot_smoke(tmp_path) -> None:
    curves, _summary = survival_atlas(
        [0.0, 1.0],
        parameter_anchors=[(1.0, 0.5), (1.0, 1.0)],
    )
    output_path = tmp_path / "noise_survival_atlas.png"
    plot_survival_curves_by_anchor(curves, output_path)
    assert output_path.exists()
    assert output_path.stat().st_size > 0
