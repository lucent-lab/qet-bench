# Contributing

`qet-bench` is a narrow reproducibility package for the exact two-qubit QET
benchmark. Contributions should preserve the no-postselection protocol, the
explicit Alice/Bob energy ledger, and the no-free-energy wording.

## Reporting Issues

Open a GitHub issue with:

- the command you ran,
- the Python version,
- the package version or commit hash,
- the full error output,
- and whether generated artifacts changed.

For scientific issues, include the relevant `(h, k)` parameters, the expected
ledger quantity, and the artifact or test that exposes the discrepancy.

## Development Workflow

Before submitting a pull request, run:

```bash
python -m pip install -e ".[dev]" -c requirements-lock.txt
python -m pytest
python scripts/reproduce_benchmarks.py
python scripts/make_all_figures.py
```

If your change adds optional Qiskit/Aer behavior, the base test suite must still
pass without Qiskit installed. Optional Qiskit checks should skip cleanly when
the extra dependencies are absent.

## Scope Rules

- Keep runtime dependencies limited to NumPy, SciPy, pandas, and Matplotlib
  unless a dependency is optional.
- Do not postselect Alice measurement branches.
- Do not describe QET as free energy or as an autonomous power source.
- Treat noise and readout studies as fixed-protocol diagnostics unless a full
  environment/controller ledger is explicitly implemented and documented.
- Keep generated artifacts deterministic and mapped in
  `docs/artifact_manifest.md`.
