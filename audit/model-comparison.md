# Checked geometric model comparison

Reviewed 2026-11-12. M1 is the strict cylindrical baseline; M2/M3 allow a free dorsal offset. M4's numerical fit is reproducible but its proposed physical frustum fails the common-tangent constraint.

## Direct physical falsification of M4's formulation

In coordinates u along the body axis and v transverse to it, an end ellipse has u²/b² + v²/a² = 1. M4's upper line is v=-r-mu, where m=(1-s)r/L. A tangent requires r²=a²+m²b², obtained from the ellipse support function (or a zero discriminant after substituting the line). Homothetic rear ellipses centered at u=-L impose the same condition.

Stored M4 parameters: a=19.262717 px, b=15.434227 px, r=19.294848 px, L=44.143566 px, s=0.618699. Thus m=0.166665 and the required tangent intercept is 19.433711 px. The actual line intercept is smaller by 0.138863 px, so the line cuts the projected end ellipse rather than touching it. This falsifies the physical silhouette interpretation of the fitted M4 geometry. It is an algebraic consistency failure, not a calibrated statistical significance or a test of every possible 3D cone.

`audit_3d_projective_geometry.py` computes these values; the regression test independently evaluates the discriminant. No full camera-ray/occlusion-constrained cone optimization has been performed by that script.

## Reproduced image-plane fits

| Model | k | Total RMS px | Front | Rear | Dorsal | Nominal chi-square | Nominal BIC |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M1 | 6 | 0.3788 | 0.2376 | 0.4830 | 0.4217 | 2653.51 | 2680.17 |
| M2 | 7 | 0.3468 | 0.2314 | 0.3049 | 0.4851 | 1916.15 | 1947.25 |
| M3 | 7 | 0.3389 | 0.2422 | 0.3784 | 0.4054 | not evaluated here | not evaluated here |
| M4 | 8 | 0.2549 | 0.1930 | 0.2684 | 0.3096 | 1044.06 | 1079.60 |

M3 minimizes an unweighted objective; the others minimize station-weighted residuals. The nominal BIC favors M4 under the stated independent-error model, but does not cure its physical constraint violation. All nominal reduced chi-squares are large. The original model-specific Birge BIC ranking is withdrawn: chi-square/[chi-square/(N-k)] + k ln N = N-k+k ln N, independent of fit quality. No replacement calibrated model ranking is claimed.

## Rear arc

With the front shape and orientation fixed, the standalone scan minimizes at s=0.930. At s=1, delta chi-square=4.8216, nominal z=2.196 and the 95% grid interval [0.87,0.99] excludes 1. RMS changes from 0.184339 to 0.186291 px. Multiplying this difference by a pixel scale gives an equivalent image-plane distance, not a measured surface tolerance.

The historical scalar rescaling used 22 residual degrees of freedom at fixed s (24 points minus two translations), giving z=0.684 and interval [0.77,1.17]. If counting the fitted scale as well, 21 degrees of freedom gives a slightly different result. Neither calculation estimates spatial covariance or a true coverage-calibrated interval. Retain the nominal exclusion and the sensitivity result with their distinct assumptions.

The scan at s around 0.60 holds a different front shape/orientation than M4. Its large deviance is not a one-parameter likelihood-ratio rejection of the full M4 solution. Likewise, the 7.73 px center displacement describes parameter changes, not a requirement for an edge at the ellipse center.

Perspective convergence of about 0.461 degrees at an assumed 20-degree inclination is a conditional estimate, not a global bound over all inclinations. The approximately 35-degree observed opening is incompatible with opposite cylindrical generators at the considered inclinations; it does not by itself prove burial or exclude every cone.

The separate audit re-optimization uses different starting values: M4 scale differs from the stored fit by about 6.2e-6, while RMS differs by about 6.3e-7 px. These are close numerical solutions, not bit-identical independent optimizations. The full original pipeline replay is bit-identical. The audit bootstrap (500 resamples, fixed jitter direction) yields an orientation spread of 3.79 degrees, versus the historical 4.23 from a different procedure; neither is a calibrated spatial bootstrap.
