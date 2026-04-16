"""Simple channel and classical readout-noise helpers."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from qet_bench.pauli import I2, X, Y, Z, kron

ComplexArray = NDArray[np.complex128]
FloatArray = NDArray[np.float64]


def apply_channel(rho: ComplexArray, kraus_ops: Sequence[ComplexArray]) -> ComplexArray:
    """Apply a Kraus channel to a density matrix."""
    if not kraus_ops:
        raise ValueError("at least one Kraus operator is required")
    out = np.zeros_like(rho, dtype=np.complex128)
    for kraus in kraus_ops:
        if kraus.shape[1] != rho.shape[0] or kraus.shape[0] != rho.shape[0]:
            raise ValueError("Kraus operator shape must match rho")
        out += kraus @ rho @ kraus.conj().T
    return out


def dephasing_channel(p: float) -> list[ComplexArray]:
    """Return one-qubit phase-flip Kraus operators with probability ``p``."""
    _validate_probability(p, "p")
    return [np.sqrt(1.0 - p) * I2, np.sqrt(p) * Z]


def depolarizing_channel(p: float) -> list[ComplexArray]:
    """Return one-qubit depolarizing Kraus operators with total error ``p``."""
    _validate_probability(p, "p")
    return [
        np.sqrt(1.0 - p) * I2,
        np.sqrt(p / 3.0) * X,
        np.sqrt(p / 3.0) * Y,
        np.sqrt(p / 3.0) * Z,
    ]


def amplitude_damping_channel(gamma: float) -> list[ComplexArray]:
    """Return one-qubit amplitude-damping Kraus operators."""
    _validate_probability(gamma, "gamma")
    k0 = np.array([[1.0, 0.0], [0.0, np.sqrt(1.0 - gamma)]], dtype=np.complex128)
    k1 = np.array([[0.0, np.sqrt(gamma)], [0.0, 0.0]], dtype=np.complex128)
    return [k0, k1]


def lift_to_two_qubits(kraus_ops: Sequence[ComplexArray], qubit: int) -> list[ComplexArray]:
    """Lift one-qubit Kraus operators to the two-qubit Hilbert space.

    Qubit ``0`` is Alice, the left tensor factor; qubit ``1`` is Bob, the
    right tensor factor.
    """
    if qubit not in (0, 1):
        raise ValueError("qubit must be 0 or 1")
    lifted: list[ComplexArray] = []
    for kraus in kraus_ops:
        if kraus.shape != (2, 2):
            raise ValueError("each Kraus operator must be 2x2")
        lifted.append(kron(kraus, I2) if qubit == 0 else kron(I2, kraus))
    return lifted


def binary_confusion_matrix(p01: float, p10: float | None = None) -> FloatArray:
    """Return a 2x2 classical readout confusion matrix.

    Columns are the true bit value and rows are the reported bit value:
    ``matrix[reported, true]``. ``p01`` is ``P(report 1 | true 0)`` and
    ``p10`` is ``P(report 0 | true 1)``. If ``p10`` is omitted, a symmetric
    readout error model is used.
    """
    if p10 is None:
        p10 = p01
    _validate_probability(p01, "p01")
    _validate_probability(p10, "p10")
    return np.array([[1.0 - p01, p10], [p01, 1.0 - p10]], dtype=np.float64)


def apply_binary_confusion(probabilities: Sequence[float], confusion: FloatArray) -> FloatArray:
    """Apply a 2x2 readout confusion matrix to a binary probability vector."""
    probs = np.asarray(probabilities, dtype=np.float64)
    if probs.shape != (2,):
        raise ValueError("probabilities must have shape (2,)")
    if confusion.shape != (2, 2):
        raise ValueError("confusion must have shape (2, 2)")
    return confusion @ probs


def _validate_probability(value: float, name: str) -> None:
    if value < 0.0 or value > 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
