"""Authentic DRXX context and stored-M1 overlays for the paper evidence build."""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from scipy.spatial import cKDTree

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ROI = (1014, 1104, 932, 1007)  # Half-open x and y bounds, zero-based DRXX.
STYLES = {
    'front': ('#57e1a0', 'o', 'Near rim, 35'),
    'rear': ('#ffcf56', 's', 'Rear arc, 24'),
    'dorsal': ('#55d9ff', '^', 'Dorsal edge, 26'),
}


def crop(ax, image, limits):
    x0, x1, y0, y1 = ROI
    ax.imshow(image[y0:y1, x0:x1], cmap='gray', interpolation='none',
              extent=(x0-.5, x1-.5, y1-.5, y0-.5), vmin=limits[0], vmax=limits[1])
    ax.set(xlim=(x0-.5, x1-.5), ylim=(y1-.5, y0-.5),
           xlabel='DRXX x (pixel)', ylabel='DRXX y (pixel)')


def stations(ax, data, size=19):
    for name, (color, marker, label) in STYLES.items():
        ax.scatter(*data[name]['xy'].T, s=size, marker=marker, facecolor=color,
                   edgecolor='black', linewidth=.35, label=label, zorder=6)


def interpreted_regions(ax):
    for label, xy, text in [
        ('Regolith contact\n(interpreted)', (1039.71, 971.30), (1017, 986)),
        ('Cast shadow on soil\n(interpreted)', (1084, 995), (1050, 1003)),
    ]:
        ax.annotate(label, xy=xy, xytext=text, fontsize=12, color='white',
                    arrowprops={'arrowstyle': '->', 'color': 'white', 'lw': .8},
                    bbox={'facecolor': 'black', 'alpha': .72, 'edgecolor': 'none', 'pad': 2})


def save(fig, stem):
    path = HERE/'figures'/stem
    fig.savefig(path.with_suffix('.pdf'), bbox_inches='tight',
                metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(path.with_suffix('.png'), dpi=600, bbox_inches='tight')
    plt.close(fig)


def build_native_figures(data, image, model, orthogonal_distance):
    out = HERE/'figures'
    out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14,
                         'pdf.fonttype': 42, 'savefig.pad_inches': .08})
    x0, x1, y0, y1 = ROI
    local_limits = np.percentile(image[y0:y1, x0:x1], [2, 98])
    scene_limits = np.percentile(image, [1, 99])
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 6))
    ax = axes[0]
    ax.imshow(image, cmap='gray', interpolation='none', vmin=scene_limits[0], vmax=scene_limits[1])
    ax.add_patch(Rectangle((x0-.5, y0-.5), x1-x0, y1-y0, fill=False,
                           edgecolor='white', linewidth=3))
    ax.add_patch(Rectangle((x0-.5, y0-.5), x1-x0, y1-y0, fill=False,
                           edgecolor='black', linewidth=1.2, linestyle='--'))
    ax.annotate('Target ROI', xy=(x0, y0), xytext=(790, 740), color='white',
                arrowprops={'arrowstyle': '->', 'color': 'white'},
                bbox={'facecolor': 'black', 'alpha': .7, 'pad': 3})
    ax.set(xlim=(-.5, image.shape[1]-.5), ylim=(image.shape[0]-.5, -.5),
           xlabel='DRXX x (pixel)', ylabel='DRXX y (pixel)', title='(a) Complete Sol 3556 DRXX frame')
    ax = axes[1]
    crop(ax, image, local_limits)
    stations(ax, data, size=16)
    source = json.loads((ROOT/'independent-reconstruction/step3_features.json').read_text())
    pebble = next(p for p in source['arch_radial_points'] if abs(p['theta_deg']+45)<.001)
    ax.scatter(pebble['x_erf'], pebble['y_erf'], marker='x', color='white', s=45, linewidth=1.5)
    ax.annotate('Excluded pebble', xy=(pebble['x_erf'], pebble['y_erf']), xytext=(1071, 954),
                fontsize=12, color='white', arrowprops={'arrowstyle': '->', 'color': 'white'},
                bbox={'facecolor': 'black', 'alpha': .7, 'pad': 2})
    interpreted_regions(ax)
    ax.set_title('(b) ROI and recorded boundaries')
    handles = [Line2D([], [], linestyle='none', marker=marker, markerfacecolor=color,
                      markeredgecolor='black', markersize=6, label=label)
               for color, marker, label in STYLES.values()]
    fig.legend(handles=handles, loc='lower center', ncol=3, frameon=False, bbox_to_anchor=(.5, .015))
    fig.tight_layout(rect=(0, .08, 1, 1))
    save(fig, 'target-boundaries')

    p = model['params']
    angle = np.radians(p['theta_axis_deg'])
    along = np.array([np.cos(angle), np.sin(angle)])
    normal = np.array([-np.sin(angle), np.cos(angle)])
    centers = {'front': np.array([p['xc_f'], p['yc_f']]),
               'rear': np.array([p['xc_r'], p['yc_r']])}
    phase = np.linspace(0, 2*np.pi, 2400, endpoint=False)
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.6), gridspec_kw={'width_ratios': [1.25, 1]})
    ax = axes[0]
    crop(ax, image, local_limits)
    arc_records = {}
    residuals = {}
    for name, center in centers.items():
        curve = center+p['b']*np.cos(phase)[:, None]*along+p['a']*np.sin(phase)[:, None]*normal
        _, nearest = cKDTree(curve).query(data[name]['xy'])
        observed_phase = np.unwrap(phase[nearest])
        lo, hi = float(observed_phase.min()), float(observed_phase.max())
        supported = np.mod(phase-lo, 2*np.pi) <= hi-lo
        color = STYLES[name][0]
        ax.plot(*np.vstack([curve, curve[0]]).T, c=color, ls=(0, (4, 3)), lw=1, alpha=.8)
        visible_curve = curve.copy()
        visible_curve[~supported] = np.nan
        ax.plot(*visible_curve.T, c=color, lw=1.8)
        arc_records[name] = {'phase_start_rad': lo, 'phase_stop_rad': hi,
                             'meaning': 'Curve interval spanned by the nearest model points to retained stations.'}
        xy = data[name]['xy']
        residuals[name] = orthogonal_distance(xy[:, 0], xy[:, 1], *center, p['a'], p['b'], angle)
    cf, cr = centers['front'], centers['rear']
    ax.plot(*np.array([cf, cr]).T, c='white', ls='-.', lw=1)
    ax.scatter(*np.array([cf, cr]).T, marker='+', c='white', s=70, linewidth=1.2)
    ends = np.array([cf-p['a']*normal, cr-p['a']*normal])
    dorsal = data['dorsal']['xy']
    projection = (dorsal-ends[0])@along
    ax.plot(*ends.T, c=STYLES['dorsal'][0], lw=1, ls=(0, (4, 3)))
    sampled_interval = [max(-p['L_proj'], float(projection.min())), min(0., float(projection.max()))]
    sampled_line = ends[0]+np.array(sampled_interval)[:, None]*along
    ax.plot(*sampled_line.T, c=STYLES['dorsal'][0], lw=1.8)
    for lo, hi in [(projection.min(), -p['L_proj']), (0., projection.max())]:
        if hi > lo:
            extension = ends[0]+np.array([lo, hi])[:, None]*along
            ax.plot(*extension.T, c=STYLES['dorsal'][0], ls=':', lw=1.5)
    residuals['dorsal'] = (dorsal-cf)@normal+p['a']
    stations(ax, data, size=18)
    interpreted_regions(ax)
    ax.set_title('(a) Stored strict M1 on authentic radiance')
    ax = axes[1]
    for name, (color, marker, label) in STYLES.items():
        # Dark outlines and distinct symbols preserve identity in grayscale.
        ax.plot(np.arange(len(residuals[name])), residuals[name], color='0.45', lw=.7)
        ax.scatter(np.arange(len(residuals[name])), residuals[name], marker=marker,
                   c=color, edgecolor='black', linewidth=.5, s=27, label=label)
    ax.axhline(0, color='black', lw=.7)
    ax.set(xlabel='Station index within each family', ylabel='Signed orthogonal residual (pixel)',
           title=f"(b) In-sample M1 residuals / {model['residuals_px']['total_rms']:.4f} px RMS")
    ax.legend(fontsize=12, frameon=False, loc='lower left')
    fig.legend(handles=[Line2D([], [], color='black', lw=1.5, label='Curve over sampled arc'),
                        Line2D([], [], color='black', ls='--', label='Unmeasured curve extension'),
                        Line2D([], [], color='black', ls='-.', label='Inferred center axis'),
                        Line2D([], [], color='black', ls=':', label='Tangent line extension')],
               loc='lower center', ncol=2, frameon=False, fontsize=12, bbox_to_anchor=(.5, -.005))
    fig.tight_layout(rect=(0, .105, 1, 1))
    save(fig, 'joint-m1-overlay')
    rms = float(np.sqrt(np.mean(np.concatenate(list(residuals.values()))**2)))
    assert abs(rms-model['residuals_px']['total_rms']) < 1e-9
    generator_fraction = -(dorsal-ends[0])@along/p['L_proj']
    metadata = {'pds_product': '3556MR1025170721700585C00_DRXX',
                'image_path': 'data/3556MR1025170721700585C00_DRXX.IMG',
                'label_path': 'data/3556MR1025170721700585C00_DRXX.LBL',
                'shape_yx': list(image.shape), 'roi_half_open_xxyy': list(ROI),
                'coordinates': 'Zero-based DRXX subframe, x right and y down. No rotation or reprojection.',
                'radiometry': 'Arithmetic mean of three PDS-scaled radiance bands, zero offsets.',
                'display': 'Linear grayscale clipping only. No spatial interpolation or enhancement.',
                'full_frame_limits': scene_limits.tolist(), 'crop_limits': local_limits.tolist(),
                'radiance_units': 'W m^-2 sr^-1 nm^-1', 'attribution': 'NASA/JPL-Caltech/MSSS',
                'attribution_support': ['PDS label institution MALIN SPACE SCIENCE SYSTEMS, host MSL, MAST_RIGHT',
                    'https://science.nasa.gov/resource/curiositys-mastcam-views-flaky-streambed-rocks/'],
                'model_source': 'independent-reconstruction/step9_joint_model.json',
                'model_key': 'M1_Strict_Right_Circular_Cylinder_6DOF',
                'stored_parameters': p, 'recomputed_m1_rms_px': rms, 'sampled_arc_intervals': arc_records,
                'station_counts': {name: len(group['xy']) for name, group in data.items()},
                'dorsal_indices_past_generator_endpoint': np.flatnonzero((generator_fraction<0)|(generator_fraction>1)).tolist(),
                'interpretations': 'Soil contact and cast-shadow labels are region interpretations, without fitted perimeters.'}
    (HERE/'figure-provenance.json').write_text(json.dumps(metadata, indent=2)+'\n', encoding='utf-8')
