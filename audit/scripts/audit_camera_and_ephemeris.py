"""
Audit Camera Geometry, Local Scale, and Solar Ephemeris
Part of the Argon Red-Team Audit of martian-cylinder.
Independently verifies:
1. CAHVOR and CAHV model projections & ray-tracing
2. Local perspective Jacobian, IFOV, and distortion anisotropy at target
3. SITE_FRAME extrinsics & solar ephemeris
4. Projected 2D shadow vector direction (paraxial camera basis vs local raycast)
5. Metric pixel scales across slant range scenarios
"""

import os
import json
import numpy as np

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def quat_to_rotmat(q):
    q0, q1, q2, q3 = q
    return np.array([
        [1 - 2*(q2**2 + q3**2), 2*(q1*q2 - q0*q3),   2*(q1*q3 + q0*q2)],
        [2*(q1*q2 + q0*q3),   1 - 2*(q1**2 + q3**2), 2*(q2*q3 - q0*q1)],
        [2*(q1*q3 - q0*q2),   2*(q2*q3 + q0*q1),   1 - 2*(q1**2 + q2**2)]
    ], dtype=np.float64)

def cahv_intrinsics(A, H, V):
    hc = float(np.dot(A, H))
    vc = float(np.dot(A, V))
    hs = float(np.linalg.norm(np.cross(A, H)))
    vs = float(np.linalg.norm(np.cross(A, V)))
    return hc, vc, hs, vs

def cahvor_project(P, C, A, H, V, O, R):
    p = P - C
    omega = np.dot(p, O)
    lam = p / omega - O
    tau = np.dot(lam, lam)
    mu = R[0] + R[1]*tau + R[2]*(tau**2)
    p_corr = p + mu * (p - omega * O)
    x = np.dot(p_corr, H) / np.dot(p_corr, A)
    y = np.dot(p_corr, V) / np.dot(p_corr, A)
    return np.array([x, y])

def cahvor_pixel_to_ray(x, y, C, A, H, V, O, R, tol=1e-12, max_iter=30):
    r = np.cross(V - y*A, H - x*A)
    if np.dot(r, A) < 0:
        r = -r
    u = r / np.linalg.norm(r)
    for _ in range(max_iter):
        P_test = C + u
        pred = cahvor_project(P_test, C, A, H, V, O, R)
        err = np.array([x, y]) - pred
        if np.linalg.norm(err) < tol:
            break
        eps = 1e-7
        e1 = np.cross(A, np.array([1, 0, 0]))
        if np.linalg.norm(e1) < 0.1:
            e1 = np.cross(A, np.array([0, 1, 0]))
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(A, e1)
        e2 /= np.linalg.norm(e2)
        
        p1 = cahvor_project(C + u + eps*e1, C, A, H, V, O, R)
        p2 = cahvor_project(C + u + eps*e2, C, A, H, V, O, R)
        J = np.column_stack([(p1 - pred)/eps, (p2 - pred)/eps])
        d_alpha = np.linalg.lstsq(J, err, rcond=None)[0]
        u = u + d_alpha[0]*e1 + d_alpha[1]*e2
        u /= np.linalg.norm(u)
    return u

def main():
    print("=== AUDITING CAMERA GEOMETRY, LOCAL SCALE & SOLAR EPHEMERIS ===")
    
    # 1. PDS Vectors for DRXX (CAHVOR) and DRLX (CAHV)
    C_drxx = np.array([6.840714e-01, 6.478303e-01, -1.926771e+00])
    A_drxx = np.array([-2.572619e-03, 8.584127e-01, 5.129360e-01])
    H_drxx = np.array([-1.337762e+04, 5.174538e+02, 4.305226e+02])
    V_drxx = np.array([1.026375e+02, -6.412962e+03, 1.174322e+04])
    O_drxx = np.array([4.395304e-03, 8.532572e-01, 5.214551e-01])
    R_drxx = np.array([-1.060000e-04, 1.436779e+00, -6.858840e-01])

    C_drlx = np.array([6.851803e-01, 5.712697e-01, -1.973070e+00])
    A_drlx = np.array([-1.274819e-03, 8.552468e-01, 5.182193e-01])
    H_drlx = np.array([-1.359430e+04, 5.222195e+02, 4.042223e+02])
    V_drlx = np.array([7.433327e+01, -6.539554e+03, 1.193167e+04])

    q_site = np.array([0.3101999, -0.1235113, -0.0378476, 0.9418538])
    R_site = quat_to_rotmat(q_site)

    hc_xx, vc_xx, hs_xx, vs_xx = cahv_intrinsics(A_drxx, H_drxx, V_drxx)
    hc_lx, vc_lx, hs_lx, vs_lx = cahv_intrinsics(A_drlx, H_drlx, V_drlx)

    print("\n1. Camera Intrinsics:")
    print(f"  DRXX Paraxial: hc = {hc_xx:.2f} px, vc = {vc_xx:.2f} px, hs = {hs_xx:.2f} px/rad, vs = {vs_xx:.2f} px/rad")
    print(f"  DRLX Pinhole:  hc = {hc_lx:.2f} px, vc = {vc_lx:.2f} px, hs = {hs_lx:.2f} px/rad, vs = {vs_lx:.2f} px/rad")
    print(f"  DRLX Aspect Ratio hs/vs: {hs_lx/vs_lx:.7f} (exact square pixels)")

    # 2. Local Jacobian at Target Centroid (1061, 980) in DRXX
    x0, y0 = 1061.0, 980.0
    u_target = cahvor_pixel_to_ray(x0, y0, C_drxx, A_drxx, H_drxx, V_drxx, O_drxx, R_drxx)
    off_axis_A = float(np.degrees(np.arccos(np.clip(np.dot(u_target, A_drxx), -1, 1))))
    off_axis_O = float(np.degrees(np.arccos(np.clip(np.dot(u_target, O_drxx), -1, 1))))
    
    e_h = np.cross(A_drxx, np.array([0, 0, 1]))
    e_h /= np.linalg.norm(e_h)
    e_v = np.cross(u_target, e_h)
    e_v /= np.linalg.norm(e_v)
    e_h = np.cross(e_v, u_target)
    e_h /= np.linalg.norm(e_h)

    d_theta = 1e-6
    p_h = cahvor_project(C_drxx + u_target + d_theta*e_h, C_drxx, A_drxx, H_drxx, V_drxx, O_drxx, R_drxx)
    p_v = cahvor_project(C_drxx + u_target + d_theta*e_v, C_drxx, A_drxx, H_drxx, V_drxx, O_drxx, R_drxx)
    J = np.column_stack([(p_h - np.array([x0, y0]))/d_theta, (p_v - np.array([x0, y0]))/d_theta])
    
    U, S, Vt = np.linalg.svd(J)
    sigma1, sigma2 = float(S[0]), float(S[1])
    f_local = float(np.sqrt(sigma1 * sigma2))
    ifov_urad = float((1.0 / f_local) * 1e6)
    anisotropy_pct = float((sigma1 / sigma2 - 1.0) * 100.0)

    print("\n2. Target (1061, 980) Local Scale & Distortion:")
    print(f"  Off-axis angle wrt A: {off_axis_A:.4f}°")
    print(f"  Off-axis angle wrt O: {off_axis_O:.4f}°")
    print(f"  Jacobian Singular Values: sigma1 = {sigma1:.2f} px/rad, sigma2 = {sigma2:.2f} px/rad")
    print(f"  Geometric Mean Focal Scale: f_local = {f_local:.2f} px/rad")
    print(f"  Local IFOV: {ifov_urad:.3f} µrad/px (Stored: 74.304 µrad/px, Match: {abs(ifov_urad - 74.304) < 0.01})")
    print(f"  Distortion Anisotropy: {anisotropy_pct:.4f}% (Stored: 0.5948%, Match: {abs(anisotropy_pct - 0.5948) < 0.01})")

    # 3. Solar Ephemeris & Shadow Vector
    sol_az = 186.8169
    sol_el = 69.8224
    s_site = np.array([
        np.cos(np.radians(sol_el)) * np.cos(np.radians(sol_az)),
        np.cos(np.radians(sol_el)) * np.sin(np.radians(sol_az)),
        -np.sin(np.radians(sol_el))
    ])
    s_rov = np.dot(R_site.T, s_site)

    # A. Paraxial Camera Basis Projection (as implemented in Step 2):
    h_unit = (H_drxx - hc_xx * A_drxx) / hs_xx
    v_unit = (V_drxx - vc_xx * A_drxx) / vs_xx
    sun_cam_x = float(np.dot(s_rov, h_unit))
    sun_cam_y = float(np.dot(s_rov, v_unit))
    shadow_paraxial_deg = float(np.degrees(np.arctan2(-sun_cam_y, -sun_cam_x)))
    shadow_paraxial_slope = float(-sun_cam_y / -sun_cam_x)

    # B. Target Local CAHVOR Ray Projection:
    P_base = C_drxx + u_target * 3.957
    P_shadow = P_base - s_rov * 0.1
    p0 = cahvor_project(P_base, C_drxx, A_drxx, H_drxx, V_drxx, O_drxx, R_drxx)
    p_s = cahvor_project(P_shadow, C_drxx, A_drxx, H_drxx, V_drxx, O_drxx, R_drxx)
    dx_s = p_s[0] - p0[0]
    dy_s = p_s[1] - p0[1]
    theta_shadow_local = float(np.degrees(np.arctan2(dy_s, dx_s)))
    shadow_local_slope = float(dy_s / dx_s)

    print("\n3. Solar Ephemeris & Shadow Vector:")
    print(f"  Solar Elevation: {sol_el:.4f}°, Azimuth: {sol_az:.4f}°")
    print(f"  Paraxial Camera Basis Angle: {shadow_paraxial_deg:.4f}° (slope: {shadow_paraxial_slope:.4f})")
    print(f"  Local CAHVOR Raycast Angle:  {theta_shadow_local:.4f}° (slope: {shadow_local_slope:.4f})")
    print(f"  Stored Value in Repo:        +63.429° (slope 2.000)")
    print(f"  Match with Paraxial Basis:   {abs(shadow_paraxial_deg - 63.429) < 0.01} (Delta = {shadow_paraxial_deg - 63.429:.5f}°)")

    # 4. Metric Scales across Range Scenarios
    scenarios = [
        ("ROVER_NAV_FRAME Z=0 Plane", 3.5539),
        ("Minimum Autofocus Bound", 3.6000),
        ("Best Focus Distance (Nominal)", 3.9570),
        ("Maximum Autofocus Bound", 4.4000),
        ("SITE_FRAME Horizontal Plane", 5.1764)
    ]
    print("\n4. Metric Pixel Scale across Range Scenarios:")
    for name, D in scenarios:
        scale_mm_px = (D * 1000.0) / f_local
        w_chord_mm = 35.54 * scale_mm_px
        diam_mm = 39.47 * scale_mm_px
        print(f"  {name:<32} (D = {D:.4f} m): scale = {scale_mm_px:.5f} mm/px | Chord = {w_chord_mm:.2f} mm | Diam = {diam_mm:.2f} mm")

    out_file = os.path.join(ROOT_DIR, "audit", "camera_audit.json")
    with open(out_file, "w") as f:
        json.dump({
            "f_local_px_rad": f_local,
            "ifov_urad_px": ifov_urad,
            "anisotropy_pct": anisotropy_pct,
            "shadow_paraxial_deg": shadow_paraxial_deg,
            "shadow_local_deg": theta_shadow_local,
            "scenarios": {name: {"D_m": D, "scale_mm_px": (D * 1000.0) / f_local} for name, D in scenarios}
        }, f, indent=2)
    print(f"\nSaved camera audit data to: {out_file}")

if __name__ == "__main__":
    main()
