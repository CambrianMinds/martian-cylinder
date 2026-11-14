# Module 03: Ventifacts, Diagenetic Concretions, Pipe Structures, and Gale Crater Stratigraphy

**Archive Reference:** Sol 3556 Forensic Research Dossier · Companion Dataset to [https://doi.org/10.5281/zenodo.23789092](https://doi.org/10.5281/zenodo.23789092)  
**Target PDS Product:** `3556MR1025170721700585C00` (Sol 3556, August 7, 2022, 12:10:25 LTST)  
**Geological Setting:** Paraitepuy Pass (Flanked by *Bolivar* and *Deepdale* Buttes), Mirador Formation (Contigo / Catrimani Members), Clay-Sulfate Transition Zone, Mount Sharp (*Aeolis Mons*), Gale Crater, Mars.

---

## 1. Stratigraphic and Lithological Context of Paraitepuy Pass

On Sol 3556, *Curiosity* was positioned inside **Paraitepuy Pass**, a narrow valley cut between steep erosional buttes (*Bolivar* to the west/southwest and *Deepdale* to the east/northeast) that marks the stratigraphic boundary between the underlying clay-rich *Carolyn Shoemaker* / *Murray* formations and the overlying **Layered Sulfate Unit (LSu)**, informally designated the **Mirador formation** (Rapin et al., 2023; Roberts et al., 2025, 2026).

### 1.1 Local Bedrock Lithology & Weathering Style
The Mastcam Right sequence (`mcam02517`, *"Stereo documentation of bedding styles exposed in Bolivar cliff face"*) targeted the basal members of the Mirador formation (specifically the **Contigo** and **Catrimani** members):
- **Primary Lithology:** Fine-to-medium grained, cross-stratified aeolian sandstones (ancient wind-ripple laminae and dune foresets) interbedded with sulfate-cemented siltstones and episodic interdune/pond lenses (Roberts et al., 2025, 2026).
- **Mechanical Breakdown & Clast Production:** When exposed to diurnal thermal fatigue ($\Delta T \approx 70\text{--}90\text{ K/sol}$) and aeolian undermining, the cross-bedded Mirador and Stimson sandstones fracture preferentially along **planar bedding laminae** ($2\text{--}15\text{ mm}$ thick) and steep **orthogonal tectonic/contractional joints**.
- **Resulting Detrital Clast Population:** This fracture mechanics regime produces **tabular, platy sandstone slabs** (e.g., control clasts R01, R05, R10, R13 in Table 1) and **sub-angular to sub-rounded equant pebbles** (e.g., R03, R04, R06, R11, R15). Across our empirical control sample ($N = 20$) extracted directly from the Sol 3556 detector frame:
  - **Mean Circularity ($b/a$):** $0.829 \pm 0.100$ (population SD; $\pm 0.102$ sample SD)
  - **Mean Aspect Ratio ($L/W$):** $1.23 \pm 0.16$ (range $1.02\text{--}1.72$)
  - **Mean Lateral Flank Linearity ($R^2$):** $0.104 \pm 0.081$ (maximum $0.2708$ on clast R02)

---

## 2. Aeolian Ventifact Mechanics: Why Wind Abrasion Cannot Act as a Lathe

A common qualitative dismissal of unusual Martian rocks is to invoke **ventifaction**—abrasion by wind-driven saltating sand grains over millions of years (Bridges et al., 2014; Laity & Bridges, 2009). However, the physical fluid dynamics and boundary mechanics of saltation abrasion strictly forbid the generation of a right circular cylinder ($R^2 = 0.9985$, $b/a = 0.9335$, $L/D = 3.24$).

### 2.1 The Physics of Saltation Impact Abrasion
In the Martian boundary layer, basaltic sand grains ($d \approx 100\text{--}300\ \mu\text{m}$) travel along ballistic saltation trajectories concentrated within the lowest $1\text{--}20\text{ cm}$ above the ground (Greeley et al., 2002; Sullivan et al., 2022). Abrasion susceptibility ($S_a$) depends strongly on the local **impact angle ($\alpha_{\text{imp}}$)** between the incoming particle velocity vector $\mathbf{v}_p$ and the target rock surface normal $\mathbf{\hat{n}}$ (Laity & Bridges, 2009):
- **Brittle Silicate/Sulfate Rocks:** Maximum micro-fracturing and mass removal occur at high impact angles ($\alpha_{\text{imp}} \approx 60^\circ\text{--}90^\circ$, i.e., surfaces facing directly into the wind), whereas grazing impacts ($\alpha_{\text{imp}} < 15^\circ$) cause polishing or shallow fluting.

### 2.2 Geometric Consequences under Fixed vs. Mobile Regimes

| Abrasion Regime | Physical Mechanism | Resulting 3D Geometry | Conflict with Sol 3556 Cylinder ($R^2 = 0.9985$, $b/a = 0.9335$) |
| :--- | :--- | :--- | :--- |
| **1. Anchored / Partially Buried Clast**<br>*(Unidirectional Wind)* | Windward face experiences high-angle impact erosion, flattening into a sloped planar facet (*Einkanter*) while leeward and buried surfaces remain rough and un-abraded. | **Asymmetric pyramidal or wedge-shaped stone** with a sharp upper keel, basal undercutting, and flat windward facet. | Fails completely: produces polygonal/triangular cross-sections, tapering edges, and zero rotational symmetry around a longitudinal axis. |
| **2. Anchored Clast**<br>*(Bi- or Multi-Directional Seasonal Winds)* | Alternating upslope/downslope canyon winds plane two or three intersecting flat facets separated by sharp ridges (*Zweikanter* or *Dreikanter*). | **Faceted polyhedron** with sharp longitudinal ridge keels and concave flutes/grooves. | Fails completely: produces sharp dihedral keels rather than a continuous smooth circular barrel (directional Sobel field, Figure 3e) and never forms a flat $90^\circ$ circular end-cap. |
| **3. Mobile / Tumbling Pebble**<br>*(Periodic Creep & Rolling)* | High-curvature corners and protruding ends experience the highest impact stress and chip away fastest (**Sternberg's Law of Corner Rounding**). | **Sub-spherical pebble or prolate ellipsoid** with convex, rounded/tapered poles (like a rugby ball or river cobble). | Fails completely: corner rounding rapidly **destroys** any sharp $90^\circ$ circular rim and rounds the ends into convex domes, whereas the Sol 3556 cylinder preserves a razor-sharp perpendicular planar end-cap ($S_x < -20\text{ DN}$). |

**Key Deduction:** To machine a rock into a right circular cylinder with $R^2 = 0.9985$ mutually parallel straight generators and a perpendicular flat circular face ($b/a = 0.9335$), the rock would have to rotate continuously at constant angular velocity around a fixed longitudinal spindle axis while an abrasive jet cuts strictly parallel to that axis, followed by a perpendicular cross-cut saw plane. **No aeolian boundary layer on Earth or Mars acts as a mechanical lathe.**

### 2.3 Empirical Benchmark from NASA's Gale Crater Ventifact Field (Sols 3415–3418, Greenheugh Pediment)
Just ~140 sols prior to Sol 3556, *Curiosity* traversed the sandstone capping unit of the nearby **Greenheugh pediment**, entering one of the densest fields of wind-carved ventifacts encountered during the mission. In NASA's official mission report (*"Sols 3417–3418: A View Filled With Ventifacts"*, March 16, 2022), JPL Planetary Geologist Dr. Abigail Fraeman documented the diagnostic morphology of authentic Gale Crater ventifacts (including the APXS/MAHLI target *"Knott"* and ChemCam targets *"Old Nab"* and *"Little Mell"*):
> *"From here we can see hundreds of ventifacts — a term that describes rocks which have been abraded by wind-blown sand into distinctive, flattened facets with crisp edges."* (Fraeman, 2022)

As directly captured in *Curiosity*'s Sol 3415 Left Navigation Camera frame (`NLB_700661467EDR_F0933078NCAM00299M_.jpg`, archived in `data/NLB_700661467EDR_F0933078NCAM00299M_.jpg`), every wind-abraded rock across the pediment exhibits **flat, slanted planar facets meeting at sharp, angular pyramidal keels (*Dreikanter*)** and fluted grooves—the exact physical antithesis of an axisymmetric, constant-diameter right circular cylinder ($R^2 = 0.9985$) with a perpendicular circular end-cap ($b/a = 0.9335$).

---

## 3. Diagenetic Concretions, Nodules, Veins, and "Pipe Concretions"

Because Gale Crater hosts a rich record of post-depositional groundwater alteration (diagenesis), we rigorously evaluate every class of diagenetic mineral structure documented on Mars and in terrestrial desert analogs.

### 3.1 Catalog of Gale Crater & Meridiani Planum Diagenetic Morphologies
Extensive surveys by *Curiosity*'s Mastcam, MAHLI, and ChemCam instruments (Grotzinger et al., 2014; Nachon et al., 2014, 2017; Sun et al., 2019; Kronyak et al., 2019; Rapin et al., 2023) as well as *Opportunity*'s Microscopic Imager in Meridiani Planum (NASA Photojournal **PIA19113**, *"Martian Concretions Near Fram Crater"*, Sol 84, archived in `data/PIA19113_concretions.jpg`) classify Martian diagenetic features into four morphological categories:

1. **Spheroidal & Sub-Spherical Nodules ("Blueberries" & Mudstone/Sandstone Concretions):**
   - *Mechanism:* Isotropic Fickian diffusion of dissolved $\text{Fe}^{2+}$, $\text{Mg}^{2+}$, $\text{Ca}^{2+}$, and $\text{SO}_4^{2-}$ around point nucleation sites in homogeneous pore spaces.
   - *Geometry:* Equant spheres or oblate spheroids ($D \approx 1\text{--}15\text{ mm}$, aspect ratio $L/W \approx 1.01\text{--}1.15$), exemplified by NASA benchmark image **PIA19113** (`data/PIA19113_concretions.jpg`) and represented in our Sol 3556 control sample by clast **R07** ($11.9 \times 11.5\text{ mm}$, $b/a = 0.9602$, $L/W = 1.04$, flank linearity $R^2 = 0.0595$).
   - *Exclusion:* Spherical concretions have an aspect ratio of $\sim 1.0$, differing from the cylinder's $3.24:1$ aspect ratio by **$+12.06\,\sigma$ to $+12.56\,\sigma$**. Even when fractured (as seen in the upper-right spherule of PIA19113), Martian concretions exhibit granular internal textures and spherical outer walls rather than elongated parallel cylindrical barrels.
2. **Hollow Nodules & Raised Ridges (Yellowknife Bay / Sheepbed Member):**
   - *Geometry:* Sub-spherical millimeter-scale spheres that weathered open to expose hollow interiors or irregular raised rims (Grotzinger et al., 2014).
   - *Exclusion:* Equant $1\text{--}5\text{ mm}$ pitted spheres; zero resemblance to a $35\text{ mm}$ solid cylinder.
3. **Dendritic, Botryoidal, and Coalesced Nodular Aggregates (Pahrump Hills / Glen Torridon / Mirador):**
   - *Geometry:* Branching, grape-like (*botryoidal*), or knobby clusters formed where multiple spherical concretions grow together along bedding planes (Nachon et al., 2017; Sun et al., 2019).
   - *Exclusion:* Highly undulatory, bulbous margins with deep re-entrant necks ($R^2 < 0.15$).
4. **Mineral-Filled Fracture Veins & Boxwork (Anhydrite / Bassanite / Gypsum):**
   - *Geometry:* Planar, tabular sheets ($1\text{--}10\text{ mm}$ thick) precipitated inside brittle tensile cracks (Kronyak et al., 2019). When eroded out of host rock, they form jagged, flat plates or intersecting boxwork fins.
   - *Exclusion:* Tabular flat plates, not circular cylinders.

### 3.2 Deep-Dive Evaluation of Terrestrial "Pipe Concretions" (Navajo Sandstone Analog)
The closest known geological analog to a cylindrical rock in nature is the **iron-oxide pipelike concretion ("pipe concretion")**, famously documented in the Jurassic Navajo Sandstone of southern Utah by Chan et al. (2004) and Loope, Kettler, & Weber (2011).

In the Navajo Sandstone, oxygenated groundwater flowing along sub-horizontal permeability pathways away from vertical joints precipitated goethite and hematite cement in centrifugal reaction fronts, producing elongated sub-cylindrical pipes ranging from $<1\text{ cm}$ to $>50\text{ cm}$ in diameter (Loope et al., 2011).

**Why the Sol 3556 Cylinder Is Not a Diagenetic Pipe Concretion:**

| Forensic Diagnostic Criterion | Terrestrial / Martian Diagenetic Pipe Concretion<br>*(Loope et al., 2011; Chan et al., 2004)* | Sol 3556 Cylindrical Anomaly<br>*(`3556MR1025170721700585C00`)* |
| :--- | :--- | :--- |
| **1. Longitudinal Generator Linearity ($R^2$)** | **Bulbous, Corrugated, & Tapering ($R^2 \approx 0.10\text{--}0.35$):** Because pore permeability varies across individual wind-ripple laminae, centrifugal cementation expands faster in coarse laminae and pinches in fine laminae, creating a ribbed, nodular, flaring outer rind. | **Sub-Pixel Machine-Grade Parallelism ($R^2 = 0.9985$, $\Delta\theta < 0.7^\circ$):** Zero periodic bulging across $35\text{ mm}$ of length; maintains constant $34.0\text{ px}$ diameter from front face to rear cap. |
| **2. Internal Cross-Section & Core Structure** | **Hollow Tube or Recessed Soft Core:** Pipe concretions form by centrifugal precipitation of an outer iron-oxide rind ($1\text{--}10\text{ mm}$ thick) enclosing an uncemented or weakly cemented sandstone core. Upon erosion, the soft core weather out, leaving a **hollow pipe** or concentric Liesegang rings. | **Solid, Homogeneous Planar Face ($b/a = 0.9335$):** The horizontal Sobel gradient ($S_x$) and raw intensity profile across the $37.6 \times 35.1\text{ px}$ end face show a continuous, solid, flat surface with zero central hole, zero annular wall rim, and zero concentric rings. |
| **3. Terminal Fracture Morphology** | **Irregular / Hackly / Conchoidal Break:** When a brittle sandstone concretion snaps transversely, fracture propagation follows grain boundaries, producing an uneven, stepped, or oblique rough surface. | **Razor-Sharp $90^\circ$ Planar End Cap:** Terminates perpendicular to the longitudinal axis at both the front circular face and the rear regolith boundary (Figure 4). |
| **4. Surface Micro-Texture & Albedo** | **Granular Host-Sandstone Texture:** Because concretions cement pre-existing sand grains ($\sim 100\text{--}500\ \mu\text{m}$), their exterior has the rough, dark, low-albedo texture of iron-oxide-coated sandstone. | **Smooth Specular/Diffuse Highlight Ridge:** Exhibits a continuous, uninterrupted longitudinal brightness crest along the upper barrel generator (`DRCL` intensity $I \approx 175\text{ DN}$). |

---

## 4. Exclusion of Prismatic Mineral Crystals & Columnar Jointing

Could the object be a single euhedral mineral crystal (such as a hexagonal quartz, apatite, tourmaline, or gypsum/selenite prism) or a miniature basaltic column?

1. **Geochemical & Paragenetic Impossibility in Gale Crater:**
   - Free-standing $3.5\text{ cm} \times 1.1\text{ cm}$ euhedral single crystals require large, open hydrothermal vugs or pegmatitic cavities. Seven years of X-ray diffraction by *Curiosity*'s CheMin instrument across Gale Crater mudstones and sandstones show that sulfate and silicate phases occur exclusively as micro-crystalline cements, fine detrital grains ($< 0.5\text{ mm}$), or fibrous millimeter-thin fracture veins (Blake et al., 2013; Rampe et al., 2020).
2. **Continuous Curvature vs. Polygonal Crystal Faces (Figure 3e):**
   - Euhedral prismatic crystals and columnar basalt joints are **polygons** (typically 4-, 6-, or 8-sided prisms bounded by flat planar crystal faces meeting at discrete interfacial angles of $60^\circ$, $90^\circ$, or $120^\circ$).
   - Under directional illumination ($\theta_\odot = 69.82^\circ$), a hexagonal or octagonal prism displays **step-function brightness jumps** across discrete flat facets and sharp longitudinal corner edges, and its cross-section is a polygon rather than a circle.
   - In contrast, the directional Sobel gradient field of the Sol 3556 feature (Figure 3e) and its transverse intensity profile demonstrate **smooth, continuous azimuthal curvature** characteristic of a true circular surface of revolution ($b/a = 0.9335$, radial RMSE $\sigma_r = 503\ \mu\text{m}$).

---

## 5. Verified Citations for Module 03

1. **Bridges, N. T., Calef, F. J., Hallet, B., et al. (2014).** "The rock abrasion record at Gale Crater: Mars Science Laboratory results from Bradbury Landing to Rocknest." *Journal of Geophysical Research: Planets*, 119(6), 1374–1389. DOI: [10.1002/2013JE004579](https://doi.org/10.1002/2013JE004579)
2. **Laity, J. E., & Bridges, N. T. (2009).** "Ventifacts on Earth and Mars: Analytical, field, and laboratory studies supporting sand abrasion and windward feature development." *Geomorphology*, 105(3–4), 202–217. DOI: [10.1016/j.geomorph.2008.09.014](https://doi.org/10.1016/j.geomorph.2008.09.014)
3. **Chan, M. A., Beitler, B., Parry, W. T., Ormö, J., & Komatsu, G. (2004).** "A possible terrestrial analogue for haematite concretions on Mars." *Nature*, 429(6993), 731–734. DOI: [10.1038/nature02600](https://doi.org/10.1038/nature02600)
4. **Loope, D. B., Kettler, R. M., & Weber, K. A. (2011).** "Morphologic Clues to the Origins of Iron Oxide–Cemented Spheroids, Boxworks, and Pipelike Concretions, Navajo Sandstone of South-Central Utah, U.S.A." *The Journal of Geology*, 119(5), 505–520. DOI: [10.1086/661110](https://doi.org/10.1086/661110)
5. **Sun, V. Z., Stack, K. M., Kah, L. C., et al. (2019).** "Late-stage diagenetic concretions in the Murray formation, Gale crater, Mars." *Icarus*, 321, 866–890. DOI: [10.1016/j.icarus.2018.12.030](https://doi.org/10.1016/j.icarus.2018.12.030)
6. **Nachon, M., Mangold, N., Forni, O., et al. (2017).** "Chemistry of diagenetic features analyzed by ChemCam at Pahrump Hills, Gale crater, Mars." *Icarus*, 281, 121–136. DOI: [10.1016/j.icarus.2016.08.026](https://doi.org/10.1016/j.icarus.2016.08.026)
7. **Kronyak, R. E., Kah, L. C., Edgett, K. S., et al. (2019).** "Mineral-filled fractures as indicators of multigenerational fluid flow in the Pahrump Hills member of the Murray formation, Gale crater, Mars." *Earth and Space Science*, 6(2), 238–265. DOI: [10.1029/2018EA000482](https://doi.org/10.1029/2018EA000482)
8. **Rapin, W., Dromart, G., Clark, B. C., et al. (2023).** "Sustained wet-dry cycling on early Mars." *Nature*, 620, 299–302. DOI: [10.1038/s41586-023-06220-3](https://doi.org/10.1038/s41586-023-06220-3)
9. **Roberts, A. L., Gupta, S., Banham, S. G., et al. (2025).** "Paleo-scours within the layered sulfate-bearing unit at Gale crater, Mars: evidence for intense wind erosion." *Journal of Geophysical Research: Planets*, 130, e2024JE008680. DOI: [10.1029/2024JE008680](https://doi.org/10.1029/2024JE008680)
10. **Roberts, A. L., Gupta, S., et al. (2026).** "An aeolian depositional sequence shaped by near-surface water at the base of the layered sulfate unit, Gale crater, Mars." *Journal of Geophysical Research: Planets*, 131(5), e2025JE009556. DOI: [10.1029/2025JE009556](https://doi.org/10.1029/2025JE009556)
11. **Grotzinger, J. P., Sumner, D. Y., Kah, L. C., et al. (2014).** "A Habitable Fluvio-Lacustrine Environment at Yellowknife Bay, Gale Crater, Mars." *Science*, 343(6169), 1242777. DOI: [10.1126/science.1242777](https://doi.org/10.1126/science.1242777)
12. **Fraeman, A. A. (2022).** "Sols 3417–3418: A View Filled With Ventifacts." *NASA Mars Exploration Program / Curiosity Rover Mission Updates* (March 16, 2022), featuring Sol 3415 Left Navcam image `NLB_700661467EDR_F0933078NCAM00299M_`. URL: [https://science.nasa.gov/blog/sols-3417-3418-a-view-filled-with-ventifacts/](https://science.nasa.gov/blog/sols-3417-3418-a-view-filled-with-ventifacts/)
13. **NASA / JPL-Caltech / Cornell / USGS (2004).** "Martian Concretions Near Fram Crater (PIA19113)." *NASA Planetary Photojournal*, MER *Opportunity* Microscopic Imager & Pancam composite, Sol 84 (April 19, 2004). URL: [https://science.nasa.gov/photojournal/martian-concretions-near-fram-crater/](https://science.nasa.gov/photojournal/martian-concretions-near-fram-crater/)

