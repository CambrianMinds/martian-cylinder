"""Partial-rim measurements on inventoried original PDS arrays."""
from pathlib import Path
import json
import sys
import numpy as np
from scipy.ndimage import map_coordinates, gaussian_filter, zoom
from scipy.optimize import least_squares, curve_fit
from scipy.special import erf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pds_images import BASE, read_image

ROOT = BASE.parents[1]
sys.path.insert(0, str(ROOT/'independent-reconstruction'))
from step4_endface_and_conic_models import point_to_ellipse_orth_dist


def ellipse_fit(xy, seed, mask=None):
    if mask is None:
        mask = np.ones(len(xy), dtype=bool)
    cx, cy = seed['center_xy'];rx, ry = seed['radii_xy']
    initial = [cx, cy, max(rx, ry), min(rx, ry), np.pi/2 if rx >= ry else 0]
    radius = max(rx, ry)
    lower = [cx-2*radius, cy-2*radius, .1*radius, .05*radius, -2*np.pi]
    upper = [cx+2*radius, cy+2*radius, 4*radius, 4*radius, 2*np.pi]
    def residual(parameters):
        return point_to_ellipse_orth_dist(xy[:, 0], xy[:, 1], *parameters)
    solutions = []
    for angle in [initial[4]-.2, initial[4], initial[4]+.2]:
        start = initial.copy();start[-1] = angle
        solution = least_squares(lambda p: residual(p)[mask], start,
                                 bounds=(lower, upper), max_nfev=1500)
        if solution.success:
            solutions.append(solution)
    if not solutions:
        raise RuntimeError('All ellipse starts failed')
    solution = min(solutions, key=lambda s: s.fun@s.fun)
    return solution.x, residual(solution.x)


def extract(image, selection):
    center = np.array(selection['center_xy'])
    rx, ry = selection['radii_xy']
    half = selection['search_half_width_px']
    records = []
    for angle in np.linspace(*selection['angles_deg'], selection['stations']):
        phase = np.radians(angle)
        seed = center+np.array([rx*np.cos(phase), ry*np.sin(phase)])
        normal = np.array([np.cos(phase)/rx, np.sin(phase)/ry])
        normal /= np.linalg.norm(normal)
        s = np.arange(-half, half+.025, .05)
        points = seed+s[:, None]*normal
        values = map_coordinates(image, [points[:, 1], points[:, 0]], order=1, mode='nearest')
        smooth = gaussian_filter(values, .65/.05)
        gradient = np.gradient(smooth, .05)*selection['polarity']
        index = int(np.argmax(gradient[1:-1]))+1
        denominator = gradient[index-1]-2*gradient[index]+gradient[index+1]
        shift = .5*(gradient[index-1]-gradient[index+1])/denominator if abs(denominator)>1e-15 else 0
        peak = s[index]+np.clip(shift, -1, 1)*.05
        mask = abs(s-peak) <= 2.2
        baseline, top = values[mask][0], values[mask][-1]
        def transition(v, low, high, location, width):
            return low+(high-low)*.5*(1+erf((v-location)/(np.sqrt(2)*width)))
        status = 'converged'
        try:
            spread = max(np.ptp(values), 1e-5)
            fitted, covariance = curve_fit(transition, s[mask], values[mask],
                p0=[baseline, top, peak, .8],
                bounds=([values.min()-spread, values.min()-spread, peak-1.2, .2],
                        [values.max()+spread, values.max()+spread, peak+1.2, 2.5]), maxfev=2500)
            location = float(fitted[2])
            uncertainty = float(np.sqrt(max(covariance[2, 2], 0)))
        except (ValueError, RuntimeError):
            location, uncertainty = float(peak), None
            status = 'error_function_failed_gradient_fallback'
        records.append(dict(angle_deg=float(angle), seed_xy=seed.tolist(), normal_xy=normal.tolist(),
                            gradient_xy=(seed+peak*normal).tolist(),
                            erf_xy=(seed+location*normal).tolist(),
                            uncertainty_px=uncertainty, polarity=selection['polarity'],
                            signed_peak_gradient=float(gradient[index]), status=status,
                            excluded=False, profile_s_px=s.tolist(), profile_values=values.tolist()))
    return records


def evaluate(records, selection):
    rows = {}
    for method in ['gradient', 'erf']:
        xy = np.array([row[method+'_xy'] for row in records])
        parameters, residual = ellipse_fit(xy, selection)
        diameter = 2*max(parameters[2:4])
        reference_diameter = selection.get('reference_diameter_px',2*max(selection['radii_xy']))
        predicted = np.empty(len(xy))
        for test in np.array_split(np.arange(len(xy)), 5):
            mask = np.ones(len(xy), dtype=bool)
            mask[max(0, int(test.min())-2):min(len(xy), int(test.max())+3)] = False
            _, heldout_residual = ellipse_fit(xy, selection, mask)
            predicted[test] = heldout_residual[test]
        rows[method] = dict(parameters=parameters.tolist(), diameter_px=float(diameter),
                            rms_px=float(np.sqrt(np.mean(residual**2))),
                            reference_diameter_px=float(reference_diameter),
                            normalized_rms=float(np.sqrt(np.mean(residual**2))/reference_diameter),
                            normalized_fitted_diameter_rms=float(np.sqrt(np.mean(residual**2))/diameter),
                            guarded_rms_px=float(np.sqrt(np.mean(predicted**2))),
                            guarded_normalized_rms=float(np.sqrt(np.mean(predicted**2))/reference_diameter),
                            residuals_px=residual.tolist(), guarded_residuals_px=predicted.tolist(),
                            n=len(xy))
    return rows


def main():
    selections = json.loads((BASE/'boundary-inventory/control-selections.json').read_text())
    results = []
    fig, axes = plt.subplots(len(selections), 3, figsize=(14, 4*len(selections)))
    for index, selection in enumerate(selections):
        image, _ = read_image(BASE/'sources/images'/(selection['product']+'.IMG'))
        raw = extract(image, selection)
        # Persist the station inventory before calculating any fit residual.
        path = BASE/'boundary-inventory'/(selection['case_id']+'.json')
        path.write_text(json.dumps({'selection': selection, 'stations': raw}, indent=2)+'\n')
        result = {'case_id': selection['case_id'], 'source_product': selection['product'],
                  'scope': 'Observed original-image partial rim. R and D unobservable.',
                  'native': evaluate(raw, selection), 'seed_sensitivity': []}
        for factor in [.9, 1.1]:
            changed = {**selection, 'radii_xy': [v*factor for v in selection['radii_xy']],
                       'reference_diameter_px':2*max(selection['radii_xy'])}
            stations = extract(image, changed)
            (BASE/'boundary-inventory'/(selection['case_id']+f'-seed-{factor}.json')).write_text(
                json.dumps({'selection': changed, 'stations': stations}, indent=2)+'\n')
            result['seed_sensitivity'].append({'factor': factor, 'fits': evaluate(stations, changed)})
        scale = 40/(2*max(selection['radii_xy']))
        smoothed = gaussian_filter(image, .7/scale)
        matched = zoom(smoothed, scale, order=1)
        transformed = {**selection, 'center_xy': [v*scale for v in selection['center_xy']],
                       'radii_xy': [v*scale for v in selection['radii_xy']],
                       'search_half_width_px': max(2, scale*selection['search_half_width_px'])}
        matched_stations = extract(matched, transformed)
        (BASE/'boundary-inventory'/(selection['case_id']+'-matched.json')).write_text(json.dumps(
            {'selection': transformed, 'scale': scale, 'output_blur_sigma_px': .7,
             'stations': matched_stations}, indent=2)+'\n')
        result['matched_resolution'] = {'nominal_diameter_px': 40, 'scale': scale,
                                        'output_blur_sigma_px': .7,
                                        'fits': evaluate(matched_stations, transformed)}
        results.append(result)
        ax = axes[index, 0];cx, cy=selection['center_xy'];rx, ry=selection['radii_xy']
        ax.imshow(image, cmap='gray', vmin=np.percentile(image, 1), vmax=np.percentile(image, 99))
        xy=np.array([record['erf_xy'] for record in raw]);ax.scatter(*xy.T,s=12,c='#15dca1')
        ax.set(xlim=(cx-1.35*rx,cx+1.35*rx),ylim=(cy+1.6*ry,cy-1.6*ry),
               title=selection['case_id']+' / observed original PDS')
        for method in ['gradient','erf']:
            axes[index, 1].plot(result['native'][method]['residuals_px'],label=method)
            axes[index, 2].plot(result['matched_resolution']['fits'][method]['residuals_px'],label=method)
        axes[index, 1].set(title='Observed partial-rim residuals',xlabel='Station',ylabel='Native px')
        axes[index, 2].set(title='40 px nominal diameter, added blur',xlabel='Station',ylabel='Resampled px')
        axes[index, 1].legend();axes[index, 2].legend()
    (BASE/'results/observed-controls.json').write_text(json.dumps(results,indent=2)+'\n')
    fig.tight_layout();fig.savefig(BASE/'figures/observed-control-metrology.png',dpi=160);plt.close(fig)
    for result in results:
        print(result['case_id'], {key:round(value['normalized_rms'],5)
              for key,value in result['native'].items()})


if __name__ == '__main__':
    main()
