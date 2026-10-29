# Agent Instructions: Close All Peer-Review Audit Findings (`CMR-2026-01`)

Execute the following upgrades across the repository to resolve Findings A, B, and C from the independent evidence audit.

## 1. Upgrade `reproduce_analysis.py` (Resolves Finding C & Finding A)

Modify `reproduce_analysis.py` so that every measurement is computed directly from the raw pixel arrays and verified against a locked cryptographic manifest (no reused constants):

1. **Lock Full 64-Character SHA-256 Checksums:**
   - Compute the full 64-hex-character SHA-256 hash of all eight raw PDS files in `data/` (`3556MR1025170721700585C00_{DRCL,DRCX,DRLX,DRXX}.{IMG,LBL}`) plus `3556MR1025170721700585C00_DRCL.png` and `crop_bottom_right.png`.
   - Embed these exact 64-character strings in an immutable `EXPECTED_SHA256` dictionary at the top of `reproduce_analysis.py` and `assert actual_hash == expected_hash` for every file.

2. **Invoke Live Pixel-Level Contour Extraction & Ellipse Fitting:**
   - In Section 4 of `main()`, do **not** hardcode `b_over_a = 35.12 / 37.63`.
   - Instead, extract the $120 \times 120$ sub-raster `DRCL[940:1060, 1009:1129]`, compute the sub-pixel Sobel gradient magnitude $|G| = \sqrt{S_x^2 + S_y^2}$ and directional gradients $(S_x, S_y)$ using parabolic 3-point sub-pixel peak interpolation along radial rays emanating from the end-cap centroid $(x_c \approx 57.5, y_c \approx 48.0)$ (excluding the ground-shadow sector at $+23.37^\circ$ and the adjacent right-hand rock clast).
   - Pass the extracted sub-pixel rim coordinates $(x_{\text{rim}}, y_{\text{rim}})$ directly into `fit_ellipse_fitzgibbon(x_rim, y_rim)` in `main()`, print the fitted `(major_2a, minor_2b, circ_ratio, theta_deg)`, and `assert` that the live pixel fit reproduces $2a \approx 37.63\text{ px}$, $2b \approx 35.12\text{ px}$, and $b/a = 0.9335 \pm 0.005$.

3. **Invoke Live Pixel-Level Generator Parallelism ($R^2$) Regression:**
   - Extract the upper illuminated generator ridge and lower shadow-boundary generator ridge across the cylinder barrel from the $120 \times 120$ sub-raster using vertical column gradient extrema ($S_y$ peaks/valleys along the barrel axis $\theta \approx 218^\circ$).
   - Run ordinary least squares (`np.polyfit`) on the extracted pixel coordinates to compute the coefficient of determination $R^2$ and angular divergence $\Delta\theta$ directly from the image pixels, and `assert R2 > 0.995`.

4. **Explicitly Separate 3D Cylinder Cross-Section Scale vs. Axial Foreshortening (Resolves Finding A):**
   - Update Section 2 of `reproduce_analysis.py` to print a complete, unambiguous uncertainty matrix separating **pixel measurement method** ($D_{\text{3D}} = 34.0\text{ px}$ true cylinder barrel vs. $D_{\text{Sobel}} = 37.63\text{ px}$ 2D Sobel kernel-broadened ellipse major axis, which includes $\sim 1.8\text{ px}$ of $3 \times 3$ convolution broadening) from **slant-range depth-of-field bounds** ($r \in [3.63, 4.30]\text{ m}$, nominal $s_0 = 3.957\text{ m}$):
     - **Normal-to-view scale ($s_\perp = r \cdot \text{IFOV}$):** Applies directly to the transverse diameter $D$ of a 3D right circular cylinder, because any plane tangent to the side of a 3D circular cylinder presents a constant cross-sectional width $D$ perpendicular to the line of sight regardless of viewing elevation (unlike a flat 2D paint mark on a horizontal floor, which would foreshorten by $\sin 22^\circ$).
       - At $r = 3.63\text{ m}$ ($s_\perp = 0.269\text{ mm/px}$): $34.0\text{ px} \rightarrow 9.13\text{ mm}$; $37.63\text{ px} \rightarrow 10.11\text{ mm}$.
       - At $r = 3.957\text{ m}$ ($s_\perp = 0.293\text{ mm/px}$): $34.0\text{ px} \rightarrow 9.96\text{ mm}$; $37.63\text{ px} \rightarrow 11.02\text{ mm}$.
       - At $r = 4.30\text{ m}$ ($s_\perp = 0.318\text{ mm/px}$): $34.0\text{ px} \rightarrow 10.82\text{ mm}$; $37.63\text{ px} \rightarrow 11.97\text{ mm}$.
     - **3D Axial Foreshortening Scale ($s_{\text{axial}} = s_\perp / \cos\beta = 0.317\text{ mm/px}$ at $s_0 = 3.957\text{ m}$):** Applies to the longitudinal axis $L$ and ground-projected chord measurements where the cylinder axis is inclined by $\beta = \arccos(b/a) \approx 21.0^\circ\text{--}23.8^\circ$ relative to the sensor plane ($\cos\beta \approx 0.924$, $1/\cos\beta \approx 1.082$):
       - At $r = 3.63\text{ m}$ ($s_{\text{axial}} = 0.291\text{ mm/px}$): $34.0\text{ px} \rightarrow 9.89\text{ mm}$; $37.63\text{ px} \rightarrow 10.95\text{ mm}$; $L(110\text{ px}) \rightarrow 32.0\text{ mm}$.
       - At $r = 3.957\text{ m}$ ($s_{\text{axial}} = 0.317\text{ mm/px}$): $34.0\text{ px} \rightarrow 10.78\text{ mm}$; $37.63\text{ px} \rightarrow 11.93\text{ mm}$; $L(110\text{ px}) \rightarrow 34.87\text{ mm}$.
       - At $r = 4.30\text{ m}$ ($s_{\text{axial}} = 0.344\text{ mm/px}$): $34.0\text{ px} \rightarrow 11.71\text{ mm}$; $37.63\text{ px} \rightarrow 12.96\text{ mm}$; $L(110\text{ px}) \rightarrow 37.89\text{ mm}$.

5. **Include Distribution-Free Non-Parametric Tests in Section 5 (Resolves Finding B):**
   - Alongside the population ($\text{ddof}=0$) and sample ($\text{ddof}=1$) standardized $z$-scores, compute and print:
     - **Chebyshev's Inequality Upper Bound** ($P(|X - \mu| \ge k\sigma) \le 1/k^2$, valid for *any* probability distribution with finite variance):
       - Aspect ratio ($k = 12.06$): $P \le 1 / 12.06^2 = 6.88 \times 10^{-3}$ ($0.69\%$).
       - Parallelism ($k = 10.70$): $P \le 1 / 10.70^2 = 8.74 \times 10^{-3}$ ($0.87\%$).
     - **One-Sided Cantelli (Chebyshev-Cantelli) Inequality Bound** ($P(X - \mu \ge k\sigma) \le 1/(1 + k^2)$):
       - Aspect ratio: $P \le 6.83 \times 10^{-3}$; Parallelism: $P \le 8.66 \times 10^{-3}$.
     - **Exact Non-Parametric Empirical Rank / Exceedance Test ($N = 20$ controls + $1$ target = $21$):**
       - Target ranks $1/21$ ($p_{\text{emp}} = 1/21 = 0.0476$) on both aspect ratio and parallelism, exceeding the maximum control rock in the scene by $2.08\times$ in aspect ratio ($3.24$ vs. $\max = 1.56$) and $3.69\times$ in generator parallelism ($0.9985$ vs. $\max = 0.2708$).

---

## 2. Update `data/control_rocks_distribution.json` & Control Verification

1. Add the pixel bounding-box / centroid coordinates `(x_px, y_px, w_px, h_px)` in `3556MR1025170721700585C00_DRCL.png` for each of the $N=20$ control clasts in `data/control_rocks_distribution.json` (or provide a companion `verify_control_clasts()` function in `reproduce_analysis.py` that extracts their Sobel contours directly from `DRCL.png` and verifies that the JSON metrics match the pixel-derived contours).
2. Update the `EXPECTED_SHA256` manifest in `reproduce_analysis.py` if `control_rocks_distribution.json` is modified.

---

## 3. Update `martian_cylinder_paper.tex` & `martian_cylinder_paper.md` (Resolves Findings A & B)

1. **Section 3.2 (Spatial Resolution and Physical Scale):**
   - Explicitly distinguish between:
     - **Normal-to-Sight Transverse Cylinder Scale ($s_\perp = r \cdot \text{IFOV} = 0.293\text{ mm/px}$ at $3.957\text{ m}$, $[0.269, 0.318]\text{ mm/px}$ across $r \in [3.63, 4.30]\text{ m}$):** Explain geometrically why a 3D circular cylinder's transverse diameter $D$ projects perpendicular to the viewing ray without $1/\sin(22^\circ)$ flat-ground foreshortening (yielding $D_\perp = 9.96\text{ mm}$ for $34.0\text{ px}$ at $3.957\text{ m}$, or $9.13\text{--}11.97\text{ mm}$ across the full DoF and $34.0\text{--}37.63\text{ px}$ method envelope).
     - **3D Foreshortened Axial Scale ($s_{\text{axial}} = s_\perp / \cos\beta = 0.317\text{ mm/px}$ at $3.957\text{ m}$):** Explain that because the cylinder's longitudinal axis is inclined by $\beta \approx 21.0^\circ\text{--}22.0^\circ$ relative to the sensor plane, axial and ground-projected dimensions scale by $1/\cos\beta \approx 1.082$ (yielding $10.78\text{--}11.93\text{ mm}$ at $3.957\text{ m}$ and $34.87\text{ mm}$ exposed length). Clarify why the naive flat-ground depth factor $1/\sin(22^\circ) = 2.67$ applies only to zero-relief 2D markings painted on a horizontal plane along the camera azimuth, not to a 3D solid of revolution oriented nearly broadside ($\theta = 218^\circ$).
2. **Section 4.4 & Table 1 (Empirical Null Distribution & Statistical Significance):**
   - Retain the exact standardized $z$-scores ($+12.06\,\sigma$ sample SD / $+12.56\,\sigma$ tabulated for aspect ratio; $+10.70\,\sigma$ sample SD / $+10.97\,\sigma$ population SD for $R^2$ parallelism).
   - Remove the parametric Gaussian tail extrapolation ($p < 10^{-9}$) for bounded $R^2 \in [0, 1]$ and small $N=20$, and replace it with:
     - The distribution-free **Cantelli / Chebyshev inequality bound** ($p \le 1/(1+k^2) < 0.0087$ for parallelism and $p < 0.0069$ for aspect ratio under arbitrary non-Gaussian distributions).
     - The exact **non-parametric empirical exceedance bound** ($p = 1/(N+1) = 0.0476$ per metric, and $3.69\times$ higher $R^2$ than the highest natural clast in the scene).
3. **Recompile PDFs:**
   - Run `pdflatex -interaction=nonstopmode martian_cylinder_paper.tex` twice and `pdflatex -interaction=nonstopmode citizen_science_article.tex` twice.
   - Verify zero `Overfull \hbox` warnings and confirm page counts remain clean.

---

## 4. Update `README.md`, `index.html`, and `llms.txt`

1. **Update Key Findings Table in `README.md` and `llms.txt`:**
   - Report both the normal-to-view transverse diameter interval ($9.1\text{--}12.0\text{ mm}$ across $s_\perp \in [0.269, 0.318]\text{ mm/px}$) and the 3D foreshortened scale ($10.8\text{--}12.5\text{ mm}$ at $0.317\text{ mm/px}$), with nominal best estimate $11.0 \pm 1.2\text{ mm}$ (or $9.1\text{--}12.5\text{ mm}$ full envelope).
   - Report both the standardized $z$-scores ($+12.06\,\sigma$, $+10.70\,\sigma$) and the distribution-free Cantelli bounds ($p < 0.007$, $p < 0.009$).
2. **Add the Plain-Spoken Colophon to `index.html`:**
   - Insert the plain-spoken authorship colophon block (using `border-left: 3px solid var(--accent-ochre);`) before the footer in `index.html`.
3. **Final Verification:**
   - Run `python3 reproduce_analysis.py` and confirm it exits with code `0` with all SHA-256 assertions and live pixel fits passing.
