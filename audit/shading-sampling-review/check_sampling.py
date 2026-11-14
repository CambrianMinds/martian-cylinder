"""Replay original and current Step 5 profile selections on the same image."""
from pathlib import Path
import json
import subprocess
import sys

import numpy as np
from scipy.ndimage import map_coordinates

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL_REVISION = 'd0a63274ada472d77a905268366f2fcbd21eed3d'
sys.path.insert(0, str(ROOT / 'independent-reconstruction/scripts'))
from step3_feature_extraction import load_drxx


def measure_profiles(image, edges, native_spacing):
    angle = np.radians(edges['bisector_angle_full_erf_deg'])
    axis = np.array([np.cos(angle), np.sin(angle)])
    normal = np.array([axis[1], -axis[0]])
    origin = np.array(edges['apex_intersection_full_xy'])
    positions, radiances, groups, profiles = [], [], [], []
    for index, station in enumerate([15, 18.5, 22, 25.5, 29]):
        half_width = station * np.tan(np.radians(edges['convergence_angle_full_erf_deg'] / 2))
        count = int(np.floor(1.44 * half_width)) + 1 if native_spacing else 29
        transverse = np.linspace(-.72, .72, count)
        xy = origin + station * axis + (transverse * half_width)[:, None] * normal
        radiance = map_coordinates(image, [xy[:, 1], xy[:, 0]], order=1, mode='nearest')
        normalized = radiance / radiance.mean()
        positions.extend(transverse)
        radiances.extend(normalized)
        groups.extend([index] * count)
        profiles.append({'station_px': station, 'xy': xy.tolist(),
                         'normalized_radiance': normalized.tolist(),
                         'curvature_coefficient': float(np.polyfit(transverse, normalized, 2)[0])})
    positions, radiances, groups = map(np.asarray, [positions, radiances, groups])
    coefficients, covariance = np.polyfit(positions, radiances, 2, cov=True)
    error = float(np.sqrt(covariance[0, 0]))
    return {
        'samples': len(positions),
        'curvature_coefficient': float(coefficients[0]),
        'nominal_error': error,
        'nominal_z': float(abs(coefficients[0]) / error),
        'leave_one_profile_out_curvature': [
            float(np.polyfit(positions[groups != index], radiances[groups != index], 2)[0])
            for index in range(5)],
        'profiles': profiles,
    }


def main():
    original = json.loads(subprocess.check_output(
        ['git', 'show', ORIGINAL_REVISION + ':independent-reconstruction/step3_features.json'],
        cwd=ROOT))['longitudinal_edges_drxx']
    current = json.loads((ROOT / 'independent-reconstruction/step3_features.json').read_text())[
        'longitudinal_edges_drxx']
    _, _, image = load_drxx()
    results = {
        'original_revision': ORIGINAL_REVISION,
        'origin_displacement_px': float(np.linalg.norm(
            np.array(original['apex_intersection_full_xy']) - current['apex_intersection_full_xy'])),
        'scope': 'Nominal polynomial-fit uncertainties. Native spacing and omitted-profile checks '
                 'are sensitivity checks. No spatial-covariance calibration is applied.',
    }
    for name, edges in [('original', original), ('current', current)]:
        results[name] = {
            'origin_xy': edges['apex_intersection_full_xy'],
            'bisector_angle_deg': edges['bisector_angle_full_erf_deg'],
            'original_density': measure_profiles(image, edges, native_spacing=False),
            'native_spacing': measure_profiles(image, edges, native_spacing=True),
        }
    output = Path(__file__).with_name('results.json')
    output.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({name: {key: results[name][key]['nominal_z']
                            for key in ['original_density', 'native_spacing']}
                      for name in ['original', 'current']}, indent=2))


if __name__ == '__main__':
    main()
