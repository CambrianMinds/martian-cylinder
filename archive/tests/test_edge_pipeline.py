"""Synthetic-image tests for the shared edge pipeline in audit_reanalysis.py (audit finding 4)."""
import os
import sys
import unittest

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import audit_reanalysis as ar  # noqa: E402


def step_image(shape, angle_deg, curvature=0.0, noise=0.0, seed=0):
    """Bright half-plane whose boundary is a line at angle_deg (optionally parabolic)."""
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(float)
    t = np.radians(angle_deg)
    d = (-(xx - w / 2) * np.sin(t) + (yy - h / 2) * np.cos(t))  # signed perpendicular distance
    s = (xx - w / 2) * np.cos(t) + (yy - h / 2) * np.sin(t)
    d = d - curvature * s ** 2
    img = 1.0 / (1.0 + np.exp(-d / 0.8)) * 100 + 50
    if noise:
        img = img + np.random.default_rng(seed).normal(0, noise, img.shape)
    return img


class TestSharedPipeline(unittest.TestCase):
    def rmse(self, img):
        _, _, G = ar.sobel(img)
        h, w = img.shape
        return ar.common_edge_pipeline(G, [2, 2, w - 2, h - 2])["rmse_perp"]

    def test_straight_edge_is_straight_at_any_orientation(self):
        vals = [self.rmse(step_image((60, 60), a, noise=1.0)) for a in (0, 15, 29, 45, 70, 90)]
        for v in vals:
            self.assertLess(v, 0.35)

    def test_curved_edge_scores_worse(self):
        straight = self.rmse(step_image((60, 60), 20, noise=1.0))
        curved = self.rmse(step_image((60, 60), 20, curvature=0.02, noise=1.0))
        self.assertGreater(curved, 2 * straight)

    def test_transpose_invariance(self):
        img = step_image((60, 60), 25, noise=1.0, seed=3)
        self.assertAlmostEqual(self.rmse(img), self.rmse(img.T.copy()), delta=0.08)


if __name__ == "__main__":
    unittest.main()

