# qet-bench

`qet-bench` is a reproducible benchmark suite for the minimal two-qubit Quantum
Energy Teleportation (QET) protocol. It implements the exact Hamiltonian model,
Alice measurement, classical feedforward, Bob rotation, energy ledger, null
tests, count-based estimators, and deterministic figure scripts.

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
wrong-angle scan, feedforward/readout error sweeps, dephasing, depolarizing,
amplitude-damping, Bob-angle miscalibration, and coarse sampled crossing
summaries.

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
  uncertainty propagation, sweeps, controller/battery accounting, and plotting.
- `scripts/`: reproduction and figure-generation entry points.
- `tests/`: regression tests for exact values, accounting, null behavior, and
  count-estimator conventions.
- `docs/`: scientific notes for the first deliverable.
- `paper/`: manuscript skeleton and reference placeholder.

## Publication Target

The first target is a reproducibility or research-software submission: an
independent exact implementation, canonical regression values, null tests,
noise/readout diagnostics, command-line reproduction scripts, figures, and a
manuscript scaffold. A later physics-paper route would require an additional
scientific result beyond reproducing the two-qubit benchmark.

## Controller/Battery Extension

The `qet_bench.controller` module wraps the exact ledger with nonnegative
controller costs and reports `net_battery_gain = E_B - E_A - overhead`. This is
an accounting extension, not a microscopic hardware model, and it keeps the
measurement, communication, reset, and pulse resources explicit.

## Reproducibility Notes

`requirements-lock.txt` pins the dependency set used by CI and local
reproduction. `pyproject.toml` keeps broad package dependencies so the library
can still be installed in newer scientific Python environments.
