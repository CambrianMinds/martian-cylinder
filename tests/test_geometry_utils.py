"""Independent regression tests for geometry_utils (audit findings 2, 4, 6).

Expected values come from closed-form geometry, not from published results.
Run:  python -m unittest discover -s tests -v
"""
import math
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import geometry_utils as gu  # noqa: E402


class TestFace2Projection(unittest.TestCase):
    def test_face_ratio_gives_axis_angle(self):
        self.assertAlmostEqual(gu.view_angle_from_face_ratio(0.9335), 21.0, delta=0.05)
        self.assertAlmostEqual(gu.view_angle_from_face_ratio(1.0), 0.0, places=6)
        self.assertAlmostEqual(gu.view_angle_from_face_ratio(0.5), 60.0, places=6)

    def test_axial_factor_is_inverse_sine_not_inverse_cosine(self):
        # Audit finding 2: legacy code used 1/cos(beta)=1.082 for b/a=0.924.
        f = gu.axial_deforeshortening_factor(0.9335)
        self.assertAlmostEqual(f, 1.0 / math.sin(math.acos(0.9335)), places=9)
        self.assertGreater(f, 2.7)
        self.assertLess(f, 2.85)
        self.assertGreater(abs(f - 1.0 / 0.924), 1.5, "must differ from the legacy 1/cos factor")

    def test_forward_inverse_round_trip(self):
        for length, radius, theta in [(35, 5.5, 21), (90, 5.5, 21), (35, 5.5, 60), (20, 4, 80)]:
            p = gu.project_cylinder_orthographic(length, radius, theta)
            rec = gu.length_from_projected_axis(p["axis_2d"], p["b_over_a"])
            self.assertAlmostEqual(rec, length, places=6)
            rec2 = gu.length_from_silhouette(p["silhouette_2d"], radius, p["b_over_a"])
            self.assertAlmostEqual(rec2, length, places=6)

    def test_silhouette_is_not_axis_length(self):
        p = gu.project_cylinder_orthographic(100, 17, 21)
        self.assertGreater(p["silhouette_2d"], p["axis_2d"] + 30)

    def test_perspective_ratio_reference_case(self):
        # Audit acceptance case: 35 mm at 3957 mm, 156 deg tilt => ~0.992.
        self.assertAlmostEqual(gu.perspective_radius_ratio(35, 3957, 156), 0.992, delta=5e-4)


class TestStraightnessInvariance(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(7)
        self.x = np.arange(25, dtype=float)
        self.y = 0.5607 * self.x + rng.normal(0, 0.12, 25)

    def test_ordinary_r2_is_rotation_sensitive(self):
        # Audit finding 4.1: same points, different R^2 once rotated.
        r2_a = gu.r2_ordinary(self.x, self.y)
        xr, yr = gu.rotate_points(self.x, self.y, -29.28)  # make the line ~horizontal
        r2_b = gu.r2_ordinary(xr, yr)
        self.assertGreater(abs(r2_a - r2_b), 0.5)

    def test_tls_rmse_is_rotation_invariant(self):
        base = gu.tls_line_fit(self.x, self.y)["rmse_perp"]
        for deg in (0, 17, 45, 90, 133, 211):
            xr, yr = gu.rotate_points(self.x, self.y, deg)
            self.assertAlmostEqual(gu.tls_line_fit(xr, yr)["rmse_perp"], base, places=9)

    def test_tls_known_residual(self):
        # Points alternating +/-0.1 perpendicular to a 30 deg line => TLS RMSE ~0.1 (never above).
        t = np.arange(20, dtype=float)
        th = math.radians(30)
        d = np.array([math.cos(th), math.sin(th)])
        n = np.array([-d[1], d[0]])
        off = np.where(np.arange(20) % 2 == 0, 0.1, -0.1)
        pts = np.outer(t, d) + np.outer(off, n)
        r = gu.tls_line_fit(pts[:, 0], pts[:, 1])["rmse_perp"]
        self.assertLessEqual(r, 0.1 + 1e-12)  # TLS minimises, so <= generating noise
        self.assertAlmostEqual(r, 0.1, delta=1e-3)

    def test_curved_edge_scores_worse_than_straight(self):
        t = np.linspace(-1, 1, 25)
        straight = gu.normalized_straightness(t * 20, t * 5)
        arc = gu.normalized_straightness(20 * np.sin(t), 20 * (1 - np.cos(t)))
        self.assertGreater(arc, 5 * straight + 1e-6)

    def test_best_window_prefers_straight_subsegment(self):
        t = np.arange(60, dtype=float)
        y = np.where(t < 30, 0.0, 0.02 * (t - 30) ** 2)
        w = gu.best_straight_window(t, y, 20)
        self.assertLess(w["start"], 12)


class TestStatistics(unittest.TestCase):
    def test_empirical_rank_floor(self):
        self.assertAlmostEqual(gu.empirical_rank_p(100.0, np.arange(20.0)), 1 / 21)
        self.assertAlmostEqual(gu.empirical_rank_p(-1.0, np.arange(20.0)), 1.0)

    def test_bootstrap_ci_brackets_sd(self):
        rng = np.random.default_rng(1)
        v = rng.normal(0, 1, 20)
        lo, hi = gu.bootstrap_sd_ci(v, n_boot=500)
        self.assertLess(lo, np.std(v, ddof=1))
        self.assertGreater(hi, np.std(v, ddof=1))


if __name__ == "__main__":
    unittest.main()
