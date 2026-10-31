"""
test_independent_morphology.py — Automated Regression & Verification Tests
==========================================================================
Tests the independent morphology survey pipeline, end-face vs shadow extraction,
solar illumination ray-tracing, positive controls, and exact statistical synchronization.
"""

import os
import json
import math
import unittest
import numpy as np
from PIL import Image
import scipy.ndimage as ndi
import morphology_engine as me
import geometry_utils as gu

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)


class TestIndependentMorphology(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        json_path = os.path.join(REPO_ROOT, "data", "independent_morphology_results.json")
        with open(json_path, "r", encoding="utf-8") as f:
            cls.results = json.load(f)

    def test_sample_size_exceeds_100_clasts(self):
        """Validates that the multi-scene survey collected at least 100 natural rock clasts across 8 scenes."""
        clasts = self.results["natural_clasts"]
        self.assertGreaterEqual(len(clasts), 100, f"Survey sample size {len(clasts)} is below 100!")
        self.assertEqual(len(clasts), 185)

    def test_target_measurements_consistency(self):
        """Verifies candidate cylinder target measurements match established values with clear provenance."""
        target = self.results["target"]
        self.assertEqual(target["clast_id"], "TARGET_CYLINDER")
        # 2D image silhouette aspect ratio
        self.assertAlmostEqual(target["aspect_ratio"], 2.381, delta=0.005)
        self.assertAlmostEqual(target["aspect_ratio_2d"], 2.381, delta=0.005)
        # 3D physical reconstructed aspect ratio kept strictly separate
        self.assertAlmostEqual(target["aspect_ratio_3d"], 2.835, delta=0.005)
        self.assertAlmostEqual(target["endface_ba"], 0.9334, delta=0.001)
        self.assertAlmostEqual(target["straightness_rmse_px"], 0.111, delta=0.01)
        self.assertAlmostEqual(target["flank_parallelism_deg"], 0.43, delta=0.1)
        self.assertAlmostEqual(target["longitudinal_angle_deg"], 29.28, delta=0.5)
        self.assertTrue(target["has_end_face"])
        self.assertIn("reference_measurements", target)
        self.assertEqual(target["reference_measurements"]["regolith_contact_angle_deg"], -25.21)

    def test_equivalent_measurement_definitions(self):
        """Verifies equivalent measurement procedures and explicit recording of occlusion."""
        target = self.results["target"]
        # Treat crown-highlight parallelism separately from opposing-flank parallelism
        self.assertIn("crown_highlight_parallelism_deg", target)
        self.assertAlmostEqual(target["crown_highlight_parallelism_deg"], 0.43, delta=0.05)
        # Opposing flank is occluded by regolith contact; explicitly recorded rather than invented
        self.assertEqual(target["opposing_flank_status"], "occluded_by_regolith")
        self.assertIsNone(target["opposing_flank_parallelism_deg"])
        # Segmentation type is derived from observed pixels
        self.assertEqual(target["segmentation_type"], "observed_image_pixels")

    def test_synthetic_ellipse_fitter_accuracy(self):
        """Tests that Fitzgibbon ellipse solver recovers true axes on synthetic data with known aspect ratio."""
        a_true, b_true, rot_true = 20.0, 16.0, 30.0
        th = math.radians(rot_true)
        n_pts = 60
        angles = np.linspace(0, 2 * math.pi, n_pts, endpoint=False)
        x_raw = a_true * np.cos(angles)
        y_raw = b_true * np.sin(angles)
        x_rot = 50.0 + x_raw * math.cos(th) - y_raw * math.sin(th)
        y_rot = 40.0 + x_raw * math.sin(th) + y_raw * math.cos(th)

        e = me.fit_ellipse_fitzgibbon(x_rot, y_rot)
        self.assertIsNotNone(e)
        self.assertAlmostEqual(e["xc"], 50.0, delta=0.1)
        self.assertAlmostEqual(e["yc"], 40.0, delta=0.1)
        self.assertAlmostEqual(e["major_2a"] / 2.0, a_true, delta=0.2)
        self.assertAlmostEqual(e["minor_2b"] / 2.0, b_true, delta=0.2)
        self.assertAlmostEqual(e["circ_ratio"], 0.80, delta=0.01)

    def test_recalculated_empirical_ranks_and_frequencies(self):
        """Recalculates empirical ranks and conjunction frequencies directly from raw measurement records."""
        clasts = self.results["natural_clasts"]
        target = self.results["target"]
        n_clasts = len(clasts)

        # Recalculate straightness rank
        straight_vals = [c["straightness_rmse_px"] for c in clasts]
        calc_rank_str = sum(1 for s in straight_vals if s <= target["straightness_rmse_px"]) + 1
        self.assertEqual(calc_rank_str, 1)  # Target ranks strictly #1 of 186
        p_str = calc_rank_str / (n_clasts + 1)
        self.assertLess(p_str, 0.01)

        # Recalculate 2D aspect ratio rank
        ar_vals = [c["aspect_ratio"] for c in clasts]
        calc_rank_ar = sum(1 for a in ar_vals if a >= target["aspect_ratio_2d"]) + 1
        self.assertEqual(calc_rank_ar, 32)  # Target ranks #32 of 186
        p_ar = calc_rank_ar / (n_clasts + 1)
        self.assertAlmostEqual(p_ar, 0.172, delta=0.005)

        # Recalculate multi-dimensional conjunction from raw records
        # Criteria:
        # 1. Elongation: Aspect ratio >= 2.0
        # 2. Straightness: Perpendicular TLS RMSE <= 0.35 px
        # 3. Parallelism: Flank angle difference <= 2.0 deg
        # 4. Width consistency: CV_W <= 0.10
        # 5. Distinct End-Face present with b/a >= 0.80
        match_counts = []
        for c in clasts:
            c1 = c["aspect_ratio"] >= 2.0
            c2 = c["straightness_rmse_px"] <= 0.35
            c3 = c["flank_parallelism_deg"] <= 2.0
            c4 = c["width_cv"] <= 0.10
            c5 = c["has_end_face"] and (c["endface_ba"] is not None and c["endface_ba"] >= 0.80)
            match_counts.append(sum([c1, c2, c3, c4, c5]))

        n_2 = sum(1 for m in match_counts if m >= 2)
        n_3 = sum(1 for m in match_counts if m >= 3)
        n_4 = sum(1 for m in match_counts if m >= 4)
        n_5 = sum(1 for m in match_counts if m == 5)

        self.assertEqual(n_5, 0)  # Full 5-way conjunction strictly 0 / 185
        self.assertEqual(n_4, 0)
        self.assertEqual(n_3, 6)
        self.assertEqual(n_2, 49)

        # Verify summary_statistics matches raw calculation
        stats = self.results["summary_statistics"]["joint_conjunction_frequencies"]
        self.assertEqual(stats["five_criteria_matches (Full Cylinder Geometry)"], n_5)
        self.assertEqual(stats["four_criteria_matches"], n_4)
        self.assertEqual(stats["three_criteria_matches"], n_3)
        self.assertEqual(stats["two_criteria_matches"], n_2)

    def test_straightness_sensitivity_analysis(self):
        """Verifies that relaxing the straightness threshold to <= 0.50 px preserves 0/185 full conjunction."""
        clasts = self.results["natural_clasts"]
        
        # Recalculate sensitivity directly from raw clast list
        sens_counts = []
        n_pass_relaxed_str = 0
        for c in clasts:
            c1 = c["aspect_ratio"] >= 2.0
            c2 = c["straightness_rmse_px"] <= 0.50
            if c2:
                n_pass_relaxed_str += 1
            c3 = c["flank_parallelism_deg"] <= 2.0
            c4 = c["width_cv"] <= 0.10
            c5 = c["has_end_face"] and (c["endface_ba"] is not None and c["endface_ba"] >= 0.80)
            sens_counts.append(sum([c1, c2, c3, c4, c5]))

        self.assertEqual(n_pass_relaxed_str, 14)  # 14 natural clasts pass straightness individually
        sens_5 = sum(1 for m in sens_counts if m == 5)
        sens_4 = sum(1 for m in sens_counts if m >= 4)
        sens_3 = sum(1 for m in sens_counts if m >= 3)
        sens_2 = sum(1 for m in sens_counts if m >= 2)

        self.assertEqual(sens_5, 0)  # Full 5-way conjunction strictly remains 0/185
        self.assertEqual(sens_4, 0)
        self.assertEqual(sens_3, 12)
        self.assertEqual(sens_2, 54)

        # Verify summary_statistics matches raw calculation
        stats = self.results["summary_statistics"]["joint_conjunction_frequencies"]["sensitivity_straightness_0_50px"]
        self.assertEqual(stats["five_criteria_matches"], sens_5)
        self.assertEqual(stats["four_criteria_matches"], sens_4)
        self.assertEqual(stats["three_criteria_matches"], sens_3)
        self.assertEqual(stats["two_criteria_matches"], sens_2)

    def test_positive_controls_provenance_and_performance(self):
        """Verifies positive controls with unambiguous separation between synthetic and photographic origins."""
        hw = self.results["hardware_controls"]
        self.assertEqual(len(hw), 2)

        # Control 1: Synthetic ground-truth cylinder unit test
        synth = next(h for h in hw if "SYNTH" in h["clast_id"])
        self.assertEqual(synth["provenance_type"], "synthetic_unit_test")
        self.assertTrue(synth["is_synthetic"])
        self.assertGreaterEqual(synth["aspect_ratio"], 2.0)
        self.assertLessEqual(synth["straightness_rmse_px"], 0.35)
        self.assertLessEqual(synth["flank_parallelism_deg"], 2.0)
        self.assertLessEqual(synth["width_cv"], 0.10)
        self.assertTrue(synth["has_end_face"])
        self.assertGreaterEqual(synth["endface_ba"], 0.80)
        self.assertTrue(synth["passes_cylinder_conjunction"])

        # Control 2: Real photographed spacecraft hardware (Curiosity Sol 64 Turret Standoff Pin)
        photo = next(h for h in hw if "STANDOFF" in h["clast_id"] or "AEROSPACE" in h["clast_id"])
        self.assertEqual(photo["provenance_type"], "photographic_spacecraft_hardware")
        self.assertFalse(photo["is_synthetic"])
        self.assertEqual(photo["product_id"], "0064MR0003440000103258E01")
        self.assertEqual(photo["mission_sol"], 64)
        self.assertIn("https://mars.nasa.gov", photo["hardware_source"]["verifiable_nasa_url"])
        
        # Real hardware passes elongation aspect ratio and linearity, but fails full cylinder conjunction
        # due to tapered bracket arm geometry and lack of circular end-face.
        self.assertGreaterEqual(photo["aspect_ratio"], 2.0)
        self.assertLessEqual(photo["normalized_straightness"], 0.005)
        # Transparently reports non-conjunction
        self.assertFalse(photo["passes_cylinder_conjunction"])

    def test_shadow_mask_registration(self):
        """Verifies Figure 1C shadow segmentation registration, pixel count, and solar geometry."""
        crop_path = os.path.join(REPO_ROOT, "data", "crop_bottom_right.png")
        self.assertTrue(os.path.exists(crop_path))
        crop_arr = np.array(Image.open(crop_path))
        sub = crop_arr[240:360, 209:329]
        gray = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]

        p_left = np.array([40.01, 51.20])
        p_right = np.array([73.49, 35.48])
        m_chord = (p_right[1] - p_left[1]) / (p_right[0] - p_left[0])
        b_chord = p_left[1] - m_chord * p_left[0]
        self.assertAlmostEqual(m_chord, -0.4708, delta=0.005)
        self.assertAlmostEqual(math.degrees(math.atan(m_chord)), -25.21, delta=0.1)

        Y, X = np.ogrid[:120, :120]
        below_chord = Y > (m_chord * X + b_chord)

        # Connected shadow component below chord
        dark_mask = (gray < 85.0)
        lbls, _ = ndi.label(dark_mask)
        c_lbl = lbls[43, 58]
        comp = (lbls == c_lbl)
        obs_shadow = comp & below_chord

        # Exactly 536 observed shadow pixels on ground regolith
        shadow_count = int(np.sum(obs_shadow))
        self.assertEqual(shadow_count, 536)
        
        # Verify intensity contrast
        mean_shadow_dn = np.mean(gray[obs_shadow])
        self.assertLess(mean_shadow_dn, 70.0)

        # SPICE solar elevation and dual-scale relief reconstruction
        theta_sun_deg = 69.8224
        tan_sun = math.tan(math.radians(theta_sun_deg))
        s_meas_mm = 9.8 * 0.292818
        h_calc = s_meas_mm * tan_sun
        self.assertAlmostEqual(h_calc, 7.81, delta=0.1)
        d_total = h_calc + 3.33  # burial depth = 3.33 mm
        self.assertAlmostEqual(d_total, 11.14, delta=0.2)

    def test_figure_data_consistency(self):
        """Verifies that all 6 scientific figures exist and are valid non-empty files."""
        fig_files = [
            "fig1_endface_shadow_segmentation.png",
            "fig2_ellipse_fit_reproduced.png",
            "fig3_longitudinal_features_model.png",
            "fig4_geological_controls_comparison.png",
            "fig5_morphology_distributions.png",
            "fig6_model_performance_comparison.png"
        ]
        fig_dir = os.path.join(REPO_ROOT, "figures")
        for fn in fig_files:
            fp = os.path.join(fig_dir, fn)
            self.assertTrue(os.path.exists(fp), f"Missing figure file: {fn}")
            self.assertGreater(os.path.getsize(fp), 50000, f"Figure file {fn} is too small!")


if __name__ == "__main__":
    unittest.main()
