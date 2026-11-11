"""
geometry_utils.py — rotation-invariant measurement and projection helpers
=========================================================================
Added in response to the independent audit (audit.md).  Everything here is a
small, dependency-light (numpy only) function with an analytically known answer
so that it can be unit-tested against independently derived values
(tests/test_geometry_utils.py).
"""

import math

import numpy as np


# ----------------------------------------------------------------------
# Audit finding 2 — end-face circularity vs axial foreshortening
# ----------------------------------------------------------------------
def view_angle_from_face_ratio(b_over_a: float) -> float:
    """Angle theta (deg) between cylinder axis (= end-face normal) and line of sight.

    Orthographic projection of a circular face: b/a = |cos(theta)|.
    """
    if not 0.0 < b_over_a <= 1.0:
        raise ValueError("b/a must lie in (0, 1]")
    return math.degrees(math.acos(b_over_a))


def axial_deforeshortening_factor(b_over_a: float) -> float:
    """Factor 1/sin(theta) that converts projected axis length to true axis length.

    The face normal IS the cylinder axis, so the face ellipticity fixes both the
    cap foreshortening (cos theta) and the axial foreshortening (sin theta).
    """
    theta = math.radians(view_angle_from_face_ratio(b_over_a))
    return 1.0 / math.sin(theta)


def project_cylinder_orthographic(length: float, radius: float, theta_deg: float) -> dict:
    """Forward model: image-plane extents of a right circular cylinder.

    theta is the angle between the axis and the line of sight.
    Returns the projected centre-to-centre axis length, cap semi-axes, and the
    apex-to-apex silhouette length along the projected axis.
    """
    th = math.radians(theta_deg)
    axis_2d = length * math.sin(th)
    b = radius * abs(math.cos(th))
    return {
        "axis_2d": axis_2d,
        "cap_a": radius,
        "cap_b": b,
        "b_over_a": b / radius,
        "silhouette_2d": axis_2d + 2.0 * b,
    }


def length_from_projected_axis(axis_2d: float, b_over_a: float) -> float:
    """True axis length from projected centre-to-centre separation and face ellipticity."""
    return axis_2d * axial_deforeshortening_factor(b_over_a)


def length_from_silhouette(silhouette_2d: float, radius: float, b_over_a: float) -> float:
    """True axis length from the apex-to-apex silhouette extent (subtracts both cap semi-minors)."""
    axis_2d = silhouette_2d - 2.0 * radius * b_over_a
    return length_from_projected_axis(axis_2d, b_over_a)


def perspective_radius_ratio(length_mm: float, range_mm: float, theta_deg: float) -> float:
    """Pinhole rear/front cap radius ratio for a cylinder centred at range_mm."""
    dz = length_mm * abs(math.cos(math.radians(theta_deg)))
    return (range_mm - dz / 2.0) / (range_mm + dz / 2.0)


# ----------------------------------------------------------------------
# Audit finding 4 — rotation-invariant straightness
# ----------------------------------------------------------------------
def tls_line_fit(x, y) -> dict:
    """Orthogonal (total) least-squares line through points.

    Returns centroid, unit direction, angle (deg, modulo 180), signed perpendicular
    residuals and their RMSE.  Invariant to rotation/translation of the points.
    """
    pts = np.column_stack([np.asarray(x, float), np.asarray(y, float)])
    c = pts.mean(axis=0)
    q = pts - c
    # principal direction = right-singular vector with largest singular value
    _, _, vt = np.linalg.svd(q, full_matrices=False)
    d = vt[0]
    n = np.array([-d[1], d[0]])
    resid = q @ n
    return {
        "centroid": c,
        "direction": d,
        "angle_deg": math.degrees(math.atan2(d[1], d[0])) % 180.0,
        "residuals": resid,
        "rmse_perp": float(math.sqrt(np.mean(resid ** 2))),
        "extent": float(np.ptp(q @ d)),
    }


def normalized_straightness(x, y) -> float:
    """Perpendicular RMSE divided by feature extent (dimensionless, rotation-invariant).

    0 = perfectly straight.  Lower is straighter.
    """
    fit = tls_line_fit(x, y)
    return fit["rmse_perp"] / max(fit["extent"], 1e-9)


def best_straight_window(x, y, window: int) -> dict:
    """Smallest perpendicular RMSE over every run of `window` consecutive ordered points.

    A deliberately generous summary for natural edges: it grants each edge its
    straightest sub-segment of fixed length.
    """
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    n = len(x)
    if n < window or window < 3:
        return {"rmse_perp": float("nan"), "start": -1, "extent": 0.0}
    best = None
    for s in range(0, n - window + 1):
        f = tls_line_fit(x[s : s + window], y[s : s + window])
        if best is None or f["rmse_perp"] < best["rmse_perp"]:
            best = {"rmse_perp": f["rmse_perp"], "start": s, "extent": f["extent"], "angle_deg": f["angle_deg"]}
    return best


def r2_ordinary(x, y) -> float:
    """Ordinary y-on-x regression R^2 (NOT rotation invariant; kept to demonstrate the defect)."""
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    p = np.polyfit(x, y, 1)
    ss_res = np.sum((y - np.polyval(p, x)) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    return float(1.0 - ss_res / ss_tot) if ss_tot > 0 else 0.0


def rotate_points(x, y, deg: float):
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    x = np.asarray(x, float)
    y = np.asarray(y, float)
    return c * x - s * y, s * x + c * y


# ----------------------------------------------------------------------
# Audit finding 6 — descriptive vs inferential statistics
# ----------------------------------------------------------------------
def empirical_rank_p(target: float, controls, higher_is_extreme: bool = True) -> float:
    """(1 + #controls at least as extreme) / (N + 1): the smallest attainable value is 1/(N+1)."""
    c = np.asarray(controls, float)
    k = int(np.sum(c >= target)) if higher_is_extreme else int(np.sum(c <= target))
    return (k + 1) / (len(c) + 1)


def bootstrap_sd_ci(values, n_boot: int = 5000, seed: int = 12345, alpha: float = 0.05):
    """Percentile bootstrap CI for the sample SD (shows how weak a z-score from N=20 is)."""
    rng = np.random.default_rng(seed)
    v = np.asarray(values, float)
    sds = np.array([np.std(rng.choice(v, size=len(v), replace=True), ddof=1) for _ in range(n_boot)])
    return float(np.percentile(sds, 100 * alpha / 2)), float(np.percentile(sds, 100 * (1 - alpha / 2)))

