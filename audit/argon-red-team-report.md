# Argon audit: checked findings and dispositions

Reviewed 2026-11-12. This revision supersedes the original report's unsupported confidence and independence claims. Numerical evidence is in the JSON outputs and reproduction log. This is a local repository verification, not a new NASA archive download or a new geological survey.

| Issue | Disposition | Evidence and limits |
| --- | --- | --- |
| ARGON-H01: M4 | Physical formulation rejected | Direct ellipse/line tangency check in `audit_3d_projective_geometry.py`; derivation in `model-comparison.md`. Keep M4's reproducible numerical fit as a diagnostic, not a physical frustum. A shifted ellipse center need not lie on a visible edge. The fixed-shape rear scan is not a 16-sigma test of M4's changed ellipse shape. |
| ARGON-H02: rear scale | Reporting corrected | Nominal z=sqrt(4.8216)=2.196, not 1.55. Nominal CI [0.87,0.99] excludes 1. Scalar Birge sensitivity includes 1 but does not calibrate spatial covariance. |
| ARGON-H03: tolerance | Qualification added to active summaries | M1 RMS 0.3788 px is an image-plane residual, not physical roughness. Reduced chi-square 33.59 signals an inadequate nominal error/model description; correlation alone has not been established as the cause. |
| ARGON-M01: shadow | Conditional; independent reproduction outstanding | 32.82 degrees is fitted receiving-plane rotation, not surveyed absolute terrain slope. Thresholds share pixels. The audit script transcribes prior reported values, not a new ray trace. |
| ARGON-M02: range | Conditional dimensions documented | Focus calibration is not independent ranging. Focus-band diameter about 10.6–12.9 mm; this is a scenario span, not an 11.6 +/- 1.2 mm statistical confidence interval. |
| ARGON-M03: controls | Limited evidence; broader survey outstanding | Three selected clasts do not establish regional rarity or natural impossibility. The audit control script transcribes reported comparisons. |
| ARGON-L01: root PDF | Repaired | Paper source corrected for M4 tangency and current photometry, rebuilt, and copied byte-for-byte to the root PDF. |
| ARGON-L02: CI | Workflow repaired; hosted execution pending | Current reconstruction, its dependency file, and audit tests replace archived commands. Reproduction returns nonzero on failure or numerical drift. |
| ARGON-L03: links | Repaired in active Markdown and llms.txt | Machine-local file URLs converted to document-relative links. |

## Verification performed

The full reconstruction completed in 136.91 seconds with zero numerical differences and identical hashes for all eight JSON outputs. All ten audit scripts ran successfully. All 15 regression tests passed; Windows sandbox permissions required the temporary-file tests to run outside the sandbox. The corrected 15-page paper was rebuilt with XeLaTeX and its changed pages visually reviewed. Hosted GitHub execution has not been observed.

## Corrections to the audit itself

The current Step 5 output reports curvature significance z=0.95, contradicting both the historical 7.38 in the report and the audit's hardcoded 11.45. The rock audit now reads the real pipeline output. Neither historical significance is current evidence.

- Removed the model-by-model Birge BIC ranking. Dividing each model's chi-square by its own chi-square/(N-k) makes the residual term exactly N-k and mechanically rewards smaller k. It is not a comparable common likelihood.
- Birge scaling is scalar variance inflation, not a spatial covariance fit. The reported lag correlation and AR(1) effective sample size are descriptive diagnostics on 24 residuals, not a measured covariance for all 85 stations.
- The provenance script checks local checksums against stored local values. It does not download NASA files or independently recompute SPICE kernels. Camera angles use stored telemetry.
- Reused extraction and geometry routines make this a reproduction and consistency check, not a wholly independent implementation.
- The shadow threshold table previously contained hardcoded intermediate values without direct source evidence. Those entries are removed; only explicitly sourced summary values are retained as reported, not independently verified.
- The old ledger manually assigned MATCH to hardcoded claims and stale line numbers. Its replacement inventories actual JSON numeric values with locatable paths and explicitly labels their verification limits.

The selected boundaries admit a subpixel cylindrical fit. M4's physical formulation fails its silhouette constraint. These observations do not uniquely establish material, origin, true physical tolerances, or regional geological rarity. Independent ranging, receiving-ground measurement, covariance calibration, and a broader control sample remain outstanding scientific work, not completed fixes.
