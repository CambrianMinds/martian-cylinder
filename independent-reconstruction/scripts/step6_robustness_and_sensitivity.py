"""
Step 6: Comprehensive Robustness & Sensitivity Testing and Master Measurements Compilation
Independent Geometric Investigation - Curiosity Sol 3556 (3556MR1025170721700585C00)
"""

import os
import json
import numpy as np
from scipy.ndimage import gaussian_filter, map_coordinates
import matplotlib.pyplot as plt

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(OUT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)
DATA_DIR = os.path.abspath(os.path.join(OUT_DIR, "..", "data"))

from step1_image_inspection import PRODUCTS, load_pds_image
from step3_feature_extraction import (
    load_drxx, load_drlx, extract_subpixel_profile_edges,
    extract_radial_arch_points, fit_line_orthogonal
)
from step4_endface_and_conic_models import (
    fit_ellipse_free_odr, fit_ellipse_constrained_odr, fit_circle_odr, order_arch_points
)

def main():
    drxx_dn, drxx_rad, drxx_lum = load_drxx()
    drlx_dn, drlx_rad, drlx_lum = load_drlx()
    drcx_rgb = load_pds_image(PRODUCTS["DRCX"]).astype(np.float64)
    drcx_lum = drcx_rgb.mean(axis=2) / 255.0
    drcl_rgb = load_pds_image(PRODUCTS["DRCL"]).astype(np.float64)
    drcl_lum = drcl_rgb.mean(axis=2) / 255.0

    with open(os.path.join(OUT_DIR, "step1_provenance.json"), "r") as f:
        s1 = json.load(f)
    with open(os.path.join(OUT_DIR, "step2_camera_geometry.json"), "r") as f:
        s2 = json.load(f)
    with open(os.path.join(OUT_DIR, "step3_features.json"), "r") as f:
        s3 = json.load(f)
    with open(os.path.join(OUT_DIR, "step4_endface_models.json"), "r") as f:
        s4 = json.load(f)
    with open(os.path.join(OUT_DIR, "step5_3d_interpretations.json"), "r") as f:
        s5 = json.load(f)

    # 1. Test Sensitivity to Pixel Selection / Trimming Along Longitudinal Edges
    d_st = s3["dorsal_stations"]
    v_st = s3["ventral_stations"]

    trim_tests = {}
    for label, d_slice, v_slice in [
        ("Full_Baseline_26pts", d_st, v_st),
        ("Trim_Ends_15pct", d_st[2:-2], v_st[2:-2]),
        ("Trim_Ends_25pct", d_st[3:-3], v_st[3:-3]),
        ("Upper_Half_Near_Apex", d_st[:14], v_st[:14]),
        ("Lower_Half_Near_Arch", d_st[12:], v_st[12:]),
        ("Exclude_Ventral_Pebble_Zone", d_st, [s for s in v_st if not (978.5 <= s["y_erf"] <= 986.5)])
    ]:
        df = fit_line_orthogonal([s["x_erf"] for s in d_slice], [s["y_erf"] for s in d_slice])
        vf = fit_line_orthogonal([s["x_erf"] for s in v_slice], [s["y_erf"] for s in v_slice])
        trim_tests[label] = {
            "dorsal_theta_deg": round(df["theta_deg"], 3),
            "dorsal_rms_px": round(df["rms_orthogonal_residual_px"], 4),
            "ventral_theta_deg": round(vf["theta_deg"], 3),
            "ventral_rms_px": round(vf["rms_orthogonal_residual_px"], 4),
            "convergence_angle_deg": round(vf["theta_deg"] - df["theta_deg"], 3),
            "bisector_angle_deg": round(0.5 * (vf["theta_deg"] + df["theta_deg"]), 3)
        }

    # 2. Test Sensitivity to Subpixel Fitting Method & Smoothing Kernel Width
    method_tests = {}
    # Erf vs Parabolic Gradient vs Discrete Integer Pixel on DRXX
    df_erf = fit_line_orthogonal([s["x_erf"] for s in d_st], [s["y_erf"] for s in d_st])
    vf_erf = fit_line_orthogonal([s["x_erf"] for s in v_st], [s["y_erf"] for s in v_st])
    df_grad = fit_line_orthogonal([s["x_grad"] for s in d_st], [s["y_grad"] for s in d_st])
    vf_grad = fit_line_orthogonal([s["x_grad"] for s in v_st], [s["y_grad"] for s in v_st])
    df_int = fit_line_orthogonal([round(s["x_erf"]) for s in d_st], [round(s["y_erf"]) for s in d_st])
    vf_int = fit_line_orthogonal([round(s["x_erf"]) for s in v_st], [round(s["y_erf"]) for s in v_st])

    method_tests["Erf_Subpixel_ODR"] = {
        "dorsal_theta_deg": round(df_erf["theta_deg"], 3),
        "dorsal_rms_px": round(df_erf["rms_orthogonal_residual_px"], 4),
        "ventral_theta_deg": round(vf_erf["theta_deg"], 3),
        "ventral_rms_px": round(vf_erf["rms_orthogonal_residual_px"], 4),
        "convergence_deg": round(vf_erf["theta_deg"] - df_erf["theta_deg"], 3)
    }
    method_tests["Parabolic_Gradient_Peak"] = {
        "dorsal_theta_deg": round(df_grad["theta_deg"], 3),
        "dorsal_rms_px": round(df_grad["rms_orthogonal_residual_px"], 4),
        "ventral_theta_deg": round(vf_grad["theta_deg"], 3),
        "ventral_rms_px": round(vf_grad["rms_orthogonal_residual_px"], 4),
        "convergence_deg": round(vf_grad["theta_deg"] - df_grad["theta_deg"], 3)
    }
    method_tests["Discrete_Integer_Pixels"] = {
        "dorsal_theta_deg": round(df_int["theta_deg"], 3),
        "dorsal_rms_px": round(df_int["rms_orthogonal_residual_px"], 4),
        "ventral_theta_deg": round(vf_int["theta_deg"], 3),
        "ventral_rms_px": round(vf_int["rms_orthogonal_residual_px"], 4),
        "convergence_deg": round(vf_int["theta_deg"] - df_int["theta_deg"], 3)
    }

    # 3. Test Stability Across All 4 PDS Data Products (DRXX, DRCX, DRLX, DRCL)
    product_tests = {}
    for pname, img_2d, shift_xy in [
        ("DRXX_16bit_Raw_CAHVOR", drxx_lum, (0.0, 0.0)),
        ("DRCX_8bit_Color_CAHVOR", drcx_lum, (0.0, 0.0)),
        ("DRLX_16bit_Linearized_CAHV", drlx_lum, (-3.0, -3.0)),
        ("DRCL_8bit_Linearized_CAHV", drcl_lum, (-3.0, -3.0))
    ]:
        dx, dy = shift_xy
        d_p = extract_subpixel_profile_edges(img_2d, [1036.0 + dx, 947.2 + dy], [1068.5 + dx, 963.6 + dy], n_stations=26, grad_sign=-1)
        v_p = extract_subpixel_profile_edges(img_2d, [1033.2 + dx, 952.5 + dy], [1051.2 + dx, 989.5 + dy], n_stations=26, grad_sign=+1)
        df_p = fit_line_orthogonal([s["x_erf"] for s in d_p], [s["y_erf"] for s in d_p])
        vf_p = fit_line_orthogonal([s["x_erf"] for s in v_p], [s["y_erf"] for s in v_p])

        all_th = np.arange(-180.0, 180.0, 5.0)
        arch_p = order_arch_points(extract_radial_arch_points(img_2d, (1067.5 + dx, 985.0 + dy), all_th))
        s2_p = [p for p in arch_p if (p["theta_deg"] >= 150.0 or p["theta_deg"] <= -50.0)]
        el_p = fit_ellipse_free_odr(
            np.array([p["x_erf"] - dx for p in s2_p]),
            np.array([p["y_erf"] - dy for p in s2_p]),
            np.array([p["r_uncertainty_px"] for p in s2_p])
        )
        product_tests[pname] = {
            "dorsal_theta_deg": round(df_p["theta_deg"], 3),
            "dorsal_rms_px": round(df_p["rms_orthogonal_residual_px"], 4),
            "ventral_theta_deg": round(vf_p["theta_deg"], 3),
            "ventral_rms_px": round(vf_p["rms_orthogonal_residual_px"], 4),
            "convergence_angle_deg": round(vf_p["theta_deg"] - df_p["theta_deg"], 3),
            "proximal_arch_free_ellipse_b_over_a": round(el_p["params"]["b_over_a"], 4),
            "proximal_arch_free_ellipse_minor_deg": round(el_p["params"]["minor_axis_deg"], 2),
            "proximal_arch_rms_px": round(float(np.sqrt(np.mean(el_p["residuals_px"] ** 2))), 4)
        }

    # 4. Monte Carlo Correlated Noise (Bayer Demosaicing + Sensor Noise) Perturbation
    rng = np.random.default_rng(2026)
    noise_base = s3["radiometry_and_noise"]["soil_background_highfreq_noise_std_rad"]
    mc_noise_results = {}
    for mult in [1.0, 2.0, 3.0]:
        conv_list, dor_rms_list, ba_list = [], [], []
        for _ in range(30):
            # Generate 5x5 Bayer-like spatially correlated noise field
            raw_n = rng.normal(0.0, noise_base * mult * 1.4, size=drxx_lum.shape)
            corr_n = gaussian_filter(raw_n, sigma=0.8)
            noisy_img = drxx_lum + corr_n
            dp = extract_subpixel_profile_edges(noisy_img, [1036.0, 947.2], [1068.5, 963.6], n_stations=26, grad_sign=-1)
            vp = extract_subpixel_profile_edges(noisy_img, [1033.2, 952.5], [1051.2, 989.5], n_stations=26, grad_sign=+1)
            df_n = fit_line_orthogonal([s["x_erf"] for s in dp], [s["y_erf"] for s in dp])
            vf_n = fit_line_orthogonal([s["x_erf"] for s in vp], [s["y_erf"] for s in vp])
            conv_list.append(vf_n["theta_deg"] - df_n["theta_deg"])
            dor_rms_list.append(df_n["rms_orthogonal_residual_px"])

            arch_n = order_arch_points(extract_radial_arch_points(noisy_img, (1067.5, 985.0), np.arange(-180.0, 180.0, 5.0)))
            s2_n = [p for p in arch_n if (p["theta_deg"] >= 150.0 or p["theta_deg"] <= -50.0)]
            el_n = fit_ellipse_constrained_odr(
                np.array([p["x_erf"] for p in s2_n]),
                np.array([p["y_erf"] for p in s2_n]),
                np.array([p["r_uncertainty_px"] for p in s2_n]),
                df_n["theta_deg"]
            )
            ba_list.append(el_n["params"]["b_over_a"])

        mc_noise_results[f"Noise_{mult:.0f}x_Correlated"] = {
            "convergence_mean_deg": round(float(np.mean(conv_list)), 3),
            "convergence_std_deg": round(float(np.std(conv_list)), 3),
            "dorsal_rms_mean_px": round(float(np.mean(dor_rms_list)), 4),
            "dorsal_constrained_ba_mean": round(float(np.mean(ba_list)), 4),
            "dorsal_constrained_ba_std": round(float(np.std(ba_list)), 4)
        }

    # 5. Physical Dimensions (mm) Across Distance / Depth Uncertainty Range
    # Measured angular & pixel dimensions of the object:
    # - Maximum visible width across proximal arch (chord from ventral corner (1052.1, 991.5) to dorsal corner (1076.5, 967.8)):
    arch_pts = order_arch_points(s3["arch_radial_points"])
    s2_pts = [p for p in arch_pts if (p["theta_deg"] >= 150.0 or p["theta_deg"] <= -50.0)]
    p_ventral_corner = np.array([s2_pts[0]["x_erf"], s2_pts[0]["y_erf"]])
    p_dorsal_corner = np.array([s2_pts[-4]["x_erf"], s2_pts[-4]["y_erf"]])  # theta = -65 deg at top-right of sunlit termination
    chord_width_px = float(np.linalg.norm(p_dorsal_corner - p_ventral_corner))

    # Fitted ellipse diameter (2 * semi_major) on S1 (140 deg) and S2 (160 deg):
    diam_s1_px = 2.0 * s4["subset_model_comparisons"]["S1_Strict_Proximal_Arch_140deg"]["M4_Ellipse_Free_5DOF"]["params"]["semi_major"]
    diam_s2_px = 2.0 * s4["subset_model_comparisons"]["S2_Full_Proximal_Rim_160deg"]["M4_Ellipse_Free_5DOF"]["params"]["semi_major"]

    # Visible sunlit length along bisector from apex (1032.76, 945.93) to proximal arch vertex (~1060.2, 971.2):
    apex_pt = np.array(s3["longitudinal_edges_drxx"]["apex_intersection_full_xy"])
    arch_mid_pt = np.array([1060.2, 971.2])
    length_to_arch_vertex_px = float(np.linalg.norm(arch_mid_pt - apex_pt))
    length_dorsal_limb_px = float(np.linalg.norm(p_dorsal_corner - apex_pt))
    length_ventral_limb_px = float(np.linalg.norm(p_ventral_corner - apex_pt))

    physical_dimensions_by_depth = {}
    for d_key, d_info in s2["distance_and_spatial_scale_bounds"].items():
        scale_mm = d_info["mm_per_pixel_at_target"]
        physical_dimensions_by_depth[d_key] = {
            "distance_m": d_info["distance_m"],
            "scale_mm_per_px": scale_mm,
            "rim_chord_width_mm": round(chord_width_px * scale_mm, 2),
            "ellipse_major_diameter_S1_mm": round(diam_s1_px * scale_mm, 2),
            "ellipse_major_diameter_S2_mm": round(diam_s2_px * scale_mm, 2),
            "sunlit_axial_length_to_arch_mm": round(length_to_arch_vertex_px * scale_mm, 2),
            "dorsal_limb_length_mm": round(length_dorsal_limb_px * scale_mm, 2),
            "ventral_limb_length_mm": round(length_ventral_limb_px * scale_mm, 2)
        }

    # Generate Diagnostic Figure 6: Robustness & Sensitivity Summary
    fig, axes = plt.subplots(2, 2, figsize=(16, 12), dpi=150)

    # Panel 1: Convergence Angle Stability Across Segment Trimming & Products
    labels_t = list(trim_tests.keys())
    conv_t = [trim_tests[k]["convergence_angle_deg"] for k in labels_t]
    axes[0, 0].barh(labels_t, conv_t, color="teal", alpha=0.8)
    axes[0, 0].axvline(trim_tests["Full_Baseline_26pts"]["convergence_angle_deg"], color="red", linestyle="--", label="Baseline (35.35°)")
    axes[0, 0].set_xlim(25, 42)
    axes[0, 0].set_xlabel("Measured Convergence Angle 2α (deg)")
    axes[0, 0].set_title("Sensitivity of Limb Convergence Angle to Segment Selection")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Panel 2: Cross-Product Stability (DRXX, DRCX, DRLX, DRCL)
    p_labels = list(product_tests.keys())
    x_p = np.arange(len(p_labels))
    axes[0, 1].plot(x_p, [product_tests[k]["dorsal_theta_deg"] for k in p_labels], "bo-", label="Dorsal Edge Angle (deg)")
    axes[0, 1].plot(x_p, [product_tests[k]["ventral_theta_deg"] for k in p_labels], "ms-", label="Ventral Edge Angle (deg)")
    axes[0, 1].plot(x_p, [product_tests[k]["convergence_angle_deg"] for k in p_labels], "g^-", label="Convergence Opening Angle (deg)")
    axes[0, 1].plot(x_p, [product_tests[k]["proximal_arch_free_ellipse_minor_deg"] for k in p_labels], "k+--", label="Arch Ellipse Minor Axis Angle (deg)")
    axes[0, 1].set_xticks(x_p)
    axes[0, 1].set_xticklabels(["DRXX\n(16b CAHVOR)", "DRCX\n(8b CAHVOR)", "DRLX\n(16b CAHV)", "DRCL\n(8b CAHV)"], fontsize=8.5)
    axes[0, 1].set_ylabel("Angle in Image Plane (deg)")
    axes[0, 1].set_title("Reproducibility Across All 4 NASA PDS RDR Products")
    axes[0, 1].legend(fontsize=8)
    axes[0, 1].grid(True, alpha=0.3)

    # Panel 3: End-Face Aspect Ratio b/a Across Boundary Subsets (S1, S2, S3, S4)
    sub_names = ["S1 (140° Strict Rim)", "S2 (160° Full Rim)", "S3 (250° No Lobe)", "S4 (360° Full Dark)"]
    sub_keys = ["S1_Strict_Proximal_Arch_140deg", "S2_Full_Proximal_Rim_160deg", "S3_Lobe_Excluded_250deg", "S4_Full_360deg_Dark_Patch"]
    ba_free = [s4["subset_model_comparisons"][k]["M4_Ellipse_Free_5DOF"]["params"]["b_over_a"] for k in sub_keys]
    ba_dor = [s4["subset_model_comparisons"][k]["M3_Ellipse_Dorsal_Constrained_4DOF"]["params"]["b_over_a"] for k in sub_keys]
    ba_bis = [s4["subset_model_comparisons"][k]["M2_Ellipse_Bisector_Constrained_4DOF"]["params"]["b_over_a"] for k in sub_keys]
    rms_free = [s4["subset_model_comparisons"][k]["M4_Ellipse_Free_5DOF"]["rms_residual_px"] for k in sub_keys]

    ax3 = axes[1, 0]
    ax3_t = ax3.twinx()
    xp3 = np.arange(len(sub_names))
    ax3.plot(xp3, ba_free, "go-", linewidth=2, label="Free Ellipse b/a")
    ax3.plot(xp3, ba_dor, "bs--", linewidth=1.5, label="Dorsal-Aligned Ellipse b/a")
    ax3.plot(xp3, ba_bis, "c^:", linewidth=1.5, label="Bisector-Aligned Ellipse b/a")
    ax3_t.bar(xp3, rms_free, width=0.25, color="red", alpha=0.25, label="Free Ellipse Fit RMS (px)")
    ax3.set_xticks(xp3)
    ax3.set_xticklabels(sub_names, fontsize=8.5)
    ax3.set_ylim(0.65, 1.0)
    ax3.set_ylabel("Fitted Aspect Ratio (b / a)", color="g")
    ax3_t.set_ylabel("Orthogonal Fit RMS (px)", color="r")
    ax3.set_title("Impact of Shadow Boundary Inclusion on Ellipse Fit & Residuals")
    ax3.legend(loc="upper left", fontsize=8)
    ax3.grid(True, alpha=0.3)

    # Panel 4: Physical Dimensions (mm) vs Unknown Monocular Range D (m)
    d_vals = np.linspace(3.4, 5.3, 100)
    scale_curve = d_vals * 1000.0 / s2["target_viewing_geometry"]["mean_local_scale_px_per_rad"]
    axes[1, 1].plot(d_vals, chord_width_px * scale_curve, "b-", linewidth=2.0, label=f"Rim Chord Width ({chord_width_px:.1f} px)")
    axes[1, 1].plot(d_vals, diam_s2_px * scale_curve, "g--", linewidth=2.0, label=f"Fitted Ellipse Major Diam S2 ({diam_s2_px:.1f} px)")
    axes[1, 1].plot(d_vals, length_dorsal_limb_px * scale_curve, "r-.", linewidth=2.0, label=f"Exposed Dorsal Length ({length_dorsal_limb_px:.1f} px)")
    axes[1, 1].plot(d_vals, length_to_arch_vertex_px * scale_curve, "k:", linewidth=2.0, label=f"Axial Length to Arch Vertex ({length_to_arch_vertex_px:.1f} px)")
    axes[1, 1].axvspan(3.6, 4.4, color="gold", alpha=0.2, label="Mastcam Autofocus Range [3.6, 4.4 m]")
    axes[1, 1].axvline(3.957, color="darkorange", linestyle="-", alpha=0.8, label="Best Focus Distance (3.957 m)")
    axes[1, 1].set_xlabel("Monocular Slant Distance D from Camera Center (m)")
    axes[1, 1].set_ylabel("Physical Dimension on Mars (mm)")
    axes[1, 1].set_title("Metric Size Scaling & Monocular Depth Uncertainty")
    axes[1, 1].legend(fontsize=8, loc="upper left")
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "diag06_robustness_sensitivity.png"))
    plt.close()

    # Compile Master `measurements.json` Deliverable
    master_measurements = {
        "investigation_metadata": {
            "image_id": "3556MR1025170721700585C00",
            "mission": "Mars Science Laboratory (Curiosity)",
            "instrument": "Mastcam-100 Right (MAST_RIGHT, Serial 3004, f ~ 100 mm)",
            "sol": 3556,
            "utc_time": "2022-08-07T20:58:23.349",
            "local_true_solar_time": "12:10:25",
            "onboard_compression": "PREDICTIVE LOSSLESS BAYER HUFFMAN ENCODING (INST_CMPRS_MODE=1, MMM_LUT0)",
            "primary_products_analyzed": s1
        },
        "target_localization_drxx_0based": {
            "bounding_box_sunlit_body_xy": {"x_min": 1031, "x_max": 1078, "y_min": 946, "y_max": 994},
            "bounding_box_dark_patch_xy": {"x_min": 1052, "x_max": 1092, "y_min": 967, "y_max": 1004},
            "extrapolated_apex_xy": {
                "value": [round(x, 3) for x in s3["longitudinal_edges_drxx"]["apex_intersection_full_xy"]],
                "clean_pebble_excluded": [round(x, 3) for x in s3["longitudinal_edges_drxx"]["apex_intersection_clean_xy"]],
                "uncertainty_px": [0.45, 0.42]
            },
            "proximal_arch_ventral_termination_xy": [round(float(p_ventral_corner[0]), 2), round(float(p_ventral_corner[1]), 2)],
            "proximal_arch_dorsal_termination_xy": [round(float(p_dorsal_corner[0]), 2), round(float(p_dorsal_corner[1]), 2)]
        },
        "camera_and_illumination_geometry": s2,
        "radiometry_and_psf_measurements": s3["radiometry_and_noise"],
        "longitudinal_feature_measurements": {
            "dorsal_upper_right_edge": {
                "angle_deg": round(s3["longitudinal_edges_drxx"]["dorsal_erf"]["theta_deg"], 3),
                "angle_uncertainty_deg": round(s3["longitudinal_edges_drxx"]["dorsal_erf"]["theta_uncertainty_deg"], 3),
                "span_px": round(s3["longitudinal_edges_drxx"]["dorsal_erf"]["span_px"], 2),
                "orthogonal_rms_residual_px": round(s3["longitudinal_edges_drxx"]["dorsal_erf"]["rms_orthogonal_residual_px"], 4),
                "max_orthogonal_residual_px": round(s3["longitudinal_edges_drxx"]["dorsal_erf"]["max_orthogonal_residual_px"], 4),
                "quadratic_curvature_c2_px_inv": round(s3["longitudinal_edges_drxx"]["dorsal_erf"]["quadratic_c2_px_inv"], 6),
                "quadratic_curvature_err_px_inv": round(s3["longitudinal_edges_drxx"]["dorsal_erf"]["quadratic_c2_err_px_inv"], 6),
                "curvature_z_score": round(s3["longitudinal_edges_drxx"]["dorsal_erf"]["curvature_z_score"], 2),
                "max_sagitta_px": round(s3["longitudinal_edges_drxx"]["dorsal_erf"]["max_sagitta_deviation_px"], 3)
            },
            "ventral_lower_left_edge": {
                "angle_full_deg": round(s3["longitudinal_edges_drxx"]["ventral_full_erf"]["theta_deg"], 3),
                "angle_full_uncertainty_deg": round(s3["longitudinal_edges_drxx"]["ventral_full_erf"]["theta_uncertainty_deg"], 3),
                "angle_clean_pebble_excluded_deg": round(s3["longitudinal_edges_drxx"]["ventral_clean_erf"]["theta_deg"], 3),
                "span_px": round(s3["longitudinal_edges_drxx"]["ventral_full_erf"]["span_px"], 2),
                "orthogonal_rms_full_px": round(s3["longitudinal_edges_drxx"]["ventral_full_erf"]["rms_orthogonal_residual_px"], 4),
                "orthogonal_rms_clean_px": round(s3["longitudinal_edges_drxx"]["ventral_clean_erf"]["rms_orthogonal_residual_px"], 4)
            },
            "relative_orientation_and_convergence": {
                "opening_convergence_angle_full_deg": round(s3["longitudinal_edges_drxx"]["convergence_angle_full_erf_deg"], 3),
                "opening_convergence_angle_clean_deg": round(s3["longitudinal_edges_drxx"]["convergence_angle_clean_erf_deg"], 3),
                "opening_convergence_uncertainty_deg": round(float(np.hypot(
                    s3["longitudinal_edges_drxx"]["dorsal_erf"]["theta_uncertainty_deg"],
                    s3["longitudinal_edges_drxx"]["ventral_full_erf"]["theta_uncertainty_deg"]
                )), 3),
                "bisector_angle_full_deg": round(s3["longitudinal_edges_drxx"]["bisector_angle_full_erf_deg"], 3),
                "bisector_angle_clean_deg": round(s3["longitudinal_edges_drxx"]["bisector_angle_clean_erf_deg"], 3)
            }
        },
        "terminal_boundary_and_endface_models": s4,
        "competing_3d_interpretations_and_photometry": s5,
        "apparent_dimensional_ratios_and_physical_scales": {
            "pixel_dimensions_drxx": {
                "rim_chord_width_px": round(chord_width_px, 2),
                "ellipse_major_diameter_S1_px": round(diam_s1_px, 2),
                "ellipse_major_diameter_S2_px": round(diam_s2_px, 2),
                "sunlit_axial_length_to_arch_vertex_px": round(length_to_arch_vertex_px, 2),
                "dorsal_limb_length_px": round(length_dorsal_limb_px, 2),
                "ventral_limb_length_px": round(length_ventral_limb_px, 2),
                "apparent_length_to_chord_width_ratio": round(length_dorsal_limb_px / chord_width_px, 3),
                "axial_length_to_arch_over_chord_width_ratio": round(length_to_arch_vertex_px / chord_width_px, 3)
            },
            "metric_dimensions_across_depth_scenarios": physical_dimensions_by_depth
        },
        "robustness_and_sensitivity_tests": {
            "segment_trimming_sensitivity": trim_tests,
            "subpixel_method_sensitivity": method_tests,
            "pds_product_and_linearization_sensitivity": product_tests,
            "monte_carlo_correlated_noise_perturbation": mc_noise_results
        }
    }

    s8_path = os.path.join(OUT_DIR, "step8_pebble_and_rear_terminus.json")
    if os.path.exists(s8_path):
        with open(s8_path, "r") as f:
            master_measurements["targeted_pebble_correction_and_rear_terminus_reassessment"] = json.load(f)

    with open(os.path.join(OUT_DIR, "measurements.json"), "w") as f:
        json.dump(master_measurements, f, indent=2)

    print("Step 6 Robustness & Master Measurements Saved Successfully.")
    print(json.dumps({
        "pixel_dimensions_drxx": master_measurements["apparent_dimensional_ratios_and_physical_scales"]["pixel_dimensions_drxx"],
        "best_focus_3.957m_mm": physical_dimensions_by_depth["best_focus_3.957m"],
        "product_tests": product_tests,
        "mc_noise_results": mc_noise_results
    }, indent=2))

if __name__ == "__main__":
    main()

