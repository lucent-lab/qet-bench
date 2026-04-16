# Optional Qiskit/Aer Interoperability

The exact NumPy simulator and the pure-Python reference branch implementation
remain the authoritative benchmark definitions. The Qiskit/Aer bridge is an
optional interoperability check for users who want to inspect branch-resolved
ideal circuits or feed Qiskit count dictionaries into the same local-energy
estimators.

## Dependency Boundary

The base package does not require Qiskit, Qiskit Aer, cloud credentials, or
backend access. Install the optional extra only when you want the bridge:

```bash
pip install -e ".[qiskit]"
python scripts/run_qiskit_bridge.py
```

All Qiskit imports are lazy. Importing `qet_bench` or
`qet_bench.qiskit_bridge` works without Qiskit installed.

## Bit Ordering

Internal count estimators use two-bit strings in `q0q1` order:

- left bit: Alice qubit `q0`
- right bit: Bob qubit `q1`

For Qiskit circuits that measure `q0 -> c0` and `q1 -> c1`, raw count strings
are displayed as `c1c0`. The bridge reverses each two-bit Qiskit key exactly
once at the adapter boundary before calling `qet_bench.counts`.

Use `canonicalize_counts_q0q1(counts, source_order="qiskit")` for raw Qiskit
counts and `source_order="q0q1"` only for dictionaries that already use the
package convention.

## Circuit Scope

The bridge uses branch-resolved ideal circuits rather than dynamic feedforward
circuits. Each Alice measurement outcome is represented by a normalized branch
state prepared in a circuit, Bob's conditional rotation is already applied, and
Python performs the unconditional branch average with the exact branch weights.
This keeps the check independent of backend support for mid-circuit measurement
and dynamic control.

The optional Aer script is therefore a simulator-interoperability diagnostic,
not a replacement for the exact ledger and not a hardware execution protocol.
As in the rest of the package, no result is interpreted as free energy: Bob's
local extraction is reported against the Alice-side measurement/control ledger.
