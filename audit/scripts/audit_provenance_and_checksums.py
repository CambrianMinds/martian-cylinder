"""
Audit Provenance and Checksums Script
Part of the Argon Red-Team Audit of martian-cylinder.
Verifies SHA-256 hashes of all primary NASA PDS files and active pipeline assets.
Parses PDS3 labels to confirm observational metadata.
"""

import os
import hashlib
import json
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
INDEP_DIR = os.path.join(ROOT_DIR, "independent-reconstruction")
PAPERS_DIR = os.path.join(ROOT_DIR, "papers")

def sha256_file(filepath):
    if not os.path.isfile(filepath):
        return None
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

def parse_pds_label_value(content, key):
    # PDS quoted strings can span physical lines.
    quoted = re.findall(r'^\s*' + re.escape(key) + r'\s*=\s*"([^"]*)"', content, re.MULTILINE)
    quoted = [value for value in quoted if value.strip().upper() != 'NULL']
    if quoted:
        return ' '.join(quoted[-1].split())
    # Match KEY = VALUE across all occurrences, return non-NULL if possible
    matches = re.findall(r'^\s*' + re.escape(key) + r'\s*=\s*(.+?)\r?$', content, re.MULTILINE)
    if matches:
        for val in reversed(matches):  # usually later occurrence is the telemetry/instrument specific one
            val = val.strip()
            # Strip <units>
            val = re.sub(r'<[^>]+>', '', val).strip()
            # Clean quotes
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1].strip()
            if val.upper() != "NULL":
                return val
        return matches[-1].strip()
    return None

def main():
    print("=== AUDITING PROVENANCE, DATA INTEGRITY, AND PDS3 METADATA ===")
    
    # 1. Primary Data Checksums
    primary_files = [
        "3556MR1025170721700585C00_DRXX.IMG",
        "3556MR1025170721700585C00_DRXX.LBL",
        "3556MR1025170721700585C00_DRXX.fits",
        "3556MR1025170721700585C00_DRXX.png",
        "3556MR1025170721700585C00_DRLX.IMG",
        "3556MR1025170721700585C00_DRLX.LBL",
        "3556MR1025170721700585C00_DRLX.fits",
        "3556MR1025170721700585C00_DRCX.IMG",
        "3556MR1025170721700585C00_DRCX.LBL",
        "3556MR1025170721700585C00_DRCL.IMG",
        "3556MR1025170721700585C00_DRCL.LBL",
        "crop_bottom_right.png"
    ]
    
    data_checksums = {}
    for fname in primary_files:
        fpath = os.path.join(DATA_DIR, fname)
        size = os.path.getsize(fpath) if os.path.exists(fpath) else -1
        csum = sha256_file(fpath)
        data_checksums[fname] = {"bytes": size, "sha256": csum}
        print(f"  {fname:<38} : {size:>10} bytes | {csum}")

    # 2. Check root vs papers PDF
    root_pdf = os.path.join(ROOT_DIR, "martian-cylinder-technical-paper.pdf")
    papers_pdf = os.path.join(PAPERS_DIR, "martian-cylinder-technical-paper.pdf")
    root_pdf_size = os.path.getsize(root_pdf) if os.path.exists(root_pdf) else -1
    papers_pdf_size = os.path.getsize(papers_pdf) if os.path.exists(papers_pdf) else -1
    print("\n--- Technical Paper PDF Check ---")
    print(f"  Root PDF size:   {root_pdf_size} bytes (SHA256: {sha256_file(root_pdf)})")
    print(f"  Papers PDF size: {papers_pdf_size} bytes (SHA256: {sha256_file(papers_pdf)})")
    if root_pdf_size < 1000:
        print("  [DEFECT DETECTED] Root PDF is a truncated pointer/corrupted stub (15 bytes)!")

    # 3. Verify PDS3 Label Fields in DRXX.LBL
    drxx_lbl_path = os.path.join(DATA_DIR, "3556MR1025170721700585C00_DRXX.LBL")
    with open(drxx_lbl_path, "r", encoding="latin-1") as f:
        drxx_lbl = f.read()

    meta_checks = {
        "INSTRUMENT_ID": parse_pds_label_value(drxx_lbl, "INSTRUMENT_ID"),
        "FILTER_NAME": parse_pds_label_value(drxx_lbl, "FILTER_NAME"),
        "EXPOSURE_DURATION": float(parse_pds_label_value(drxx_lbl, "EXPOSURE_DURATION") or 0),
        "INST_CMPRS_MODE": int(parse_pds_label_value(drxx_lbl, "INST_CMPRS_MODE") or -1),
        "INST_CMPRS_NAME": parse_pds_label_value(drxx_lbl, "INST_CMPRS_NAME"),
        "BEST_FOCUS_DISTANCE": float(parse_pds_label_value(drxx_lbl, "MSL:BEST_FOCUS_DISTANCE") or 0),
        "MINIMUM_FOCUS_DISTANCE": float(parse_pds_label_value(drxx_lbl, "MSL:MINIMUM_FOCUS_DISTANCE") or 0),
        "MAXIMUM_FOCUS_DISTANCE": float(parse_pds_label_value(drxx_lbl, "MSL:MAXIMUM_FOCUS_DISTANCE") or 0),
        "SOLAR_AZIMUTH": float(parse_pds_label_value(drxx_lbl, "SOLAR_AZIMUTH") or 0),
        "SOLAR_ELEVATION": float(parse_pds_label_value(drxx_lbl, "SOLAR_ELEVATION") or 0),
        "SOL_ID": parse_pds_label_value(drxx_lbl, "PLANET_DAY_NUMBER"),
        "START_TIME": parse_pds_label_value(drxx_lbl, "IMAGE_TIME"),
        "LOCAL_TRUE_SOLAR_TIME": parse_pds_label_value(drxx_lbl, "LOCAL_TRUE_SOLAR_TIME"),
    }

    print("\n--- PDS3 Label Metadata Verification (DRXX.LBL) ---")
    for k, v in meta_checks.items():
        print(f"  {k:<25}: {v}")

    # 4. Compare with step1_provenance.json
    prov_path = os.path.join(INDEP_DIR, "step1_provenance.json")
    if os.path.exists(prov_path):
        with open(prov_path, "r") as f:
            stored_prov = json.load(f)
        print("\n--- Comparing with step1_provenance.json ---")
        for prod, info in stored_prov.items():
            if not isinstance(info, dict) or "sha256" not in info:
                continue
            expected_csum = info.get("sha256")
            img_fname = info.get("file")
            actual_csum = data_checksums.get(img_fname, {}).get("sha256")
            match = (expected_csum == actual_csum)
            print(f"  {img_fname:<38}: SHA256 Match = {match}")

    # Save summary
    out_json = os.path.join(ROOT_DIR, "audit", "provenance_audit.json")
    with open(out_json, "w") as f:
        json.dump({
            "primary_checksums": data_checksums,
            "metadata_checks": meta_checks,
            "root_pdf_defect": {"size": root_pdf_size, "expected_size": papers_pdf_size,
                "detected": root_pdf_size < 1000 or sha256_file(root_pdf) != sha256_file(papers_pdf)},
            "verification_scope": "Local checksums and stored PDS label values; no remote archive download or SPICE kernel recomputation."
        }, f, indent=2)
    print(f"\nSaved audit summary to: {out_json}")

if __name__ == "__main__":
    main()
