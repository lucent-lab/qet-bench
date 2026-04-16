# Controller and Battery Accounting

The exact QET ledger reports Alice's injected system energy `E_A`, Bob's local
extraction `E_B`, and the model-level accounting gap `E_A - E_B`. A
controller-inclusive ledger adds explicit nonnegative overheads for operations
that are outside the two-qubit Hamiltonian:

- measurement-record reset,
- classical communication,
- Bob's control pulse,
- state preparation,
- calibration.

The conservative net battery balance is

```math
W_\mathrm{net}=E_B-E_A-W_\mathrm{controller}.
```

For the exact ground-state protocol and nonnegative controller overheads,
`W_net <= 0`. This extension is intentionally an accounting layer, not a
microscopic detector or pulse-generator simulation. It is useful for checking
that any later hardware or battery model keeps the payer explicit.

The helper `landauer_reset_cost` returns `bits * k_B * T * ln(2)` in joules.
The helper `landauer_controller_costs` maps that SI reset cost into the
dimensionless model units once an energy-unit calibration is supplied.

