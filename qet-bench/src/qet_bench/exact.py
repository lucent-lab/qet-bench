"""Exact density-matrix simulation for the two-qubit QET protocol."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from qet_bench.hamiltonians import qet_hamiltonians
from qet_bench.noise import apply_channel

ComplexArray = NDArray[np.complex128]
Ledger = dict[str, float]


def ground_state(h: float, k: float) -> ComplexArray:
    """Return the analytic ground-state ket in the ``|00>, |01>, |10>, |11>`` basis."""
    if h <= 0:
        raise ValueError("h must be positive")
    if k < 0:
        raise ValueError("k must be nonnegative")

    s = float(np.sqrt(h * h + k * k))
    amp_00 = np.sqrt((1.0 - h / s) / 2.0)
    amp_11 = np.sqrt((1.0 + h / s) / 2.0)
    return np.array([amp_00, 0.0, 0.0, -amp_11], dtype=np.complex128)


def bob_angle(h: float, k: float) -> float:
    """Return Bob's optimal feedforward rotation angle for the benchmark model."""
    if h <= 0:
        raise ValueError("h must be positive")
    if k < 0:
        raise ValueError("k must be nonnegative")
    return float(0.5 * np.arctan2(h * k, h * h + 2.0 * k * k))


def qet_ledger(
    h: float = 1.0,
    k: float = 0.5,
    feedforward_error_probability: float = 0.0,
    initial_state: str = "ground",
) -> Ledger:
    """Run the exact QET protocol and return the energy ledger.

    Alice's projective measurement branches are kept unnormalized and summed,
    so the result is an unconditional average over all outcomes. No branch is
    postselected. With ``feedforward_error_probability=q``, Bob receives the
    flipped classical sign with probability ``q``.

    ``initial_state`` may be ``"ground"`` or ``"product_00"``. For the ground
    state, ``E_A`` matches the standard injected-energy expression because the
    Hamiltonian constants set the ground energy to zero. For ``"product_00"``,
    ``E_A`` is reported as Alice's energy change relative to that initial state.
    """
    phi = bob_angle(h, k)
    return _qet_ledger_with_phi(
        h=h,
        k=k,
        phi=phi,
        feedforward_error_probability=feedforward_error_probability,
        initial_state=initial_state,
    )


def qet_ledger_with_noise(
    h: float = 1.0,
    k: float = 0.5,
    pre_bob_kraus_ops: Sequence[ComplexArray] | None = None,
    feedforward_error_probability: float = 0.0,
    initial_state: str = "ground",
    phi: float | None = None,
) -> Ledger:
    """Run QET with an optional trace-preserving channel before Bob's rotation.

    The added channel is an open-system diagnostic: its energy exchange with an
    environment is reported as ``noise_energy_delta`` but is not claimed as a
    closed thermodynamic ledger.
    """
    if phi is None:
        phi = bob_angle(h, k)
    return _qet_ledger_with_phi(
        h=h,
        k=k,
        phi=phi,
        feedforward_error_probability=feedforward_error_probability,
        initial_state=initial_state,
        pre_bob_kraus_ops=pre_bob_kraus_ops,
    )


def _qet_ledger_with_phi(
    h: float,
    k: float,
    phi: float,
    feedforward_error_probability: float = 0.0,
    initial_state: str = "ground",
    pre_bob_kraus_ops: Sequence[ComplexArray] | None = None,
) -> Ledger:
    if feedforward_error_probability < 0.0 or feedforward_error_probability > 1.0:
        raise ValueError("feedforward_error_probability must be between 0 and 1")

    ops = qet_hamiltonians(h, k)
    i4 = _matrix(ops["I4"])
    x0 = _matrix(ops["X0"])
    y1 = _matrix(ops["Y1"])
    h1_op = _matrix(ops["H1"])
    v_op = _matrix(ops["V"])
    htot = _matrix(ops["Htot"])

    ket = _initial_ket(h, k, initial_state)
    rho0 = _density(ket)
    initial_energy = _expectation(rho0, htot)

    rho_after_alice = np.zeros((4, 4), dtype=np.complex128)
    rho_after_noise = np.zeros((4, 4), dtype=np.complex128)
    rho_final = np.zeros((4, 4), dtype=np.complex128)
    q = feedforward_error_probability

    for mu in (-1, 1):
        projector = 0.5 * (i4 + mu * x0)
        rho_mu = projector @ rho0 @ projector
        rho_after_alice += rho_mu
        if pre_bob_kraus_ops is None:
            rho_mu_for_bob = rho_mu
        else:
            rho_mu_for_bob = apply_channel(rho_mu, pre_bob_kraus_ops)
        rho_after_noise += rho_mu_for_bob

        for received_mu, probability in ((mu, 1.0 - q), (-mu, q)):
            unitary = np.cos(phi) * i4 - 1j * received_mu * np.sin(phi) * y1
            rho_final += probability * unitary @ rho_mu_for_bob @ unitary.conj().T

    post_alice_energy = _expectation(rho_after_alice, htot)
    post_noise_energy = _expectation(rho_after_noise, htot)
    if initial_state == "ground":
        e_a = post_alice_energy
    else:
        e_a = post_alice_energy - initial_energy

    h1_energy = _expectation(rho_final, h1_op)
    v_energy = _expectation(rho_final, v_op)
    e1 = h1_energy + v_energy
    e_b = -e1
    e_a_minus_e_b = e_a - e_b
    e_b_over_e_a = e_b / e_a if abs(e_a) > 1.0e-15 else float("nan")

    return {
        "H1": h1_energy,
        "V": v_energy,
        "E1": e1,
        "E_B": e_b,
        "E_A": e_a,
        "E_A_minus_E_B": e_a_minus_e_b,
        "E_B_over_E_A": e_b_over_e_a,
        "phi": float(phi),
        "trace_final": float(np.real(np.trace(rho_final))),
        "initial_energy": initial_energy,
        "post_alice_energy": post_alice_energy,
        "post_noise_energy": post_noise_energy,
        "noise_energy_delta": post_noise_energy - post_alice_energy,
        "final_global_energy": _expectation(rho_final, htot),
    }


def _initial_ket(h: float, k: float, initial_state: str) -> ComplexArray:
    if initial_state == "ground":
        return ground_state(h, k)
    if initial_state == "product_00":
        return np.array([1.0, 0.0, 0.0, 0.0], dtype=np.complex128)
    raise ValueError('initial_state must be "ground" or "product_00"')


def _density(ket: ComplexArray) -> ComplexArray:
    return np.outer(ket, ket.conj()).astype(np.complex128, copy=False)


def _expectation(rho: ComplexArray, operator: ComplexArray) -> float:
    return float(np.real(np.trace(rho @ operator)))


def _matrix(value: ComplexArray | float) -> ComplexArray:
    if isinstance(value, float):
        raise TypeError("expected a matrix, got a scalar")
    return value
