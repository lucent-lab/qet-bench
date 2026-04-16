"""Optional Qiskit/Aer interoperability helpers.

The exact NumPy ledger remains the source of truth for the benchmark. This
module is a thin adapter for branch-resolved ideal-circuit checks and for
normalizing Qiskit count dictionaries into the package's ``q0q1`` convention.
All Qiskit imports are lazy so the base package has no Qiskit dependency.
"""

from __future__ import annotations

import importlib.util
from collections.abc import Mapping
from math import sqrt
from typing import Any, Literal

import numpy as np
from numpy.typing import NDArray

from qet_bench.counts import local_energies_from_counts
from qet_bench.exact import qet_ledger
from qet_bench.reference_branch import (
    State,
    apply_bob_rotation,
    apply_x0_projector,
    bob_angle,
    norm,
    reference_ground_state,
)

CountValue = int | float
Counts = Mapping[str, CountValue]
ComplexArray = NDArray[np.complex128]
CountOrder = Literal["qiskit", "q0q1"]
MeasurementBasis = Literal["z1", "xx"]

INSTALL_HINT = 'Install optional dependencies with: pip install -e ".[qiskit]"'


def is_qiskit_available() -> bool:
    """Return whether the optional core Qiskit package is importable."""
    return importlib.util.find_spec("qiskit") is not None


def is_qiskit_aer_available() -> bool:
    """Return whether the optional Qiskit Aer simulator package is importable."""
    return importlib.util.find_spec("qiskit_aer") is not None


def require_qiskit() -> Any:
    """Import and return Qiskit, or raise a helpful optional-dependency error."""
    try:
        import qiskit
    except ImportError as exc:
        raise RuntimeError(f"Qiskit is optional for qet-bench. {INSTALL_HINT}") from exc
    return qiskit


def canonicalize_counts_q0q1(
    counts: Counts,
    source_order: CountOrder = "qiskit",
) -> dict[str, float]:
    """Return count keys in canonical ``q0q1`` order.

    Internal count estimators in :mod:`qet_bench.counts` use two-character
    bitstrings in ``q0q1`` order: Alice qubit ``q0`` is the left bit and Bob
    qubit ``q1`` is the right bit.

    For Qiskit circuits that measure ``q0 -> c0`` and ``q1 -> c1``, raw count
    strings are displayed as ``c1c0``. The default ``source_order="qiskit"``
    therefore reverses each two-bit key once at the adapter boundary.
    """
    if source_order not in ("qiskit", "q0q1"):
        raise ValueError('source_order must be "qiskit" or "q0q1"')

    canonical: dict[str, float] = {}
    for bitstring, count in counts.items():
        if count < 0:
            raise ValueError("count values must be nonnegative")
        bits = _clean_two_bit_key(bitstring)
        key = bits[::-1] if source_order == "qiskit" else bits
        canonical[key] = canonical.get(key, 0.0) + float(count)
    return canonical


def ledger_from_qiskit_counts(
    counts_z1: Counts,
    counts_xx: Counts,
    h: float,
    k: float,
    source_order: CountOrder = "qiskit",
) -> dict[str, float]:
    """Estimate the local Bob ledger from raw Qiskit count dictionaries.

    The two input dictionaries are assumed to come from independent circuits:
    one computational-basis circuit for ``Z1`` and one X-basis circuit for
    ``X0 X1``. Raw Qiskit bitstrings are normalized into ``q0q1`` order before
    delegating to :func:`qet_bench.counts.local_energies_from_counts`.
    """
    return local_energies_from_counts(
        counts_z1=canonicalize_counts_q0q1(counts_z1, source_order=source_order),
        counts_xx=canonicalize_counts_q0q1(counts_xx, source_order=source_order),
        h=h,
        k=k,
    )


def build_branch_circuit(
    h: float,
    k: float,
    mu: int,
    measurement_basis: MeasurementBasis = "z1",
    received_mu: int | None = None,
    initial_state: str = "ground",
) -> Any:
    """Build a branch-resolved ideal Qiskit circuit for one Alice outcome.

    The circuit prepares the normalized final branch state after Alice's
    ``X0`` measurement outcome ``mu`` and Bob's conditional rotation using
    ``received_mu``. When ``received_mu`` is omitted, Bob receives the correct
    Alice sign. This avoids dynamic-circuit assumptions and keeps feedforward
    averaging in Python.

    ``measurement_basis="z1"`` measures the computational basis for ``Z1``.
    ``measurement_basis="xx"`` applies Hadamards before measurement so the
    resulting counts estimate ``X0 X1``.
    """
    _validate_mu(mu)
    if received_mu is None:
        received_mu = mu
    _validate_mu(received_mu)
    if measurement_basis not in ("z1", "xx"):
        raise ValueError('measurement_basis must be "z1" or "xx"')

    qiskit = require_qiskit()
    state, _branch_weight = _normalized_final_branch_state(
        h=h,
        k=k,
        mu=mu,
        received_mu=received_mu,
        initial_state=initial_state,
    )
    circuit = qiskit.QuantumCircuit(2, 2, name=f"qet_mu_{mu}_{measurement_basis}")
    circuit.initialize(_q0q1_state_to_qiskit_vector(state), [0, 1])
    if measurement_basis == "xx":
        circuit.h(0)
        circuit.h(1)
    circuit.measure([0, 1], [0, 1])
    return circuit


def run_aer_branches(
    h: float = 1.0,
    k: float = 0.5,
    shots: int = 4096,
    seed: int = 0,
    feedforward_error_probability: float = 0.0,
    initial_state: str = "ground",
) -> dict[str, float]:
    """Run a branch-resolved ideal Aer smoke check and return a count ledger.

    Each Alice branch is simulated as a normalized state-preparation circuit,
    and the resulting counts are reweighted by the exact branch probability.
    This is an interoperability diagnostic, not the canonical benchmark
    simulator. The exact QET ledger is included in the output for comparison.
    """
    if shots <= 0:
        raise ValueError("shots must be positive")
    if feedforward_error_probability < 0.0 or feedforward_error_probability > 1.0:
        raise ValueError("feedforward_error_probability must be between 0 and 1")

    qiskit = require_qiskit()
    simulator_class = _require_aer_simulator()
    simulator = simulator_class(seed_simulator=seed)

    circuits: list[Any] = []
    labels: list[MeasurementBasis] = []
    weights: list[float] = []
    q = feedforward_error_probability
    for measurement_basis in ("z1", "xx"):
        for mu in (-1, 1):
            for received_mu, probability in ((mu, 1.0 - q), (-mu, q)):
                if probability == 0.0:
                    continue
                _state, branch_weight = _normalized_final_branch_state(
                    h=h,
                    k=k,
                    mu=mu,
                    received_mu=received_mu,
                    initial_state=initial_state,
                )
                circuits.append(
                    build_branch_circuit(
                        h=h,
                        k=k,
                        mu=mu,
                        measurement_basis=measurement_basis,
                        received_mu=received_mu,
                        initial_state=initial_state,
                    )
                )
                labels.append(measurement_basis)
                weights.append(branch_weight * probability)

    transpiled = qiskit.transpile(circuits, simulator, seed_transpiler=seed)
    result = simulator.run(transpiled, shots=shots, seed_simulator=seed).result()
    weighted_counts: dict[MeasurementBasis, dict[str, float]] = {"z1": {}, "xx": {}}
    for index, measurement_basis in enumerate(labels):
        raw_counts = result.get_counts(index)
        canonical = canonicalize_counts_q0q1(raw_counts, source_order="qiskit")
        _add_weighted_counts(
            weighted_counts[measurement_basis],
            canonical,
            weights[index],
        )

    ledger = local_energies_from_counts(
        counts_z1=weighted_counts["z1"],
        counts_xx=weighted_counts["xx"],
        h=h,
        k=k,
    )
    exact = qet_ledger(
        h=h,
        k=k,
        feedforward_error_probability=feedforward_error_probability,
        initial_state=initial_state,
    )
    ledger.update(
        {
            "exact_E_A": exact["E_A"],
            "exact_E_B": exact["E_B"],
            "absolute_E_B_error": abs(ledger["E_B"] - exact["E_B"]),
            "shots_per_branch": float(shots),
            "seed": float(seed),
            "branch_weight_total_z1": sum(
                weight for label, weight in zip(labels, weights, strict=True) if label == "z1"
            ),
            "branch_weight_total_xx": sum(
                weight for label, weight in zip(labels, weights, strict=True) if label == "xx"
            ),
        }
    )
    return ledger


def _require_aer_simulator() -> Any:
    try:
        from qiskit_aer import AerSimulator
    except ImportError as exc:
        raise RuntimeError(f"Qiskit Aer is optional for qet-bench. {INSTALL_HINT}") from exc
    return AerSimulator


def _initial_state(h: float, k: float, initial_state: str) -> State:
    if initial_state == "ground":
        return reference_ground_state(h, k)
    if initial_state == "product_00":
        return (1.0 + 0.0j, 0.0j, 0.0j, 0.0j)
    raise ValueError('initial_state must be "ground" or "product_00"')


def _normalized_final_branch_state(
    h: float,
    k: float,
    mu: int,
    received_mu: int,
    initial_state: str,
) -> tuple[ComplexArray, float]:
    state = _initial_state(h, k, initial_state)
    alice_branch = apply_x0_projector(state, mu)
    branch_weight = norm(alice_branch)
    if branch_weight <= 0.0:
        raise ValueError("Alice branch has zero weight")
    phi = bob_angle(h, k)
    bob_branch = apply_bob_rotation(alice_branch, received_mu, phi)
    normalized = np.array(bob_branch, dtype=np.complex128) / sqrt(branch_weight)
    return normalized, branch_weight


def _q0q1_state_to_qiskit_vector(state: ComplexArray) -> ComplexArray:
    """Convert ``|q0 q1>`` amplitude order to Qiskit's little-endian order."""
    return np.array([state[0], state[2], state[1], state[3]], dtype=np.complex128)


def _clean_two_bit_key(bitstring: str) -> str:
    bits = bitstring.replace(" ", "")
    if len(bits) != 2 or any(bit not in "01" for bit in bits):
        raise ValueError("count keys must be two-character bitstrings")
    return bits


def _validate_mu(mu: int) -> None:
    if mu not in (-1, 1):
        raise ValueError("mu must be -1 or 1")


def _add_weighted_counts(
    target: dict[str, float],
    counts: Mapping[str, float],
    weight: float,
) -> None:
    for bitstring, count in counts.items():
        target[bitstring] = target.get(bitstring, 0.0) + weight * count
