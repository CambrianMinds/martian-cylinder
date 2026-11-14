"""
Step 2: Intrinsic & Extrinsic Camera Geometry (CAHVOR & CAHV) and Illumination Modeling
Independent Geometric Investigation - Curiosity Sol 3556 (3556MR1025170721700585C00)
"""

import os
import json
import numpy as np

OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Primary parameters extracted directly from 3556MR1025170721700585C00_DRXX.LBL and DRLX.LBL
CAHVOR_DRXX = {
    "C": np.array([6.840714e-01, 6.478303e-01, -1.926771e+00]),
    "A": np.array([-2.572619e-03, 8.584127e-01, 5.129360e-01]),
    "H": np.array([-1.337762e+04, 5.174538e+02, 4.305226e+02]),
    "V": np.array([1.026375e+02, -6.412962e+03, 1.174322e+04]),
    "O": np.array([4.395304e-03, 8.532572e-01, 5.214551e-01]),
    "R": np.array([-1.060000e-04, 1.436779e+00, -6.858840e-01]),
    "width": 1328,
    "height": 1184
}

CAHV_DRLX = {
    "C": np.array([6.851803e-01, 5.712697e-01, -1.973070e+00]),
    "A": np.array([-1.274819e-03, 8.552468e-01, 5.182193e-01]),
    "H": np.array([-1.359430e+04, 5.222195e+02, 4.042223e+02]),
    "V": np.array([7.433327e+01, -6.539554e+03, 1.193167e+04]),
    "width": 1323,
    "height": 1180
}

ROVER_TO_SITE = {
    "origin_offset": np.array([-135.052963, 86.146790, -20.508987]),
    # Scalar-first quaternion (q0, q1, q2, q3) rotating ROVER_NAV_FRAME -> SITE_FRAME
    "quaternion": np.array([0.3101999, -0.1235113, -0.0378476, 0.9418538])
}

DERIVED_PARMS = {
    "min_focus_distance_m": 3.6,
    "best_focus_distance_m": 3.957,
    "max_focus_distance_m": 4.4,
    "fixed_instrument_azimuth_deg": 227.7412,
    "fixed_instrument_elevation_deg": -22.0047,
    "solar_azimuth_deg": 186.8169,
    "solar_elevation_deg": 69.8224,
    "horizontal_fov_deg": 5.5921,
    "vertical_fov_deg": 4.9866,
    "focus_position_count": 2705
}

def quat_to_rotmat(q):
    """Convert scalar-first quaternion (w, x, y, z) to 3x3 rotation matrix."""
    w, x, y, z = q / np.linalg.norm(q)
    return np.array([
        [1 - 2*(y*y + z*z), 2*(x*y - w*z),     2*(x*z + w*y)],
        [2*(x*y + w*z),     1 - 2*(x*x + z*z), 2*(y*z - w*x)],
        [2*(x*z - w*y),     2*(y*z + w*x),     1 - 2*(x*x + y*y)]
    ])

def extract_cahv_intrinsics(model):
    A = model["A"] / np.linalg.norm(model["A"])
    H = model["H"]
    V = model["V"]
    hc = float(np.dot(A, H))
    vc = float(np.dot(A, V))
    hs = float(np.linalg.norm(np.cross(A, H)))
    vs = float(np.linalg.norm(np.cross(A, V)))
    h_prime = (H - hc * A) / hs
    v_prime = (V - vc * A) / vs
    # Check orthogonality defect angle between H' and V'
    cos_theta = float(np.clip(np.dot(h_prime, v_prime), -1.0, 1.0))
    skew_deg = float(np.degrees(np.arccos(cos_theta)) - 90.0)
    hfov_deg = float(2.0 * np.degrees(np.arctan((model["width"] / 2.0) / hs)))
    vfov_deg = float(2.0 * np.degrees(np.arctan((model["height"] / 2.0) / vs)))
    ifov_h_urad = float(1e6 / hs)
    ifov_v_urad = float(1e6 / vs)
    return {
        "hc_px": hc,
        "vc_px": vc,
        "hs_px": hs,
        "vs_px": vs,
        "aspect_ratio_vs_over_hs": vs / hs,
        "skew_deg": skew_deg,
        "computed_hfov_deg": hfov_deg,
        "computed_vfov_deg": vfov_deg,
        "ifov_h_urad_per_px": ifov_h_urad,
        "ifov_v_urad_per_px": ifov_v_urad,
        "h_unit": h_prime,
        "v_unit": v_prime,
        "a_unit": A
    }

def cahv_pixel_to_ray(x, y, model):
    """
    Exact inverse projection of pixel (x, y) to unit ray direction u in ROVER_NAV_FRAME
    for a linear CAHV camera model.
    By definition:
      x = (p . H) / (p . A)  =>  p . (H - x A) = 0
      y = (p . V) / (p . A)  =>  p . (V - y A) = 0
    Therefore ray vector p is parallel to (V - y A) x (H - x A), oriented such that p . A > 0.
    """
    A, H, V = model["A"], model["H"], model["V"]
    ray = np.cross(V - y * A, H - x * A)
    if np.dot(ray, A) < 0:
        ray = -ray
    return ray / np.linalg.norm(ray)

def cahvor_project_3d_to_2d(P, model):
    """
    Forward projection of 3D point P (in ROVER_NAV_FRAME) to 2D pixel (x, y)
    using Gennery (1992) CAHVOR equations.
    """
    C, A, H, V, O, R = model["C"], model["A"], model["H"], model["V"], model["O"], model["R"]
    p = P - C
    omega = np.dot(p, O)
    p_prime = p / omega
    lambda_vec = p_prime - O
    tau = np.dot(lambda_vec, lambda_vec)
    mu = R[0] + R[1] * tau + R[2] * (tau ** 2)
    p_corr = p + mu * (p - omega * O)
    denom = np.dot(p_corr, A)
    x = np.dot(p_corr, H) / denom
    y = np.dot(p_corr, V) / denom
    return np.array([x, y])

def cahvor_pixel_to_ray(x, y, model, tol=1e-12, max_iter=30):
    """
    Iterative numerical inversion of CAHVOR pixel (x, y) to unit ray in ROVER_NAV_FRAME.
    Starts from linear CAHV ray and solves cahvor_project_3d_to_2d(C + u, model) = (x, y).
    """
    u = cahv_pixel_to_ray(x, y, model)
    C = model["C"]
    # Refine u using Gauss-Newton on two tangent coordinates
    intr = extract_cahv_intrinsics(model)
    e1, e2, e3 = intr["h_unit"], intr["v_unit"], intr["a_unit"]
    alpha = np.dot(u, e1) / np.dot(u, e3)
    beta = np.dot(u, e2) / np.dot(u, e3)

    eps = 1e-7
    for _ in range(max_iter):
        u_curr = e3 + alpha * e1 + beta * e2
        u_curr /= np.linalg.norm(u_curr)
        xy_pred = cahvor_project_3d_to_2d(C + u_curr, model)
        res = np.array([x, y]) - xy_pred
        if np.linalg.norm(res) < tol:
            break
        # Jacobian via finite differences
        u_da = e3 + (alpha + eps) * e1 + beta * e2
        u_da /= np.linalg.norm(u_da)
        xy_da = cahvor_project_3d_to_2d(C + u_da, model)

        u_db = e3 + alpha * e1 + (beta + eps) * e2
        u_db /= np.linalg.norm(u_db)
        xy_db = cahvor_project_3d_to_2d(C + u_db, model)

        J = np.column_stack([(xy_da - xy_pred) / eps, (xy_db - xy_pred) / eps])
        delta = np.linalg.solve(J, res)
        alpha += delta[0]
        beta += delta[1]

    u_final = e3 + alpha * e1 + beta * e2
    return u_final / np.linalg.norm(u_final)

def az_el_to_site_vec(az_deg, el_deg):
    """
    Convert SITE_FRAME azimuth (clockwise from +X North) and elevation (up from horizontal, i.e. -Z)
    to a unit 3D vector in SITE_FRAME (+X North, +Y East, +Z Down).
    """
    az = np.radians(az_deg)
    el = np.radians(el_deg)
    vx = np.cos(el) * np.cos(az)
    vy = np.cos(el) * np.sin(az)
    vz = -np.sin(el)  # Positive elevation is UP, whereas +Z is DOWN
    return np.array([vx, vy, vz])

def site_vec_to_az_el(v):
    v = v / np.linalg.norm(v)
    el_deg = float(np.degrees(np.arcsin(-v[2])))
    az_deg = float(np.degrees(np.arctan2(v[1], v[0])) % 360.0)
    return az_deg, el_deg

def main():
    R_rov_to_site = quat_to_rotmat(ROVER_TO_SITE["quaternion"])
    intr_drxx = extract_cahv_intrinsics(CAHVOR_DRXX)
    intr_drlx = extract_cahv_intrinsics(CAHV_DRLX)

    # Verify optical axis A in SITE_FRAME against FIXED_INSTRUMENT_AZIMUTH / ELEVATION
    A_site_drxx = R_rov_to_site @ intr_drxx["a_unit"]
    az_drxx, el_drxx = site_vec_to_az_el(A_site_drxx)

    A_site_drlx = R_rov_to_site @ intr_drlx["a_unit"]
    az_drlx, el_drlx = site_vec_to_az_el(A_site_drlx)

    # Target object approximate center in DRXX: x = 1061, y = 980
    tx_drxx, ty_drxx = 1061.0, 980.0
    ray_target_rov = cahvor_pixel_to_ray(tx_drxx, ty_drxx, CAHVOR_DRXX)
    ray_target_site = R_rov_to_site @ ray_target_rov
    target_az_site, target_el_site = site_vec_to_az_el(ray_target_site)

    # Angle between target ray and optical axis A (and optical distortion axis O)
    off_axis_angle_A_deg = float(np.degrees(np.arccos(np.clip(np.dot(ray_target_rov, intr_drxx["a_unit"]), -1.0, 1.0))))
    O_unit = CAHVOR_DRXX["O"] / np.linalg.norm(CAHVOR_DRXX["O"])
    off_axis_angle_O_deg = float(np.degrees(np.arccos(np.clip(np.dot(ray_target_rov, O_unit), -1.0, 1.0))))

    # Measure local Jacobian / distortion of CAHVOR at the target location (tx_drxx, ty_drxx)
    C = CAHVOR_DRXX["C"]
    e1, e2, e3 = intr_drxx["h_unit"], intr_drxx["v_unit"], intr_drxx["a_unit"]
    # Build orthonormal local ray basis around ray_target_rov
    r0 = ray_target_rov
    t_h = e1 - np.dot(e1, r0) * r0
    t_h /= np.linalg.norm(t_h)
    t_v = np.cross(r0, t_h)
    t_v /= np.linalg.norm(t_v)

    eps_ang = 1e-5  # 10 urad angular step
    xy_0 = cahvor_project_3d_to_2d(C + r0, CAHVOR_DRXX)
    xy_h = cahvor_project_3d_to_2d(C + (r0 + eps_ang * t_h), CAHVOR_DRXX)
    xy_v = cahvor_project_3d_to_2d(C + (r0 + eps_ang * t_v), CAHVOR_DRXX)
    J_ang_to_px = np.column_stack([(xy_h - xy_0) / eps_ang, (xy_v - xy_0) / eps_ang])
    u_svd, s_svd, vt_svd = np.linalg.svd(J_ang_to_px)
    anisotropy_ratio = float(s_svd[0] / s_svd[1])
    mean_local_scale_px_per_rad = float(np.sqrt(s_svd[0] * s_svd[1]))
    mean_local_ifov_urad_per_px = float(1e6 / mean_local_scale_px_per_rad)

    # Solar vector in SITE_FRAME, ROVER_NAV_FRAME, and Camera Image Plane (h_unit, v_unit, a_unit)
    sun_to_source_site = az_el_to_site_vec(DERIVED_PARMS["solar_azimuth_deg"], DERIVED_PARMS["solar_elevation_deg"])
    sun_to_source_rov = R_rov_to_site.T @ sun_to_source_site
    # Direction of sunlight propagation (from Sun to surface) is -sun_to_source
    sun_ray_site = -sun_to_source_site
    sun_ray_rov = -sun_to_source_rov

    # Project vector towards Sun onto camera (h_unit, v_unit, a_unit) basis:
    # Note: +h_unit is +x (right in image), +v_unit is +y (down in image), +a_unit is into the scene (away from camera)
    sun_cam_x = float(np.dot(sun_to_source_rov, e1))
    sun_cam_y = float(np.dot(sun_to_source_rov, e2))
    sun_cam_z = float(np.dot(sun_to_source_rov, e3))
    # 2D image-plane direction of incoming illumination (from top/left/etc. in image coordinates)
    sun_img_az_deg = float(np.degrees(np.arctan2(sun_cam_y, sun_cam_x)))  # angle in (x, y) where 0=+x(right), -90=-y(up), +90=+y(down)
    shadow_img_az_deg = float(np.degrees(np.arctan2(-sun_cam_y, -sun_cam_x)))
    phase_angle_deg = float(np.degrees(np.arccos(np.clip(np.dot(-ray_target_rov, sun_to_source_rov), -1.0, 1.0))))

    # Intersect target ray with horizontal ground plane in ROVER_NAV_FRAME (Z_nav = 0) and SITE_FRAME flat ground
    # In ROVER_NAV_FRAME, rover wheels rest near Z_nav = 0. Camera C_z = -1.926771 m.
    C_site = ROVER_TO_SITE["origin_offset"] + R_rov_to_site @ C
    # Distance if intersecting Z_nav = 0 plane:
    dist_znav0 = float(-C[2] / ray_target_rov[2]) if ray_target_rov[2] > 0 else None
    # Distance if intersecting horizontal plane at Rover origin in SITE_FRAME (Z_site = ROVER_TO_SITE["origin_offset"][2]):
    dz_site_to_rover_origin = ROVER_TO_SITE["origin_offset"][2] - C_site[2]
    dist_zsite0 = float(dz_site_to_rover_origin / ray_target_site[2]) if ray_target_site[2] > 0 else None

    # Scale in mm/pixel across focus range [3.6 m, 3.957 m, 4.4 m] and ground-intersection ranges
    scales = {}
    for label, d_m in [
        ("min_focus_3.600m", 3.600),
        ("best_focus_3.957m", 3.957),
        ("max_focus_4.400m", 4.400),
        ("horiz_plane_zsite_rover_origin", dist_zsite0),
        ("rover_nav_plane_z0", dist_znav0)
    ]:
        if d_m is not None:
            scales[label] = {
                "distance_m": round(d_m, 4),
                "mm_per_pixel_at_target": round(d_m * 1000.0 / mean_local_scale_px_per_rad, 5),
                "mm_per_pixel_paraxial": round(d_m * 1000.0 / intr_drxx["hs_px"], 5)
            }

    # Rover tilt in SITE_FRAME:
    rover_down_site = R_rov_to_site @ np.array([0.0, 0.0, 1.0])
    rover_tilt_deg = float(np.degrees(np.arccos(np.clip(rover_down_site[2], -1.0, 1.0))))

    results = {
        "intrinsics_drxx_cahvor": {k: v for k, v in intr_drxx.items() if not isinstance(v, np.ndarray)},
        "intrinsics_drlx_cahv": {k: v for k, v in intr_drlx.items() if not isinstance(v, np.ndarray)},
        "extrinsics_verification": {
            "pds_fixed_instrument_azimuth_deg": DERIVED_PARMS["fixed_instrument_azimuth_deg"],
            "computed_drxx_axis_azimuth_deg": round(az_drxx, 4),
            "computed_drlx_axis_azimuth_deg": round(az_drlx, 4),
            "pds_fixed_instrument_elevation_deg": DERIVED_PARMS["fixed_instrument_elevation_deg"],
            "computed_drxx_axis_elevation_deg": round(el_drxx, 4),
            "computed_drlx_axis_elevation_deg": round(el_drlx, 4),
            "rover_tilt_deg_in_site_frame": round(rover_tilt_deg, 4),
            "camera_center_rover_nav_m": C.tolist(),
            "camera_center_site_m": C_site.tolist(),
            "camera_height_above_rover_origin_site_m": float(ROVER_TO_SITE["origin_offset"][2] - C_site[2])
        },
        "target_viewing_geometry": {
            "target_pixel_drxx": [tx_drxx, ty_drxx],
            "target_ray_rover_nav": ray_target_rov.tolist(),
            "target_ray_site": ray_target_site.tolist(),
            "target_azimuth_site_deg": round(target_az_site, 4),
            "target_elevation_site_deg": round(target_el_site, 4),
            "grazing_angle_wrt_horizontal_deg": round(-target_el_site, 4),
            "off_axis_angle_from_A_deg": round(off_axis_angle_A_deg, 4),
            "off_axis_angle_from_O_deg": round(off_axis_angle_O_deg, 4),
            "local_jacobian_singular_values_px_per_rad": s_svd.tolist(),
            "local_anisotropy_ratio_s1_over_s2": round(anisotropy_ratio, 6),
            "local_anisotropy_percent": round((anisotropy_ratio - 1.0) * 100.0, 4),
            "mean_local_scale_px_per_rad": round(mean_local_scale_px_per_rad, 3),
            "mean_local_ifov_urad_per_px": round(mean_local_ifov_urad_per_px, 3)
        },
        "solar_illumination_geometry": {
            "solar_azimuth_site_deg": DERIVED_PARMS["solar_azimuth_deg"],
            "solar_elevation_site_deg": DERIVED_PARMS["solar_elevation_deg"],
            "sun_direction_site": sun_to_source_site.tolist(),
            "sun_direction_rover_nav": sun_to_source_rov.tolist(),
            "sun_direction_camera_xyz": [round(sun_cam_x, 5), round(sun_cam_y, 5), round(sun_cam_z, 5)],
            "sun_direction_image_plane_angle_deg": round(sun_img_az_deg, 3),
            "shadow_cast_image_plane_angle_deg": round(shadow_img_az_deg, 3),
            "solar_phase_angle_at_target_deg": round(phase_angle_deg, 3)
        },
        "distance_and_spatial_scale_bounds": scales
    }

    with open(os.path.join(OUT_DIR, "step2_camera_geometry.json"), "w") as f:
        json.dump(results, f, indent=2)

    print("Camera Geometry Summary:")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()

