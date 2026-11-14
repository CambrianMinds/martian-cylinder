"""Report sourced shadow claims; no independent ray-tracing computation."""
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
    (ROOT/'audit/shadow_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])
if __name__=='__main__': main()
