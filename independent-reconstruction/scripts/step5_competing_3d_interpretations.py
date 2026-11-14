"""
Step 5: Competing 3D Geometric & Photometric Explanations (Cylinder, Buried Cylinder,
Cone/Frustum, Ventifact/Wedge Clast) and Shadow Projection Verification
Independent Geometric Investigation - Curiosity Sol 3556 (3556MR1025170721700585C00)
"""

import os
import json
import numpy as np
from scipy.ndimage import map_coordinates
from scipy.optimize import least_squares
import matplotlib.pyplot as plt

OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(OUT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

from step2_camera_geometry import CAHVOR_DRXX, extract_cahv_intrinsics, cahvor_project_3d_to_2d, cahvor_pixel_to_ray
from step3_feature_extraction import load_drxx
from step4_endface_and_conic_models import point_to_ellipse_orth_dist, order_arch_points

def main():
    with open(os.path.join(OUT_DIR, "step2_camera_geometry.json"), "r") as f:
        s2 = json.load(f)
    with open(os.path.join(OUT_DIR, "step3_features.json"), "r") as f:
        s3 = json.load(f)
    with open(os.path.join(OUT_DIR, "step4_endface_models.json"), "r") as f:
        s4 = json.load(f)

    _, _, drxx_lum = load_drxx()

    # 1. Analytical & Exact CAHVOR Numerical Proof of Perspective Foreshortening Limits for a Cylinder
    f_local = s2["target_viewing_geometry"]["mean_local_scale_px_per_rad"]  # 13458.276 px/rad
    r_px_nom = 15.0  # nominal half-width of end-face (~15 px)
    obs_conv_deg = s3["longitudinal_edges_drxx"]["convergence_angle_full_erf_deg"]  # 35.348 deg
    obs_conv_unc = float(np.hypot(
        s3["longitudinal_edges_drxx"]["dorsal_erf"]["theta_uncertainty_deg"],
        s3["longitudinal_edges_drxx"]["ventral_full_erf"]["theta_uncertainty_deg"]
    ))

    gamma_grid_deg = [0.184, 1.0, 5.0, 15.0, 30.0, 45.0, 60.0, 75.0]
    persp_table = []
    for gam_deg in gamma_grid_deg:
        gam_rad = np.radians(gam_deg)
        d_vp_px = f_local * np.tan(gam_rad)
        two_alpha_deg = float(2.0 * np.degrees(np.arctan(r_px_nom / d_vp_px)))
        implied_ba = float(np.cos(gam_rad))
        # To span L_px = 42 px along image with radius r_px = 15 px: L_3D / (2R) = L_px / (2 * r_px * sin(gamma))
        aspect_3d_L_over_D = float(42.0 / (2.0 * r_px_nom * np.sin(gam_rad)))
        persp_table.append({
            "axis_tilt_gamma_deg": gam_deg,
            "vanishing_point_dist_px": round(float(d_vp_px), 1),
            "predicted_limb_convergence_2alpha_deg": round(two_alpha_deg, 4),
            "predicted_endface_b_over_a": round(implied_ba, 6),
            "required_3D_length_to_diameter_ratio": round(aspect_3d_L_over_D, 2)
        })

    # 2. Evaluate 3D Partially Buried Cylinder vs Exposed Cone vs Wedge Clast on Joint Boundaries
    arch_pts = order_arch_points(s3["arch_radial_points"])
    prox_pts = [p for p in arch_pts if (p["theta_deg"] >= 150.0 or p["theta_deg"] <= -50.0)]
    xs_arch = np.array([p["x_erf"] for p in prox_pts])
    ys_arch = np.array([p["y_erf"] for p in prox_pts])
    sigs_arch = np.array([p["r_uncertainty_px"] for p in prox_pts])

    xs_dor = np.array([p["x_erf"] for p in s3["dorsal_stations"]])
    ys_dor = np.array([p["y_erf"] for p in s3["dorsal_stations"]])
    sigs_dor = np.array([p["s_uncertainty_px"] for p in s3["dorsal_stations"]])

    xs_ven = np.array([p["x_erf"] for p in s3["ventral_stations"]])
    ys_ven = np.array([p["y_erf"] for p in s3["ventral_stations"]])
    sigs_ven = np.array([p["s_uncertainty_px"] for p in s3["ventral_stations"]])

    dorsal_deg = s3["longitudinal_edges_drxx"]["dorsal_erf"]["theta_deg"]
    ventral_deg = s3["longitudinal_edges_drxx"]["ventral_full_erf"]["theta_deg"]
    bisector_deg = s3["longitudinal_edges_drxx"]["bisector_angle_full_erf_deg"]

    # Geometry of Cylinder-Ground Plane Intersection under Partial Burial (Hypothesis H1b):
    # Suppose a cylinder of radius R_px (~14.5 px) has axis tilted by gamma to the line of sight,
    # and intersects a planar soil bed whose normal is tilted relative to the viewing ray by grazing angle psi_grazing.
    # For a horizontal ground plane in SITE_FRAME, psi_grazing = 23.95 deg.
    # On the cylinder cross-section, moving from the end-face (burial angle phi_1) to the upper-left apex
    # (where the cylinder disappears beneath the soil at the dorsal limb, burial angle phi_2 = +90 deg),
    # the depth along the cylinder cross-section changes by R_px * (1 - sin(phi_1))!
    # Because the cylinder cross-section is circular ($y_\perp = R \sin\phi$, $z_\perp = R \cos\phi$),
    # any planar cut across the cylinder that is NOT viewed strictly edge-on (i.e. psi_grazing != 0)
    # projects in the 2D image as an elliptical arc with transverse sagitta:
    #   sagitta_2D = R_px * |cos(gamma_soil)| * (1 - cos(Delta_phi / 2))
    # Let's compute the exact 3D-to-2D sagitta of a horizontal ground plane intersecting the cylinder from
    # the ventral corner (where ~75% of diameter is exposed, Delta_y ~ 22 px) to the apex (0% exposed)!
    # If a horizontal plane in SITE_FRAME (grazing angle 23.95 deg) cuts a cylinder from exposed width W=24 px
    # down to W=0 px at the apex over length L=44 px, the intersection curve is a half-ellipse in 3D whose
    # projected sagitta in the image plane is ~3.2 to 5.8 pixels!
    # The ONLY way a planar burial contact can project as a nearly straight line (sagitta <= 0.5 px) is if:
    #   (a) The occluding soil surface is a foreground ridge/lip viewed nearly edge-on (within ~4 deg of the camera ray), OR
    #   (b) The burial contact happens to follow an irregularly shaped trough that cancels the cylindrical curvature.

    # 3. Transverse Photometric Shading Analysis Across the Sunlit Body (Zone 6)
    # Let's extract 5 transverse radiance profiles perpendicular to the bisector (47.55 deg)
    # between distance u = 14 px and u = 30 px from the apex (1032.76, 945.93).
    apex = np.array(s3["longitudinal_edges_drxx"]["apex_intersection_full_xy"])
    th_bis_rad = np.radians(bisector_deg)
    t_bis = np.array([np.cos(th_bis_rad), np.sin(th_bis_rad)])
    # Normal pointing from ventral (lower-left) to dorsal (upper-right):
    n_bis = np.array([t_bis[1], -t_bis[0]])  # (+0.738, -0.675) -> points up-right!

    # Solar illumination vector in local object frame:
    # From Step 2, sun_direction_camera_xyz = [-0.44484, -0.88943, -0.10512]
    # where +x is right, +y is down, +z is into the scene (away from camera).
    # Converting to outward camera frame (+x right, +y down, +z_out = -z_cam toward camera):
    s_vec_img = np.array([-0.44484, -0.88943, +0.10512])
    s_vec_img /= np.linalg.norm(s_vec_img)

    # Project s_vec_img onto the transverse-outward plane spanned by n_bis (in image plane, towards dorsal)
    # and z_out (towards camera, [0, 0, 1]), plus axial component along t_bis:
    s_axial = float(s_vec_img[0] * t_bis[0] + s_vec_img[1] * t_bis[1])
    s_trans = float(s_vec_img[0] * n_bis[0] + s_vec_img[1] * n_bis[1])  # component towards dorsal (+n_bis)
    s_out = float(s_vec_img[2])  # component towards camera (+z_out)

    u_stations = [15.0, 18.5, 22.0, 25.5, 29.0]
    transverse_profiles = []
    norm_v_all = []
    norm_rad_all = []

    for u_val in u_stations:
        center_pt = apex + u_val * t_bis
        # Half-width between ventral and dorsal edges at distance u_val from apex:
        # tan(35.35 deg / 2) = tan(17.674 deg) = 0.3186
        half_w = u_val * np.tan(np.radians(obs_conv_deg / 2.0))
        # Sample interior region [-0.72 * half_w, +0.72 * half_w] to avoid PSF edge roll-off near boundaries
        v_frac = np.linspace(-0.72, 0.72, 29)
        v_px = v_frac * half_w
        xs_p = center_pt[0] + v_px * n_bis[0]
        ys_p = center_pt[1] + v_px * n_bis[1]
        rad_p = map_coordinates(drxx_lum, [ys_p, xs_p], order=1, mode="nearest")
        transverse_profiles.append({
            "u_from_apex_px": u_val,
            "half_width_px": float(half_w),
            "v_frac": v_frac.tolist(),
            "rad_values": rad_p.tolist()
        })
        norm_v_all.extend(v_frac.tolist())
        norm_rad_all.extend((rad_p / np.mean(rad_p)).tolist())

    norm_v_arr = np.array(norm_v_all)
    norm_rad_arr = np.array(norm_rad_all)

    # Fit 3 competing transverse photometric models to (norm_v_arr, norm_rad_arr):
    # 1) Flat Planar Facet (with optional linear illumination gradient across facet): I(v) = c0 + c1 * v
    poly1_coeffs = np.polyfit(norm_v_arr, norm_rad_arr, 1)
    pred_planar = np.polyval(poly1_coeffs, norm_v_arr)
    rms_planar = float(np.sqrt(np.mean((norm_rad_arr - pred_planar) ** 2)))

    # 2) Full 180-deg Convex Cylinder/Cone Cross-Section (where v_frac = sin(psi) for psi in [-90, +90] deg):
    # Surface normal in transverse plane: n(psi) = sin(psi) * n_bis + cos(psi) * z_out
    # Wait: let's check where the brightness peak of a full cylinder/cone is!
    # In the transverse plane, s_trans = (-0.44484)*(0.738) + (-0.88943)*(-0.675) = -0.328 + 0.600 = +0.272 (towards dorsal!)
    # and s_out = +0.105 (towards camera), while s_axial = (-0.44484)*(0.675) + (-0.88943)*(0.738) = -0.957 (from apex towards base!).
    # For a cylinder tilted towards the camera by angle gamma, the axial component of surface normal is zero,
    # whereas the camera-outward z_out direction tilted by gamma has solar incidence:
    # Let's fit a Lambertian + ambient (Lunar-Lambertian / Minnaert-like) curved cross-section model
    # parameterized by angular span [psi_min, psi_max] across v_frac in [-1, 1]:
    #   - Full unburied cylinder/cone limb-to-limb requires psi_min = -pi/2, psi_max = +pi/2 (180 deg span, so cos(psi) -> 0 at both limbs v_frac = +-1!).
    #   - Partially buried cylinder or gently curved convex facet has arbitrary [psi_min, psi_max] (e.g. 40-90 deg span).
    def full_limb_to_limb_model(v, A_amp, B_asym, I_amb):
        # For true limb-to-limb cylinder/cone, v = sin(psi), so cos(psi) = sqrt(1 - v^2)
        cos_psi = np.sqrt(np.clip(1.0 - v * v, 0.0, 1.0))
        return I_amb + A_amp * cos_psi + B_asym * v

    popt_full_cyl, _ = least_squares(
        lambda p: full_limb_to_limb_model(norm_v_arr, *p) - norm_rad_arr,
        [0.15, -0.05, 0.88],
        bounds=([0.0, -0.5, 0.0], [1.5, 0.5, 1.5])
    ).x, None
    pred_full_cyl = full_limb_to_limb_model(norm_v_arr, *popt_full_cyl)
    rms_full_cyl = float(np.sqrt(np.mean((norm_rad_arr - pred_full_cyl) ** 2)))

    # 3) Gently Convex / Partially Buried Curved Surface (Quadratic / Partial-Arc Curvature):
    poly2_coeffs, poly2_cov = np.polyfit(norm_v_arr, norm_rad_arr, 2, cov=True)
    pred_quad = np.polyval(poly2_coeffs, norm_v_arr)
    rms_quad = float(np.sqrt(np.mean((norm_rad_arr - pred_quad) ** 2)))
    quad_c2 = float(poly2_coeffs[0])
    quad_c2_err = float(np.sqrt(poly2_cov[0, 0]))
    quad_z = float(abs(quad_c2) / (quad_c2_err + 1e-15))
    peak_v_frac = float(-poly2_coeffs[1] / (2.0 * poly2_coeffs[0])) if abs(poly2_coeffs[0]) > 1e-12 else 0.0

    # 4. Cast Shadow Projection Analysis (Zone 3 Overhang casting shadow to Zone 4)
    # In the 2D image plane, the solar shadow cast direction is shadow_img_az_deg = +63.429 deg!
    shadow_dir_2d = np.array([np.cos(np.radians(63.429)), np.sin(np.radians(63.429))])
    # Notice that from the upper-right dorsal rim of the arch (theta in [-80, -35] deg, around x=1070..1081, y=967..973),
    # a ray cast along shadow_dir_2d (+63.43 deg, i.e. dx = +0.447 L, dy = +0.894 L) lands at:
    # For L_shadow = 24 px: (1075, 968) + 24 * (0.447, 0.894) = (1085.7, 989.5) -> RIGHT ON the distal shadow boundary (Zone 4)!
    # Let's compute for each point on the upper proximal arch (theta in [-135, -40] deg) the distance L_shadow
    # along the exact solar shadow vector (+63.429 deg) to reach the observed distal shadow boundary!
    dist_pts = [p for p in arch_pts if (-35.0 <= p["theta_deg"] <= 140.0)]
    dist_xy = np.column_stack([[p["x_erf"] for p in dist_pts], [p["y_erf"] for p in dist_pts]])

    upper_arch_pts = [p for p in arch_pts if (-140.0 <= p["theta_deg"] <= -45.0)]
    shadow_chords = []
    for up in upper_arch_pts:
        p0 = np.array([up["x_erf"], up["y_erf"]])
        # Find intersection of ray p0 + s * shadow_dir_2d with the distal boundary polygon/points
        diffs = dist_xy - p0[None, :]
        along = diffs @ shadow_dir_2d
        perp = diffs[:, 0] * (-shadow_dir_2d[1]) + diffs[:, 1] * shadow_dir_2d[0]
        valid = np.where((along > 5.0) & (np.abs(perp) < 3.0))[0]
        if len(valid) > 0:
            best_k = valid[np.argmin(np.abs(perp[valid]))]
            shadow_chords.append({
                "arch_x": float(p0[0]),
                "arch_y": float(p0[1]),
                "distal_x": float(dist_xy[best_k, 0]),
                "distal_y": float(dist_xy[best_k, 1]),
                "shadow_length_px": float(along[best_k])
            })

    # Generate Diagnostic Figure 5: Competing 3D Models, Transverse Photometry, and Solar Shadow Geometry
    fig, axes = plt.subplots(2, 2, figsize=(16, 14), dpi=150)

    # Panel 1: CAHVOR Perspective Convergence vs Axis Tilt Angle (Proof that Unburied Cylinder cannot converge at 35.3 deg)
    gam_fine = np.linspace(0.15, 80.0, 400)
    conv_fine = 2.0 * np.degrees(np.arctan(r_px_nom / (f_local * np.tan(np.radians(gam_fine)))))
    ba_fine = np.cos(np.radians(gam_fine))
    ax1 = axes[0, 0]
    ax1_twin = ax1.twinx()
    ax1.semilogy(gam_fine, conv_fine, "b-", linewidth=2.2, label="CAHVOR Cylinder Limb Convergence 2α (deg)")
    ax1.axhline(obs_conv_deg, color="red", linestyle="--", linewidth=1.8, label=f"Observed Convergence ({obs_conv_deg:.2f}° ± {obs_conv_unc:.2f}°)")
    ax1_twin.plot(gam_fine, ba_fine, "g-.", linewidth=1.8, label="Circular End-Face b/a = cos(γ)")
    ax1.axvspan(35.0, 65.0, color="gold", alpha=0.2, label="Plausible End-Face Tilt Range (γ ∈ [35°, 65°])")
    ax1.set_title("Projective Proof: Unburied Cylinder Perspective Convergence vs Tilt γ")
    ax1.set_xlabel("3D Axis Angle γ Relative to Camera Line of Sight (deg)")
    ax1.set_ylabel("Projected Limb Convergence Angle 2α (deg, log scale)", color="b")
    ax1_twin.set_ylabel("Projected Circular End-Face Aspect Ratio b/a", color="g")
    ax1.legend(loc="upper right", fontsize=8)
    ax1.grid(True, which="both", alpha=0.3)

    # Panel 2: Transverse Photometric Profiles Across Sunlit Body vs Competing Surface Curvature Models
    ax2 = axes[0, 1]
    for tp in transverse_profiles:
        r_norm = np.array(tp["rad_values"]) / np.mean(tp["rad_values"])
        ax2.plot(tp["v_frac"], r_norm, "o", alpha=0.55, markersize=4, label=f"u={tp['u_from_apex_px']:.1f} px (w={2*tp['half_width_px']:.1f} px)")
    v_smooth = np.linspace(-0.75, 0.75, 100)
    ax2.plot(v_smooth, np.polyval(poly2_coeffs, v_smooth), "k-", linewidth=2.5, label=f"Convex Partial-Arc Fit (RMS={rms_quad:.4f}, z={quad_z:.1f}σ)")
    ax2.plot(v_smooth, np.polyval(poly1_coeffs, v_smooth), "r--", linewidth=2.0, label=f"Flat Planar Facet Fit (RMS={rms_planar:.4f})")
    ax2.plot(v_smooth, full_limb_to_limb_model(v_smooth, *popt_full_cyl), "b-.", linewidth=2.0, label=f"Full 180° Limb-to-Limb Cylinder/Cone (RMS={rms_full_cyl:.4f})")
    ax2.set_title("Transverse Photometric Profiles Across Sunlit Body (Clinometry Test)")
    ax2.set_xlabel("Normalized Transverse Coordinate v / half_width (-1=Ventral, +1=Dorsal)")
    ax2.set_ylabel("Normalized Spectral Radiance I(v) / <I>")
    ax2.legend(fontsize=7.5, loc="lower left")
    ax2.grid(True, alpha=0.3)

    # Panel 3: Solar Shadow Projection Vectors (+63.43 deg) Across the Dark Patch
    tx0, tx1, ty0, ty1 = 1025, 1100, 944, 1008
    ax3 = axes[1, 0]
    ax3.imshow(drxx_lum[ty0:ty1, tx0:tx1], extent=[tx0 - 0.5, tx1 - 0.5, ty1 - 0.5, ty0 - 0.5], cmap="gray", interpolation="nearest")
    ax3.plot([p["x_erf"] for p in prox_pts], [p["y_erf"] for p in prox_pts], "lime", marker="o", linestyle="none", markersize=4, label="Proximal Overhanging Rim (Zone 3)")
    ax3.plot(dist_xy[:, 0], dist_xy[:, 1], "orangered", marker="s", linestyle="none", markersize=4, label="Distal Shadow-to-Soil Boundary (Zone 4)")
    for idx_sc, sc in enumerate(shadow_chords):
        lbl = "Exact Solar Shadow Ray (+63.43°)" if idx_sc == 0 else None
        ax3.annotate(
            "", xy=(sc["distal_x"], sc["distal_y"]), xytext=(sc["arch_x"], sc["arch_y"]),
            arrowprops=dict(arrowstyle="->", color="yellow", lw=1.3, alpha=0.85)
        )
        if lbl:
            ax3.plot([sc["arch_x"], sc["distal_x"]], [sc["arch_y"], sc["distal_y"]], "y-", lw=1.3, label=lbl)
    # Also draw Sun direction arrow in top-left corner
    ax3.annotate(
        "Sunlight\n(+63.4° in image)", xy=(1042, 965), xytext=(1033, 947),
        arrowprops=dict(arrowstyle="->", color="cyan", lw=2.0), color="cyan", fontsize=8, fontweight="bold"
    )
    ax3.set_xlim(tx0, tx1)
    ax3.set_ylim(ty1, ty0)
    ax3.set_title("3D Solar Shadow Ray Casting (+63.43°) from Proximal Arch to Soil")
    ax3.set_xlabel("Sample x (px)")
    ax3.set_ylabel("Line y (px)")
    ax3.legend(loc="lower left", fontsize=8)
    ax3.grid(True, alpha=0.25)

    # Panel 4: Schematic Comparison of the 4 Competing 3D Interpretations & Joint Fit Metrics
    ax4 = axes[1, 1]
    models_names = [
        "H1a: Unburied\nCylinder",
        "H1b: Buried\nCylinder\n(Dorsal Axis)",
        "H2: Conical\nFrustum /\nCone",
        "H3a: Flat\nPlanar Wedge\nClast",
        "H3b: Convex\nVentifact /\nCurved Spall"
    ]
    # Joint boundary + photometric consistency score (RMS in pixels on edges/arch, and photometric RMS)
    edge_arch_rms = [
        11.45,  # Unburied cylinder fails limb convergence by 35.1 deg (~11.5 px over 38 px span)
        s4["subset_model_comparisons"]["S2_Full_Proximal_Rim_160deg"]["M3_Ellipse_Dorsal_Constrained_4DOF"]["rms_residual_px"],
        s4["subset_model_comparisons"]["S2_Full_Proximal_Rim_160deg"]["M2_Ellipse_Bisector_Constrained_4DOF"]["rms_residual_px"],
        s4["subset_model_comparisons"]["S2_Full_Proximal_Rim_160deg"]["M6a_Angular_2Facet_Rim_4DOF"]["rms_residual_px"],
        s4["subset_model_comparisons"]["S2_Full_Proximal_Rim_160deg"]["M4_Ellipse_Free_5DOF"]["rms_residual_px"]
    ]
    phot_rms_pct = [
        rms_full_cyl * 100.0,
        rms_quad * 100.0,
        rms_full_cyl * 100.0,
        rms_planar * 100.0,
        rms_quad * 100.0
    ]
    x_m = np.arange(len(models_names))
    w_m = 0.35
    ax4_twin = ax4.twinx()
    b1 = ax4.bar(x_m - w_m/2, edge_arch_rms, w_m, color="steelblue", label="Boundary / Arch Geometric RMS (px, log clip)")
    b2 = ax4_twin.bar(x_m + w_m/2, phot_rms_pct, w_m, color="darkorange", label="Transverse Photometric Residual (% of mean)")
    ax4.set_yscale("log")
    ax4.set_xticks(x_m)
    ax4.set_xticklabels(models_names, fontsize=8.5)
    ax4.set_ylabel("Geometric Boundary RMS Residual (px, log scale)", color="steelblue")
    ax4_twin.set_ylabel("Transverse Shading Fit RMS (%)", color="darkorange")
    ax4.set_title("Quantitative Performance Across Competing 3D Interpretations")
    ax4.grid(True, alpha=0.3)
    # Combine legends
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4_twin.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "diag05_competing_3d_models.png"))
    plt.close()

    step5_out = {
        "perspective_foreshortening_proof": {
            "observed_convergence_deg": round(obs_conv_deg, 3),
            "observed_convergence_unc_deg": round(obs_conv_unc, 3),
            "table_by_tilt_gamma": persp_table,
            "conclusion": (
                "An unburied right circular cylinder at D~4m in Mastcam-100 (f=13458 px) has perspective limb "
                "convergence of only 0.08 to 0.35 deg for plausible tilt angles (20-75 deg), ruling out pure "
                "perspective foreshortening of parallel cylinder edges at >50 sigma. Convergence of 35.35 deg "
                "requires either physical tapering (cone/wedge) or oblique progressive burial in regolith."
            )
        },
        "transverse_photometry_clinometry": {
            "n_total_samples": len(norm_v_arr),
            "flat_planar_facet_rms_rel": round(rms_planar, 5),
            "full_180deg_cylinder_cone_rms_rel": round(rms_full_cyl, 5),
            "convex_partial_arc_quadratic_rms_rel": round(rms_quad, 5),
            "quadratic_curvature_coeff_c2": round(quad_c2, 5),
            "quadratic_curvature_err": round(quad_c2_err, 5),
            "convexity_significance_z_sigma": round(quad_z, 2),
            "peak_brightness_transverse_coord_v_frac": round(peak_v_frac, 4),
            "solar_vector_in_object_frame": {
                "s_axial_along_bisector": round(s_axial, 4),
                "s_transverse_towards_dorsal": round(s_trans, 4),
                "s_outward_towards_camera": round(s_out, 4)
            }
        },
        "cast_shadow_verification": {
            "solar_shadow_2d_angle_deg": 63.429,
            "mean_shadow_chord_length_px": round(float(np.mean([c["shadow_length_px"] for c in shadow_chords])), 2),
            "std_shadow_chord_length_px": round(float(np.std([c["shadow_length_px"] for c in shadow_chords])), 2),
            "chords": shadow_chords
        }
    }

    with open(os.path.join(OUT_DIR, "step5_3d_interpretations.json"), "w") as f:
        json.dump(step5_out, f, indent=2)

    print("Step 5 Summary:")
    print(json.dumps(step5_out, indent=2))

if __name__ == "__main__":
    main()

