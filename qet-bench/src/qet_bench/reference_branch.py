"""Pure-Python branch-by-branch reference implementation for two-qubit QET.

This module is intentionally independent of the NumPy matrix implementation in
``qet_bench.exact``. It represents kets as four Python complex amplitudes in
``|00>, |01>, |10>, |11>`` order and applies the protocol through explicit
basis-state rules. It is meant as a small reviewer-auditable cross-check, not as
the primary simulator.
"""

from __future__ import annotations

from math import atan2, cos, sin, sqrt

State = tuple[complex, complex, complex, complex]


def ground_state_coeffs(h: float, k: float) -> tuple[float, float]:
    """Return the nonzero ``|00>`` and ``|11>`` ground-state amplitudes."""
    _validate_parameters(h, k)
    scale = sqrt(h * h + k * k)
    amp_00 = sqrt((1.0 - h / scale) / 2.0)
    amp_11 = -sqrt((1.0 + h / scale) / 2.0)
    return amp_00, amp_11


def reference_ground_state(h: float, k: float) -> State:
    """Return the analytic ground-state ket as a four-amplitude tuple."""
    amp_00, amp_11 = ground_state_coeffs(h, k)
    return (complex(amp_00), 0.0j, 0.0j, complex(amp_11))


def apply_x0_projector(state: State, mu: int) -> State:
    """Apply Alice's unnormalized ``P_mu = (I + mu X0) / 2`` branch."""
    _validate_mu(mu)
    a00, a01, a10, a11 = state
    return (
        0.5 * (a00 + mu * a10),
        0.5 * (a01 + mu * a11),
        0.5 * (a10 + mu * a00),
        0.5 * (a11 + mu * a01),
    )


def apply_bob_rotation(state: State, mu: int, phi: float) -> State:
    """Apply Bob's ``cos(phi) I - i mu sin(phi) Y1`` rotation to a branch."""
    _validate_mu(mu)
    c = cos(phi)
    s = sin(phi)
    a00, a01, a10, a11 = state
    return (
        c * a00 - mu * s * a01,
        mu * s * a00 + c * a01,
        c * a10 - mu * s * a11,
        mu * s * a10 + c * a11,
    )


def bob_angle(h: float, k: float) -> float:
    """Return Bob's analytic rotation angle using only scalar arithmetic."""
    _validate_parameters(h, k)
    return 0.5 * atan2(h * k, h * h + 2.0 * k * k)


def norm(state: State) -> float:
    """Return the unnormalized branch weight ``<state|state>``."""
    return float(sum(abs(amplitude) ** 2 for amplitude in state))


def expect_z0(state: State) -> float:
    """Return the unnormalized ``Z0`` expectation in ``q0q1`` ordering."""
    a00, a01, a10, a11 = state
    return float(abs(a00) ** 2 + abs(a01) ** 2 - abs(a10) ** 2 - abs(a11) ** 2)


def expect_z1(state: State) -> float:
    """Return the unnormalized ``Z1`` expectation in ``q0q1`` ordering."""
    a00, a01, a10, a11 = state
    return float(abs(a00) ** 2 - abs(a01) ** 2 + abs(a10) ** 2 - abs(a11) ** 2)


def expect_x0x1(state: State) -> float:
    """Return the unnormalized ``X0 X1`` expectation."""
    a00, a01, a10, a11 = state
    return float(2.0 * ((a00.conjugate() * a11 + a01.conjugate() * a10).real))


def expect_h0(state: State, h: float, k: float) -> float:
    """Return the unnormalized local Alice Hamiltonian expectation."""
    scale = sqrt(h * h + k * k)
    return h * expect_z0(state) + (h * h / scale) * norm(state)


def expect_h1(state: State, h: float, k: float) -> float:
    """Return the unnormalized local Bob Hamiltonian expectation."""
    scale = sqrt(h * h + k * k)
    return h * expect_z1(state) + (h * h / scale) * norm(state)


def expect_v(state: State, h: float, k: float) -> float:
    """Return the unnormalized interaction Hamiltonian expectation."""
    scale = sqrt(h * h + k * k)
    return 2.0 * k * expect_x0x1(state) + (2.0 * k * k / scale) * norm(state)


def expect_htot(state: State, h: float, k: float) -> float:
    """Return the unnormalized total Hamiltonian expectation."""
    return expect_h0(state, h, k) + expect_h1(state, h, k) + expect_v(state, h, k)


def reference_qet_ledger(
    h: float = 1.0,
    k: float = 0.5,
    feedforward_error_probability: float = 0.0,
    initial_state: str = "ground",
) -> dict[str, float]:
    """Return the QET ledger from explicit branch-amplitude arithmetic.

    Alice branches are unnormalized and both outcomes are always included.
    ``feedforward_error_probability`` flips the sign received by Bob with the
    same convention as the production simulator.
    """
    if feedforward_error_probability < 0.0 or feedforward_error_probability > 1.0:
        raise ValueError("feedforward_error_probability must be between 0 and 1")

    state = _initial_state(h, k, initial_state)
    initial_energy = expect_htot(state, h, k)
    phi = bob_angle(h, k)
    q = feedforward_error_probability

    post_alice_energy = 0.0
    h1_energy = 0.0
    v_energy = 0.0
    trace_final = 0.0

    for mu in (-1, 1):
        alice_branch = apply_x0_projector(state, mu)
        post_alice_energy += expect_htot(alice_branch, h, k)

        for received_mu, probability in ((mu, 1.0 - q), (-mu, q)):
            bob_branch = apply_bob_rotation(alice_branch, received_mu, phi)
            h1_energy += probability * expect_h1(bob_branch, h, k)
            v_energy += probability * expect_v(bob_branch, h, k)
            trace_final += probability * norm(bob_branch)

    e_a = post_alice_energy if initial_state == "ground" else post_alice_energy - initial_energy
    e1 = h1_energy + v_energy
    e_b = -e1
    e_b_over_e_a = e_b / e_a if abs(e_a) > 1.0e-15 else float("nan")

    return {
        "H1": h1_energy,
        "V": v_energy,
        "E1": e1,
        "E_B": e_b,
        "E_A": e_a,
        "E_A_minus_E_B": e_a - e_b,
        "E_B_over_E_A": e_b_over_e_a,
        "phi": phi,
        "trace_final": trace_final,
        "initial_energy": initial_energy,
        "post_alice_energy": post_alice_energy,
    }


def reference_branch_audit(h: float = 1.0, k: float = 0.5) -> list[dict[str, float | int]]:
    """Return a branch audit for Alice outcomes before feedforward mixing."""
    state = reference_ground_state(h, k)
    phi = bob_angle(h, k)
    rows: list[dict[str, float | int]] = []
    for mu in (-1, 1):
        alice_branch = apply_x0_projector(state, mu)
        bob_branch = apply_bob_rotation(alice_branch, mu, phi)
        rows.append(
            {
                "mu": mu,
                "branch_weight": norm(alice_branch),
                "branch_energy_after_alice": expect_htot(alice_branch, h, k),
                "branch_h1_after_bob": expect_h1(bob_branch, h, k),
                "branch_v_after_bob": expect_v(bob_branch, h, k),
                "branch_e1_after_bob": expect_h1(bob_branch, h, k)
                + expect_v(bob_branch, h, k),
            }
        )
    return rows


def _initial_state(h: float, k: float, initial_state: str) -> State:
    if initial_state == "ground":
        return reference_ground_state(h, k)
    if initial_state == "product_00":
        return (1.0 + 0.0j, 0.0j, 0.0j, 0.0j)
    raise ValueError('initial_state must be "ground" or "product_00"')


def _validate_parameters(h: float, k: float) -> None:
    if h <= 0.0:
        raise ValueError("h must be positive")
    if k < 0.0:
        raise ValueError("k must be nonnegative")


def _validate_mu(mu: int) -> None:
    if mu not in (-1, 1):
        raise ValueError("mu must be -1 or 1")
