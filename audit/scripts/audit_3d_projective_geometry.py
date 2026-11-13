"""Check M4's physical common-tangent constraint, not a full 3D refit."""
from pathlib import Path
import json
import math

ROOT = Path(__file__).resolve().parents[2]

def tangent_check(p):
    m = (1-p['scale_ratio_s'])*p['r_dorsal']/p['L_proj']
    required = math.hypot(p['a'], m*p['b'])
    return {
        'line_slope_axis_coordinates': m,
        'actual_intercept_px': p['r_dorsal'],
        'required_tangent_intercept_px': required,
        'intercept_shortfall_px': required-p['r_dorsal'],
        'tangency_identity_residual_px2': p['r_dorsal']**2-p['a']**2-(m*p['b'])**2,
        'physical_tangency_satisfied': math.isclose(required, p['r_dorsal'], abs_tol=1e-8),
    }

def main():
    s9 = json.loads((ROOT/'independent-reconstruction/step9_joint_model.json').read_text())
    p = s9['joint_models']['M4_Tapered_Conical_Frustum_Coupled_8DOF']['params']
    baseline = s9['independent_baselines']['freely_translated_rear_ellipse']
    result = {
        'm1_axis_deg': s9['joint_models']['M1_Strict_Right_Circular_Cylinder_6DOF']['params']['theta_axis_deg'],
        'm4_axis_deg': p['theta_axis_deg'], 'm4_alpha_deg': p['half_taper_alpha_deg'],
        'm4_s': p['scale_ratio_s'],
        'rear_center_shift_px': math.hypot(p['xc_r']-baseline['xc'], p['yc_r']-baseline['yc']),
        'max_persp_convergence_deg': 2*math.degrees(math.atan(19.7/(13458.28*math.tan(math.radians(20))))),
        'convergence_assumption': '20 degree inclination; not a universal maximum',
        'm4_tangency': tangent_check(p),
        'full_3d_cone_refit_performed': False,
        'fixed_shape_rear_scan_is_test_of_full_m4': False,
    }
    (ROOT/'audit/projective_geometry_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
