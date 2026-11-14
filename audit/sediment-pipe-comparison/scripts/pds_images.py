"""Read the archived PDS3 arrays and record their product provenance."""
from pathlib import Path
import csv
import hashlib
import json
import re
import numpy as np
from PIL import Image, ImageDraw

BASE = Path(__file__).resolve().parents[1]


def field(label, key, default=''):
    match = re.search(r'^\s*' + re.escape(key) + r'\s*=\s*([^\r\n]+)', label, re.M)
    return match.group(1).strip().strip('"') if match else default


def read_image(path):
    path = Path(path)
    label = path.with_suffix('.LBL').read_text(encoding='ascii', errors='replace')
    section = re.search(r'^OBJECT\s*=\s*IMAGE\s*$([\s\S]*?)^END_OBJECT\s*=\s*IMAGE\s*$', label, re.M).group(1)
    height, width, bands = [int(field(section, key)) for key in ['LINES', 'LINE_SAMPLES', 'BANDS']]
    bits = int(field(section, 'SAMPLE_BITS'))
    signed = field(section, 'SAMPLE_TYPE') == 'MSB_INTEGER'
    dtype = np.dtype(('>' if 'MSB' in field(section, 'SAMPLE_TYPE') else '<') +
                     ('i' if signed else 'u') + str(bits // 8))
    pointer = re.search(r'\^IMAGE\s*=\s*\("[^"\n]+"\s*,\s*(\d+)\)', label)
    offset = (int(pointer.group(1)) - 1) * int(field(label, 'RECORD_BYTES')) if pointer else 0
    raw = np.fromfile(path, dtype=dtype, offset=offset, count=bands * height * width)
    assert raw.size == bands * height * width
    image = raw.reshape(bands, height, width).astype(float)
    scaling = re.search(r'RADIANCE_SCALING_FACTOR\s*=\s*\(([^)]+)\)', label)
    if scaling:
        factors = np.array([float(x) for x in scaling.group(1).split(',')])
        image *= factors[:, None, None]
    return image.mean(axis=0), label


def main():
    acquisitions = {}
    for file in (BASE / 'sources').glob('*-results.json'):
        for record in json.loads(file.read_text()):
            if record['status'] in ['downloaded', 'cached']:
                acquisitions[record['path']] = record
    rows = []
    thumbs = []
    for path in sorted((BASE / 'sources/images').glob('*.IMG')):
        image, label = read_image(path)
        low, high = np.percentile(image, [1, 99])
        preview = Image.fromarray(np.uint8(np.clip((image-low)/(high-low), 0, 1)*255))
        preview.convert('RGB').save(BASE / 'figures' / (path.stem + '-preview.png'))
        preview.thumbnail((470, 370))
        tile = Image.new('RGB', (490, 420), 'white')
        tile.paste(preview, (10, 35));ImageDraw.Draw(tile).text((8, 5), path.stem, fill='black')
        thumbs.append(tile)
        record = acquisitions[path.relative_to(BASE).as_posix()]
        rows.append(dict(case_id=path.stem, product_id=field(label, 'PRODUCT_ID'),
                         instrument=field(label, 'INSTRUMENT_ID'),
                         acquisition_date=field(label, 'START_TIME'),
                         sol=field(label, 'PLANET_DAY_NUMBER', field(label, 'PLANET_DAY_NUMBER', path.name[:4])),
                         processing_level=field(label, 'DATA_SET_ID'),
                         width=image.shape[1], height=image.shape[0],
                         sample_bits=16, path=path.relative_to(BASE).as_posix(),
                         url=record['url'], sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                         label_sha256=hashlib.sha256(path.with_suffix('.LBL').read_bytes()).hexdigest(),
                         eligibility='pending visual screening',
                         optical_blur='not independently calibrated'))
    with (BASE / 'image-manifest.csv').open('w', newline='', encoding='utf-8') as stream:
        writer=csv.DictWriter(stream, fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    sheet=Image.new('RGB', (980, 420*((len(thumbs)+1)//2)), '#dddddd')
    for index,tile in enumerate(thumbs):sheet.paste(tile, ((index%2)*490, (index//2)*420))
    sheet.save(BASE/'figures/original-image-inventory.png')
    print('Decoded and inventoried',len(rows),'original PDS products.')


if __name__ == '__main__':
    main()
