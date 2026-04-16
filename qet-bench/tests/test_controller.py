from qet_bench.controller import (
    ControllerCosts,
    controller_inclusive_ledger,
    landauer_controller_costs,
    landauer_reset_cost,
)
from qet_bench.exact import qet_ledger


def test_controller_inclusive_zero_overhead_matches_base_gap() -> None:
    base = qet_ledger(h=1.0, k=0.5)
    ledger = controller_inclusive_ledger(h=1.0, k=0.5)
    assert abs(ledger["controller_inclusive_gap"] - base["E_A_minus_E_B"]) < 1.0e-12
    assert ledger["net_battery_gain"] <= 1.0e-12


def test_controller_overhead_makes_battery_balance_more_conservative() -> None:
    costs = ControllerCosts(
        measurement_record_reset=0.01,
        classical_communication=0.02,
        bob_control_pulse=0.03,
    )
    base = qet_ledger(h=1.0, k=0.5)
    ledger = controller_inclusive_ledger(h=1.0, k=0.5, costs=costs)
    assert abs(ledger["controller_overhead"] - 0.06) < 1.0e-12
    assert abs(ledger["controller_inclusive_gap"] - (base["E_A_minus_E_B"] + 0.06)) < 1.0e-12
    assert ledger["net_battery_gain"] < base["E_B"] - base["E_A"]


def test_landauer_helpers() -> None:
    one_bit_cost = landauer_reset_cost(bits=1.0, temperature_kelvin=300.0)
    assert one_bit_cost > 0.0
    costs = landauer_controller_costs(
        bits_to_reset=1.0,
        temperature_kelvin=300.0,
        energy_unit_joule=one_bit_cost,
    )
    assert abs(costs.measurement_record_reset - 1.0) < 1.0e-12

