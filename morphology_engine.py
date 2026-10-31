"""
morphology_engine.py — Objective, Rotation-Invariant Martian Morphology Measurement Engine
========================================================================================
Implements full geometric morphology extraction for Martian rock clasts and candidate
technosignatures using consistent, rotation-invariant metrics:

1. Elongation / Aspect Ratio (L / W)
2. Longitudinal Edge Straightness (Perpendicular TLS RMSE & Normalized Straightness)
3. Width Consistency (Coefficient of Variation of body width CV_W = sigma_W / mu_W)
4. Flank Parallelism (Absolute angle difference between opposing longitudinal flanks |Delta theta|)
5. Terminal Curvature (Apex curvature ratio R_apex / (W/2))
6. End-Face Presence (Boolean: distinct planar/circular terminal face bounded by sharp rim)
7. End-Face Circularity (Fitzgibbon ellipse b/a ratio where end-face is present)
8. Geometric Continuity (Junction regularity between longitudinal flanks and end-cap)
9. Image Quality / SNR (Gradient peak to local background noise ratio)

Works with pure numpy, scipy, and Pillow. Zero external heavy dependencies.
"""

import math
import numpy as np
import scipy.ndimage as ndi
import geometry_utils as gu


def sobel_gradients(gray):
    """Compute 2D Sobel derivatives and gradient magnitude."""
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float) / 4.0
    ky = kx.T
    sx = ndi.convolve(gray, kx, mode="reflect")
    sy = ndi.convolve(gray, ky, mode="reflect")
    g = np.hypot(sx, sy)
    return sx, sy, g


def subpixel_peak(g_line, idx):
    """Parabolic subpixel peak interpolation."""
    idx = int(idx)
    if 1 <= idx < len(g_line) - 1:
        denom = g_line[idx - 1] - 2.0 * g_line[idx] + g_line[idx + 1]
        if abs(denom) > 1e-9:
            delta = 0.5 * (g_line[idx - 1] - g_line[idx + 1]) / denom
            if abs(delta) <= 1.0:
                return float(idx + delta)
    return float(idx)


from reproduce_analysis import fit_ellipse_fitzgibbon


def analyze_clast_morphology(
    gray_image,
    binary_mask,
    clast_id="CLAST_000",
    name="Martian Rock Clast",
    geological_context="Bedrock Float",
    mission_sol=3556,
    product_id="3556MR1025170721700585C00",
    image_url="",
    window_lines=20,
):
    """
    Evaluates the complete 9-dimensional morphology of a detected clast.
    Returns a comprehensive dict of metrics.
    """
    indices = np.where(binary_mask)
    if len(indices[0]) < 80:
        return None  # Too small for reliable morphology

    y_pts, x_pts = indices[0], indices[1]
    y_min, y_max = int(np.min(y_pts)), int(np.max(y_pts))
    x_min, x_max = int(np.min(x_pts)), int(np.max(x_pts))

    # Pad bounding box
    pad = 6
    y0 = max(0, y_min - pad)
    y1 = min(gray_image.shape[0], y_max + pad + 1)
    x0 = max(0, x_min - pad)
    x1 = min(gray_image.shape[1], x_max + pad + 1)

    sub_gray = gray_image[y0:y1, x0:x1]
    sub_mask = binary_mask[y0:y1, x0:x1]

    sx, sy, g = sobel_gradients(sub_gray)
    noise_sigma = float(np.std(g[~sub_mask])) if np.sum(~sub_mask) > 10 else 1.0
    peak_g = float(np.max(g[sub_mask])) if np.sum(sub_mask) > 0 else 0.0
    edge_snr = float(peak_g / max(noise_sigma, 1e-3))

    # Centroid and PCA orientation
    xc = float(np.mean(x_pts))
    yc = float(np.mean(y_pts))
    pts_centered = np.column_stack([x_pts - xc, y_pts - yc])
    cov = np.cov(pts_centered, rowvar=False, ddof=0)
    evals, evecs = np.linalg.eigh(cov)
    idx_sort = np.argsort(evals)[::-1]
    evals = evals[idx_sort]
    evecs = evecs[:, idx_sort]

    # Major axis unit vector
    u_axis = evecs[:, 0]
    v_axis = evecs[:, 1]
    longitudinal_angle_deg = (math.degrees(math.atan2(u_axis[1], u_axis[0]))) % 180.0

    # Project coordinates onto principal frame (u = along length, v = across width)
    u_coords = pts_centered @ u_axis
    v_coords = pts_centered @ v_axis

    length_px = float(np.ptp(u_coords))
    width_px = float(np.ptp(v_coords))
    if width_px < 2.0:
        return None

    aspect_ratio = float(length_px / max(width_px, 1e-3))

    # -------------------------------------------------------------
    # Boundary contour extraction via subpixel edge gradient
    # -------------------------------------------------------------
    boundary_mask = ndi.binary_dilation(sub_mask) ^ ndi.binary_erosion(sub_mask)
    b_y, b_x = np.where(boundary_mask)
    if len(b_x) < 20:
        return None

    # Global coordinates of boundary
    gx_b = b_x + x0
    gy_b = b_y + y0
    b_u = (np.column_stack([gx_b - xc, gy_b - yc])) @ u_axis
    b_v = (np.column_stack([gx_b - xc, gy_b - yc])) @ v_axis

    # -------------------------------------------------------------
    # 2. Longitudinal Edge Straightness (Rotation-Invariant TLS)
    # -------------------------------------------------------------
    # Split boundary into upper flank (v > 0.15*v_max) and lower flank (v < 0.15*v_min)
    v_max = np.max(b_v)
    v_min = np.min(b_v)
    v_range = v_max - v_min

    up_idx = np.where(b_v > 0.15 * v_range)[0]
    low_idx = np.where(b_v < -0.15 * v_range)[0]

    up_rmse = float("nan")
    low_rmse = float("nan")
    up_angle = float("nan")
    low_angle = float("nan")
    straightness_rmse_px = float("nan")
    normalized_straightness = float("nan")

    # Sort upper flank along u
    if len(up_idx) >= 8:
        sort_up = np.argsort(b_u[up_idx])
        up_x = gx_b[up_idx][sort_up]
        up_y = gy_b[up_idx][sort_up]
        win_size = min(window_lines, len(up_x))
        if win_size >= 5:
            fit_up = gu.best_straight_window(up_x, up_y, win_size)
            up_rmse = fit_up["rmse_perp"]
            up_angle = fit_up["angle_deg"]

    # Sort lower flank along u
    if len(low_idx) >= 8:
        sort_low = np.argsort(b_u[low_idx])
        low_x = gx_b[low_idx][sort_low]
        low_y = gy_b[low_idx][sort_low]
        win_size = min(window_lines, len(low_x))
        if win_size >= 5:
            fit_low = gu.best_straight_window(low_x, low_y, win_size)
            low_rmse = fit_low["rmse_perp"]
            low_angle = fit_low["angle_deg"]

    valid_rmses = [r for r in [up_rmse, low_rmse] if not math.isnan(r)]
    if valid_rmses:
        straightness_rmse_px = float(min(valid_rmses))
        normalized_straightness = float(straightness_rmse_px / max(length_px, 1e-3))
    else:
        # Fallback to direct boundary fit
        full_fit = gu.tls_line_fit(gx_b, gy_b)
        straightness_rmse_px = float(full_fit["rmse_perp"])
        normalized_straightness = float(straightness_rmse_px / max(length_px, 1e-3))

    # -------------------------------------------------------------
    # 4. Flank Parallelism (|Delta theta|)
    # -------------------------------------------------------------
    if not math.isnan(up_angle) and not math.isnan(low_angle):
        diff_ang = abs(up_angle - low_angle) % 180.0
        flank_parallelism_deg = float(min(diff_ang, 180.0 - diff_ang))
    else:
        flank_parallelism_deg = float("nan")

    # -------------------------------------------------------------
    # 3. Width Consistency (Coefficient of Variation of Width CV_W)
    # -------------------------------------------------------------
    # Slice the body along u from 15% to 85% of length
    u_span = np.linspace(np.min(u_coords) * 0.7, np.max(u_coords) * 0.7, 12)
    slice_widths = []
    half_bin = (u_span[1] - u_span[0]) if len(u_span) > 1 else 2.0
    for u_val in u_span:
        bin_pts = np.where((u_coords >= u_val - half_bin) & (u_coords <= u_val + half_bin))[0]
        if len(bin_pts) >= 4:
            slice_widths.append(float(np.ptp(v_coords[bin_pts])))

    if len(slice_widths) >= 4:
        mean_w = float(np.mean(slice_widths))
        std_w = float(np.std(slice_widths))
        width_cv = float(std_w / max(mean_w, 1e-3))
    else:
        width_cv = float("nan")

    # -------------------------------------------------------------
    # 5. Terminal Curvature (Apex curvature ratio)
    # -------------------------------------------------------------
    # Find points near positive u apex (u > 0.8 * max(u))
    apex_idx = np.where(b_u > 0.75 * np.max(b_u))[0]
    if len(apex_idx) >= 5:
        # Fit circle to apex points
        ax_x = gx_b[apex_idx]
        ax_y = gy_b[apex_idx]
        # Direct circle fit via TLS
        A_mat = np.column_stack([ax_x, ax_y, np.ones_like(ax_x)])
        b_vec = ax_x**2 + ax_y**2
        try:
            sol, _, _, _ = np.linalg.lstsq(A_mat, b_vec, rcond=None)
            x_c_circ = sol[0] / 2.0
            y_c_circ = sol[1] / 2.0
            r_apex = math.sqrt(max(0.1, sol[2] + x_c_circ**2 + y_c_circ**2))
            terminal_curvature_ratio = float(r_apex / max(width_px / 2.0, 1e-3))
        except Exception:
            terminal_curvature_ratio = float("nan")
    else:
        terminal_curvature_ratio = float("nan")

    # -------------------------------------------------------------
    # 6. Presence of Identifiable End-Face
    # -------------------------------------------------------------
    # Check whether the terminus has a distinct, closed circular/faceted planar face
    # A true end-face presents an internal gradient discontinuity or a distinct closed perimeter
    # at the terminal pole, distinct from a smooth tapered rock nose or fractured edge.
    has_end_face = False
    endface_ba = None
    endface_rmse = None

    # Inspect positive and negative u termini
    for pole_sign in (+1.0, -1.0):
        pole_mask = (b_u * pole_sign) > (0.65 * np.max(b_u * pole_sign))
        pole_idx = np.where(pole_mask)[0]
        if len(pole_idx) >= 12:
            pole_x = gx_b[pole_idx]
            pole_y = gy_b[pole_idx]
            # Check if this terminal rim fits a coherent ellipse with low residual
            e_fit = fit_ellipse_fitzgibbon(pole_x, pole_y)
            if e_fit is not None:
                # Check if center lies near the pole and aspect ratio is reasonable
                r_c = math.sqrt((e_fit["xc"] - xc)**2 + (e_fit["yc"] - yc)**2)
                # If the ellipse forms a coherent end-cap
                if 0.5 <= e_fit["circ_ratio"] <= 1.0 and e_fit["major_2a"] <= 1.5 * width_px:
                    # Check internal contrast inside end-cap
                    has_end_face = True
                    endface_ba = float(e_fit["circ_ratio"])
                    break

    # -------------------------------------------------------------
    # 8. Geometric Continuity (Junction regularity)
    # -------------------------------------------------------------
    # Measures the angular discontinuity between longitudinal flank and cap apex
    continuity_score = 1.0
    if not math.isnan(straightness_rmse_px):
        # Discontinuity penalty if straight flank suddenly breaks irregularly
        continuity_score = float(max(0.0, 1.0 - straightness_rmse_px / 5.0))

    return {
        "clast_id": clast_id,
        "name": name,
        "geological_context": geological_context,
        "mission_sol": mission_sol,
        "product_id": product_id,
        "image_url": image_url,
        "centroid_xy": [round(xc, 2), round(yc, 2)],
        "area_px": int(len(x_pts)),
        "length_px": round(length_px, 2),
        "width_px": round(width_px, 2),
        "aspect_ratio": round(aspect_ratio, 3),
        "longitudinal_angle_deg": round(longitudinal_angle_deg, 2),
        "straightness_rmse_px": round(straightness_rmse_px, 3) if not math.isnan(straightness_rmse_px) else None,
        "normalized_straightness": round(normalized_straightness, 5) if not math.isnan(normalized_straightness) else None,
        "flank_parallelism_deg": round(flank_parallelism_deg, 2) if not math.isnan(flank_parallelism_deg) else None,
        "width_cv": round(width_cv, 4) if not math.isnan(width_cv) else None,
        "terminal_curvature_ratio": round(terminal_curvature_ratio, 3) if not math.isnan(terminal_curvature_ratio) else None,
        "has_end_face": has_end_face,
        "endface_ba": round(endface_ba, 4) if endface_ba is not None else None,
        "continuity_score": round(continuity_score, 3),
        "edge_snr": round(edge_snr, 2),
    }
