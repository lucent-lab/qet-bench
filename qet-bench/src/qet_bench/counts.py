"""Energy estimators from simple two-qubit count dictionaries."""

from __future__ import annotations

import numpy as np

Counts = dict[str, int]


def z1_expect_from_counts(counts: Counts) -> float:
    """Estimate ``<Z1>`` from counts in the computational basis.

    Count keys must be two-character bitstrings in ``q0q1`` order: Alice is
    the left bit and Bob is the right bit. Bob bit ``0`` contributes ``+1`` and
    Bob bit ``1`` contributes ``-1``.
    """
    total = _shots(counts)
    value = 0.0
    for bitstring, count in counts.items():
        bits = _clean_bitstring(bitstring)
        value += (1.0 if bits[1] == "0" else -1.0) * count
    return value / total


def x0x1_expect_from_counts(counts: Counts) -> float:
    """Estimate ``<X0 X1>`` from counts measured in the X basis.

    The same ``q0q1`` bit ordering is used after the basis rotation. A measured
    bit ``0`` denotes the ``+1`` eigenvalue and bit ``1`` denotes ``-1``.
    Therefore equal bits contribute ``+1`` and unequal bits contribute ``-1``.
    """
    total = _shots(counts)
    value = 0.0
    for bitstring, count in counts.items():
        bits = _clean_bitstring(bitstring)
        parity = 1.0 if bits[0] == bits[1] else -1.0
        value += parity * count
    return value / total


def local_energies_from_counts(
    counts_z1: Counts,
    counts_xx: Counts,
    h: float,
    k: float,
) -> dict[str, float]:
    """Estimate ``H1``, ``V``, ``E1``, and ``E_B`` from independent circuits."""
    if h <= 0:
        raise ValueError("h must be positive")
    if k < 0:
        raise ValueError("k must be nonnegative")
    s = float(np.sqrt(h * h + k * k))
    z1 = z1_expect_from_counts(counts_z1)
    x0x1 = x0x1_expect_from_counts(counts_xx)
    h1 = h * z1 + h * h / s
    v = 2.0 * k * x0x1 + 2.0 * k * k / s
    e1 = h1 + v
    return {
        "Z1": z1,
        "X0X1": x0x1,
        "H1": h1,
        "V": v,
        "E1": e1,
        "E_B": -e1,
        "shots_z1": float(_shots(counts_z1)),
        "shots_xx": float(_shots(counts_xx)),
    }


def _shots(counts: Counts) -> int:
    total = sum(counts.values())
    if total <= 0:
        raise ValueError("counts must contain at least one shot")
    return total


def _clean_bitstring(bitstring: str) -> str:
    bits = bitstring.replace(" ", "")
    if len(bits) != 2 or any(bit not in "01" for bit in bits):
        raise ValueError("count keys must be two-character bitstrings")
    return bits

