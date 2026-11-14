# Reproducing the comparison

Run from the repository root. This study writes only inside `audit/sediment-pipe-comparison`. The technical manuscript and original extraction outputs are inputs, not generated products of these commands.

Python 3.13 was used with NumPy, SciPy, Matplotlib, Pillow and PyMuPDF. Exact installed versions are in `results/environment.json`. Install these packages in a separate environment if needed. The existing tracked modules under `independent-reconstruction` and the original Sol 3556 PDS image under `data/` are required. The working-tree inputs identified in `sources/baseline.json` must also be present to run the original-input invariance test. Their hashes distinguish this study's actual starting state from the parent commit.

In PowerShell, set the interpreter once:

```powershell
$studyPython = 'C:\Users\Justi\AppData\Local\Programs\Python\Python313\python.exe'
```

The downloaded sources are retained locally. `image-manifest.csv` contains exact PDS URLs, original image and label checksums, instrument identifiers, acquisition dates and processing levels. Publication figures are used for visual screening only. No measurements were made on printed illustrations.

The acquisition logs preserve failed historical URL attempts as well as resolved URLs. To fetch all successfully resolved products into an otherwise empty study source directory, use the consolidated `sources/resolved-acquisition.json`:

```powershell
& $studyPython audit/sediment-pipe-comparison/scripts/acquire_sources.py sources/resolved-acquisition.json
```

The downloader caches existing files; integrity is checked separately against the retained manifest. Network access may require permission in a sandbox. An HTTP failure must not be interpreted as evidence about the geology.

Recompute in this order:

```powershell
& $studyPython audit/sediment-pipe-comparison/scripts/target_benchmark.py
& $studyPython audit/sediment-pipe-comparison/scripts/pds_images.py
& $studyPython audit/sediment-pipe-comparison/scripts/screen_inventory.py
& $studyPython audit/sediment-pipe-comparison/scripts/control_metrology.py
& $studyPython audit/sediment-pipe-comparison/scripts/run_physical_experiments.py
& $studyPython audit/sediment-pipe-comparison/scripts/final_checks.py
& $studyPython audit/sediment-pipe-comparison/scripts/reevaluate_m4.py
& $studyPython audit/sediment-pipe-comparison/scripts/build_report.py
& $studyPython audit/sediment-pipe-comparison/scripts/verify_study.py
```

`verify_study.py` records the automated test output and verifies original-image and label hashes. It also writes an artifact manifest. Floating-point fitting can vary slightly across SciPy versions; the benchmark assertions use tolerances at the reported precision. The observed-control extraction takes longer than the small geometric fits because every profile and seed sensitivity is retained.

The visual screening classifications and selections are human decisions recorded in JSON, not an automated discovery algorithm. Re-running the screen script reproduces those decisions. The Yellowknife M100 localization record gives a camera-ray estimate based on an approximate focus distance; visual scene correspondence established the selected tile. Its predicted location is not treated as an independently measured range. Localization does not enter a fit or score.

`figures/` contains the reproducible analysis graphics. Page images in `sources/` are inspection aids from the retained primary PDFs; they are not numerical inputs. `results/physical-frustum.json` is a later, explicitly exploratory physical model. The frozen protocol and dated amendments distinguish prespecified work from subsequent extensions.

The full requested natural-object N+R+D comparison and formation-to-image validation remain incomplete because the screened objects do not expose the required configuration. `report.md` identifies the completed partial measurements and the remaining tests. No missing geological family is assigned a failure score.

The M4 reevaluation adds finite-generator distances to both physical models. Earlier results retain their original extended-line scoring for traceability. The source import paths support the workspace's later move into `independent-reconstruction/scripts`. The benchmark explicitly locates the target image in repository `data/`. Hash verification accepts an unchanged baseline Python source at its relocated path.
