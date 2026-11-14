from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'README.md'; s=p.read_text(encoding='utf-8')
s=s.replace('$a = 19.95\\text{ px}$, $b = 16.74\\text{ px}$', '$a = 20.029\\text{ px}$, $b = 16.846\\text{ px}$')
s=s.replace('$b/a = 0.8392$ (tilt $\\gamma = 32.9^\\circ$)', '$b/a = 0.8411$ (tilt $\\gamma = 32.75^\\circ$)')
s=s.replace('$b/a = 0.833\\text{--}0.839$', '$b/a = 0.8330$')
s=s.replace('from $0.417\\text{ px}$', 'from $0.4112\\text{ px}$ (same constrained model)')
# Use explicit breaks instead of trailing Markdown whitespace.
s='\n'.join(line.rstrip()+('<br>' if line.endswith('  ') else '') for line in s.splitlines())+'\n'
p.write_text(s,encoding='utf-8')

p=ROOT/'independent-reconstruction/report.md'; s=p.read_text(encoding='utf-8')
lines=s.splitlines()
for i,line in enumerate(lines):
    if line.startswith('> 2. **Direct Physical Contradiction with the Rear Arc**'):
        lines[i]='> 2. **Direct physical inconsistency of M4**: Its upper line cuts its own end ellipses rather than being tangent. The required intercept is 19.433711 px; M4 uses 19.294848 px. This rejects M4 as a physical frustum. The standalone fixed-front-shape scan is a different constrained model and is not a 16-sigma test of the full M4 solution.'
    if line.startswith('- **Buried Cylinder (H1b) vs. Tapered Cone (H2)**'):
        lines[i]='- **Buried Cylinder versus M4**: M4 fails its physical tangency constraint. M1 supplies the strict cylindrical baseline with 0.3788 px RMS over 85 stations. Current Step 5 photometry does not independently reject planar shading. Physical origin and all possible tapered shapes are not determined by this test.'
    if 'Forcing a conical taper' in line and '> 260' in line:
        lines[i]='- The standalone rear scan holds the front shape and orientation fixed; its large deviance near s=0.60 applies to that constrained family, not the changed front geometry in M4. The raw difference between s=0.93 and s=1 is small, but the nominal confidence interval excludes s=1.'
start=next((i for i,line in enumerate(lines) if line.startswith('### 8.5 ')),None)
if start is not None:
    # Section 8.5 is the final section in this report.
    lines=lines[:start]+'''### 8.5 Controls and photometry: verification limits

The narrative comparison reports edge RMS values of 0.971, 1.724, and 1.953 px for three selected nearby clasts, versus 0.2422 px for the target. It reports normalized Laplacian variances of 1.64e-4, 2.45e-4, and 2.98e-4, versus 8.02e-5 for the target. These are reported local comparisons; the audit has not independently regenerated the selections or measurements and does not treat them as a regional geological distribution.

The current Step 5 JSON gives quadratic coefficient -0.01285 +/- 0.01357, z=0.95, with relative RMS 0.02682 (planar) and 0.02673 (quadratic). Historical claims of 7.38 or 11.45 sigma are not current pipeline results. Significant curvature or rejection of flat shading is not established by the current test.
'''.splitlines()
p.write_text('\n'.join(lines)+'\n',encoding='utf-8')

p=ROOT/'audit/model-comparison.md'; s=p.read_text(encoding='utf-8')
s=s.replace('| 1830.4 | 1861.5 |','| not evaluated here | not evaluated here |')
s += '\nThe separate audit re-optimization uses different starting values: M4 scale differs from the stored fit by about 6.2e-6, while RMS differs by about 6.3e-7 px. These are close numerical solutions, not bit-identical independent optimizations. The full original pipeline replay is bit-identical. The audit bootstrap (500 resamples, fixed jitter direction) yields an orientation spread of 3.79 degrees, versus the historical 4.23 from a different procedure; neither is a calibrated spatial bootstrap.\n'
p.write_text(s,encoding='utf-8')

p=ROOT/'audit/argon-red-team-report.md';s=p.read_text(encoding='utf-8')
s=s.replace('## Corrections to the audit itself','## Verification performed\n\nThe full reconstruction completed in 136.91 seconds with zero numerical differences and identical hashes for all eight JSON outputs. All ten audit scripts ran successfully. All 15 regression tests passed; Windows sandbox permissions required the temporary-file tests to run outside the sandbox. The corrected 15-page paper was rebuilt with XeLaTeX and its changed pages visually reviewed. Hosted GitHub execution has not been observed.\n\n## Corrections to the audit itself')
p.write_text(s,encoding='utf-8')
