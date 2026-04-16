# Manuscript Build Target

The first manuscript target is a reproducibility or research-software submission
using `paper.md` as the source text and `references.bib` as the citation file.

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

Current intended targets:

- ReScience C or a comparable reproducibility venue if framed as an independent
  exact reproduction and validation suite.
- JOSS, SoftwareX, or JORS if framed as reusable research software.

