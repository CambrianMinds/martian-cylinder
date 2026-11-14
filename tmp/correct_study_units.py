from pathlib import Path
import csv,json
OUT=Path(__file__).resolve().parents[1]/'comparative-study'
def correct(value):
    if isinstance(value,dict):
        for k,v in value.items():
            if k=='start_arc_px':value[k]=v*2
            else:correct(v)
    elif isinstance(value,list):
        for v in value:correct(v)
for name in ['results.json','comparison-summary.json']:
    p=OUT/name;d=json.loads(p.read_text());correct(d);p.write_text(json.dumps(d,indent=2)+'\n')
for p in list(OUT.glob('edge-windows-*.csv'))+[OUT/'ellipse-arcs.csv']:
    temporary=p.with_suffix('.fixed.csv')
    with p.open(newline='') as src,temporary.open('w',newline='') as dest:
        reader=csv.DictReader(src);writer=csv.DictWriter(dest,fieldnames=reader.fieldnames);writer.writeheader()
        for r in reader:
            r['start_arc_px']=str(float(r['start_arc_px'])*2);writer.writerow(r)
    temporary.replace(p)
