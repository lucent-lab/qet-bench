# Manuscript Build Target

The first manuscript target is a reproducibility or research-software submission
using `paper.md` as the source text and `references.bib` as the citation file.
The current text is journal-neutral and should be adapted to the target venue's
template before submission.

Release target:

- Repository: <https://github.com/lucent-lab/qet-bench>
- Release tag: `v0.1.0`
- Citation metadata: `../CITATION.cff`
- Artifact manifest: `../docs/artifact_manifest.md`
- Bibliography source: `references.bib`

Preferred build path:

```bash
pandoc paper.md \
  --from markdown \
  --citeproc \
  --bibliography references.bib \
  --output qet-bench-manuscript.pdf
```

The manuscript is intentionally journal-neutral for the first review pass.
Before submission, choose the target venue and add the required template,
metadata, citation style, author list, availability statement, and generated
figure references.

Verification record for `v0.1.0`:

```bash
python -m pip install --upgrade -c requirements-lock.txt pip setuptools wheel
python -m pip install -e ".[dev]" -c requirements-lock.txt
python -m pytest
python scripts/reproduce_benchmarks.py
python scripts/make_all_figures.py
```

These commands were run locally on Python 3.11 and Python 3.12. Hosted GitHub
Actions is configured, but hosted jobs were blocked by organization runner
quota at the time this note was written.

Current intended targets:

- ReScience C or a comparable reproducibility venue if framed as an independent
  exact reproduction and validation suite.
- JOSS, SoftwareX, or JORS if framed as reusable research software.
