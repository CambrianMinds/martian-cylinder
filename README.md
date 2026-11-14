# Martian cylinder investigation

Quantitative boundary metrology of Curiosity Sol 3556 Mastcam-100 product `3556MR1025170721700585C00`.

**Author:** Justin Bogner, Cambrian Minds Media. The current technical manuscript is the 13 November 2026 journal revision, *Subpixel Geometric Reconstruction of a Cylindrical Candidate in Curiosity Mastcam-100 Imagery*, subtitled *Boundary metrology, frozen-shape prediction, and geological comparison*.

## Current documents

- [Technical paper PDF](papers/martian-cylinder-technical-paper.pdf) and [LaTeX source](papers/martian-cylinder-technical-paper.tex).
- [Journal revision report](papers/journal-revision-report.md) and [numerical/provenance verification](papers/journal-numerical-verification.json).
- [Narrative essay, revision 16](teaching-myself-the-scientific-method-rev16.md).
- [Technical summary](independent-reconstruction/report.md), [plain-language summary](independent-reconstruction/report_layman.md), and [methods guide](independent-reconstruction/methods.md).
- [Geological comparison](audit/comparative-study/report.md), [predictive validation](audit/predictive-validation/report.md), and [M4/finite-boundary reevaluation](audit/sediment-pipe-comparison/m4-reevaluation.md).
- [Repository repair record](papers/repository-repair.md). Superseded documents are retained in [archive](archive/README.md).

## Measured results and interpretation

The retained near-rim, exposed rear-arc and dorsal-boundary families contain 35, 24 and 26 stations. A six-parameter common-section, common-axis image-plane model with an exact tangent line fits these 85 coordinates at 0.3788 pixels RMS. The geometry exhibits manufacturing-like regularity and motivates manufacture as a hypothesis. The complete three-dimensional shape, composition and origin remain unresolved.

| Coordinate-level test | RMS, native pixels |
| --- | ---: |
| Strict M1, all 85 stations fitted | 0.3788 |
| Six-anchor rear registration, 18 stations withheld | 0.2084 |
| Guarded contiguous rear holdouts | 0.2429 |
| Guarded M1 holdouts across three families | 0.7233 |
| Entire dorsal family withheld | 1.9092 |

The rear tests freeze the front/dorsal-derived shape and estimate rear translation from registration stations. All tests reuse the selected coordinates from one acquisition. Their conditioning is described in the paper.

The original tangent-line objective extends beyond the modeled finite generator. The later finite-generator sensitivity gives circular-segment full/guarded RMS 0.7717/1.9363 pixels and physically tangent frustum RMS 0.3946/0.7176 pixels. The earlier M4 construction remains rejected because its line cuts its own ellipse. The corrected physical frustum is a separate exploratory model with incomplete full-scene validation.

The geological comparison contains 28 retrieved images and 18 uniformly measured whole frames. Of 226,426 overlapping control windows, 835 are at least as straight under the declared method, with qualifying segments in 17 frames. This measures straightness under that method. The frequency of the complete three-family configuration has not been measured. The separate pipe-image screen supplies partial-rim comparisons with incomplete exposure and ambiguous local contacts.

Photometric curvature depends on the sampled region and density. The manuscript retains the original-region and shifted-region results with their respective assumptions. Nominal station errors and image residuals do not establish physical manufacturing tolerances or origin probabilities.

## Reproduction

Use Python 3.11 or 3.12 for the pinned project dependencies, plus XeLaTeX for the manuscript. Run from the repository root:

```sh
python -m pip install -r papers/requirements.txt
python audit/sediment-pipe-comparison/scripts/target_benchmark.py
python papers/run_comparison_checks.py
python papers/build_paper_evidence.py
cd papers
xelatex -interaction=nonstopmode -halt-on-error martian-cylinder-technical-paper.tex
xelatex -interaction=nonstopmode -halt-on-error martian-cylinder-technical-paper.tex
cd ..
python papers/verify_journal_revision.py
```

Original PDS arrays and labels are in `data/`. The canonical reconstruction implementations are in `independent-reconstruction/scripts/`, with their stored JSON measurements in `independent-reconstruction/`. Figure products, display transforms and coordinates are recorded in [figure-provenance.json](papers/figure-provenance.json). The [evidence manifest](papers/paper-evidence-manifest.json) records the numerical inputs and code used by the paper.

`archive/` contains historical manuscripts, preliminary interpretations and retired tooling. Temporary environments, build snapshots and caches are local working material under ignored `tmp/` and `.venv/` directories. A virtual environment should be recreated from requirements when needed.

## Data and licensing

NASA/JPL-Caltech/MSSS imagery is attributed in the paper and figure provenance. Repository authorship, data citation and licensing are retained in [CITATION.cff](CITATION.cff), [.zenodo.json](.zenodo.json) and [LICENSE](LICENSE).
