import numpy as np

from qet_bench.pauli import I2, X, Z, kron, lift_one_qubit


def test_kron_matches_numpy() -> None:
    assert np.allclose(kron(X, Z), np.kron(X, Z))


def test_lift_one_qubit_ordering() -> None:
    assert np.allclose(lift_one_qubit(X, 0), np.kron(X, I2))
    assert np.allclose(lift_one_qubit(Z, 1), np.kron(I2, Z))

