"""Geometry, observation eligibility, withheld isolation and provenance checks."""
from pathlib import Path
import hashlib
import json
import sys
import unittest
import numpy as np

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]
sys.path.insert(0,str(BASE/'scripts'))
import physical_model as model
import target_benchmark as target
from control_metrology import ellipse_fit
from pds_images import read_image


class ComparisonTests(unittest.TestCase):
    def test_original_inputs_unchanged(self):
        baseline=json.loads((BASE/'sources/baseline.json').read_text())
        for relative,digest in baseline['source_hashes'].items():
            source=ROOT/relative
            if not source.exists() and source.suffix=='.py' and source.parent.name=='independent-reconstruction':
                source=source.parent/'scripts'/source.name
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),digest,relative)

    def test_target_benchmarks(self):
        result=json.loads((BASE/'results/target-benchmark/results.json').read_text())
        self.assertAlmostEqual(result['full_m1_fit']['total_rms_px'],.37882893,places=6)
        self.assertAlmostEqual(result['sparse_rear_registration']['test_rms_px'],.2084,places=4)
        self.assertAlmostEqual(result['blocked_rear_registration']['pooled_test_rms_px'],.2429,places=4)
        self.assertAlmostEqual(result['blocked_m1_prediction']['total_rms_px'],.7233,places=4)

    def test_cahvor_roundtrip(self):
        xy=np.array([[1030.,950.],[1068.,986.],[1080.,975.]])
        rays=model.rays(xy)
        np.testing.assert_allclose(model.project(model.CAMERA['C']+4*rays),xy,atol=2e-6)

    def test_analytic_ellipse_recovery(self):
        phase=np.linspace(0,2*np.pi,60,endpoint=False)
        xy=np.column_stack([100+20*np.cos(phase),100+12*np.sin(phase)])
        fit,residual=ellipse_fit(xy,{'center_xy':[100,100],'radii_xy':[20,12]})
        self.assertLess(np.sqrt(np.mean(residual**2)),1e-6)
        np.testing.assert_allclose(sorted(fit[2:4]),[12,20],atol=1e-5)

    def test_guard_masks_and_scoring(self):
        result=json.loads((BASE/'results/physical-model.json').read_text())
        for name,total in [('front',35),('rear',24),('dorsal',26)]:
            scored=[]
            for fold in result['folds']:
                group=fold['features'][name]
                test=np.array(group['test_indices']);train=np.array(group['training_indices'])
                self.assertFalse(set(test)&set(train))
                for index in train:
                    self.assertGreater(np.min(abs(test-index)),2)
                scored.extend(test)
            self.assertEqual(sorted(scored),list(range(total)))

    def test_synthetic_known_geometry_recovery(self):
        experiments=json.loads((BASE/'results/synthetic-controls.json').read_text())
        ideal=experiments[0]
        self.assertLess(ideal['total_rms_px'],.001)
        known=np.array(json.loads((BASE/'results/physical-model.json').read_text())['parameters'])
        np.testing.assert_allclose(ideal['fit_parameters'],known,atol=.01)

    def test_negative_controls_measure_deviations(self):
        results={row['id']:row for row in json.loads((BASE/'results/synthetic-controls.json').read_text())}
        self.assertGreater(results['centerline_bend_20pct_radius']['total_rms_px'],1.)
        self.assertGreater(results['radius_modulation_10pct']['total_rms_px'],.5)
        self.assertGreater(results['taper_20pct']['total_rms_px'],results['ideal']['total_rms_px'])

    def test_projection_approximation_is_small(self):
        result=json.loads((BASE/'results/physical-model.json').read_text())
        self.assertLess(max(result['conic_approximation_rms_px'].values()),.001)

    def test_partial_images_never_receive_joint_results(self):
        controls=json.loads((BASE/'results/observed-controls.json').read_text())
        for control in controls:
            self.assertNotIn('joint_fit',control)
            self.assertIn('R and D unobservable',control['scope'])

    def test_navcam_header_offsets(self):
        image,label=read_image(BASE/'sources/images/NRB_445620806EDR_F0261274NCAM00354M1.IMG')
        self.assertEqual(image.shape,(1024,1024))
        self.assertTrue(np.all(np.isfinite(image)))
        self.assertLess(image.max(),65536)

    def test_burial_fit_is_not_visibility_proof(self):
        result=json.loads((BASE/'results/physical-model.json').read_text())
        case=result['burial_visibility']['plane_cases'][0]
        self.assertLess(case['soil_contact_rms_px'],.3)
        self.assertEqual(case['approximate_pixel_support_within_1px']['front'],0)

    def test_frustum_generator_is_physical_surface_tangent(self):
        record=json.loads((BASE/'results/physical-frustum.json').read_text())
        p=np.array(record['parameters']);g=model.geometry(p)
        offset=g['front']-model.CAMERA['C']
        slope=g['radius']*(1-p[6])/g['length']
        first=offset@g['first'];second=offset@g['second']
        phase0=np.arctan2(second,first)
        delta=np.arccos((slope*(offset@g['axis'])-g['radius'])/np.hypot(first,second))
        for phase in [phase0-delta,phase0+delta]:
            radial=np.cos(phase)*g['first']+np.sin(phase)*g['second']
            transverse=-np.sin(phase)*g['first']+np.cos(phase)*g['second']
            along=g['axis']+slope*radial
            normal=model.unit(np.cross(transverse,along))
            for fraction in [0,.5,1]:
                point=g['front']-fraction*g['length']*g['axis']+g['radius']*(1+fraction*(p[6]-1))*radial
                view=model.unit(point-model.CAMERA['C'])
                self.assertLess(abs(view@normal),1e-10)

    def test_exploratory_frustum_guarded_isolation(self):
        result=json.loads((BASE/'results/physical-frustum.json').read_text())
        for fold in result['folds']:
            for name,group in fold['features'].items():
                for index in group['training_indices']:
                    self.assertGreater(min(abs(index-j) for j in group['test_indices']),2)

    def test_report_numbers_come_from_saved_results(self):
        report=(BASE/'report.md').read_text(encoding='utf-8')
        result=json.loads((BASE/'results/physical-model.json').read_text())
        frustum=json.loads((BASE/'results/physical-frustum.json').read_text())
        for value in [result['full_fit']['total_rms_px'],result['guarded_prediction']['total_rms_px'],
                      frustum['full_rms_px'],frustum['guarded_rms_px']]:
            self.assertIn(f'{value:.4f}',report)

    def test_finite_generator_rejects_line_extension(self):
        data,_,_=target.load_data()
        record=json.loads((BASE/'results/physical-frustum.json').read_text())
        p=np.array(record['parameters'])
        _,line=model.projected_boundaries(p)
        trial={name:{key:value.copy() for key,value in group.items()} for name,group in data.items()}
        trial['dorsal']['xy'][0]=line[1]+.2*(line[1]-line[0])
        extended=model.residuals(p,trial)['dorsal'][0]
        finite=model.residuals(p,trial,finite_generator=True)['dorsal'][0]
        self.assertLess(abs(extended),1e-8)
        self.assertAlmostEqual(finite,.2*np.linalg.norm(line[1]-line[0]),places=8)


if __name__=='__main__':
    unittest.main()
