from qet_bench.exact import qet_ledger


def test_primary_exact_benchmark() -> None:
    ledger = qet_ledger(h=1.0, k=0.5)
    expected = {
        "E_A": 0.8944271909999154,
        "H1": 0.1873204098133684,
        "V": -0.2598931856865897,
        "E1": -0.0725727758732213,
        "E_B": 0.0725727758732213,
    }
    for key, value in expected.items():
        assert abs(ledger[key] - value) < 1.0e-9


def test_secondary_exact_benchmark() -> None:
    ledger = qet_ledger(h=1.0, k=1.0)
    expected = {
        "E_A": 0.7071067811865467,
        "H1": 0.2598931856865898,
        "V": -0.3746408196267373,
        "E1": -0.1147476339401475,
        "E_B": 0.1147476339401475,
    }
    for key, value in expected.items():
        assert abs(ledger[key] - value) < 1.0e-9


def test_final_trace_is_one() -> None:
    ledger = qet_ledger(h=1.0, k=0.5)
    assert abs(ledger["trace_final"] - 1.0) < 1.0e-12

