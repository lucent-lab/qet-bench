# Manuscript Build Target

The manuscript set now contains a JOSS-style research-software source and a
ReScience-oriented reproducibility source. SoftwareX would still require a
separate template adaptation.

Current review targets:

- Repository: <https://github.com/lucent-lab/qet-bench>
- Current review target: `v0.2.0`
- Package/CFF version: `0.2.0`
- Latest pre-candidate checkpoint: `v0.2.0-blocker-ledger`
- Clean reproducibility baseline: `v0.1.0`
- Citation metadata: `../CITATION.cff`
- Artifact manifest: `../docs/artifact_manifest.md`
- Release validation log: `../docs/release_validation.md`
- JOSS-style source: `paper.md`
- ReScience-oriented source: `rescience.md`
- Bibliography source: `references.bib`

## Local Build

Generic Pandoc smoke build:

```bash
pandoc paper.md \
  --from markdown \
  --citeproc \
  --bibliography references.bib \
  --output qet-bench-manuscript.pdf
```

JOSS-compatible build, when Docker is available:

```bash
docker run --rm \
  --volume "$PWD":/data \
  --user "$(id -u):$(id -g)" \
  --env JOURNAL=joss \
  openjournals/inara
```

## Submission Blockers

The paper text is not yet a final submission. The hard blockers are:

| Area | Required before submission |
|---|---|
| Author metadata | Confirm author list, affiliations, ORCID identifiers, and corresponding author. |
| Archival DOI | Archive the target release with Zenodo, Software Heritage, or equivalent and update the paper metadata. |
| Repository access | Ensure the GitHub repository is public or that reviewers have explicit access. |
| Public history | JOSS currently screens for sustained public development history and research impact; submit to JOSS only after those signals exist. |
| Hosted CI | Re-run GitHub Actions when quota is available, or clearly document local CI as the validation record for a reproducibility venue. |
| Community guidelines | Keep `../CONTRIBUTING.md` current and make sure issue reporting and contribution workflow are visible from the repository root. |
| Funding/COI | Replace the draft acknowledgement with explicit funding and conflict statements. |
| AI disclosure | Human author must verify the AI usage disclosure is complete and accurate. |
| Venue template | ReScience C now has a dedicated source file; SoftwareX still requires its own article template and metadata. |

Verification record for the `v0.2.0` review target:

```bash
python -m pip install --upgrade -c requirements-lock.txt pip setuptools wheel
python -m pip install -e ".[dev]" -c requirements-lock.txt
python -m pytest
python scripts/reproduce_benchmarks.py
python scripts/make_all_figures.py
```

These commands were run locally on Python 3.11 and Python 3.12. Hosted GitHub
Actions is configured, but hosted jobs were blocked before execution by the
account billing/spending limit at the time this note was written. The latest
blocked hosted run was
<https://github.com/lucent-lab/qet-bench/actions/runs/24507161016>.

## Venue Fit

| Venue | Fit | Main risk |
|---|---|---|
| ReScience C or comparable reproducibility venue | Strongest near-term fit; `rescience.md` frames the work as exact reproduction plus validation suite. | Must keep novelty claims bounded and ensure the repository is public before submission. |
| JOSS | Good format fit after public-history and impact signals mature. | Immediate submission risks desk rejection if public development history and adoption evidence are insufficient. |
| SoftwareX | Possible if expanded into the required template and impact/reuse narrative. | SoftwareX expects a descriptive paper plus an open-source distribution and stronger reuse framing. |
