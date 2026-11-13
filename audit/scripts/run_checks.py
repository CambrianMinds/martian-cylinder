"""Refresh audit outputs, then verify their mathematical and distribution invariants."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = [
    'audit_provenance_and_checksums.py', 'audit_camera_and_ephemeris.py',
    'audit_subpixel_edge_profiles.py', 'audit_conic_and_facet_odr.py',
    'audit_joint_models_85pt.py', 'audit_rear_arc_likelihood.py',
    'audit_3d_projective_geometry.py', 'audit_shadow_raycast.py',
    'audit_rock_controls_benchmark.py', 'audit_generate_claim_ledger.py',
]

def main():
    for script in SCRIPTS:
        subprocess.run([sys.executable, str(Path(__file__).parent/script)], cwd=ROOT, check=True)
    subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'audit/tests', '-v'], cwd=ROOT, check=True)

if __name__ == '__main__':
    main()
