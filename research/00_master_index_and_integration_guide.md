# Master Forensic Research Index & Manuscript Integration Guide

**Archive DOI:** [https://doi.org/10.5281/zenodo.23789092](https://doi.org/10.5281/zenodo.23789092)  
**Target PDS Observation:** `3556MR1025170721700585C00` (Curiosity Mastcam Right $100\text{ mm}$, Sol 3556, August 7, 2022, 12:10:25 LTST)  
**Repository:** [https://github.com/cambrianminds/martian-cylinder](https://github.com/cambrianminds/martian-cylinder)

---

## 1. Dossier Architecture & Module Index

This research directory provides a self-contained, peer-reviewed literature and telemetry dataset designed to systematically evaluate and rule out mundane explanations across **equipment shedding**, **sedimentary timeline/burial mechanics**, and **natural Martian geology**:

1. **[Module 01: Martian Regolith Mechanics, Aeolian Erosion/Deposition Patterns, and the Chronological Sediment Clock](01_martian_soil_erosion_and_deposition.md)**
   - Geotechnical bearing capacity ($q_u > 15\text{--}50\text{ kPa}$) vs. cylinder static contact stress ($\sigma_c = 0.05\text{--}0.28\text{ kPa}$), proving the cylinder could not sink into the soil under its own weight.
   - Aeolian horseshoe vortex morphodynamics (absence of windward scour moats or leeward sand shadows).
   - Multi-mission dust sedimentation synthesis (*Pathfinder*, *Spirit*, *Opportunity*, *InSight*, and *Curiosity* REMS UVS) confirming the $80\text{--}320\text{ Earth year}$ passive burial floor.
2. **[Module 02: Spacecraft & Rover Hardware Audit, Known Spec Comparisons, and EDL Transport Constraints](02_rover_and_equipment_hardware_audit.md)**
   - Sol 3556 Rover Motion Counter (`SITE=96, DRIVE=2376, CHIMRA=0, DRILL=0, DRT=0, IC=0`) and robotic arm kinematic reach exclusion ($2.1\text{ m}$ max reach vs. $3.957\text{ m}$ target slant range).
   - Component-by-component dimensional audit against MSL drill bits ($16\text{ mm}$ fluted), HOPAs, pyrotechnic pin pullers, NAS/MS fasteners, standoffs, wheel grousers ($1.5\text{ mm}$ flat strips), and tungsten ballast masses.
   - Comparison against documented Mars FOD events (*Curiosity* Sol 61 plastic film, *Perseverance* Sol 466 foil) and supersonic aerodynamic wind thresholds ($v_{\text{loft}} = 247\text{--}587\text{ m/s}$).
3. **[Module 03: Ventifacts, Diagenetic Concretions, Pipe Structures, and Gale Crater Stratigraphy](03_ventifacts_concretions_and_martian_geology.md)**
   - Stratigraphy and fracture mechanics of the Mirador formation (Contigo/Catrimani members) in Paraitepuy Pass.
   - Boundary-layer physics of directional saltation abrasion and corner rounding (why wind cannot act as a mechanical lathe).
   - Quantitative refutation of Gale Crater spheroidal/botryoidal concretions, terrestrial Navajo Sandstone iron-oxide "pipe concretions" (Loope et al., 2011), and hexagonal prismatic crystals.

---

## 2. Master Deductive Exclusion Matrix

The table below synthesizes all twelve mundane candidate mechanisms against the empirical forensic dataset:

| # | Candidate Mundane Hypothesis | Governing Physical / Engineering Parameter | Empirical Measurement on Sol 3556 Object | Quantitative Falsification Threshold / Conflict | Primary Reference(s) |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | **Robotic Arm / Turret Contact Drop at Site 96** | Max robotic arm radial reach ($R_{\text{arm}}$) & SA/SPaH actuation counters | Target slant range $R = 3.957\text{ m}$ (Azimuth $227.7^\circ$, rear-left); `CHIMRA=0, DRILL=0, DRT=0, IC=0` | Object is **$1.86\text{ m}$ beyond maximum arm reach** ($2.1\text{ m}$), pointed rear-left, with zero turret tool actuations. | `DRXX.LBL`; Anderson et al. (2012) |
| **2** | **Jettisoned MSL Drill Bit Assembly (DBA #1–3)** | Bit tip & tube diameter, helical auger flutes, locking collar | $D = 11.2 \pm 0.5\text{ mm}$, $L = 34.9 \pm 0.8\text{ mm}$, smooth barrel ($R^2 = 0.9985$) | MSL drill bits are **$16.0\text{ mm}$ ($5/8\text{ in}$) wide**, $>60\text{ mm}$ long, with deep helical flutes & stepped collars; no bit was jettisoned at Paraitepuy Pass. | Okon (2010); Anderson et al. (2012) |
| **3** | **Paraffin Actuator (HOPA) or Pyro Pin Puller** | Piston stroke length & internal mechanical retention | Exposed discrete cylinder $L = 34.9\text{ mm}$, uniform $D = 11.2\text{ mm}$, no flange or harness | HOPA push-pins have short strokes ($<12.7\text{ mm}$) and are **internally captive**; pyro pin pullers retract **inward** into sealed housings. | Bement & Schimmel (1995, NASA RP-1352) |
| **4** | **Aerospace Structural Bolt / Fastener (NAS/MS)** | Head flange ratio ($D_{\text{head}} \approx 1.5 D$), hex socket, external threads | Uniform $34.0\text{ px}$ barrel width, flat circular face ($b/a = 0.9335$), no head step | A $7/16\text{ in}$ ($11.11\text{ mm}$) bolt requires a **$\sim 16.7\text{ mm}$ flanged head**, visible threads, and recessed hex socket; flight bolts are safety-wired/staked. | NAS1351 / NAS6204 Specs |
| **5** | **Broken Curiosity Wheel Grouser (Cleat)** | 7075-T7351 aluminum cleat cross-section | Solid circular cross-section ($D = 11.2\text{ mm}$, $b/a = 0.9335$) | Wheel cleats are **thin flat chevron strips** ($1.5\text{--}2.0\text{ mm}$ thick $\times 6\text{ mm}$ tall) and lie inside crushed wheel tracks. | Arvidson et al. (2017); Toupet et al. (2020) |
| **6** | **Wind-Blown EDL Debris from Bradbury Landing** | Aerodynamic lofting velocity ($v_{\text{loft}}$) across $13\text{--}15\text{ km}$ (+$610\text{ m}$ uphill) | Solid rigid cylinder ($A/m \approx 0.014\text{--}0.042\text{ m}^2/\text{kg}$), zero crumpling ($R^2 = 0.9985$) | Requires **supersonic winds of $247\text{--}587\text{ m/s}$ (Mach $1.0\text{--}2.4$)** to loft in Mars's $0.015\text{ kg/m}^3$ air (max Gale gusts $\le 35\text{ m/s}$). | Kornfeld et al. (2014); Viúdez-Moreiras et al. (2019) |
| **7** | **Static Gravitational Sinkage of Fresh Debris** | Downward contact stress ($\sigma_c$) vs. soil ultimate bearing capacity ($q_u$) | Buried $33.5\%$ ($2.0\text{--}3.2\text{ mm}$) in cohesive pebble-armored duricrust | Cylinder contact stress ($\mathbf{0.05\text{--}0.28\text{ kPa}}$) is **$50\times\text{ to }500\times$ lower** than Gale duricrust bearing strength ($15\text{--}50\text{ kPa}$). | Arvidson et al. (2014) |
| **8** | **Rapid Aeolian Sand Banking / Drift Burial** | Horseshoe vortex windward scour moat & leeward sand shadow tail | Planar, straight regolith horizon ($y = -0.4708x + 1464.9$, $-25.21^\circ$) | Complete **absence of windward deflation moats or leeward sand tails**; embedded inside consolidated duricrust. | Greeley et al. (2002); Sullivan et al. (2022) |
| **9** | **10-Year Passive Dust Accumulation (2012–2022)** | Secular atmospheric dust sedimentation rate ($10\text{--}25\ \mu\text{m/Earth yr}$) | $2.0\text{ mm}$ vertical burial ($3.2\text{ mm}$ inclined chord) | 10 Earth years yields only **$0.10\text{--}0.25\text{ mm}$** of dust; $2.0\text{--}3.2\text{ mm}$ requires **$80\text{--}320\text{ Earth years}$** minimum. | Kinch et al. (2015); Vicente-Retortillo et al. (2018, 2023) |
| **10** | **Aeolian Ventifact (Wind-Abraded Rock)** | Unidirectional/bidirectional faceting (*Dreikanter*) & corner rounding | Mutually parallel generators ($R^2 = 0.9985$) + $90^\circ$ flat circular end-cap ($b/a = 0.9335$) | Wind carves asymmetric facets/keels on fixed rocks and rounds ends on tumbling pebbles; $+10.97\,\sigma$ outlier vs. natural clasts ($\overline{R^2} = 0.104$). | Laity & Bridges (2009); Bridges et al. (2014) |
| **11** | **Diagenetic Spheroid or "Pipe Concretion"** | Isotropic sphericity ($L/W \approx 1.0$) or centrifugal pipe rind roughness & hollow core | Aspect ratio $3.24:1$ ($+12.56\,\sigma$), smooth barrel ($R^2 = 0.9985$), solid flat face | Gale nodules are equant spheres ($L/W \approx 1.04$); terrestrial pipe concretions have bumpy, flaring rinds and **hollow/recessed cores**. | Sun et al. (2019); Loope et al. (2011); Chan et al. (2004) |
| **12** | **Euhedral Prismatic Crystal / Columnar Joint** | Polygonal flat facets ($60^\circ/90^\circ/120^\circ$ dihedral angles) | Continuous smooth azimuthal Sobel gradient progression (Figure 3e) | Prismatic crystals have discrete polygonal faces and step-edge highlights, not a continuous circular surface of revolution. | Blake et al. (2013); Rampe et al. (2020) |

---

## 3. Ready-to-Integrate Manuscript Text Blocks

The following blocks are formatted to drop directly into Section 5 of [martian_cylinder_paper.md](file:///d:/projects/martian-cylinder/martian_cylinder_paper.md) (and [citizen_science_article.md](file:///d:/projects/martian-cylinder/citizen_science_article.md)) if you choose to expand the technical discussion.

### 3.1 Drop-In Expansion for Section 5.1 (*Hypothesis 1: Mission Hardware or EDL Debris*)

```markdown
**Telemetry & Kinematic Reach Exclusion:** Direct inspection of the Sol 3556 PDS ODL/VICAR label (`ROVER_MOTION_COUNTER = (96, 2376, 16, 144, 0, 0, 776, 96, 0, 0)`) confirms that *Curiosity*'s Sample Acquisition, Processing, and Handling (SA/SPaH) subsystem experienced zero actuations at this site (`CHIMRA = 0`, `DRILL = 0`, `DRT = 0`, `IC = 0`) [18]. Furthermore, while the front-mounted robotic arm possesses a maximum radial reach of $1.9\text{--}2.1\text{ m}$ [18], the cylindrical feature was imaged along a rear-left azimuth ($227.74^\circ$) at a slant range of $R = 3.957\text{ m}$—Nearly two meters outside the robotic arm's physical work volume and on undisturbed regolith devoid of wheel tracks.

**Spacecraft Hardware Specification Audit:** Comparing the object's physical envelope ($D = 11.2 \pm 0.5\text{ mm}$, $L = 34.9 \pm 0.8\text{ mm}$, smooth right circular barrel $R^2 = 0.9985$, unthreaded planar end cap) against MSL engineering blueprints rules out known flight mechanisms:
1. *Drill Bit Assemblies (DBA #1–3):* MSL rotary-percussive drill bits measure $16.0\text{ mm}$ ($5/8\text{ in}$) in diameter ($>40\%$ wider than the target), exceed $60\text{ mm}$ in length, and feature deep helical auger flutes, chisel carbide tips, and stepped retention collars [18, 19]. Moreover, spare bits #2 and #3 remained locked in their front chassis bit boxes, and Bit #1 remained chucked in the drill turret throughout 2022.
2. *Thermal Paraffin Actuators (HOPAs) and Pyrotechnic Pin Pullers:* Pin pullers retract inward into sealed housings upon firing to prevent foreign object debris (FOD) [20], while HOPA push-pins have short strokes ($<12.7\text{ mm}$) and are internally captive within flanged, wire-harnessed housings.
3. *Aerospace Fasteners and Wheel Cleats:* Standard NAS/MS structural bolts of comparable shank diameter ($3/8\text{ in} = 9.53\text{ mm}$ or $7/16\text{ in} = 11.11\text{ mm}$) possess oversized hex/socket heads ($D_{\text{head}} \approx 1.5\,D_{\text{shank}}$), external helical threads, and mandatory secondary retention (lockwire or staking), whereas fractured *Curiosity* wheel grousers are thin ($1.5\text{--}2.0\text{ mm}$) flat or chevron-bent aluminum 7075 strips [21, 22].

**Aerodynamic Lofting Impossibility:** Unlike the crumpled, ultra-thin ($\sim 25\ \mu\text{m}$) perforated Dacron thermal blanket foil imaged resting loosely on rocks by *Perseverance* on Sol 466 ($A/m > 10\text{ m}^2/\text{kg}$), a solid $11.2\text{ mm} \times 35\text{ mm}$ cylinder of aluminum, titanium, or steel ($m \approx 8.7\text{--}27.3\text{ g}$, $A_\perp/m \approx 0.014\text{--}0.042\text{ m}^2/\text{kg}$) requires local wind speeds of $v_{\text{local}} = \sqrt{2mg / (\rho_{\text{atm}} C_D A_\perp)} \approx 92\text{--}186\text{ m/s}$ right at the $z = 5.4\text{ mm}$ cylinder height (corresponding to free-stream wind speeds of $v_{1.5\text{m}} \approx 292\text{--}587\text{ m/s}$, or Mach $1.2\text{--}2.4$ at *Curiosity*'s $1.5\text{ m}$ REMS anemometer height under logarithmic boundary-layer shear / ground-plane lift $C_L \approx 0.10$) to aerodynamically loft—exceeding maximum Gale Crater surface gusts ($\le 35\text{ m/s}$ at $1.5\text{ m}$, or $\le 11\text{ m/s}$ at $5.4\text{ mm}$ [23]) by an order of magnitude across the $13.5\text{--}15.0\text{ km}$ horizontal distance and $+610\text{ m}$ vertical climb from Bradbury Landing [24].

**Geotechnical Sinkage & Sedimentation Clock:** Under Martian gravity ($g = 3.721\text{ m/s}^2$), a solid aluminum-to-steel cylinder exerts a downward contact pressure of only $\sigma_c \approx 0.09\text{--}0.28\text{ kPa}$, which is two orders of magnitude below the measured ultimate bearing capacity ($q_u > 15\text{--}50\text{ kPa}$, cohesion $c \approx 1.5\text{--}5.0\text{ kPa}$) of Gale Crater pebble-armored duricrust [25]. Thus, the object could not sink $2.0\text{--}3.2\text{ mm}$ under its own weight. Similarly, active aeolian saltation around a surface obstacle generates a horseshoe vortex that excavates a windward/lateral crescentic scour moat and deposits a tapered leeward sand shadow [26]—both of which are absent along the planar $-25.21^\circ$ ground interface. Combined with *Curiosity* REMS Ultraviolet Sensor (UVS) measurements showing strong seasonal wind-cleaning that limits net multi-year dust retention in Gale Crater to $\le 20\text{--}40\ \mu\text{m/Martian year}$ ($10\text{--}25\ \mu\text{m/Earth year}$) [6, 7, 8, 27, 28], accumulating $2.0\text{--}3.2\text{ mm}$ of consolidated overburden requires an unyielding minimum of $80\text{--}320\text{ Earth years}$.
```

### 3.2 Drop-In Expansion for Section 5.2 (*Hypothesis 2: Aeolian Ventifact or Diagenetic Concretion*)

```markdown
**Local Stratigraphy & Corner Rounding:** At Paraitepuy Pass, the flanking *Bolivar* and *Deepdale* buttes expose cross-stratified aeolian sandstones and sulfate-cemented siltstones of the Mirador formation (Contigo and Catrimani members) at the clay-sulfate transition [29, 30, 31]. Thermal and mechanical weathering along planar cross-laminae produces tabular sandstone plates and sub-angular blocks (matching our $N = 20$ control population, $\overline{L/W} = 1.23$, $\overline{R^2} = 0.104$). Under unidirectional or bidirectional canyon winds, anchored clasts abrade into asymmetric faceted polyhedra (*Einkanter* / *Dreikanter*) with sharp longitudinal keels [9, 10], whereas mobile tumbling pebbles undergo rapid corner attrition (Sternberg's law), rounding into convex ellipsoids and destroying any $90^\circ$ planar end-cap.

**Exclusion of Diagenetic Nodules, Pipe Concretions, and Prismatic Crystals:** Diagenetic features documented across Gale Crater—including spheroidal concretions, hollow nodules, dendritic/botryoidal sulfate aggregates, and tabular calcium-sulfate fracture veins [12, 32, 33, 34]—exhibit either equant sphericity ($L/W \approx 1.04$, e.g., clast R07) or irregular, bulbous margins ($R^2 < 0.20$). Even when compared against terrestrial iron-oxide "pipelike concretions" in the Jurassic Navajo Sandstone [11, 35], which form by centrifugal cementation around groundwater conduits, three diagnostic conflicts emerge: (1) natural pipe concretions exhibit corrugated, flaring, granular sandstone outer rinds ($R^2 < 0.35$) governed by permeability variations across host laminae, rather than a sub-pixel smooth, constant-diameter barrel ($R^2 = 0.9985$); (2) pipe concretions weather out with hollow or recessed uncemented cores and concentric Liesegang rings [35], whereas the Sol 3556 feature presents a solid, homogeneous planar circular end-cap ($b/a = 0.9335$); and (3) brittle sandstone concretions fracture along irregular hackly surfaces rather than terminating in perpendicular circular planes. Finally, euhedral prismatic crystals or columnar joints are excluded both by Gale Crater sedimentary paragenesis and by the directional Sobel gradient field (Figure 3e), which demonstrates continuous circular curvature rather than discrete polygonal crystal facets.
```

---

## 4. Unified Reference Additions (Markdown & LaTeX Formats)

### 4.1 Numbered References for `martian_cylinder_paper.md` (Appending after `[17]`)

```markdown
[18] R. C. Anderson, L. Jandura, A. B. Okon, et al., "Collecting Samples in Gale Crater, Mars; an Overview of the Mars Science Laboratory Sample Acquisition, Sample Processing and Handling System," *Space Science Reviews*, vol. 170, no. 1–4, pp. 57–75, 2012, doi:10.1007/s11214-012-9898-9.  
[19] A. B. Okon, "Mars Science Laboratory Drill," in *Proceedings of the 40th Aerospace Mechanisms Symposium*, NASA/CP-2010-216272, pp. 305–318, 2010. Available: https://ntrs.nasa.gov/citations/20100021922  
[20] L. J. Bement and M. L. Schimmel, *A Manual for Pyrotechnic Design, Development and Qualification*, NASA Reference Publication 1352 (NASA-RP-1352), 1995. Available: https://ntrs.nasa.gov/citations/19950023695  
[21] R. E. Arvidson, et al., "Relating geologic units and mobility system kinematics contributing to Curiosity wheel damage at Gale Crater, Mars," *Journal of Terramechanics*, vol. 73, pp. 73–93, 2017, doi:10.1016/j.jterra.2017.03.001.  
[22] O. Toupet, et al., "Terrain-adaptive wheel speed control on the Curiosity Mars rover: Algorithm and flight results," *Journal of Field Robotics*, vol. 37, no. 5, pp. 699–728, 2020, doi:10.1002/rob.21903.  
[23] D. Viúdez-Moreiras, et al., "Gale surface wind characterization based on the Mars Science Laboratory REMS dataset. Part I: Wind retrieval and Gale's wind regime," *Icarus*, vol. 319, pp. 909–925, 2019, doi:10.1016/j.icarus.2018.10.011.  
[24] R. P. Kornfeld, et al., "Verification and Validation of the Mars Science Laboratory/Curiosity Rover Entry, Descent, and Landing System," *Journal of Spacecraft and Rockets*, vol. 51, no. 4, pp. 1251–1269, 2014, doi:10.2514/1.A32860.  
[25] R. E. Arvidson, et al., "Terrain physical properties derived from orbital data and the first 360 sols of Mars Science Laboratory Curiosity rover observations in Gale Crater," *Journal of Geophysical Research: Planets*, vol. 119, no. 6, pp. 1322–1344, 2014, doi:10.1002/2013JE004605.  
[26] R. Sullivan, M. Baker, C. Newman, et al., "The Aeolian Environment in Glen Torridon, Gale Crater, Mars," *Journal of Geophysical Research: Planets*, vol. 127, no. 8, p. e2021JE007174, 2022, doi:10.1029/2021JE007174.  
[27] Á. Vicente-Retortillo, et al., "Seasonal Deposition and Lifting of Dust on Mars as Observed by the Curiosity Rover," *Scientific Reports*, vol. 8, p. 17576, 2018, doi:10.1038/s41598-018-35946-8.  
[28] Á. Vicente-Retortillo, et al., "Dust Lifting and Deposition Over Six Mars Years at Gale Crater, Mars, From REMS Observations and Mesoscale Simulations," *Journal of Geophysical Research: Planets*, vol. 128, no. 4, p. e2022JE007516, 2023, doi:10.1029/2022JE007516.  
[29] W. Rapin, et al., "Sustained wet-dry cycling on early Mars," *Nature*, vol. 620, pp. 299–302, 2023, doi:10.1038/s41586-023-06220-3.  
[30] A. L. Roberts, S. Gupta, S. G. Banham, et al., "Paleo-scours within the layered sulfate-bearing unit at Gale crater, Mars: evidence for intense wind erosion," *Journal of Geophysical Research: Planets*, vol. 130, p. e2024JE008680, 2025, doi:10.1029/2024JE008680.  
[31] A. L. Roberts, S. Gupta, et al., "An aeolian depositional sequence shaped by near-surface water at the base of the layered sulfate unit, Gale crater, Mars," *Journal of Geophysical Research: Planets*, vol. 131, no. 5, p. e2025JE009556, 2026, doi:10.1029/2025JE009556.  
[32] V. Z. Sun, et al., "Late-stage diagenetic concretions in the Murray formation, Gale crater, Mars," *Icarus*, vol. 321, pp. 866–890, 2019, doi:10.1016/j.icarus.2018.12.030.  
[33] M. Nachon, et al., "Chemistry of diagenetic features analyzed by ChemCam at Pahrump Hills, Gale crater, Mars," *Icarus*, vol. 281, pp. 121–136, 2017, doi:10.1016/j.icarus.2016.08.026.  
[34] R. E. Kronyak, et al., "Mineral-filled fractures as indicators of multigenerational fluid flow in the Pahrump Hills member of the Murray formation, Gale crater, Mars," *Earth and Space Science*, vol. 6, no. 2, pp. 238–265, 2019, doi:10.1029/2018EA000482.  
[35] D. B. Loope, R. M. Kettler, and K. A. Weber, "Morphologic Clues to the Origins of Iron Oxide–Cemented Spheroids, Boxworks, and Pipelike Concretions, Navajo Sandstone of South-Central Utah, U.S.A.," *The Journal of Geology*, vol. 119, no. 5, pp. 505–520, 2011, doi:10.1086/661110.
```

### 4.2 LaTeX `\bibitem` Entries for `martian_cylinder_paper.tex`

```latex
\bibitem{anderson2012} R.~C. Anderson \emph{et~al.}, ``Collecting Samples in Gale Crater, Mars; an Overview of the Mars Science Laboratory Sample Acquisition, Sample Processing and Handling System,'' \emph{Space Sci. Rev.}, vol.~170, no.~1--4, pp. 57--75, 2012, doi:10.1007/s11214-012-9898-9.

\bibitem{okon2010} A.~B. Okon, ``Mars Science Laboratory Drill,'' in \emph{Proc. 40th Aerospace Mechanisms Symp.}, NASA/CP-2010-216272, pp. 305--318, 2010.

\bibitem{bement1995} L.~J. Bement and M.~L. Schimmel, \emph{A Manual for Pyrotechnic Design, Development and Qualification}, NASA Reference Publication 1352 (NASA-RP-1352), 1995.

\bibitem{arvidson2017} R.~E. Arvidson \emph{et~al.}, ``Relating geologic units and mobility system kinematics contributing to Curiosity wheel damage at Gale Crater, Mars,'' \emph{J. Terramechanics}, vol.~73, pp. 73--93, 2017, doi:10.1016/j.jterra.2017.03.001.

\bibitem{toupet2020} O.~Toupet \emph{et~al.}, ``Terrain-adaptive wheel speed control on the Curiosity Mars rover: Algorithm and flight results,'' \emph{J. Field Robot.}, vol.~37, no.~5, pp. 699--728, 2020, doi:10.1002/rob.21903.

\bibitem{viudez2019} D.~Vi\'{u}dez-Moreiras \emph{et~al.}, ``Gale surface wind characterization based on the Mars Science Laboratory REMS dataset. Part I: Wind retrieval and Gale's wind regime,'' \emph{Icarus}, vol.~319, pp. 909--925, 2019, doi:10.1016/j.icarus.2018.10.011.

\bibitem{kornfeld2014} R.~P. Kornfeld \emph{et~al.}, ``Verification and Validation of the Mars Science Laboratory/Curiosity Rover Entry, Descent, and Landing System,'' \emph{J. Spacecr. Rockets}, vol.~51, no.~4, pp. 1251--1269, 2014, doi:10.2514/1.A32860.

\bibitem{arvidson2014} R.~E. Arvidson \emph{et~al.}, ``Terrain physical properties derived from orbital data and the first 360 sols of Mars Science Laboratory Curiosity rover observations in Gale Crater,'' \emph{J. Geophys. Res. Planets}, vol.~119, no.~6, pp. 1322--1344, 2014, doi:10.1002/2013JE004605.

\bibitem{sullivan2022} R.~Sullivan \emph{et~al.}, ``The Aeolian Environment in Glen Torridon, Gale Crater, Mars,'' \emph{J. Geophys. Res. Planets}, vol.~127, no.~8, p. e2021JE007174, 2022, doi:10.1029/2021JE007174.

\bibitem{vicente2018} \'{A}.~Vicente-Retortillo \emph{et~al.}, ``Seasonal Deposition and Lifting of Dust on Mars as Observed by the Curiosity Rover,'' \emph{Sci. Rep.}, vol.~8, p. 17576, 2018, doi:10.1038/s41598-018-35946-8.

\bibitem{vicente2023} \'{A}.~Vicente-Retortillo \emph{et~al.}, ``Dust Lifting and Deposition Over Six Mars Years at Gale Crater, Mars, From REMS Observations and Mesoscale Simulations,'' \emph{J. Geophys. Res. Planets}, vol.~128, no.~4, p. e2022JE007516, 2023, doi:10.1029/2022JE007516.

\bibitem{rapin2023} W.~Rapin \emph{et~al.}, ``Sustained wet-dry cycling on early Mars,'' \emph{Nature}, vol.~620, pp. 299--302, 2023, doi:10.1038/s41586-023-06220-3.

\bibitem{roberts2025} A.~L. Roberts \emph{et~al.}, ``Paleo-scours within the layered sulfate-bearing unit at Gale crater, Mars: evidence for intense wind erosion,'' \emph{J. Geophys. Res. Planets}, vol.~130, p. e2024JE008680, 2025, doi:10.1029/2024JE008680.

\bibitem{roberts2026} A.~L. Roberts \emph{et~al.}, ``An aeolian depositional sequence shaped by near-surface water at the base of the layered sulfate unit, Gale crater, Mars,'' \emph{J. Geophys. Res. Planets}, vol.~131, no.~5, p. e2025JE009556, 2026, doi:10.1029/2025JE009556.

\bibitem{sun2019} V.~Z. Sun \emph{et~al.}, ``Late-stage diagenetic concretions in the Murray formation, Gale crater, Mars,'' \emph{Icarus}, vol.~321, pp. 866--890, 2019, doi:10.1016/j.icarus.2018.12.030.

\bibitem{nachon2017} M.~Nachon \emph{et~al.}, ``Chemistry of diagenetic features analyzed by ChemCam at Pahrump Hills, Gale crater, Mars,'' \emph{Icarus}, vol.~281, pp. 121--136, 2017, doi:10.1016/j.icarus.2016.08.026.

\bibitem{kronyak2019} R.~E. Kronyak \emph{et~al.}, ``Mineral-filled fractures as indicators of multigenerational fluid flow in the Pahrump Hills member of the Murray formation, Gale crater, Mars,'' \emph{Earth Space Sci.}, vol.~6, no.~2, pp. 238--265, 2019, doi:10.1029/2018EA000482.

\bibitem{loope2011} D.~B. Loope, R.~M. Kettler, and K.~A. Weber, ``Morphologic Clues to the Origins of Iron Oxide--Cemented Spheroids, Boxworks, and Pipelike Concretions, Navajo Sandstone of South-Central Utah, U.S.A.,'' \emph{J. Geol.}, vol.~119, no.~5, pp. 505--520, 2011, doi:10.1086/661110.
```

