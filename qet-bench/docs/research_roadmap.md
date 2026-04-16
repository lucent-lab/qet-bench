# Research Roadmap Register

This register tracks the project roadmap at publication granularity. It should
be updated whenever a stage changes status, a release tag is cut, or an archive
DOI becomes available.

For the step-by-step path from the QET benchmark into broader void/vacuum
energy-accounting work, see `vacuum_investigation_roadmap.md`. For review risks
and submission blockers, see `blocker_ledger.md`. For the current local
validation record while hosted CI is unavailable, see `release_validation.md`.

Status values:

- **Done:** implemented, locally verified, merged, and tagged.
- **Processing:** active or accepted next work, but not yet a reviewed release.
- **Not done:** planned or candidate work with no accepted release artifact.

Reference policy:

- Use a release tag for completed internal milestones.
- Add an archive DOI, Software Heritage ID, or paper DOI when available.
- For active work without a tag, use "pending" and replace it when merged.

| Stage | Status | Reproduction Or New Territory | Deliverable | Reference |
|---|---|---|---|---|
| Exact two-qubit QET benchmark package | Done | Reproduction | Minimal exact simulator, Hamiltonians, ledgers, null tests, count estimators, deterministic benchmark scripts, generated artifacts, artifact manifest. | `v0.1.0` |
| Repository hygiene and local CI path | Done | Reproduction hardening | `.gitignore`, GitHub Actions workflow, pinned requirements lock, local CI recipe for Python 3.11 and 3.12. Hosted CI remains billing/quota-blocked until re-run. | `v0.1.0` |
| Controller accounting extension | Done | Accounting extension; not new microscopic physics | Conservative nonnegative controller-cost ledger and documentation. Reports diagnostic net battery gain without claiming a hardware battery model. | `v0.1.0` |
| Manuscript release provenance | Done | Publication hardening | Paper build notes, release-provenance wording, local verification record, and submission-risk notes. | `v0.2.0-manuscript` |
| Independent pure-Python reference branch | Done | Reproduction cross-check | Branch-amplitude implementation independent of the NumPy matrix propagation path, with benchmark and branch-audit artifacts. | `v0.2.0-manuscript` |
| Optional Qiskit/Aer interoperability bridge | Done | Reproduction/interoperability | Lazy optional Qiskit/Aer adapter, count-key canonicalizer, branch-resolved ideal-circuit script, docs, and tests that pass without Qiskit installed. | `v0.2.0-qiskit-bridge` |
| Fixed-protocol noise-survival atlas | Done | New simulation diagnostic; not a universal threshold result | Anchor-aware survival curves and summaries across a predeclared `(h, k)` set, interval-averaged survival ratios, and small-multiples figures. | `v0.2.0-noise-atlas` |
| JOSS-style manuscript hardening | Done | Publication hardening | JOSS-shaped `paper.md`, stricter venue notes, claim-to-artifact map, quality-control table, expanded citation metadata, and contribution guidelines. | `v0.2.0-paper-review` |
| Public archive and DOI | Processing | Publication hardening | Archive the chosen review snapshot with Zenodo, Software Heritage, or equivalent; update `CITATION.cff`, `paper.md`, and this register with DOI/SWHID. | pending |
| Hosted CI revalidation | Processing | Reproduction hardening | Re-run GitHub Actions once billing/quota permits; latest hosted jobs were blocked before execution, so `release_validation.md` records the local Python 3.11/3.12 validation substitute. | pending; blocked run <https://github.com/lucent-lab/qet-bench/actions/runs/24506144229> |
| Optional Aer smoke artifact with Qiskit installed | Processing | Reproduction/interoperability | Local Python 3.12.8 smoke passed with `qiskit==2.3.1` and `qiskit-aer==0.17.2`; document the generated comparison artifact and close after merge/tag. | pending |
| ReScience-style reproducibility package | Processing | Reproduction publication | `paper/rescience.md` frames the work as an exact reproduction of the two-qubit QET benchmark with validation artifacts and bounded novelty claims; close after merge/tag and final author metadata confirmation. | pending |
| Full microscopic controller/environment ledger | Not done | New methods territory | Replace conservative bookkeeping diagnostics with an explicit modeled controller, memory reset, pulse, and environment exchange ledger. | none |
| Many-qubit QET extension | Not done | New physics/simulation territory | Extend beyond two qubits to chains or network geometries, with explicit local-energy partitions and finite-size/scaling diagnostics. | none |
| Finite-temperature or mixed-state QET | Not done | New physics/simulation territory | Study thermal or mixed resource states and compare extraction/accounting behavior against the pure ground-state benchmark. | none |
| DCE/Casimir/ultrastrong-coupling audit module | Not done | New vacuum-mechanism audit territory | Add a separate module that tracks pump, switching, reset, and environment work for one non-QET vacuum-adjacent mechanism. | none |
| Hardware or hardware-faithful execution | Not done | New experimental/hardware-simulation territory | Define a circuit/backend protocol, calibration assumptions, count-processing path, and bounded interpretation for real or hardware-faithful execution. | none |

## Maintenance Checklist

When updating this table:

1. Keep "Reproduction Or New Territory" conservative. Reimplementing the same
   benchmark in another stack is reproduction unless it changes the scientific
   question.
2. Do not mark a stage **Done** until it is merged, locally verified, and
   tagged or archived.
3. Replace tag-only references with DOI/SWHID references when archival records
   exist.
4. Update `blocker_ledger.md` when a stage opens, carries, mitigates, or closes
   a review blocker.
5. Keep no-free-energy and fixed-protocol/no-threshold language visible for any
   stage involving accounting, noise, or hardware.
