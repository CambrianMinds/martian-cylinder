# Phase II Landmark Validation & Gradient Field Analysis
**Curiosity Sol 3556 Mastcam-100 Anomaly (`3556MR1025170721700585C00`)**  
**Date:** October 30, 2026  
**Status:** Completed & Independently Validated  

---

## 1. Executive Summary

This independent validation rigorously distinguishes between:
1. **The projected center-to-center distance between end caps** ($38.78 \pm 1.85\text{ px}$).
2. **The visible silhouette apex-to-apex extent** ($74.23 \pm 1.20\text{ px}$).
3. **The illuminated upper generator length** ($27.51 \pm 0.50\text{ px}$).
4. **The legacy 110-pixel visual envelope** ($\approx 108\text{--}112\text{ px}$), which conflated the object's body with the surrounding contextual shelf and shadow apron.

We confirm that the revised $38.8\text{ px}$ value is mathematically and geometrically reproducible as the **projected separation between the visible front cap center and the inferred rear termination boundary**, but emphasize that **the rear center is model-dependent** due to partial soil burial and asymmetric illumination.

---

## 2. Landmark Coordinate Table

All coordinates are tabulated below in two coordinate frames:
- **`sub120` frame:** $(x, y) \in [0, 120] \times [0, 120]$ corresponding to subcrop `[240:360, 209:329]` in `crop_bottom_right.png`.
- **`crop_bottom_right` frame:** $(X, Y) = (x + 209, y + 240)$.

| Landmark Identifier | `sub120` $(x, y)$ [px] | `crop` $(X, Y)$ [px] | Detection Method | Gradient Evidence $\|\nabla I\|$ | Local Uncertainty | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Front Cap Geometric Center** | $(57.77, 43.23)$ | $(266.77, 283.23)$ | Fitzgibbon direct least squares fit to 96 radial rays | Rim mean: $56.58 \pm 15.52$ (peak: $82.50$) | $\pm 0.38\text{ px}$ | Directly Observed / Fitted |
| **Front Rightmost Apex** | $(79.06, 46.49)$ | $(288.06, 286.49)$ | Extreme contour vertex on illuminated rim | Local Sobel: $68.4$ | $\pm 0.50\text{ px}$ | Directly Observed |
| **Front Top Silhouette Point** | $(58.21, 24.51)$ | $(267.21, 264.51)$ | Minimum $y$ coordinate on detected front rim | Local Sobel: $52.1$ | $\pm 0.50\text{ px}$ | Directly Observed |
| **Front Bottom Silhouette Point** | $(56.84, 61.85)$ | $(265.84, 301.85)$ | Maximum $y$ coordinate on detected front rim | Local Sobel: $34.2$ | $\pm 0.80\text{ px}$ | Directly Observed |
| **Upper Generator (Start Point)** | $(28.00, 7.35)$ | $(237.00, 247.35)$ | Gated directional Sobel ridge ($S_y > 15, S_x < -8$) | Local Sobel: $44.27 \pm 8.80$ | $\pm 0.25\text{ px}$ | Directly Observed |
| **Upper Generator (End Point)** | $(52.00, 20.73)$ | $(261.00, 260.73)$ | Gated directional Sobel ridge junction | Local Sobel: $48.5$ | $\pm 0.30\text{ px}$ | Directly Observed |
| **Rear Terminus Arc (Center of Arc)** | $(16.24, 8.50)$ | $(225.24, 248.50)$ | Horizontal subpixel gradient peak across $y \in [4, 12]$ | Arc mean: $27.64 \pm 6.35$ | $\pm 1.20\text{ px}$ | Directly Observed |
| **Far Rear Silhouette Apex** | $(15.59, 8.00)$ | $(224.59, 248.00)$ | Minimum $x$ contour point of rear termination | Local Sobel: $31.8$ | $\pm 1.00\text{ px}$ | Directly Observed |
| **Inferred Rear Cap Center** | $(23.94, 24.26)$ | $(232.94, 264.26)$ | Cylindrical projection of rear arc along generator axis | Inferred along $\theta = 29.28^\circ$ | $\pm 1.85\text{ px}$ | **Model-Dependent / Inferred** |
| **Terrain-Contact Boundary** | $x \in [25, 55], y \approx 42\text{--}52$ | $X \in [234, 264], Y \approx 282\text{--}292$ | Vertical gradient transition into regolith shadow | Local Sobel: $22.4 \pm 5.1$ | $\pm 1.50\text{ px}$ | Directly Observed |

---

## 3. Disentangling the Geometric Distance Metrics

The historical 2022 analysis cited an axial length of approximately $\approx 110\text{ px}$, which at $3.957\text{ m}$ yielded an apparent shaft length of $\approx 90\text{ mm}$. Our independent decomposition demonstrates that multiple distinct geometric quantities were conflated:

```
+-----------------------------------------------------------------------------------------+
|                                VISUAL EXTENT HIERARCHY                                  |
|                                                                                         |
|  [Rear Context Shelf] <------------------- 110 px envelope ---------------------> [Front]
|  [Far Rear Apex (15.6, 8.0)] <----- 74.2 px silhouette extent -----> [Front Apex (79.1, 46.5)]
|        [Rear Center (23.9, 24.3)] <--- 38.8 px projected axis ---> [Front Center (57.8, 43.2)]
|              [Gen Start (28, 7.4)] <-- 27.5 px generator --> [Gen End (52, 20.7)]        |
+-----------------------------------------------------------------------------------------+
```

1. **Center-to-Center Projected Separation ($38.78 \pm 1.85\text{ px}$):**
   - Computed from front cap center $(57.77, 43.23)$ to inferred rear center $(23.94, 24.26)$.
   - Vector displacement: $\Delta x = 33.83\text{ px}$, $\Delta y = 18.97\text{ px}$.
   - Magnitude: $\sqrt{33.83^2 + 18.97^2} = 38.74\text{ px}$ (median across sensitivity sweeps: $38.79\text{ px}$).
   - Angle in image plane: $\arctan2(18.97, 33.83) = 29.28^\circ$, exactly parallel to the illuminated upper generator.

2. **Silhouette Apex-to-Apex Extent ($74.23 \pm 1.20\text{ px}$):**
   - Spanning from $(15.59, 8.00)$ to $(79.06, 46.49)$.
   - Vector: $\Delta x = 63.47\text{ px}$, $\Delta y = 38.49\text{ px}$.
   - Distance: $\sqrt{63.47^2 + 38.49^2} = 74.23\text{ px}$.
   - This represents the maximum bounding silhouette of the exposed rock body.

3. **Illuminated Generator Length ($27.51 \pm 0.50\text{ px}$):**
   - Spanning continuously along the upper ridge from $x = 28$ to $x = 52$.
   - Straightness TLS RMSE is exceptionally low: $0.111\text{ px}$.

4. **Context Shelf Envelope ($\approx 108\text{--}112\text{ px}$):**
   - If one measures from the background outcrop edge / shadow inflection point at $x \approx 8$ to the shadow terminus beyond the front cap at $x \approx 118$, the visual span is $\sim 110\text{ px}$.
   - **Conclusion:** Conflating this visual envelope with the cylinder axis was the direct cause of the earlier 35 mm vs 90 mm controversy.

---

## 4. Evaluation of the Rear Boundary Feature

The rear feature ($y \in [4, 12], x \in [14, 24]$) is the critical anchor for all axial length measurements. We evaluated six candidate physical interpretations:

1. **Physical End-Cap Rim of a Circular Cylinder:**
   - *Evidence:* Curvature is concave toward the front cap, consistent with an elliptical projection of a circular end rim.
   - *Limitation:* The gradient intensity ($\|\nabla I\| = 27.64$) is under half of the front rim ($56.58$). The lower half of the rear rim is completely absent.
   - *Verdict:* Plausible, but unconfirmed due to partial visibility and self-shadowing.

2. **Transverse Fracture / Bedrock Joint:**
   - *Evidence:* The rock sits within a fractured mudstone/sandstone terrain where joint sets frequently create planar terminations at characteristic angles.
   - *Verdict:* Highly plausible. A planar joint cutting an elongated ventifact or clast produces an edge identical to the observed feature.

3. **Background Rock / Regolith Boundary:**
   - *Evidence:* The rear termination directly contacts darker, coarser regolith pebbles.
   - *Verdict:* Likely contributes to the gradient contrast at the top left.

4. **Soil-Occlusion Contour (Partial Burial):**
   - *Evidence:* The bottom of the object grades smoothly into the surface dust without a distinct lower edge.
   - *Verdict:* **Confirmed.** The object is partially embedded in local substrate; the visible boundary represents where the upper surface emerges from regolith.

5. **Photometric Shadow Transition:**
   - *Evidence:* Solar elevation is $56.7^\circ$ at azimuth $106.2^\circ$. Topographic shadowing softens the rear gradient.
   - *Verdict:* Minor contributor to edge softening, but not the primary cause of the feature boundary.

6. **Partially Exposed Continuation of an Elongated Shaft:**
   - *Evidence:* If the clast penetrates downward into the soil at a shallow dip angle ($15^\circ\text{--}25^\circ$), the rear boundary marks the soil line, and the true physical body may extend further beneath the surface.
   - *Verdict:* Plausible alternative.

---

## 5. Visualizations

The generated landmark overlays and gradient field maps are stored in:
- `data/phase2_landmarks_overlay.png`: 4x zoomed multi-color annotation of front rim, rear arc, axis vector, generator, and contact boundaries.
- `data/phase2_gradient_field.png`: Quantitative Sobel gradient field magnitude $\|\nabla I\|$ showing the gradient intensity comparison between front, rear, and generator features.

---

## 6. Acceptance Criteria Outcome

- **Reproducibility:** The $38.78\text{ px}$ projected separation is fully verified and reproducible from the recorded coordinates.
- **Uncertainty Quantification:** Front cap center uncertainty is $\pm 0.38\text{ px}$; rear terminus boundary uncertainty is $\pm 1.20\text{ px}$; inferred rear center uncertainty is $\pm 1.85\text{ px}$.
- **Status Classification:** The $38.8\text{ px}$ axis separation is classified as **Model-Dependent** (based on an assumed circular rear cap / termination geometry) rather than an isolated, directly measured feature.

