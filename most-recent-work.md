Sol 3556 Cylindrical Geometry: Reproducibility Package
Curiosity Mastcam-100 / Mastcam-Right · Product 3556MR1025170721700585C00_DRCL
Analysis record: November 10, 2026
Prepared for: Justin Bogner · Cambrian Minds Media
Purpose and principal result
This package reproduces the measurements made in the November 2026 investigation of the apparent cylindrical object in Curiosity Sol 3556 imagery. It deliberately separates the object's exposed front rim, its longitudinal edge, and its cast shadow on the ground. The cast shadow is not the buried lower portion of the projected front-face ellipse.

The exposed upper rim fits an ellipse with minor/major axis ratio 0.8246 (61 selected native-image points; residual 0.2156 raw pixels). The fitted minor-axis direction 28.533° differs by 0.751° from the independently measured longitudinal edge direction 29.284°. The recorded solar position, an obliquely oriented circular front face, and a locally sloping receiving ground plane generate a projected curved shadow consistent with the visible forward shadow. A raw-image threshold analysis, independent of the painted blue shadow outline, gives a best fit at 32.82° receiving-plane rotation for the 85-DN threshold, with 1.049 native-pixel or 4.80 enlarged-image-pixel RMS vertical discrepancy.

This is a conditional geometric compatibility test, not a measurement of the terrain slope. The receiving-plane angle was obtained by fitting shadow data; its value should not be reused as independent evidence. The rear termination is assumed to be the object boundary as indicated by the investigator; its contour is not newly measured in this package.
Minimal measurement inventory
Quantity Value Status / origin
Exposed rim points 61, with 2 disconnected picks excluded Native DRCL-derived grayscale ROI; measure-exposed-rim.py
Free ellipse major diameter 40.303 raw px Fit to exposed upper arc
Free ellipse minor diameter 33.234 raw px Fit to exposed upper arc
Minor/major ellipse ratio 0.8246 Derived from measured rim
Minor-axis bearing 28.533° Fit; sensitive to arc truncation
Ellipse radial RMSE 0.2156 raw px Fit residual
Circle radial RMSE 0.7267 raw px Same sampled arc, different model
Upper longitudinal edge bearing 29.284° Previously measured in upstream repository
Longitudinal straightness 0.111 raw px perpendicular RMSE Previously measured, not recomputed here
Recorded solar elevation 69.8224° NASA PDS3 label
Recorded solar azimuth 186.8169° NASA PDS3 label
Shadow travel direction 6.8169° azimuth Derived; away from Sun
Nominal focus distance 3.957 m Instrument metadata; not direct range
Face/view obliquity 34.45° arccos(0.8246) using circular-face assumption
Selected face-axis elevation approximately -0.34° Forward 3D model; one branch, not independently identified by rear contour
Radius at nominal focus about 5.86 mm Conditional on focus distance / camera model
85-DN ground rotation fit 32.82° Fitted to raw-shadow ground-boundary profile
85-DN RMS residual 1.049 raw px / 4.80 enlarged px Model vs extracted raw-image boundary
Rotation range, 9 thresholds 28.10°–35.12° Sensitivity across 65–105 DN thresholds

Important: Native image coordinates and enlarged annotation coordinates are different; the enlargement factor is 549/120 = 4.575. A fit residual of 1.049 native pixels is not 1.049 annotation pixels. The exposed ellipse refers to the front outer rim; the cast shadow is a separate ground projection. Geometry and solar ephemeris are separate sources of constraints.
Data sources and provenance

- Original instrument product: NASA Mars Science Laboratory Mastcam-Right, Sol 3556; observation product 3556MR1025170721700585C00_DRCL.
- Working upstream repository: <https://github.com/CambrianMinds/martian-cylinder>
- Calibrated crop (500 x 450 RGB): data/crop_bottom_right.png in that repository. Its verified Git blob SHA is 34a38f6b8c1b9ef9fe5b3a553a0af47f300e7a95 (not a normal file SHA256).
- Camera parameters: data/3556MR1025170721700585C00_DRCL.LBL from the same repository. Values transcribed for computation appear in data/calibration-used.json and in scripts/project-shadow.py.
- Native exposed-rim luminance region: data/exposed-rim-source-roi.npy, image coordinates relative to the 120 x 120 scene. This array is archived to permit fully offline re-fitting of the front rim.
- Raw-shadow boundary profiles: data/raw-shadow-profiles.json, measured directly from the unannotated DRCL-derived crop at nine grayscale thresholds. These points are archived to permit fully offline comparison of the shadow model.
- User annotation: data/annotated-face-shadow.jpg identifies the pink physical face, green exposed rim, red contact chord, orange ground shadow, and blue drawn shadow outline. The blue outline is not used when segmenting the raw cast shadow.
- User visual comparison: data/visual-shadow-comparison-user.png, supplied for visual context, not used as an independent instrument measurement.
For full raw-image segmentation from the original source (instead of the archived raw-pixel profiles), download the public calibrated crop with python scripts/fetch-original-crop.py. The downloader validates the source blob checksum and refuses silent substitutions. Full downstream measurement and fit reproduction runs offline using the archived ROI and profiles.
How to reproduce
Python >= 3.10 recommended. From the extracted top-level folder:
python -m pip install -r requirements.txt
python scripts/run-all.py
run-all.py reruns: upper-rim extraction and ellipse/circle fits; 3D solar projection; comparison with annotated blue curve; independent comparison with the archived native-pixel shadow boundary; generation of all eight figures; and regression verification of the numerical results. Outputs go to outputs/ and figures/.

To rerun the raw shadow pixel segmentation from GitHub:
python scripts/fetch-original-crop.py
python scripts/extract-raw-shadow.py --crop data/crop-bottom-right-from-github.png \
  --output outputs/raw-shadow-profiles-from-crop.json
python scripts/compare-raw-shadow.py --profiles outputs/raw-shadow-profiles-from-crop.json \
  --output outputs/raw-shadow-comparison-from-crop.json
There is no need to download new data to reproduce the numerical result after the profiles have been archived; downloading the full crop is relevant to verifying the segmentation step independently.
Methods, in order

1. Trace the exposed front rim
Select the illuminated green-bounded outer rim from the native grayscale ROI. Do not use the entire dark bean shape; do not treat the lower cast-shadow outline as part of the cap. Local gradient peaks are refined subpixel-wise. Two discontinuous ground detections are omitted using an image-continuity rule. Fit an unconstrained ellipse and a circle to the same 61 retained edge points. Repeat the ellipse fit with its minor-axis bearing fixed at the independently measured upper-generator direction. Run small perturbations of starting center and exposed-arc extent. The full-arc minor-axis direction is sensitive to trimming, which is reported in Figure 7.
2. Establish the 3D cylinder hypothesis
Assume the exposed projected ellipse represents a planar circular end face normal to a right-cylinder axis. The ellipse ratio gives approximate viewing obliquity by acos(b/a). The ellipse minor-axis bearing and the image camera geometry give candidate face normals. Choose the branch consistent with the observed face being predominantly in self-shadow. Reconstruct the rim in 3D using the CAHV camera and nominal focus distance, then map it back into the enlarged-image coordinates. The near-horizontal axis is a selected model branch, not an independent measurement of horizontal level or of the soil's incline.
3. Establish contact chord and receiving plane
Use the red, annotation-derived front/ground intersection line, y = -0.46865*x + 385.107 in the 549x549 enlarged image. Intersect it with the modeled front rim to locate its contact endpoints. Rotate a candidate receiving plane around the 3D line joining these endpoints. This preserves the contact seam while allowing a local ground surface to slope downward toward the front. Rotation is measured relative to the constructed starting plane (nominally level), not a directly surveyed Martian topographic slope.
4. Project sunlight onto candidate ground surfaces
Take the recorded solar elevation 69.8224° and azimuth 186.8169°. For each 3D rim point, extend a ray away from the Sun until it intersects the receiving plane. Re-project the ray/ground intersection through the camera model. Record the outer curved boundary. No cast-shadow pixels are involved in constructing a candidate raycast curve.
5. Extract ground-shadow observations without blue annotation
From the unannotated calibrated source crop, convert RGB to luminance (round(0.299R + 0.587G + 0.114B)). Restrict to ground pixels below the fixed annotated red chord, apply thresholds 65–105 DN in 5-DN increments, take the largest 8-connected dark component, and record its bottommost native pixel for each successive x-column. The spatial selection and chord still encode human judgment; the blue painted arc does not. This method is a simple repeatable brightness-edge proxy, not a physical albedo/illumination separation of every nearby regolith pixel.
6. Compare independently extracted boundary to model
For each threshold, vary one parameter, the receiving-plane rotation, and minimize the root-mean-square vertical difference between the model's lower envelope and the raw-image bottommost dark-pixel profile. Report the optimized angle, resulting RMS residual, the flat-ground residual, and threshold sensitivity. Preserve the fixed cylinder/rim/Sun geometry; do not use the drawn blue outline to optimize the native-pixel fit.
Primary results
The outputs/exposed-rim-measurements.json and outputs/raw-shadow-comparison-results.json files contain all primary result rows with full recorded settings.

- The upper-rim ellipse is tightly fitted and its full-arc bearing closely agrees with the independently measured upper generator. This is positive geometric evidence for a cylindrical interpretation.
- The receiving-plane rotation of 32.82° at 85 DN yields a model-to-raw-shadow vertical RMS of 1.049 native pixels. At 0°, the same comparison gives 6.746 native pixels RMS. This is a substantial improvement for the locally sloping receiving-surface family.
- Across thresholds 65, 70, ..., 105 DN, best rotations span 28.10–35.12°, with best residuals 0.753–1.049 raw pixels. All nine extracted boundaries have consistent bowed shape, despite differing selected darkness cutoffs.
- The original hand-drawn blue boundary is close to the predicted outline, and the independently extracted raw-dark-boundary has similar curvature. The drawn and raw contours need not coincide to the pixel, because the drawn outline was an interpretive markup and the threshold extraction is brightness-based.
Figure index

1. figures/figure-01-exposed-rim-fit.png: original native-pixel upper-rim ellipse and circle fits.
2. figures/figure-02-annotated-scene.png: interpretation of the separate face/chord/ground-shadow regions.
3. figures/figure-03-solar-projection-comparison.png: flat versus raw-best versus annotation-best modeled shadow boundary.
4. figures/figure-04-raw-shadow-boundary.png: raw-image shadow profiles at three brightness thresholds versus modeled curve.
5. figures/figure-05-ground-rotation-sensitivity.png: RMS error as a function of the receiving-plane rotation.
6. figures/figure-06-threshold-robustness.png: ground-rotation estimate and residual versus threshold.
7. figures/figure-07-arc-selection-sensitivity.png: front-rim ellipse sensitivity to selection.
8. figures/figure-08-user-visual-comparison.png: the investigator's close-up comparison of painted, modeled, and extracted boundaries.
Limitations and interpretation

- A circular front face and right cylinder are the working hypothesis used in the 3D ray projection. These procedures test coherence; they do not establish uniqueness against all other conceivable solids.
- The rear terminus is assumed physically part of the cylinder. This package does not measure an independent 3D rear-plane orientation or constrain cylinder length from that terminus.
- The red chord is interpretation-assisted. Repositioning it, changing ellipse selection, or allowing nonplanar local ground will change the inferred parameters. The blue curve was excluded only from the raw profile segmentation, not from the earlier hand-drawn comparison figure.
- A one-parameter family of ground planes is fitted to the observed shadow. Therefore the optimum ground inclination is not independent evidence and must not be counted as such.
- The raw shadow's boundary is diffuse and scene texture may shift threshold-selected pixels. The threshold sweep is a reproducibility/sensitivity test, not proof of exact soil geometry.
- The camera focus range is not an independently measured object distance. Physical diameter depends on assumed distance; image-plane quantities and dimensionless ratios do not.
- More than one 3D cylinder-axis branch is compatible with an ellipse from a single view. The approximate near-horizontal inclination is selected using scene/lighting interpretation and should not be treated as a precision field measurement.
Conclusion: The observed exposed-rim geometry and longitudinal edge support a provisional geometrically cylindrical identification, and the recorded solar illumination permits a close modeled match to the observed forward cast shadow on a locally sloping receiving surface. The cast shadow creates no identified geometric contradiction to that interpretation. The shadow-fit result supports compatibility rather than independently certifying the cylinder or the terrain slope.
Integrity, status, and use
All figures in this package were created for this analysis or provided directly by the investigator. No figures are reused from the upstream GitHub repository. The results/ directory contains the rerun logs and archived numerical reference values. scripts/verify-results.py compares the primary numbers against the archived baseline to catch accidental drift. data/source-provenance.json and data/calibration-used.json document the input and model parameters. Generated artifacts and scripts are provided for technical examination and potential publication, not as evidence of physical manufacture or non-natural origin.
