# Current methods guide

The [technical manuscript](../papers/martian-cylinder-technical-paper.tex) defines the current equations, selections, fitted parameters and limits. Its [evidence manifest](../papers/paper-evidence-manifest.json) identifies the numerical inputs. The [previous methods document](../archive/superseded-docs-2026-11-13/independent-reconstruction/methods.md) is archived.

1. Decode the original DRXX radiance product and retain zero-based pixel coordinates. Use the PDS CAHVOR camera parameters for geometric projection.
2. Classify material, soil-contact and shadow boundaries before interpreting their shape. Retain the 35 near-rim, 24 rear and 26 dorsal stations and documented exclusions.
3. Fit orthogonal curve distances under the stated M1 common-section, common-axis and upper-line tangency constraints. Its objective uses an extended tangent line.
4. Freeze front/dorsal-derived shape for rear prediction, allowing the stated translation registration. Use guarded coordinate holdouts and report whole-dorsal withholding separately.
5. Evaluate finite-generator extent, alternative physical surfaces and scene visibility as distinct sensitivities. The original M4 formula fails its tangent constraint.
6. Compare straightness under the common image preprocessing and window definition. Preserve extraction ambiguity and incomplete geological exposure.

Canonical implementations live in `scripts/`. Their output root is `independent-reconstruction/`, and the original imagery remains in `../data/`. The paper's deterministic figure build reads stored measurements and creates authentic-image overlays. Follow the [current reproduction commands](../README.md#reproduction) and [figure provenance](../papers/figure-provenance.json).
