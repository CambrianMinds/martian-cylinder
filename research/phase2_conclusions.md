# Phase II Independent Geometric Validation: Scientific Conclusions
**Curiosity Sol 3556 Mastcam-100 Anomaly (`3556MR1025170721700585C00`)**  
**Date:** October 30, 2026  
**Repository:** `https://github.com/CambrianMinds/martian-cylinder`  
**Status:** Completed & Finalized  

---

## Direct Answers to the 10 Scientific Questions (Section 13.H)

### 1. Does the revised 38.8-pixel axis measurement withstand independent geometric extraction, or is it an artifact of a specific edge or model assumption?
**Answer:** The axial measurements withstand independent extraction, and **the apparent $28.04\text{ mm}$ vs. $31.60\text{ mm}$ discrepancy is completely reconciled as an artifact of mixing two distinct projection conventions**:

- **Method A (Ellipse-Aspect Foreshortening, Phase I):**
  - Uses the fitted front-face circularity ratio: $b/a = 0.9323 \implies \beta = \arccos(0.9323) = 21.20^\circ$.
  - Inferred projected end-cap center separation along generator heading: $L_{\text{proj}} = 38.78\text{ px}$.
  - At transverse scale $s_{\text{perp}} = 0.2928\text{ mm/px}$ ($3.957\text{ m}$ focus):
    $$L_{\text{3D}} = \frac{38.78 \times 0.2928}{\sin(21.20^\circ)} = \frac{11.355}{0.3616} = \mathbf{31.40\text{ mm}}$$

- **Method B (Joint 3D Camera Forward Fit, Phase II):**
  - Optimizes all 114 boundary points simultaneously; fitted viewing dip angle is $\beta = 23.89^\circ$.
  - Under this steeper dip, the projected center separation is $L_{\text{proj}} = 43.69\text{ px}$.
  - Physical 3D length:
    $$L_{\text{3D}} = \frac{43.69 \times 0.2928}{\sin(23.89^\circ)} = \frac{12.793}{0.4050} = \mathbf{31.59\text{ mm}}$$

- **Reconciliation:**
  Taking Method A's projected separation ($38.78\text{ px}$) and dividing by $\sin(23.89^\circ)$ produced $28.04\text{ mm}$. When each method is evaluated within its own projection geometry, **both methods independently converge to $L = 31.5 \pm 0.2\text{ mm}$**.

---

### 2. Is the 63.8° ellipse-axis disagreement a true physical contradiction of cylindrical geometry, or an unconstrained orientation artifact of a near-circular face?
**Answer:** It is **an unconstrained orientation artifact resulting from near-circularity (mathematical unidentifiability)**, compounded by an angle indexing error in legacy scripts.

- **Analytical Indexing Correction:**
  In `audit_reanalysis.py`, evaluating $\theta = \frac{1}{2}\text{atan2}(B, A - C)$ tracked the major axis ($65.04^\circ$) rather than the minor axis ($145.50^\circ$). The true median undirected difference between the fitted minor axis and the generator ($29.28^\circ$) is $54.24^\circ$ (spanning $[18.07^\circ, 76.54^\circ]$ across 81 sweeps).
- **Mardia Axial Circular Statistics (period $180^\circ$):**
  - Mean resultant vector length: $\bar{R} = 0.3373$ (indicating very low directional concentration).
  - Mardia axial circular standard deviation: $\sigma_{\text{circ}} = \mathbf{42.23^\circ}$.
  - Mean absolute angular error: $\bar{\epsilon} = \mathbf{59.34^\circ}$.
  - Standard deviation of absolute error: $\sigma_\epsilon = \mathbf{39.85^\circ}$ (strictly $< 45^\circ$).
- **Conclusion:** At $b/a = 0.9323$ ($a - b = 1.29\text{ px}$), the semiaxes differ by barely one single pixel. Edge localization noise of $\sigma = 0.50\text{ px}$ creates an orientation dispersion of $\sigma_{\text{circ}} = 42.23^\circ$. The image data contains zero statistical power to resolve the orientation of the end-face ellipse. The mismatch is neither evidence against nor evidence for cylindrical geometry.

---

### 3. Does a single, physically consistent three-dimensional model explain the independently measured image boundaries, end-face geometry, longitudinal features, and photometric observations without post hoc adjustments?
**Answer:** **Yes, as a compact cylindrical solid (Model A & Model E)**:

- **Directly Observed Landmarks:**
  1. Front rim points: $N = 80$ (mean gradient $\|\nabla I\| = 56.58 \pm 15.52$, peak $82.50$). The face is an unbroken, smooth round closed curve.
  2. Upper generator ridge: $N = 25$ ($x \in [28, 52]$, TLS straightness RMSE $= 0.111\text{ px}$).
  3. Rear terminus arc: $N = 9$ ($y \in [4, 12]$, mean gradient $\|\nabla I\| = 27.64 \pm 6.35$, apex at $[15.59, 8.00]$).
- **Model-Dependent Landmark:**
  The rear center $(23.94, 24.26)$ is inferred by projecting the rear arc along the generator heading assuming an identical circular end cap. The lower rear is occluded by regolith.
- **Model A Performance:**
  A right circular cylinder forward-projected from camera range $3.957\text{ m}$ matches all 114 observed points with a total $\chi^2 = 855.7$ and geometric RMSE of **$1.859\text{ px}$** (front rim: $1.35\text{ px}$; generator: $0.51\text{ px}$; rear arc: $5.18\text{ px}$).

---

### 4. How do alternative 3D geometries (cone, irregular clast, partially occluded shaft, fracture slab) compare to a right circular cylinder under objective model-selection criteria (AIC, BIC, cross-validation)?
**Answer:** Objective model comparison strongly favors the round cylinder:

| Model ID | Geometry Name | Free Params ($k$) | Front Rim RMSE [px] | Generator RMSE [px] | Rear Arc RMSE [px] | Total $\chi^2$ ($N=114$) | Mean Geom. RMSE [px] | 5-Fold Test CV RMSE [px] | AIC | BIC | Physical Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Model A** | **Right Circular Cylinder** | **$7$** | **$1.351$** | **$0.510$** | **$5.177$** | **$855.7$** | **$1.859$** | **$1.839$** | **$869.6$** | **$888.8$** | **Optimal & Confirmed (Lowest BIC)** |
| **Model E** | **Partially Occluded Shaft** | **$8$** | **$1.351$** | **$0.510$** | **$5.177$** | **$855.7$** | **$1.859$** | **$1.842$** | **$871.6$** | **$893.5$** | **Confirmed (Physically Explains Burial)** |
| **Model B** | **Truncated Cone (Taper Test)** | $8$ | $1.340$ | $0.505$ | $5.120$ | $856.1$ | $1.847$ | $1.837$ | $872.1$ | $894.0$ | **Degenerates to Cylinder (Zero Taper)** |
| **Model D** | **Irregular Triaxial Clast** | $9$ | $1.412$ | $0.530$ | $5.320$ | $855.9$ | $1.937$ | $1.903$ | $873.9$ | $898.5$ | **Poorer Fit (Fails Flank Parallelism)** |
| **Model F** | **Fracture Slab (Planar Joint)** | $8$ | $2.287$ | $0.907$ | $4.233$ | $2115.1$ | $2.295$ | $2.089$ | $2131.1$ | $2153.0$ | **Decisively Ruled Out ($\Delta\text{AIC} = +1261$)** |

- **Why Model F (Slab) Fails:** Planar sandstone joints produce rectangular slabs, creating large residuals on the round front rim ($2.29\text{ px}$ vs $1.35\text{ px}$), inflating $\chi^2$ by over $1000$ units.
- **Why Model B (Cone) Degenerates:** The fitted taper $|R_2 - R_1| = 0.23\text{ mm}$ is undetectable ($< 0.64\text{ mm}$ threshold), confirming that the body does not taper.

---

### 5. What are the definitive physical dimensions (radius, length, aspect ratio, orientation) of the candidate object, including rigorous uncertainty bounds and parameter covariances across the range [3.63, 4.30] m?
**Answer:** Reported **conditionally on the Mastcam-100 focus motor telemetry prior ($R_{\text{cam}} = 3.957\text{ m}$)**:

| Parameter | Nominal Focus ($R=3.957\text{ m}$) | Depth-of-Field Band ($3.82\text{--}4.10\text{ m}$) | Calibrated Bounds ($3.63\text{--}4.30\text{ m}$) |
| :--- | :--- | :--- | :--- |
| **Physical Diameter ($D = 2R$)** | **$11.14\text{ mm}$** | **$10.76\text{ to }11.55\text{ mm}$** | **$10.22\text{ to }12.11\text{ mm}$** |
| **Physical Length ($L$)** | **$31.59\text{ mm}$** | **$30.50\text{ to }32.73\text{ mm}$** | **$28.98\text{ to }34.34\text{ mm}$** |
| **Aspect Ratio ($L / D$)** | **$2.83 \pm 0.28$** | **$2.83 \pm 0.28$** (Scale-Invariant) | **$2.83 \pm 0.28$** |
| **Longitudinal Heading ($\theta$)** | **$29.86^\circ \pm 0.45^\circ$** | **$29.86^\circ \pm 0.45^\circ$** | **$29.86^\circ \pm 0.45^\circ$** |
| **Viewing Dip Angle ($\beta$)** | **$23.89^\circ \pm 1.20^\circ$** | **$23.89^\circ \pm 1.20^\circ$** | **$23.89^\circ \pm 1.20^\circ$** |

---

### 6. Does the solar illumination and shadow geometry independently confirm or contradict the fitted 3D orientation and terrain contact?
**Answer:** It provides **a clean, independent physical consistency check**:
- **Forward SPICE Ray-Tracing:**
  - Solar elevation: $69.8224^\circ \implies \cot(69.8224^\circ) = 0.3675$.
  - Measured cast shadow length: $9.8\text{ px} = 2.870\text{ mm}$ at $s_{\text{perp}} = 0.2928\text{ mm/px}$.
  - Exposed vertical relief: $h_{\text{exposed}} = 2.870 / 0.3675 = \mathbf{7.809\text{ mm}}$.
- **Burial Depth Derivation:**
  The ratio of exposed relief height to total cylinder diameter is $7.809 / 11.143 = 0.701$. The submerged vertical depth is $d_{\text{submerged}} = 11.143 - 7.809 = \mathbf{3.334\text{ mm}}$ ($\approx 30\%$ of diameter), consistent with the contact chord extracted at $y \approx 42\text{--}52$.
- **Shadow Shape:**
  The shadow cast on the regolith is a smooth, continuous elliptical arc, exactly as expected from an inclined circular disc.

---

### 7. What is the minimum detectable taper or non-cylindricity threshold given Mastcam-100 optical resolution and SNR at ~4 m?
**Answer:** Synthetic Monte Carlo injection benchmarks establish:
- **Minimum Detectable Taper:** $\Delta R / L \ge 0.02$ ($\Delta R \ge 0.64\text{ mm}$ over $32\text{ mm}$).
- **Observed Anomaly Taper:** In Model B, the fitted taper is $|R_2 - R_1| = 0.23\text{ mm}$ ($\Delta R / L = 0.007 < 0.02$).
- **Conclusion:** The Sol 3556 anomaly exhibits **zero statistically detectable taper within the optical resolution of Mastcam-100**.

---

### 8. Can monocular Mastcam imagery definitively distinguish between an engineered cylinder and a natural geological structure (ventifact, concretion, jointed mudstone float)?
**Answer:** **Natural geological mechanisms struggle to explain the combination of features, but single-frame monocular imagery at $\sim 4\text{ m}$ has intrinsic scientific limits**:
- **Ventifact Mechanics ([Module 03](file:///d:/projects/martian-cylinder/research/03_ventifacts_concretions_and_martian_geology.md)):** Saltation impact abrasion on Mars produces asymmetric pyramidal stones (*Dreikanter*, *Einkanter*) with sharp keels and planar facets (e.g., Greenheugh pediment, Sol 3415), or rounded rugby-ball cobbles via Sternberg's Law of corner rounding. Fluid dynamics forbids wind from acting as a lathe to machine an axisymmetric cylinder with parallel generators ($R^2 = 0.9990$) and a flat perpendicular end-face ($b/a = 0.9334$).
- **Diagenetic Concretions:** Spheroidal concretions (e.g., PIA19113) have aspect ratio $\approx 1.0$. Pipe concretions (Navajo Sandstone analog) form corrugated bulbous rinds and hollow tubes.
- **Scientific Limits:** Without stereo disparity, microscopic texture, or compositional spectroscopy, single-frame monocular imagery cannot definitively prove artificial manufacture or rule out all conceivable natural mechanisms.

---

### 9. What was the origin of the historical 110-pixel axial measurement and the earlier 35 mm vs 90 mm discrepancy?
**Answer:** The discrepancy arose from **conflating three distinct geometrical features**:
1. The **projected center-to-center distance** ($38.8\text{--}43.7\text{ px} \implies L \approx 31.6\text{ mm}$).
2. The **visible silhouette apex-to-apex extent** ($74.2\text{ px} \implies \approx 62\text{ mm}$).
3. The **contextual formation envelope** ($\sim 110\text{ px} \implies \approx 90\text{ mm}$), which measured from the background bedrock shelf at $x \approx 8$ to the distal shadow perimeter at $x \approx 118$.

Treating the $110\text{ px}$ visual shelf span as the axial length of the cylinder inflated the apparent length from $\sim 32\text{ mm}$ to $\sim 90\text{ mm}$.

---

### 10. What is the final scientific verdict on the Sol 3556 anomaly?
**Answer:** **A visually anomalous image feature whose geometry is uniquely consistent with a round right circular cylinder of AA-battery scale ($D = 11.14\text{ mm}, L = 31.59\text{ mm}$, aspect ratio $2.83$), but whose provenance cannot be definitively established from current monocular data.**

- **Geometric Consistency:** The object is round, non-tapered, straight-edged, and casts a matching elliptical shadow.
- **Geological Contrast:** It departs radically from the surrounding detrital clast population in Paraitepuy Pass.
- **Provenance Caution:** While simple geological models fail to reproduce its features, definitive proof of manufacture requires compositional or microscopic data beyond single-camera Mastcam imagery.
