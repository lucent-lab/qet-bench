"""Pauli matrices and small tensor-product helpers for two-qubit QET."""

from __future__ import annotations

from functools import reduce

import numpy as np
from numpy.typing import NDArray

ComplexArray = NDArray[np.complex128]

I2: ComplexArray = np.eye(2, dtype=np.complex128)
X: ComplexArray = np.array([[0, 1], [1, 0]], dtype=np.complex128)
Y: ComplexArray = np.array([[0, -1j], [1j, 0]], dtype=np.complex128)
Z: ComplexArray = np.array([[1, 0], [0, -1]], dtype=np.complex128)


def kron(*operators: ComplexArray) -> ComplexArray:
    """Return the Kronecker product of the supplied operators in order."""
    if not operators:
        raise ValueError("at least one operator is required")
    return reduce(np.kron, operators).astype(np.complex128, copy=False)


def lift_one_qubit(
    operator: ComplexArray,
    qubit: int,
    n_qubits: int = 2,
) -> ComplexArray:
    """Lift a one-qubit operator to an ``n_qubits`` Hilbert space.

    Qubit index ``0`` is the leftmost tensor factor. For this project, qubit
    ``0`` is Alice and qubit ``1`` is Bob, so ``lift_one_qubit(X, 0)`` returns
    ``X tensor I`` and ``lift_one_qubit(X, 1)`` returns ``I tensor X``.
    """
    if operator.shape != (2, 2):
        raise ValueError("operator must be a 2x2 matrix")
    if n_qubits < 1:
        raise ValueError("n_qubits must be positive")
    if qubit < 0 or qubit >= n_qubits:
        raise ValueError("qubit index is out of range")

    factors = [I2] * n_qubits
    factors[qubit] = operator
    return kron(*factors)

