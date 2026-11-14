"""
Independent Mathematical Verification Test Suite
Part of the Argon Red-Team Audit of martian-cylinder.
Tests camera Jacobians, subpixel metrology, ODR fitting, Birge calibration,
and 3D cone geometric constraints independently of the original codebase.
"""

import unittest
import numpy as np
import json
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INDEP_DIR = os.path.join(ROOT_DIR, "independent-reconstruction")
AUDIT_DIR = os.path.join(ROOT_DIR, "audit")

class TestIndependentMath(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(INDEP_DIR, "step2_camera_geometry.json")) as f:
            cls.cam = json.load(f)
        with open(os.path.join(INDEP_DIR, "step8_pebble_and_rear_terminus.json")) as f:
            cls.s8 = json.load(f)
        with open(os.path.join(INDEP_DIR, "step9_joint_model.json")) as f:
            cls.s9 = json.load(f)
        with open(os.path.join(AUDIT_DIR, "camera_audit.json")) as f:
            cls.cam_audit = json.load(f)
        with open(os.path.join(AUDIT_DIR, "rear_arc_audit.json")) as f:
            cls.rear_audit = json.load(f)
        with open(os.path.join(AUDIT_DIR, "projective_geometry_audit.json")) as f:
            cls.proj_audit = json.load(f)

    def test_camera_jacobian_and_ifov(self):
        """Verify CAHVOR Gennery Jacobian singular values and IFOV."""
        geom = self.cam["target_viewing_geometry"]
        s1, s2 = geom["local_jacobian_singular_values_px_per_rad"]
        self.assertAlmostEqual(s1, 13498.24, delta=0.5)
        self.assertAlmostEqual(s2, 13418.43, delta=0.5)
        
        # Mean local scale
        f_mean = np.sqrt(s1 * s2)
        ifov = 1e6 / f_mean
        self.assertAlmostEqual(ifov, 74.304, delta=0.01)
        
        # Anisotropy
        anisotropy = (s1 / s2 - 1.0) * 100.0
        self.assertAlmostEqual(anisotropy, 0.5948, delta=0.01)
        self.assertLess(anisotropy, 1.0, "Distortion anisotropy must be under 1% at target")

    def test_solar_shadow_vector(self):
        """Verify solar illumination vector and image plane shadow angle."""
        sun_az = self.cam["solar_illumination_geometry"]["solar_azimuth_site_deg"]
        sun_el = self.cam["solar_illumination_geometry"]["solar_elevation_site_deg"]
        self.assertAlmostEqual(sun_az, 186.8169, delta=0.001)
        self.assertAlmostEqual(sun_el, 69.8224, delta=0.001)
        
        # Shadow angle
        shd_angle = self.cam["solar_illumination_geometry"]["shadow_cast_image_plane_angle_deg"]
        self.assertAlmostEqual(shd_angle, 63.429, delta=0.01)

    def test_pebble_outlier_impact(self):
        """Verify pebble outlier at theta=-45 deg causes 2.5x degradation in RMS."""
        f = self.s8["front_face_models_before_vs_after_single_outlier_exclusion"]
        rms_uncorrected = f["uncorrected_36pt_rim_including_theta_minus45"]["M3_Ellipse_Dorsal_Constrained_4DOF"]["rms_residual_px"]
        rms_clean = f["corrected_35pt_clean_rim_excluding_only_theta_minus45"]["M3_Ellipse_Dorsal_Constrained_4DOF"]["rms_residual_px"]
        
        self.assertAlmostEqual(rms_uncorrected, 0.4112, delta=0.001)
        self.assertAlmostEqual(rms_clean, 0.1618, delta=0.001)
        self.assertGreater(rms_uncorrected / rms_clean, 2.5)

    def test_rear_arc_likelihood_and_birge_adjustment(self):
        """Verify Question B: Profile likelihood scan, discrepancy in text, and Birge reconciliation."""
        self.assertEqual(round(self.rear_audit["best_s"], 2), 0.93)
        self.assertAlmostEqual(self.rear_audit["min_rms_px"], 0.18434, delta=0.001)
        self.assertAlmostEqual(self.rear_audit["s_1_000"]["rms_px"], 0.18629, delta=0.001)
        
        delta_rms = self.rear_audit["s_1_000"]["delta_rms_px"]
        self.assertAlmostEqual(delta_rms, 0.00195, delta=0.0001)
        
        # Delta chi2
        dchi2 = self.rear_audit["s_1_000"]["delta_chi2"]
        self.assertAlmostEqual(dchi2, 4.8216, delta=0.01)
        
        # Confirm reported 1.55 sigma defect: sqrt(dchi2 / 2) vs sqrt(dchi2)
        reported_z = self.rear_audit["s_1_000"]["z_erroneous_text"]
        self.assertAlmostEqual(reported_z, 1.5527, delta=0.01)
        
        true_uncalibrated_z = self.rear_audit["s_1_000"]["z_nominal"]
        self.assertAlmostEqual(true_uncalibrated_z, 2.1958, delta=0.01)
        
        # Birge ratio calibration
        chi2_nu = self.rear_audit["birge_calibration"]["chi2_nu"]
        self.assertGreater(chi2_nu, 10.0, "Nominal reduced chi2 must indicate severe underestimation of uncertainty")
        
        z_birge = self.rear_audit["birge_calibration"]["z_birge"]
        self.assertLess(z_birge, 1.0, "Birge-adjusted z-score must be < 1 sigma")
        self.assertAlmostEqual(z_birge, 0.684, delta=0.05)

    def test_joint_model_residuals(self):
        """Verify 85-point joint model residuals for M1, M2, and M4."""
        jm = self.s9["joint_models"]
        m1 = jm["M1_Strict_Right_Circular_Cylinder_6DOF"]
        m2 = jm["M2_Cylinder_Free_Dorsal_Crest_Offset_7DOF"]
        m4 = jm["M4_Tapered_Conical_Frustum_Coupled_8DOF"]
        
        self.assertAlmostEqual(m1["residuals_px"]["total_rms"], 0.3788, delta=0.001)
        self.assertAlmostEqual(m2["residuals_px"]["total_rms"], 0.3468, delta=0.001)
        self.assertAlmostEqual(m4["residuals_px"]["total_rms"], 0.2549, delta=0.001)
        
        # M4 parameters
        self.assertAlmostEqual(m4["params"]["scale_ratio_s"], 0.6187, delta=0.001)
        self.assertAlmostEqual(m4["params"]["theta_axis_deg"], 39.33, delta=0.05)
        self.assertAlmostEqual(m4["params"]["half_taper_alpha_deg"], 9.46, delta=0.05)

    def test_m4_conical_model_falsification(self):
        """Verify M4's physical rejection through its ellipse-line discriminant."""
        rear_shift = self.proj_audit["rear_center_shift_px"]
        self.assertAlmostEqual(rear_shift, 7.73, delta=0.1)
        self.assertAlmostEqual(self.proj_audit["m4_s"], 0.6187, delta=0.001)
        p = self.s9['joint_models']['M4_Tapered_Conical_Frustum_Coupled_8DOF']['params']
        m = (1-p['scale_ratio_s'])*p['r_dorsal']/p['L_proj']
        # Substitute v=-r-mu in u^2/b^2+v^2/a^2=1.
        A = 1/p['b']**2 + m*m/p['a']**2
        B = 2*p['r_dorsal']*m/p['a']**2
        C = p['r_dorsal']**2/p['a']**2-1
        self.assertGreater(B*B-4*A*C, 0)
        self.assertFalse(self.proj_audit['m4_tangency']['physical_tangency_satisfied'])
        self.assertAlmostEqual(self.proj_audit['m4_tangency']['intercept_shortfall_px'], 0.138863, places=5)

if __name__ == "__main__":
    unittest.main()
