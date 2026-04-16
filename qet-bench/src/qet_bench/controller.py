"""Controller and battery-inclusive accounting helpers for QET ledgers."""

from __future__ import annotations

from dataclasses import dataclass
from math import log

from qet_bench.exact import qet_ledger

BOLTZMANN_CONSTANT_J_PER_K = 1.380_649e-23


@dataclass(frozen=True)
class ControllerCosts:
    """Nonnegative controller costs expressed in QET model energy units.

    The exact QET ledger already includes Alice's injected system energy
    ``E_A``. These fields represent additional controller-side overheads such
    as memory reset, communication, pulse generation, state preparation, or
    calibration. They are deliberately additive and conservative.
    """

    measurement_record_reset: float = 0.0
    classical_communication: float = 0.0
    bob_control_pulse: float = 0.0
    state_preparation: float = 0.0
    calibration: float = 0.0

    def total(self) -> float:
        """Return the total nonnegative controller overhead."""
        values = (
            self.measurement_record_reset,
            self.classical_communication,
            self.bob_control_pulse,
            self.state_preparation,
            self.calibration,
        )
        if any(value < 0.0 for value in values):
            raise ValueError("controller costs must be nonnegative")
        return float(sum(values))


def controller_inclusive_ledger(
    h: float = 1.0,
    k: float = 0.5,
    costs: ControllerCosts | None = None,
    feedforward_error_probability: float = 0.0,
    initial_state: str = "ground",
) -> dict[str, float]:
    """Return an exact QET ledger plus conservative controller accounting.

    The returned ``net_battery_gain`` is the Bob-side recovered energy minus
    Alice's injected energy and all explicit controller overheads:

    ``net_battery_gain = E_B - E_A - controller_overhead``.

    For the exact ground-state protocol with nonnegative overheads, this value
    should be nonpositive because the base model has ``E_A >= E_B``.
    """
    cost_model = costs if costs is not None else ControllerCosts()
    base = qet_ledger(
        h=h,
        k=k,
        feedforward_error_probability=feedforward_error_probability,
        initial_state=initial_state,
    )
    overhead = cost_model.total()
    recovered = base["E_B"]
    paid = base["E_A"] + overhead
    controller_gap = base["E_A_minus_E_B"] + overhead

    return {
        **base,
        "controller_measurement_record_reset": cost_model.measurement_record_reset,
        "controller_classical_communication": cost_model.classical_communication,
        "controller_bob_control_pulse": cost_model.bob_control_pulse,
        "controller_state_preparation": cost_model.state_preparation,
        "controller_calibration": cost_model.calibration,
        "controller_overhead": overhead,
        "controller_inclusive_gap": controller_gap,
        "paid_energy": paid,
        "recovered_energy": recovered,
        "net_battery_gain": recovered - paid,
        "alice_battery_delta": -(
            base["E_A"]
            + cost_model.measurement_record_reset
            + cost_model.classical_communication
            + cost_model.state_preparation
            + cost_model.calibration
        ),
        "bob_battery_delta": recovered - cost_model.bob_control_pulse,
    }


def landauer_reset_cost(
    bits: float = 1.0,
    temperature_kelvin: float = 300.0,
    boltzmann_constant_j_per_k: float = BOLTZMANN_CONSTANT_J_PER_K,
) -> float:
    """Return the Landauer reset bound ``bits * k_B * T * ln(2)`` in joules."""
    if bits < 0.0:
        raise ValueError("bits must be nonnegative")
    if temperature_kelvin < 0.0:
        raise ValueError("temperature_kelvin must be nonnegative")
    if boltzmann_constant_j_per_k <= 0.0:
        raise ValueError("boltzmann_constant_j_per_k must be positive")
    return float(bits * boltzmann_constant_j_per_k * temperature_kelvin * log(2.0))


def landauer_controller_costs(
    bits_to_reset: float = 1.0,
    temperature_kelvin: float = 300.0,
    energy_unit_joule: float = 1.0,
) -> ControllerCosts:
    """Return controller costs with a Landauer reset term in model units.

    ``energy_unit_joule`` is the physical joule value corresponding to one
    dimensionless QET model energy unit. The returned reset cost is
    ``landauer_reset_cost(...) / energy_unit_joule``.
    """
    if energy_unit_joule <= 0.0:
        raise ValueError("energy_unit_joule must be positive")
    reset_cost = landauer_reset_cost(bits_to_reset, temperature_kelvin) / energy_unit_joule
    return ControllerCosts(measurement_record_reset=reset_cost)

