# qet-bench: Exact Two-Qubit Quantum Energy Teleportation Benchmarks

## Abstract

We present `qet-bench`, a compact Python benchmark suite for the minimal
two-qubit Quantum Energy Teleportation protocol. The package reproduces exact
benchmark energies, records the Alice and Bob ledger terms, and includes null
tests, noise/readout diagnostics, and a controller-inclusive accounting layer.
The central accounting result is that Bob-side local energy extraction is
accompanied by Alice-side energy injection and satisfies `E_A >= E_B` in the
exact ground-state protocol.

## Statement of Need

QET is conceptually subtle because it combines ground-state entanglement,
measurement backaction, classical feedforward, and local energy extraction.
The protocol was introduced as a way to use local measurement information to
extract energy from a distant subsystem while preserving global energy
accounting [@hotta2008measurement; @hotta2009spin]. Recent hardware-oriented
work has renewed interest in small, auditable reproductions of the effect
[@ikeda2023hardware]. `qet-bench` is intended to make the minimal example easy
to rerun, test, and extend without requiring a quantum SDK or cloud hardware.

Small reproducible benchmarks also help separate the real local QET effect from
incorrect interpretations that omit the measurement/control ledger. The
thermodynamic guardrail is the passivity of equilibrium states
[@pusz1978passive] together with explicit accounting for measurement, feedback,
memory reset, and controller work [@landauer1961irreversibility;
@bennett1982thermodynamics; @sagawa2009minimal; @sagawa2010jarzynski].

## Model

The software implements the two-qubit Hamiltonian `H_tot = H0 + H1 + V` with the
analytic ground state, Alice `X0` measurement, and Bob `Y1` feedforward rotation.
All branches are averaged without postselection.

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
`E_A - E_B`. The exact ground-state protocol is required to satisfy
`E_A - E_B >= 0` within numerical tolerance.

The controller-inclusive extension adds explicit nonnegative overheads for
measurement-record reset, classical communication, Bob's control pulse, state
preparation, and calibration. It reports

```math
W_\mathrm{net}=E_B-E_A-W_\mathrm{controller},
```

which must remain nonpositive for the ground-state protocol when all controller
costs are nonnegative.

## Exact Reproduction Benchmarks

The first benchmark point is `h=1, k=0.5`; the second is `h=1, k=1`. Both are
included as regression tests with absolute tolerance `1e-9`.

| `h` | `k` | `E_A` | `H1` | `V` | `E1` | `E_B` |
|---:|---:|---:|---:|---:|---:|---:|
| 1.0 | 0.5 | 0.8944271909999154 | 0.1873204098133684 | -0.2598931856865897 | -0.0725727758732213 | 0.0725727758732213 |
| 1.0 | 1.0 | 0.7071067811865467 | 0.2598931856865898 | -0.3746408196267373 | -0.1147476339401475 | 0.1147476339401475 |

## Null Tests

Null tests cover zero coupling, scrambled feedforward, a product-state
reference, wrong-angle scans, and Bob-only random local unitaries.

## Noise/Readout Sweeps

The first release includes generated sweeps for classical feedforward/readout
errors, dephasing, depolarizing noise, amplitude damping, and Bob-angle
miscalibration. Open-system channel sweeps report the environment exchange term
as a model diagnostic rather than as a closed thermodynamic ledger. The readout
sweep is the symmetric Alice-bit sign-flip model used by Bob's classical
feedforward, not a full count-corruption model.

## Software Architecture

The package is organized as small modules: Pauli helpers, Hamiltonian
construction, exact protocol simulation, ledgers, null tests, noise channels,
count estimators, sweep utilities, statistics, controller accounting, and
plotting. It uses NumPy, SciPy, pandas, and Matplotlib
[@harris2020array; @virtanen2020scipy; @mckinney2010data; @hunter2007matplotlib].

## Limitations

This release is a two-qubit exact benchmark. The controller/battery layer is a
conservative accountant, not a microscopic detector, memory, pulse generator, or
hardware backend. It does not establish a new many-body threshold or an
experimental hardware claim.

## References

See `references.bib`.

