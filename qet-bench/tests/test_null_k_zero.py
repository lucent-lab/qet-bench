from qet_bench.exact import qet_ledger
from qet_bench.null_tests import k_zero_scan


def test_extraction_vanishes_at_k_zero() -> None:
    ledger = qet_ledger(h=1.0, k=0.0)
    assert abs(ledger["E_B"]) < 1.0e-12


def test_k_zero_scan_contains_zero_coupling() -> None:
    data = k_zero_scan(h=1.0, ks=[0.0, 1.0e-6])
    first = data.sort_values("k").iloc[0]
    assert first["k"] == 0.0
    assert abs(first["E_B"]) < 1.0e-12

