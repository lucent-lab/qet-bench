---
title: "qet-bench: Reproducible Exact Benchmarks for Two-Qubit Quantum Energy Teleportation"
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

`qet-bench` is a small scientific Python package for reproducing and auditing a
minimal two-qubit Quantum Energy Teleportation (QET) benchmark. The software
implements the exact Hamiltonian model, Alice's local measurement, classical
feedforward, Bob's local rotation, and the associated energy ledger. Its purpose
is to make a subtle quantum-information protocol easy to rerun without a
quantum SDK, cloud backend, or hardware credentials.

The benchmark demonstrates conditional Bob-side local energy extraction from an
entangled ground state while keeping the global accounting explicit. It does
not claim an autonomous energy source: Alice's measurement and control
resources pay for Bob's local extraction, and the exact ground-state ledger is
checked against $E_A \ge E_B$.

# Statement of need

QET combines ground-state entanglement, measurement backaction, classical
information, and local control [@hotta2008measurement; @hotta2009spin]. These
ingredients make the effect easy to misstate if the Alice-side energy injection
or the unconditional average over measurement branches is omitted. Recent
hardware-oriented work has renewed interest in compact, auditable versions of
the protocol [@ikeda2023hardware].

`qet-bench` is intended for researchers, reviewers, and students who need a
reference implementation of the two-qubit benchmark with explicit energy
accounting, null tests, deterministic artifacts, and count-estimator
conventions. It is not a general quantum simulator. Its narrower role is to
provide a reproducible testbed for validating formulas, branch averaging,
bit-ordering conventions, and no-free-energy interpretations before moving to
larger simulations or hardware-specific workflows.

# State of the field

General-purpose quantum software packages such as Qiskit and QuTiP provide
broad circuit, state-vector, and open-system simulation capabilities
[@qiskit2023; @johansson2012qutip]. Those tools are appropriate for many
quantum-computing and quantum-dynamics tasks, but they do not by themselves
define a compact QET reference ledger, exact benchmark fixtures, no-postselection
null tests, and publication-ready generated artifacts for the Hotta two-qubit
model.

`qet-bench` therefore does not compete with those packages as a simulator. It
builds a benchmark layer around the minimal QET protocol and keeps the runtime
dependencies limited to NumPy, SciPy, pandas, and Matplotlib
[@harris2020array; @virtanen2020scipy; @mckinney2010data;
@hunter2007matplotlib]. Optional Qiskit/Aer interoperability is provided only as
a branch-resolved cross-check and count-convention bridge; the exact ledger
remains the source of truth.

# Software design

The package favors explicit formulas over framework abstraction. Hamiltonian
terms, Pauli operators, exact density-matrix propagation, pure-Python branch
checks, count estimators, noise diagnostics, and plotting are separated into
small modules. This design makes each part of the ledger independently
inspectable and keeps the first reproducibility path independent of quantum SDK
version drift.

The benchmark scripts write deterministic CSV and figure artifacts under
`results/`. The artifact manifest maps each output to the script that generates
it and to the tests that cover it. Users can either call the API directly, for
example `qet_ledger(h=1.0, k=0.5)`, or run the reproduction scripts. The
canonical exact regression points are:

| $h$ | $k$ | $E_A$ | $E_B$ | $E_A-E_B$ |
|---:|---:|---:|---:|---:|
| 1.0 | 0.5 | 0.8944271909999154 | 0.0725727758732213 | 0.8218544151266941 |
| 1.0 | 1.0 | 0.7071067811865467 | 0.1147476339401475 | 0.5923591472463992 |

The paper claims are tied to generated artifacts rather than prose alone:

| Claim | Primary artifact |
|---|---|
| Exact reproduction | `results/data/benchmarks.csv` |
| No-postselection null behavior | `results/figures/null_test_comparison.png` |
| Fixed-protocol noise diagnostics | `results/figures/noise_survival_atlas.png` |

# Quality control

Validation covers exact benchmark values, final-state trace preservation,
global accounting, zero-coupling behavior, scrambled feedforward, count
bit-order conventions, controller-accounting overheads, optional Qiskit import
guards, and fixed-protocol noise-survival diagnostics. The local quality gate
installs the pinned dependency set and regenerates benchmark and figure
artifacts:

| Environment | Commands |
|---|---|
| Python 3.11 and 3.12 base path | `pytest`; `reproduce_benchmarks.py`; `make_all_figures.py` |
| Python 3.12 optional bridge | `pip install -e ".[qiskit]"`; `run_qiskit_bridge.py` |

# Research impact statement

The immediate scholarly value of `qet-bench` is reproducible reference material
for a known QET model rather than a new physical theorem. It packages exact
values, null tests, cross-checks, figures, and explicit no-free-energy
accounting in a form that can be reused by future QET simulations, teaching
materials, and hardware-oriented studies.

This is a first public release line. Its current impact evidence is therefore
package-level: tagged releases, a lockfile-backed validation path, generated
review artifacts, a pure-Python independent branch check, optional Qiskit/Aer
interoperability, and contribution guidelines. It should not be represented as
a mature community package with demonstrated external adoption.

# Availability and reproducibility

The software repository is
<https://github.com/lucent-lab/qet-bench>. The current review target is
`v0.2.0` with package and citation version `0.2.0`; the latest pre-candidate
project-management checkpoint is tagged as `v0.2.0-blocker-ledger`, and the
earlier clean reproducibility baseline is tagged as `v0.1.0`. Generated
artifacts are tracked for reviewer convenience, but the source of truth is the
package code, tests, scripts, lock file, and artifact manifest.

The public repository has been archived by Software Heritage with snapshot
identifier `swh:1:snp:9636ad3f493c249270cba77ae4810908dce45834`.

The local reproduction path is:

```bash
python -m pip install -e ".[dev]" -c requirements-lock.txt
python -m pytest
python scripts/reproduce_benchmarks.py
python scripts/make_all_figures.py
```

Hosted GitHub Actions CI passed on Python 3.11 and Python 3.12 for the current
review target. Local CI and optional Qiskit/Aer smoke checks are recorded in
`docs/release_validation.md`.

# Limitations

The software covers a two-qubit exact benchmark. The controller/battery layer is
a conservative accounting diagnostic, not a microscopic model of detectors,
memory, pulse generation, or an environment. Noise and readout sweeps are
fixed-protocol diagnostics over named channel families, not universal thresholds
or hardware noise claims. The package does not establish a new QET mechanism,
many-body scaling law, or hardware demonstration.

# AI usage disclosure

Generative AI assistance from OpenAI Codex models, including GPT-5-class models
and GPT-5.4 Mini review agents, was used for code generation, refactoring,
testing, documentation, manuscript drafting, and adversarial review. AI-assisted
changes were checked through exact benchmark regressions, an independent
pure-Python branch implementation, local test suites, artifact regeneration,
and human review before acceptance.

# Acknowledgements

No external funding is declared.

# References
