# Frozen evaluation protocol

Frozen before new fits and simulations on 13 November 2026. Branch `audit/sediment-pipe-comparison`. Parent HEAD 623ed7758098affc68515852024cddc0702f0178. Existing working-tree changes belong to prior work and are excluded from this study's commits.

## Research plan and initial sources

1. Reproduce the November 13 target from the retained coordinate extraction and predictive-validation functions, with outputs redirected into this directory. Record source hashes and distinguish committed source from working-tree additions.
2. Retrieve Rubin et al. (2017), supplement 2017002, official PDS products and labels for sols 173, 528, 542 and 1051. Resolve abbreviated sequence names through published documentation and archive indexes. Search original literature for exposed terrestrial pipe columns and finite segments. The existing root research ZIP is a screening scaffold and synthetic demonstration, not new empirical evidence.
3. Classify N (one near termination), R (far termination of the same body), and D (longitudinal exterior material boundary) before residual fitting. A single ring supports partial comparison. Two separate rings never count as two ends. Store explicit visibility and exclusion decisions. Retain all screened candidates regardless of apparent regularity.
4. Fit eligible material curves using directed gradient and error-function/gradient-peak localization, orthogonal ellipse distances, TLS, and exact joint tangency. Report pixel and diameter-normalized RMS, visible coverage and resolution. Make no full-model inference where a required family is unobservable. Selection is one analyst pass with algorithmic sensitivity, with no claim of blind independent annotation.
5. Fit a genuine 3D circular finite segment through the retained CAHVOR camera and include an oblique foreground burial surface. The physical history is fluidization, cementation, exhumation, fracture and burial. Literature support for those stages is distinguished from assumed end-face orientation and small-scale regularity. Fit only geometric parameters. A round cemented segment and an engineered round segment with identical surface geometry have identical image predictions. The fit alone cannot estimate the frequency of either formation history.
6. Test deterministic sensitivity families with taper, centerline bending, cross-section modulation and terminal tilt. Values are exploratory dimensionless stress tests, not geological probability distributions. Include clear synthetic labels. Apply antialiased image sampling and specified Gaussian blur where rendered images are evaluated. Report geometric-coordinate fits separately from extraction on rendered imagery.
7. Use recorded target weights to reproduce the benchmark and a common unweighted/dimensionless comparison protocol for controls and simulations. Any difference in method or selection must be explicit. Freeze six rear anchors at indices 0,4,8,12,16,20, five contiguous folds with two neighboring guards, and three fixed orientation initializations. Select optimization starts by training error. Never tune on withheld scores. Rear translation is fitted registration. No claim of predicting absolute length from a single front section.
8. Validate analytic tangency, perspective projection, known synthetic parameters, eligibility, negative-control mismatch, reproducibility and heldout isolation. Inspect spatial residual correlation and practical parameter sensitivity. Formal independent station errors are not calibrated significance or origin odds.
9. Generate the report's numerical tables from result JSON and provide complete provenance, failures, eligibility classifications, separate observed/synthetic results and explicit answers A-F. Freeze limitations honestly if a full empirical comparator is unavailable.

## Sources to resolve

- Rubin et al. (2017), DOI 10.1130/G38339.1, author-hosted PDF supplied in assignment, Figs. 2-4, Table 1 and GSA supplement 2017002.
- NASA PDS Mastcam and Navcam lossless/calibrated archives. Initial sequence hints MR00926, MR002083, navcam00354 and ML004625 are not full product IDs.
- Hurst et al. (2011), sediment injection review, plus primary Utah/Colorado Plateau pipe studies cited by Rubin.
- Existing target `independent-reconstruction/` and `audit/predictive-validation/`.

## Amendments

Any changes required by archive availability or unsuitable geometry will be dated here before the affected fitting. All acquired candidates and all failures remain in acquisition and screening inventories.
