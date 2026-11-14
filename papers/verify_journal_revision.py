"""Verify the November 13 paper's retained numbers, provenance and final PDF."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import importlib.metadata
import fitz
from build_paper_evidence import verify, canonical_text_sha, matches_recorded_text_hash

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    baseline = load(HERE/'journal-revision-baseline.json')
    preserved = {}
    for relative, expected in baseline['sha256'].items():
        if relative.startswith('audit/'):
            actual = sha(ROOT/relative)
            assert matches_recorded_text_hash(ROOT/relative,expected), relative
            preserved[relative] = actual
    manifest = load(HERE/'paper-evidence-manifest.json')
    for relative, expected in manifest['sha256'].items():
        path=ROOT/relative
        canonical=manifest['canonical_lf_sha256'].get(relative)
        assert sha(path)==expected or (canonical and canonical_text_sha(path)==canonical), relative
    prediction = load(ROOT/'audit/predictive-validation/results.json')
    verify(prediction)
    checks = {
        'm1_joint': (prediction['full_m1_fit']['total_rms_px'], .3788),
        'sparse_rear': (prediction['sparse_rear_registration']['test_rms_px'], .2084),
        'guarded_rear': (prediction['blocked_rear_registration']['pooled_test_rms_px'], .2429),
        'guarded_joint': (prediction['blocked_m1_prediction']['total_rms_px'], .7233),
        'entire_dorsal_withheld': (prediction['dorsal_entirely_withheld']['withheld_dorsal_rms_px'], 1.9092),
    }
    for name, (value, expected) in checks.items():
        assert abs(value-expected) < .00005, name
    figure = load(HERE/'figure-provenance.json')
    assert figure['station_counts'] == {'front': 35, 'rear': 24, 'dorsal': 26}
    assert figure['roi_half_open_xxyy'] == [1014, 1104, 932, 1007]
    assert figure['shape_yx'] == [1184, 1328]
    assert len(figure['dorsal_indices_past_generator_endpoint']) == 5
    assert abs(figure['recomputed_m1_rms_px']-.37882893015484004) < 1e-9
    summary = load(ROOT/'audit/comparative-study/comparison-summary.json')['sigma0.7_span36.4']
    images = load(ROOT/'audit/comparative-study/image-manifest.json')['images']
    whole_frames = [row for row in images if row.get('role') == 'whole_frame']
    assert len(whole_frames) == 18
    windows = ROOT/'audit/comparative-study/edge-windows-sigma0.7_span36.4.csv.gz'
    import csv
    import gzip
    qualifying_frames = set()
    with gzip.open(windows, 'rt', encoding='utf-8') as stream:
        for row in csv.DictReader(stream):
            if float(row['rms_px']) <= summary['target_selected']['rms_px']:
                qualifying_frames.add(row['scene'])
    assert len(qualifying_frames) == 17
    source = (HERE/'martian-cylinder-technical-paper.tex').read_text(encoding='utf-8')
    original = subprocess.check_output(['git', 'show', baseline['starting_commit']+
                                        ':papers/martian-cylinder-technical-paper.tex'], cwd=ROOT).decode('utf-8')
    equations = lambda text: re.findall(r'\\begin\{(equation|align)\}(.*?)\\end\{\1\}', text, re.S)
    normalize = lambda blocks: [(kind, ' '.join(body.split())) for kind, body in blocks]
    assert normalize(equations(source)) == normalize(equations(original)), 'Original equations changed'
    citations = lambda text: set(re.findall(r'\\bibitem\{([^}]+)\}', text))
    assert citations(original).issubset(citations(source)), 'Original bibliography entry removed'
    assert '0.2549' in source and '19.433711' in source, 'Original M4 rejection missing'
    document = fitz.open(HERE/'martian-cylinder-technical-paper.pdf')
    text = '\n'.join(page.get_text() for page in document)
    assert baseline['title'] in ' '.join(text.split())
    assert baseline['subtitle'] in ' '.join(text.split())
    for expected in ['13 November 2026', '0.3788', '0.2084', '0.2429', '0.7233', '1.9092',
                     '226,426', '835', 'Planetary-Science Significance']:
        assert expected in text, expected
    assert '\ufffd' not in text
    log = (HERE/'martian-cylinder-technical-paper.log').read_text(encoding='utf-8')
    errors = ['Overfull', 'Missing character:', 'There were undefined references',
              'There were undefined citations', 'Rerun to get cross-references right']
    for error in errors:
        assert error not in log, error
    # Each image is embedded as an authentic raster with vector annotations.
    image_shapes = {}
    for name in ['target-boundaries', 'joint-m1-overlay']:
        image_doc = fitz.open(HERE/'figures'/f'{name}.pdf')
        image_shapes[name] = sorted(set((item[2], item[3]) for item in image_doc[0].get_images()))
    assert (1328, 1184) in image_shapes['target-boundaries']
    assert (90, 75) in image_shapes['joint-m1-overlay']
    report = {
        'starting_commit': baseline['starting_commit'], 'branch': 'paper/nov13-journal-revision',
        'preserved_results_sha256': preserved, 'verified_manifest_entries': len(manifest['sha256']),
        'prediction_values_px': {name: value for name, (value, _) in checks.items()},
        'original_equation_environments_preserved': len(equations(original)),
        'original_bibliography_entries_preserved': len(citations(original)),
        'whole_frames': len(whole_frames), 'frames_with_qualifying_segments': len(qualifying_frames),
        'images_checked': 28, 'control_windows': 226426, 'qualifying_windows': 835,
        'image_raster_dimensions_in_vector_figures': image_shapes,
        'pdf_pages': len(document), 'pdf_sha256': sha(HERE/'martian-cylinder-technical-paper.pdf'),
        'source_sha256': sha(HERE/'martian-cylinder-technical-paper.tex'),
        'latex_errors_absent': errors,
        'font_substitution_notices': log.count('LaTeX Font Warning:'),
        'underfull_box_notices': log.count('Underfull'),
        'verification_python': sys.version,
        'verification_packages': {name: importlib.metadata.version(name)
                                  for name in ['numpy','scipy','matplotlib','Pillow','PyMuPDF']},
        'scope': 'Numerical and provenance checks. Visual page inspection is documented in the change report.'}
    (HERE/'journal-numerical-verification.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
