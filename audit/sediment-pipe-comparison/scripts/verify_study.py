"""Run recorded tests, verify source bytes, and inventory final study artifacts."""
from pathlib import Path
import csv
import hashlib
import importlib.metadata
import json
import platform
import subprocess
import sys

BASE=Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checked=[]
    with (BASE/'image-manifest.csv').open(encoding='utf-8') as stream:
        for row in csv.DictReader(stream):
            path=BASE/row['path']
            assert digest(path)==row['sha256'],str(path)
            if row['label_sha256']:
                assert digest(path.with_suffix('.LBL'))==row['label_sha256'],str(path)
            checked.append(row['case_id'])
    environment={'python':sys.version,'platform':platform.platform(),
                 'packages':{name:importlib.metadata.version(name) for name in
                             ['numpy','scipy','matplotlib','Pillow','PyMuPDF']}}
    (BASE/'results/environment.json').write_text(json.dumps(environment,indent=2)+'\n')
    run=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(BASE/'tests'),'-v'],
                       stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (BASE/'results/tests.txt').write_text(run.stdout,encoding='utf-8')
    print(run.stdout)
    if run.returncode:
        raise SystemExit(run.returncode)
    (BASE/'results/source-verification.json').write_text(json.dumps(
        {'verified_manifest_entries':checked,'all_image_and_label_checksums_match':True},indent=2)+'\n')
    artifacts={str(path.relative_to(BASE)).replace('\\','/'):digest(path)
               for path in sorted(BASE.rglob('*')) if path.is_file()
               and '__pycache__' not in path.parts and path.suffix!='.pyc'
               and path.name!='artifact-manifest.json'}
    (BASE/'results/artifact-manifest.json').write_text(json.dumps(artifacts,indent=2)+'\n')
    print('Verified',len(checked),'source entries and inventoried',len(artifacts),'artifacts.')


if __name__=='__main__':
    main()
