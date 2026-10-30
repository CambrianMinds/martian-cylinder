# Module 02: Spacecraft & Rover Hardware Audit, Known Spec Comparisons, and EDL Transport Constraints

**Archive Reference:** Sol 3556 Forensic Research Dossier · Companion Dataset to [https://doi.org/10.5281/zenodo.23789092](https://doi.org/10.5281/zenodo.23789092)  
**Target PDS Product:** `3556MR1025170721700585C00` (Sol 3556, August 7, 2022, 12:10:25 LTST)  
**Target Physical Envelope:**

- **Transverse Diameter ($D_\perp$):** $9.96\text{--}11.02\text{ mm}$ nominal ($9.13\text{--}11.97\text{ mm}$ full DoF envelope)
- **Axial / Ground-Projected Diameter ($D_{\text{axial}}$):** $10.78\text{--}11.93\text{ mm}$ nominal ($11.2 \pm 0.5\text{ mm}$ dual-scale bracket)
- **Exposed Longitudinal Length ($L$):** $34.9 \pm 0.8\text{ mm}$ ($35 \pm 2\text{ mm}$ physical bound; $32.0\text{--}37.9\text{ mm}$ full DoF envelope)
- **Aspect Ratio ($L/D$):** $3.24 : 1$
- **Geometric Regularity:** Right circular cylinder with smooth opposing linear generators ($R^2 = 0.9985$, $\Delta\theta < 0.7^\circ$) and a flat, unthreaded, unflanged planar circular end cap ($b/a = 0.9335$, matching the $22^\circ\text{--}24^\circ$ 3D viewing foreshortening angle).

---

## 1. Sol 3556 Rover Telemetry & Kinematic Reach Exclusion

Before comparing component blueprints, the raw PDS ODL/VICAR label (`3556MR1025170721700585C00_DRXX.LBL` / `DRXX-metadata.txt`) provides direct mechanical telemetry on the state and position of *Curiosity*'s subsystems at the exact moment of image acquisition:

### 1.1 Rover Motion Counter (RMC) Audit

Lines 49–57 and 118–125 of `DRXX-metadata.txt` record the 10-element `ROVER_MOTION_COUNTER`:

| RMC Index Name | Sol 3556 Value | Subsystem Meaning & Operational State at Site 96 / Drive 2376 |
| :--- | :---: | :--- |
| **`SITE`** | `96` | Major localization frame index (Paraitepuy Pass approach). |
| **`DRIVE`** | `2376` | Mobility drive step index within Site 96. |
| **`POSE`** | `16` | Rover chassis attitude/localization solution index. |
| **`ARM`** | `144` | Robotic arm articulation counter (stowed/Static configuration at `ORIGIN_OFFSET_VECTOR = (1.238 m, -0.477 m, -0.244 m)` in `ROVER_NAV_FRAME`). |
| **`CHIMRA`** | **`0`** | Collection and Handling for In-Situ Martian Rock Analysis: **Zero actuations** at this site/drive. |
| **`DRILL`** | **`0`** | Rotary-Percussive Drill mechanism: **Zero actuations** at this site/drive. |
| **`RSM`** | `776` | Remote Sensing Mast pointing index (Azimuth $227.7412^\circ$, Elevation $-22.0047^\circ$). |
| **`HGA`** | `96` | High-Gain Antenna gimbal pointing index. |
| **`DRT`** | **`0`** | Dust Removal Tool (wire-bristle rotary brush): **Zero actuations** at this site/drive. |
| **`IC`** | **`0`** | Sample Inlet Cover mechanism: **Zero actuations** at this site/drive. |

### 1.2 Kinematic Reach & Traverse Path Exclusion

1. **Outside Robotic Arm Work Volume:** *Curiosity*'s 5-degree-of-freedom Instrument Deployment Device (Robotic Arm) is mounted on the front-left chassis (`X = +1.238 m, Y = -0.477 m` in `ROVER_NAV_FRAME`) and has a maximum radial reach of **$1.9\text{ to }2.1\text{ meters}$** from the front hazard panel (Anderson et al., 2012; Robinson et al., 2012).
2. **Rear-Left Pointing Vector:** In contrast, Mastcam Right (`MAST_RIGHT`) is mounted on the Remote Sensing Mast (`X = +0.684 m, Y = +0.648 m, Z = -1.927 m`) and was pointed at `FIXED_INSTRUMENT_AZIMUTH = 227.7412°` (looking backward and to the left/southwest of the rover at a slant range of **$R = 3.957\text{ m}$**, ground horizontal range $\sim 3.67\text{ m}$).
3. **Zero Contact Activity:** The RMC counters (`CHIMRA=0`, `DRILL=0`, `DRT=0`, `IC=0`) confirm that no drilling, brushing, scooping, or sample transfer occurred at this stop. Furthermore, the cylinder is situated on undisturbed, sloping, rock-strewn regolith outside the rover's wheel tracks (no cleat imprints exist in the `DRCX` frame).

---

## 2. Component-by-Component Specification Audit vs. Target Dimensions

To test whether the Sol 3556 cylinder matches any known *Curiosity* (MSL) hardware specification, we audit every cylindrical or tubular element on the spacecraft:

| Candidate Hardware Component | Actual Engineering Specifications & Dimensions | Morphological & Operational Features | Match to Sol 3556 Object ($D \approx 11.2\text{ mm}, L \approx 35\text{ mm}$)? |
| :--- | :--- | :--- | :--- |
| **1. Drill Bit Assembly (DBA #1, #2, #3)**<br>*(Okon, 2010; Anderson et al., 2012)* | **Bit Tip Diameter:** $15.9\text{--}16.0\text{ mm}$ ($5/8\text{ in}$)<br>**Collection Tube OD:** $\sim 16\text{ mm}$<br>**Overall Assembly Length:** $> 120\text{ mm}$ (drilling depth up to $50\text{--}65\text{ mm}$) | Features a chisel-shaped tungsten-carbide cutting tip, deep external helical auger flutes, a concentric sample collection tube, and a wide stepped hex/bayonet locking collar. | **RULED OUT.**<br>1) Diameter is $43\%$ too large ($16\text{ mm}$ vs. $11.2\text{ mm}$).<br>2) Has helical flutes and stepped collars, violating $R^2 = 0.9985$ smooth barrel.<br>3) Spare bits #2 and #3 remain locked in the bit boxes on the front chassis; Bit #1 remained in the drill chuck throughout 2022. |
| **2. Drill Contact Sensor / Stabilizer Prongs**<br>*(Okon, 2010)* | **Two lateral contact tines** flanking the drill bit, $L > 80\text{ mm}$, integrated with spring-loaded potentiometers and broad footpads. | Non-detachable structural assemblies bolted to the drill front housing. | **RULED OUT.**<br>Wrong geometry, size, and fully accounted for on the turret in subsequent MAHLI/Navcam selfies. |
| **3. High-Output Paraffin Actuators (HOPAs)**<br>*(Starsys / Sierra Nevada Corp. IHOP-15 / HP-25 / HP-50)* | **Body Diameter:** $9.5\text{--}19.0\text{ mm}$<br>**Pin Stroke:** $3.2\text{--}12.7\text{ mm}$<br>**Housing:** Flanged cylindrical body with electrical heater leads and mounting threads. | Thermal wax actuators used for one-time cover releases and launch locks. The push-pin is **internally captive** (retained by an internal piston stop) and cannot eject from the housing. | **RULED OUT.**<br>Actuator pins are mechanically captive with short strokes ($<13\text{ mm}$), while full actuator housings have mounting flanges, threaded collars, and wire harnesses. |
| **4. Pyrotechnic Pin Pullers (NASA Standard / TiNi)**<br>*(Bement & Schimmel, 1995, NASA RP-1352)* | **Pin Diameter:** $3.18\text{ mm}$ ($1/8\text{ in}$), $6.35\text{ mm}$ ($1/4\text{ in}$), or $9.53\text{ mm}$ ($3/8\text{ in}$)<br>**Housing:** Rectangular or flanged block with dual NSI (NASA Standard Initiator) hex ports. | Pin pullers **retract** a pin inward into a sealed housing upon firing to release a clevis load; they are specifically designed to prevent any ejecta or FOD release. | **RULED OUT.**<br>Pin pullers retract inward and remain permanently captured inside the actuator body bolted to the spacecraft structure. |
| **5. Aerospace Structural Fasteners (Bolts / Screws)**<br>*(NAS1351, NAS1352, NAS6204–6207, MS21250)* | **Standard Shank Diameters:**<br>#8 ($4.17\text{ mm}$), #10 ($4.83\text{ mm}$), $1/4\text{ in}$ ($6.35\text{ mm}$), $5/16\text{ in}$ ($7.94\text{ mm}$), $3/8\text{ in}$ ($9.53\text{ mm}$), $7/16\text{ in}$ ($11.11\text{ mm}$). | Every aerospace structural bolt features a wider **socket/hex head or flange** ($D_{\text{head}} \approx 1.5\times D_{\text{shank}}$), external helical threads, and JPL-mandated secondary retention (lockwire, staked epoxy, or captive nut). | **RULED OUT.**<br>A $7/16\text{ in}$ ($11.11\text{ mm}$) bolt would have a $\sim 16.7\text{ mm}$ head, visible thread pitch steps, and a recessed hex socket on the end face, contradicting the uniform $34\text{ px}$ barrel and flat end cap. |
| **6. Cylindrical Standoffs, Spacers, or Precision Dowel Pins**<br>*(NAS / MS Hardware)* | Unthreaded sleeves or solid dowel pins can be manufactured at $D = 3/8\text{ in}$ ($9.53\text{ mm}$) or $7/16\text{ in}$ ($11.11\text{ mm}$), $L = 1.375\text{ in}$ ($34.9\text{ mm}$). | Standoffs are hollow (through-bolted) and captured by a central screw; dowel pins are press-fit into blind or captured mating bores inside structural joints. | **CHRONOLOGICALLY & MECHANICALLY EXCLUDED.**<br>A spacer cannot detach unless its retaining bolt also shears/unthreads, and any hardware dropped by *Curiosity* in 2022 could not be buried under $80\text{--}320\text{ years}$ of compacted regolith. |
| **7. Mobility Wheel Grousers (Cleats) & Skin**<br>*(Arvidson et al., 2017; Toupet et al., 2020)* | **Wheel OD:** $500\text{ mm}$, **Width:** $400\text{ mm}$<br>**Skin Thickness:** $0.75\text{ mm}$<br>**Grouser (Cleat) Cross-Section:** $\sim 6\text{ mm}$ tall $\times 1.5\text{--}2.0\text{ mm}$ thick machined 7075-T7351 aluminum chevron strips. | *Curiosity* has suffered fatigue fractures of several wheel grousers and skin punctures since Sol 490. Shed wheel fragments are flat/curved chevron strips, not solid $11.2\text{ mm}$ cylinders. | **RULED OUT.**<br>Wheel cleats are thin, flat/angled strips ($1.5\text{--}2\text{ mm}$ thick), completely incompatible with an $11.2\text{ mm}$ diameter circular cylinder. |
| **8. EDL Cruise & Entry Tungsten Ballast Masses**<br>*(Kornfeld et al., 2014; Prakash et al., 2008)* | **Cruise Balance Masses:** Six $25\text{ kg}$ tungsten blocks<br>**Entry Balance Masses:** Two $75\text{ kg}$ tungsten blocks | Jettisoned exo-atmospherically (prior to atmospheric entry) and prior to parachute deploy, impacting tens of kilometers away and creating meter-scale craters discovered from orbit by HiRISE. | **RULED OUT.**<br>Four orders of magnitude too massive ($25\text{--}75\text{ kg}$ vs. $\sim 10\text{--}27\text{ g}$) and impacted $15\text{--}80\text{ km}$ away. |

---

## 3. Comparative Dataset of Documented Mars Hardware Debris (FOD) Events

Whenever terrestrial spacecraft shed hardware on Mars, the resulting debris exhibits unmistakable diagnostic traits: **zero stratigraphic burial** (resting loosely on top of the surface or wedged onto rock outcrops), **crumpled/torn sheet-metal or polymer morphology**, or **immediate proximity to active rover mechanisms**.

| Mission & Sol | Location | Debris Description & Material | Physical Dimensions | Emplacement & Burial State | Reference |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Curiosity Sol 61**<br>(Oct 7, 2012) | *Rocknest*<br>(Gale Crater) | Bright shred of transparent plastic cable-tie wrapper / Kapton film shed during first scoop operations. | $\sim 13\text{ mm} \times 1\text{--}2\text{ mm}$ (thin curled sliver, $<0.1\text{ mm}$ thick) | Resting loosely **on top** of loose sand grains directly beneath the robotic arm scoop. Zero burial. | NASA/JPL-Caltech Mission Status Report (Oct 2012); Blake et al. (2013) |
| **Curiosity Sol 1647+**<br>(2017–2024) | Mount Sharp Traverse<br>(Gale Crater) | Fractured aluminum 7075-T7351 wheel grouser chevrons from middle wheels. | Thin chevron strip ($\sim 1.5\text{--}2\text{ mm}$ thick $\times 6\text{ mm}$ high) | Imaged on wheel or resting freshly inside crushed wheel tracks. | Arvidson et al. (2017), [10.1016/j.jterra.2017.03.001](https://doi.org/10.1016/j.jterra.2017.03.001); Toupet et al. (2020) |
| **Perseverance Sol 466**<br>(June 13, 2022) | *Hogwallow Flats*<br>(Jezero Crater) | Crumpled piece of perforated aluminized Kapton/Dacron multi-layer insulation (MLI) thermal blanket from EDL descent stage ($2\text{ km}$ away). | $\sim 50\text{--}80\text{ mm}$ crumpled ultra-thin foil sheet ($m < 1\text{ g}$, area-to-mass ratio $> 10\text{ m}^2/\text{kg}$) | Wedged **loosely on top** of jagged outcrop prongs; blown there because ultra-light foil acts as a sail in Martian wind. Zero soil burial. | NASA/JPL-Caltech Perseverance Blog (June 2022) |
| **Perseverance Sol 495**<br>(July 12, 2022) | *Hogwallow Flats*<br>(Jezero Crater) | Tangled bundle of Dacron netting fiber from EDL thermal blanket. | Thin fibrous cordage ($\sim 0.5\text{ mm}$ strand thickness) | Resting loosely on top of rock surface; disappeared several sols later when blown away by wind. | NASA/JPL-Caltech Perseverance Blog (July 2022) |
| **Sol 3556 Cylinder**<br>(Aug 7, 2022) | *Paraitepuy Pass*<br>(Gale Crater) | Rigid, undeformed right circular cylinder ($R^2 = 0.9985$, $b/a = 0.9335$). | **$D = 11.2 \pm 0.5\text{ mm}$**<br>**$L = 34.9 \pm 0.8\text{ mm}$**<br>($3.24:1$ aspect ratio) | **Embedded $33.5\%$ ($2.0\text{--}3.2\text{ mm}$)** inside consolidated pebble-armored duricrust along a planar horizon, $13\text{--}15\text{ km}$ (air) / $28.4\text{ km}$ (drive) from EDL site. | Bogner (2026), [10.5281/zenodo.23789092](https://doi.org/10.5281/zenodo.23789092) |

---

## 4. Aerodynamic & Ballistic Transport Bounds from EDL Sites

### 4.1 Distance from MSL Entry, Descent, and Landing (EDL) Hardware in Gale Crater

All major *Curiosity* EDL hardware impacted on the flat crater floor (*Aeolis Palus*) near Bradbury Landing on August 6, 2012 (Vasavada et al., 2014; Kornfeld et al., 2014):

- **Bradbury Landing (Touchdown Site):** $4.5895^\circ\text{S}, 137.4417^\circ\text{E}$ (Elevation $-4,501\text{ m}$ MOLA).
- **MSL Descent Stage (Sky Crane) Crash Site:** $\sim 650\text{ m}$ WNW of Bradbury Landing.
- **Backshell & Parachute Impact Site:** $\sim 615\text{ m}$ NW of Bradbury Landing.
- **Heat Shield Impact Site:** $\sim 1.2\text{ km}$ ESE of Bradbury Landing.
- **Sol 3556 Site 96 (Paraitepuy Pass):** Cumulative odometry **$28.4\text{ km}$ ($17.6\text{ miles}$)** along the rover traverse, and **$13.5\text{ to }15.0\text{ km}$ ($8.4\text{--}9.3\text{ miles}$)** in a direct straight line SSE, plus an **uphill vertical climb of $+610\text{ meters}$** onto the flank of Mount Sharp.

### 4.2 Aerodynamic Threshold Wind Speed to Loft or Roll a Solid $11.2\text{ mm} \times 35\text{ mm}$ Cylinder

Unlike the ultra-thin perforated Dacron foil found by *Perseverance* (which has a thickness of $\sim 25\text{--}50\ \mu\text{m}$ and an area-to-mass ratio $A/m \sim 10\text{--}20\text{ m}^2/\text{kg}$), a solid $11.2\text{ mm} \times 35\text{ mm}$ cylinder has a projected cross-sectional area $A_\perp = D \cdot L = 3.92 \times 10^{-4}\text{ m}^2$ and a tiny area-to-mass ratio:

- For Aluminum ($\rho = 2,700\text{ kg/m}^3$, $m = 9.31\text{ g}$): $A_\perp / m = 0.042\text{ m}^2/\text{kg}$ ($250\times\text{--}500\times$ lower than foil).
- For Titanium ($\rho = 4,430\text{ kg/m}^3$, $m = 15.28\text{ g}$): $A_\perp / m = 0.026\text{ m}^2/\text{kg}$.
- For Stainless Steel ($\rho = 7,900\text{ kg/m}^3$, $m = 27.26\text{ g}$): $A_\perp / m = 0.014\text{ m}^2/\text{kg}$.

To aerodynamically suspend or loft a solid cylinder against Martian gravity ($g = 3.721\text{ m/s}^2$) in Mars's thin atmosphere ($\rho_{\text{atm}} \approx 0.015\text{--}0.020\text{ kg/m}^3$ at $6\text{--}8\text{ hPa}$), we evaluate both the **direct local wind speed** $v_{\text{local}}$ right at the cylinder's centroid height ($z = D/2 \approx 5.4\text{ mm}$ above the ground, assuming $C_D = 1.0$) where $F_D = \frac{1}{2} \rho_{\text{atm}} v_{\text{local}}^2 C_D A_\perp = m g$:

$$v_{\text{local}} = \sqrt{\frac{2 m g}{\rho_{\text{atm}} C_D A_\perp}} = \sqrt{\frac{\pi \rho_{\text{obj}} D g}{2 \rho_{\text{atm}} C_D}}$$

and the corresponding **free-stream wind speed at *Curiosity*'s $1.5\text{ m}$ REMS anemometer height** ($v_{1.5\text{m}}$), accounting for logarithmic planetary boundary-layer shear ($u(z)/u(1.5\text{ m}) = \ln(z/z_0)/\ln(1500/z_0) \approx 0.316$ for aerodynamic roughness $z_0 \approx 0.46\text{ mm}$, or equivalently a ground-plane lift coefficient $C_L \approx 0.10$, giving $v_{1.5\text{m}} \approx 3.16\, v_{\text{local}}$):

- **Engineering Polymer / Hollow Sleeve ($\rho_{\text{eff}} = 1,400\text{ kg/m}^3$, $m \approx 4.5\text{ g}$):** $v_{\text{local}} \approx \mathbf{67\text{--}78\text{ m/s}}$ at $z = 5.4\text{ mm}$, corresponding to $v_{1.5\text{m}} \approx \mathbf{210\text{--}247\text{ m/s}}$ ($\mathbf{470\text{--}553\text{ mph}}$, Mach $0.9\text{--}1.03$ on Mars!)
- **Aluminum 6061/7075 ($\rho = 2,700\text{ kg/m}^3$, $m \approx 8.7\text{--}9.3\text{ g}$):** $v_{\text{local}} \approx \mathbf{92\text{--}109\text{ m/s}}$ at $z = 5.4\text{ mm}$, corresponding to $v_{1.5\text{m}} \approx \mathbf{292\text{--}343\text{ m/s}}$ ($\mathbf{653\text{--}768\text{ mph}}$, Mach $1.2\text{--}1.43$ on Mars!)
- **Titanium Ti-6Al-4V ($\rho = 4,430\text{ kg/m}^3$, $m \approx 14.2\text{--}15.3\text{ g}$):** $v_{\text{local}} \approx \mathbf{118\text{--}139\text{ m/s}}$ at $z = 5.4\text{ mm}$, corresponding to $v_{1.5\text{m}} \approx \mathbf{374\text{--}440\text{ m/s}}$ ($\mathbf{836\text{--}984\text{ mph}}$, Mach $1.6\text{--}1.83$ on Mars!)
- **Stainless Steel 304 / Inconel ($\rho = 7,900\text{--}8,000\text{ kg/m}^3$, $m \approx 25.6\text{--}27.3\text{ g}$):** $v_{\text{local}} \approx \mathbf{159\text{--}186\text{ m/s}}$ at $z = 5.4\text{ mm}$, corresponding to $v_{1.5\text{m}} \approx \mathbf{502\text{--}587\text{ m/s}}$ ($\mathbf{1,123\text{--}1,313\text{ mph}}$, Mach $2.1\text{--}2.45$ on Mars!)

Because maximum surface wind gusts in Gale Crater measured by REMS at $1.5\text{ m}$ height rarely exceed $20\text{--}35\text{ m/s}$ (corresponding to only $6\text{--}11\text{ m/s}$ at $z = 5.4\text{ mm}$; Viúdez-Moreiras et al., 2019), **aerodynamic wind transport of the cylinder from the EDL crash sites—especially $610\text{ m}$ uphill across $13.5\text{--}15.0\text{ km}$ of rugged boulders, buttes, and dunes—is physically impossible.**

### 4.3 Exclusion of All Other Historical Mars Missions

To ensure complete closure against hardware from earlier human spacecraft, we verify the landing/impact coordinates of every other Mars lander, rover, and impactor in history:

| Mission & Year | Landing / Impact Region | Coordinates | Great-Circle Distance from Gale Crater ($4.6^\circ\text{S}, 137.4^\circ\text{E}$) |
| :--- | :--- | :---: | :---: |
| **InSight** (2018) | *Elysium Planitia* | $4.5^\circ\text{N}, 135.6^\circ\text{E}$ | **$\sim 550\text{ km}$ North** (separated by the global dichotomy boundary escarpment) |
| **MER Spirit** (2004) | *Gusev Crater* | $14.6^\circ\text{S}, 175.5^\circ\text{E}$ | **$\sim 2,280\text{ km}$ East-Southeast** |
| **Zhurong** (2021) | *Utopia Planitia* | $25.1^\circ\text{N}, 109.9^\circ\text{E}$ | **$\sim 2,360\text{ km}$ Northwest** |
| **Beagle 2** (2003) | *Isidis Planitia* | $11.5^\circ\text{N}, 90.4^\circ\text{E}$ | **$\sim 2,920\text{ km}$ West-Northwest** |
| **Perseverance** (2021) | *Jezero Crater* | $18.4^\circ\text{N}, 77.5^\circ\text{E}$ | **$\sim 3,730\text{ km}$ West-Northwest** |
| **Viking 2** (1976) | *Utopia Planitia* | $48.0^\circ\text{N}, 134.3^\circ\text{E}$ | **$\sim 3,120\text{ km}$ North** |
| **Mars 2 / 3 / 6, Viking 1, Pathfinder, Opportunity, Phoenix, Polar Lander, Schiaparelli** | Western Hemisphere & Polar Regions | $> 5,000\text{ km}$ away | **$5,000\text{ to }9,500\text{ km}$ distant** |

**Conclusion:** Gale Crater has received **only one** human spacecraft mission (*Curiosity*, August 6, 2012). No pre-2012 Soviet, NASA, ESA, or CNSA hardware has ever entered or impacted within $500\text{ km}$ of Gale Crater.

---

## 5. Verified Citations for Module 02

1. **Anderson, R. C., Jandura, L., Okon, A. B., et al. (2012).** "Collecting Samples in Gale Crater, Mars; an Overview of the Mars Science Laboratory Sample Acquisition, Sample Processing and Handling System." *Space Science Reviews*, 170(1–4), 57–75. DOI: [10.1007/s11214-012-9898-9](https://doi.org/10.1007/s11214-012-9898-9)
2. **Okon, A. B. (2010).** "Mars Science Laboratory Drill." *Proceedings of the 40th Aerospace Mechanisms Symposium*, NASA/CP-2010-216272, pp. 305–318. NTRS ID: [20100021922](https://ntrs.nasa.gov/citations/20100021922)
3. **Bement, L. J., & Schimmel, M. L. (1995).** *A Manual for Pyrotechnic Design, Development and Qualification*. NASA Reference Publication 1352 (NASA-RP-1352). NTRS ID: [19950023695](https://ntrs.nasa.gov/citations/19950023695)
4. **Kornfeld, R. P., Prakash, R., Devereaux, A. S., et al. (2014).** "Verification and Validation of the Mars Science Laboratory/Curiosity Rover Entry, Descent, and Landing System." *Journal of Spacecraft and Rockets*, 51(4), 1251–1269. DOI: [10.2514/1.A32860](https://doi.org/10.2514/1.A32860)
5. **Vasavada, A. R., et al. (2014).** "Overview of the Mars Science Laboratory mission: Bradbury Landing to Yellowknife Bay and beyond." *Journal of Geophysical Research: Planets*, 119(6), 1134–1161. DOI: [10.1002/2014JE004622](https://doi.org/10.1002/2014JE004622)
6. **Arvidson, R. E., et al. (2017).** "Relating geologic units and mobility system kinematics contributing to Curiosity wheel damage at Gale Crater, Mars." *Journal of Terramechanics*, 73, 73–93. DOI: [10.1016/j.jterra.2017.03.001](https://doi.org/10.1016/j.jterra.2017.03.001)
7. **Toupet, O., Biesiadecki, J. J., Rankin, A. L., et al. (2020).** "Terrain-adaptive wheel speed control on the Curiosity Mars rover: Algorithm and flight results." *Journal of Field Robotics*, 37(5), 699–728. DOI: [10.1002/rob.21903](https://doi.org/10.1002/rob.21903)
8. **Viúdez-Moreiras, D., Gómez-Elvira, J., Newman, C. E., et al. (2019).** "Gale surface wind characterization based on the Mars Science Laboratory REMS dataset. Part I: Wind retrieval and Gale's windireland regime." *Icarus*, 319, 909–925. DOI: [10.1016/j.icarus.2018.10.011](https://doi.org/10.1016/j.icarus.2018.10.011)
