# November 13 technical manuscript journal revision

The authoritative source is `papers/martian-cylinder-technical-paper.tex`, titled *Subpixel Geometric Reconstruction of a Cylindrical Candidate in Curiosity Mastcam-100 Imagery*, with subtitle *Boundary metrology, frozen-shape prediction, and geological comparison*. Its author and revision date remain Justin Bogner and 13 November 2026.

Work began from clean commit `0ba7b986dbf84afe5483991dc9330edbab3cc0fb` on the dedicated branch `paper/nov13-journal-revision`. The verified starting source SHA-256 was `899a3cf559d2b69dba9ede40486e70b3caefe34e5186ee6e536af87cf4273b6f`. Both starting PDF copies were `c1304e151b9d0bf7b6ce6cc86f57eda6d12e9fffe400cf94439008ad37b1a1b9`. Full provenance is retained in `journal-revision-baseline.json`. The older November 11 manuscript supplied no replacement text or figures.

## Figures and presentation

- Figure 1, Section 2.2, now pairs the complete authentic Sol 3556 DRXX frame with its annotated target enlargement. This replaces the previous unmarked enlargement while retaining the detailed station/exclusion panel. It identifies the lower-right ROI, PDS product, zero-based coordinates, crop bounds and display transforms.
- Figure 2, Section 5, replaces the schematic with the exact stored six-parameter M1 overlay and its residuals. It shows all 35 near-rim, 24 rear and 26 dorsal stations with distinct markers. Sampled curve intervals are solid, unmeasured continuations dashed, the inferred center axis dash-dot and the extended tangent dotted. Soil-contact and cast-shadow labels identify interpretations.
- Figure 3 continues to show frozen-shape rear prediction, registration anchors, heldout stations and residuals. Its analytical content is retained. The revised build uses the current script layout when importing the archived data routines.
- The paper retains three figures. The complete manuscript is 18 pages, compared with the 16-page starting PDF. New sensitivity and significance text accounts for the added length. The bibliography's forced page break was removed to avoid an otherwise sparse page.

`build_paper_evidence.py` invokes the new `native_image_figures.py` helper. The locator and joint overlay are supplied as PDFs with embedded native raster imagery and vector annotations, plus 600-dpi PNGs. The PDF embeds the source frame at 1328 by 1184 pixels and the crop at 90 by 75 pixels. Grayscale display uses explicit linear clipping. No spatial interpolation, geometric reprojection, retouching or generative processing is applied. Credit is NASA/JPL-Caltech/MSSS, consistent with the MSL Mastcam/MSSS label and NASA's Mastcam credit convention. `figure-provenance.json` records the product, calibration, crop, limits, model parameters and sampled intervals.

## Scientific and editorial changes

- Section 6.6 retains the original M4 rejection and rear-scale sensitivity, including the exact tangency defect. New Section 6.7 reports the finite-generator omission, distinguishes the original image-plane M1 tests from later camera-projected sensitivities, and presents the finite circular/frustum scores in Table 4. It also records the soil-plane visibility failure and the foreground-bank assumptions.
- Section 8 adds the separate nine-image sediment-pipe screen and its three partial-rim measurements. It identifies incomplete geometry and ambiguous station identity. The original 28-image comparison, 18 whole frames, 226,426 windows, 835 qualifying windows and 17 qualifying frames are retained.
- Section 9.1, *Planetary-Science Significance*, develops the contribution of joint small-feature metrology, registered heldout prediction, the scope of geological comparison, camera-projected physical-model tests and reuse of the workflow. It preserves manufacturing-like geometric regularity and manufacture as a hypothesis. The argument stands on the measured morphology and predictive tests.
- The abstract and conclusion incorporate the finite-boundary sensitivity and unresolved complete shape. Repeated result numbers were removed from the conclusion while their definitions and values remain in Section 6 and the validation table.
- Section 10 identifies the working replay and figure build, current script locations and provenance files. The bibliography retains every original entry and adds the verified Rubin supplemental-material reference.

No boundary station, exclusion, measurement method, fitted analytical parameter, uncertainty estimate or retained result JSON was edited. The new figures use the stored M1 parameters. All 17 original equation environments and all 13 original bibliography entries are preserved.

## Numerical and visual verification

The exact machine-readable record is `journal-numerical-verification.json`. Its regenerated checks pass for 98 manifest entries, original image hashes, every control-window count, all five required predictive results, 18 whole frames and qualifying segments in 17 frames. An isolated replay exactly matches all fitted parameters, folds, residuals and diagnostics in the five retained predictive-result sections. The original results file is unchanged. `journal-predictive-replay.json` records this check.

All six existing comparison tests also pass through `papers/run_comparison_checks.py`, which restores the import path for the relocated reconstruction modules. The archived test and analysis implementations are unchanged. `comparison-checks.txt` records the output. `papers/requirements.txt` extends the existing study dependencies with PyMuPDF for the new PDF verification entry point.

Two successive figure builds produced byte-identical PDFs for Figures 1, 2 and 3. `figure-determinism.json` records their digests. XeLaTeX completed two final passes. The final log contains no overfull boxes, missing characters, unresolved citations or unresolved references. Eight underfull-box notices and four existing math-font substitution notices remain. Page rendering shows no missing glyphs or cropped figures.

The repository enforces LF text checkout while several historical outputs were written with Windows CRLF. The evidence manifest now retains raw observed-byte digests and adds canonical-LF digests for text inputs. Verification accepts only that newline conversion for text. PDS image and label digests remain byte-exact. This corrects a provenance portability issue without changing numerical inputs or the archived result files.

The complete page overview and full-size pages were rendered for review. Figures 1 and 2, Figure 3's prediction display, the finite-boundary table, revised significance text, reproduction listing, conclusion, references and appendices were inspected visually. All imagery uses legible pixel axes, separate marker shapes and captioned limits. Both distributed PDF copies have identical bytes. Current source/PDF hashes are in the numerical report.

## Remaining issues affecting interpretation or submission

1. Some dorsal stations lie beyond the fitted finite generator. The original line-and-conic scores remain valid for their stated objective. Selecting a complete physical surface requires further boundary classification and scene visibility testing, which the new sensitivity section identifies explicitly.
2. The screened pipe examples lack a complete matched three-family exposure. Some partial-rim stations are ambiguous. Geological frequency of the conjunction and origin probabilities remain undetermined. The complete terrain, shadow and radiometric scene has not been jointly validated for the tapered alternative.
3. The photometric significance retains its documented sampling dependence and nominal error model. It is preserved as a separate observational constraint.
4. No target journal was specified. The existing research-article layout is retained. Journal-specific template and submission requirements remain to be applied once a venue is selected.

The subsequent master-branch repair corrected the historical scripts' data/output roots and stale import paths after their relocation. It also integrated this journal revision into master and retired superseded summaries. The numerical expressions and archived outputs were preserved. See [repository-repair.md](repository-repair.md) for the repair provenance and verification.
