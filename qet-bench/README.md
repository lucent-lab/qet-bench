# qet-bench

`qet-bench` is a reproducible benchmark suite for the minimal two-qubit Quantum
Energy Teleportation (QET) protocol. It implements the exact Hamiltonian model,
Alice measurement, classical feedforward, Bob rotation, energy ledger, null
tests, count-based estimators, and deterministic figure scripts.
It also includes a pure-Python reference branch implementation that cross-checks
the exact benchmark without using the main NumPy matrix propagation path.

The scientific target is narrow and explicit: demonstrate Bob-side local energy
extraction from an entangled ground state after Alice measurement and classical
feedforward, while showing that the global ledger obeys

```math
E_A \ge E_B.
```

## No-Free-Energy Warning

QET is not a vacuum power source. In this benchmark, Alice's measurement injects
energy and supplies the classical control information used by Bob. Bob's local
extraction is paid for by those resources, and the reported global accounting
gap `E_A - E_B` is nonnegative for the exact ground-state protocol.

## Quickstart

```bash
pip install -e ".[dev]" -c requirements-lock.txt
pytest
python scripts/reproduce_benchmarks.py
python scripts/make_all_figures.py
```

The scripts write reproducible artifacts under `results/data/` and
`results/figures/`.

`make_all_figures.py` emits the exact ledger sweep, null-test diagnostics,
wrong-angle scan, Alice-bit sign-flip/readout-control sweeps, dephasing,
depolarizing, amplitude-damping, Bob-angle miscalibration, and coarse sampled crossing
summaries. It also emits fixed-protocol noise-survival diagnostics across a
small predeclared `(h, k)` anchor set using the ratio
`R(lambda)=E_B(lambda)/E_B(0)`.

See [docs/artifact_manifest.md](docs/artifact_manifest.md) for the full
CSV/figure provenance table. See
[docs/research_roadmap.md](docs/research_roadmap.md) for the maintained
roadmap table that separates reproduction work from new research territory and
records milestone tags. See
[docs/release_validation.md](docs/release_validation.md) for the current local
validation log while hosted GitHub Actions runners are unavailable. See
[docs/vacuum_investigation_roadmap.md](docs/vacuum_investigation_roadmap.md)
for the step-by-step path from QET benchmarks toward deeper vacuum-energy
accounting audits. See [docs/blocker_ledger.md](docs/blocker_ledger.md) for
the maintained review/submission blocker ledger.

## Optional Qiskit/Aer Bridge

Qiskit and Qiskit Aer are optional interoperability dependencies, not part of
the base reproducibility path. The bridge provides branch-resolved ideal
circuits and a count-key normalizer for Qiskit's bitstring convention:

```bash
pip install -e ".[qiskit]"
python scripts/run_qiskit_bridge.py
```

The bridge keeps the exact ledger as the source of truth and does not require
hardware backends, cloud credentials, or dynamic-circuit support. See
[docs/qiskit_interop.md](docs/qiskit_interop.md) for the bit-order contract.

## Artifact Manifest

| Artifact | Script | What it validates |
|---|---|---|
| `results/data/benchmarks.csv` | `scripts/reproduce_benchmarks.py` | Exact benchmark values for the two quoted parameter points and the final-state trace check. |
| `results/data/h_over_k_sweep.csv` | `scripts/run_parameter_sweep.py` | Smooth ledger behavior across the main `h/k` scan. |
| `results/figures/energy_ledger_vs_h_over_k.png` | `scripts/run_parameter_sweep.py` | Visual ledger check for the exact protocol as coupling ratio varies. |
| `results/data/feedforward_error_sweep.csv` | `scripts/run_noise_sweeps.py` | Sensitivity to scrambled classical feedforward. |
| `results/figures/eb_vs_feedforward_error.png` | `scripts/run_noise_sweeps.py` | Monotone loss or reversal of Bob extraction under feedforward error. |
| `results/data/readout_error_sweep.csv` | `scripts/run_noise_sweeps.py` | Symmetric Alice-bit sign-flip model labeled for the readout/control path, not a full count-corruption model. |
| `results/figures/eb_vs_readout_error.png` | `scripts/run_noise_sweeps.py` | Alice-bit sign-flip diagnostic for the classical control path. |
| `results/data/dephasing_sweep.csv` | `scripts/run_noise_sweeps.py` | Bob-side phase noise sensitivity. |
| `results/data/depolarizing_sweep.csv` | `scripts/run_noise_sweeps.py` | Bob-side depolarizing noise sensitivity. |
| `results/data/amplitude_damping_sweep.csv` | `scripts/run_noise_sweeps.py` | Bob-side amplitude-damping sensitivity. |
| `results/data/bob_angle_miscalibration_sweep.csv` | `scripts/run_noise_sweeps.py` | Robustness to Bob-angle miscalibration. |
| `results/data/noise_crossings.csv` | `scripts/run_noise_sweeps.py` | Coarse sampled crossing metadata for the noise sweeps. |
| `results/data/k_zero_scan.csv` | `scripts/run_null_tests.py` | Vanishing extraction in the `k \to 0` null limit. |
| `results/data/scrambled_bit_scan.csv` | `scripts/run_null_tests.py` | Loss of extraction as the feedforward bit is randomized. |
| `results/data/wrong_angle_scan.csv` | `scripts/run_null_tests.py` | Bob-angle scan against the analytic optimum. |
| `results/data/bob_only_random_scan.csv` | `scripts/run_null_tests.py` | Diagnostic upper bound for Bob-only local unitaries. |
| `results/data/null_tests_summary.json` | `scripts/run_null_tests.py` | Compact summary of the null-test outcomes. |
| `results/figures/null_test_comparison.png` | `scripts/run_null_tests.py` | Side-by-side null-test comparison figure. |
| `results/figures/wrong_angle_scan.png` | `scripts/run_null_tests.py` | Bob-angle miscalibration figure. |

## Exact Benchmarks

| h | k | E_A | H1 | V | E1 | E_B |
|---:|---:|---:|---:|---:|---:|---:|
| 1.0 | 0.5 | 0.8944271909999154 | 0.1873204098133684 | -0.2598931856865897 | -0.0725727758732213 | 0.0725727758732213 |
| 1.0 | 1.0 | 0.7071067811865467 | 0.2598931856865898 | -0.3746408196267373 | -0.1147476339401475 | 0.1147476339401475 |

## Model Summary

The two-qubit Hamiltonian is

```math
H_\mathrm{tot}=H_0+H_1+V,
```

with

```math
H_n = h Z_n + \frac{h^2}{\sqrt{h^2+k^2}} I,\quad
V = 2k X_0 X_1 + \frac{2k^2}{\sqrt{h^2+k^2}} I.
```

Alice measures `X0`, Bob applies an outcome-conditioned `Y1` rotation, and all
measurement outcomes are averaged. The package never postselects branches.

## Repository Layout

- `src/qet_bench/`: exact model, ledgers, null tests, noise helpers, counts,
  uncertainty propagation, sweeps, controller/battery accounting, optional
  Qiskit/Aer interop, and plotting.
- `scripts/`: reproduction and figure-generation entry points.
- `tests/`: regression tests for exact values, accounting, null behavior, and
  count-estimator conventions.
- `docs/`: scientific notes for the first deliverable.
- `paper/`: JOSS-style manuscript draft, build notes, and bibliography.

## Publication Target

The first target is a reproducibility or research-software submission: an
independent exact implementation, canonical regression values, null tests,
noise/readout diagnostics, command-line reproduction scripts, figures, and a
manuscript scaffold. A later physics-paper route would require an additional
scientific result beyond reproducing the two-qubit benchmark.

## Controller Accounting Extension

The `qet_bench.controller` module wraps the exact ledger with nonnegative
controller costs and reports the diagnostic key
`net_battery_gain = E_B - E_A - overhead`. This is a conservative accounting
extension, not a microscopic hardware or battery model, and it keeps the
measurement, communication, reset, and pulse resources explicit.

## Reproducibility Notes

`requirements-lock.txt` pins the dependency set used by CI and local
reproduction. `pyproject.toml` keeps broad package dependencies so the library
can still be installed in newer scientific Python environments.
