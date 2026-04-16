"""Exact two-qubit Quantum Energy Teleportation benchmark tools."""

from __future__ import annotations

__all__ = [
    "__version__",
    "ControllerCosts",
    "bob_angle",
    "controller_inclusive_ledger",
    "ground_state",
    "landauer_controller_costs",
    "landauer_reset_cost",
    "qet_ledger",
    "qet_ledger_with_noise",
]

__version__ = "0.1.0"


def __getattr__(name: str) -> object:
    """Lazily expose public helpers without importing NumPy at package import."""
    if name in {
        "ControllerCosts",
        "controller_inclusive_ledger",
        "landauer_controller_costs",
        "landauer_reset_cost",
    }:
        from qet_bench import controller

        return getattr(controller, name)

    if name in {"bob_angle", "ground_state", "qet_ledger", "qet_ledger_with_noise"}:
        from qet_bench import exact

        return getattr(exact, name)

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
