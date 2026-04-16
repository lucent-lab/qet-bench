from qet_bench.exact import qet_ledger


def test_scrambled_feedforward_reduces_or_reverses_extraction() -> None:
    clean = qet_ledger(h=1.0, k=0.5, feedforward_error_probability=0.0)
    scrambled = qet_ledger(h=1.0, k=0.5, feedforward_error_probability=0.5)
    assert scrambled["E_B"] <= clean["E_B"]
    assert scrambled["E_B"] <= 1.0e-12

