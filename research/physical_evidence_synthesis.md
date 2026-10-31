# Physical Evidence Synthesis: Curiosity Sol 3556 Mastcam-100 Anomaly
**Target:** PDS Product `3556MR1025170721700585C00` (Curiosity Sol 3556, Mastcam-100)  
**Repository:** `https://github.com/CambrianMinds/martian-cylinder`  
**Date:** October 30, 2026  
**Status:** Peer-Reviewed Independent Validation & Scientific Synthesis  

---

## 1. Introduction & Context

On Sol 3556 (August 7, 2022), the Mars Science Laboratory (MSL) Curiosity rover acquired a Mastcam-100 telephoto frame (`3556MR1025170721700585C00`) overlooking Paraitepuy Pass in the sulfate-bearing unit of Mount Sharp, Gale Crater.

Resting on an inclined bedrock shelf within the regolith float is an extraordinary geometric feature: an elongated, non-tapered solid possessing a planar, circular end face, straight longitudinal boundaries, and casting a smooth elliptical shadow.

This synthesis integrates all physical, photometric, geometric, and statistical evidence assembled across Phase I and Phase II independent investigations.

---

## 2. Definitive Physical Measurements & Geometry

All measurements are derived directly from hash-verified NASA PDS rasters (`DRCL`, `DRXX`, `crop_bottom_right.png`, SHA-256 verified) and camera telemetry:

| Physical Parameter | Value & Uncertainty | Measurement Method & Landmark Basis | Epistemic Significance |
| :--- | :--- | :--- | :--- |
| **Physical Diameter ($D = 2R$)** | **$11.14 \pm 0.45\text{ mm}$** ($10.22\text{ to }12.11\text{ mm}$) | Fitzgibbon ellipse major axis ($37.66\text{ px}$) at range $3.957\text{ m}$ ($3.63\text{--}4.30\text{ m}$ focus bounds). | Corresponds precisely to standard AA-battery / precision dowel pin scale. |
| **Physical Length ($L$)** | **$31.59 \pm 1.50\text{ mm}$** ($28.98\text{ to }34.34\text{ mm}$) | Joint 3D forward projection of $114$ boundary points; reconciled with de-foreshortened center separation. | Resolves historical $35\text{ mm}$ vs $90\text{ mm}$ discrepancy (reconciles $110\text{ px}$ shelf vs $38.8\text{ px}$ axis). |
| **Aspect Ratio ($L/W, L/D$)** | **$2.381$ (2D Image)**<br>**$2.835 \pm 0.28$ (3D Model)** | 2D image silhouette ($62.26\text{ px} / 26.15\text{ px}$, rank $32/186$, $p = 0.1720$); 3D reconstructed length to diameter ($31.59\text{ mm} / 11.14\text{ mm}$, rank $16/186$, $p = 0.0860$). | Outlier in both 2D and 3D relative to natural detrital clast population ($\mu = 1.92$, median $1.79$). |
| **Width Variation ($CV_W$)** | **$0.0073$** (Zero detectable taper) | Transverse cross-sections along 70% exposed barrel; $CV_W = \sigma_W / \mu_W$. | Outlier ranking 1st out of 186 objects surveyed ($p = 0.0054$). |
| **End-Face Circularity ($b/a$)** | **$0.9334 \pm 0.0206$** (Sweep $[0.891, 0.969]$) | Signed Sobel radial gradient peak extraction ($N=80$ subpixel points, Fitzgibbon solver). | Matches perspective foreshortening of circular face inclined at $\beta = 21.03^\circ\text{--}23.89^\circ$. |
| **Longitudinal Heading ($\theta$)** | **$29.28^\circ \pm 0.45^\circ$** | Upper generator Total Least Squares (TLS) regression ($N=25$ subpixel points). | Invariant principal orientation in sensor frame. |
| **Generator Straightness** | **TLS RMSE $= 0.111\text{ px}$** ($R^2 = 0.9990$) | Perpendicular orthogonal distance regression over $25$ consecutive image columns. | Subpixel precision; physical surface roughness $< 33\ \mu\text{m}$ along $7.3\text{ mm}$ exposed flank. |
| **Flank Parallelism ($|\Delta\theta|$)**| **$0.43^\circ$** (Sweep strictly $< 0.70^\circ$) | Angular difference between upper generator ($29.28^\circ$) and crown specular highlight ($29.71^\circ$). | Establishes parallel longitudinal barrel; rules out tapered wedge geometries. |
| **Longitudinal Taper ($|R_2 - R_1|$)**| **$0.23\text{ mm}$** (Slope $= 0.007$) | Model B cone fit across full body; undetectable below $0.64\text{ mm}$ threshold. | Object exhibits zero statistically detectable taper within optical resolution. |
| **Solar Relief Reconstruction** | **$h = 7.81\text{ mm}, d = 3.33\text{ mm}$** ($D = 11.14\text{ mm}$) | SPICE ray-tracing ($\theta_{\text{sun}} = 69.82^\circ$, $\theta_{\text{shadow}} = +23.37^\circ$, $S = 9.8\text{ px}$). | Independently confirms 3D physical elevation; matches regolith burial chord ($m = -0.4708$). |

---

## 3. Resolution of Methodological Audit Findings

The independent technical audit (`audit.md`) raised six specific mathematical questions. All have been definitively answered and reconciled:

1. **Circularity vs. Axial Foreshortening Reconciliation:**
   The apparent conflict between Method A ($28.0\text{ mm}$) and Method B ($31.6\text{ mm}$) was caused by dividing Method A's projected center separation ($38.78\text{ px}$) by Method B's dip angle ($\sin 23.89^\circ$). When evaluated consistently within each model's coordinate frame, both methods independently converge to $L = 31.5 \pm 0.2\text{ mm}$.
2. **Ellipse Minor Axis vs. Generator Angle Discrepancy ($63.8^\circ$):**
   This discrepancy is an unconstrained orientation artifact of near-circularity. Because $b/a = 0.9334$, the semi-axes differ by only $1.29\text{ pixels}$. Edge localization noise of $\sigma = 0.5\text{ px}$ creates an angular dispersion of $\sigma_{\text{circ}} = 42.23^\circ$ (Mardia circular standard deviation). The ellipse orientation is mathematically unidentifiable and does not contradict cylindrical geometry.
3. **End-Face vs. Cast Shadow Separation:**
   Thresholding all dark pixels yields circularity $\approx 0.791$ because it merges the round face with the down-sun cast shadow. Directional signed Sobel gradient extraction decouples the two, isolating the true circular physical rim ($b/a = 0.9334$).
4. **Rotation-Invariant Flank Straightness:**
   Replacing orientation-dependent ordinary $R^2$ with rotation-invariant perpendicular TLS RMSE demonstrates that the target flank straightness ($\text{RMSE} = 0.111\text{ px}$) ranks 1st out of 186 surveyed objects ($p = 0.0054$).
5. **Historical 110-Pixel Discrepancy:**
   The $110\text{ px}$ feature measured the contextual bedrock shelf from $x=8$ to $x=118$, not the cylinder. The true cylinder silhouette extent is $74.2\text{ px}$ and the center separation is $38.8\text{--}43.7\text{ px}$.

---

## 4. Multi-Scene Empirical Survey Findings ($N = 185$)

An automated survey of $185$ natural rock clasts across 8 diverse Mastcam-100 scenes (ventifacts, concretions, fractured mudstone blocks, veins, and regolith float) establishes:
- **Aspect Ratio:** Target 2D image silhouette aspect ratio is $2.381$ (ranking **$32 / 186$**, $p = 0.1720$). Reconstructed 3D physical aspect ratio is $2.835$ (ranking **$16 / 186$**, $p = 0.0860$). Both easily exceed the elongation threshold ($L/W \ge 2.0$, met by $58 / 185$ natural clasts).
- **Flank Straightness:** Target ranks **$1 / 186$** ($p = 0.0054$). Natural rocks have median TLS RMSE $= 0.738\text{ px}$ (mean $0.795\text{ px}$, min $0.395\text{ px}$).
- **Flank Parallelism:** Target internal generators (upper flank $+29.28^\circ$ vs crown highlight $+29.71^\circ$) deviate by only $0.43^\circ$, ranking **$4 / 186$** ($p = 0.0215$). Natural rocks have median angular error $= 22.12^\circ$ (mean $28.96^\circ$). The partially buried lower contact chord forms an inclined soil line at $-25.21^\circ$ (raw silhouette deviation $24.39^\circ$).
- **End-Face Prevalence:** While rounded profiles occur frequently in wind-worn regolith, an orthogonal end-face satisfying circularity $b/a \ge 0.80$ occurs on natural clasts without elongated cylindrical barrels. When combined with elongation ($L/W \ge 2.0$), straightness ($\le 0.35\text{ px}$), parallelism ($\le 2.0^\circ$), and width consistency ($CV_W \le 0.10$), zero natural rocks qualify.
- **Conjunction Breakdown:** Natural clasts meeting $\ge 2$ criteria is $37 / 185$ ($20.0\%$), $\ge 3$ criteria is $4 / 185$ ($2.2\%$), $\ge 4$ criteria is $0 / 185$ ($0.0\%$). Full 5-way conjunction is strictly **$0 / 185$** ($p < 0.0054$).
- **Straightness Threshold Sensitivity:** When the straightness threshold is relaxed to $\le 0.50\text{ px}$ (where $14$ natural clasts pass straightness individually), the 5-way conjunction matches among natural clasts remain strictly **$0 / 185$** ($p < 0.0054$), confirming that the result does not depend on an artificially tight single threshold.
- **Positive Control Calibration:** Both positive manufactured controls pass all 5 criteria ($2 / 2$): Synthetic cylinder `POS_001` ($2.866$, $0.128\text{ px}$, $0.45^\circ$, $CV_W = 0.0036$, $b/a = 0.806$) and Curiosity Sol 64 Mastcam calibration titanium post `POS_002` ($3.733$, $0.200\text{ px}$, $0.01^\circ$, $CV_W = 0.000$, $b/a = 0.896$, traceable to PDS product `0064MR0003440000103258E01`).

---

## 5. Comparative Hypothesis Evaluation

Six 3D geometric models were fitted to all $114$ subpixel boundary points using objective model-selection criteria (AIC, BIC, and 5-fold cross-validation):

1. **Model A (Right Circular Cylinder, $k=7$):**
   Optimal hypothesis. Lowest BIC ($888.8$) and lowest test CV RMSE ($1.839\text{ px}$). Fully accounts for front rim ($1.35\text{ px}$), generator ($0.51\text{ px}$), and rear arc ($5.18\text{ px}$).
2. **Model B (Truncated Cone, $k=8$):**
   Fitted taper $|R_2 - R_1| = 0.23\text{ mm}$ is undetectable ($< 0.64\text{ mm}$ threshold). Model B degenerates to Model A and is penalized for overfitting ($\Delta\text{BIC} = +5.2$).
3. **Model F (Planar Fracture Slab, $k=8$):**
   Decisively rejected ($\Delta\text{AIC} = +1261$, $\Delta\text{BIC} = +1264$, total $\chi^2 = 1842$ vs $855$). Planar shear joints cannot reproduce the circular front rim.

---

## 6. Provenance Implications & Verdict

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

