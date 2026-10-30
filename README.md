# Morphological and Photometric Analysis of an Unidentified Cylindrical Feature in Curiosity Sol 3556 Mastcam Imagery

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23789092.svg)](https://doi.org/10.5281/zenodo.23789092)
[![Verification Suite](https://github.com/cambrianminds/martian-cylinder/actions/workflows/verify.yml/badge.svg)](https://github.com/cambrianminds/martian-cylinder/actions/workflows/verify.yml)
[![License: MIT](https://img.shields.io/badge/Code%20License-MIT-blue.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/Text%20License-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](requirements.txt)

**Author:** Justin Bogner (Cambrian Minds)  
**Technical Report:** `CMR-2026-01` · October 2026 · **DOI:** [`10.5281/zenodo.23789092`](https://doi.org/10.5281/zenodo.23789092)  
**Live Monograph & Interactive Studio:** [https://cambrianminds.github.io/martian-cylinder/](https://cambrianminds.github.io/martian-cylinder/)

## Overview

This repository contains the complete NASA Planetary Data System (PDS) raw telemetry, calibrated image products, LaTeX/Markdown manuscripts, interactive 3D central-perspective photogrammetry studio, and deterministic Python verification suite for the forensic investigation of the cylindrical anomaly imaged by the Mars Science Laboratory (*Curiosity*) Mastcam Right ($100\text{ mm}$) camera on Sol 3556 (August 7, 2022, 12:10:25 Local True Solar Time) at Paraitepuy Pass in Gale Crater (PDS Product ID: `3556MR1025170721700585C00`).

### Key Empirical Findings

| Metric / Parameter | Measured Value | Uncertainty / Control Comparison | Source / Method |
| :--- | :--- | :--- | :--- |
| **PDS Product ID** | `3556MR1025170721700585C00` | `DRCL`, `DRCX`, `DRLX`, `DRXX` | NASA PDS Archive (Release `0032`) |
| **Focus Motor Count & Slant Range** | `2705` counts $\rightarrow 3.957\text{ m}$ | $3.63\text{--}4.30\text{ m}$ optical DoF ($3.6\text{--}4.4\text{ m}$ PDS) | `MSL:FOCUS_POSITION_COUNT`, Eq. (1)–(3) |
| **Normal & Axial Pixel Scale** | $\text{IFOV} = 0.074\text{ mrad/px}$ | $0.269\text{--}0.318\text{ mm/px}$ ($s_\perp$) to $0.291\text{--}0.344\text{ mm/px}$ ($s_{\text{axial}}$) | Mastcam-100 ($f=100\text{ mm}, f/12, c=7.4\,\mu\text{m}$) |
| **Transverse Diameter ($D$)** | $11.0 \pm 1.2\text{ mm}$ (nominal) | $9.1\text{--}12.0\text{ mm}$ ($s_\perp$) / $10.8\text{--}12.5\text{ mm}$ ($s_{\text{axial}}$) | Normal silhouette vs. 3D axial envelope |
| **Exposed Longitudinal Length ($L$)** | $35 \pm 2\text{ mm}$ | $32.0\text{--}37.9\text{ mm}$ ($110.0\text{ px}$; nominal $34.87\text{ mm}$) | 3D Central-Perspective Projection (Fig. 4) |
| **Aspect Ratio ($L/D$)** | $3.24 : 1$ | $+12.06\,\sigma$ sample SD; Cantelli $p < 0.007$; rank $1/21$ | Natural clasts ($N=20$): $\mu = 1.23 \pm 0.16$ (live verified) |
| **End-Cap Circularity ($b/a$)** | $0.9335$ | $+1.03\,\sigma$ sample SD ($p = 0.15$); perspective invariant | Matches 3D viewing foreshortening $\cos\beta$ ($1.8^\circ$) |
| **Generator Parallelism ($R^2$)** | $0.9985$ ($\Delta\theta < 0.7^\circ$) | $+10.70\,\sigma$ sample SD; Cantelli $p < 0.009$; rank $1/21$ | Natural clasts ($N=20$): $\overline{R^2} = 0.104 \pm 0.081$, max $0.271$ |
| **Solar Shadow & Relief** | $\cot(69.8224^\circ) = 0.3675$ | $S = 9.8\pm 0.7\text{ px} \implies h \in [7.8, 8.5]\text{ mm}$, $D_{\text{recon}} \in [10.8, 11.7]\text{ mm}$ | Reconciled across normal ($0.293$) & ground ($0.317\text{ mm/px}$) scales |
| **Regolith Burial & Dust Clock** | $33.5\%$ buried ($2.0\text{--}3.2\text{ mm}$) | $80\text{--}200\text{ yr}$ ($2.0\text{ mm}$) to $128\text{--}320\text{ yr}$ ($3.2\text{ mm}$) | Passive fallout rate $10\text{--}25\,\mu\text{m/Earth yr}$ |

## Repository Structure

```text
martian-cylinder/
├── README.md                          # Repository documentation and reproduction guide
├── CITATION.cff                       # Machine-readable academic citation metadata (CFF 1.2.0)
├── LICENSE                            # Dual MIT (code) / CC-BY-4.0 (manuscripts) / Public Domain (PDS data)
├── requirements.txt                   # Python dependencies for the verification suite
├── reproduce_analysis.py              # Standalone peer-review verification script (exit code 0)
├── martian_cylinder_paper.tex         # Formal scientific manuscript (LaTeX source)
├── martian_cylinder_paper.pdf         # Compiled formal scientific manuscript (PDF)
├── martian_cylinder_paper.md          # Markdown version of the formal scientific manuscript
├── citizen_science_article.tex        # Companion citizen science & methodology essay (LaTeX source)
├── citizen_science_article.pdf        # Compiled citizen science essay monograph (PDF)
├── citizen_science_article.md         # Markdown version of the citizen science essay
├── DRXX-metadata.txt                  # Full ASCII PDS3 ODL/VICAR label for 3556MR1025170721700585C00
├── index.html                         # Public multimedia monograph website
├── site.css                           # Stylesheet for the public presentation website
├── site.js                            # Interactive lightbox and BibTeX copy controller
├── llms.txt                           # Structured LLM/crawler summary of verified findings
├── cylinder-tool/                     # Interactive 3D Central-Perspective Photogrammetry Studio
│   ├── index.html                     # Studio web interface (pre-calibrated to Sol 3556 fit)
│   ├── cylinder.js                    # 3D central-perspective cylinder projection engine
│   ├── app.js                         # Viewport, Sobel edge filter, and telemetry controller
│   ├── presets_data.js                # Embedded base64 Sol 3556 discovery crop for offline use
│   └── style.css                      # Studio UI stylesheet
└── data/                              # Raw NASA PDS archive files, figures, and control measurements
    ├── 3556MR1025170721700585C00_DRCL.{IMG,LBL,fits,png}  # Radiometrically calibrated color product
    ├── 3556MR1025170721700585C00_DRCX.{IMG,LBL,fits,png}  # Full-frame calibrated color product (1328x1184)
    ├── 3556MR1025170721700585C00_DRLX.{IMG,LBL,fits}      # Linearized radiometric product
    ├── 3556MR1025170721700585C00_DRXX.{IMG,LBL,fits}      # Uncalibrated raw RDR product
    ├── control_rocks_distribution.json                    # N = 20 background clast measurements & statistics
    ├── crop_bottom_right.png                              # 500x450 regional context crop (DRCL[700:1150, 800:1300])
    ├── thumb_mask.jpg                                     # Figure 2 segmentation and solar shadow mask
    ├── sobel_analysis_panel.png                           # Figure 3 multi-axis Sobel gradient panel
    ├── martian-cylinder-overlay-1792827816792.png         # Figure 4 3D photogrammetric fit (110x34 px, AR 3.24:1)
    ├── mastcam_full_context.png                           # Full Mastcam-100 context diagram
    ├── scale_comparison.png                               # Physical scale comparison vs. ANSI AA battery
    └── bogner_mariner1971_report.pdf                      # JPL TM 33-591 (R. S. Bogner, 1973, N73-25095)
```

## Reproducing the Analysis & Compiling Manuscripts

### 1. Run the Deterministic Verification Suite

Install the minimal scientific Python dependencies (`numpy`, `Pillow`) and run `reproduce_analysis.py`:

```bash
pip install -r requirements.txt
python3 reproduce_analysis.py
```

For lightweight or sandbox-constrained environments without the full 40 MB raw PDS binaries, run with `--crop-only`:

```bash
python3 reproduce_analysis.py --crop-only
```

The script verifies the SHA-256 checksums of all eight raw NASA PDS `.IMG`/`.LBL` archive files (in standard mode), parses the ODL telemetry header, validates the CAHVOR camera matrix intrinsics and optical depth-of-field equations, projects the SPICE solar shadow vector ($+23.3728^\circ$), reconstructs the dual-scale vertical shadow relief, verifies the exact pixel provenance of `crop_bottom_right.png` (`DRCL[700:1150, 800:1300]`) and the $120 \times 120$ Sobel sub-raster (`DRCL[940:1060, 1009:1129]`), performs multi-parameter perturbation sensitivity sweeps across 75 generator windows and 81 ellipse sectors, independently extracts and verifies all $N=20$ background control clasts directly from live detector pixels ($0.00\text{ px}$ axis discrepancy, $0.0000\ R^2$ discrepancy, $\text{SNR} > 1.5$), and recomputes both population ($\text{ddof}=0$) and unbiased sample ($\text{ddof}=1$) $z$-scores and Cantelli inequalities.

### 2. Recompile the LaTeX Manuscripts

Both manuscripts use portable standard TeX Live packages (`lmodern`, `amsmath`, `booktabs`, `graphicx`, `geometry`, `hyperref`, `cite`, `caption`, `microtype`) and compile cleanly with `pdflatex` or `lualatex`:

```bash
pdflatex -interaction=nonstopmode martian_cylinder_paper.tex
pdflatex -interaction=nonstopmode martian_cylinder_paper.tex

pdflatex -interaction=nonstopmode citizen_science_article.tex
pdflatex -interaction=nonstopmode citizen_science_article.tex
```

### 3. Launch the Interactive 3D Photogrammetry Studio

Open `cylinder-tool/index.html` directly in any modern browser (or serve the repository root via `python3 -m http.server 8000`). The studio opens pre-calibrated to the Sol 3556 cylinder fit ($110 \times 34\text{ px}$, $\theta = 218^\circ$, $\text{Tilt} = 156^\circ$, $\text{AR} = 3.24:1$, $0.317\text{ mm/px}$).

## Citation

```bibtex
@techreport{bogner2026martian,
  author      = {Bogner, Justin},
  title       = {Morphological and Photometric Analysis of an Unidentified Cylindrical Feature in Curiosity Sol 3556 Mastcam Imagery: Constraints on Aeolian, Diagenetic, and Artificial Provenance via Sub-Pixel Gradient Forensics},
  institution = {Cambrian Minds},
  number      = {CMR-2026-01},
  year        = {2026},
  month       = oct,
  url         = {https://cambrianminds.github.io/martian-cylinder/martian_cylinder_paper.pdf}
}
```
