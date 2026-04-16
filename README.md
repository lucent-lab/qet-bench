# qet-bench

This repository hosts `qet-bench`, a reproducible benchmark suite for the
minimal two-qubit Quantum Energy Teleportation (QET) protocol.

The package lives in [`qet-bench/`](qet-bench/). It implements the exact
Hamiltonian model, Alice measurement, classical feedforward, Bob rotation,
energy ledger, null tests, count estimators, deterministic artifact scripts,
an independent pure-Python reference branch, and an optional Qiskit/Aer
interoperability bridge.

The scientific scope is intentionally narrow: `qet-bench` demonstrates
Bob-side local energy extraction from ground-state correlations while keeping
the global ledger explicit. It does not claim autonomous vacuum power or a
hardware energy source.

## Quickstart

```bash
cd qet-bench
python -m pip install -e ".[dev]" -c requirements-lock.txt
python -m pytest
python scripts/reproduce_benchmarks.py
python scripts/make_all_figures.py
```

Optional Qiskit/Aer smoke check:

```bash
cd qet-bench
python -m pip install -e ".[qiskit]" -c requirements-lock.txt
python scripts/run_qiskit_bridge.py
```

## Review Materials

- [Package README](qet-bench/README.md)
- [Artifact manifest](qet-bench/docs/artifact_manifest.md)
- [Release validation log](qet-bench/docs/release_validation.md)
- [Research roadmap register](qet-bench/docs/research_roadmap.md)
- [Blocker ledger](qet-bench/docs/blocker_ledger.md)
- [Manuscript draft](qet-bench/paper/paper.md)
- [Manuscript build notes](qet-bench/paper/README.md)
