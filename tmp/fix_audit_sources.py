from pathlib import Path
import subprocess
import json
ROOT=Path(__file__).resolve().parents[1]
def write(name,s): (ROOT/name).write_text(s,encoding='utf-8')
# Restore only our link-only edits to historical documents and the user's staged brief.
for name in ['teaching-myself-the-scientific-method-rev10-corrected.md','teaching-myself-the-scientific-method-rev11.md','teaching-myself-the-scientific-method-rev12.md','martian-cylinder-red-team-brief.md']:
    ref=':'+name if name=='martian-cylinder-red-team-brief.md' else 'HEAD:'+name
    (ROOT/name).write_bytes(subprocess.check_output(['git','show',ref],cwd=ROOT))

write('audit/scripts/audit_shadow_raycast.py', '''"""Report sourced shadow claims; no independent ray-tracing computation."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
def main():
    source=ROOT/'most-recent-work.md'
    text=source.read_text(encoding='utf-8')
    for required in ['32.82', '1.049', '6.746', '28.10', '35.12']:
        if required not in text:
            raise ValueError('Reported source changed; review shadow transcription')
    result={
        'status': 'REPORTED_NOT_INDEPENDENTLY_REPRODUCED',
        'source': 'most-recent-work.md',
        'source_lines': [{'line':i, 'text':line} for i,line in enumerate(text.splitlines(),1)
                         if any(x in line for x in ['32.82','28.10','1.049','6.746'])],
        'best_fit_85dn': {'receiving_plane_rotation_deg':32.82,'native_rms_px':1.049,'flat_ground_native_rms_px':6.746},
        'threshold_rotation_span_deg':[28.10,35.12],
        'threshold_rms_span_px':[0.753,1.049],
        'independent_ground_survey':False,
        'intermediate_threshold_values_verified':False
    }
    (ROOT/'audit/shadow_audit.json').write_text(json.dumps(result,indent=2)+'\\n')
    print(result['status'])
if __name__=='__main__': main()
''')
write('audit/scripts/audit_rock_controls_benchmark.py', '''"""Separate actual pipeline photometry from unreplicated narrative rock controls."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
def main():
    source=ROOT/'independent-reconstruction/report.md'
    lines=source.read_text(encoding='utf-8').splitlines()
    s5=json.loads((ROOT/'independent-reconstruction/step5_3d_interpretations.json').read_text())
    result={
        'rock_controls_status':'REPORTED_NOT_INDEPENDENTLY_REPRODUCED',
        'rock_controls_source':'independent-reconstruction/report.md',
        'reported_control_lines':[{'line':i,'text':line} for i,line in enumerate(lines,1)
            if any(x in line for x in ['0.971','1.724','1.953','8.02','1.64','2.45','2.98'])],
        'pipeline_clinometry':s5['transverse_photometry_clinometry'],
        'pipeline_source':'independent-reconstruction/step5_3d_interpretations.json#/transverse_photometry_clinometry',
        'regional_population_inference_supported':False
    }
    (ROOT/'audit/geological_controls_audit.json').write_text(json.dumps(result,indent=2)+'\\n')
    print(json.dumps(result['pipeline_clinometry'],indent=2))
if __name__=='__main__': main()
''')

# The current step5 output contradicts both 7.38 and 11.45 sigma prose.
z=json.loads((ROOT/'independent-reconstruction/step5_3d_interpretations.json').read_text())['transverse_photometry_clinometry']['convexity_significance_z_sigma']
for name in ['README.md','llms.txt','independent-reconstruction/report.md','independent-reconstruction/report_layman.md','independent-reconstruction/methods.md']:
    p=ROOT/name; s=p.read_text(encoding='utf-8')
    first,sep,rest=s.partition('\n')
    notice=f'**Photometry correction:** The current Step 5 JSON reports curvature significance z={z:.2f}, not the historical 7.38 or 11.45 quoted below. Those older shading-rejection claims are superseded; the current pipeline does not establish significant convex curvature. The three-rock comparison remains a reported, unreplicated narrative benchmark.\n'
    write(name,first+'\n\n'+notice+rest)
    # Remove misleading significance assertions rather than rely on a banner alone.
    s=(ROOT/name).read_text(encoding='utf-8')
    import re
    s=re.sub(r'^.*(?:11\.45|>11\\sigma|>11|7\.38|> 11 standard|> 11\\sigma).*$',
        f'Current Step 5 photometry: z={z:.2f}; significant curvature or rejection of flat shading is not established.',s,flags=re.M)
    write(name,s)

p=ROOT/'audit/argon-red-team-report.md'
s=p.read_text(encoding='utf-8').replace('## Corrections to the audit itself','## Corrections to the audit itself\n\nThe current Step 5 output reports curvature significance z=0.95, contradicting both the historical 7.38 in the report and the audit\'s hardcoded 11.45. The rock audit now reads the real pipeline output. Neither historical significance is current evidence.')
write('audit/argon-red-team-report.md',s)
