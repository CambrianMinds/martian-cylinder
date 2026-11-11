"""
Step 4: End-Face / Terminal Boundary Geometric Modeling, Model Selection (AICc/BIC),
and Partial-Arc Degeneracy Analysis
Independent Geometric Investigation - Curiosity Sol 3556 (3556MR1025170721700585C00)
"""

import os
import json
import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(OUT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def load_step3():
    with open(os.path.join(OUT_DIR, "step3_features.json"), "r") as f:
        return json.load(f)

def point_to_ellipse_orth_dist(xs, ys, xc, yc, a, b, phi_minor_rad):
    """
    Compute exact signed Euclidean orthogonal residuals from points (xs, ys) to an ellipse
    centered at (xc, yc) with semi-major axis `a`, semi-minor axis `b` (where minor axis is along
    angle `phi_minor_rad`, and major axis is along `phi_minor_rad + pi/2`).
    In local frame (u along minor axis, v along major axis):
      u(psi) = b * cos(psi)
      v(psi) = a * sin(psi)
    Uses vectorised Newton-Raphson refinement on eccentric angle psi for each point.
    """
    c = np.cos(phi_minor_rad)
    s = np.sin(phi_minor_rad)
    dx = xs - xc
    dy = ys - yc
    # Local coordinates: u along phi_minor, v perpendicular (+90 deg)
    u = dx * c + dy * s
    v = -dx * s + dy * c

    # Initial angle psi
    psi = np.arctan2(v / (a + 1e-12), u / (b + 1e-12))
    # 8 iterations of Newton-Raphson to minimize f(psi) = 0.5 * ((b cos psi - u)^2 + (a sin psi - v)^2)
    for _ in range(8):
        cp = np.cos(psi)
        sp = np.sin(psi)
        du = b * cp - u
        dv = a * sp - v
        f1 = -b * sp * du + a * cp * dv
        f2 = -b * cp * du + b * b * sp * sp - a * sp * dv + a * a * cp * cp
        step = f1 / (np.maximum(np.abs(f2), 1e-10) * np.where(f2 >= 0, 1.0, -1.0))
        psi -= np.clip(step, -0.5, 0.5)

    u_foot = b * np.cos(psi)
    v_foot = a * np.sin(psi)
    dist = np.sqrt((u - u_foot) ** 2 + (v - v_foot) ** 2)
    # Sign: positive if outside ellipse ((u/b)^2 + (v/a)^2 > 1), negative if inside
    radial_norm = (u / (b + 1e-12)) ** 2 + (v / (a + 1e-12)) ** 2
    sign = np.where(radial_norm >= 1.0, 1.0, -1.0)
    return sign * dist

def fit_circle_odr(xs, ys, sigmas):
    xc0, yc0 = np.mean(xs), np.mean(ys)
    r0 = np.mean(np.sqrt((xs - xc0) ** 2 + (ys - yc0) ** 2))
    def res_fn(p):
        xc, yc, r = p
        d = np.sqrt((xs - xc) ** 2 + (ys - yc) ** 2) - r
        return d / sigmas
    sol = least_squares(res_fn, [xc0, yc0, r0], method="lm")
    xc, yc, r = sol.x
    raw_res = np.sqrt((xs - xc) ** 2 + (ys - yc) ** 2) - r
    return {
        "params": {"xc": float(xc), "yc": float(yc), "R": float(r), "a": float(r), "b": float(r), "b_over_a": 1.0, "tilt_deg": 0.0},
        "k_params": 3,
        "residuals_px": raw_res,
        "sigma_px": sigmas
    }

def fit_ellipse_constrained_odr(xs, ys, sigmas, phi_minor_deg):
    phi_rad = np.radians(phi_minor_deg)
    xc0, yc0 = 1067.5, 984.5
    def res_fn(p):
        xc, yc, a, b = p
        d = point_to_ellipse_orth_dist(xs, ys, xc, yc, a, b, phi_rad)
        return d / sigmas
    bounds = ([1050.0, 965.0, 5.0, 3.0], [1088.0, 1005.0, 35.0, 35.0])
    sol = least_squares(res_fn, [xc0, yc0, 15.5, 13.0], bounds=bounds, max_nfev=2000)
    xc, yc, a, b = sol.x
    # Ensure b <= a for aspect ratio reporting, and record whether minor axis is along phi_minor_deg or +90 deg
    if b <= a:
        ba = float(b / a)
        eff_minor_deg = float(phi_minor_deg)
    else:
        ba = float(a / b)
        eff_minor_deg = float((phi_minor_deg + 90.0) % 180.0)
    raw_res = point_to_ellipse_orth_dist(xs, ys, xc, yc, a, b, phi_rad)
    tilt_deg = float(np.degrees(np.arccos(np.clip(ba, 0.0, 1.0))))
    return {
        "params": {
            "xc": float(xc), "yc": float(yc),
            "a_perp_axis": float(a), "b_along_axis": float(b),
            "semi_major": float(max(a, b)), "semi_minor": float(min(a, b)),
            "b_along_over_a_perp": float(b / a),
            "b_over_a": ba,
            "fixed_axis_deg": float(phi_minor_deg),
            "effective_minor_axis_deg": eff_minor_deg,
            "implied_circular_tilt_deg": tilt_deg
        },
        "k_params": 4,
        "residuals_px": raw_res,
        "sigma_px": sigmas
    }

def fit_ellipse_free_odr(xs, ys, sigmas, p_init=None):
    if p_init is not None:
        def res_fn(p):
            xc, yc, a, b, phi = p
            return point_to_ellipse_orth_dist(xs, ys, xc, yc, a, b, phi) / sigmas
        bounds = ([1050.0, 965.0, 5.0, 3.0, -np.pi], [1088.0, 1005.0, 35.0, 35.0, np.pi])
        best_sol = least_squares(res_fn, p_init, bounds=bounds, max_nfev=400)
    else:
        best_cost = 1e18
        best_sol = None
        for phi_init_deg in np.linspace(0.0, 160.0, 9):
            phi0 = np.radians(phi_init_deg)
            def res_fn(p):
                xc, yc, a, b, phi = p
                return point_to_ellipse_orth_dist(xs, ys, xc, yc, a, b, phi) / sigmas
            bounds = ([1050.0, 965.0, 5.0, 3.0, -np.pi], [1088.0, 1005.0, 35.0, 35.0, np.pi])
            sol = least_squares(res_fn, [1067.5, 984.5, 16.0, 13.5, phi0], bounds=bounds, max_nfev=800)
            if sol.cost < best_cost:
                best_cost = sol.cost
                best_sol = sol

    xc, yc, a, b, phi = best_sol.x
    raw_res = point_to_ellipse_orth_dist(xs, ys, xc, yc, a, b, phi)
    if b <= a:
        semi_major, semi_minor = float(a), float(b)
        minor_deg = float(np.degrees(phi) % 180.0)
    else:
        semi_major, semi_minor = float(b), float(a)
        minor_deg = float((np.degrees(phi) + 90.0) % 180.0)
    # Put minor_deg in [-90, 90] for easy comparison with dorsal (~30 deg) and bisector (~47.6 deg)
    if minor_deg > 90.0:
        minor_deg -= 180.0
    ba = semi_minor / semi_major
    tilt_deg = float(np.degrees(np.arccos(np.clip(ba, 0.0, 1.0))))
    return {
        "params": {
            "xc": float(xc), "yc": float(yc),
            "semi_major": semi_major, "semi_minor": semi_minor,
            "b_over_a": float(ba),
            "minor_axis_deg": float(minor_deg),
            "major_axis_deg": float(minor_deg + 90.0),
            "implied_circular_tilt_deg": tilt_deg
        },
        "k_params": 5,
        "residuals_px": raw_res,
        "sigma_px": sigmas
    }

def point_to_parabola_orth_dist(xs, ys, xv, yv, c2, phi_rad):
    """
    Orthogonal distance from points (xs, ys) to parabola u = c2 * v^2
    with vertex (xv, yv) and symmetry axis along angle phi_rad.
    """
    c = np.cos(phi_rad)
    s = np.sin(phi_rad)
    dx = xs - xv
    dy = ys - yv
    u = dx * c + dy * s
    v = -dx * s + dy * c

    # Minimize 0.5 * ((c2 * t^2 - u)^2 + (t - v)^2) over t using Newton-Raphson
    t = v.copy()
    for _ in range(10):
        du = c2 * t * t - u
        f1 = 2.0 * c2 * t * du + (t - v)
        f2 = 2.0 * c2 * du + 4.0 * (c2 * t) ** 2 + 1.0
        t -= np.clip(f1 / np.maximum(f2, 1e-10), -2.0, 2.0)
    u_foot = c2 * t * t
    v_foot = t
    dist = np.sqrt((u - u_foot) ** 2 + (v - v_foot) ** 2)
    sign = np.where(u >= c2 * v * v, 1.0, -1.0)
    return sign * dist

def fit_parabola_odr(xs, ys, sigmas):
    phi0 = np.radians(45.0)
    def res_fn(p):
        xv, yv, c2, phi = p
        return point_to_parabola_orth_dist(xs, ys, xv, yv, c2, phi) / sigmas
    bounds = ([1045.0, 960.0, 0.005, -np.pi], [1080.0, 995.0, 0.25, np.pi])
    sol = least_squares(res_fn, [1057.0, 974.0, 0.045, phi0], bounds=bounds, max_nfev=2000)
    xv, yv, c2, phi = sol.x
    raw_res = point_to_parabola_orth_dist(xs, ys, xv, yv, c2, phi)
    axis_deg = float(np.degrees(phi) % 180.0)
    if axis_deg > 90.0:
        axis_deg -= 180.0
    return {
        "params": {
            "vertex_x": float(xv), "vertex_y": float(yv),
            "curvature_c2_px_inv": float(c2),
            "vertex_radius_of_curvature_px": float(1.0 / (2.0 * c2)),
            "axis_angle_deg": axis_deg
        },
        "k_params": 4,
        "residuals_px": raw_res,
        "sigma_px": sigmas
    }

def point_to_polyline_dist(xs, ys, verts_xy):
    """Exact Euclidean distance from points (xs, ys) to a piecewise linear chain of vertices."""
    verts = np.asarray(verts_xy, dtype=float).reshape((-1, 2))
    min_d = np.full_like(xs, 1e9, dtype=float)
    signed_d = np.zeros_like(xs, dtype=float)
    for i in range(len(verts) - 1):
        p0, p1 = verts[i], verts[i + 1]
        seg = p1 - p0
        seg_len2 = np.dot(seg, seg) + 1e-12
        t = np.clip(((xs - p0[0]) * seg[0] + (ys - p0[1]) * seg[1]) / seg_len2, 0.0, 1.0)
        proj_x = p0[0] + t * seg[0]
        proj_y = p0[1] + t * seg[1]
        d = np.sqrt((xs - proj_x) ** 2 + (ys - proj_y) ** 2)
        cross = (xs - p0[0]) * seg[1] - (ys - p0[1]) * seg[0]
        sgn = np.where(cross >= 0, 1.0, -1.0)
        mask = d < min_d
        min_d[mask] = d[mask]
        signed_d[mask] = sgn[mask] * d[mask]
    return signed_d

def fit_polygonal_facets_odr(xs, ys, sigmas, n_segments=2):
    # Initialize vertices evenly along the ordered point sequence
    idx_init = np.linspace(0, len(xs) - 1, n_segments + 1).astype(int)
    p0 = np.column_stack([xs[idx_init], ys[idx_init]]).ravel()
    def res_fn(p):
        return point_to_polyline_dist(xs, ys, p) / sigmas
    sol = least_squares(res_fn, p0, max_nfev=3000)
    raw_res = point_to_polyline_dist(xs, ys, sol.x)
    verts = sol.x.reshape((-1, 2)).tolist()
    # Number of effective shape parameters: (n_segments + 1) vertices -> 2*n_segments + 2 minus 2 endpoint tangent DOFs = 2*n_segments
    k_eff = 2 * n_segments
    return {
        "params": {"vertices_xy": verts, "n_segments": n_segments},
        "k_params": k_eff,
        "residuals_px": raw_res,
        "sigma_px": sigmas
    }

def compute_fit_metrics(fit_result):
    res = np.asarray(fit_result["residuals_px"], dtype=float)
    sig = np.asarray(fit_result["sigma_px"], dtype=float)
    n = len(res)
    k = fit_result["k_params"]
    dof = max(n - k, 1)
    rms_px = float(np.sqrt(np.mean(res ** 2)))
    max_px = float(np.max(np.abs(res)))
    # Use a realistic floor on total edge localization uncertainty (combining statistical fit error + 0.12 px pixelation/demosaicing floor)
    sig_eff = np.sqrt(sig ** 2 + 0.12 ** 2)
    chi2 = float(np.sum((res / sig_eff) ** 2))
    red_chi2 = float(chi2 / dof)
    aic = float(chi2 + 2.0 * k)
    aicc = float(aic + (2.0 * k * (k + 1.0)) / max(n - k - 1.0, 1.0))
    bic = float(chi2 + k * np.log(n))
    return {
        "n_points": n,
        "k_params": k,
        "dof": dof,
        "rms_residual_px": round(rms_px, 4),
        "max_residual_px": round(max_px, 4),
        "chi2": round(chi2, 3),
        "reduced_chi2": round(red_chi2, 4),
        "AIC": round(aic, 3),
        "AICc": round(aicc, 3),
        "BIC": round(bic, 3),
        "params": fit_result["params"]
    }

def order_arch_points(pts):
    """Order points continuously clockwise from bottom-left (+150 deg -> +180 -> -180 -> -50 deg)."""
    def sort_key(p):
        th = p["theta_deg"]
        # Map [140, 180] to [-220, -180] so it sorts continuously before [-180, +140]
        return th - 360.0 if th >= 135.0 else th
    return sorted(pts, key=sort_key)

def main():
    s3 = load_step3()
    arch_pts = order_arch_points(s3["arch_radial_points"])
    bisector_deg = s3["longitudinal_edges_drxx"]["bisector_angle_full_erf_deg"]
    dorsal_deg = s3["longitudinal_edges_drxx"]["dorsal_erf"]["theta_deg"]

    # Define the 4 boundary subsets
    subsets = {
        "S1_Strict_Proximal_Arch_140deg": [
            p for p in arch_pts if (p["theta_deg"] >= 160.0 or p["theta_deg"] <= -60.0)
        ],
        "S2_Full_Proximal_Rim_160deg": [
            p for p in arch_pts if (p["theta_deg"] >= 150.0 or p["theta_deg"] <= -50.0)
        ],
        "S3_Lobe_Excluded_250deg": [
            p for p in arch_pts if not (-30.0 <= p["theta_deg"] <= 75.0)
        ],
        "S4_Full_360deg_Dark_Patch": arch_pts
    }

    all_subset_results = {}
    raw_fits_for_plotting = {}

    for sub_name, pts in subsets.items():
        xs = np.array([p["x_erf"] for p in pts])
        ys = np.array([p["y_erf"] for p in pts])
        sigs = np.array([p["r_uncertainty_px"] for p in pts])

        m_circle = fit_circle_odr(xs, ys, sigs)
        m_el_bis = fit_ellipse_constrained_odr(xs, ys, sigs, bisector_deg)
        m_el_dor = fit_ellipse_constrained_odr(xs, ys, sigs, dorsal_deg)
        m_el_free = fit_ellipse_free_odr(xs, ys, sigs)

        sub_dict = {
            "M1_Circle_3DOF": compute_fit_metrics(m_circle),
            "M2_Ellipse_Bisector_Constrained_4DOF": compute_fit_metrics(m_el_bis),
            "M3_Ellipse_Dorsal_Constrained_4DOF": compute_fit_metrics(m_el_dor),
            "M4_Ellipse_Free_5DOF": compute_fit_metrics(m_el_free)
        }

        # For open arch subsets (S1, S2), also fit Parabolic Arch and 2-Segment / 3-Segment Polygonal Facets
        if "Proximal" in sub_name:
            m_parab = fit_parabola_odr(xs, ys, sigs)
            m_poly2 = fit_polygonal_facets_odr(xs, ys, sigs, n_segments=2)
            m_poly3 = fit_polygonal_facets_odr(xs, ys, sigs, n_segments=3)
            sub_dict["M5_Parabolic_Arch_4DOF"] = compute_fit_metrics(m_parab)
            sub_dict["M6a_Angular_2Facet_Rim_4DOF"] = compute_fit_metrics(m_poly2)
            sub_dict["M6b_Angular_3Facet_Rim_6DOF"] = compute_fit_metrics(m_poly3)
            raw_fits_for_plotting[sub_name] = {
                "xs": xs, "ys": ys,
                "circle": m_circle, "el_bis": m_el_bis, "el_dor": m_el_dor,
                "el_free": m_el_free, "parab": m_parab, "poly2": m_poly2, "poly3": m_poly3
            }
        else:
            raw_fits_for_plotting[sub_name] = {
                "xs": xs, "ys": ys,
                "circle": m_circle, "el_bis": m_el_bis, "el_dor": m_el_dor, "el_free": m_el_free
            }

        all_subset_results[sub_name] = sub_dict

    # Bootstrap uncertainty & partial-arc profile sensitivity on S2 (Full Proximal Rim) and S3 (Lobe-Excluded)
    rng = np.random.default_rng(12345)
    boot_results = {}
    for sub_key in ["S2_Full_Proximal_Rim_160deg", "S3_Lobe_Excluded_250deg", "S4_Full_360deg_Dark_Patch"]:
        pts = subsets[sub_key]
        xs = np.array([p["x_erf"] for p in pts])
        ys = np.array([p["y_erf"] for p in pts])
        sigs = np.array([p["r_uncertainty_px"] for p in pts])
        n = len(xs)
        b_ba, b_tilt, b_minor, b_a, b_b = [], [], [], [], []
        base_p = all_subset_results[sub_key]["M4_Ellipse_Free_5DOF"]["params"]
        p0_boot = [base_p["xc"], base_p["yc"], base_p["semi_major"], base_p["semi_minor"], np.radians(base_p["minor_axis_deg"])]
        for _ in range(200):
            idx = rng.integers(0, n, size=n)
            bx = xs[idx] + rng.normal(0, 0.12, size=n)
            by = ys[idx] + rng.normal(0, 0.12, size=n)
            f_res = fit_ellipse_free_odr(bx, by, sigs[idx], p_init=p0_boot)["params"]
            b_ba.append(f_res["b_over_a"])
            b_tilt.append(f_res["implied_circular_tilt_deg"])
            b_minor.append(f_res["minor_axis_deg"])
            b_a.append(f_res["semi_major"])
            b_b.append(f_res["semi_minor"])
        boot_results[sub_key] = {
            "b_over_a_mean": float(np.mean(b_ba)),
            "b_over_a_std": float(np.std(b_ba)),
            "b_over_a_ci95": [float(np.percentile(b_ba, 2.5)), float(np.percentile(b_ba, 97.5))],
            "tilt_deg_mean": float(np.mean(b_tilt)),
            "tilt_deg_std": float(np.std(b_tilt)),
            "tilt_deg_ci95": [float(np.percentile(b_tilt, 2.5)), float(np.percentile(b_tilt, 97.5))],
            "minor_axis_deg_mean": float(np.mean(b_minor)),
            "minor_axis_deg_std": float(np.std(b_minor)),
            "semi_major_px_mean": float(np.mean(b_a)),
            "semi_major_px_std": float(np.std(b_a)),
            "semi_minor_px_mean": float(np.mean(b_b)),
            "semi_minor_px_std": float(np.std(b_b))
        }

    # Profile RMS map across fixed aspect ratio (b/a in [0.45, 1.0]) on S2_Full_Proximal_Rim_160deg
    # to test how strongly a 160-deg arc constrains b/a when center (xc, yc) is free vs constrained!
    pts_s2 = subsets["S2_Full_Proximal_Rim_160deg"]
    xs_s2 = np.array([p["x_erf"] for p in pts_s2])
    ys_s2 = np.array([p["y_erf"] for p in pts_s2])
    sigs_s2 = np.array([p["r_uncertainty_px"] for p in pts_s2])
    ba_grid = np.linspace(0.50, 1.00, 21)
    profile_ba_bisector = []
    profile_ba_dorsal = []
    for ba_val in ba_grid:
        # Fix phi_minor = bisector_deg and b = ba_val * a; optimize xc, yc, a
        phi_b = np.radians(bisector_deg)
        def res_b(p):
            xc, yc, a = p
            return point_to_ellipse_orth_dist(xs_s2, ys_s2, xc, yc, a, ba_val * a, phi_b)
        sol_b = least_squares(res_b, [1067.5, 984.5, 15.5], bounds=([1052, 968, 8.0], [1085, 1002, 28.0]))
        rms_b = float(np.sqrt(np.mean(sol_b.fun ** 2)))
        profile_ba_bisector.append({"b_over_a": float(ba_val), "rms_px": round(rms_b, 4), "xc": float(sol_b.x[0]), "yc": float(sol_b.x[1]), "a_px": float(sol_b.x[2])})

        phi_d = np.radians(dorsal_deg)
        def res_d(p):
            xc, yc, a = p
            return point_to_ellipse_orth_dist(xs_s2, ys_s2, xc, yc, a, ba_val * a, phi_d)
        sol_d = least_squares(res_d, [1067.5, 984.5, 15.5], bounds=([1052, 968, 8.0], [1085, 1002, 28.0]))
        rms_d = float(np.sqrt(np.mean(sol_d.fun ** 2)))
        profile_ba_dorsal.append({"b_over_a": float(ba_val), "rms_px": round(rms_d, 4), "xc": float(sol_d.x[0]), "yc": float(sol_d.x[1]), "a_px": float(sol_d.x[2])})

    out_json = {
        "subset_model_comparisons": all_subset_results,
        "bootstrap_uncertainties": boot_results,
        "partial_arc_ba_profile_S2": {
            "bisector_aligned": profile_ba_bisector,
            "dorsal_aligned": profile_ba_dorsal
        }
    }
    with open(os.path.join(OUT_DIR, "step4_endface_models.json"), "w") as f:
        json.dump(out_json, f, indent=2)

    # Generate Diagnostic Figure 4: End-Face Conic & Alternative Model Fits + Partial-Arc Degeneracy
    from step3_feature_extraction import load_drxx
    _, _, drxx_lum = load_drxx()

    fig, axes = plt.subplots(2, 2, figsize=(16, 14), dpi=150)
    tx0, tx1, ty0, ty1 = 1042, 1098, 960, 1008
    axes[0, 0].imshow(drxx_lum[ty0:ty1, tx0:tx1], extent=[tx0 - 0.5, tx1 - 0.5, ty1 - 0.5, ty0 - 0.5], cmap="gray", interpolation="nearest")

    # Overlay fitted ellipses across S2, S3, S4
    psi_plot = np.linspace(0, 2 * np.pi, 200)
    colors_sub = {
        "S2_Full_Proximal_Rim_160deg": ("lime", "S2 Free Ellipse (160° Proximal Rim)"),
        "S3_Lobe_Excluded_250deg": ("cyan", "S3 Free Ellipse (250° Lobe-Excluded)"),
        "S4_Full_360deg_Dark_Patch": ("orange", "S4 Free Ellipse (360° Full Dark Patch)")
    }
    for skey, (col, lbl) in colors_sub.items():
        fp = all_subset_results[skey]["M4_Ellipse_Free_5DOF"]["params"]
        xc, yc, a, b, mdeg = fp["xc"], fp["yc"], fp["semi_major"], fp["semi_minor"], fp["minor_axis_deg"]
        ph = np.radians(mdeg)
        u_p = b * np.cos(psi_plot)
        v_p = a * np.sin(psi_plot)
        xp = xc + u_p * np.cos(ph) - v_p * np.sin(ph)
        yp = yc + u_p * np.sin(ph) + v_p * np.cos(ph)
        axes[0, 0].plot(xp, yp, color=col, linewidth=1.8, label=f"{lbl}: b/a={fp['b_over_a']:.2f}, minor={mdeg:.1f}°")
        axes[0, 0].plot(xc, yc, marker="+", color=col, markersize=8)

    # Also plot S2 Circle
    cp_s2 = all_subset_results["S2_Full_Proximal_Rim_160deg"]["M1_Circle_3DOF"]["params"]
    axes[0, 0].plot(
        cp_s2["xc"] + cp_s2["R"] * np.cos(psi_plot),
        cp_s2["yc"] + cp_s2["R"] * np.sin(psi_plot),
        "w--", linewidth=1.2, label=f"S2 Circle: R={cp_s2['R']:.2f} px"
    )
    axes[0, 0].plot(xs_s2, ys_s2, "go", markersize=4, label="S2 Proximal Rim Points")
    axes[0, 0].set_xlim(tx0, tx1)
    axes[0, 0].set_ylim(ty1, ty0)
    axes[0, 0].set_title("End-Face Ellipse Sensitivity to Boundary Arc Selection")
    axes[0, 0].set_xlabel("Sample x (px)")
    axes[0, 0].set_ylabel("Line y (px)")
    axes[0, 0].legend(loc="lower left", fontsize=8)
    axes[0, 0].grid(True, alpha=0.25)

    # Panel 2: Compare Curved Models vs Angular Polygonal Facets on S2 Proximal Rim
    axes[0, 1].imshow(drxx_lum[ty0:ty1, tx0:tx1], extent=[tx0 - 0.5, tx1 - 0.5, ty1 - 0.5, ty0 - 0.5], cmap="gray", interpolation="nearest")
    axes[0, 1].plot(xs_s2, ys_s2, "go", markersize=4, label="S2 Proximal Rim Points (N=33)")
    # Plot Parabolic Arch
    par_p = all_subset_results["S2_Full_Proximal_Rim_160deg"]["M5_Parabolic_Arch_4DOF"]["params"]
    v_grid = np.linspace(-18, 18, 120)
    u_grid = par_p["curvature_c2_px_inv"] * (v_grid ** 2)
    ph_par = np.radians(par_p["axis_angle_deg"])
    x_par = par_p["vertex_x"] + u_grid * np.cos(ph_par) - v_grid * np.sin(ph_par)
    y_par = par_p["vertex_y"] + u_grid * np.sin(ph_par) + v_grid * np.cos(ph_par)
    axes[0, 1].plot(x_par, y_par, "c-", linewidth=2.0, label=f"Parabolic Arch (RMS={all_subset_results['S2_Full_Proximal_Rim_160deg']['M5_Parabolic_Arch_4DOF']['rms_residual_px']:.3f} px)")

    # Plot 2-facet and 3-facet polygons
    v2 = np.array(all_subset_results["S2_Full_Proximal_Rim_160deg"]["M6a_Angular_2Facet_Rim_4DOF"]["params"]["vertices_xy"])
    v3 = np.array(all_subset_results["S2_Full_Proximal_Rim_160deg"]["M6b_Angular_3Facet_Rim_6DOF"]["params"]["vertices_xy"])
    axes[0, 1].plot(v2[:, 0], v2[:, 1], "r--o", linewidth=1.8, label=f"2-Facet Angular Rim (RMS={all_subset_results['S2_Full_Proximal_Rim_160deg']['M6a_Angular_2Facet_Rim_4DOF']['rms_residual_px']:.3f} px)")
    axes[0, 1].plot(v3[:, 0], v3[:, 1], "m-.s", linewidth=1.8, label=f"3-Facet Angular Rim (RMS={all_subset_results['S2_Full_Proximal_Rim_160deg']['M6b_Angular_3Facet_Rim_6DOF']['rms_residual_px']:.3f} px)")
    axes[0, 1].set_xlim(tx0, tx1)
    axes[0, 1].set_ylim(ty1, ty0)
    axes[0, 1].set_title("Smooth Conic Arch vs Angular Fracture Facets (S2 Rim)")
    axes[0, 1].set_xlabel("Sample x (px)")
    axes[0, 1].set_ylabel("Line y (px)")
    axes[0, 1].legend(loc="lower left", fontsize=8)
    axes[0, 1].grid(True, alpha=0.25)

    # Panel 3: Orthogonal Residual Profiles along the S2 Rim for all competing models
    rf_s2 = raw_fits_for_plotting["S2_Full_Proximal_Rim_160deg"]
    idx_seq = np.arange(len(xs_s2))
    axes[1, 0].axhline(0, color="black", linestyle="--", alpha=0.5)
    axes[1, 0].plot(idx_seq, rf_s2["el_free"]["residuals_px"], "g-o", markersize=3, label="Free Ellipse (5 DOF)")
    axes[1, 0].plot(idx_seq, rf_s2["circle"]["residuals_px"], "b--s", markersize=3, label="Circle (3 DOF)")
    axes[1, 0].plot(idx_seq, rf_s2["parab"]["residuals_px"], "c-^", markersize=3, label="Parabola (4 DOF)")
    axes[1, 0].plot(idx_seq, rf_s2["poly2"]["residuals_px"], "r:x", markersize=4, label="2-Facet Angular (4 DOF)")
    axes[1, 0].plot(idx_seq, rf_s2["poly3"]["residuals_px"], "m-.d", markersize=3, label="3-Facet Angular (6 DOF)")
    axes[1, 0].set_title("Point-by-Point Orthogonal Residuals Along Proximal Arch (S2)")
    axes[1, 0].set_xlabel("Ordered Station Index Along Arch (Bottom-Left to Top-Right)")
    axes[1, 0].set_ylabel("Orthogonal Residual d_perp (px)")
    axes[1, 0].legend(fontsize=8)
    axes[1, 0].grid(True, alpha=0.3)

    # Panel 4: Partial-Arc Aspect Ratio Degeneracy Curve (RMS vs b/a on 160-deg Proximal Rim)
    axes[1, 1].plot(
        [d["b_over_a"] for d in profile_ba_bisector],
        [d["rms_px"] for d in profile_ba_bisector],
        "b-o", label=f"Minor Axis Fixed to Bisector ({bisector_deg:.1f}°)"
    )
    axes[1, 1].plot(
        [d["b_over_a"] for d in profile_ba_dorsal],
        [d["rms_px"] for d in profile_ba_dorsal],
        "r-s", label=f"Minor Axis Fixed to Dorsal Limb ({dorsal_deg:.1f}°)"
    )
    axes[1, 1].axhline(
        all_subset_results["S2_Full_Proximal_Rim_160deg"]["M4_Ellipse_Free_5DOF"]["rms_residual_px"],
        color="green", linestyle="--", label="Unconstrained 5-DOF Free Ellipse Minimum"
    )
    axes[1, 1].set_title("Partial-Arc (160°) Curvature-Center Tradeoff: Orthogonal RMS vs b/a")
    axes[1, 1].set_xlabel("Forced Ellipse Aspect Ratio (b / a = cos(tilt))")
    axes[1, 1].set_ylabel("Minimum Orthogonal RMS Residual on S2 Arch (px)")
    axes[1, 1].legend(fontsize=8)
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "diag04_endface_models.png"))
    plt.close()

    print("Step 4 Model Comparison Summary:")
    print(json.dumps(all_subset_results, indent=2))
    print("Bootstrap Uncertainties:")
    print(json.dumps(boot_results, indent=2))

if __name__ == "__main__":
    main()
