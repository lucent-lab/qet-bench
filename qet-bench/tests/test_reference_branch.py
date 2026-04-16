from qet_bench.exact import qet_ledger
from qet_bench.reference_branch import (
    apply_x0_projector,
    expect_x0x1,
    expect_z0,
    expect_z1,
    norm,
    reference_branch_audit,
    reference_ground_state,
    reference_qet_ledger,
)


def test_reference_primary_benchmark() -> None:
    ledger = reference_qet_ledger(h=1.0, k=0.5)
    expected = {
        "E_A": 0.8944271909999154,
        "H1": 0.1873204098133684,
        "V": -0.2598931856865897,
        "E1": -0.0725727758732213,
        "E_B": 0.0725727758732213,
    }
    for key, value in expected.items():
        assert abs(ledger[key] - value) < 1.0e-9


def test_reference_secondary_benchmark() -> None:
    ledger = reference_qet_ledger(h=1.0, k=1.0)
    expected = {
        "E_A": 0.7071067811865467,
        "H1": 0.2598931856865898,
        "V": -0.3746408196267373,
        "E1": -0.1147476339401475,
        "E_B": 0.1147476339401475,
    }
    for key, value in expected.items():
        assert abs(ledger[key] - value) < 1.0e-9


def test_reference_branches_are_not_postselected() -> None:
    state = reference_ground_state(h=1.0, k=0.5)
    branches = [apply_x0_projector(state, mu) for mu in (-1, 1)]
    assert all(norm(branch) > 0.0 for branch in branches)
    assert abs(sum(norm(branch) for branch in branches) - 1.0) < 1.0e-12


def test_reference_trace_and_k_zero() -> None:
    assert abs(reference_qet_ledger(h=1.0, k=0.5)["trace_final"] - 1.0) < 1.0e-12
    assert abs(reference_qet_ledger(h=1.0, k=0.0)["E_B"]) < 1.0e-12


def test_reference_matches_production_for_benchmarks() -> None:
    for h, k in ((1.0, 0.5), (1.0, 1.0)):
        exact = qet_ledger(h=h, k=k)
        reference = reference_qet_ledger(h=h, k=k)
        for key in ("E_A", "H1", "V", "E1", "E_B", "trace_final"):
            assert abs(reference[key] - exact[key]) < 1.0e-12


def test_reference_bit_ordering_observables() -> None:
    assert expect_z0((1.0 + 0.0j, 0.0j, 0.0j, 0.0j)) == 1.0
    assert expect_z1((0.0j, 1.0 + 0.0j, 0.0j, 0.0j)) == -1.0
    assert expect_x0x1((1.0 + 0.0j, 0.0j, 0.0j, 1.0 + 0.0j)) == 2.0


def test_reference_branch_audit_sums_to_ledger() -> None:
    audit = reference_branch_audit(h=1.0, k=0.5)
    ledger = reference_qet_ledger(h=1.0, k=0.5)
    assert len(audit) == 2
    assert abs(sum(row["branch_weight"] for row in audit) - 1.0) < 1.0e-12
    assert abs(sum(row["branch_energy_after_alice"] for row in audit) - ledger["E_A"]) < 1.0e-12
    assert abs(sum(row["branch_e1_after_bob"] for row in audit) - ledger["E1"]) < 1.0e-12

