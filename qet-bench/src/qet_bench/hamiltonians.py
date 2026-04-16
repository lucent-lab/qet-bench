"""Hamiltonian construction for the minimal two-qubit QET model."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray

from qet_bench.pauli import I2, X, Y, Z, kron, lift_one_qubit

ComplexArray = NDArray[np.complex128]
HamiltonianDict = dict[str, ComplexArray | float]


def qet_hamiltonians(h: float, k: float) -> HamiltonianDict:
    """Return Hamiltonian terms and common observables for the QET model.

    Parameters
    ----------
    h:
        Positive local field scale.
    k:
        Nonnegative two-qubit coupling scale.

    Returns
    -------
    dict
        Dictionary containing ``H0``, ``H1``, ``V``, ``Htot``, lifted Pauli
        observables, ``XX``, ``I4``, and ``s = sqrt(h**2 + k**2)``.
    """
    if h <= 0:
        raise ValueError("h must be positive")
    if k < 0:
        raise ValueError("k must be nonnegative")

    s = float(np.sqrt(h * h + k * k))
    i4 = kron(I2, I2)
    x0 = lift_one_qubit(X, 0)
    x1 = lift_one_qubit(X, 1)
    y1 = lift_one_qubit(Y, 1)
    z0 = lift_one_qubit(Z, 0)
    z1 = lift_one_qubit(Z, 1)
    xx = kron(X, X)

    h0 = h * z0 + (h * h / s) * i4
    h1 = h * z1 + (h * h / s) * i4
    v = 2.0 * k * xx + (2.0 * k * k / s) * i4
    htot = h0 + h1 + v

    return {
        "H0": h0,
        "H1": h1,
        "V": v,
        "Htot": htot,
        "X0": x0,
        "X1": x1,
        "Y1": y1,
        "Z0": z0,
        "Z1": z1,
        "XX": xx,
        "I4": i4,
        "s": s,
    }

