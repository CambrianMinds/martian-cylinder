import unittest
import numpy as np
import json,csv,hashlib,gzip
from analyze import ROOT,OUT,line_fit,ellipse_fit,windows,gray,sample_window
from scipy import ndimage as ndi
from skimage.measure import find_contours

class TestMeasurements(unittest.TestCase):
    def test_rotated_line_and_known_roughness(self):
        rng=np.random.default_rng(76)
        u=np.linspace(-18.2,18.2,1000);v=rng.normal(0,.25,len(u))
        th=.53;p=np.column_stack([u*np.cos(th)-v*np.sin(th),u*np.sin(th)+v*np.cos(th)])
        rms,angle=line_fit(p)
        self.assertAlmostEqual(rms,.25,delta=.02)
        self.assertAlmostEqual(angle,np.degrees(th),delta=.1)

    def test_partial_ellipse_and_line_not_equivalent(self):
        t=np.linspace(0,np.pi,35)
        p=np.column_stack([20*np.cos(t),16*np.sin(t)])+[80,70]
        e=ellipse_fit(p)
        self.assertIsNotNone(e)
        self.assertLess(e['ellipse_rms_px'],1e-7)
        self.assertAlmostEqual(e['b_over_a'],.8,places=5)
        self.assertGreater(line_fit(p)[0],3)

    def test_real_contour_detector_on_synthetic_straight_step(self):
        y,x=np.mgrid[:80,:80]
        a=40+140/(1+np.exp((y-.5*x-20)/.8))
        records=list(windows(a,36.4,.7,'line','synthetic'))
        self.assertTrue(records)
        # Coordinates/residuals are converted back from binned sampling.
        self.assertLess(np.median([r['rms_px'] for r,p in records]),.3)

    def test_original_image_checksums(self):
        rows=json.loads((OUT/'image-manifest.json').read_text())['images']
        for r in rows:
            if 'path'in r:
                self.assertEqual(hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest(),r['sha256'])

    def test_counts_and_target_exclusion_recomputed_from_export(self):
        summary=json.loads((OUT/'comparison-summary.json').read_text())['sigma0.7_span36.4']
        n=below=0
        with gzip.open(OUT/'edge-windows-sigma0.7_span36.4.csv.gz','rt',encoding='utf-8') as f:
            for row in csv.DictReader(f):
                n+=1;below+=float(row['rms_px'])<=summary['target_selected']['rms_px']
                if row['scene']=='sol3556_585':
                    self.assertFalse(1015<float(row['x'])<1110 and 925<float(row['y'])<1020)
        self.assertEqual(n,summary['n_control_windows'])
        self.assertEqual(below,summary['n_at_or_below_target'])

    def test_exported_target_coordinates_reproduce_residual(self):
        r=json.loads((OUT/'comparison-summary.json').read_text())['sigma0.7_span36.4']['target_selected']
        a=ndi.gaussian_filter(gray(OUT/'images/sol3556_585.jpg'),r['sigma_px']/2)
        contour=find_contours(a,r['level_dn'],fully_connected='high')[r['contour']]
        arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(contour,axis=0),axis=1))]
        pts=sample_window(contour,arc,r['start_arc_px']/2,r['span_px']/2,26)*2+.5
        self.assertAlmostEqual(line_fit(pts)[0],r['rms_px'],places=9)
        np.testing.assert_allclose(pts.mean(0),[r['x'],r['y']],atol=1e-9)

if __name__=='__main__':unittest.main()
