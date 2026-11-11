"""
Step 3: Reproducible Subpixel Feature Extraction, Radiometric & Noise Characterization,
and Boundary Ambiguity Analysis
Independent Geometric Investigation - Curiosity Sol 3556 (3556MR1025170721700585C00)
"""

import os
import json
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates
from scipy.optimize import curve_fit
from scipy.special import erf
import matplotlib.pyplot as plt

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(OUT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)
DATA_DIR = os.path.abspath(os.path.join(OUT_DIR, "..", "data"))

RAD_SCALE = np.array([1.201e-04, 1.112e-04, 1.037e-04])

def load_drxx():
    path = os.path.join(DATA_DIR, "3556MR1025170721700585C00_DRXX.IMG")
    raw = np.fromfile(path, dtype=">u2").reshape((3, 1184, 1328))
    arr = np.transpose(raw, (1, 2, 0)).astype(np.float64)
    rad = arr * RAD_SCALE[None, None, :]
    lum = rad.mean(axis=2)
    return arr, rad, lum

def load_drlx():
    path = os.path.join(DATA_DIR, "3556MR1025170721700585C00_DRLX.IMG")
    raw = np.fromfile(path, dtype=">u2").reshape((3, 1180, 1323))
    arr = np.transpose(raw, (1, 2, 0)).astype(np.float64)
    rad = arr * RAD_SCALE[None, None, :]
    lum = rad.mean(axis=2)
    return arr, rad, lum

def erf_edge_model(s, I_low, I_high, s0, sigma):
    return I_low + 0.5 * (I_high - I_low) * (1.0 + erf((s - s0) / (np.sqrt(2.0) * sigma)))

def extract_subpixel_profile_edges(
    img_2d, p_start, p_end, n_stations=26, half_width=3.5, n_samples=71, grad_sign=1
):
    """
    Sample 1D profiles perpendicular to a baseline segment from p_start to p_end.
    `n_hat = [-t_hat[1], t_hat[0]]` points LEFT/DOWN for a downward-right segment in image coordinates (y increases downward).
      - Dorsal (upper) outer edge: +n moves from DARK background into BRIGHT object -> grad_sign = +1.
      - Ventral (lower-left) edge: +n moves from BRIGHT object into DARK soil -> grad_sign = -1.
    Select the contrast transition of the physical object, not an oppositely signed interior edge.
    At each station, compute both:
      1) Directional Gaussian-smoothed parabolic gradient extremum (non-parametric subpixel edge)
      2) Local Error Function (erf) edge model fit around the directional gradient peak
    """
    if grad_sign not in (-1, 1):
        raise ValueError('grad_sign must be +1 (dark to bright) or -1 (bright to dark) along +n')
    p_start = np.array(p_start, dtype=float)
    p_end = np.array(p_end, dtype=float)
    t_vec = p_end - p_start
    length = np.linalg.norm(t_vec)
    t_hat = t_vec / length
    n_hat = np.array([-t_hat[1], t_hat[0]])

    s_grid = np.linspace(-half_width, half_width, n_samples)
    ds = s_grid[1] - s_grid[0]
    u_fracs = np.linspace(0.0, 1.0, n_stations)

    stations = []
    for idx, u in enumerate(u_fracs):
        base_pt = p_start + u * t_vec
        xs = base_pt[0] + s_grid * n_hat[0]
        ys = base_pt[1] + s_grid * n_hat[1]
        prof_lin = map_coordinates(img_2d, [ys, xs], order=1, mode="nearest")

        # Directional gradient peak (grad_sign * dI/ds)
        prof_smooth = gaussian_filter(prof_lin, sigma=0.65 / ds)
        grad = np.gradient(prof_smooth, ds) * grad_sign
        # Restrict peak search to central [-2.2, +2.2] px around baseline
        central_mask = np.abs(s_grid) <= 2.2
        central_indices = np.where(central_mask)[0]
        k_max = int(central_indices[np.argmax(grad[central_indices])])

        if 1 <= k_max < len(s_grid) - 1:
            g_m1, g_0, g_p1 = grad[k_max - 1], grad[k_max], grad[k_max + 1]
            denom = (g_m1 - 2.0 * g_0 + g_p1)
            offset = 0.5 * (g_m1 - g_p1) / denom if abs(denom) > 1e-12 else 0.0
            offset = np.clip(offset, -1.0, 1.0)
            s_grad = float(s_grid[k_max] + offset * ds)
        else:
            s_grad = float(s_grid[k_max])

        # Local window around s_grad for erf fit (+/- 2.2 px)
        loc_mask = np.abs(s_grid - s_grad) <= 2.2
        s_sub = s_grid[loc_mask]
        p_sub = prof_lin[loc_mask]
        p0 = [p_sub[0], p_sub[-1], s_grad, 0.8]
        bounds = (
            [min(p_sub) - 0.05, min(p_sub) - 0.05, s_grad - 1.2, 0.2],
            [max(p_sub) + 0.05, max(p_sub) + 0.05, s_grad + 1.2, 2.5]
        )
        try:
            popt, pcov = curve_fit(erf_edge_model, s_sub, p_sub, p0=p0, bounds=bounds, maxfev=2000)
            s_erf = float(popt[2])
            sigma_psf = float(popt[3])
            contrast = float(abs(popt[1] - popt[0]))
            s_err = float(np.sqrt(pcov[2, 2])) if pcov[2, 2] > 0 else 0.08
            fit_rms = float(np.sqrt(np.mean((p_sub - erf_edge_model(s_sub, *popt)) ** 2)))
            if abs(s_erf - s_grad) > 0.8:
                s_best = s_grad
            else:
                s_best = s_erf
        except Exception:
            s_best = s_grad
            sigma_psf = 0.8
            contrast = float(p_sub.max() - p_sub.min())
            s_err = 0.12
            fit_rms = 0.0

        pt_erf = base_pt + s_best * n_hat
        pt_grad = base_pt + s_grad * n_hat
        # A geometric edge is only useful if the observed brightness step has the
        # expected direction across the body/background interface.
        minus_intensity = float(np.interp(s_best - 1.0, s_grid, prof_lin))
        plus_intensity = float(np.interp(s_best + 1.0, s_grid, prof_lin))
        signed_step = float(grad_sign * (plus_intensity - minus_intensity))
        stations.append({
            'expected_grad_sign': int(grad_sign),
            'signed_physical_edge_step': signed_step,
            'edge_polarity_ok': bool(signed_step > 0.0),
            "station_idx": idx,
            "u_frac": float(u),
            "s_along_px": float(u * length),
            "x_erf": float(pt_erf[0]),
            "y_erf": float(pt_erf[1]),
            "x_grad": float(pt_grad[0]),
            "y_grad": float(pt_grad[1]),
            "s_offset_erf": s_best,
            "s_offset_grad": s_grad,
            "s_uncertainty_px": max(s_err, abs(s_best - s_grad) * 0.5, 0.04),
            "sigma_blur_px": sigma_psf,
            "contrast_rad": contrast,
            "profile_rms": fit_rms
        })
    return stations

def extract_radial_arch_points(img_2d, center_xy, theta_deg_list, r_min=6.0, r_max=25.0, n_samples=77):
    cx, cy = center_xy
    r_grid = np.linspace(r_min, r_max, n_samples)
    dr = r_grid[1] - r_grid[0]
    pts = []
    for th_deg in theta_deg_list:
        th = np.radians(th_deg)
        dx, dy = np.cos(th), np.sin(th)
        xs = cx + r_grid * dx
        ys = cy + r_grid * dy
        prof = map_coordinates(img_2d, [ys, xs], order=1, mode="nearest")
        prof_s = gaussian_filter(prof, sigma=0.7 / dr)
        grad = np.gradient(prof_s, dr)
        k_max = int(np.argmax(grad))
        if 1 <= k_max < len(r_grid) - 1:
            g_m1, g_0, g_p1 = grad[k_max - 1], grad[k_max], grad[k_max + 1]
            denom = (g_m1 - 2.0 * g_0 + g_p1)
            offset = 0.5 * (g_m1 - g_p1) / denom if abs(denom) > 1e-12 else 0.0
            offset = np.clip(offset, -1.0, 1.0)
            r_grad = float(r_grid[k_max] + offset * dr)
        else:
            r_grad = float(r_grid[k_max])

        mask = np.abs(r_grid - r_grad) <= 3.0
        r_sub = r_grid[mask]
        p_sub = prof[mask]
        p0 = [p_sub[0], p_sub[-1], r_grad, 0.9]
        bounds = (
            [min(p_sub) - 0.02, min(p_sub) - 0.02, r_grad - 1.5, 0.2],
            [max(p_sub) + 0.02, max(p_sub) + 0.02, r_grad + 1.5, 2.8]
        )
        try:
            popt, pcov = curve_fit(erf_edge_model, r_sub, p_sub, p0=p0, bounds=bounds, maxfev=2000)
            r_erf = float(popt[2])
            sigma_blur = float(popt[3])
            contrast = float(popt[1] - popt[0])
            r_err = float(np.sqrt(pcov[2, 2])) if pcov[2, 2] > 0 else 0.1
            if abs(r_erf - r_grad) > 1.0:
                r_best = r_grad
            else:
                r_best = r_erf
        except Exception:
            r_best = r_grad
            sigma_blur = 1.0
            contrast = float(p_sub.max() - p_sub.min())
            r_err = 0.15

        pts.append({
            "theta_deg": float(th_deg),
            "r_erf_px": r_best,
            "r_grad_px": r_grad,
            "x_erf": float(cx + r_best * dx),
            "y_erf": float(cy + r_best * dy),
            "x_grad": float(cx + r_grad * dx),
            "y_grad": float(cy + r_grad * dy),
            "r_uncertainty_px": max(r_err, abs(r_best - r_grad) * 0.5, 0.06),
            "sigma_blur_px": sigma_blur,
            "contrast_rad": contrast,
            "grad_peak": float(grad[k_max])
        })
    return pts

def fit_line_orthogonal(xs, ys, weights=None):
    xs = np.asarray(xs, dtype=float)
    ys = np.asarray(ys, dtype=float)
    if weights is None:
        w = np.ones_like(xs)
    else:
        w = np.asarray(weights, dtype=float)
    w = w / np.sum(w)
    xm = float(np.sum(w * xs))
    ym = float(np.sum(w * ys))
    dx = xs - xm
    dy = ys - ym
    cov = np.array([
        [np.sum(w * dx * dx), np.sum(w * dx * dy)],
        [np.sum(w * dx * dy), np.sum(w * dy * dy)]
    ])
    eigvals, eigvecs = np.linalg.eigh(cov)
    t_hat = eigvecs[:, 1]
    if t_hat[0] < 0:
        t_hat = -t_hat
    n_hat = np.array([-t_hat[1], t_hat[0]])
    u = dx * t_hat[0] + dy * t_hat[1]
    v = dx * n_hat[0] + dy * n_hat[1]
    rms_orth = float(np.sqrt(np.mean(v ** 2)))
    max_orth = float(np.max(np.abs(v)))
    span_u = float(u.max() - u.min())

    poly_coeffs, poly_cov = np.polyfit(u, v, 2, cov=True)
    c2 = float(poly_coeffs[0])
    c2_err = float(np.sqrt(poly_cov[0, 0]))
    kappa_inv_px = float(1.0 / abs(2.0 * c2)) if abs(c2) > 1e-12 else 1e9
    sagitta_px = float(abs(c2) * (span_u / 2.0) ** 2)
    rms_quad = float(np.sqrt(np.mean((v - np.polyval(poly_coeffs, u)) ** 2)))

    rng = np.random.default_rng(42)
    boot_thetas = []
    n = len(xs)
    for _ in range(1000):
        idx = rng.integers(0, n, size=n)
        bx, by = xs[idx], ys[idx]
        bxm, bym = bx.mean(), by.mean()
        bcov = np.cov(bx - bxm, by - bym)
        _, bvecs = np.linalg.eigh(bcov)
        bt = bvecs[:, 1]
        if bt[0] < 0:
            bt = -bt
        boot_thetas.append(np.degrees(np.arctan2(bt[1], bt[0])))
    theta_deg = float(np.degrees(np.arctan2(t_hat[1], t_hat[0])))
    theta_std_deg = float(np.std(boot_thetas))

    return {
        "centroid_xy": [xm, ym],
        "t_hat": t_hat.tolist(),
        "n_hat": n_hat.tolist(),
        "theta_deg": theta_deg,
        "theta_uncertainty_deg": theta_std_deg,
        "span_px": span_u,
        "rms_orthogonal_residual_px": rms_orth,
        "max_orthogonal_residual_px": max_orth,
        "quadratic_c2_px_inv": c2,
        "quadratic_c2_err_px_inv": c2_err,
        "curvature_z_score": float(abs(c2) / (c2_err + 1e-15)),
        "radius_of_curvature_px": kappa_inv_px,
        "max_sagitta_deviation_px": sagitta_px,
        "rms_quadratic_residual_px": rms_quad,
        "u_coords": u.tolist(),
        "v_residuals": v.tolist()
    }

def main():
    drxx_dn, drxx_rad, drxx_lum = load_drxx()
    drlx_dn, drlx_rad, drlx_lum = load_drlx()

    # 1. Radiometric & Noise Characterization
    soil_patch = drxx_lum[925:942, 1000:1030]
    soil_smooth = gaussian_filter(soil_patch, sigma=1.5)
    soil_noise_std = float(np.std(soil_patch - soil_smooth))

    obj_bright_patch = drxx_lum[958:968, 1044:1054]
    obj_bright_mean = float(np.mean(obj_bright_patch))
    obj_bright_max = float(np.max(drxx_lum[950:985, 1032:1070]))

    shadow_core_patch = drxx_lum[976:994, 1060:1076]
    shadow_core_mean = float(np.mean(shadow_core_patch))
    shadow_core_min = float(np.min(shadow_core_patch))
    shadow_core_std = float(np.std(shadow_core_patch))
    shadow_dn_band = [float(np.mean(drxx_dn[976:994, 1060:1076, b])) for b in range(3)]
    bright_dn_band = [float(np.mean(drxx_dn[958:968, 1044:1054, b])) for b in range(3)]
    snr_edge = (obj_bright_mean - shadow_core_mean) / soil_noise_std

    # 2. Extract Longitudinal Boundaries in DRXX
    # Zone 1: Dorsal (Upper-Right) Edge: (1036.0, 947.2) to (1068.5, 963.6), grad_sign = -1
    dorsal_stations_drxx = extract_subpixel_profile_edges(
        drxx_lum, [1036.0, 947.2], [1068.5, 963.6], n_stations=26, half_width=3.5, grad_sign=+1
    )
    # Zone 2: Ventral (Lower-Left) Edge: (1033.2, 952.5) to (1051.2, 989.5), grad_sign = +1
    ventral_full_stations_drxx = extract_subpixel_profile_edges(
        drxx_lum, [1033.2, 952.5], [1051.2, 989.5], n_stations=26, half_width=3.5, grad_sign=-1
    )
    # Refuse a contour whose intensity transition contradicts the visible
    # bright-object/dark-background boundary for most stations.
    for name, points in [('dorsal', dorsal_stations_drxx), ('ventral', ventral_full_stations_drxx)]:
        fraction = np.mean([p['edge_polarity_ok'] for p in points])
        if fraction < 0.70:
            raise RuntimeError(f'{name} edge polarity failed: {fraction:.0%} of stations follow the expected physical transition')

    # Clean ventral subset excluding the pebble contact region y in [978.5, 986.5]
    ventral_clean_stations_drxx = [
        s for s in ventral_full_stations_drxx if not (978.5 <= s["y_erf"] <= 986.5)
    ]

    dorsal_fit_erf = fit_line_orthogonal(
        [s["x_erf"] for s in dorsal_stations_drxx],
        [s["y_erf"] for s in dorsal_stations_drxx]
    )
    dorsal_fit_grad = fit_line_orthogonal(
        [s["x_grad"] for s in dorsal_stations_drxx],
        [s["y_grad"] for s in dorsal_stations_drxx]
    )
    ventral_full_fit_erf = fit_line_orthogonal(
        [s["x_erf"] for s in ventral_full_stations_drxx],
        [s["y_erf"] for s in ventral_full_stations_drxx]
    )
    ventral_clean_fit_erf = fit_line_orthogonal(
        [s["x_erf"] for s in ventral_clean_stations_drxx],
        [s["y_erf"] for s in ventral_clean_stations_drxx]
    )
    ventral_full_fit_grad = fit_line_orthogonal(
        [s["x_grad"] for s in ventral_full_stations_drxx],
        [s["y_grad"] for s in ventral_full_stations_drxx]
    )

    # Multi-band (R, G, B) line fits on DRXX
    band_fits = {}
    for b_idx, b_name in enumerate(["Red_Band0", "Green_Band1", "Blue_Band2"]):
        b_img = drxx_rad[:, :, b_idx]
        d_st = extract_subpixel_profile_edges(b_img, [1036.0, 947.2], [1068.5, 963.6], n_stations=26, grad_sign=+1)
        v_st = extract_subpixel_profile_edges(b_img, [1033.2, 952.5], [1051.2, 989.5], n_stations=26, grad_sign=-1)
        df = fit_line_orthogonal([s["x_erf"] for s in d_st], [s["y_erf"] for s in d_st])
        vf = fit_line_orthogonal([s["x_erf"] for s in v_st], [s["y_erf"] for s in v_st])
        band_fits[b_name] = {
            "dorsal_theta_deg": df["theta_deg"],
            "dorsal_rms_px": df["rms_orthogonal_residual_px"],
            "dorsal_centroid_xy": df["centroid_xy"],
            "ventral_theta_deg": vf["theta_deg"],
            "ventral_rms_px": vf["rms_orthogonal_residual_px"],
            "ventral_centroid_xy": vf["centroid_xy"],
            "convergence_angle_deg": vf["theta_deg"] - df["theta_deg"]
        }

    # DRLX (CAHV linearized) line fits (shifted by dx=-3, dy=-3)
    dorsal_st_drlx = extract_subpixel_profile_edges(
        drlx_lum, [1033.0, 944.2], [1065.5, 960.6], n_stations=26, grad_sign=+1
    )
    ventral_st_drlx = extract_subpixel_profile_edges(
        drlx_lum, [1030.2, 949.5], [1048.2, 986.5], n_stations=26, grad_sign=-1
    )
    dorsal_fit_drlx = fit_line_orthogonal([s["x_erf"] for s in dorsal_st_drlx], [s["y_erf"] for s in dorsal_st_drlx])
    ventral_fit_drlx = fit_line_orthogonal([s["x_erf"] for s in ventral_st_drlx], [s["y_erf"] for s in ventral_st_drlx])

    # Compute intersection point (apex) of Dorsal and Ventral lines in DRXX
    p1 = np.array(dorsal_fit_erf["centroid_xy"])
    t1 = np.array(dorsal_fit_erf["t_hat"])
    p2 = np.array(ventral_full_fit_erf["centroid_xy"])
    t2 = np.array(ventral_full_fit_erf["t_hat"])
    s_sol = np.linalg.solve(np.column_stack([t1, -t2]), p2 - p1)
    apex_xy_full = (p1 + s_sol[0] * t1).tolist()

    p2c = np.array(ventral_clean_fit_erf["centroid_xy"])
    t2c = np.array(ventral_clean_fit_erf["t_hat"])
    s_sol_c = np.linalg.solve(np.column_stack([t1, -t2c]), p2c - p1)
    apex_xy_clean = (p1 + s_sol_c[0] * t1).tolist()

    # 3. Extract End-Face / Shadow Boundary Points in DRXX
    dark_center = (1067.5, 985.0)
    all_thetas = np.arange(-180.0, 180.0, 5.0)
    arch_all_pts = extract_radial_arch_points(drxx_lum, dark_center, all_thetas, r_min=6.0, r_max=25.0)

    def is_proximal_rim(th_deg):
        return (th_deg >= 150.0) or (th_deg <= -50.0)

    def is_proximal_strict(th_deg):
        return (th_deg >= 160.0) or (th_deg <= -60.0)

    feature_data = {
        "extraction_geometry": {
            "version": "physical-edge-polarity-v2",
            "image_y_axis": "down",
            "normal_definition": "(-tangent_y, tangent_x)",
            "dorsal_grad_sign": 1,
            "ventral_grad_sign": -1,
            "description": "Upper exterior dark-to-bright and lower exterior bright-to-dark along +normal."
        },
        "radiometry_and_noise": {
            "soil_background_highfreq_noise_std_rad": soil_noise_std,
            "object_bright_mean_rad": obj_bright_mean,
            "object_bright_max_rad": obj_bright_max,
            "shadow_core_mean_rad": shadow_core_mean,
            "shadow_core_min_rad": shadow_core_min,
            "shadow_core_std_rad": shadow_core_std,
            "contrast_ratio_bright_over_shadow": obj_bright_mean / shadow_core_mean,
            "edge_snr": snr_edge,
            "bright_mean_dn_rgb": bright_dn_band,
            "shadow_mean_dn_rgb": shadow_dn_band,
            "mean_dorsal_psf_sigma_px": float(np.mean([s["sigma_blur_px"] for s in dorsal_stations_drxx])),
            "mean_dorsal_psf_fwhm_px": float(2.3548 * np.mean([s["sigma_blur_px"] for s in dorsal_stations_drxx])),
            "mean_proximal_arch_psf_sigma_px": float(np.mean([p["sigma_blur_px"] for p in arch_all_pts if is_proximal_strict(p["theta_deg"])]))
        },
        "longitudinal_edges_drxx": {
            "dorsal_erf": dorsal_fit_erf,
            "dorsal_grad": dorsal_fit_grad,
            "ventral_full_erf": ventral_full_fit_erf,
            "ventral_clean_erf": ventral_clean_fit_erf,
            "ventral_full_grad": ventral_full_fit_grad,
            "convergence_angle_full_erf_deg": ventral_full_fit_erf["theta_deg"] - dorsal_fit_erf["theta_deg"],
            "convergence_angle_clean_erf_deg": ventral_clean_fit_erf["theta_deg"] - dorsal_fit_erf["theta_deg"],
            "convergence_angle_grad_deg": ventral_full_fit_grad["theta_deg"] - dorsal_fit_grad["theta_deg"],
            "bisector_angle_full_erf_deg": 0.5 * (ventral_full_fit_erf["theta_deg"] + dorsal_fit_erf["theta_deg"]),
            "bisector_angle_clean_erf_deg": 0.5 * (ventral_clean_fit_erf["theta_deg"] + dorsal_fit_erf["theta_deg"]),
            "apex_intersection_full_xy": apex_xy_full,
            "apex_intersection_clean_xy": apex_xy_clean
        },
        "longitudinal_edges_multiband_drxx": band_fits,
        "longitudinal_edges_drlx_cahv": {
            "dorsal_theta_deg": dorsal_fit_drlx["theta_deg"],
            "dorsal_rms_px": dorsal_fit_drlx["rms_orthogonal_residual_px"],
            "ventral_theta_deg": ventral_fit_drlx["theta_deg"],
            "ventral_rms_px": ventral_fit_drlx["rms_orthogonal_residual_px"],
            "convergence_angle_deg": ventral_fit_drlx["theta_deg"] - dorsal_fit_drlx["theta_deg"],
            "bisector_angle_deg": 0.5 * (ventral_fit_drlx["theta_deg"] + dorsal_fit_drlx["theta_deg"])
        },
        "dorsal_stations": dorsal_stations_drxx,
        "ventral_stations": ventral_full_stations_drxx,
        "arch_radial_points": arch_all_pts
    }

    with open(os.path.join(OUT_DIR, "step3_features.json"), "w") as f:
        json.dump(feature_data, f, indent=2)

    # Diagnostic Figure 3: Subpixel Edge Localization & Residual Analysis
    fig, axes = plt.subplots(2, 2, figsize=(16, 14), dpi=150)
    tx0, tx1, ty0, ty1 = 1020, 1105, 942, 1015
    crop_lum = drxx_lum[ty0:ty1, tx0:tx1]

    axes[0, 0].imshow(crop_lum, extent=[tx0 - 0.5, tx1 - 0.5, ty1 - 0.5, ty0 - 0.5], cmap="gray", interpolation="nearest")
    axes[0, 0].plot([s["x_erf"] for s in dorsal_stations_drxx], [s["y_erf"] for s in dorsal_stations_drxx], "c.-", label="Dorsal Edge (Zone 1, Erf)")
    axes[0, 0].plot([s["x_erf"] for s in ventral_full_stations_drxx], [s["y_erf"] for s in ventral_full_stations_drxx], "m.-", label="Ventral Edge (Zone 2, Erf)")
    # Plot fitted lines extrapolated to apex
    s_vals = np.linspace(-25, 22, 50)
    axes[0, 0].plot(p1[0] + s_vals * t1[0], p1[1] + s_vals * t1[1], "c--", alpha=0.7)
    axes[0, 0].plot(p2[0] + s_vals * t2[0], p2[1] + s_vals * t2[1], "m--", alpha=0.7)
    axes[0, 0].plot(apex_xy_full[0], apex_xy_full[1], "yo", markersize=8, label=f"Apex ({apex_xy_full[0]:.1f}, {apex_xy_full[1]:.1f})")

    prox_pts = [p for p in arch_all_pts if is_proximal_rim(p["theta_deg"])]
    dist_pts = [p for p in arch_all_pts if not is_proximal_rim(p["theta_deg"])]
    axes[0, 0].plot([p["x_erf"] for p in prox_pts], [p["y_erf"] for p in prox_pts], "lime", marker="o", linestyle="none", markersize=4, label="Proximal Rim Arch (Zone 3)")
    axes[0, 0].plot([p["x_erf"] for p in dist_pts], [p["y_erf"] for p in dist_pts], "orangered", marker="s", linestyle="none", markersize=4, label="Distal Shadow Boundary (Zone 4)")
    axes[0, 0].plot(dark_center[0], dark_center[1], "r+", markersize=10)
    axes[0, 0].set_xlim(tx0, tx1)
    axes[0, 0].set_ylim(ty1, ty0)
    axes[0, 0].set_title("Subpixel Feature Extraction on DRXX Luminance")
    axes[0, 0].set_xlabel("Sample x (px)")
    axes[0, 0].set_ylabel("Line y (px)")
    axes[0, 0].legend(loc="lower left", fontsize=8)
    axes[0, 0].grid(True, alpha=0.25)

    axes[0, 1].axhline(0, color="black", linestyle="--", alpha=0.5)
    axes[0, 1].plot(dorsal_fit_erf["u_coords"], dorsal_fit_erf["v_residuals"], "co-", label=f"Dorsal Line Residual (RMS={dorsal_fit_erf['rms_orthogonal_residual_px']:.3f} px)")
    axes[0, 1].plot(ventral_full_fit_erf["u_coords"], ventral_full_fit_erf["v_residuals"], "mo-", label=f"Ventral Full Residual (RMS={ventral_full_fit_erf['rms_orthogonal_residual_px']:.3f} px)")
    axes[0, 1].set_title("Longitudinal Edge Straightness: Orthogonal Residuals v(u)")
    axes[0, 1].set_xlabel("Position along edge u from centroid (px)")
    axes[0, 1].set_ylabel("Orthogonal deviation v (px)")
    axes[0, 1].set_ylim(-0.6, 0.6)
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    th_arr = [p["theta_deg"] for p in arch_all_pts]
    c_arr = [p["contrast_rad"] for p in arch_all_pts]
    sig_arr = [p["sigma_blur_px"] for p in arch_all_pts]
    ax3 = axes[1, 0]
    ax3_twin = ax3.twinx()
    ax3.plot(th_arr, c_arr, "b-o", markersize=4, label="Edge Contrast (W/m^2/sr/nm)")
    ax3_twin.plot(th_arr, sig_arr, "r--s", markersize=3, alpha=0.7, label="Edge Blur Sigma (px)")
    ax3.axvspan(-45, 145, color="orangered", alpha=0.15, label="Distal Shadow-to-Soil Zone")
    ax3.set_title("Boundary Contrast & Sharpness vs Polar Angle Around Dark Patch")
    ax3.set_xlabel("Polar Angle theta from (1067.5, 985.0) [deg]")
    ax3.set_ylabel("Radiance Step Contrast", color="b")
    ax3_twin.set_ylabel("Gaussian Edge Sigma (px)", color="r")
    ax3.grid(True, alpha=0.3)
    ax3.legend(loc="upper left", fontsize=8)

    b_names = list(band_fits.keys())
    d_thetas = [band_fits[k]["dorsal_theta_deg"] for k in b_names]
    v_thetas = [band_fits[k]["ventral_theta_deg"] for k in b_names]
    conv_thetas = [band_fits[k]["convergence_angle_deg"] for k in b_names]
    x_pos = np.arange(len(b_names))
    width = 0.25
    axes[1, 1].bar(x_pos - width, d_thetas, width, label="Dorsal Angle (deg)", color="steelblue")
    axes[1, 1].bar(x_pos, v_thetas, width, label="Ventral Angle (deg)", color="mediumvioletred")
    axes[1, 1].bar(x_pos + width, conv_thetas, width, label="Convergence Opening Angle (deg)", color="seagreen")
    axes[1, 1].set_xticks(x_pos)
    axes[1, 1].set_xticklabels(["Red (Band 0)", "Green (Band 1)", "Blue (Band 2)"])
    axes[1, 1].set_ylabel("Angle in Image Plane (deg)")
    axes[1, 1].set_title("Stability Across RGB Spectral Bands (Bayer Demosaicing Test)")
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "diag03_subpixel_edges.png"))
    plt.close()

    print("Step 3 Refined Summary:")
    print(json.dumps({
        "dorsal_theta_deg": dorsal_fit_erf["theta_deg"],
        "dorsal_theta_unc_deg": dorsal_fit_erf["theta_uncertainty_deg"],
        "dorsal_rms_px": dorsal_fit_erf["rms_orthogonal_residual_px"],
        "dorsal_max_res_px": dorsal_fit_erf["max_orthogonal_residual_px"],
        "dorsal_curvature_z": dorsal_fit_erf["curvature_z_score"],
        "dorsal_sagitta_px": dorsal_fit_erf["max_sagitta_deviation_px"],
        "ventral_full_theta_deg": ventral_full_fit_erf["theta_deg"],
        "ventral_full_theta_unc_deg": ventral_full_fit_erf["theta_uncertainty_deg"],
        "ventral_full_rms_px": ventral_full_fit_erf["rms_orthogonal_residual_px"],
        "ventral_clean_theta_deg": ventral_clean_fit_erf["theta_deg"],
        "ventral_clean_rms_px": ventral_clean_fit_erf["rms_orthogonal_residual_px"],
        "convergence_angle_full_deg": feature_data["longitudinal_edges_drxx"]["convergence_angle_full_erf_deg"],
        "convergence_angle_clean_deg": feature_data["longitudinal_edges_drxx"]["convergence_angle_clean_erf_deg"],
        "convergence_angle_grad_deg": feature_data["longitudinal_edges_drxx"]["convergence_angle_grad_deg"],
        "bisector_angle_full_deg": feature_data["longitudinal_edges_drxx"]["bisector_angle_full_erf_deg"],
        "apex_xy_full": apex_xy_full,
        "apex_xy_clean": apex_xy_clean,
        "drlx_convergence_angle_deg": feature_data["longitudinal_edges_drlx_cahv"]["convergence_angle_deg"],
        "drlx_dorsal_rms_px": dorsal_fit_drlx["rms_orthogonal_residual_px"],
        "drlx_ventral_rms_px": ventral_fit_drlx["rms_orthogonal_residual_px"]
    }, indent=2))

if __name__ == "__main__":
    main()
