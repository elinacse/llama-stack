# OGX Technical Whitepaper (LaTeX)

This directory holds `ogx.tex` (and its build artifacts `ogx.bbl`, `ogx.pdf`,
`references.bib`), a standalone, diagram-heavy technical whitepaper. **It is a
separate document from the JOSS submission**, not an alternate build of it.

- **JOSS manuscript:** [`paper.md`](https://github.com/ogx-ai/ogx/blob/40eb48a6e2319a5804881a3c72b30db197d976b4/paper.md)
  and [`paper.bib`](https://github.com/ogx-ai/ogx/blob/40eb48a6e2319a5804881a3c72b30db197d976b4/paper.bib)
  at commit `40eb48a6e2319a5804881a3c72b30db197d976b4` -- the last commit on the
  default branch that changed either file, and the manuscript revision the
  generated JOSS proof (openjournals/joss-reviews#11234) corresponds to. These
  are pinned to that exact commit, not the moving default branch, because
  `paper.md`/`paper.bib` are not carried into software release tags (`v1.0.2`
  does not contain them), so a tag alone cannot identify which manuscript
  revision a given proof was built from.
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
| Manuscript (`paper.md` / `paper.bib`) | -- | commit `40eb48a6e2319a5804881a3c72b30db197d976b4` |

If the manuscript commit above is not confirmed to be the one the existing
JOSS proof PDF was actually generated from, a maintainer should run
`@editorialbot generate pdf` against that exact commit on the review issue to
produce a proof that matches it, and update this table if the confirmed
commit differs.
