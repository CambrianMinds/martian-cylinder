"""Compact exports and record checksums. Coordinates are native-equivalent pixels."""
from pathlib import Path
import csv,gzip,json,hashlib,io
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'audit/comparative-study'

def main():
    for path in list(OUT.glob('edge-windows-*.csv'))+[OUT/'ellipse-arcs.csv']:
        if not path.exists():continue
        # Gzip has a stable timestamp for deterministic scientific exports.
        with path.open(encoding='utf-8',newline='') as src, path.with_suffix('.csv.gz').open('wb') as raw:
            with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as zipped:
                with io.TextIOWrapper(zipped,encoding='utf-8',newline='') as dest:
                    reader=csv.DictReader(src);writer=csv.DictWriter(dest,fieldnames=reader.fieldnames)
                    writer.writeheader();writer.writerows(reader)
    manifest={}
    for p in sorted(OUT.rglob('*')):
        intermediate=p.name.startswith('edge-windows-') and p.suffix=='.csv' or p.name=='ellipse-arcs.csv'
        if p.is_file() and '__pycache__' not in str(p) and p.name!='artifact-checksums.json' and not intermediate:
            manifest[p.relative_to(OUT).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
    (OUT/'artifact-checksums.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Hashed {len(manifest)} artifacts.')

if __name__=='__main__':main()
