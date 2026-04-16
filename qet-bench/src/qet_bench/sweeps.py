"""Parameter sweeps for the exact two-qubit QET benchmark."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from qet_bench.exact import (
    _qet_ledger_with_phi,
    bob_angle,
    qet_ledger,
    qet_ledger_with_noise,
)
from qet_bench.noise import (
    amplitude_damping_channel,
    dephasing_channel,
    depolarizing_channel,
    lift_to_two_qubits,
)


def sweep_h_over_k(ratios: Iterable[float], k: float = 1.0) -> pd.DataFrame:
    """Sweep ``h/k`` at fixed positive ``k`` and return a data frame."""
    if k <= 0:
        raise ValueError("k must be positive for an h/k sweep")
    rows: list[dict[str, float]] = []
    for ratio in ratios:
        if ratio <= 0:
            raise ValueError("all h/k ratios must be positive")
        h = float(ratio) * k
        row = {"h_over_k": float(ratio), "h": h, "k": float(k)}
        row.update(qet_ledger(h=h, k=k))
        rows.append(row)
    return pd.DataFrame(rows)


def sweep_feedforward_error(
    qs: Iterable[float],
    h: float = 1.0,
    k: float = 0.5,
) -> pd.DataFrame:
    """Sweep classical feedforward sign-flip probability ``q``."""
    rows: list[dict[str, float]] = []
    for q in qs:
        row = {
            "feedforward_error_probability": float(q),
            "h": float(h),
            "k": float(k),
        }
        row.update(qet_ledger(h=h, k=k, feedforward_error_probability=float(q)))
        rows.append(row)
    return pd.DataFrame(rows)


def sweep_readout_error(
    ps: Iterable[float],
    h: float = 1.0,
    k: float = 0.5,
) -> pd.DataFrame:
    """Sweep symmetric Alice-bit readout confusion used for Bob feedforward."""
    rows: list[dict[str, float]] = []
    for p in ps:
        row = {
            "readout_error_probability": float(p),
            "h": float(h),
            "k": float(k),
        }
        row.update(qet_ledger(h=h, k=k, feedforward_error_probability=float(p)))
        rows.append(row)
    return pd.DataFrame(rows)


def sweep_bob_angle_miscalibration(
    offsets: Iterable[float],
    h: float = 1.0,
    k: float = 0.5,
) -> pd.DataFrame:
    """Sweep Bob rotation angle offsets around the exact optimum."""
    optimal = bob_angle(h, k)
    rows: list[dict[str, float]] = []
    for offset in offsets:
        phi = optimal + float(offset)
        row = {
            "angle_offset": float(offset),
            "phi": phi,
            "phi_optimal": optimal,
            "h": float(h),
            "k": float(k),
        }
        row.update(_qet_ledger_with_phi(h=h, k=k, phi=phi))
        rows.append(row)
    return pd.DataFrame(rows)


def sweep_dephasing(
    ps: Iterable[float],
    h: float = 1.0,
    k: float = 0.5,
    qubit: int = 1,
) -> pd.DataFrame:
    """Sweep a phase-flip channel applied after Alice and before Bob."""
    return _sweep_pre_bob_channel("dephasing", ps, h=h, k=k, qubit=qubit)


def sweep_depolarizing(
    ps: Iterable[float],
    h: float = 1.0,
    k: float = 0.5,
    qubit: int = 1,
) -> pd.DataFrame:
    """Sweep a depolarizing channel applied after Alice and before Bob."""
    return _sweep_pre_bob_channel("depolarizing", ps, h=h, k=k, qubit=qubit)


def sweep_amplitude_damping(
    gammas: Iterable[float],
    h: float = 1.0,
    k: float = 0.5,
    qubit: int = 1,
) -> pd.DataFrame:
    """Sweep an amplitude-damping channel applied after Alice and before Bob."""
    return _sweep_pre_bob_channel("amplitude_damping", gammas, h=h, k=k, qubit=qubit)


def _sweep_pre_bob_channel(
    noise_model: str,
    strengths: Iterable[float],
    h: float,
    k: float,
    qubit: int,
) -> pd.DataFrame:
    rows: list[dict[str, float | int | str]] = []
    for strength in strengths:
        p = float(strength)
        if noise_model == "dephasing":
            channel = dephasing_channel(p)
        elif noise_model == "depolarizing":
            channel = depolarizing_channel(p)
        elif noise_model == "amplitude_damping":
            channel = amplitude_damping_channel(p)
        else:
            raise ValueError(f"unknown noise_model: {noise_model}")

        row: dict[str, float | int | str] = {
            "noise_model": noise_model,
            "noise_strength": p,
            "noise_qubit": qubit,
            "h": float(h),
            "k": float(k),
        }
        row.update(
            qet_ledger_with_noise(
                h=h,
                k=k,
                pre_bob_kraus_ops=lift_to_two_qubits(channel, qubit),
            )
        )
        rows.append(row)
    return pd.DataFrame(rows)
