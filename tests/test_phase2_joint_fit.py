"""
Unit tests for Phase II Joint 3D Geometric Fits and Orientation Unidentifiability.
"""

import math
import unittest
import numpy as np
import joint_geometry_fit as jgf
from reproduce_analysis import fit_ellipse_fitzgibbon

class TestPhase2JointFit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = jgf.extract_ground_truth_points()

    def test_cylinder_projection_basic(self):
        """Model A forward projection must generate valid closed loops and generators."""
        p = [57.66, 42.99, 5.92, 33.59, 29.86, 23.89, 4.21]
        geom = jgf.project_cylinder_model(p)
        xr, yr = geom['front_rim']
        xg, yg = geom['gen_up']
        self.assertEqual(len(xr), 64)
        self.assertEqual(len(xg), 32)
        # Check that front center is near (57.66, 42.99)
        self.assertAlmostEqual(np.mean(xr), 57.66, delta=1.0)
        self.assertAlmostEqual(np.mean(yr), 42.99, delta=1.0)

    def test_cylinder_model_residual_on_real_data(self):
        """Optimized cylinder model must achieve RMSE < 2.0 px on extracted points."""
        p_opt = [57.66, 42.99, 5.92, 33.59, 29.86, 23.89, 4.21]
        geom = jgf.project_cylinder_model(p_opt)
        chi2, rmse, n, _ = jgf.compute_model_loss(geom, self.data)
        self.assertLess(rmse, 2.0)
        self.assertEqual(n, 114)

    def test_fracture_slab_poorer_fit_than_cylinder(self):
        """Rectangular fracture slab must have significantly higher chi2 than circular cylinder."""
        p_cyl = [57.66, 42.99, 5.92, 33.59, 29.86, 23.89, 4.21]
        g_cyl = jgf.project_cylinder_model(p_cyl)
        chi2_cyl, _, _, _ = jgf.compute_model_loss(g_cyl, self.data)

        p_slab = [57.98, 43.17, 9.63, 9.51, 29.97, 19.71, 33.61, 3.84]
        g_slab = jgf.project_fracture_slab_model(p_slab)
        chi2_slab, _, _, _ = jgf.compute_model_loss(g_slab, self.data)

        self.assertGreater(chi2_slab, chi2_cyl * 1.5)

    def test_ellipse_orientation_unidentifiability(self):
        """For near-circular ellipse (b/a ~ 0.934), orientation error with 0.5px noise exceeds 30 deg."""
        np.random.seed(123)
        a, b = 18.85, 17.61
        th_true = math.radians(29.28)
        t = np.linspace(0, 2*np.pi, 96, endpoint=False)
        x_el = a * np.cos(t) * (-math.sin(th_true)) + b * np.sin(t) * math.cos(th_true)
        y_el = a * np.cos(t) * (math.cos(th_true)) + b * np.sin(t) * math.sin(th_true)

        errors = []
        for _ in range(50):
            xn = x_el + np.random.normal(0, 0.5, size=x_el.shape)
            yn = y_el + np.random.normal(0, 0.5, size=y_el.shape)
            e = fit_ellipse_fitzgibbon(xn, yn)
            # Compute minor axis
            xm, ym = np.mean(xn), np.mean(yn)
            scale = max(np.std(xn), np.std(yn), 1.0)
            u = (xn - xm) / scale
            v = (yn - ym) / scale
            D1 = np.column_stack([u**2, u * v, v**2])
            D2 = np.column_stack([u, v, np.ones_like(u)])
            S1 = D1.T @ D1; S2 = D1.T @ D2; S3 = D2.T @ D2
            C1 = np.array([[0.0, 0.0, 2.0], [0.0, -1.0, 0.0], [2.0, 0.0, 0.0]])
            T = -np.linalg.inv(S3) @ S2.T
            M = np.linalg.inv(C1) @ (S1 + S2 @ T)
            eigvals, eigvecs = np.linalg.eig(M)
            cond = 4.0 * eigvecs[0, :] * eigvecs[2, :] - eigvecs[1, :] ** 2
            valid = np.where(cond > 0)[0]
            idx = valid[np.argmin(np.abs(eigvals[valid]))]
            a1 = np.real(eigvecs[:, idx])
            a2 = T @ a1
            A, B, C, D, E, F = np.concatenate([a1, a2])
            Q = np.array([[A, B/2], [B/2, C]])
            w, V = np.linalg.eigh(Q)
            minor_v = V[:, np.argmax(w)]
            minor_deg = float(np.degrees(np.arctan2(minor_v[1], minor_v[0])) % 180.0)
            d_th = abs(minor_deg - 29.28) % 180.0
            if d_th > 90.0:
                d_th = 180.0 - d_th
            errors.append(d_th)

        mean_err = np.mean(errors)
        self.assertGreater(mean_err, 30.0)

if __name__ == '__main__':
    unittest.main()

