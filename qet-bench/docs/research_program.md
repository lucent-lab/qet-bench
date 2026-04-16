# qet-bench Research Program

`qet-bench` is the first software deliverable in a ground-state-correlation
energy-accounting program. The first release focuses on an exact two-qubit QET
model that is small enough to audit line by line and reproduce on a laptop.

The deliverable is designed to support a reproducibility or research-software
submission, not a claim of autonomous vacuum power. The required thesis is:

```text
Ground-state entanglement plus Alice measurement and classical feedforward can
enable Bob-side local energy extraction, while the full ledger remains
thermodynamically consistent with E_A >= E_B.
```

## First-Release Scope

- Exact analytic ground state for the two-qubit Hamiltonian.
- Projective Alice measurement of `X0`.
- Outcome-conditioned Bob rotation with optional classical sign-flip error.
- Energy ledger with `E_A`, `H1`, `V`, `E1`, `E_B`, and `E_A - E_B`.
- Null tests for zero coupling, scrambled feedforward, product-state reference,
  wrong Bob angle, and Bob-only random local unitaries.
- Noise sweeps for feedforward/readout errors, dephasing, depolarizing noise,
  amplitude damping, and Bob-angle miscalibration.
- Count-based estimators for `Z1`, `X0X1`, and local energy terms.
- Deterministic CSV and figure generation.

## Guardrails

- Average over all measurement branches.
- Do not postselect.
- Keep Alice measurement and control resources in the story.
- Report `E_A - E_B` wherever Bob extraction is reported.
- Treat open-system noise sweeps as diagnostics unless environment/controller
  energy is explicitly included.
- Treat cloud hardware, controller-inclusive batteries, and many-qubit scaling
  as later extensions.
