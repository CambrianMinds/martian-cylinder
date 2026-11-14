# Technical paper revision verification

Revision: 13 November 2026.

- Reproduced the target-only predictive validation once after repairing its relocated root path. The complete parsed results, including all folds, parameters, residuals, input hashes, and environment metadata, exactly match the retained pre-run results.
- Corrected predictive-report transcription errors: M1 is the six-parameter model; front heldout RMS is 0.8456 px. Report and generator now use the same dorsal sensitivity interpretation and reproduction path.
- All six comparison tests passed. Checks included the 28 original image hashes, the exported count of 226,426 control windows and 835 qualifying windows, target exclusion, and reconstruction of the target contour residual. No acquisition or expanded comparison was performed.
- All 15 audit regression tests passed, including the M4 discriminant check and PDF distribution equality. Three temporary-file tests initially encountered Windows sandbox access restrictions; rerunning the suite with temporary-file access passed all tests.
- All 48 entries in `paper-evidence-manifest.json` match the current source, analysis, protocol, numerical, and figure files.
- XeLaTeX completed two passes. The final log contains no overfull boxes, missing characters, unresolved references, or unresolved citations. Existing math-font substitution notices do not produce missing glyphs in the rendered pages.
- Rendered and visually reviewed the 17-page paper, including the annotated native image, predictive figure/table, physical-tangency derivation, conclusion, references, reproduction listing, and evidence hashes. Corrected heading placement, listing splitting, figure label size, and axis tick spacing during review.
- Both distributed PDFs are byte-identical. SHA-256: `f48af9162abf90e1b34f405b28ebf90aeade23e5c0cf7b5043bb99ecba64cafa`.

Scientific scope is unchanged: the existing boundary coordinates and comparison images are retained. The paper reports predictive geometric consistency and manufacturing-like regularity without assigning composition, provenance, physical machining tolerances, or origin probabilities.

## Appendix consolidation (13 November 2026)

This editorial update supersedes the earlier 17-page PDF distribution described above.

- Retained Appendix A's measurement table and replaced the repeated selection explanation with a Section 4 reference.
- Retained Appendix B's projection and identifiability derivation.
- Folded Appendix C's dimensional range and projected center separation into Section 3.2.
- Removed Appendices D and E from the PDF. Image digests remain in `file-integrity.md`; the JSON evidence manifest and `paper-evidence-hashes.tex` remain in the repository. Section 10 identifies these files.
- Updated the manuscript digest in both evidence records.
- Completed two XeLaTeX passes; no overfull boxes, missing characters, unresolved references, or unresolved citations. Existing font-substitution and underfull-box notices remain.
- Rendered the 16-page result and inspected the page overview and the revised dimensional section and appendix page.
- Updated both distributed PDFs with byte-identical copies. No measurements, scientific conclusions, or analysis code were changed.

Current PDF SHA-256: `248077272fef7c9839bb2cda3fce7a992969b147b67bf64fda1e96279b7be729`.

## Geometry illustration (13 November 2026)

- Added Figure 2 near Section 5: common-section constraints, burial versus apparent taper, and a close-up of the actual M4 tangency failure.
- Panels (a) and (b) are explicitly schematic; panel (c) is generated from retained M4 parameters in `independent-reconstruction/step9_joint_model.json`. Its unequal plotting scales are disclosed.
- The reproducible vector-figure generator is `geometry_figure.py`, invoked by `build_paper_evidence.py`. The generator and vector figure are included in the evidence manifest.
- Completed reference-resolving XeLaTeX passes and inspected the full-page overview and final figure page. No overfull boxes, missing characters, or unresolved references/citations were found. Existing font-substitution and underfull-box notices remain.
- Both distributed PDFs now contain 17 pages and are byte-identical. The two retained appendices are unchanged. Measurements and scientific conclusions are unchanged.

Current PDF SHA-256: `6a848f262158dec13bf03025d82faa25ecb1d6164840a945f8cf2dcea5b26fa5`.

## M4 emphasis and inline-figure revision (13 November 2026)

- Removed the M4 panel from Figure 2. The two remaining schematics now appear side by side inline on page 6, between the Section 5 introduction and methods.
- Removed M4 from the abstract, conclusion, main joint-fit table, BIC comparison, and dedicated taper comparison table. Retained one methods pointer and one concise rejection paragraph with its numerical residual, tangency failure, and archived output path. M4 is not presented as a viable physical competitor.
- Retained the standalone rear-scale sensitivity result and its conditional interval, which answer a separate question.
- Started references and appendices on separate pages to avoid stranding Appendix B's equations on a mostly empty final page.
- Updated manuscript and figure evidence hashes. No measurements or analysis outputs were changed.
- Compiled with XeLaTeX until references resolved. The 16-page result has no overfull boxes, missing characters, unresolved references, or unresolved citations; existing font-substitution and underfull-box notices remain.
- Rendered and inspected the page overview, inline figure, shortened rejection discussion, and final appendix page. Both distributed PDFs are byte-identical.

Current PDF SHA-256: `d5f6551176cf97fbf3fcc06e3794852165187816cdd0cc9ddb2884199fa08a2f`.

## Shading-profile replay (13 November 2026)

- Replayed original Step 5 photometry using the Step 3 profile-selection geometry from commit d0a63274ada472d77a905268366f2fcbd21eed3d and the retained radiometric image. Reproduced nominal z=7.37854.
- Replayed the current selection and reproduced nominal z=0.94715. The upstream boundary correction moves the sampling origin approximately 13 pixels and shifts the selected region toward the rear.
- Repeated the original five cuts at approximately native-pixel spacing, yielding nominal z=4.79739. Pooled curvature remains negative after omitting any one profile. These are sensitivity checks under polynomial-fit covariance assumptions.
- Added the replay script, full coordinates, and results under `audit/shading-sampling-review/`. Updated the evidence manifest and reproduction commands.
- Corrected Section 8's earlier characterization of 7.38 as unreproduced. Updated the photometry limitation to describe the dependence on region and sampling density.
- Compiled and rendered the 16-page paper. Inspected the updated shading page and full-page overview. No overfull boxes, missing characters, or unresolved references/citations. Existing font-substitution and underfull-box notices remain.
- Updated both distributed PDFs with byte-identical copies.

Current PDF SHA-256: `c1304e151b9d0bf7b6ce6cc86f57eda6d12e9fffe400cf94439008ad37b1a1b9`.
