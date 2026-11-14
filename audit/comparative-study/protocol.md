# Curiosity geological comparison protocol

Date: 2026-11-13. Written before new quantitative results.

Question: Which aspects of the Sol 3556 candidate are unusual among resolvable Curiosity geological image features, and which have plausible natural analogues?

All comparison photographs must be acquired by Curiosity. All therefore lie within Gale Crater. Use two complementary sets: (1) whole-frame Mastcam scenes across the traverse, including same-sequence neighbors to control camera and illumination; (2) deliberately selected geological analogues illustrating concretions, resistant vein fragments, crystal-shaped features, wind abrasion, and rounded clasts. The second set is a challenge set, not a random population.

Do not reuse the archived survey's claimed 0/185 rarity without reproducing its selections and measurement definitions. Check image provenance, scene labels, and target measurement comparability first. Identify shadows, merged fragments, substrate textures, and uncertain segments explicitly. Do not call automated connected components independent geological objects without visual validation.

Quantitative comparisons will emphasize observable quantities: fixed-span line residuals, edge contrast and blur, scale-normalized outline shape where a coherent outline is visible, and robustness to smoothing, pixel sampling, and JPEG encoding. Apply an identical detector and fitting rule to target and controls within each analysis. Keep the existing hand-selected erf fit as a separate reference; never rank it directly against coarsely segmented control outlines.

Use native pixels as the primary unit. Matching apparent image size does not establish equal physical size, resolution, lithology, or viewing angle. No transfer of the target's mm/pixel scale to other images. Avoid inventing missing opposite flanks or treating a partial arc as two complete circular ends.

Report image counts, candidates, exclusions, per-scene distributions, representative nearest analogues, and sensitivity results. Overlapping edge windows and clasts in one scene are correlated. Any rank is conditional on the sampled frames and selection algorithm, not a probability that nature made the target. A conjunction claim requires measurable corresponding features on controls and a validated detector; otherwise leave it unquantified.

Provide an image/source manifest with hashes and URLs, data tables, rerunnable scripts, visual contact sheets with coordinates, and a report separating measured results, established geological mechanisms, and unresolved interpretation.

Pre-result processing amendment: first visual inspection revealed strong two-pixel sampling patterns in single-channel raw JPEG previews. Discard the initial unbinned exploratory run (no completed numerical results). Apply identical 2x2 area averaging to all quantitative frames before contour extraction, report geometry back in equivalent native pixels, and explicitly distinguish this from the original full-resolution erf metrology. Color/luminance calibration and physical sampling still differ among scenes; this is an apparent image-geometry comparison.
