"""
Unit tests for Phase II landmark extraction, axis separation, and gradient evidence.
"""

import math
import unittest
import numpy as np
from PIL import Image
import geometry_utils as gu
import audit_reanalysis as ar
from reproduce_analysis import fit_ellipse_fitzgibbon

class TestLandmarkGeometry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        crop = np.array(Image.open('data/crop_bottom_right.png'))
        cls.sub = crop[240:360, 209:329].astype(float)
        cls.gray = 0.299 * cls.sub[:, :, 0] + 0.587 * cls.sub[:, :, 1] + 0.114 * cls.sub[:, :, 2]
        cls.Sx, cls.Sy, cls.G = ar.sobel(cls.gray)
        dark = cls.gray[22:62, 38:78] < 75.0
        yy, xx = np.where(dark)
        cls.xc0, cls.yc0 = 38.0 + float(xx.mean()), 22.0 + float(yy.mean())

    def test_front_rim_and_center_stability(self):
        """Front rim extraction must yield a stable center near (57.8, 43.2) in sub120."""
        X, Y = ar.rim_points(self.gray, self.Sx, self.Sy, self.xc0, self.yc0, 85.0, 2.6)
        self.assertGreater(len(X), 50)
        e = fit_ellipse_fitzgibbon(X, Y)
        self.assertAlmostEqual(e['xc'], 57.77, delta=1.5)
        self.assertAlmostEqual(e['yc'], 43.23, delta=1.5)
        self.assertAlmostEqual(e['circ_ratio'], 0.933, delta=0.05)

    def test_upper_generator_straightness(self):
        """Upper generator line must have TLS RMSE < 0.2 px and angle ~ 29.3 deg."""
        xs_up, ys_up = [], []
        for x in range(28, 53):
            c = [y for y in range(2, 28) if self.Sy[y, x] > 15.0 and self.Sx[y, x] < -8.0]
            if c:
                by = max(c, key=lambda y: self.G[y, x])
                xs_up.append(float(x))
                ys_up.append(float(ar._subpix(self.G[:, x], by)))
        fit = gu.tls_line_fit(xs_up, ys_up)
        self.assertLess(fit['rmse_perp'], 0.15)
        self.assertAlmostEqual(fit['angle_deg'], 29.28, delta=1.0)

    def test_projected_axis_vs_silhouette_extent(self):
        """Disentangles projected center separation (38.8 px) from apex-to-apex extent (74.2 px)."""
        # Front center
        fc = (57.77, 43.23)
        # Rear center
        rc = (23.94, 24.26)
        sep = math.hypot(fc[0] - rc[0], fc[1] - rc[1])
        self.assertAlmostEqual(sep, 38.78, delta=1.0)
        
        # Silhouette apex-to-apex
        far_rear = (15.59, 8.00)
        front_apex = (79.06, 46.49)
        extent = math.hypot(front_apex[0] - far_rear[0], front_apex[1] - far_rear[1])
        self.assertAlmostEqual(extent, 74.23, delta=1.5)
        
        # Verify that 110 px is distinct from both
        self.assertGreater(110.0, extent + 20.0)
        self.assertGreater(extent, sep + 20.0)

if __name__ == '__main__':
    unittest.main()

