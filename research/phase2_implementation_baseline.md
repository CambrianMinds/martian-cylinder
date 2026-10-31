# Phase II Implementation Baseline Report
**Date:** October 30, 2026  
**Repository:** `CambrianMinds/martian-cylinder`  
**Working Directory:** `d:\projects\martian-cylinder`  
**Investigation Phase:** Phase II Independent Geometric Validation  

---

## 1. Active Commit and Branch Status

- **Upstream Remote Tracking:** `origin/master` points to commit `1e23f434911c4ac59f9b188657c9ce19327942c5` ("update DOI, documentation, and research articles for Martian cylinder analysis").
- **Current Local Branch:** `master`, ahead of `origin/master` by 1 commit (`04782e5` "modified gitignore").
- **Working Tree State:** Dirty (uncommitted Phase I remediation modifications and newly authored files).
- **Explanation of Visibility on GitHub:** The Phase I remediation cycle completed locally and is fully present in the local workspace, but has not yet been committed or pushed upstream to `origin/master`. Hence, external reviewers inspecting GitHub `master` at `1e23f43` would not yet see the Phase I files. All files are intact locally and ready for Phase II validation.

---

## 2. Inventory of Available Remediation Files

### Newly Created in Phase I:
1. `geometry_utils.py` (3,446 bytes): Rotation-invariant line fitting (total least squares / SVD), normalized straightness, sliding window analysis, face/axis projection functions (`view_angle_from_face_ratio`, `axial_deforeshortening_factor`, `project_cylinder_orthographic`), and bootstrap confidence intervals.
2. `audit_reanalysis.py` (10,950 bytes): Standalone script executing corrected physical projections, common-pipeline straightness extraction across all 20 control rocks, and bootstrap descriptive statistics.
3. `data/audit_reanalysis.json` (7,341 bytes): Machine-readable results from `audit_reanalysis.py`.
4. `AUDIT_RESPONSE.md` (6,311 bytes): Detailed issue-by-issue audit response addressing Findings 1 through 9.
5. `tests/` directory:
   - `tests/test_geometry_utils.py`: 12 automated unit tests validating projection formulas, TLS straightness invariance, and bootstrap statistics.
   - `tests/test_edge_pipeline.py`: 3 automated unit tests validating the common edge detection pipeline on synthetic step edges.
   - `tests/cylinder_projection.test.js`: 4 automated Node.js unit tests validating the interactive projection engine.

### Modified Existing Files:
1. `cylinder-tool/cylinder.js`: Added physical camera-distance model (`cameraDistanceMm`, `mmPerPx`, `getCameraDistancePx`, `setCameraDistanceMm`), resolving the dimensionless ratio error (Finding 3).
2. `cylinder-tool/app.js`: Refactored camera input controls to physical range in meters (3.96 m nominal focus).
3. `cylinder-tool/index.html`: Updated UI labels to "Camera Range (commanded focus, m)".
4. `reproduce_analysis.py`: Preserved deterministic historical reproduction while annotating legacy projection factors and adding explicit audit notes on descriptive statistics.
5. `README.md` & `martian_cylinder_paper.md`: Added prominent post-publication warning banners linking to `AUDIT_RESPONSE.md`.
6. `.github/workflows/verify.yml`: Added automated execution steps for `tests/` and `audit_reanalysis.py`.

---

## 3. Existing Test Execution and Verification Results

Executed locally on October 30, 2026:
- **Python Unit Tests:** `python -m unittest discover -s tests -v`
  - Result: **15 passed, 0 failed, 0 errors** (Runtime: 0.092s).
- **Node.js Projection Engine Tests:** `node tests/cylinder_projection.test.js`
  - Result: **4 passed, 0 failed** (All tests passed).
- **Historical Deterministic Reproduction:** `python reproduce_analysis.py --crop-only`
  - Result: **Exit Code 0** (Reproduces stored values while printing audit annotations).
- **Full PDS Archive Verification:** `python reproduce_analysis.py`
  - Result: **Exit Code 0** (Cryptographic SHA-256 integrity verified across all 8 PDS files).
- **Corrected Audit Re-analysis:** `python audit_reanalysis.py --json data/audit_reanalysis.json`
  - Result: **Exit Code 0** (Executes corrected projection, shared edge pipeline, and bootstrap statistics).

---

## 4. Differences Between Reported Changes and Actual Implementation

1. **Camera Distance Model:** The physical camera distance model is active and verified in `cylinder-tool/cylinder.js` and `app.js`. When `cameraDistanceMm` is set (3957 mm), $Z_0 = \text{range} / s_\perp = 13,514\text{ px}$, correctly producing a 0.8% rear-to-front perspective contraction ($0.9920$) instead of the erroneous 20.7% contraction ($0.7932$).
2. **Projected Axis vs Silhouette Extent:** In `reproduce_analysis.py`, the 110 px value was treated as axial extent. The reanalysis in `audit_reanalysis.py` correctly decoupled the projected center-to-center axis ($38.8\text{ px}$) from the apex-to-apex silhouette ($74\text{ px}$).
3. **Common Straightness Pipeline Status:** The shared edge pipeline implemented in `audit_reanalysis.py` successfully processed all 20 control rocks (finding R01 straight at $0.173\text{ px}$ TLS RMSE), but on the target sub-raster it extracted rows ($1.74\text{ px}$) rather than locking cleanly onto the upper generator ($0.111\text{ px}$). This confirms the audit's warning: the target comparison in Phase I remained incomplete.

---

## 5. Dependencies and Environmental Requirements

- **Operating System:** Windows 11 (64-bit).
- **Python Runtime:** Python 3.12.3 (`D:\python-3.12\python.exe`).
- **Installed Packages:**
  - `numpy`: 1.26.4
  - `scipy`: 1.15.3
  - `Pillow` (PIL): 12.1.1
- **Node Runtime:** Node.js v25.9.0.
- **LaTeX Environment:** TeX Live 2026 (pdfTeX 3.141592653-2.6-1.40.29).
- **External Network Access:** Offline-capable; all NASA PDS images, crops, metadata labels, and control JSONs are stored locally in `data/`. No external package downloads are required for local verification.

