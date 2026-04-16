# qet-bench: A Reproducible Software Benchmark for Two-Qubit Quantum Energy Teleportation

## Abstract

We present `qet-bench`, a compact Python benchmark suite for the minimal
two-qubit Quantum Energy Teleportation protocol. The package reproduces exact
benchmark energies, records the Alice and Bob ledger terms, and includes null
tests, noise/readout diagnostics, and a controller-inclusive accounting layer.
The release reproduces the known benchmark and checks that Bob-side local energy
extraction is accompanied by Alice-side energy injection with `E_A >= E_B` in
the exact ground-state protocol. This paper reports a release artifact and
reference implementation; it does not claim a new QET theorem, many-body result,
hardware demonstration, or autonomous energy source.

## Statement of Need

QET is conceptually subtle because it combines ground-state entanglement,
measurement backaction, classical feedforward, and local energy extraction.
The protocol was introduced as a way to use local measurement information to
extract energy from a distant subsystem while preserving global energy
accounting [@hotta2008measurement; @hotta2009spin]. Recent hardware-oriented
work has renewed interest in small, auditable reproductions of the effect
[@ikeda2023hardware]. `qet-bench` is intended to make the minimal example easy
to rerun, test, and extend without requiring a quantum SDK or cloud hardware.
The goal is a stable reference implementation with tests, deterministic outputs,
and a reproducible artifact set.

Small reproducible benchmarks also help separate the real local QET effect from
incorrect interpretations that omit the measurement/control ledger. The
thermodynamic guardrail is the passivity of equilibrium states
[@pusz1978passive] together with explicit accounting for measurement, feedback,
memory reset, and controller work [@landauer1961irreversibility;
@bennett1982thermodynamics; @sagawa2009minimal; @sagawa2010jarzynski].

## Model

This paper documents the exact two-qubit benchmark implemented by `qet-bench`.
The software implements the Hamiltonian `H_tot = H0 + H1 + V` with the analytic
ground state, Alice `X0` measurement, and Bob `Y1` feedforward rotation. All
branches are averaged without postselection.

For `s = sqrt(h^2 + k^2)`, the terms are

```math
H_n=hZ_n+\frac{h^2}{s}I,\quad n=0,1,
```

```math
V=2kX_0X_1+\frac{2k^2}{s}I.
```

The constants set the analytic ground energy to zero, making the injected and
extracted energy ledger directly testable.

## Energy Accounting

The reported ledger includes `E_A`, `H1`, `V`, `E1`, `E_B`, and
`E_A - E_B`. In the reproduced benchmark, the ledger satisfies
`E_A - E_B >= 0` within numerical tolerance.

The controller-inclusive extension adds explicit nonnegative overheads for
measurement-record reset, classical communication, Bob's control pulse, state
preparation, and calibration. This layer is a conservative accounting
diagnostic, not a microscopic battery model or hardware validation. It reports

```math
W_\mathrm{net}=E_B-E_A-W_\mathrm{controller},
```

which is reported as nonpositive for the ground-state protocol under the stated
nonnegative-overhead assumptions.

## Canonical Regression Benchmarks

The first benchmark point is `h=1, k=0.5`; the second is `h=1, k=1`. Both are
encoded as regression tests and release artifacts with absolute tolerance
`1e-9`.

| `h` | `k` | `E_A` | `H1` | `V` | `E1` | `E_B` |
|---:|---:|---:|---:|---:|---:|---:|
| 1.0 | 0.5 | 0.8944271909999154 | 0.1873204098133684 | -0.2598931856865897 | -0.0725727758732213 | 0.0725727758732213 |
| 1.0 | 1.0 | 0.7071067811865467 | 0.2598931856865898 | -0.3746408196267373 | -0.1147476339401475 | 0.1147476339401475 |

## Null Tests

Null tests cover zero coupling, scrambled feedforward, a product-state
reference, wrong-angle scans, and Bob-only random local unitaries. These are
deterministic diagnostics for correctness and convention handling, not evidence
of new physics.

## Noise/Readout Sweeps

The release includes generated sweeps for classical feedforward/readout errors,
dephasing, depolarizing noise, amplitude damping, and Bob-angle miscalibration.
Open-system channel sweeps report the environment exchange term as a model
diagnostic rather than as a closed thermodynamic ledger. The readout sweep is
the symmetric Alice-bit sign-flip model used by Bob's classical feedforward,
not a full count-corruption model. The fixed-protocol survival atlas extends
these diagnostics to a small predeclared `(h, k)` anchor set and reports
interval-averaged survival ratios over the sampled scan interval. These sweeps
are deterministic diagnostics and sensitivity checks; they are not threshold
results or universal robustness claims.

## Software Architecture

The package is organized as small modules: Pauli helpers, Hamiltonian
construction, exact protocol simulation, ledgers, null tests, noise channels,
count estimators, sweep utilities, statistics, controller accounting, and
plotting. It uses NumPy, SciPy, pandas, and Matplotlib
[@harris2020array; @virtanen2020scipy; @mckinney2010data; @hunter2007matplotlib].
The release artifact manifest maps each CSV and figure to its generating script,
source data, and test coverage. The primary reproduction path is:

```bash
python -m pip install -e ".[dev]" -c requirements-lock.txt
python -m pytest
python scripts/reproduce_benchmarks.py
python scripts/make_all_figures.py
```

## Availability and Reproducibility

The software is available at
<https://github.com/lucent-lab/qet-bench>. The reproducibility snapshot for this
paper is the `v0.1.0` tag. The release tracks generated `results/` artifacts for
reviewer convenience, but the source of truth is the package code, tests,
scripts, `requirements-lock.txt`, and the artifact manifest in
`docs/artifact_manifest.md`.

Local verification for the `v0.1.0` release was run with the pinned install path
on Python 3.11 and Python 3.12. The validation commands installed the package,
ran the test suite, reproduced the canonical benchmark CSV, and regenerated all
figures. Hosted GitHub Actions CI is configured, but at the time of this draft
the organization runner quota prevented hosted jobs from starting; local CI is
therefore the validation record for the current release.

## Limitations

This release is a two-qubit exact benchmark. The controller/battery layer is a
conservative accountant, not a microscopic detector, memory, pulse generator, or
hardware backend. It does not establish a new many-body threshold or an
experimental hardware claim. This release does not claim a new QET mechanism,
many-body scaling law, threshold theorem, or hardware demonstration.

Before submission, the remaining venue-specific risks are citation-style
adaptation, author and affiliation metadata, template formatting, and any
journal-specific archival requirements for the generated artifacts.

## References

See `references.bib`.
