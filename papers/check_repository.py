"""Catch merge regressions in current documents, data roots and paper inputs."""
from pathlib import Path
import importlib.util
import json
import re
import sys
import subprocess
import fitz

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'independent-reconstruction/scripts'))
from build_paper_evidence import canonical_text_sha, sha, verify


def main():
    source = ROOT/'papers/martian-cylinder-technical-paper.tex'
    text = source.read_text(encoding='utf-8')
    assert 'Subpixel Geometric Reconstruction of a Cylindrical Candidate' in text
    assert 'Boundary metrology, frozen-shape prediction, and geological comparison' in text
    assert 'Planetary-Science Significance' in text
    assert 'FiniteCylinderFitRMS' in text and '19.433711' in text
    assert (ROOT/'teaching-myself-the-scientific-method-rev16.md').is_file()
    assert not list(ROOT.glob('teaching-myself-the-scientific-method-rev1[0-3]*.md'))
    tracked_tmp=subprocess.check_output(['git','ls-files','--','tmp'],cwd=ROOT,text=True)
    assert not tracked_tmp.strip(), 'Temporary files were reintroduced into Git'
    archive=json.loads((ROOT/'archive/superseded-docs-2026-11-13/provenance.json').read_text())
    for item in archive:
        assert sha(ROOT/item['archive_path'])==item['sha256'],item['archive_path']
    pdf = ROOT/'papers/martian-cylinder-technical-paper.pdf'
    assert pdf.read_bytes() == (ROOT/'martian-cylinder-technical-paper.pdf').read_bytes()
    with fitz.open(pdf) as document:
        assert '13 November 2026' in document[0].get_text()
        assert len(document) == 18
    manifest = json.loads((ROOT/'papers/paper-evidence-manifest.json').read_text())
    for relative, expected in manifest['sha256'].items():
        path = ROOT/relative
        assert path.is_file(), relative
        canonical = manifest['canonical_lf_sha256'].get(relative)
        assert sha(path) == expected or (canonical and canonical_text_sha(path) == canonical), relative
    verify(json.loads((ROOT/'audit/predictive-validation/results.json').read_text()))
    import step3_feature_extraction as extraction
    assert Path(extraction.OUT_DIR).resolve() == (ROOT/'independent-reconstruction').resolve()
    assert Path(extraction.DATA_DIR).resolve() == (ROOT/'data').resolve()
    _, _, image = extraction.load_drxx()
    assert image.shape == (1184, 1328)
    for path in (ROOT/'independent-reconstruction/scripts').glob('step*.py'):
        spec = importlib.util.spec_from_file_location('pathcheck_'+path.stem, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        assert Path(module.OUT_DIR).resolve() == (ROOT/'independent-reconstruction').resolve(), path
    checked = 0
    for relative in ['README.md', 'independent-reconstruction/report.md',
                     'independent-reconstruction/report_layman.md', 'independent-reconstruction/methods.md',
                     'archive/README.md']:
        doc = ROOT/relative
        for target in re.findall(r'\]\(([^)]+)\)', doc.read_text(encoding='utf-8')):
            if '://' in target or target.startswith('#'):
                continue
            destination = target.split('#', 1)[0]
            if destination:
                assert (doc.parent/destination).resolve().exists(), (relative, target)
                checked += 1
    print('Current paper, matching PDFs, latest essay, numerical manifest, nine script roots, and', checked, 'documentation links verified.')


if __name__ == '__main__':
    main()
