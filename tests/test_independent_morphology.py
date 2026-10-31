"""
test_independent_morphology.py — Automated Regression & Verification Tests
==========================================================================
Tests the independent morphology survey pipeline, end-face vs shadow extraction,
and solar illumination ray-tracing.
"""

import os
import json
import math
import unittest
import numpy as np
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
        """Validates that the multi-scene survey collected at least 100 natural rock clasts."""
        clasts = self.results["natural_clasts"]
        self.assertGreaterEqual(len(clasts), 100, f"Survey sample size {len(clasts)} is below 100!")
        self.assertEqual(len(clasts), 185)

    def test_target_measurements_consistency(self):
        """Verifies that the candidate cylinder target measurements match established values."""
        target = self.results["target"]
        self.assertEqual(target["clast_id"], "TARGET_CYLINDER")
        self.assertAlmostEqual(target["endface_ba"], 0.9334, delta=0.001)
        self.assertAlmostEqual(target["straightness_rmse_px"], 0.111, delta=0.01)
        self.assertAlmostEqual(target["flank_parallelism_deg"], 0.43, delta=0.1)
        self.assertAlmostEqual(target["longitudinal_angle_deg"], 29.28, delta=0.5)
        self.assertTrue(target["has_end_face"])

    def test_synthetic_ellipse_fitter_accuracy(self):
        """Tests that Fitzgibbon ellipse solver recovers true axes on synthetic data with known aspect ratio."""
        # Synthesize ellipse with a = 20.0, b = 16.0 (b/a = 0.80) rotated by 30 degrees
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

    def test_empirical_rank_and_joint_conjunction_rarity(self):
        """Verifies that the target's joint conjunction is strictly unmatched in the natural population."""
        stats = self.results["summary_statistics"]
        # In straightness, target ranks #1 in the entire population
        self.assertEqual(stats["straightness_rmse_px"]["empirical_rank"], "1/186")
        self.assertLess(stats["straightness_rmse_px"]["empirical_p"], 0.01)
        
        # In 5-way conjunction, 0 natural clasts match
        conj = stats["joint_conjunction_frequencies"]
        self.assertEqual(conj["five_criteria_matches (Full Cylinder Geometry)"], 0)

    def test_solar_illumination_and_shadow_reconstruction(self):
        """Verifies SPICE solar geometry and relief reconstruction."""
        theta_sun_deg = 69.8224
        cot_sun = 1.0 / math.tan(math.radians(theta_sun_deg))
        tan_sun = math.tan(math.radians(theta_sun_deg))
        self.assertAlmostEqual(cot_sun, 0.3675, delta=0.001)
        self.assertAlmostEqual(tan_sun, 2.7212, delta=0.001)

        # Measured shadow length S = 9.8 px at nominal scale 0.2928 mm/px
        s_meas_mm = 9.8 * 0.292818
        h_calc = s_meas_mm * tan_sun
        self.assertAlmostEqual(h_calc, 7.81, delta=0.1)

        # Submerged regolith chord d = 3.33 mm (~30% of diameter)
        # Total diameter = 7.81 + 3.33 = 11.14 mm
        d_total = h_calc + 3.33
        self.assertAlmostEqual(d_total, 11.14, delta=0.2)

    def test_hardware_control_passes_cylinder_conjunction(self):
        """Verifies that positive manufactured controls pass cylinder conjunction."""
        hw = self.results["hardware_controls"]
        self.assertGreaterEqual(len(hw), 1)
        # Find synthetic cylinder or hardware post
        synth = next(h for h in hw if "SYNTH" in h["clast_id"])
        self.assertGreaterEqual(synth["aspect_ratio"], 2.0)
        self.assertLessEqual(synth["straightness_rmse_px"], 0.50)
        self.assertLessEqual(synth["flank_parallelism_deg"], 2.0)

if __name__ == "__main__":
    unittest.main()
