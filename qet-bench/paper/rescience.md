---
title: "Reproducing an exact two-qubit Quantum Energy Teleportation benchmark with qet-bench"
tags:
  - Python
  - quantum information
  - quantum energy teleportation
  - reproducibility
  - scientific software
authors:
  - name: Francois Gueguen
    affiliation: 1
    corresponding: true
affiliations:
  - name: "Lucent Lab"
    index: 1
date: 16 April 2026
bibliography: references.bib
---

# Summary

`qet-bench` is a small Python reproduction package for the minimal two-qubit
Quantum Energy Teleportation (QET) benchmark. It implements the exact
Hamiltonian model, Alice's local measurement, classical feedforward, Bob's local
rotation, and the energy ledger used to evaluate Bob-side local energy
extraction. The package is designed to be rerun without a quantum SDK, cloud
backend, hardware account, or proprietary software.

# Reproduced result

The reproduced result is the two-qubit QET effect: after Alice performs a local
measurement on an entangled ground state and communicates the outcome, Bob can
apply an outcome-conditioned local operation that yields positive local energy
extraction on his side [@hotta2008measurement; @hotta2009spin]. The package also
reproduces the corresponding no-free-energy accounting used in
hardware-oriented presentations of the protocol [@ikeda2023hardware]: Bob's
local extraction is bounded by Alice's measurement and control resources, and
the exact ground-state ledger satisfies $E_A \ge E_B$.

For the canonical anchors, `qet-bench` reproduces:

| $h$ | $k$ | $E_A$ | $E_B$ | $E_A-E_B$ |
|---:|---:|---:|---:|---:|
| 1.0 | 0.5 | 0.8944271909999154 | 0.0725727758732213 | 0.8218544151266941 |
| 1.0 | 1.0 | 0.7071067811865467 | 0.1147476339401475 | 0.5923591472463992 |

The replication target is intentionally narrow. It is not a new QET theorem, a
many-body simulation, or a hardware demonstration. Its value is an auditable
software reproduction of the exact benchmark, its branch averaging conventions,
and its energy-accounting interpretation.

# Implementation

The package uses explicit NumPy/SciPy density-matrix calculations for the main
exact ledger and keeps the benchmark independent of quantum-framework version
drift. An independent pure-Python branch-amplitude implementation cross-checks
the same benchmark values without using the main NumPy propagation path.

The generated artifact set includes exact benchmark CSV files, parameter
sweeps, null-test figures, fixed-protocol noise diagnostics, count-estimator
convention examples, and an artifact manifest mapping each output to the script
and tests that support it. Optional Qiskit/Aer interoperability is implemented
as a branch-resolved simulator smoke check and count-key convention bridge; it
is not part of the base reproduction path.

# Reproducibility

The base reproduction path is:

```bash
python -m pip install -e ".[dev]" -c requirements-lock.txt
python -m pytest
python scripts/reproduce_benchmarks.py
python scripts/make_all_figures.py
```

The optional Qiskit/Aer bridge can be checked with:

```bash
python -m pip install -e ".[qiskit]" -c requirements-lock.txt
python scripts/run_qiskit_bridge.py
```

The `0.2.0` review target was locally validated on Python 3.11 and Python 3.12.
Hosted GitHub Actions is configured, but hosted jobs were blocked before
execution by the account billing/spending limit at the time of this draft. The
current local validation record is maintained in
`docs/release_validation.md`.

# Reproduction checks

The reproduction is guarded by:

- exact regression tests for the two canonical benchmark points,
- final-state trace checks,
- global accounting tests for $E_A \ge E_B$,
- zero-coupling and scrambled-feedforward null tests,
- Bob-angle convention scans,
- count bit-ordering tests,
- optional Qiskit/Aer import guards and smoke checks.

Generated artifacts are intentionally reviewable but not authoritative by
themselves. The source of truth remains the package code, tests, scripts,
lockfile, and artifact manifest.

# Interpretation limits

The reproduced QET benchmark demonstrates local energy extraction enabled by
ground-state correlations, measurement, and classical feedforward. It does not
describe an autonomous energy source. Alice's measurement and control resources
are part of the ledger, and the package keeps that no-free-energy interpretation
visible in the README, tests, manuscript, roadmap, and blocker ledger.

The controller/battery accounting extension is conservative bookkeeping rather
than a microscopic detector, pulse, memory, reset, or environment model. Future
many-body, finite-temperature, hardware-faithful, or vacuum-mechanism audits
should be treated as new research territory rather than as part of this
reproduction package.

# AI usage disclosure

Generative AI assistance from OpenAI Codex models, including GPT-5-class models
and GPT-5.4 Mini review agents, was used for implementation, refactoring,
testing, documentation, manuscript drafting, and adversarial review. AI-assisted
changes were checked through exact benchmark regressions, an independent
pure-Python branch implementation, local test suites, artifact regeneration, and
human review before acceptance.

# Acknowledgements

No external funding is declared.

# References

