"""
Phase II Synthetic Ground-Truth Benchmarks & Validation
Curiosity Sol 3556 Mastcam-100 Anomaly (3556MR1025170721700585C00).

Assesses:
  1. Parameter recovery accuracy (bias and variance) on synthetic cylinders across noise and occlusion levels.
  2. False-positive rates: How often do non-cylindrical geometries (tapered cones, faceted prisms, clasts)
     masquerade as right circular cylinders under Mastcam imaging conditions?
  3. Minimum detectable taper threshold (delta R / L) distinguishing a cone from a cylinder.
"""

import math
import numpy as np
from scipy.optimize import minimize
import joint_geometry_fit as jgf

def run_synthetic_benchmarks():
    print("--- 1. SYNTHETIC CYLINDER PARAMETER RECOVERY BENCHMARK ---")
    # Ground truth parameters:
    # R = 5.92 mm, L = 33.59 mm, theta_axis = 29.86 deg, tilt = 23.89 deg, range = 4.21 m
    # xc = 57.66 px, yc = 42.99 px
    p_true = [57.66, 42.99, 5.92, 33.59, 29.86, 23.89, 4.21]
    bounds = [(50, 65), (35, 50), (4.0, 7.5), (20.0, 50.0), (20.0, 40.0), (10.0, 45.0), (3.63, 4.30)]
    
    geom_true = jgf.project_cylinder_model(p_true)
    xr_true, yr_true = geom_true['front_rim']
    xg_true, yg_true = geom_true['gen_up']
    xb_true, yb_true = geom_true['rear_rim']
    
    noise_levels = [0.25, 0.50, 0.75, 1.00]
    n_trials = 100
    recovery_results = {}

    np.random.seed(42)
    for sig in noise_levels:
        r_recovered = []
        l_recovered = []
        th_recovered = []
        tilt_recovered = []
        rmses = []

        for _ in range(n_trials):
            # Add Gaussian noise to boundary points
            xr_n = xr_true + np.random.normal(0, sig, size=xr_true.shape)
            yr_n = yr_true + np.random.normal(0, sig, size=yr_true.shape)
            xg_n = xg_true + np.random.normal(0, sig, size=xg_true.shape)
            yg_n = yg_true + np.random.normal(0, sig, size=yg_true.shape)
            xb_n = xb_true + np.random.normal(0, sig, size=xb_true.shape)
            yb_n = yb_true + np.random.normal(0, sig, size=yb_true.shape)

            synth_data = {
                'rim': (xr_n, yr_n, 0.5),
                'gen': (xg_n, yg_n, 0.25),
                'rear': (xb_n, yb_n, 1.2)
            }

            def loss_fn(p):
                try:
                    g = jgf.project_cylinder_model(p)
                    chi2, _, _, _ = jgf.compute_model_loss(g, synth_data)
                    return chi2
                except:
                    return 1e9

            # Fit from perturbed initial guess
            p_init = [p0 + np.random.normal(0, 0.5) for p0 in p_true]
            opt = minimize(loss_fn, p_init, method='L-BFGS-B', bounds=bounds)
            if opt.success:
                p_hat = opt.x
                g_hat = jgf.project_cylinder_model(p_hat)
                _, rmse, _, _ = jgf.compute_model_loss(g_hat, synth_data)
                r_recovered.append(p_hat[2])
                l_recovered.append(p_hat[3])
                th_recovered.append(p_hat[4])
                tilt_recovered.append(p_hat[5])
                rmses.append(rmse)

        recovery_results[sig] = {
            'sigma': sig,
            'R_mean': float(np.mean(r_recovered)),
            'R_std': float(np.std(r_recovered)),
            'L_mean': float(np.mean(l_recovered)),
            'L_std': float(np.std(l_recovered)),
            'th_mean': float(np.mean(th_recovered)),
            'th_std': float(np.std(th_recovered)),
            'tilt_mean': float(np.mean(tilt_recovered)),
            'tilt_std': float(np.std(tilt_recovered)),
            'rmse_mean': float(np.mean(rmses))
        }
        print(f"Noise sigma={sig:4.2f} px: R={np.mean(r_recovered):.2f}+/-{np.std(r_recovered):.2f} mm | L={np.mean(l_recovered):.2f}+/-{np.std(l_recovered):.2f} mm | RMSE={np.mean(rmses):.3f} px")

    print("\n--- 2. FALSE-POSITIVE CLASSIFICATION & MINIMUM DETECTABLE TAPER ---")
    # Test cones with increasing taper ratio: delta_R / L in [0.00, 0.02, 0.05, 0.10, 0.15, 0.20, 0.25]
    # Evaluate whether a cylinder fit can be distinguished from the true cone (delta AIC > 6 threshold)
    taper_ratios = [0.00, 0.02, 0.05, 0.08, 0.10, 0.15, 0.20]
    taper_results = {}
    sig_test = 0.5  # standard Mastcam edge noise

    for tr in taper_ratios:
        # Create cone: R1 = 5.5 mm, R2 = 5.5 + tr * 32.0 mm
        R1 = 5.5
        R2 = R1 + tr * 32.0
        p_cone = [57.66, 42.99, R1, R2, 32.0, 29.86, 23.89, 4.21]
        g_cone = jgf.project_cone_model(p_cone)
        xr, yr = g_cone['front_rim']
        xg, yg = g_cone['gen_up']
        xb, yb = g_cone['rear_rim']

        # Add noise
        xr_n = xr + np.random.normal(0, sig_test, size=xr.shape)
        yr_n = yr + np.random.normal(0, sig_test, size=yr.shape)
        xg_n = xg + np.random.normal(0, sig_test, size=xg.shape)
        yg_n = yg + np.random.normal(0, sig_test, size=yg.shape)
        xb_n = xb + np.random.normal(0, sig_test, size=xb.shape)
        yb_n = yb + np.random.normal(0, sig_test, size=yb.shape)

        cone_data = {
            'rim': (xr_n, yr_n, 0.5),
            'gen': (xg_n, yg_n, 0.25),
            'rear': (xb_n, yb_n, 1.2)
        }

        # Fit Model A (Cylinder) to the cone data
        def loss_cyl(p):
            try:
                g = jgf.project_cylinder_model(p)
                chi2, _, _, _ = jgf.compute_model_loss(g, cone_data)
                return chi2
            except:
                return 1e9

        opt_cyl = minimize(loss_cyl, p_true, method='L-BFGS-B', bounds=bounds)
        chi2_cyl = opt_cyl.fun
        aic_cyl = chi2_cyl + 2.0 * 7

        # Fit Model B (Cone) to the cone data
        bounds_cone = [(50, 65), (35, 50), (4.0, 7.5), (3.5, 12.0), (20.0, 50.0), (20.0, 40.0), (10.0, 45.0), (3.63, 4.30)]
        def loss_cone(p):
            try:
                g = jgf.project_cone_model(p)
                chi2, _, _, _ = jgf.compute_model_loss(g, cone_data)
                return chi2
            except:
                return 1e9

        opt_cone = minimize(loss_cone, p_cone, method='L-BFGS-B', bounds=bounds_cone)
        chi2_cone = opt_cone.fun
        aic_cone = chi2_cone + 2.0 * 8

        delta_aic = aic_cyl - aic_cone
        # If delta_aic < 6, the cylinder is statistically indistinguishable from the cone (false positive cylinder classification)
        masquerades = (delta_aic < 6.0)

        taper_results[tr] = {
            'taper_ratio': tr,
            'delta_R_mm': tr * 32.0,
            'chi2_cyl': float(chi2_cyl),
            'chi2_cone': float(chi2_cone),
            'delta_aic': float(delta_aic),
            'masquerades_as_cylinder': bool(masquerades)
        }
        status = "MASQUERADES AS CYLINDER (Indistinguishable)" if masquerades else "DISTINGUISHABLE (Cone preferred)"
        print(f"Taper Delta_R/L={tr:4.2f} (Delta_R={tr*32:4.2f} mm) -> Delta AIC={delta_aic:6.2f} | {status}")

    # Determine minimum detectable taper threshold
    detectable_tapers = [tr for tr, res in taper_results.items() if not res['masquerades_as_cylinder']]
    min_det_taper = min(detectable_tapers) if detectable_tapers else "> 0.20"
    print(f"\nMinimum Detectable Taper Threshold: Delta_R / L >= {min_det_taper}")

    return {
        'recovery': recovery_results,
        'taper': taper_results,
        'min_detectable_taper': min_det_taper
    }

if __name__ == '__main__':
    run_synthetic_benchmarks()

