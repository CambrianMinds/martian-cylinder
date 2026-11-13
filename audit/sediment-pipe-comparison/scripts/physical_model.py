"""Finite circular segments projected through the retained Curiosity CAHVOR camera."""
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial import cKDTree

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/'independent-reconstruction'))
from step2_camera_geometry import CAHVOR_DRXX, cahvor_pixel_to_ray, extract_cahv_intrinsics
from step4_endface_and_conic_models import point_to_ellipse_orth_dist

CAMERA = CAHVOR_DRXX
INTRINSICS = extract_cahv_intrinsics(CAMERA)
RANGE = 3.957
FOCAL = 13458.276
LOW = np.array([1055, 970, 10, 15, np.radians(15), np.radians(15)])
HIGH = np.array([1085, 1000, 30, 75, np.radians(50), np.radians(75)])


def unit(vector):
    return vector/np.linalg.norm(vector, axis=-1, keepdims=True)


def project(points):
    points = np.asarray(points) - CAMERA['C']
    omega = points @ CAMERA['O']
    transverse = points/omega[..., None] - CAMERA['O']
    tau = np.sum(transverse*transverse, axis=-1)
    coefficients = CAMERA['R']
    correction = coefficients[0]+coefficients[1]*tau+coefficients[2]*tau*tau
    corrected = points+correction[..., None]*(points-omega[..., None]*CAMERA['O'])
    denominator = corrected @ CAMERA['A']
    return np.stack([corrected@CAMERA['H']/denominator,
                     corrected@CAMERA['V']/denominator], axis=-1)


def geometry(parameters, depth_sign=-1):
    x, y, radius_px, span_px, theta, gamma = parameters[:6]
    ray = cahvor_pixel_to_ray(x, y, CAMERA)
    screen = np.cos(theta)*INTRINSICS['h_unit']+np.sin(theta)*INTRINSICS['v_unit']
    screen = unit(screen-np.dot(screen, ray)*ray)
    axis = unit(np.sin(gamma)*screen+depth_sign*np.cos(gamma)*ray)
    first = unit(np.cross(axis, ray))
    second = unit(np.cross(axis, first))
    front = CAMERA['C']+RANGE*ray
    radius = radius_px*RANGE/FOCAL
    length = span_px*RANGE/(FOCAL*np.sin(gamma))
    rear = front-length*axis
    return dict(front=front, rear=rear, radius=radius, length=length,
                axis=axis, first=first, second=second, ray=ray)


def ellipse_from_curve(points):
    """Recover a conic from a densely projected circle, retaining lens residuals."""
    origin = points.mean(axis=0)
    scale = np.std(points)
    xy = (points-origin)/scale
    x, y = xy.T
    coefficients = np.linalg.lstsq(np.column_stack([x*x, x*y, y*y, x, y]),
                                   np.ones(len(x)), rcond=None)[0]
    quadratic = np.array([[coefficients[0], coefficients[1]/2],
                          [coefficients[1]/2, coefficients[2]]])
    center = -.5*np.linalg.solve(quadratic, coefficients[3:])
    level = 1+center@quadratic@center
    eigenvalues, eigenvectors = np.linalg.eigh(quadratic)
    radii = np.sqrt(level/eigenvalues)*scale
    angle = np.arctan2(eigenvectors[1, 1], eigenvectors[0, 1])
    return origin+scale*center, radii[0], radii[1], angle


def projected_boundaries(parameters, depth_sign=-1, intrinsic_ratio=1.):
    g = geometry(parameters, depth_sign)
    end_scale = parameters[6] if len(parameters)>6 else 1.
    phase = np.linspace(0, 2*np.pi, 96, endpoint=False)
    normals = np.cos(phase)[:, None]*g['first']+intrinsic_ratio*np.sin(phase)[:, None]*g['second']
    curves = {name: project(g[name]+g['radius']*scale*normals)
              for name,scale in [('front',1.),('rear',end_scale)]}
    offset = g['front']-CAMERA['C']
    aa, bb = offset@g['first'], (offset@g['second'])/intrinsic_ratio
    phase0 = np.arctan2(bb, aa)
    radius_derivative = g['radius']*(1-end_scale)/g['length']
    tangent_value = radius_derivative*(offset@g['axis'])-g['radius']
    delta = np.arccos(tangent_value/np.hypot(aa, bb))
    candidates = []
    for phase_tangent in [phase0-delta, phase0+delta]:
        radial = np.cos(phase_tangent)*g['first']+intrinsic_ratio*np.sin(phase_tangent)*g['second']
        endpoints = project(np.array([g['front'], g['rear']])+
                            g['radius']*np.array([1.,end_scale])[:,None]*radial)
        candidates.append(endpoints)
    normal_image = np.array([-np.sin(parameters[4]), np.cos(parameters[4])])
    dorsal = min(candidates, key=lambda line: line.mean(axis=0)@normal_image)
    return curves, dorsal


def residuals(parameters, data, depth_sign=-1, intrinsic_ratio=1.):
    curves, dorsal = projected_boundaries(parameters, depth_sign, intrinsic_ratio)
    result = {}
    for name in ['front', 'rear']:
        center, a, b, angle = ellipse_from_curve(curves[name])
        xy = data[name]['xy']
        result[name] = point_to_ellipse_orth_dist(xy[:, 0], xy[:, 1], *center, a, b, angle)
    tangent = unit(dorsal[1]-dorsal[0])
    normal = np.array([-tangent[1], tangent[0]])
    result['dorsal'] = (data['dorsal']['xy']-dorsal[0])@normal
    return result


def fit(data, masks, depth_sign=-1, weighted=True, intrinsic_ratio=1., fit_taper=False):
    def objective(parameters):
        values = residuals(parameters, data, depth_sign, intrinsic_ratio)
        return np.concatenate([values[name][masks[name]] /
                               (data[name]['sigma'][masks[name]] if weighted else 1)
                               for name in data])
    solutions = []
    lower = np.r_[LOW,.3] if fit_taper else LOW
    upper = np.r_[HIGH,1.6] if fit_taper else HIGH
    for angle in [28, 31.2, 35]:
        start = [1068.3, 985.95, 20, 40.86, np.radians(angle), np.radians(38)]
        if fit_taper:
            start.append(1.)
        solution = least_squares(objective, start, bounds=(lower, upper),
                                 max_nfev=600, x_scale='jac', diff_step=1e-5)
        if solution.success:
            solutions.append(solution)
    if not solutions:
        raise RuntimeError('All 3D initializations failed')
    best = min(solutions, key=lambda solution: np.sum(solution.fun**2))
    return best.x, {'successful_starts': len(solutions),
                    'objective': float(best.fun@best.fun),
                    'start_parameters': [solution.x.tolist() for solution in solutions],
                    'jacobian_singular_values': np.linalg.svd(best.jac, compute_uv=False).tolist(),
                    'bound_hits': np.flatnonzero(np.minimum(best.x-lower, upper-best.x)<1e-5).tolist()}


def rays(xy):
    return np.array([cahvor_pixel_to_ray(x, y, CAMERA) for x, y in xy])


def surface_intersections(parameters, xy, depth_sign=-1, root_sign=-1):
    g = geometry(parameters, depth_sign)
    direction = rays(xy)
    origin = CAMERA['C']-g['front']
    radial_direction = direction-(direction@g['axis'])[:, None]*g['axis']
    radial_origin = origin-np.dot(origin, g['axis'])*g['axis']
    aa = np.sum(radial_direction**2, axis=1)
    bb = 2*radial_direction@radial_origin
    cc = radial_origin@radial_origin-g['radius']**2
    discriminant = bb*bb-4*aa*cc
    valid = discriminant >= 0
    distances = (-bb+root_sign*np.sqrt(np.maximum(discriminant, 0)))/(2*aa)
    points = CAMERA['C']+distances[:, None]*direction
    return points, valid


def fit_burial_plane(parameters, soil_xy, depth_sign=-1, root_sign=-1):
    """Fit one 3D plane to visible-cylinder intersections of the soil contact."""
    points, valid = surface_intersections(parameters, soil_xy, depth_sign, root_sign)
    if valid.sum() < 3:
        raise ValueError('Too few soil rays intersect the cylinder')
    center = points[valid].mean(axis=0)
    _, _, vectors = np.linalg.svd(points[valid]-center)
    normal = vectors[-1]
    offset = float(center@normal)
    g = geometry(parameters, depth_sign)
    phase = np.linspace(0, 2*np.pi, 12000, endpoint=False)
    radial = g['radius']*(np.cos(phase)[:, None]*g['first']+np.sin(phase)[:, None]*g['second'])
    along = (offset-(g['front']+radial)@normal)/(g['axis']@normal)
    curve3d = g['front']+radial+along[:, None]*g['axis']
    finite = (along >= -g['length']) & (along <= 0)
    curve = project(curve3d[finite])
    distances = cKDTree(curve).query(soil_xy)[0]
    return dict(normal=normal.tolist(), offset_m=offset,
                independent_parameters=3, fitted_soil_points=int(valid.sum()),
                nonintersecting_soil_rays=int((~valid).sum()),
                rms_px=float(np.sqrt(np.mean(distances**2))),
                residuals_px=distances.tolist(), curve_xy=curve.tolist())
