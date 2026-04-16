"""Null and diagnostic scans for the two-qubit QET benchmark."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd

from qet_bench.exact import _density, _expectation, _qet_ledger_with_phi, bob_angle, ground_state, qet_ledger
from qet_bench.hamiltonians import qet_hamiltonians
from qet_bench.pauli import I2, X, Y, Z, kron


def k_zero_scan(h: float = 1.0, ks: Iterable[float] | None = None) -> pd.DataFrame:
    """Scan small couplings and show that Bob extraction vanishes at ``k=0``."""
    if ks is None:
        ks = [0.0, 1.0e-8, 1.0e-6, 1.0e-4, 1.0e-2]
    rows: list[dict[str, float]] = []
    for k in ks:
        row = {"h": float(h), "k": float(k)}
        row.update(qet_ledger(h=h, k=float(k)))
        rows.append(row)
    return pd.DataFrame(rows)


def scrambled_bit_scan(
    h: float = 1.0,
    k: float = 0.5,
    qs: Iterable[float] | None = None,
) -> pd.DataFrame:
    """Scan feedforward sign-flip probability for the classical bit channel."""
    if qs is None:
        qs = np.linspace(0.0, 1.0, 21)
    rows: list[dict[str, float]] = []
    for q in qs:
        row = {
            "h": float(h),
            "k": float(k),
            "feedforward_error_probability": float(q),
        }
        row.update(qet_ledger(h=h, k=k, feedforward_error_probability=float(q)))
        rows.append(row)
    return pd.DataFrame(rows)


def product_state_null(h: float = 1.0, k: float = 0.5) -> dict[str, float | str]:
    """Run the protocol from ``|00>`` as a non-ground-state diagnostic.

    This is not a theorem about product states: ``|00>`` is an excited product
    reference for this Hamiltonian, so any local energy decrease is not QET
    from ground-state correlations. The diagnostic is included to keep that
    distinction explicit.
    """
    ledger = qet_ledger(h=h, k=k, initial_state="product_00")
    return {
        "initial_state": "product_00",
        "diagnostic": "excited product reference, not ground-state-correlation extraction",
        **ledger,
    }


def wrong_angle_scan(
    h: float = 1.0,
    k: float = 0.5,
    phis: Iterable[float] | None = None,
) -> pd.DataFrame:
    """Evaluate Bob extraction over user-supplied or default rotation angles."""
    optimal = bob_angle(h, k)
    if phis is None:
        if abs(optimal) < 1.0e-12:
            phis = np.linspace(-0.5, 0.5, 81)
        else:
            phis = np.linspace(-2.0 * optimal, 2.0 * optimal, 81)
    rows: list[dict[str, float]] = []
    for phi in phis:
        row = {"h": float(h), "k": float(k), "phi": float(phi), "phi_optimal": optimal}
        row.update(_qet_ledger_with_phi(h=h, k=k, phi=float(phi)))
        rows.append(row)
    return pd.DataFrame(rows)


def random_bob_only_unitary_scan(
    h: float = 1.0,
    k: float = 0.5,
    n: int = 1000,
    seed: int = 0,
) -> pd.DataFrame:
    """Sample random Bob-only unitaries without Alice measurement.

    The scan is a finite diagnostic, not a proof over all Bob controls. It is
    useful for checking that the implementation does not report QET-like
    extraction when the Alice measurement and feedforward channel are removed.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    rng = np.random.default_rng(seed)
    ops = qet_hamiltonians(h, k)
    h1_plus_v = ops["H1"] + ops["V"]  # type: ignore[operator]
    rho0 = _density(ground_state(h, k))

    rows: list[dict[str, float]] = []
    for _ in range(n):
        axis = rng.normal(size=3)
        axis = axis / np.linalg.norm(axis)
        angle = float(rng.uniform(0.0, 2.0 * np.pi))
        generator = axis[0] * X + axis[1] * Y + axis[2] * Z
        u1 = np.cos(angle / 2.0) * I2 - 1j * np.sin(angle / 2.0) * generator
        unitary = kron(I2, u1)
        rho = unitary @ rho0 @ unitary.conj().T
        e1 = _expectation(rho, h1_plus_v)
        rows.append(
            {
                "angle": angle,
                "axis_x": float(axis[0]),
                "axis_y": float(axis[1]),
                "axis_z": float(axis[2]),
                "E1": e1,
                "E_B": -e1,
            }
        )

    frame = pd.DataFrame(rows)
    frame.attrs["limitation"] = "finite random diagnostic, not an exhaustive theorem"
    return frame

