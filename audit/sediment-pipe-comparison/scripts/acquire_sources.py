"""Download explicitly inventoried public sources with cached byte verification."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request, urlopen
import hashlib
import json
import sys

BASE = Path(__file__).resolve().parents[1]


def acquire(item):
    destination = BASE / item['path']
    if destination.exists():
        data = destination.read_bytes()
        return {**item, 'status': 'cached', 'bytes': len(data),
                'sha256': hashlib.sha256(data).hexdigest()}
    try:
        request = Request(item['url'], headers={'User-Agent': 'Sediment-pipe-research/1.0'})
        with urlopen(request, timeout=35) as response:
            data = response.read()
            metadata = {'resolved_url': response.url,
                        'content_type': response.headers.get('Content-Type', '')}
        if item['path'].endswith('.pdf') and not data.startswith(b'%PDF'):
            raise ValueError('Expected PDF response')
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        return {**item, **metadata, 'status': 'downloaded', 'bytes': len(data),
                'sha256': hashlib.sha256(data).hexdigest()}
    except Exception as error:
        return {**item, 'status': 'failed', 'error': str(error)}


def main():
    plan = BASE / (sys.argv[1] if len(sys.argv) > 1 else 'sources/acquisition-plan.json')
    items = json.loads(plan.read_text(encoding='utf-8'))
    records = list(ThreadPoolExecutor(max_workers=2).map(acquire, items))
    output = plan.with_name(plan.stem + '-results.json')
    output.write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
    for record in records:
        print(record['status'], record['path'], record.get('error', ''))


if __name__ == '__main__':
    main()
