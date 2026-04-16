# Blocker Ledger

This ledger tracks publication, reproducibility, and review blockers across
tags and deliverables. It complements `research_roadmap.md`: the roadmap tracks
stages, while this file tracks risks that must be closed or explicitly carried.

Status values:

- **Open:** blocking or materially risky, with no accepted resolution yet.
- **Processing:** accepted work is in progress, but no merged/tagged resolution
  exists yet.
- **Mitigated:** addressed enough for the current review snapshot, but still
  needs monitoring or stronger external evidence.
- **Closed:** resolved by a merged/tagged deliverable or archival reference.

Reference policy:

- Use a release tag for resolved internal work.
- Use a commit hash only for narrow fixes that are not yet tagged.
- Prefer DOI, Software Heritage ID, hosted CI run URL, or paper DOI when
  available.

Current release identity:

- `v0.2.0` is the active publication-hardening review target.
- `0.2.0` is the package and citation metadata version.
- Earlier `v0.2.0-*` references are historical milestone tags.

| Blocker | Why it matters | Status | Scope | Resolution / Next Action | Reference |
|---|---|---|---|---|---|
| Missing exact benchmark implementation and regression fixtures | Without exact values, the package cannot serve as a reproducible QET benchmark. | Closed | Core software | Implemented exact Hamiltonian, ground state, QET ledger, benchmark CSV, figures, and regression tests. | `v0.1.0` |
| No explicit no-free-energy accounting guardrail | QET is easy to overstate if Alice injection and global accounting are omitted. | Closed | Scientific framing | README, docs, tests, and paper state that Bob extraction is paid for by Alice measurement/control resources and check `E_A >= E_B` for the exact benchmark. | `v0.1.0` |
| Missing artifact provenance | Reviewers need to know which script generated each CSV/figure and what each artifact validates. | Closed | Reproducibility | Added artifact manifest mapping outputs to generators, validation coverage, and supported claims. | `v0.1.0` |
| Hosted CI unavailable because of quota | Hosted CI gives reviewers an independent, visible validation path; local-only validation is weaker. | Closed | Review infrastructure | Repository visibility was changed to public and GitHub Actions passed on Python 3.11 and 3.12. | hosted run <https://github.com/lucent-lab/qet-bench/actions/runs/24507308274> |
| Release archive DOI or Software Heritage ID missing | A GitHub tag is useful, but archival review generally needs a persistent citation target. | Open | Publication metadata | Archive the selected review snapshot, then update `CITATION.cff`, `paper.md`, `paper/README.md`, `research_roadmap.md`, and this ledger. | pending |
| Repository access for external review | Reviewers cannot inspect a private repository unless explicit access is granted. | Closed | Review logistics | Repository visibility is public and the root README now points to package docs, validation records, and manuscript sources. | <https://github.com/lucent-lab/qet-bench> |
| Placeholder software citation metadata | Citation metadata must identify a real citable artifact and author record. | Mitigated | Publication metadata | Replaced placeholder contributor author with provisional author metadata and added preferred software citation fields. Add DOI once archived. | `v0.2.0-paper-review` |
| Manuscript venue ambiguity | Trying to satisfy JOSS, ReScience, and SoftwareX simultaneously weakens the paper. | Mitigated | Manuscript | Reframed `paper.md` as JOSS-style source and moved ReScience/SoftwareX notes to build/readiness documentation. | `v0.2.0-paper-review` |
| Manuscript lacks concrete quality-control evidence | Software venues need reproducible validation commands, versions, and artifact regeneration evidence. | Mitigated | Manuscript/review | Added quality-control table and local Python 3.11/3.12 validation record; hosted CI remains open. | `v0.2.0-paper-review` |
| Contribution and community guidelines missing | Research-software venues expect visible issue/contribution guidance. | Closed | Repository standards | Added `CONTRIBUTING.md` with issue-reporting workflow, test commands, and scope rules. | `v0.2.0-paper-review` |
| Optional Qiskit/Aer dependency could leak into base install | Base reproducibility must not require quantum SDKs or cloud credentials. | Closed | Interoperability | Added lazy optional bridge, optional extra, no-Qiskit tests, and graceful script skip when Qiskit/Aer is absent. | `v0.2.0-qiskit-bridge` |
| Qiskit bit-order ambiguity | Silent count-key reversal would corrupt `Z1` or `X0X1` estimates. | Closed | Interoperability/counts | Added documented `q0q1` canonicalization and explicit fake-count tests. | `v0.2.0-qiskit-bridge` |
| Readout/feedforward terminology confusion | Mixed labels can make a classical sign-flip model sound like a full hardware readout model. | Mitigated | Docs/manuscript | Reworded README and paper to describe the readout sweep as an Alice-bit sign-flip/control-path diagnostic. | `v0.2.0-paper-review` |
| Noise-survival wording could imply universal thresholds | Fixed-protocol simulated diagnostics are not theorem-level thresholds or hardware phase boundaries. | Mitigated | Noise diagnostics | Added anchor-aware atlas wording, interval-average definitions, and repeated non-universal/fixed-protocol language. | `v0.2.0-noise-atlas` |
| Roadmap status was not maintained in a single table | Without a maintained status table, reproduction work and new research territory blur over time. | Closed | Project management | Added `research_roadmap.md` with stage status, classification, deliverable, and release reference. | `v0.2.0-roadmap-register` |
| Blockers were only reported in chat, not tracked in-repo | Chat-only blocker lists are easy to lose and cannot be audited per release. | Processing | Project management | Maintain this blocker ledger and update it when a blocker changes status or is resolved by a tag, commit, DOI, run URL, or paper reference. | pending |
| Optional Aer smoke artifact with Qiskit installed missing | The optional bridge has no positive-path artifact unless Qiskit/Aer is installed and run. | Mitigated | Interoperability | Local Python 3.12.8 smoke passed with `qiskit==2.3.1` and `qiskit-aer==0.17.2`; `qiskit_interop.md` records the generated CSV path and observed absolute `E_B` errors. Decide during archival whether to force-add optional generated artifacts. | pending merge/tag |
| JOSS public-history / external-impact evidence is thin | Some venues screen for sustained public development and evidence of research use. | Open | Venue fit | Prefer ReScience-style reproducibility review first, or wait for public history/adoption before JOSS submission. | pending |
| ReScience-specific reproduced-result framing missing | ReScience-style review needs a crisp statement of the original result being reproduced. | Mitigated | Manuscript | Added `paper/rescience.md`, which names the reproduced two-qubit QET result, artifact bundle, reproduction commands, and interpretation limits. Final author metadata and public repository access remain separate blockers. | pending merge/tag |
| Full microscopic controller/environment ledger missing | Conservative bookkeeping is not a microscopic hardware or thermodynamic environment model. | Open | New methods research | Design and implement an explicit controller, memory, pulse, reset, and environment ledger before making stronger thermodynamic claims. | none |

## Maintenance Checklist

Update this ledger whenever:

1. A blocker is found in review, CI, manuscript work, or external feedback.
2. A blocker changes status.
3. A blocker is resolved by a tag, commit, hosted CI run, DOI/SWHID, or paper
   reference.
4. A roadmap stage creates a new blocker or carries an existing one forward.

Do not delete old blockers just because they are closed. Closed blockers explain
why a release tag exists and what risk it retired.
