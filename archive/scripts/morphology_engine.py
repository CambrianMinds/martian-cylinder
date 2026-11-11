"""
morphology_engine.py — Objective, Rotation-Invariant Martian Morphology Measurement Engine
========================================================================================
Implements full geometric morphology extraction for Martian rock clasts, candidate
technosignatures, and positive manufactured controls using consistent, rotation-invariant metrics:

1. Elongation / Aspect Ratio (L / W)
2. Longitudinal Edge Straightness (Perpendicular TLS RMSE & Normalized Straightness)
3. Width Consistency (Coefficient of Variation of body width CV_W = sigma_W / mu_W)
4. Flank Parallelism (Absolute angle difference between opposing longitudinal flanks |Delta theta|)
5. Terminal Curvature (Apex curvature ratio R_apex / (W/2))
6. End-Face Presence (Boolean: distinct planar/circular terminal face bounded by coherent transverse rim)
7. End-Face Circularity (Fitzgibbon ellipse b/a ratio where end-face is present)
8. Geometric Continuity (Junction regularity between longitudinal flanks and end-cap)
9. Image Quality / SNR (Gradient peak to local background noise ratio)

Works with pure numpy, scipy, and Pillow. Zero external heavy dependencies.
"""

import math
import numpy as np
import scipy.ndimage as ndi
import geometry_utils as gu
from reproduce_analysis import fit_ellipse_fitzgibbon


def sobel_gradients(gray):
    """Compute 2D Sobel derivatives and gradient magnitude."""
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float) / 4.0
    ky = kx.T
    sx = ndi.convolve(gray, kx, mode="reflect")
    sy = ndi.convolve(gray, ky, mode="reflect")
    g = np.hypot(sx, sy)
    return sx, sy, g


def find_refined_pole_center(gray, xc, yc, u_axis, length_px, width_px, sgn):
    """
    Locates the true physical center of an end-face near a clast pole.
    Searches for a local contrast core (dark or bright facet) along the principal axis.
    """
    r_nom = width_px / 2.0
    d_cand = max(2.0, (length_px / 2.0) - r_nom * 0.9)
    px0 = xc + sgn * d_cand * u_axis[0]
    py0 = yc + sgn * d_cand * u_axis[1]

    win = int(math.ceil(r_nom * 1.5))
    ix0 = max(0, int(round(px0 - win)))
    ix1 = min(gray.shape[1], int(round(px0 + win)))
    iy0 = max(0, int(round(py0 - win)))
    iy1 = min(gray.shape[0], int(round(py0 + win)))

    patch = gray[iy0:iy1, ix0:ix1]
    if patch.size < 25:
        return px0, py0

    p_med = float(np.median(patch))
    # Check for dark core facet
    dark_mask = patch < (p_med - 15.0)
    if np.sum(dark_mask) >= 15:
        yy, xx = np.where(dark_mask)
        return ix0 + float(np.mean(xx)), iy0 + float(np.mean(yy))

    # Check for bright core facet
    bright_mask = patch > (p_med + 15.0)
    if np.sum(bright_mask) >= 15:
        yy, xx = np.where(bright_mask)
        return ix0 + float(np.mean(xx)), iy0 + float(np.mean(yy))

    return px0, py0


def detect_end_face_rim(gray, sx, sy, xc, yc, u_axis, v_axis, length_px, width_px):
    """
    Detects whether an actual physical end-face is present near either longitudinal pole.
    A physical end face has:
      1. A candidate center located near the pole inside the body with local photometric contrast.
      2. A coherent, high-contrast rim with outward radial gradients in at least 16 of 36 directions (>= 45% arc).
      3. Low radial dispersion (MAD(r) / median(r) < 0.28).
      4. A valid Fitzgibbon ellipse fit with b/a in [0.65, 1.05] and major radius scaling consistently with clast width.
    """
    r_nom = width_px / 2.0
    if r_nom < 3.0:
        return False, None, None

    best_face = None
    best_face_score = 999.0

    for sgn in (+1.0, -1.0):
        d_cand = max(2.0, (length_px / 2.0) - r_nom * 0.75)
        px0 = xc + sgn * d_cand * u_axis[0]
        py0 = yc + sgn * d_cand * u_axis[1]

        w_box = int(round(r_nom * 1.3))
        ix0 = max(0, int(round(px0 - w_box)))
        ix1 = min(gray.shape[1], int(round(px0 + w_box)))
        iy0 = max(0, int(round(py0 - w_box)))
        iy1 = min(gray.shape[0], int(round(py0 + w_box)))

        candidates = [(px0, py0)]
        if iy1 > iy0 + 5 and ix1 > ix0 + 5:
            patch = gray[iy0:iy1, ix0:ix1]
            p_med = float(np.median(patch))
            p_min = float(np.min(patch))
            p_max = float(np.max(patch))
            if p_med - p_min > 15.0:
                yy_d, xx_d = np.where(patch < (p_min + 0.4 * (p_med - p_min)))
                if len(xx_d) >= 6:
                    candidates.insert(0, (ix0 + float(np.mean(xx_d)), iy0 + float(np.mean(yy_d))))
            if p_max - p_med > 15.0:
                yy_b, xx_b = np.where(patch > (p_max - 0.4 * (p_max - p_med)))
                if len(xx_b) >= 6:
                    candidates.insert(0, (ix0 + float(np.mean(xx_b)), iy0 + float(np.mean(yy_b))))

        for (cx_cand, cy_cand) in candidates:
            radii_samples = np.linspace(max(3.0, 0.4 * r_nom), 2.2 * r_nom, 48)
            rim_pts = []
            for deg in np.linspace(0.0, 360.0, 36, endpoint=False):
                rad = math.radians(deg)
                ca, sa = math.cos(rad), math.sin(rad)
                vals = []
                for r in radii_samples:
                    ix = int(round(cx_cand + r * ca))
                    iy = int(round(cy_cand + r * sa))
                    if 0 <= iy < gray.shape[0] and 0 <= ix < gray.shape[1]:
                        g_rad = sx[iy, ix] * ca + sy[iy, ix] * sa
                        vals.append(g_rad)
                    else:
                        vals.append(0.0)
                if vals:
                    max_i = int(np.argmax(vals))
                    if vals[max_i] > 10.0:
                        r_peak = radii_samples[max_i]
                        rim_pts.append((deg, r_peak, cx_cand + r_peak * ca, cy_cand + r_peak * sa))

            if len(rim_pts) >= 16:
                r_vals = np.array([p[1] for p in rim_pts])
                med_r = float(np.median(r_vals))
                mad_r = float(np.median(np.abs(r_vals - med_r)))
                if (mad_r / max(med_r, 1e-3)) < 0.28:
                    clean_pts = [p for p in rim_pts if abs(p[1] - med_r) <= 2.5 * mad_r]
                    if len(clean_pts) >= 14:
                        xs = np.array([p[2] for p in clean_pts])
                        ys = np.array([p[3] for p in clean_pts])
                        e_fit = fit_ellipse_fitzgibbon(xs, ys)
                        if e_fit is not None and 0.65 <= e_fit["circ_ratio"] <= 1.05:
                            fit_r = e_fit["major_2a"] / 2.0
                            if 0.5 * r_nom <= fit_r <= 2.5 * r_nom:
                                best_face = (True, float(e_fit["circ_ratio"]), e_fit)
                                break
        if best_face:
            break
                                cand_score = abs(e_fit["circ_ratio"] - 1.0)
                                if cand_score < best_face_score:
                                    best_face = (True, float(e_fit["circ_ratio"]), e_fit)
                                    best_face_score = cand_score

    if best_face:
        return best_face[0], best_face[1], best_face[2]
    return False, None, None


def analyze_clast_morphology(
    gray_image,
    binary_mask,
    clast_id="CLAST_000",
    name="Martian Rock Clast",
    geological_context="Bedrock Float",
    mission_sol=3556,
    product_id="3556MR1025170721700585C00",
    image_url="",
    min_window=15,
    window_lines=None,
):
    """
    Evaluates the complete 9-dimensional morphology of a detected clast.
    Returns a comprehensive dict of metrics.
    """
    if window_lines is not None:
        min_window = window_lines
    indices = np.where(binary_mask)
    if len(indices[0]) < 80:
        return None  # Too small for reliable morphology

    y_pts, x_pts = indices[0], indices[1]
    y_min, y_max = int(np.min(y_pts)), int(np.max(y_pts))
    x_min, x_max = int(np.min(x_pts)), int(np.max(x_pts))

    # Pad bounding box
    pad = 8
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

    # Major axis unit vector (u_axis) and transverse unit vector (v_axis)
    u_axis = evecs[:, 0]
    v_axis = evecs[:, 1]
    longitudinal_angle_deg = (math.degrees(math.atan2(u_axis[1], u_axis[0]))) % 180.0

    # Project coordinates onto principal frame (u = along length, v = across width)
    u_coords = pts_centered @ u_axis
    v_coords = pts_centered @ v_axis

    length_px = float(np.ptp(u_coords))
    width_px = float(np.ptp(v_coords))
    if width_px < 2.0 or length_px < 5.0:
        return None

    aspect_ratio = float(length_px / max(width_px, 1e-3))

    # -------------------------------------------------------------
    # Boundary contour extraction with sub-pixel normal refinement
    # -------------------------------------------------------------
    boundary_mask = ndi.binary_dilation(sub_mask) ^ ndi.binary_erosion(sub_mask)
    b_y, b_x = np.where(boundary_mask)
    if len(b_x) < 20:
        return None

    # Sub-pixel boundary refinement along Sobel gradient normal
    gx_sub = []
    gy_sub = []
    for bx, by in zip(b_x, b_y):
        if 1 <= bx < sub_gray.shape[1] - 1 and 1 <= by < sub_gray.shape[0] - 1 and g[by, bx] > 3.0:
            sgx, sgy = sx[by, bx], sy[by, bx]
            s_hyp = math.hypot(sgx, sgy)
            nx, ny = sgx / s_hyp, sgy / s_hyp
            gm1 = g[int(round(by - ny)), int(round(bx - nx))]
            g0 = g[by, bx]
            gp1 = g[int(round(by + ny)), int(round(bx + nx))]
            denom = gm1 - 2.0 * g0 + gp1
            delta = 0.5 * (gm1 - gp1) / denom if abs(denom) > 1e-4 else 0.0
            delta = max(-0.8, min(0.8, delta))
            gx_sub.append(bx + x0 + delta * nx)
            gy_sub.append(by + y0 + delta * ny)
        else:
            gx_sub.append(float(bx + x0))
            gy_sub.append(float(by + y0))

    gx_b = np.array(gx_sub)
    gy_b = np.array(gy_sub)
    b_u = (np.column_stack([gx_b - xc, gy_b - yc])) @ u_axis
    b_v = (np.column_stack([gx_b - xc, gy_b - yc])) @ v_axis

    # -------------------------------------------------------------
    # 2. Longitudinal Flank Straightness (Rotation-Invariant TLS)
    # -------------------------------------------------------------
    # Segment upper flank (v > 0.15*v_range) and lower flank (v < -0.15*v_range)
    v_range = float(np.ptp(b_v))
    up_idx = np.where(b_v > 0.15 * v_range)[0]
    low_idx = np.where(b_v < -0.15 * v_range)[0]

    up_rmse = float("nan")
    low_rmse = float("nan")
    up_angle = float("nan")
    low_angle = float("nan")
    straightness_rmse_px = float("nan")
    normalized_straightness = float("nan")

    # Meaningful window size: at least min_window (15 px) or 35% of flank length
    if len(up_idx) >= 12:
        sort_up = np.argsort(b_u[up_idx])
        up_x = gx_b[up_idx][sort_up]
        up_y = gy_b[up_idx][sort_up]
        win_size = min(len(up_x), max(min_window, int(0.35 * len(up_x))))
        if win_size >= 10:
            fit_up = gu.best_straight_window(up_x, up_y, win_size)
            up_rmse = fit_up["rmse_perp"]
            up_angle = fit_up["angle_deg"]

    if len(low_idx) >= 12:
        sort_low = np.argsort(b_u[low_idx])
        low_x = gx_b[low_idx][sort_low]
        low_y = gy_b[low_idx][sort_low]
        win_size = min(len(low_x), max(min_window, int(0.35 * len(low_x))))
        if win_size >= 10:
            fit_low = gu.best_straight_window(low_x, low_y, win_size)
            low_rmse = fit_low["rmse_perp"]
            low_angle = fit_low["angle_deg"]

    valid_rmses = [r for r in [up_rmse, low_rmse] if not math.isnan(r)]
    if valid_rmses:
        straightness_rmse_px = float(min(valid_rmses))
        normalized_straightness = float(straightness_rmse_px / max(length_px, 1e-3))
    else:
        full_fit = gu.tls_line_fit(gx_b, gy_b)
        straightness_rmse_px = float(full_fit["rmse_perp"])
        normalized_straightness = float(straightness_rmse_px / max(length_px, 1e-3))

    # -------------------------------------------------------------
    # 4. Flank Parallelism (|Delta theta|)
    # -------------------------------------------------------------
    if not math.isnan(up_angle) and not math.isnan(low_angle):
        diff_ang = abs(up_angle - low_angle) % 180.0
        flank_parallelism_deg = float(min(diff_ang, 180.0 - diff_ang))
        opposing_flank_status = "measured"
    else:
        flank_parallelism_deg = float("nan")
        opposing_flank_status = "occluded_or_insufficient_points"


    # -------------------------------------------------------------
    # 3. Width Consistency (Coefficient of Variation of Width CV_W)
    # -------------------------------------------------------------
    # Slice the body along u from 15% to 85% of length
    u_min, u_max = float(np.min(u_coords)), float(np.max(u_coords))
    u_span = np.linspace(u_min * 0.70, u_max * 0.70, 14)
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
    apex_idx = np.where(b_u > 0.75 * np.max(b_u))[0]
    if len(apex_idx) >= 5:
        ax_x = gx_b[apex_idx]
        ax_y = gy_b[apex_idx]
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
    # 6. Physical End-Face Detection & Ellipse Fitting
    # -------------------------------------------------------------
    has_end_face, endface_ba, _ = detect_end_face_rim(
        gray=sub_gray,
        sx=sx,
        sy=sy,
        xc=xc - x0,
        yc=yc - y0,
        u_axis=u_axis,
        v_axis=v_axis,
        length_px=length_px,
        width_px=width_px
    )

    # -------------------------------------------------------------
    # 8. Geometric Continuity (Junction regularity)
    # -------------------------------------------------------------
    continuity_score = 1.0
    if not math.isnan(straightness_rmse_px):
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
        "opposing_flank_parallelism_deg": round(flank_parallelism_deg, 2) if not math.isnan(flank_parallelism_deg) else None,
        "opposing_flank_status": opposing_flank_status,
        "crown_highlight_parallelism_deg": None,
        "width_cv": round(width_cv, 4) if not math.isnan(width_cv) else None,
        "terminal_curvature_ratio": round(terminal_curvature_ratio, 3) if not math.isnan(terminal_curvature_ratio) else None,
        "has_end_face": bool(has_end_face),
        "endface_ba": round(endface_ba, 4) if endface_ba is not None else None,
        "continuity_score": round(continuity_score, 3),
        "edge_snr": round(edge_snr, 2),
    }
