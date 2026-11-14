"""
Audit Reproduction Pipeline Script
Executes independent-reconstruction/scripts/run_all.py and checks determinism against committed JSON.
Generates audit/reproduction-log.md.
"""

import os
import sys
import subprocess
import time
import json
import hashlib
import platform
import numpy as np

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INDEP_DIR = os.path.join(ROOT_DIR, "independent-reconstruction")
VENV_PYTHON = sys.executable
AUDIT_DIR = os.path.join(ROOT_DIR, "audit")
REPRO_LOG = os.path.join(AUDIT_DIR, "reproduction-log.md")

JSON_TARGETS = [
    "step1_provenance.json",
    "step2_camera_geometry.json",
    "step3_features.json",
    "step4_endface_models.json",
    "step5_3d_interpretations.json",
    "step8_pebble_and_rear_terminus.json",
    "step9_joint_model.json",
    "measurements.json"
]

def sha256_file(path):
    if not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def snapshot_jsons():
    data = {}
    for j in JSON_TARGETS:
        p = os.path.join(INDEP_DIR, j)
        if os.path.exists(p):
            with open(p, "rb") as f:
                content = f.read()
            data[j] = {
                "sha256": hashlib.sha256(content).hexdigest(),
                "bytes": len(content),
                "json": json.loads(content.decode("utf-8"))
            }
        else:
            data[j] = None
    return data

def compare_json_dicts(d1, d2, path=""):
    diffs = []
    if type(d1) != type(d2):
        return [f"{path}: type mismatch ({type(d1)} vs {type(d2)})"]
    if isinstance(d1, dict):
        all_keys = set(d1.keys()).union(set(d2.keys()))
        for k in all_keys:
            subpath = f"{path}.{k}" if path else k
            if k not in d1:
                diffs.append(f"{subpath}: missing in original")
            elif k not in d2:
                diffs.append(f"{subpath}: missing in new run")
            else:
                diffs.extend(compare_json_dicts(d1[k], d2[k], subpath))
    elif isinstance(d1, list):
        if len(d1) != len(d2):
            diffs.append(f"{path}: list length mismatch ({len(d1)} vs {len(d2)})")
        else:
            for i, (v1, v2) in enumerate(zip(d1, d2)):
                diffs.extend(compare_json_dicts(v1, v2, f"{path}[{i}]"))
    elif isinstance(d1, float) or isinstance(d2, float):
        # Check numerical equality
        if not np.isclose(d1, d2, rtol=1e-5, atol=1e-7):
            diffs.append(f"{path}: float value change ({d1} -> {d2}, delta={d2 - d1})")
    else:
        if d1 != d2:
            diffs.append(f"{path}: value change ({d1} -> {d2})")
    return diffs

def main():
    print("=== STARTING REPRODUCTION RUN OF independent-reconstruction/scripts/run_all.py ===")
    
    # Snapshot before
    before_snap = snapshot_jsons()
    
    t0 = time.time()
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    env["PYTHONUTF8"] = "1"
    env["MPLBACKEND"] = "Agg"
    
    proc = subprocess.run(
        [VENV_PYTHON, os.path.join(INDEP_DIR, "scripts", "run_all.py")],
        cwd=INDEP_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env
    )
    runtime = time.time() - t0
    
    print(f"Execution finished in {runtime:.2f} seconds with exit code {proc.returncode}")
    
    # Snapshot after
    after_snap = snapshot_jsons()
    
    diff_report = {}
    total_diff_count = 0
    for j in JSON_TARGETS:
        b = before_snap[j]
        a = after_snap[j]
        if b is None or a is None:
            diff_report[j] = ["File missing in before or after!"]
            total_diff_count += 1
            continue
        
        sha_match = (b["sha256"] == a["sha256"])
        if sha_match:
            diff_report[j] = []
        else:
            diffs = compare_json_dicts(b["json"], a["json"])
            diff_report[j] = diffs
            total_diff_count += len(diffs)
            print(f"  {j}: {len(diffs)} numerical/text diffs (SHA256 changed from {b['sha256'][:10]} to {a['sha256'][:10]})")
    
    print(f"\nTotal numerical diffs detected across all JSON outputs: {total_diff_count}")

    # Generate audit/reproduction-log.md
    with open(REPRO_LOG, "w", encoding="utf-8") as f:
        f.write("# Argon Audit: Reproduction Log\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Python:** {sys.version.split()[0]}\n")
        f.write(f"**Platform:** {platform.system()} {platform.machine()}\n")
        f.write(f"**Command:** `run_all.py`\n")
        f.write(f"**Working Directory:** `independent-reconstruction/`\n")
        f.write(f"**Exit Code:** {proc.returncode}\n")
        f.write(f"**Runtime:** {runtime:.2f} seconds\n\n")
        
        f.write("## 1. Reproduction Status\n\n")
        f.write("| Output Artifact | Pre-Run SHA256 | Post-Run SHA256 | Bit-for-Bit Deterministic? | Numerical Equivalence |\n")
        f.write("| :--- | :--- | :--- | :---: | :---: |\n")
        for j in JSON_TARGETS:
            b_sha = before_snap[j]["sha256"] if before_snap[j] else "N/A"
            a_sha = after_snap[j]["sha256"] if after_snap[j] else "N/A"
            diffs = diff_report.get(j, [])
            det = "Yes" if b_sha == a_sha else "No"
            num_eq = "Identical" if len(diffs) == 0 else f"{len(diffs)} diffs"
            f.write(f"| `{j}` | `{b_sha[:12]}` | `{a_sha[:12]}` | {det} | {num_eq} |\n")
        
        f.write("\n## 2. Numerical Differences / Drift Detail\n\n")
        if proc.returncode != 0:
            f.write("Pipeline execution FAILED; unchanged outputs do not establish reproduction.\n\n")
        elif total_diff_count == 0:
            exact = all(before_snap[j] and after_snap[j] and before_snap[j]["sha256"] == after_snap[j]["sha256"] for j in JSON_TARGETS)
            f.write("All outputs are bit-for-bit identical.\n\n" if exact else "Outputs are numerically equivalent within rtol=1e-5, atol=1e-7; bytes differ.\n\n")
        else:
            for j, diffs in diff_report.items():
                if diffs:
                    f.write(f"### `{j}`\n")
                    for d in diffs[:20]:
                        f.write(f"- {d}\n")
                    if len(diffs) > 20:
                        f.write(f"- ... and {len(diffs)-20} more diffs.\n")
                    f.write("\n")

        f.write("## 3. Standard Output Log\n\n```text\n")
        f.write(proc.stdout)
        f.write("\n```\n\n")
        
        if proc.stderr:
            f.write("## 4. Standard Error Log\n\n```text\n")
            f.write(proc.stderr)
            f.write("\n```\n\n")

    print(f"Reproduction log successfully written to: {REPRO_LOG}")
    return 1 if proc.returncode != 0 or total_diff_count else 0

if __name__ == "__main__":
    sys.exit(main())
