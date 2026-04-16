"""Uncertainty estimates for Pauli-count energy estimators."""

from __future__ import annotations

import numpy as np


def pauli_standard_error(mean: float, shots: int) -> float:
    """Return the standard error of a Pauli mean estimated from ``shots``."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    variance = max(0.0, 1.0 - mean * mean)
    return float(np.sqrt(variance / shots))


def eb_standard_error_from_counts(
    z1_mean: float,
    x0x1_mean: float,
    z1_shots: int,
    x0x1_shots: int,
    h: float,
    k: float,
) -> float:
    """Propagate independent ``Z1`` and ``X0X1`` circuit errors to ``E_B``."""
    if h <= 0:
        raise ValueError("h must be positive")
    if k < 0:
        raise ValueError("k must be nonnegative")
    z1_se = pauli_standard_error(z1_mean, z1_shots)
    xx_se = pauli_standard_error(x0x1_mean, x0x1_shots)
    variance = (h * z1_se) ** 2 + (2.0 * k * xx_se) ** 2
    return float(np.sqrt(variance))

