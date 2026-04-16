from qet_bench.exact import qet_ledger


def test_ground_state_global_accounting_nonnegative() -> None:
    for h, k in [(1.0, 0.0), (1.0, 0.5), (1.0, 1.0), (2.0, 0.75)]:
        ledger = qet_ledger(h=h, k=k)
        assert ledger["E_A_minus_E_B"] >= -1.0e-10

