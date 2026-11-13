"""Separate actual pipeline photometry from unreplicated narrative rock controls."""
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
    (ROOT/'audit/geological_controls_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['pipeline_clinometry'],indent=2))
if __name__=='__main__': main()
