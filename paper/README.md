# OGX Technical Whitepaper (LaTeX)

This directory holds `ogx.tex` (and its build artifacts `ogx.bbl`, `ogx.pdf`,
`references.bib`), a standalone, diagram-heavy technical whitepaper. **It is a
separate document from the JOSS submission**, not an alternate build of it.

- **JOSS manuscript:** [`paper.md`](https://github.com/ogx-ai/ogx/blob/3488671553dc8c97391decefe9c195c7d7208bf5/paper.md)
  and [`paper.bib`](https://github.com/ogx-ai/ogx/blob/3488671553dc8c97391decefe9c195c7d7208bf5/paper.bib)
  at commit `3488671553dc8c97391decefe9c195c7d7208bf5`, including the
  revised deployment wording and versioned software and operator citations
  recorded below. These links identify the manuscript independently of the
  software release tag.
- **This whitepaper:** `ogx.tex`, built against `references.bib` and `ogx.bbl`
  in this directory. It shares subject matter with `paper.md` but is
  maintained independently, is not kept in lockstep with it, and is not part
  of the JOSS submission.

Both documents currently share the same title, which has caused confusion
about which one the JOSS proof corresponds to. If you're looking for the JOSS
manuscript, use the pinned links above.

## Revisions referenced by the paper

For reproducibility, the three revisions the manuscript describes are recorded
together here rather than only individually in `paper.bib`:

| Component | Revision | Reference |
| --- | --- | --- |
| OGX software | `v1.0.2` | commit `9424b4d9e5eca99bfc79a6e0004e28adf5f58704` |
| OGX Kubernetes Operator | `v0.10.0` | most recent tag as of the paper's 2 June 2026 date (see `paper.bib`) |
| Manuscript (`paper.md` / `paper.bib`) | -- | commit `3488671553dc8c97391decefe9c195c7d7208bf5` |

The [existing JOSS proof](https://github.com/openjournals/joss-papers/blob/28806e6eceeb8d146d178df7f4194fa2549ad4fc/joss.11234/10.21105.joss.11234.pdf)
predates these manuscript updates and still uses the unversioned software
and operator citations from the [previous source snapshot](https://github.com/ogx-ai/ogx/tree/40eb48a6e2319a5804881a3c72b30db197d976b4).
After merging the updates, run `@editorialbot generate pdf` on the
[JOSS review issue](https://github.com/openjournals/joss-reviews/issues/11234)
to generate a proof with the revised wording and versioned citations.
