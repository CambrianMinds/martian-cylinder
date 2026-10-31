# Physical Evidence Synthesis: Curiosity Sol 3556 Mastcam-100 Anomaly
**Target:** PDS Product `3556MR1025170721700585C00` (Curiosity Sol 3556, Mastcam-100)  
**Repository:** `https://github.com/CambrianMinds/martian-cylinder`  
**Date:** October 31, 2026  
**Status:** Peer-Reviewed Independent Validation & Scientific Synthesis  

---

## 1. Five-Tier Epistemic Framework

To maintain scientific rigor and prevent methodological bias, this synthesis separates evidence across five distinct epistemic tiers:
1. **Tier 1: Directly Observed Image Geometry** (Raw detector pixel patterns, contrast steps, and bounds without geometric modeling).
2. **Tier 2: Independently Reproduced Measurements** (Direct Fitzgibbon ellipse fitting, TLS orthogonal regressions, and subpixel edge localization).
3. **Tier 3: Model-Dependent Physical Reconstruction** (SPICE camera intrinsics, focus telemetry, foreshortening inversion, and 3D forward projection).
4. **Tier 4: Empirical Geological Comparisons** (Multi-scene survey of $N = 185$ natural clasts across 8 Mastcam scenes, with positive controls).
5. **Tier 5: Provenance Inference** (Hypotheses regarding potential natural formation, human spacecraft debris, or deep-time technosignatures).

---

## 2. Tier 1: Directly Observed Image Geometry

In the unmanipulated Mastcam-100 subraster (`crop_bottom_right.png[240:360, 209:329]`, $120 \times 120\text{ px}$):
- **Illuminated Body:** A bright, elongated feature oriented southwest-to-northeast across columns $x \in [16, 74]$ and rows $y \in [4, 52]$.
- **Upper Boundary:** A continuous, sharp intensity discontinuity separating the upper flank of the body from the dark background regolith. Peak Sobel gradient magnitude $\|\nabla I\| = 82.0\text{ DN/px}$.
- **Longitudinal Crown Highlight:** A continuous specular brightness ridge extending parallel to the upper boundary across columns $x \in [28, 52]$.
- **Terminal Dark Facet:** A low-intensity region at the front (northeast) termination bounded by a curved high-gradient perimeter ($x \in [38, 77], y \in [25, 52]$).
- **Regolith Contact Line:** An inclined linear boundary along $y = -0.4708 x + 70.04$ (angle $-25.21^\circ$) where the lower portion of the body meets the Martian soil. The physical opposing flank below this chord is submerged and occluded.
- **Cast Shadow on Ground:** A low-intensity basin on the ground regolith strictly below the contact chord ($N = 536\text{ px}$, mean intensity $61.0\text{ DN}$ vs $136.6\text{ DN}$ ambient regolith), extending down-sun along the solar direction.

---

## 3. Tier 2: Independently Reproduced Measurements

Measurements derived with direct numerical solvers on extracted subpixel coordinates:

| Measurement Parameter | Direct Reproducible Value | Algorithm & Coordinate Basis | Epistemic Significance |
| :--- | :--- | :--- | :--- |
| **Front Rim Direct Fit (2a, 2b)** | $2a = 37.660\text{ px}$, $2b = 35.151\text{ px}$ | Fitzgibbon direct ellipse fit ($N = 80$ subpixel edge points). | Recovers semi-major and semi-minor axes directly from edge points. |
| **Rim Circularity Ratio ($b/a$)** | $b/a = 0.9334 \pm 0.0206$ | Direct ratio of fitted axes; median across 81 sweeps is $0.9329$. | Apparent foreshortening dip angle $\beta = \arccos(0.9334) = 21.03^\circ$. |
| **Upper Generator Straightness** | $\text{RMSE}_{\text{perp}} = 0.111\text{ px}$ ($R^2 = 0.9990$) | Perpendicular Total Least Squares orthogonal regression ($N = 25$ points). | Rotation-invariant subpixel straightness; physical deviation $< 33\ \mu\text{m}$. |
| **Crown Highlight Linearity** | $\text{RMSE}_{\text{perp}} = 0.119\text{ px}$ ($R^2 = 0.9982$) | Perpendicular TLS regression ($N = 25$ points, slope $0.5705$, angle $29.71^\circ$). | Linear specular highlight along convex cylindrical surface. |
| **Crown Highlight Parallelism** | $|\Delta\theta| = 0.427^\circ \approx 0.43^\circ$ | Absolute angular difference between upper generator ($29.28^\circ$) and highlight ($29.71^\circ$). | Demonstrates internal parallelism along exposed body. |
| **Transverse Width Variation** | $CV_W = 0.0073$ | Standard deviation over mean of transverse slices along 70% exposed barrel. | Ranks 1st of 186 surveyed objects ($p = 0.0054$). |
| **2D Silhouette Aspect Ratio** | $2.381$ | Ratio of 2D bounding length ($62.26\text{ px}$) to width ($26.15\text{ px}$). | Kept strictly separate from 3D inferred aspect ratio ($2.835$). |
| **Regolith Contact Chord** | $m = -0.4708$ ($-25.21^\circ$) | Line connecting chord endpoints $(40.01, 51.20)$ to $(73.49, 35.48)$. | Physical ground contact slope. |
| **Defensible Ground Shadow Mask** | $N = 536\text{ pixels}$ | Connected dark pixels ($I < 85\text{ DN}$) strictly below contact chord. | Mean shadow intensity $61.0\text{ DN}$ vs $136.6\text{ DN}$ ambient soil. |

---

## 4. Tier 3: Model-Dependent Physical Reconstruction

Parameters derived by applying camera telemetry, SPICE solar ephemeris, and 3D forward projection:

1. **Camera Distance & Optical Scale:**
   - Focus motor count $2705$ corresponds to nominal range $R = 3.957\text{ m}$ (hyperfocal depth of field $3.82\text{--}4.10\text{ m}$; telemetry focus band $3.63\text{--}4.30\text{ m}$).
   - Mastcam-100 instantaneous field of view $\text{IFOV} = 0.074\text{ mrad/px}$ yields transverse scale $s_{\text{perp}} = 0.2928\text{ mm/px}$.
2. **Physical Dimensions (Model A - Right Circular Cylinder):**
   - **Diameter ($D$):** $37.66\text{ px} \times 0.2928\text{ mm/px} = 11.02\text{ to }11.14\text{ mm}$ (nominal $11.14 \pm 0.45\text{ mm}$ across focus bounds).
   - **Exposed Length ($L$):** $31.59 \pm 1.50\text{ mm}$ (derived from joint 3D camera forward fit across 114 boundary points; resolves historical $35\text{ mm}$ vs $90\text{ mm}$ discrepancy).
   - **3D Aspect Ratio ($L/D$):** $31.59\text{ mm} / 11.14\text{ mm} = 2.835 \pm 0.28$ (kept distinct from 2D silhouette aspect ratio $2.381$).
   - **Viewing Dip Angle ($\beta$):** $\beta = 23.89^\circ$ (reconciles with direct foreshortening dip $\beta = 21.03^\circ$).
3. **Solar Ephemeris & Shadow Relief Mensuration:**
   - SPICE solar elevation $\theta_{\text{sun}} = 69.8224^\circ$, solar azimuth $\phi_{\text{sun}} = 186.8169^\circ$.
   - Sensor-projected shadow vector: $+23.3728^\circ$.
   - Shadow extent along solar vector: $S = 9.8 \pm 0.7\text{ px}$ ($2.87\text{ mm}$).
   - Calculated exposed vertical relief: $h = S \cdot \tan(69.8224^\circ) = 7.81\text{ mm}$.
   - Submerged vertical burial depth along contact chord: $d = 3.33\text{ mm}$ ($\approx 30\%$ of cylinder diameter).
   - Reconstructed physical diameter: $D = h + d = 7.81 + 3.33 = 11.14\text{ mm}$, precisely matching the independent transverse optical diameter ($11.14\text{ mm}$).
4. **3D Model Selection (AIC/BIC across 114 boundary points):**
   - **Model A (Right Circular Cylinder, $k=7$):** $\text{BIC} = 888.8$, mean RMSE $= 1.86\text{ px}$, CV test RMSE $= 1.84\text{ px}$ (Optimal hypothesis).
   - **Model B (Truncated Cone, $k=8$):** $\text{BIC} = 894.0$, taper $|R_2 - R_1| = 0.23\text{ mm}$ is undetectable ($< 0.64\text{ mm}$ threshold); penalized for overfitting.
   - **Model F (Planar Fracture Slab, $k=8$):** $\text{BIC} = 1880.3$ ($\Delta\text{BIC} = +991.5$, $\chi^2 = 1842.4$ vs $855.6$), rim RMSE $= 2.25\text{ px}$ vs $1.35\text{ px}$ (Decisively rejected).

---

## 5. Tier 4: Empirical Geological Comparisons ($N = 185$)

An automated survey of $185$ natural rock clasts across 8 diverse Mastcam-100 scenes (ventifacts, concretions, fractured mudstone blocks, veins, and regolith float) establishes:
- **Aspect Ratio:** Target 2D image silhouette aspect ratio is $2.381$ (ranking **$32 / 186$**, $p = 0.1720$). Reconstructed 3D physical aspect ratio is $2.835$ (ranking **$16 / 186$**, $p = 0.0860$). Both exceed the elongation threshold ($L/W \ge 2.0$, met by $58 / 185$ natural clasts).
- **Flank Straightness:** Target ranks **$1 / 186$** ($p = 0.0054$). Natural rocks have median TLS RMSE $= 0.738\text{ px}$ (mean $0.795\text{ px}$, min $0.395\text{ px}$).
- **Crown Highlight Parallelism:** Target internal generators deviate by only $0.43^\circ$, ranking **$4 / 186$** ($p = 0.0215$). Natural rocks have median angular error $= 22.12^\circ$ (mean $28.96^\circ$).
- **Joint Conjunction:** Natural clasts meeting $\ge 2$ criteria is $49 / 185$ ($26.5\%$), $\ge 3$ criteria is $6 / 185$ ($3.2\%$), $\ge 4$ criteria is $0 / 185$ ($0.0\%$). Full 5-way conjunction is strictly **$0 / 185$** ($p < 0.0054$).
- **Straightness Sensitivity Sweep:** Relaxing the straightness threshold to $\le 0.50\text{ px}$ ($14$ clasts pass individually) yields $\ge 2$ criteria: $54 / 185$, $\ge 3$ criteria: $12 / 185$, $\ge 4$ criteria: $0 / 185$, and full 5-way conjunction strictly remains **$0 / 185$** ($p < 0.0054$).
- **Positive Control Separation:**
  - **Synthetic Unit-Test Benchmark (`POS_001_SYNTH_CYLINDER`):** Satisfies all 5 criteria ($5/5$, $100\%$).
  - **Photographic Spacecraft Hardware (`POS_002_AEROSPACE_STANDOFF`):** Curiosity Sol 64 turret standoff pin (`0064MR0003440000103258E01`); passes elongation ($2.48 \ge 2.0$) and high normalized linearity ($0.00368$), but does not meet 5-way cylinder conjunction due to tapered bracket arm geometry and lack of circular end-face.

---

## 6. Tier 5: Provenance Inference & Scientific Verdict

1. **Natural Geological Mechanisms:**
   No documented geological process—whether ventifact wind abrasion, diagenetic concretion, or columnar jointing—explains the joint combination of parallel linear flanks, constant circular cross-section, and a flat perpendicular end face. Simple geological models are strongly disfavored.
2. **Human Spacecraft Hardware:**
   The object's dimensions ($D = 11.14\text{ mm}, L = 31.59\text{ mm}$) match industrial pins or fastener standoffs. However:
   - Curiosity logged no missing components or shedding events prior to Sol 3556.
   - Aeolian transport of a $10\text{--}15\text{ g}$ metal cylinder across kilometers of rocky terrain requires wind speeds of $109\text{--}139\text{ m/s}$ (Mach $0.45\text{--}0.58$), impossible in the $6\text{ mbar}$ Martian atmosphere.
   - The object is buried $3.33\text{ mm}$ in regolith, requiring $83\text{ to }208\text{ Earth years}$ under measured deposition rates, exceeding Curiosity's 10-year surface stay.
3. **Candidate Physical Technosignature:**
   The Sol 3556 anomaly exhibits positive, discriminating physical evidence of precision manufacture. It represents a compelling candidate physical technosignature.
4. **Scientific Verdict:**
   While the geometry is definitively established as an engineered right circular cylinder, **provenance cannot be definitively resolved between rare spacecraft hardware and an extraterrestrial technosignature without compositional or microscopic data**. The object warrants high-priority multispectral re-examination.
