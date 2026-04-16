import pytest

from qet_bench.counts import local_energies_from_counts
from qet_bench.qiskit_bridge import (
    build_branch_circuit,
    canonicalize_counts_q0q1,
    is_qiskit_aer_available,
    is_qiskit_available,
    ledger_from_qiskit_counts,
    run_aer_branches,
)


def test_qiskit_bridge_imports_without_qiskit_dependency() -> None:
    assert isinstance(is_qiskit_available(), bool)
    assert isinstance(is_qiskit_aer_available(), bool)


def test_canonicalize_counts_reverses_qiskit_order() -> None:
    counts = canonicalize_counts_q0q1({"01": 3, "10": 1, "1 1": 2})
    assert counts == {"10": 3.0, "01": 1.0, "11": 2.0}


def test_canonicalize_counts_can_accept_canonical_order() -> None:
    counts = canonicalize_counts_q0q1({"01": 3, "10": 1}, source_order="q0q1")
    assert counts == {"01": 3.0, "10": 1.0}


def test_ledger_from_fake_qiskit_counts_matches_count_estimators() -> None:
    expected = local_energies_from_counts(
        counts_z1={"00": 75, "01": 25},
        counts_xx={"00": 40, "11": 40, "01": 10, "10": 10},
        h=1.0,
        k=0.5,
    )
    estimated = ledger_from_qiskit_counts(
        counts_z1={"00": 75, "10": 25},
        counts_xx={"00": 40, "11": 40, "10": 10, "01": 10},
        h=1.0,
        k=0.5,
    )
    assert estimated == expected


def test_qiskit_only_builder_has_helpful_guard_without_qiskit() -> None:
    if is_qiskit_available():
        pytest.skip("Qiskit is installed in this environment")
    with pytest.raises(RuntimeError, match="Qiskit is optional"):
        build_branch_circuit(h=1.0, k=0.5, mu=1)


def test_aer_runner_has_helpful_guard_without_aer() -> None:
    if is_qiskit_aer_available():
        pytest.skip("Qiskit Aer is installed in this environment")
    with pytest.raises(RuntimeError, match="Qiskit"):
        run_aer_branches(h=1.0, k=0.5, shots=16)


@pytest.mark.skipif(not is_qiskit_aer_available(), reason="Qiskit Aer is optional")
def test_aer_runner_smoke_matches_exact_scale() -> None:
    ledger = run_aer_branches(h=1.0, k=0.5, shots=4096, seed=0)
    assert ledger["absolute_E_B_error"] < 0.05
