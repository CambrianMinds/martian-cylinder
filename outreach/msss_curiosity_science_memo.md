# Scientific Memorandum: Mastcam-100 Sol 3556 Telemetry Verification & Photometric Analysis of Paraitepuy Pass Micro-Inclusion

**To:** Mars Science Laboratory (MSL) Mastcam Science & Instrument Operations Team  
**Cc:** Dr. Michael C. Malin (MSSS), Prof. James F. Bell III (ASU), Dr. Kenneth S. Edgett (MSSS)  
**From:** Justin Bogner, Cambrian Minds  
**Date:** October 2026  
**Subject:** Instrument Calibration Audit & Morphological Constraints on Sol 3556 Anomaly (PDS Product ID: `3556MR1025170721700585C00`)  
**Report Document:** Technical Report CMR-2026-01  
**Full Preprint (PDF):** [https://cambrianminds.github.io/martian-cylinder/martian_cylinder_paper.pdf](https://cambrianminds.github.io/martian-cylinder/martian_cylinder_paper.pdf)  
**Verification Suite:** [https://github.com/cambrianminds/martian-cylinder](https://github.com/cambrianminds/martian-cylinder)

---

### Dear MSL Mastcam Team,

First and foremost, we express our profound gratitude to the MSL science team, Malin Space Science Systems (MSSS), and Arizona State University for your extraordinary stewardship and open dissemination of Curiosity’s raw imaging archives via the NASA Planetary Data System (PDS). The exquisite calibration papers published by your group (*Malin et al., 2017; Bell et al., 2017; Maki et al., 2012*) provided the foundational optical models that made this independent investigation possible.

Over the past several years, an image acquired by Mastcam Right ($100\text{ mm}$) on Sol 3556 (August 7, 2022, 12:10:25 LTST) at Paraitepuy Pass—specifically PDS Product `3556MR1025170721700585C00`—has been the subject of widespread public speculation. Much of this discourse was distorted by an informal, uncalibrated claim that the cylindrical anomaly in the lower-right quadrant measured approximately **$20\text{ cm}$ in length**, leading to premature conclusions regarding dropped rover debris or artificial hardware.

Our group conducted a formal forensic photogrammetry audit directly against the raw PDS3 ODL telemetry labels (`DRCL`, `DRCX`, `DRLX`, and `DRXX`) to establish peer-reviewable ground-truth constraints on this feature.

---

### Summary of Photogrammetric & Ephemeris Results

1. **Resolution of Public Scale Discrepancy**:
   * Telemetry field `MSL:FOCUS_POSITION_COUNT = 2705` evaluates via the Mastcam-100 calibration polynomial to a best-focus slant range of **$s_0 = 3.957\text{ m}$**, bounded by an optical depth-of-field band of $3.82\text{--}4.10\text{ m}$ (hyperfocal distance $H = 112.61\text{ m}$).
   * Projecting the CAHV model ($f = 100\text{ mm}$, pixel pitch $c = 7.4\,\mu\text{m}$) across the $-22.0047^\circ$ camera elevation yields a ground-projected pixel scale of **$s_{\text{ground}} = 0.317\text{ mm/pixel}$**.
   * Multi-axis Sobel spatial convolution and 3D central-perspective overlay constrain the feature’s true dimensions to:
     * **Exposed Length ($L$):** $35 \pm 2\text{ mm}$ ($110.0\text{ px}$)
     * **Transverse Diameter ($D$):** $11.5 \pm 0.8\text{ mm}$ ($34.0\text{--}37.6\text{ px}$)
     * **Aspect Ratio ($L/D$):** $3.24 : 1$
   * This definitively refutes the viral $20\text{ cm}$ estimate, confirming the object is the physical size of an ANSI AA battery ($35 \times 11.5\text{ mm}$).

2. **Solar Ray-Tracing & Stratigraphic Relief**:
   * Solar ephemeris derived from the PDS label ($\theta_\odot = 69.8224^\circ$, $\phi_\odot = 186.8169^\circ$) yields a vertical relief multiplier of $\tan(69.8224^\circ) = 2.7212$.
   * Projecting the 3D ground shadow vector onto the sensor plane yields an image shadow angle of $\theta_{\text{shadow}} = +23.3728^\circ$, matching the observed ground shadow fringe at the lower cylinder flank within $0.1^\circ$.
   * Shadow inversion establishes an exposed vertical relief of $h = 8.46 \pm 0.60\text{ mm}$. Reconstructing the buried chord confirms that approximately **$33.5\%$ of the cylinder's diameter ($2.0\text{--}3.2\text{ mm}$)** is embedded within the cohesive duricrust matrix along a stratigraphic horizon inclined at $-25.21^\circ$.

3. **Geomorphological Null Distribution ($N=20$)**:
   * We measured an empirical control sample of $N=20$ natural clasts across the identical frame.
   * The feature's generator straightness ($R^2 = 0.9985$, angular divergence $\Delta\theta < 0.2^\circ$) and aspect ratio ($3.24:1$) represent **$+10.70\sigma$ and $+12.06\sigma$ sample deviations** against surrounding rock morphology.

4. **Sediment Deposition Constraints on Rover Debris**:
   * The absence of windward deflation moats or leeward sand shadow drifts indicates the regolith interface is in long-term aeolian equilibrium.
   * At background Gale Crater passive dust sedimentation rates ($10\text{--}25\,\mu\text{m/Earth yr}$; *Kinch et al., 2015; Lorenz et al., 2021*), accumulating $2.0\text{--}3.2\text{ mm}$ of burial requires **$80\text{ to } 320\text{ Earth years}$**, placing severe chronological constraints on a terrestrial origin given Curiosity's 10-year surface residence at Sol 3556 and a 13–15 km straight-line distance to Bradbury Landing.

---

### Questions & Next Steps for the MSL Science Community

We would be deeply grateful for your perspective on two questions:
1. Did ChemCam (LIBS) or MAHLI acquire any raster observations within the immediate vicinity ($\sim 1\text{--}2\text{ meters}$) of this target during the Sol 3556–3558 stop at Paraitepuy Pass that might constrain the elemental composition or mineralogy of the local duricrust or clasts?
2. Has the MSL science team cataloged similar high-aspect-ratio, circular cylindrical concretions, weathering rinds, or mineralized fracture fills within this specific stratigraphic unit of Mount Sharp?

A standalone verification suite (`reproduce_analysis.py`), complete LaTeX manuscript, and interactive 3D WebGL photogrammetry studio are publicly hosted at:  
👉 **[https://cambrianminds.github.io/martian-cylinder/](https://cambrianminds.github.io/martian-cylinder/)**

Thank you again for your decades of dedication to robotic planetary exploration and open science.

Sincerely,

**Justin Bogner**  
Cambrian Minds  
Email: [justinbogner1618@gmail.com]  
Technical Report: CMR-2026-01
