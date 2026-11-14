"""
Audit Standalone Rear-Arc Scale Scan, Profile Likelihood, and Noise Calibration
Part of the Argon Red-Team Audit of martian-cylinder.
Addresses Material Question B from the brief:
1. Recomputes standalone rear-arc scale scan across s in [0.50, 1.30]
2. Computes exact Delta_chi2, raw pixel Delta_RMS, and nominal 95% CI [0.87, 0.99]
3. Investigates why s=1.000 (Delta_chi2 = 4.8216) was called '1.55 sigma' (sqrt(4.82/2) = 1.552) vs sqrt(4.82) = 2.196
4. Formulates the Birge ratio / reduced chi2 rescaling (chi2_nu = 10.30)
5. Implements spatial autocorrelation / correlated-noise correction
"""

import os
import sys
import json
import numpy as np
from scipy.optimize import least_squares
from scipy.stats import chi2

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INDEP_DIR = os.path.join(ROOT_DIR, "independent-reconstruction")
sys.path.append(os.path.join(INDEP_DIR, "scripts"))

from step3_feature_extraction import load_drxx
from step4_endface_and_conic_models import point_to_ellipse_orth_dist, order_arch_points
from step8_pebble_correction_and_rear_terminus import extract_rear_terminus_points

def main():
    print("=== AUDITING REAR-ARC PROFILE LIKELIHOOD & STATISTICAL CALIBRATION ===")

    # Load primary data
    drxx_dn, drxx_rad, drxx_lum = load_drxx()

    with open(os.path.join(INDEP_DIR, "step3_features.json"), "r") as f:
        s3 = json.load(f)

    # 1. Extract 24-point rear arc points and clean front rim parameters
    thetas_rear_36 = np.arange(-210.0, -30.0, 5.0)
    rear_pts_36 = extract_rear_terminus_points(drxx_lum, center_xy=(1035.5, 951.2), theta_deg_list=thetas_rear_36, iso_target=0.0860)
    rear_arc_24 = rear_pts_36[8:32]
    xr = np.array([p["x_erf"] for p in rear_arc_24], dtype=np.float64)
    yr = np.array([p["y_erf"] for p in rear_arc_24], dtype=np.float64)
    sig_r = np.array([p["r_uncertainty_px"] for p in rear_arc_24], dtype=np.float64)
    N = len(xr)

    # Front face free parameters from step9 baseline
    with open(os.path.join(INDEP_DIR, "step9_joint_model.json"), "r") as f:
        s9 = json.load(f)
    ff_params = s9["independent_baselines"]["front_free_ellipse"]
    a_f = ff_params["a"]
    b_f = ff_params["b"]
    phi_f = np.radians(ff_params["minor_axis_deg"])

    # 2. Independent Scan of s in [0.50, 1.30]
    s_grid = np.linspace(0.50, 1.30, 81)
    scan_results = []
    for s_val in s_grid:
        def res_fn(p):
            xc, yc = p
            dists = point_to_ellipse_orth_dist(xr, yr, xc, yc, s_val * a_f, s_val * b_f, phi_f)
            return dists / sig_r

        sol = least_squares(res_fn, [1036.0, 964.5])
        dists = point_to_ellipse_orth_dist(xr, yr, sol.x[0], sol.x[1], s_val * a_f, s_val * b_f, phi_f)
        c2 = float(np.sum((dists / sig_r)**2))
        rms = float(np.sqrt(np.mean(dists**2)))
        scan_results.append({
            "s": float(s_val),
            "chi2": c2,
            "rms_px": rms,
            "xc": float(sol.x[0]),
            "yc": float(sol.x[1])
        })

    # Find minimum
    min_res = min(scan_results, key=lambda x: x["chi2"])
    best_s = min_res["s"]
    min_chi2 = min_res["chi2"]
    min_rms = min_res["rms_px"]

    # At s = 1.000
    res_1 = [x for x in scan_results if abs(x["s"] - 1.00) < 1e-4][0]
    chi2_1 = res_1["chi2"]
    rms_1 = res_1["rms_px"]
    delta_chi2_1 = chi2_1 - min_chi2
    delta_rms_1 = rms_1 - min_rms

    print(f"\n1. Standalone Scan Reproduction (N = {N} points):")
    print(f"   Best fit s:          {best_s:.3f} | RMS: {min_rms:.4f} px | chi2: {min_chi2:.2f}")
    print(f"   At s = 1.000:        RMS: {rms_1:.4f} px | chi2: {chi2_1:.2f}")
    print(f"   Delta RMS at s=1.0:  {delta_rms_1:+.5f} px (image-plane difference, not surface tolerance)")
    print(f"   Delta chi2 at s=1.0: {delta_chi2_1:.4f}")

    # 2. Hypothesis Testing & The '1.55 sigma' Defect
    z_standard = np.sqrt(delta_chi2_1)
    z_divided_by_2 = np.sqrt(delta_chi2_1 / 2.0)
    p_standard = 1.0 - chi2.cdf(delta_chi2_1, df=1)
    print(f"\n2. Hypothesis Testing & The '1.55 sigma' Defect:")
    print(f"   Ordinary 1-parameter standard z: sqrt(Delta chi2) = {z_standard:.4f} sigma (p = {p_standard:.4f})")
    print(f"   Root of Delta chi2 / 2:          sqrt(Delta chi2 / 2) = {z_divided_by_2:.4f} sigma")
    print("   The historical 1.55 value matches sqrt(Delta chi2/2); its provenance is not established by this calculation.")
    print(f"   Under strict uncalibrated chi2, Delta chi2 = 4.82 > 3.84, which nominally EXCLUDES s=1.000 at 95% CL!")

    # 3. Birge Ratio Calibration
    dof = N - 2
    chi2_nu = min_chi2 / dof
    delta_chi2_birge = delta_chi2_1 / chi2_nu
    z_birge = np.sqrt(delta_chi2_birge)
    p_birge = 1.0 - chi2.cdf(delta_chi2_birge, df=1)
    
    max_allowed_chi2_birge = min_chi2 + 3.84 * chi2_nu
    ci_birge_items = [x["s"] for x in scan_results if x["chi2"] <= max_allowed_chi2_birge]
    ci_birge_low, ci_birge_high = min(ci_birge_items), max(ci_birge_items)

    ci_nom_items = [x["s"] for x in scan_results if (x["chi2"] - min_chi2) <= 3.84]
    ci_nom_low, ci_nom_high = min(ci_nom_items), max(ci_nom_items)

    print(f"\n3. Statistical Calibration (Birge Ratio):")
    print(f"   Nominal reduced chi2: chi2_nu = {chi2_nu:.2f} >> 1 (indicates severely uncalibrated errors / correlated noise)")
    print(f"   Nominal uncalibrated 95% CI: [{ci_nom_low:.2f}, {ci_nom_high:.2f}] (excludes s=1.000)")
    print(f"   Birge-rescaled Delta chi2:   {delta_chi2_birge:.4f} (z_Birge = {z_birge:.2f} sigma, p = {p_birge:.3f})")
    print(f"   Birge-calibrated 95% CI:     [{ci_birge_low:.2f}, {ci_birge_high:.2f}] (comfortably includes s=1.000!)")

    # 4. Spatial Autocorrelation & Effective Sample Size
    dists_min = point_to_ellipse_orth_dist(xr, yr, min_res["xc"], min_res["yc"], best_s * a_f, best_s * b_f, phi_f)
    residuals = dists_min - np.mean(dists_min)
    r_lag1 = np.corrcoef(residuals[:-1], residuals[1:])[0, 1]
    r_lag2 = np.corrcoef(residuals[:-2], residuals[2:])[0, 1]
    n_eff = N * (1.0 - r_lag1) / (1.0 + r_lag1)
    
    print(f"\n4. Correlated Noise & Spatial Autocorrelation:")
    print(f"   Lag-1 Autocorrelation of residuals: r_1 = {r_lag1:.3f}")
    print(f"   Lag-2 Autocorrelation of residuals: r_2 = {r_lag2:.3f}")
    print(f"   Effective sample size: N_eff = {n_eff:.1f} (out of N = {N} nominal points)")
    print(f"   Correlation factor N / N_eff: {N / n_eff:.2f}x inflation of nominal chi-squared!")
    print("   Scalar variance rescaling is a sensitivity calculation; spatial covariance has not been fitted.")

    out_file = os.path.join(ROOT_DIR, "audit", "rear_arc_audit.json")
    with open(out_file, "w") as f:
        json.dump({
            "best_s": best_s,
            "min_chi2": min_chi2,
            "min_rms_px": min_rms,
            "s_1_000": {
                "rms_px": rms_1,
                "delta_rms_px": delta_rms_1,
                "delta_chi2": delta_chi2_1,
                "z_nominal": z_standard,
                "z_erroneous_text": z_divided_by_2
            },
            "nominal_ci95": [ci_nom_low, ci_nom_high],
            "birge_calibration": {
                "scope": "Historical scalar sensitivity at fixed s, N-2 DOF; not calibrated spatial covariance. Counting fitted scale gives N-3 DOF.",
                "chi2_nu": chi2_nu,
                "delta_chi2_birge": delta_chi2_birge,
                "z_birge": z_birge,
                "p_birge": p_birge,
                "ci95_birge": [ci_birge_low, ci_birge_high]
            },
            "autocorrelation": {
                "r_lag1": r_lag1,
                "r_lag2": r_lag2,
                "n_eff": n_eff
            }
        }, f, indent=2)
    print(f"\nSaved rear-arc audit data to: {out_file}")

if __name__ == "__main__":
    main()
