"""Guard against false-positive reproduction and untraceable evidence."""
from pathlib import Path
import csv
import importlib.util
import json
import tempfile
import types
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('reproducer', ROOT/'audit/scripts/audit_reproduce_pipeline.py')
reproducer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reproducer)

class TestAuditTools(unittest.TestCase):
    def run_mocked_pipeline(self, returncode, before, after):
        with tempfile.TemporaryDirectory() as temp:
            log = Path(temp)/'log.md'
            proc = types.SimpleNamespace(returncode=returncode, stdout='', stderr='')
            with patch.object(reproducer, 'JSON_TARGETS', ['one.json']), \
                 patch.object(reproducer, 'REPRO_LOG', str(log)), \
                 patch.object(reproducer, 'snapshot_jsons', side_effect=[{'one.json':before}, {'one.json':after}]), \
                 patch.object(reproducer.subprocess, 'run', return_value=proc):
                status = reproducer.main()
            return status, log.read_text(encoding='utf-8')

    def test_failed_run_with_unchanged_outputs_is_failure(self):
        snap = {'sha256':'a', 'json':{'x':1.0}}
        status, log = self.run_mocked_pipeline(1, snap, snap)
        self.assertEqual(status, 1)
        self.assertIn('FAILED', log)
        self.assertNotIn('All outputs are bit-for-bit identical', log)

    def test_equivalent_numbers_do_not_imply_identical_bytes(self):
        before = {'sha256':'a', 'json':{'x':1.0}}
        after = {'sha256':'b', 'json':{'x':1.00000001}}
        status, log = self.run_mocked_pipeline(0, before, after)
        self.assertEqual(status, 0)
        self.assertIn('bytes differ', log)

    def test_numeric_drift_fails(self):
        status, log = self.run_mocked_pipeline(0, {'sha256':'a','json':{'x':1.0}}, {'sha256':'b','json':{'x':2.0}})
        self.assertEqual(status, 1)

    def test_ledger_values_resolve_to_actual_sources(self):
        with (ROOT/'audit/numerical-claim-ledger.csv').open(encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
        cache = {}
        for row in rows:
            source = row['Source_File']
            if source not in cache:
                cache[source] = json.loads((ROOT/source).read_text(encoding='utf-8'))
            value = cache[source]
            for key in row['JSON_Pointer'].split('/')[1:]:
                key = key.replace('~1','/').replace('~0','~')
                value = value[int(key)] if isinstance(value,list) else value[key]
            self.assertEqual(str(value), row['Text_Quoted_Value'])
            self.assertEqual(row['Status'], 'STORED_VALUE')

    def test_photometry_summary_uses_current_pipeline(self):
        s5 = json.loads((ROOT/'independent-reconstruction/step5_3d_interpretations.json').read_text())
        controls = json.loads((ROOT/'audit/geological_controls_audit.json').read_text())
        self.assertEqual(controls['pipeline_clinometry'], s5['transverse_photometry_clinometry'])

if __name__ == '__main__':
    unittest.main()
