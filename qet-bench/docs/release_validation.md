# Release Validation Log

This log records local validation for review snapshots while hosted GitHub
Actions jobs are unavailable. Hosted CI remains the preferred independent
validation path once account billing/quota allows runners to start.

## v0.2.0 Review Target

Date: 2026-04-16

Hosted CI status:

- Workflow: `.github/workflows/ci.yml`
- Latest hosted run checked:
  <https://github.com/lucent-lab/qet-bench/actions/runs/24506144229>
- Result: jobs did not start because the account billing/spending limit blocked
  hosted runners.

Local CI mirror:

| Python | Environment | Commands | Result |
|---|---|---|---|
| 3.11.6 | `/tmp/qet-bench-py311` | `pip install -e ".[dev]" -c requirements-lock.txt`; `pytest`; `scripts/reproduce_benchmarks.py`; `scripts/make_all_figures.py` | `40 passed, 1 skipped`; benchmark and figure scripts completed with no tracked artifact diff. |
| 3.12.8 | `.venv` | `pip install -e ".[dev,qiskit]" -c requirements-lock.txt`; `pytest`; `scripts/reproduce_benchmarks.py`; `scripts/make_all_figures.py`; `scripts/run_qiskit_bridge.py`; Pandoc citation smoke build | `39 passed, 2 skipped`; benchmark and figure scripts completed with no tracked artifact diff; optional Qiskit/Aer bridge completed; Pandoc wrote `/tmp/qet-bench-manuscript.html`. |

Optional Qiskit/Aer bridge:

- `qiskit==2.3.1`
- `qiskit-aer==0.17.2`
- Generated file: `results/data/qiskit_bridge_benchmarks.csv`
- Absolute `E_B` errors:
  - `(h=1, k=0.5)`: approximately `0.01553`
  - `(h=1, k=1)`: approximately `0.00279`

The optional bridge artifact lives under the ignored `results/` tree unless a
future release deliberately force-adds optional interoperability outputs.

