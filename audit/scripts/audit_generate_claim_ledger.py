"""Inventory actual JSON numbers; no invented prose verification or line numbers."""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[2]
FIELDS = ['Claim_ID', 'Source_File', 'JSON_Pointer', 'Text_Quoted_Value',
          'Machine_Truth_Value', 'Status', 'Audit_Findings_And_Notes']

def numeric_leaves(value, pointer=''):
    if isinstance(value, dict):
        for k, v in value.items():
            key = str(k).replace('~', '~0').replace('/', '~1')
            yield from numeric_leaves(v, pointer+'/'+key)
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from numeric_leaves(v, pointer+'/'+str(i))
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        yield pointer, value

def main():
    rows = []
    sources = sorted((ROOT/'independent-reconstruction').glob('*.json'))
    sources += sorted((ROOT/'audit').glob('*_audit.json'))
    for source in sources:
        for pointer, value in numeric_leaves(json.loads(source.read_text(encoding='utf-8'))):
            # Keep named scalar summaries; coordinate and scan arrays remain in JSON.
            if any(part.isdigit() for part in pointer.split('/')):
                continue
            rows.append(dict(zip(FIELDS, [f'NUM-{len(rows)+1:05}', source.relative_to(ROOT).as_posix(),
                pointer, str(value), '', 'STORED_VALUE',
                'Actual source value; not independent truth or verification of narrative claims.'])))
    with (ROOT/'audit/numerical-claim-ledger.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f'Inventoried {len(rows)} numeric values with exact JSON pointers.')

if __name__ == '__main__':
    main()
