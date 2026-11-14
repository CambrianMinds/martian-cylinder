from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]

def write(name, text):
    (ROOT / name).write_text(text, encoding='utf-8')

write('.github/workflows/verify.yml', '''name: Peer-Review Verification Suite

on: [push, pull_request]

jobs:
  verify:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest]
        python-version: ["3.11", "3.12"]
    env:
      MPLBACKEND: Agg
      PYTHONUTF8: "1"
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install reconstruction dependencies
        run: python -m pip install -r independent-reconstruction/requirements.txt
      - name: Reproduce reconstruction and compare outputs
        run: python audit/scripts/audit_reproduce_pipeline.py
      - name: Verify audit and distribution
        run: python -m unittest discover -s audit/tests -v
''')

# Resolve links relative to each document, preserving the destination.
import os
for p in list(ROOT.glob('*.md')) + [ROOT/'llms.txt'] + list((ROOT/'independent-reconstruction').glob('*.md')):
    s = p.read_text(encoding='utf-8')
    s = re.sub(r'file:///d:/projects/martian-cylinder/([^\s)]+)',
        lambda m: os.path.relpath(ROOT/m[1], p.parent).replace('\\','/'), s, flags=re.I)
    s = s.replace('($1.55\\sigma$)', '($2.196\\sigma$ nominal; uncalibrated station errors)')
    p.write_text(s, encoding='utf-8')

qual = '''**Audit correction (2026-11-12):** M4 is rejected as a physical frustum because its fitted upper line is not tangent to its own end ellipses; see [the checked derivation](audit/model-comparison.md). Its lower image-plane RMS remains a reproducible numerical result. M1 is the strict cylindrical baseline; M2/M3 permit a free edge offset. The 85 stations are not established to be statistically independent, and subpixel residuals are image-fit errors, not measured manufacturing tolerances. The standalone rear scan gives s=0.930, nominal 95% interval [0.87, 0.99], and nominal z=2.196 at s=1. A scalar Birge rescaling is only a sensitivity calculation, not a fitted spatial covariance model. Dimensions near 11.6 mm assume the 3.957 m focus distance; approximately 10.6–12.9 mm follows from the 3.6–4.4 m focus band, which is not a probabilistic range confidence interval. The 32.82 degree shadow receiving-plane rotation is fitted, not surveyed. Three selected local rocks do not establish a regional geological distribution or the object's origin. Audit shadow/control summaries transcribe prior claims rather than independently reproduce them.
'''
for name in ['README.md', 'llms.txt', 'independent-reconstruction/report.md', 'independent-reconstruction/report_layman.md', 'independent-reconstruction/methods.md']:
    p = ROOT/name
    q = qual if p.parent == ROOT else qual.replace('(audit/model-comparison.md)', '(../audit/model-comparison.md)')
    s=p.read_text(encoding='utf-8'); first, sep, rest=s.partition('\n')
    write(name, first+'\n\n'+q+'\n'+rest)

p=ROOT/'README.md'; s=p.read_text(encoding='utf-8').replace('$s = 0.935$ ($95\\%\\text{ CI: } [0.87, 0.99]$)', '$s = 0.930$ (Step 9 nominal $95\\%\\text{ CI: } [0.87, 0.99]$)')
s=s.replace('Matches ANSI AAA battery ($10.5\\text{ mm}$)', 'Range-conditional; approximately 10.6–12.9 mm across the focus band')
write('README.md', s)
p=ROOT/'independent-reconstruction/report.md'; s=p.read_text(encoding='utf-8')
s=s.replace('Once it is recognized that the physical rear arc independently rejects $s \\le 0.62$ at $\\Delta\\chi^2 > 260$, and that the lower boundary is an overlapping soil bank rather than a cone limb, Model 4 is recognized as an overparameterized mathematical artifact.', 'M4 fails the physical tangency condition for its own end ellipses (see the audit derivation). The fixed-front-shape rear scan is a different constrained model; its deviance must not be assigned to M4 as a 16-sigma test.')
s=s.replace('rendering standalone arc curvature flat and completely consistent with zero taper ($s = 1.000$).', 'making inference sensitive to the error model. The nominal interval excludes s=1; a scalar variance sensitivity calculation includes it, without establishing spatial covariance.')
s=s.replace('**the strict-cylinder fit (Model 1) is physically and geometrically confirmed**', '**the strict-cylinder fit (Model 1) provides the physical cylindrical baseline**')
write('independent-reconstruction/report.md',s)

write('audit/argon-red-team-report.md', '''# Argon audit: checked findings and dispositions

Reviewed 2026-11-12. This revision supersedes the original report's unsupported confidence and independence claims. Numerical evidence is in the JSON outputs and reproduction log. This is a local repository verification, not a new NASA archive download or a new geological survey.

| Issue | Disposition | Evidence and limits |
| --- | --- | --- |
| ARGON-H01: M4 | Physical formulation rejected | Direct ellipse/line tangency check in `audit_3d_projective_geometry.py`; derivation in `model-comparison.md`. Keep M4's reproducible numerical fit as a diagnostic, not a physical frustum. A shifted ellipse center need not lie on a visible edge. The fixed-shape rear scan is not a 16-sigma test of M4's changed ellipse shape. |
| ARGON-H02: rear scale | Reporting corrected | Nominal z=sqrt(4.8216)=2.196, not 1.55. Nominal CI [0.87,0.99] excludes 1. Scalar Birge sensitivity includes 1 but does not calibrate spatial covariance. |
| ARGON-H03: tolerance | Qualification added to active summaries | M1 RMS 0.3788 px is an image-plane residual, not physical roughness. Reduced chi-square 33.59 signals an inadequate nominal error/model description; correlation alone has not been established as the cause. |
| ARGON-M01: shadow | Conditional; independent reproduction outstanding | 32.82 degrees is fitted receiving-plane rotation, not surveyed absolute terrain slope. Thresholds share pixels. The audit script transcribes prior reported values, not a new ray trace. |
| ARGON-M02: range | Conditional dimensions documented | Focus calibration is not independent ranging. Focus-band diameter about 10.6–12.9 mm; this is a scenario span, not an 11.6 +/- 1.2 mm statistical confidence interval. |
| ARGON-M03: controls | Limited evidence; broader survey outstanding | Three selected clasts do not establish regional rarity or natural impossibility. The audit control script transcribes reported comparisons. |
| ARGON-L01: root PDF | Repaired | Root PDF copied byte-for-byte from valid `papers/` PDF. This restores the existing paper; it does not regenerate that historical paper from current claims. |
| ARGON-L02: CI | Workflow repaired; hosted execution pending | Current reconstruction, its dependency file, and audit tests replace archived commands. Reproduction returns nonzero on failure or numerical drift. |
| ARGON-L03: links | Repaired in active Markdown and llms.txt | Machine-local file URLs converted to document-relative links. |

## Corrections to the audit itself

- Removed the model-by-model Birge BIC ranking. Dividing each model's chi-square by its own chi-square/(N-k) makes the residual term exactly N-k and mechanically rewards smaller k. It is not a comparable common likelihood.
- Birge scaling is scalar variance inflation, not a spatial covariance fit. The reported lag correlation and AR(1) effective sample size are descriptive diagnostics on 24 residuals, not a measured covariance for all 85 stations.
- The provenance script checks local checksums against stored local values. It does not download NASA files or independently recompute SPICE kernels. Camera angles use stored telemetry.
- Reused extraction and geometry routines make this a reproduction and consistency check, not a wholly independent implementation.
- The shadow threshold table previously contained hardcoded intermediate values without direct source evidence. Those entries are removed; only explicitly sourced summary values are retained as reported, not independently verified.
- The old ledger manually assigned MATCH to hardcoded claims and stale line numbers. Its replacement inventories actual JSON numeric values with locatable paths and explicitly labels their verification limits.

The selected boundaries admit a subpixel cylindrical fit. M4's physical formulation fails its silhouette constraint. These observations do not uniquely establish material, origin, true physical tolerances, or regional geological rarity. Independent ranging, receiving-ground measurement, covariance calibration, and a broader control sample remain outstanding scientific work, not completed fixes.
''')
write('audit/model-comparison.md', '''# Checked geometric model comparison

Reviewed 2026-11-12. M1 is the strict cylindrical baseline; M2/M3 allow a free dorsal offset. M4's numerical fit is reproducible but its proposed physical frustum fails the common-tangent constraint.

## Direct physical falsification of M4's formulation

In coordinates u along the body axis and v transverse to it, an end ellipse has u²/b² + v²/a² = 1. M4's upper line is v=-r-mu, where m=(1-s)r/L. A tangent requires r²=a²+m²b², obtained from the ellipse support function (or a zero discriminant after substituting the line). Homothetic rear ellipses centered at u=-L impose the same condition.

Stored M4 parameters: a=19.262717 px, b=15.434227 px, r=19.294848 px, L=44.143566 px, s=0.618699. Thus m=0.166665 and the required tangent intercept is 19.433711 px. The actual line intercept is smaller by 0.138863 px, so the line cuts the projected end ellipse rather than touching it. This falsifies the physical silhouette interpretation of the fitted M4 geometry. It is an algebraic consistency failure, not a calibrated statistical significance or a test of every possible 3D cone.

`audit_3d_projective_geometry.py` computes these values; the regression test independently evaluates the discriminant. No full camera-ray/occlusion-constrained cone optimization has been performed by that script.

## Reproduced image-plane fits

| Model | k | Total RMS px | Front | Rear | Dorsal | Nominal chi-square | Nominal BIC |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M1 | 6 | 0.3788 | 0.2376 | 0.4830 | 0.4217 | 2653.51 | 2680.17 |
| M2 | 7 | 0.3468 | 0.2314 | 0.3049 | 0.4851 | 1916.15 | 1947.25 |
| M3 | 7 | 0.3389 | 0.2422 | 0.3784 | 0.4054 | 1830.4 | 1861.5 |
| M4 | 8 | 0.2549 | 0.1930 | 0.2684 | 0.3096 | 1044.06 | 1079.60 |

M3 minimizes an unweighted objective; the others minimize station-weighted residuals. The nominal BIC favors M4 under the stated independent-error model, but does not cure its physical constraint violation. All nominal reduced chi-squares are large. The original model-specific Birge BIC ranking is withdrawn: chi-square/[chi-square/(N-k)] + k ln N = N-k+k ln N, independent of fit quality. No replacement calibrated model ranking is claimed.

## Rear arc

With the front shape and orientation fixed, the standalone scan minimizes at s=0.930. At s=1, delta chi-square=4.8216, nominal z=2.196 and the 95% grid interval [0.87,0.99] excludes 1. RMS changes from 0.184339 to 0.186291 px. Multiplying this difference by a pixel scale gives an equivalent image-plane distance, not a measured surface tolerance.

The historical scalar rescaling used 22 residual degrees of freedom at fixed s (24 points minus two translations), giving z=0.684 and interval [0.77,1.17]. If counting the fitted scale as well, 21 degrees of freedom gives a slightly different result. Neither calculation estimates spatial covariance or a true coverage-calibrated interval. Retain the nominal exclusion and the sensitivity result with their distinct assumptions.

The scan at s around 0.60 holds a different front shape/orientation than M4. Its large deviance is not a one-parameter likelihood-ratio rejection of the full M4 solution. Likewise, the 7.73 px center displacement describes parameter changes, not a requirement for an edge at the ellipse center.

Perspective convergence of about 0.461 degrees at an assumed 20-degree inclination is a conditional estimate, not a global bound over all inclinations. The approximately 35-degree observed opening is incompatible with opposite cylindrical generators at the considered inclinations; it does not by itself prove burial or exclude every cone.
''')
