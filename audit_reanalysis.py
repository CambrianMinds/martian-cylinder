#!/usr/bin/env python3
"""
audit_reanalysis.py — corrected, audit-driven re-analysis (see audit.md, AUDIT_RESPONSE.md)
=========================================================================================
Recomputes, from the bundled pixels only:
  A. Cylinder physical length / aspect ratio with ONE consistent projection model
     (end-face ellipticity fixes axial foreshortening), propagated over the
     perturbation-sweep range of the ellipse fit and over the focus-range band.
  B. Rotation-invariant straightness (perpendicular TLS RMSE) for target AND the
     N = 20 control clasts through a single shared edge-extraction pipeline.
  C. Descriptive statistics and an empirical-rank comparison, with bootstrap SD
     intervals, WITHOUT Cantelli "p-values".

Usage:  python audit_reanalysis.py [--json data/audit_reanalysis.json]
"""
import argparse
import json
import math
import os
import sys

import numpy as np
from PIL import Image

import geometry_utils as gu

HERE = os.path.dirname(os.path.abspath(__file__))
IFOV = 7.4e-5
WINDOW = 20  # consecutive scan lines per straightness window (all ROIs >= 30 px)


def sobel(gray):
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], float) / 4.0
    ky = kx.T
    from numpy.lib.stride_tricks import sliding_window_view
    win = sliding_window_view(gray, (3, 3))
    Sx = np.zeros_like(gray)
    Sy = np.zeros_like(gray)
    Sx[1:-1, 1:-1] = np.einsum("ijkl,kl->ij", win, kx)
    Sy[1:-1, 1:-1] = np.einsum("ijkl,kl->ij", win, ky)
    return Sx, Sy, np.hypot(Sx, Sy)


def _subpix(g, i):
    if 1 <= i < len(g) - 1:
        d = g[i - 1] - 2 * g[i] + g[i + 1]
        if abs(d) > 1e-9:
            return i + 0.5 * (g[i - 1] - g[i + 1]) / d
    return float(i)


def common_edge_pipeline(G, roi, window=WINDOW):
    """Shared target/control extraction: strongest gradient peak per scan line.

    For both scan orientations (columns and rows) take, on every line of the ROI,
    the sub-pixel position of the maximum gradient magnitude, then report the
    straightest `window`-line run (perpendicular TLS RMSE).  No thresholds, no
    hand-picked sub-windows, no PCA pre-rotation; the better orientation wins.
    """
    x0, y0, x1, y1 = roi
    sub = G[y0:y1, x0:x1]
    best = None
    for orient in ("cols", "rows"):
        pts_x, pts_y = [], []
        if orient == "cols":
            for c in range(sub.shape[1]):
                col = sub[:, c]
                r = _subpix(col, int(np.argmax(col)))
                pts_x.append(x0 + c)
                pts_y.append(y0 + r)
        else:
            for r_ in range(sub.shape[0]):
                row = sub[r_, :]
                c = _subpix(row, int(np.argmax(row)))
                pts_x.append(x0 + c)
                pts_y.append(y0 + r_)
        w = gu.best_straight_window(pts_x, pts_y, window)
        if best is None or w["rmse_perp"] < best["rmse_perp"]:
            best = dict(w, orient=orient)
    return best


def analyse_length(crop_gray_rgb, circ_samples, rear_pts, front_center, axis_angle_deg, R_px):
    out = []
    ux, uy = math.cos(math.radians(axis_angle_deg)), math.sin(math.radians(axis_angle_deg))
    for ba in circ_samples:
        theta = gu.view_angle_from_face_ratio(ba)
        b = R_px * ba
        vx, vy = -uy, ux
        u_c = []
        for xp, yp in rear_pts:
            dx, dy = xp - front_center[0], yp - front_center[1]
            u, v = dx * ux + dy * uy, dx * vx + dy * vy
            if abs(v) < R_px:
                u_c.append(u + b * math.sqrt(1 - (v / R_px) ** 2))
        axis_2d = -float(np.mean(u_c))
        out.append((ba, theta, axis_2d, gu.length_from_projected_axis(axis_2d, ba)))
    return out


def sample_field(F, x, y):
    x0, y0 = int(math.floor(x)), int(math.floor(y))
    if x0 < 0 or y0 < 0 or x0 + 1 >= F.shape[1] or y0 + 1 >= F.shape[0]:
        return 0.0
    dx, dy = x - x0, y - y0
    return ((1 - dx) * (1 - dy) * F[y0, x0] + dx * (1 - dy) * F[y0, x0 + 1]
            + (1 - dx) * dy * F[y0 + 1, x0] + dx * dy * F[y0 + 1, x0 + 1])


def rim_points(gray, Sx, Sy, xc, yc, i_stop, k_mad):
    """Same radial-gradient rim search as reproduce_analysis.py (unchanged algorithm)."""
    r_samples = np.linspace(6.0, 28.0, 89)
    pts = []
    for deg in np.linspace(0.0, 360.0, 96, endpoint=False):
        ca, sa = math.cos(math.radians(deg)), math.sin(math.radians(deg))
        vals = []
        for r in r_samples:
            xs, ys = xc + r * ca, yc + r * sa
            g = sample_field(Sx, xs, ys) * ca + sample_field(Sy, xs, ys) * sa
            vals.append(g)
            if sample_field(gray, xs, ys) > i_stop and g < 0.0:
                break
        mi = int(np.argmax(vals))
        if 1 <= mi < len(vals) - 1:
            d = vals[mi - 1] - 2 * vals[mi] + vals[mi + 1]
            dl = 0.5 * (vals[mi - 1] - vals[mi + 1]) / d if abs(d) > 1e-5 else 0.0
            rp = r_samples[mi] + dl * (r_samples[1] - r_samples[0])
            pts.append((rp, xc + rp * ca, yc + rp * sa))
    rps = np.array([p[0] for p in pts])
    med = float(np.median(rps))
    mad = float(np.median(np.abs(rps - med)))
    keep = [p for p in pts if abs(p[0] - med) <= k_mad * mad]
    return np.array([p[1] for p in keep]), np.array([p[2] for p in keep])


def section_length(crop, fit_ellipse):
    sub = crop[240:360, 209:329].astype(float)
    gray = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
    Sx, Sy, G = sobel(gray)

    dark = gray[22:62, 38:78] < 75.0
    yy, xx = np.where(dark)
    xc0, yc0 = 38.0 + xx.mean(), 22.0 + yy.mean()

    # rear-terminus arc (unchanged landmark rule, y = 4..12)
    rear = []
    for y in range(4, 13):
        bx = max(range(14, 24), key=lambda x: G[y, x])
        rear.append((_subpix(G[y, :], bx), float(y)))

    # upper-generator direction (paper's gated extraction)
    xs_up, ys_up = [], []
    for x in range(28, 53):
        c = [y for y in range(2, 28) if Sy[y, x] > 15.0 and Sx[y, x] < -8.0]
        if c:
            by = max(c, key=lambda y: G[y, x])
            xs_up.append(x)
            ys_up.append(_subpix(G[:, x], by))
    gen_angle = gu.tls_line_fit(xs_up, ys_up)["angle_deg"]
    gated_rmse = gu.tls_line_fit(xs_up, ys_up)["rmse_perp"]

    rows = []
    for dx in (-1.0, 0.0, 1.0):
        for dy in (-1.0, 0.0, 1.0):
            for ist in (80.0, 85.0, 90.0):
                for km in (2.5, 2.6, 2.7):
                    X, Y = rim_points(gray, Sx, Sy, xc0 + dx, yc0 + dy, ist, km)
                    e = fit_ellipse(X, Y)
                    minor_dir = e["theta_deg"] % 180.0  # fitter returns minor-axis direction
                    rows.append((e, minor_dir))
    ba = np.array([e["circ_ratio"] for e, _ in rows])
    minor = np.array([m for _, m in rows])

    # Axis direction candidates (image plane, 0..180).  Cylinder axis must be parallel to the
    # ellipse MINOR axis if the end face is a circle perpendicular to the axis.
    res = {"generator_angle_deg": gen_angle, "gated_generator_rmse_perp_px": gated_rmse,
           "ellipse_minor_axis_deg_median": float(np.median(minor)),
           "ellipse_minor_axis_deg_range": [float(minor.min()), float(minor.max())],
           "ba_sweep": {"median": float(np.median(ba)), "min": float(ba.min()), "max": float(ba.max())}}
    d = abs(gen_angle - np.median(minor)) % 180.0
    res["generator_vs_minor_axis_mismatch_deg"] = float(min(d, 180.0 - d))

    # Length from each sweep member using the GENERATOR direction (an independent landmark) and
    # alternatively the ellipse minor axis.  Axis points from rear to front => +u toward front.
    s_perp = {r: r * IFOV * 1000.0 for r in (3.63, 3.957, 4.30)}
    for label, use_gen in (("generator_axis", True), ("ellipse_minor_axis", False)):
        L_px, A2d, th = [], [], []
        for (e, m), b in zip(rows, ba):
            ang = gen_angle if use_gen else m
            # choose sign so that rear points lie at negative u
            for sgn in (1.0, -1.0):
                a = math.radians(ang) + (0.0 if sgn > 0 else math.pi)
                ux, uy = math.cos(a), math.sin(a)
                R = e["major_2a"] / 2.0
                bb = R * b
                u_c = []
                for xp, yp in rear:
                    dx, dy = xp - e["xc"], yp - e["yc"]
                    u = dx * ux + dy * uy
                    v = -dx * uy + dy * ux
                    if abs(v) < R:
                        u_c.append(u + bb * math.sqrt(1 - (v / R) ** 2))
                if u_c and np.mean(u_c) < 0:
                    ax = -float(np.mean(u_c))
                    A2d.append(ax)
                    L_px.append(gu.length_from_projected_axis(ax, b))
                    th.append(gu.view_angle_from_face_ratio(b))
                    break
        L_px = np.array(L_px)
        res[label] = {
            "n": int(len(L_px)),
            "projected_axis_px_median": float(np.median(A2d)),
            "view_angle_deg_median": float(np.median(th)),
            "length_px": {"median": float(np.median(L_px)), "p05": float(np.percentile(L_px, 5)),
                          "p95": float(np.percentile(L_px, 95))},
            "length_mm_at_3.957m": {"median": float(np.median(L_px) * s_perp[3.957]),
                                    "p05": float(np.percentile(L_px, 5) * s_perp[3.957]),
                                    "p95": float(np.percentile(L_px, 95) * s_perp[3.957])},
            "length_mm_range_3.63_to_4.30m": [float(np.percentile(L_px, 5) * s_perp[3.63]),
                                               float(np.percentile(L_px, 95) * s_perp[4.30])],
        }
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    from reproduce_analysis import fit_ellipse_fitzgibbon

    crop = np.array(Image.open(os.path.join(HERE, "data", "crop_bottom_right.png")))
    gray_full = 0.299 * crop[:, :, 0] + 0.587 * crop[:, :, 1] + 0.114 * crop[:, :, 2]
    _, _, G = sobel(gray_full)
    rocks = json.load(open(os.path.join(HERE, "data", "control_rocks_distribution.json"), encoding="utf-8"))["rocks"]

    print("=" * 78)
    print(" AUDIT RE-ANALYSIS (geometry, straightness, descriptive statistics)")
    print("=" * 78)

    # ---------------- A. geometry ----------------
    A = section_length(crop, fit_ellipse_fitzgibbon)
    print("\n[A] Consistent end-face / axial projection (audit finding 2)")
    print(f"  face b/a sweep (81 configs): median {A['ba_sweep']['median']:.4f}, range [{A['ba_sweep']['min']:.4f}, {A['ba_sweep']['max']:.4f}]")
    print(f"  upper-generator direction     : {A['generator_angle_deg']:.2f} deg")
    print(f"  ellipse minor-axis direction  : {A['ellipse_minor_axis_deg_median']:.2f} deg (range {A['ellipse_minor_axis_deg_range'][0]:.1f}..{A['ellipse_minor_axis_deg_range'][1]:.1f})")
    print(f"  mismatch generator vs minor axis: {A['generator_vs_minor_axis_mismatch_deg']:.1f} deg  <-- a circular face normal to the axis requires ~0")
    for k in ("generator_axis", "ellipse_minor_axis"):
        r = A[k]
        print(f"  [{k}] n={r['n']}: view angle {r['view_angle_deg_median']:.1f} deg, projected axis {r['projected_axis_px_median']:.1f} px")
        print(f"      L = {r['length_px']['median']:.0f} px (5-95%: {r['length_px']['p05']:.0f}-{r['length_px']['p95']:.0f}) -> "
              f"{r['length_mm_at_3.957m']['median']:.1f} mm at 3.957 m; 5-95% x focus band: "
              f"{r['length_mm_range_3.63_to_4.30m'][0]:.0f}-{r['length_mm_range_3.63_to_4.30m'][1]:.0f} mm")

    # ---------------- B. common-pipeline straightness ----------------
    ctrl = [dict(id=r["id"], legacy_r2=r["r2_parallelism"], **common_edge_pipeline(G, r["crop_roi_xyxy"])) for r in rocks]
    cr = np.array([c["rmse_perp"] for c in ctrl])
    sx0, sy0 = 209, 240
    target_rois = {"tight (rows 242-262)": [sx0 + 26, sy0 + 2, sx0 + 56, sy0 + 22],
                   "wide (rows 242-270)": [sx0 + 26, sy0 + 2, sx0 + 56, sy0 + 30]}
    tgt = {k: common_edge_pipeline(G, v) for k, v in target_rois.items()}
    print("\n[B] Rotation-invariant straightness, ONE shared pipeline (audit finding 4)")
    print("    metric: perpendicular TLS RMSE (px) of the straightest %d-line run of the per-line strongest edge" % WINDOW)
    for c in sorted(ctrl, key=lambda c: c["rmse_perp"])[:5]:
        print(f"    straightest controls: {c['id']} rmse={c['rmse_perp']:.3f} px (legacy R2 = {c['legacy_r2']:.3f})")
    print(f"    controls: median {np.median(cr):.2f}, min {cr.min():.3f}, max {cr.max():.2f} px")
    for k, v in tgt.items():
        p = gu.empirical_rank_p(v["rmse_perp"], cr, higher_is_extreme=False)
        print(f"    target [{k}]: rmse={v['rmse_perp']:.3f} px, empirical rank p = {p:.4f}")
    print(f"    paper's hand-gated target pipeline (sign-gated, 25 cols; NOT applicable to controls): rmse_perp = {A['gated_generator_rmse_perp_px']:.3f} px")
    print("    => the shared pipeline does not lock onto the cylinder edge (inconclusive for the target), while control R01")
    print("       reaches a comparable perpendicular residual, so 'natural clasts lack straight edges' is not supported as stated.")

    # ---------------- C. descriptive statistics ----------------
    asp = np.array([r["aspect_ratio"] for r in rocks])
    lo, hi = gu.bootstrap_sd_ci(asp)
    print("\n[C] Descriptive statistics (audit finding 6) — NOT calibrated p-values")
    print(f"    control L/W: mean {asp.mean():.3f}, SD(ddof=1) {asp.std(ddof=1):.3f}, bootstrap 95% CI of SD [{lo:.3f}, {hi:.3f}]")
    print("    target-to-control z-scores are descriptive only: N=20, hand-selected controls, target chosen post hoc")

    out = {"geometry": A, "straightness_common_pipeline": {
        "window_lines": WINDOW, "controls": ctrl,
        "target": {k: dict(v) for k, v in tgt.items()}},
        "aspect_sd_bootstrap_ci": [lo, hi]}
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, default=float)
        print(f"\n  wrote {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
