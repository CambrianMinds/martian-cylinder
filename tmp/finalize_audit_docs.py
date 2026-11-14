from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'papers/martian-cylinder-technical-paper.tex'
s=p.read_text(encoding='utf-8')
s=s.replace("That is an actual competing result, not a mismatch in the reported data.", "That is a reproducible numerical result. A direct physical check, however, rejects the fitted formulation as a frustum silhouette: in axial coordinates its line is $v=-r-mu$, with $m=(1-s)r/L$. Tangency to the end ellipse $u^2/b^2+v^2/a^2=1$ requires $r^2=a^2+m^2b^2$. M4 gives $r=19.294848\\px$ whereas the required intercept is $19.433711\\px$. Its line therefore cuts its own projected end ellipse. The lower RMS does not validate its physical interpretation. This algebraic failure is distinct from assigning a fixed-front-shape rear-scan deviance to M4, which also changes front shape and orientation.")
s=s.replace("The scientific result is not that the photograph forces a particular taper. It is that the measured boundaries admit a stringent constant-section cylindrical configuration, while an explicitly different tapered formulation also captures the image geometry. Their different axial relations matter to physical interpretation. Since the image provides one camera view of partially buried surfaces, image-plane model selection alone does not close the 3D reconstruction uniquely.", "The measured boundaries admit a stringent constant-section cylindrical configuration. M4 captures the image geometry numerically but fails its own physical tangency condition and is rejected as a physical frustum. This does not test every possible cone or uniquely establish material or origin. A full camera-ray and occlusion-constrained alternative fit remains distinct work.")
s=re.sub(r'An additional radiometric test examines intensity.*?(?=\n\n)', r'An additional radiometric test examines intensity across the upper body. The current Step 5 output reports curvature coefficient $-0.01285 \\pm 0.01357$, with significance $z=0.95$, and relative residuals 0.02682 for the planar fit and 0.02673 for the quadratic fit. Historical prose quoted 7.38 or 11.45 for other or undocumented selections; those values are not reproduced by the current pipeline. The current test does not establish significant curvature or reject planar shading. Albedo, scattering, dust, and illumination geometry further limit shape inference from brightness.', s, flags=re.S)
p.write_text(s,encoding='utf-8')

# Replace the unsupported three-proof explanation with the actual M4 failure.
p=ROOT/'independent-reconstruction/report_layman.md'; s=p.read_text(encoding='utf-8')
start=s.find('   **No. The cone is ruled out by three independent physical proofs:**')
end=s.find('\n---',start)
if start>=0 and end>=0:
    s=s[:start]+'''   **The tested M4 model fails a physical consistency check.** Its upper outline cuts through its own fitted end ellipses instead of touching them as a solid frustum's silhouette must. Its smaller fitting error is real, but its proposed physical geometry is inconsistent. The audit gives the calculation. This rejects M4's formulation without claiming that every possible tapered object has been tested.
'''+s[end:]
s=s.replace('~30–35 mm long', '~12 mm exposed projected center separation at the assumed range')
s=s.replace('both ends of the object have the exact same circular curve and diameter', 'the exposed rear curve can be closely fitted by an unchanged copy of the front ellipse')
p.write_text(s,encoding='utf-8')

p=ROOT/'audit/argon-red-team-report.md';s=p.read_text(encoding='utf-8')
s=s.replace('Root PDF copied byte-for-byte from valid `papers/` PDF. This restores the existing paper; it does not regenerate that historical paper from current claims.', 'Paper source corrected for M4 tangency and current photometry, rebuilt, and copied byte-for-byte to the root PDF.')
p.write_text(s,encoding='utf-8')
