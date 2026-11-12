# Martian Cylinder Investigation: Curiosity Sol 3556 Anomaly

> **High-Precision Subpixel Photogrammetric, Radiometric, and Geometric Analysis of an Unidentified Cylindrical Feature in Curiosity Mastcam-100 Imagery (`3556MR1025170721700585C00`)**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23789092.svg)](https://doi.org/10.5281/zenodo.23789092)
[![License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/Text%20License-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](requirements.txt)

**Author:** Justin Bogner ([Cambrian Minds](https://github.com/CambrianMinds))  
**Target Observation:** Mars Science Laboratory (*Curiosity*) Mastcam Right ($100\text{ mm}$), Sol 3556 (August 7, 2022, 12:10:25 LTST), Paraitepuy Pass, Gale Crater  
**PDS Product ID:** `3556MR1025170721700585C00` (`DRXX`, `DRLX`, `DRCX`, `DRCL`)  
**Primary Technical Report:** [`independent-reconstruction/report.md`](file:///d:/projects/martian-cylinder/independent-reconstruction/report.md)  
**Plain-English Summary:** [`independent-reconstruction/report_layman.md`](file:///d:/projects/martian-cylinder/independent-reconstruction/report_layman.md)  
**Narrative Essay:** [`teaching-myself-the-scientific-method-rev13-draft.md`](file:///d:/projects/martian-cylinder/teaching-myself-the-scientific-method-rev13-draft.md)  

---

## Executive Summary

This repository contains the complete NASA Planetary Data System (PDS) raw telemetry, calibrated image products, mathematical formulations, and Python verification pipelines for the forensic photogrammetric investigation of an anomalous, geometrically regular cylindrical feature in Curiosity Mastcam-100 imagery on Sol 3556.

The object is located in the lower-right foreground of observation `3556MR1025170721700585C00`, captured at Paraitepuy Pass at a calibrated best-focus distance of $3.957\text{ m}$ (local pixel scale $0.294\text{ mm/pixel}$).

Using 16-bit uncompressed PDS telemetry (`DRXX`/`DRLX`), rigorous subpixel edge extraction, directional solar ray tracing, and an 85-point joint geometric model, this investigation establishes that the object is a **centimeter-scale right circular cylinder** ($11.6\text{ mm}$ diameter—identical to a standard AAA battery—and $\sim 12\text{ mm}$ exposed projected length) resting partially buried within sloping Martian regolith. A strict 6-DOF right circular cylinder model fits all 85 observational stations across the front rim, rear terminus, and upper barrel edge simultaneously with a total root-mean-square residual of **$0.3788\text{ pixels}$** (~$110\ \mu\text{m}$ on the Martian surface).

```
                      [Front Rim N=35]
                  Smooth, tilted circle
              RMS = 0.162 px  (Diam = 11.6 mm)
                     \          /
                      \________/
                      /        \
                     /  BODY    \
   [Rear Terminus N=24]          \  [Upper Dorsal Edge N=26]
   1:1 match to front             \ Laser-straight (RMS = 0.242 px)
   RMS = 0.185 px                  \ Aligned to front minor axis to 0.9σ
   ------------------------------------------------------------------
   JOINT STRICT CYLINDER FIT (Model 1, 85 Points): RMS = 0.3788 px (~110 µm)
```

---

## Project Timeline & Methodological Evolution

The investigation advanced through three distinct phases:

1. **Phase 1: Initial Discovery & Post-Publication Audit (October 2026)**  
   The initial study utilized 2D central-perspective canvas overlays and preliminary bounding boxes. A post-publication peer audit (`archive/legacy_audit/audit.md`, `archive/legacy_audit/AUDIT_RESPONSE.md`) demonstrated that 2D manual overlays suffered from parameter coupling, that length bounds required strict 3D ray modeling, and that the feature's lower dark patch had been conflated with an unburied circular face. The preliminary manuscripts and early tooling are preserved in [`archive/`](file:///d:/projects/martian-cylinder/archive/).

2. **Phase 2: Forward Shadow Ray-Tracing & Ground Slope Decoupling (November 2026)**  
   Documented in [`most-recent-work.md`](file:///d:/projects/martian-cylinder/most-recent-work.md), this analysis decoupled the object's physical rim from the forward dark region. Using NASA's SPICE solar ephemeris (elevation $69.8224^\circ$, azimuth $186.8169^\circ$, image shadow angle $+63.43^\circ$), ray casting proved that the dark forward area is **not** an exposed cylinder face, but the **cast shadow of the overhanging front rim projected onto locally sloping ground**. An unannotated raw-image 85-DN brightness profile matched the projected shadow to $1.049\text{ native pixels}$ RMS ($4.80\text{ enlarged px}$) at a ground slope rotation of $32.82^\circ$.

3. **Phase 3: Independent Subpixel Reconstruction & 85-Point Joint Model (November 2026)**  
   Conducted strictly from the primary 16-bit PDS RDR files (`DRXX` with full `CAHVOR` radial distortion model and `DRLX` linearized with `CAHV`). This phase resolved the physical edge polarity (`grad_sign = +1` outer material boundary), discovered that a single outlier at $\theta = -45^\circ$ belonged to an adjacent upper-right pebble, isolated the unburied rear terminus arc ($N=24$), and proved a 1:1 curvature match between the front and rear ends. Step 9 synthesized these features into an 85-point joint optimization, confirming a strict right circular cylinder to $0.3788\text{ px}$ overall error.

---

## Key Verified Findings

| Parameter / Feature | Measured Value | Uncertainty / Verification | Method / Source |
| :--- | :--- | :--- | :--- |
| **Observation Product** | `3556MR1025170721700585C00` | Lossless Bayer Huffman (`INST_CMPRS_MODE = 1`) | NASA PDS3 RDR (`DRXX` & `DRLX`) |
| **Focus Motor Count & Distance** | Count `2705` $\to 3.957\text{ m}$ | Focus range band $3.6\text{--}4.4\text{ m}$ | `MSL:BEST_FOCUS_DISTANCE` |
| **Local Pixel Scale** | $\text{IFOV} = 74.304\ \mu\text{rad/px}$ | $0.2940\text{ mm/pixel}$ at $3.957\text{ m}$ | `CAHVOR` Jacobian ($\sigma_1/\sigma_2 - 1 = 0.59\%$) |
| **Clean Front Rim ($N=35$)** | $a = 19.95\text{ px}$, $b = 16.74\text{ px}$ | $b/a = 0.8392$ (tilt $\gamma = 32.9^\circ$), $\text{RMS} = \mathbf{0.1618\text{ px}}$ | Single pebble outlier ($\theta=-45^\circ$) excluded; [Step 8](file:///d:/projects/martian-cylinder/independent-reconstruction/step8_pebble_correction_and_rear_terminus.py) |
| **Physical Diameter ($2a$)** | **$11.6\text{ mm}$** ($11.55\text{--}11.72\text{ mm}$) | Matches ANSI AAA battery ($10.5\text{ mm}$) | Metric projection at $3.957\text{ m}$ slant range |
| **Front Rim Minor Axis** | $\phi_{\text{minor}} = 32.70^\circ \pm 4.23^\circ$ | Matches dorsal edge ($28.89^\circ$) to $0.90\sigma$ ($p = 0.37$) | 5-DOF Free Ellipse ODR with bootstrap |
| **Upper Dorsal Edge ($N=26$)** | $\theta_{\text{dorsal}} = 28.89^\circ \pm 0.35^\circ$ | $\text{RMS} = \mathbf{0.2422\text{ px}}$ ($71\ \mu\text{m}$), sagitta $0.280\text{ px}$ | True outer boundary (`grad_sign = +1`); [Step 3](file:///d:/projects/martian-cylinder/independent-reconstruction/step3_feature_extraction.py) |
| **Exposed Rear Arc ($N=24$)** | 1:1 unscaled copy of front rim | $\text{RMS} = \mathbf{0.1854\text{ px}}$ ($0.318\text{ px}$ max residual) | Lower-left soil burial separated; [Step 8](file:///d:/projects/martian-cylinder/independent-reconstruction/step8_pebble_correction_and_rear_terminus.py) |
| **Rear-to-Front Scale Ratio ($s$)** | $s = 0.935$ ($95\%\text{ CI: } [0.87, 0.99]$) | Standalone $s=1.000$ differs by only **$0.0019\text{ px}$** ($0.6\ \mu\text{m}$) | Standalone rear-arc curvature unidentifiability; [Step 9](file:///d:/projects/martian-cylinder/independent-reconstruction/step9_joint_geometric_model.py) |
| **Strict Cylinder Fit (Model 1)** | **$\mathbf{0.3788\text{ px}}$ total RMS** | Front: $0.238\text{ px}$, Rear: $0.483\text{ px}$, Dorsal: $0.422\text{ px}$ | 6 DOF ($s=1.000$ fixed, collinear, tangent silhouette); [Step 9](file:///d:/projects/martian-cylinder/independent-reconstruction/step9_joint_geometric_model.py) |
| **Solar Illumination & Shadow** | El $69.8224^\circ$, Az $186.8169^\circ$ | 2D shadow vector $\theta_{\text{shadow}} = +63.429^\circ$ | SPICE geometry; [Step 2](file:///d:/projects/martian-cylinder/independent-reconstruction/step2_camera_geometry.py) / [`most-recent-work.md`](file:///d:/projects/martian-cylinder/most-recent-work.md) |
| **Raw Forward Shadow Match** | $\text{RMS} = 1.049\text{ native px}$ ($4.80\text{ enl}$) | Evaluated across 9 raw DN thresholds ($65\text{--}105\text{ DN}$) | Receiving plane tilt $32.82^\circ$; [`most-recent-work.md`](file:///d:/projects/martian-cylinder/most-recent-work.md) |
| **Edge Straightness vs Rocks** | Target: $0.242\text{ px}$ RMS | Nearby Rocks: $0.971\text{ px}$, $1.724\text{ px}$, $1.953\text{ px}$ | **Target is 4× to 8× straighter** than scene rocks |
| **Surface Texture vs Rocks** | Target: $\sigma_{\text{Lap}}^2 = 8.02 \times 10^{-5}$ | Nearby Rocks: $1.64\text{--}2.98 \times 10^{-4}$ | **Target is 2× to 4× smoother** (Laplacian variance) |
| **Photometric Light Gradient** | Convex roll-off ($z = 11.45\sigma$) | Flat rock facet model rejected at $>11\sigma$ | Transverse clinometry; [Step 5](file:///d:/projects/martian-cylinder/independent-reconstruction/step5_competing_3d_interpretations.py) / [Step 9](file:///d:/projects/martian-cylinder/independent-reconstruction/step9_joint_geometric_model.py) |

---

## The Four Pieces That Form the Lock

```
                     +---------------------------------------+
                     | Piece #1: Front Circular Rim          |
                     | 35 clean points (outlier removed)     |
                     | Oval tilt b/a = 0.839; RMS = 0.162 px |
                     | Diameter: 11.6 mm (~AAA battery)      |
                     +-------------------+-------------------+
                                         |
                                         | Lines up within 0.9σ
                                         v
+----------------------------------------+---------------------------------------+
| Piece #2: Upper Dorsal Edge            | Piece #3: Rear Terminus Arc           |
| 26 stations over 36.4 px               | 24 exposed boundary points            |
| Direction: 28.89° ± 0.35°              | 1:1 unscaled front copy: RMS=0.185 px |
| Straightness: RMS = 0.242 px (71 µm)   | Scale s = 0.935 (ΔRMS = 0.002 px @ 1) |
+----------------------------------------+---------------------------------------+
                                         |
                                         | Unified rigid 3D constraint
                                         v
                     +---------------------------------------+
                     | Piece #4: Strict 6-DOF Cylinder       |
                     | Model 1: Collinear, s=1.0, Tangent    |
                     | Total Joint RMS: 0.3788 px (~110 µm)  |
                     | Forward Shadow: Raycast RMS = 1.05 px |
                     +---------------------------------------+
```

1. **Piece #1 (Front Rim)**: The illuminated upper rim traces an unconstrained ellipse with $b/a = 0.833\text{--}0.839$, perfectly matching an obliquely viewed planar circle tilted at $33^\circ$. Excluding a single outlier at $\theta = -45.0^\circ$ that catches an adjacent pebble drops the rim fit residual from $0.417\text{ px}$ to **$0.1618\text{ px}$** (< 1/6th pixel!). Angular rock facet models fail ($\Delta\text{AIC}_c > +600$).
2. **Piece #2 (Dorsal Edge)**: The sunlit upper boundary runs laser-straight across 26 stations with an orthogonal RMS of **$0.242\text{ px}$** ($71\ \mu\text{m}$) and maximum sagitta of $0.280\text{ px}$. Crucially, the minor axis of the front rim ($32.70^\circ \pm 4.23^\circ$) and the dorsal edge ($28.89^\circ$) align to within **$0.90\sigma$**, satisfying the exact geometric condition for a right cylinder.
3. **Piece #3 (Rear Terminus)**: When the oblique lower-left regolith burial line is separated from the true rear end, an **unscaled 1:1 copy of the front rim** matches all 24 exposed rear points to **$0.1854\text{ px}$ RMS**. The rear cap does not taper: standalone rear-arc curvature is consistent with zero taper ($s = 1.000$) to within two thousandths of a pixel ($0.0019\text{ px} \approx 0.6\ \mu\text{m}$).
4. **Piece #4 (Joint Lock & Shadow)**: A strict 6-DOF right circular cylinder model (collinear centers, zero uncoupled offsets, exact outer tangent silhouette) fits all 85 points simultaneously with an overall error of **$0.3788\text{ pixels}$** (~110 microns on Mars). Forward solar ray-tracing reproduces the separate forward dark boundary on sloping regolith to $1.049\text{ px}$ RMS.

---

## Repository Structure

```text
martian-cylinder/
├── README.md                          # Repository documentation and comprehensive guide
├── llms.txt                           # Structured machine-readable summary for AI/LLMs
├── most-recent-work.md                # Phase 2 forward shadow reproducibility package
├── teaching-myself-the-scientific-method-rev13-draft.md  # Narrative essay by Justin Bogner
├── requirements.txt                   # Minimal Python dependencies (numpy, scipy, Pillow)
├── CITATION.cff                       # Citation metadata (CFF 1.2.0)
├── LICENSE                            # Dual MIT (code) / CC BY 4.0 (text)
├── DRXX-metadata.txt                  # Full ASCII PDS3 label for 3556MR1025170721700585C00
│
├── independent-reconstruction/        # Phase 3 Independent Subpixel Analysis Suite
│   ├── run_all.py                     # Master execution runner (runs steps 1-9 sequentially)
│   ├── step1_image_inspection.py      # Provenance, SHA-256 checks, 16-bit linear calibration
│   ├── step2_camera_geometry.py       # CAHVOR/CAHV camera matrices, solar ephemeris, scale bounds
│   ├── step3_feature_extraction.py    # Subpixel erf/gradient edge tracking with physical polarity
│   ├── step4_endface_and_conic_models.py # Conic/polygonal ODR fits, AICc/BIC model selection
│   ├── step5_competing_3d_interpretations.py # Perspective convergence proof, clinometry, shadow
│   ├── step6_robustness_and_sensitivity.py   # Perturbation sweeps, Monte Carlo Bayer noise, JSON export
│   ├── step7_pebble_and_rear_terminus_inspection.py # Zoomed analysis of adjacent pebble & rear
│   ├── step8_pebble_correction_and_rear_terminus.py # Pebble outlier removal & 1:1 rear-to-front match
│   ├── step9_joint_geometric_model.py # Strict 85-point joint 3D cylinder/cone optimization
│   ├── measurements.json              # Master compiled measurement inventory (117 KB)
│   ├── step9_joint_model.json         # Comprehensive joint model parameters and scan logs (97 KB)
│   ├── methods.md                     # Formal mathematical definitions, ODR formulations, and assumptions
│   ├── report.md                      # Comprehensive peer-review technical investigation report
│   ├── report_layman.md               # Plain-English companion summary explaining the lock
│   └── figures/                       # Diagnostic figures (diag01 through diag09, benchmarks)
│
├── data/                              # Primary NASA PDS3 data products and calibration crops
│   ├── 3556MR1025170721700585C00_DRXX.{IMG,LBL,fits,png} # Raw 16-bit CAHVOR radiance product
│   ├── 3556MR1025170721700585C00_DRLX.{IMG,LBL,fits}     # Linearized 16-bit CAHV product
│   ├── 3556MR1025170721700585C00_DRCX.{IMG,LBL,fits,png} # 8-bit color product
│   ├── 3556MR1025170721700585C00_DRCL.{IMG,LBL,fits,png} # 8-bit color linearized product
│   ├── crop_bottom_right.png          # 500x450 calibrated context crop
│   └── bogner_mariner1971_report.pdf  # Historical JPL TM 33-591 (R. S. Bogner, 1973)
│
├── research/                          # Scientific context and background literature
│   ├── 00_master_index_and_integration_guide.md
│   ├── 01_martian_soil_erosion_and_deposition.md
│   ├── 02_rover_and_equipment_hardware_audit.md
│   ├── 03_ventifacts_concretions_and_martian_geology.md
│   ├── physical_evidence_synthesis.md
│   └── technosignature_assessment.md
│
└── archive/                           # Archived Phase 1 manuscripts, audit logs, and legacy tools
    ├── legacy_audit/                  # audit.md, AUDIT_RESPONSE.md, peer_review_response.md
    ├── legacy_papers/                 # martian_cylinder_paper.tex/.pdf, citizen_science_article.tex/.pdf
    ├── legacy_web/                    # index.html, site.css, site.js
    ├── cylinder-tool/                 # 2D Canvas photogrammetry tool
    └── scripts/                       # Phase 1 & 2 Python verification scripts
```

---

## Reproducing the Analysis

### 1. Install Dependencies

The independent reconstruction pipeline requires Python 3.10+ and standard numerical libraries:

```bash
pip install -r requirements.txt
```

*(Dependencies: `numpy>=1.24.0`, `scipy>=1.10.0`, `Pillow>=9.5.0`)*

### 2. Run the Full Independent Reconstruction Pipeline

Execute the master runner directly:

```bash
cd independent-reconstruction
python run_all.py
```

The script executes all 9 steps in sequence:
- **Steps 1 & 2**: Verifies the raw NASA PDS3 binaries (`DRXX`, `DRLX`), computes CAHVOR/CAHV camera intrinsics, validates solar ephemeris vectors, and sets distance-dependent scale envelopes.
- **Step 3**: Performs subpixel edge extraction along normal profiles with physical polarity tracking (`grad_sign = +1` outer material boundary).
- **Steps 4 & 5**: Evaluates conic models via Euclidean Orthogonal Distance Regression (ODR), calculates AICc/BIC model selection metrics, proves perspective convergence limits, and performs transverse photometric clinometry.
- **Steps 7 & 8**: Isolates the adjacent pebble outlier at $\theta = -45^\circ$, re-fits the clean 35-point front rim, isolates the exposed rear-terminus arc ($N=24$), and demonstrates the unscaled 1:1 front-to-rear curvature match.
- **Step 9**: Solves the 85-point joint geometric optimization (Models 1 through 4), resolving the collinear cylinder axis and quantifying scale ratio profile likelihoods.
- **Step 6**: Runs perturbation batteries (trimming, edge estimators, Monte Carlo Bayer noise) and compiles [`measurements.json`](file:///d:/projects/martian-cylinder/independent-reconstruction/measurements.json).

### 3. Verify Key Results via Python

You can query the compiled JSON artifacts directly:

```python
import json

# Verify the strict 6-DOF cylinder joint fit (Model 1)
with open("independent-reconstruction/step9_joint_model.json") as f:
    joint_data = json.load(f)
m1 = joint_data["joint_models"]["M1_Strict_Right_Circular_Cylinder_6DOF"]
print(f"Model 1 Total Joint RMS: {m1['residuals_px']['total_rms']:.4f} pixels")
print(f"Model 1 Front RMS:       {m1['residuals_px']['front_rms']:.4f} pixels")
print(f"Model 1 Rear RMS:        {m1['residuals_px']['rear_rms']:.4f} pixels")
print(f"Model 1 Dorsal RMS:      {m1['residuals_px']['dorsal_rms']:.4f} pixels")

# Verify the clean 35-point front rim fit
with open("independent-reconstruction/step8_pebble_and_rear_terminus.json") as f:
    step8_data = json.load(f)
front_m3 = step8_data["front_face_models_before_vs_after_single_outlier_exclusion"]["corrected_35pt_clean_rim_excluding_only_theta_minus45"]["M3_Ellipse_Dorsal_Constrained_4DOF"]
print(f"Clean Front Rim RMS:     {front_m3['rms_residual_px']:.4f} pixels")

# Verify the rear 1:1 match
rear_1to1 = step8_data["rear_terminal_contour_analysis"]["exposed_rear_cap_arc_1to1_and_coaxial_match"]["unscaled_1to1_dorsal_front_face_match"]
print(f"Rear 1:1 Match RMS:      {rear_1to1['rms_residual_px']:.4f} pixels")
```

---

## Primary Diagnostic Figures

All diagnostic figures generated by the pipeline are stored in [`independent-reconstruction/figures/`](file:///d:/projects/martian-cylinder/independent-reconstruction/figures/):

- [`diag01_localization_drcx.png`](file:///d:/projects/martian-cylinder/independent-reconstruction/figures/diag01_localization_drcx.png): Full Mastcam context and target subframe localization.
- [`diag02_radiometric_comparison.png`](file:///d:/projects/martian-cylinder/independent-reconstruction/figures/diag02_radiometric_comparison.png): 16-bit linear radiance vs 8-bit tone-mapped comparison across RGB bands.
- [`diag03_subpixel_edges.png`](file:///d:/projects/martian-cylinder/independent-reconstruction/figures/diag03_subpixel_edges.png): Directional subpixel profile extraction and edge polarity tracking.
- [`diag04_endface_models.png`](file:///d:/projects/martian-cylinder/independent-reconstruction/figures/diag04_endface_models.png): Conic and polygonal ODR model comparison across subsets S1–S4.
- [`diag05_competing_3d_models.png`](file:///d:/projects/martian-cylinder/independent-reconstruction/figures/diag05_competing_3d_models.png): 3D perspective convergence proof, transverse clinometry, and SPICE solar shadow vectors.
- [`diag06_robustness_sensitivity.png`](file:///d:/projects/martian-cylinder/independent-reconstruction/figures/diag06_robustness_sensitivity.png): Trimming, estimator perturbation, and Monte Carlo noise injection sweeps.
- [`diag07_pebble_and_rear_terminus_zoom.png`](file:///d:/projects/martian-cylinder/independent-reconstruction/figures/diag07_pebble_and_rear_terminus_zoom.png): Radiometric zoom identifying the upper-right pebble and the rear soil burial boundary.
- [`diag08_pebble_correction_and_rear_terminus.png`](file:///d:/projects/martian-cylinder/independent-reconstruction/figures/diag08_pebble_correction_and_rear_terminus.png): Single outlier exclusion on the front rim and the unscaled 1:1 rear-to-front curvature match.
- [`diag09_joint_geometric_model.png`](file:///d:/projects/martian-cylinder/independent-reconstruction/figures/diag09_joint_geometric_model.png): 85-point joint geometric optimization and collinear cylinder axis resolution.
- [`smoothness_and_roughness_comparison.png`](file:///d:/projects/martian-cylinder/independent-reconstruction/figures/smoothness_and_roughness_comparison.png): Edge straightness, Laplacian surface texture, and photometric light roll-off benchmarked against nearby natural rocks.

---

## Historical Heritage & Citation

This project is dedicated to the memory of **Richard "Sam" Bogner (1931–2015)**, Space Power Systems Engineer at NASA Jet Propulsion Laboratory (Surveyor lunar landers, Mariner Mars 1971 / Mariner 9 orbiter battery subsystem, Hughes Space and Communications, GM SunRaycer). His meticulous technical documentation of Mariner 9's nickel-cadmium batteries on Mars half a century ago inspired the forensic engineering rigor applied here.

### Citation

```bibtex
@techreport{bogner2026martian,
  author      = {Bogner, Justin},
  title       = {Morphological, Photometric, and Geometric Analysis of an Unidentified Cylindrical Feature in Curiosity Sol 3556 Mastcam Imagery},
  institution = {Cambrian Minds},
  year        = {2026},
  month       = nov,
  doi         = {10.5281/zenodo.23789092},
  url         = {https://github.com/CambrianMinds/martian-cylinder}
}
```
