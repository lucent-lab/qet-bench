import numpy as np

from qet_bench.exact import qet_ledger, qet_ledger_with_noise
from qet_bench.noise import dephasing_channel, lift_to_two_qubits
from qet_bench.null_tests import wrong_angle_scan
from qet_bench.sweeps import (
    sweep_amplitude_damping,
    sweep_bob_angle_miscalibration,
    sweep_dephasing,
    sweep_depolarizing,
    sweep_readout_error,
)


def test_noise_free_noisy_ledger_matches_exact_ledger() -> None:
    exact = qet_ledger(h=1.0, k=0.5)
    noisy_path = qet_ledger_with_noise(
        h=1.0,
        k=0.5,
        pre_bob_kraus_ops=lift_to_two_qubits(dephasing_channel(0.0), qubit=1),
    )
    assert abs(noisy_path["E_B"] - exact["E_B"]) < 1.0e-12
    assert abs(noisy_path["noise_energy_delta"]) < 1.0e-12


def test_wrong_angle_scan_finds_optimum_near_benchmark_angle() -> None:
    data = wrong_angle_scan(h=1.0, k=0.5)
    best = data.loc[data["E_B"].idxmax()]
    assert abs(best["phi"] - best["phi_optimal"]) < 1.0e-12


def test_noise_sweeps_emit_expected_columns() -> None:
    strengths = np.array([0.0, 0.25])
    for data in (
        sweep_readout_error(strengths),
        sweep_dephasing(strengths),
        sweep_depolarizing(strengths),
        sweep_amplitude_damping(strengths),
        sweep_bob_angle_miscalibration(strengths),
    ):
        assert "E_B" in data.columns
        assert len(data) == 2
