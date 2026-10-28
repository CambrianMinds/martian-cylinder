# Technical Memorandum: NASA PDS Telemetry Audit & Photogrammetric Correction for Curiosity Sol 3556 Anomaly

**To:** Prof. Avi Loeb, Frank B. Baird Jr. Professor of Science, Harvard University; Head, The Galileo Project  
**From:** Justin Bogner, Cambrian Minds  
**Date:** October 2026  
**Subject:** Photogrammetric Scale Correction & Geomorphological Constraints on the Sol 3556 Curiosity "Cylinder" (PDS Product `3556MR1025170721700585C00`)  
**Technical Report Reference:** CMR-2026-01  
**Full Paper (PDF):** [https://cambrianminds.github.io/martian-cylinder/martian_cylinder_paper.pdf](https://cambrianminds.github.io/martian-cylinder/martian_cylinder_paper.pdf)  
**Interactive 3D Tool & Verification Suite:** [https://cambrianminds.github.io/martian-cylinder/](https://cambrianminds.github.io/martian-cylinder/)  
**Code Repository:** [https://github.com/cambrianminds/martian-cylinder](https://github.com/cambrianminds/martian-cylinder)

---

### Executive Summary

In your March 2026 essay (*"Is the Mysterious Cylinder on Mars, Photographed in 2022 by the Curiosity Rover, a Human-Made Debris?"*), you highlighted the curious geometry of the cylindrical feature imaged by the *Curiosity* rover Mastcam Right (100 mm) camera on Sol 3556 at Paraitepuy Pass. In that article and subsequent discussions, an early informal estimate was cited suggesting the object measures approximately **$20\text{ cm}$ ($8\text{ inches}$) in length**.

Because this $20\text{ cm}$ figure has propagated across public and scientific commentary, our team conducted a rigorous, deterministic forensic audit directly against the raw NASA Planetary Data System (PDS Release 0032) telemetry and CAHVOR camera matrices. 

We write to share our findings and provide the verified physical parameters for your records and any future commentary:

---

### Key Findings & Telemetry Corrections

1. **Physical Scale is $35\text{ mm}$, Not $20\text{ cm}$ (AA Battery Scale)**:
   * Parsing the raw PDS label (`3556MR1025170721700585C00_DRXX.LBL`) yields an exact focus motor telemetry count `MSL:FOCUS_POSITION_COUNT = 2705`.
   * Evaluating the Malin Space Science Systems (MSSS) optical polynomial curves and CAHV camera intrinsics ($f = 100\text{ mm}, c = 7.4\,\mu\text{m}$, $\text{IFOV} = 0.074\text{ mrad/px}$) establishes a true slant range of **$R = 3.957\text{ m}$** (optical depth of field: $3.82\text{--}4.10\text{ m}$).
   * At this geometry (camera elevation $-22.0047^\circ$), the ground sampling scale is **$0.317\text{ mm/pixel}$**.
   * In-situ 3D central-perspective photogrammetry establishes an exposed length of $110.0\text{ px}$ and transverse diameter of $34.0\text{--}37.6\text{ px}$, constraining the true physical dimensions to:
     $$\text{Length } L = 35 \pm 2\text{ mm} \quad (\approx 1.38\text{ in})$$
     $$\text{Diameter } D = 11.5 \pm 0.8\text{ mm} \quad (\approx 0.45\text{ in})$$
     $$\text{Aspect Ratio } L/D = 3.24 : 1$$
   * The feature is the physical size of a standard ANSI AA battery—roughly one-sixth the size previously reported.

2. **The "Rover Debris" Hypothesis is Constrained by the Sedimentation Clock**:
   * The cylinder is not resting loosely on top of active aeolian dust; its lower third ($\approx 2.0\text{--}3.2\text{ mm}$ of vertical relief) is embedded within a cohesive, undisturbed duricrust soil matrix.
   * Crucially, high-resolution spatial gradients reveal **no windward deflation moats, scour trenches, or leeward sand shadow drifts**, indicating the surrounding surface has reached long-term aeolian equilibrium.
   * In Gale Crater, passive atmospheric dust deposition rates are well constrained by MSL and MER calibration targets at $10\text{--}25\,\mu\text{m}$ per Earth year.
   * Accumulating $2.0\text{ to } 3.2\text{ mm}$ of passive dust to bury the cylinder requires **$80\text{ to } 320\text{ Earth years}$**. *Curiosity* had operated on Mars for only 10.0 Earth years at Sol 3556, and Gale Crater has hosted no other landing mission in history.
   * Furthermore, *Curiosity*'s landing site (Bradbury Landing), where the descent stage crashed, is over $28\text{ km}$ along the rover drive path and $13\text{--}15\text{ km}$ in a direct straight line. In Mars's $6\text{ mbar}$ atmosphere, aeolian dynamic pressure cannot loft and transport a dense $35\text{ mm}$ solid cylinder across $13\text{ km}$ of rugged mountainous terrain.

3. **Statistically Anomalous Against Background Clasts ($N=20$)**:
   * We measured a control population of $N=20$ natural clasts across the identical raw frame (`3556MR1025170721700585C00_DRCL`).
   * The cylinder's generator straightness ($R^2 = 0.9985$, angular divergence $\Delta\theta < 0.2^\circ$) represents a **$+10.70\sigma$ (sample) / $+10.97\sigma$ (population)** outlier compared to natural clast morphology ($\mu_{R^2} = 0.104 \pm 0.081$).
   * Its aspect ratio ($3.24 : 1$) is a **$+12.06\sigma$ (sample) / $+12.56\sigma$ (population)** departure from natural rock fragmentation distributions ($\mu = 1.23 \pm 0.16$).

4. **Solar Ephemeris Ray-Tracing Match**:
   * Inverting the 2D sensor cast shadow vector yields an angle of $\theta_{\text{shadow}} = +23.3728^\circ$, matching NASA SPICE solar ephemeris for Sol 3556 12:10:25 LTST ($\theta_\odot = 69.8224^\circ, \phi_\odot = 186.8169^\circ$) to within $0.1^\circ$, independently confirming vertical relief ($h = 8.46 \pm 0.60\text{ mm}$).

---

### Verification & Reproduction

All code, data, and derivations are 100% open and deterministic:
* **Peer-Review Script**: Running `python reproduce_analysis.py` automatically validates all SHA-256 archive hashes, parses telemetry, ray-traces the SPICE shadow, and recomputes the $N=20$ control statistics (exits 0).
* **Interactive Tool**: A browser-based WebGL photogrammetry studio is hosted live at [https://cambrianminds.github.io/martian-cylinder/cylinder-tool/index.html](https://cambrianminds.github.io/martian-cylinder/cylinder-tool/index.html), allowing reviewers to dynamically inspect the 3D central-perspective fit against Curiosity's camera depression angle.

We hope these empirical measurements assist your continuing investigation of anomalous planetary features, and we welcome any critical feedback, correspondence, or replication efforts from you or the Galileo Project research team.

Respectfully submitted,

**Justin Bogner**  
Cambrian Minds · Technical Report CMR-2026-01  
Email: [justinbogner1618@gmail.com]  
Website: [https://cambrianminds.github.io/martian-cylinder/](https://cambrianminds.github.io/martian-cylinder/)
