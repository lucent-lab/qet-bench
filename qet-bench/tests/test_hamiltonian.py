import numpy as np

from qet_bench.exact import ground_state
from qet_bench.hamiltonians import qet_hamiltonians


def test_ground_energy_is_zero() -> None:
    ops = qet_hamiltonians(h=1.0, k=0.5)
    ket = ground_state(h=1.0, k=0.5)
    rho = np.outer(ket, ket.conj())
    energy = np.trace(rho @ ops["Htot"])
    assert abs(float(np.real(energy))) < 1.0e-12


def test_hamiltonian_validates_parameters() -> None:
    for h, k in [(0.0, 0.5), (1.0, -0.1)]:
        try:
            qet_hamiltonians(h=h, k=k)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid parameters should raise ValueError")

