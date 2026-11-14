"""
Pipeline Reproducibility and Audit Integrity Test Suite
Part of the Argon Red-Team Audit of martian-cylinder.
Tests file integrity, PDS checksums, existence of reproduction databases,
and claim ledger completeness.
"""

import unittest
import os
import hashlib
import json
import csv

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
INDEP_DIR = os.path.join(ROOT_DIR, "independent-reconstruction")
AUDIT_DIR = os.path.join(ROOT_DIR, "audit")

class TestReproducibility(unittest.TestCase):

    def test_pds_raw_checksums(self):
        """Verify raw PDS image checksums match step1_provenance.json exactly."""
        with open(os.path.join(INDEP_DIR, "step1_provenance.json")) as f:
            prov = json.load(f)
        
        for pds_key in ["DRXX", "DRLX", "DRCX", "DRCL"]:
            fname = prov[pds_key]["file"]
            file_path = os.path.join(DATA_DIR, fname)
            self.assertTrue(os.path.exists(file_path), f"Missing {fname}")
            
            with open(file_path, "rb") as f:
                computed_sha = hashlib.sha256(f.read()).hexdigest()
            
            stored_sha = prov[pds_key]["sha256"]
            self.assertEqual(computed_sha, stored_sha, f"Checksum mismatch for {fname}")
            label = os.path.splitext(file_path)[0] + '.LBL'
            with open(label, 'rb') as f:
                self.assertEqual(hashlib.sha256(f.read()).hexdigest(), prov[pds_key]['lbl_sha256'])

    def test_reconstruction_pipeline_outputs_exist(self):
        """Verify all 8 independent-reconstruction output JSON files exist and are non-empty."""
        expected_files = [
            "measurements.json",
            "step1_provenance.json",
            "step2_camera_geometry.json",
            "step3_features.json",
            "step4_endface_models.json",
            "step5_3d_interpretations.json",
            "step8_pebble_and_rear_terminus.json",
            "step9_joint_model.json"
        ]
        for fname in expected_files:
            fpath = os.path.join(INDEP_DIR, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing pipeline output {fname}")
            self.assertGreater(os.path.getsize(fpath), 100, f"File {fname} appears empty")

    def test_claim_ledger_integrity(self):
        """Verify numerical claim ledger CSV exists, has > 50 entries, and no broken fields."""
        ledger_path = os.path.join(AUDIT_DIR, "numerical-claim-ledger.csv")
        self.assertTrue(os.path.exists(ledger_path), "numerical-claim-ledger.csv does not exist")
        
        with open(ledger_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        self.assertGreaterEqual(len(rows), 50, "Ledger must contain at least 50 claims")
        for i, row in enumerate(rows):
            self.assertTrue(row["Claim_ID"], f"Row {i} missing Claim_ID")
            self.assertTrue(row["Status"], f"Row {i} missing Status")
            self.assertTrue(row["Text_Quoted_Value"], f"Row {i} missing Text_Quoted_Value")

    def test_root_pdf_repaired(self):
        """The distributed root paper must equal the valid paper in papers/."""
        root_pdf = os.path.join(ROOT_DIR, "martian-cylinder-technical-paper.pdf")
        self.assertTrue(os.path.exists(root_pdf))
        
        real_pdf = os.path.join(ROOT_DIR, "papers", "martian-cylinder-technical-paper.pdf")
        self.assertTrue(os.path.exists(real_pdf))
        self.assertGreater(os.path.getsize(real_pdf), 100000, "Real PDF in papers/ must exceed 100 KB")
        with open(root_pdf, "rb") as f:
            root_bytes = f.read()
        with open(real_pdf, "rb") as f:
            self.assertEqual(root_bytes, f.read())
        self.assertTrue(root_bytes.startswith(b"%PDF-"))
        self.assertIn(b"%%EOF", root_bytes[-1024:])

if __name__ == "__main__":
    unittest.main()
