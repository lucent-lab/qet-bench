from qet_bench.counts import local_energies_from_counts, x0x1_expect_from_counts, z1_expect_from_counts


def test_z1_count_bit_ordering_q0q1() -> None:
    assert z1_expect_from_counts({"10": 5}) == 1.0
    assert z1_expect_from_counts({"01": 5}) == -1.0
    assert z1_expect_from_counts({"00": 75, "01": 25}) == 0.5


def test_x0x1_count_parity() -> None:
    counts = {"00": 40, "11": 40, "01": 10, "10": 10}
    assert x0x1_expect_from_counts(counts) == 0.6


def test_local_energies_from_counts() -> None:
    energies = local_energies_from_counts(
        counts_z1={"00": 75, "01": 25},
        counts_xx={"00": 40, "11": 40, "01": 10, "10": 10},
        h=1.0,
        k=0.5,
    )
    assert energies["Z1"] == 0.5
    assert energies["X0X1"] == 0.6
    assert energies["E_B"] == -energies["E1"]

