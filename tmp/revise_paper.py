from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'audit/comparative-study'
for path in (out/'scripts').glob('*.py'):
    text=path.read_text(encoding='utf-8')
    text=text.replace("ROOT=Path(__file__).resolve().parents[2]", "ROOT=Path(__file__).resolve().parents[3]")
    text=text.replace("ROOT/'comparative-study'", "ROOT/'audit/comparative-study'")
    text=text.replace('python comparative-study/', 'python audit/comparative-study/')
    text=text.replace('-r comparative-study/', '-r audit/comparative-study/')
    text=text.replace('-s comparative-study/', '-s audit/comparative-study/')
    path.write_text(text,encoding='utf-8')
for path in [out/'image-manifest.json', out/'report.md']:
    text=path.read_text(encoding='utf-8').replace('comparative-study/', 'audit/comparative-study/')
    path.write_text(text,encoding='utf-8')

p=ROOT/'papers/martian-cylinder-technical-paper.tex'
t=p.read_text(encoding='utf-8')
def replace(old,new):
    global t
    if old not in t: raise ValueError('Missing manuscript anchor: '+old[:90])
    t=t.replace(old,new)
def section(start,end,new):
    global t
    a=t.index(start);b=t.index(end,a)
    t=t[:a]+new+'\n\n'+t[b:]

t=t.replace('% Self-contained technical manuscript. Original vector diagrams; no images\n% from the source repository are reproduced here.', '% Technical manuscript with native-image crops and JSON-derived predictive figures.')
t=t.replace('11 November 2026','13 November 2026')
t=t.replace('A quantitative analysis of two terminal curves, exterior tangency, partial burial, and competing physical models','Boundary metrology, frozen-shape prediction, and geological comparison')
replace('\\begin{document}', '\\input{paper-analysis-values.tex}\n\\begin{document}')
section('\\noindent A centimeter-scale object', '\\end{abstract}', r'''\noindent A centimeter-scale object in Curiosity Mastcam-100 imagery acquired on sol 3556 exhibits two curved terminations and a straight upper exterior boundary. Physically directed subpixel localization yields 35 near-rim, 24 far-termination, and 26 upper-boundary stations. A six-parameter common-section, common-axis model with exact upper tangency fits all 85 observations at $0.3788\px$ RMS. More importantly, a front/dorsal-derived ellipse with frozen size, shape, and orientation predicts rear points beyond those used for translation: six anchors predict the other 18 stations at $\SparseRearRMS\px$ RMS, and guarded contiguous rear holdouts yield $\BlockedRearRMS\px$. Guarded spatial holdouts of the strict model yield $\BlockedJointRMS\px$ across all three features. Withholding the entire dorsal boundary is reported separately as a cross-feature sensitivity test. An earlier tapered formulation achieves a lower numerical residual but violates its own ellipse--line tangency condition and is rejected as a physical frustum. A completed comparison of 28 Curiosity images, including 18 uniformly measured whole frames, demonstrates comparable straight segments in geological scenes but does not establish the frequency of the full measured conjunction. The configuration exhibits manufacturing-like geometric regularity supported by predictive tests; composition and provenance are not determined.''')
replace('A secondary question is which physical formation histories can plausibly account for that conjunction.', 'The central evidentiary question is whether that geometry predicts observed boundary points that did not participate in its registration or fit. Determining physical origin is beyond the present scope.')
replace('This paper reports the resulting measurements, model performance, uncertainty structure, and comparison of candidate formation mechanisms. Observed pixel features, geometric constraints, and interpretations of physical origin are treated as separate levels of inference.', r'''This paper reports measurements, predictive validation, uncertainty structure, and the completed geological comparison. To our knowledge, this is the first publicly documented, reproducible quantitative metrology study of this particular feature. Earlier recognition and visualization are acknowledged: Ward credits Rami Bar Ilan with discovery, and MILTOID presented Bayer decoding and a visual 3D cylinder overlay in October 2025 \cite{ward2025,miltoid2025}. Those preliminary checks precede the numerical metrology and predictive tests reported here. The original study appears in the repository history on 24 October 2026 and in the Zenodo deposit published 30 October; independent reconstruction was added on 11 November, followed by the 13 November predictive validation \cite{bogner2026deposit}.''')
replace('The complete image data and executable analyses are archived in the research repository', 'The image data and executable analyses are retained in the research repository')

# Add the native-image figure immediately after the feature classification.
anchor='\\section{Camera Geometry, Illumination, and Scale}'
replace(anchor,r'''\begin{figure}[ht]
\centering
\includegraphics[width=0.94\linewidth]{figures/target-boundaries.pdf}
\caption{Native DRXX radiometric image, enlarged without generative enhancement. The unmarked crop (left) and the same crop with recorded stations (right) identify the near rim, rear terminus, dorsal material boundary, excluded adjacent-pebble station, and soil/shadow contacts. Display contrast is normalized for visibility; measurements use the original radiometric arrays. Labels for soil and shadow identify interpreted regions rather than newly sampled contours.}
\label{fig:target}
\end{figure}

'''+anchor)

replace('\\(M_4\\) is a coupled conical-frustum model with eight parameters', '\\(M_4\\) is the earlier eight-parameter tapered image-plane formulation, originally interpreted as a conical frustum')
replace('Its additional freedom allows a geometrically different explanation of the observed angular spread.', 'Its additional freedom absorbs the observed angular spread numerically, but the formulation fails the physical tangency check in \\cref{sec:taper}.')
replace('\\(M_4\\), tapered &', '\\(M_4\\), invalid frustum &')
replace('The nominal weighted objectives produce reported BIC values of 2680.2 for \\(M_1\\), 1947.3 for \\(M_2\\), and 1079.6 for \\(M_4\\), under their specified station uncertainty model.', 'The nominal weighted objectives give BIC values of 2680.2, 1947.3, and 1079.6 for \\(M_1,M_2,M_4\\). These are diagnostics under uncalibrated station errors, not physical-model probabilities. For \\(M_1\\), \\(\\chi^2=2653.51\\) with 79 nominal residual degrees of freedom gives \\(\\chi^2_\\nu=33.59\\). M4 additionally fails its physical silhouette condition.')
section('\\begin{figure}[ht]\n\\centering\n\\begin{tikzpicture}', 'The 6-parameter model', '')
replace('They do not require dismissing a more flexible competing image-plane model.', 'M4\'s smaller numerical residual does not restore its failed physical tangency constraint.')

anchor='\\subsection{Axis alignment and orientation identifiability}'
replace(anchor,r'''\subsection{Predictive validation beyond registration points}
\label{sec:prediction}

The new tests preserve the existing coordinates and exclusions. Their protocol was written before these validation runs; the tests are retrospective coordinate-level checks, not a blind repeat of boundary selection. Two front-shape references must be distinguished. The freely oriented ellipse above gives $0.18629\px$ rear RMS. The predictive tests instead freeze the front ellipse constrained to the measured dorsal orientation: $a=20.02897\px$, $b=16.84577\px$, $\theta=28.89475^\circ$, and scale $s=1$. Fitting only its rear translation reproduces $\RegisteredRearRMS\px$ RMS. Neither rear size nor orientation is adjusted.

\begin{table}[ht]
\centering\small
\caption{Descriptive fits and heldout predictions. All errors are raw RMS distances in native pixels; the first and fourth rows are in-sample references.}
\label{tab:prediction}
\begin{tabularx}{\linewidth}{@{}l X X r@{}}
\toprule
\textbf{Check} & \textbf{Used in fit} & \textbf{Scored observations} & \textbf{RMS} \\
\midrule
Frozen rear registration & All 24 rear stations; two translations & Same 24 rear stations & \RegisteredRearRMS \\
Sparse registration & Rear indices 0, 4, 8, 12, 16, 20 & Other 18 rear stations & \SparseRearRMS \\
Guarded rear blocks & Remaining rear stations, excluding guards & Each rear station withheld once & \BlockedRearRMS \\
Strict $M_1$, full fit & All 85 stations; six parameters & Same 85 stations & \FullJointRMS \\
Guarded $M_1$ blocks & Remaining stations from all three families & Each of 85 stations withheld once & \BlockedJointRMS \\
Entire dorsal withheld & All front and rear stations only & All 26 dorsal stations & \DorsalWithheldRMS \\
\bottomrule
\end{tabularx}
\end{table}

In five contiguous rear folds, the test block and two neighboring guard stations at each boundary are excluded from translation fitting. The strict-model folds similarly withhold one contiguous block from each feature family, with two-station guards. Every point is scored once across folds. Three prespecified starting angles ($28^\circ$, $31.2^\circ$, $35^\circ$) are tried; the smallest training objective selects the solution, never the withheld score. All starts converge and no parameter reaches a bound. Strict-model heldout RMS values are front $0.8456\px$, rear $0.5946\px$, and dorsal $0.6491\px$; pooling their squared residuals gives $\BlockedJointRMS\px$.

The rear agreement survives both sparse registration and guarded holdouts at approximately $0.2$--$0.24\px$. It therefore extends beyond the rear points used to position the transferred shape. This predicts local curve positions after registration, not the rear's absolute position or cylinder length from the front alone.

\begin{figure}[ht]
\centering
\includegraphics[width=0.95\linewidth]{figures/rear-prediction.pdf}
\caption{Frozen front/dorsal-derived ellipse translated using six rear anchors. Left: native radiometric crop with the transferred curve, fitted anchors, and 18 withheld stations. Right: signed orthogonal residuals for sparse-registration and guarded-block predictions. The curve is clipped to the exposed rear region for legibility; the concealed perimeter is not observed.}
\label{fig:prediction}
\end{figure}

Withholding the entire dorsal feature is a separate sensitivity experiment. Front/rear-only fitting predicts its tangent at $\DorsalWithheldRMS\px$ RMS, maximum $3.391\px$, with axis $33.177^\circ$ rather than the measured dorsal bearing $28.895^\circ$. These modest absolute image deviations are larger than the residuals of the complete fit. They demonstrate the information supplied by the dorsal boundary: removing that measured constraint changes the preferred orientation and tangent. This experiment is not a mandatory passing standard, a measurement of physical surface damage, or a calibrated rejection. It also does not replace the fixed-shape rear tests, which retain the dorsal information by design.

'''+anchor)
replace('\\textbf{Coupled conical model}', '\\textbf{Rejected tapered formulation}')
replace('Taper absorbs axis/boundary angular coupling \\\\', 'Numerical taper violates physical tangency \\\\')
replace('The workflow samples several overlapping descriptions', 'The workflow samples several overlapping descriptions') if False else None
replace('These tests support the stability of the selected boundaries and the value of presenting image-space residuals without converting them into unsupported manufacturing tolerances.', 'These tests characterize the stability of selected image boundaries. Physical tolerance and error-model limits are collected in \\cref{sec:limits}.')

anchor='Three locally selected natural rock boundaries in the same image provide a scale-matched context.'
replace(anchor,r'''The completed comparison uses 28 retrieved Curiosity images, including 18 whole Mastcam frames measured uniformly and ten captioned geological/context images. A common contour method applies $2\times2$ area averaging, brightness-level contours, and 26 equally spaced samples over a 36.4-native-pixel span. Its target window is selected by proximity to the existing dorsal stations, not minimum RMS. It yields $0.303\px$ RMS, a separate measurement from the full-resolution erf result of $0.2422\px$.

Among 226,426 control windows, 835 ($0.369\%$) are at least as straight; qualifying segments occur in 17 of 18 frames. Straight segments therefore occur in geological scenes. These overlapping photometric windows are correlated and may follow material, fracture, shadow, or shading boundaries; they are not counts of independent rocks. Their fraction is not an origin probability. Smoothing and span change the conditional fraction, so the full sensitivity tables are retained in the supplementary comparison report \cite{comparison2026}.

The conjunction of terminal curvature, transferred geometry, and longitudinal constraint remains the relevant object-level result. The comparison did not estimate the frequency of that complete conjunction. Its automatic rim contour differs from the recorded rim stations by 2.88 pixels on average, preventing a comparable rim ranking; appearance-search scores likewise are not physical-model likelihoods. No full counterpart of the target's 85-station reconstruction was demonstrated by that study. The detailed image inventory, comparison atlas, preprocessing sensitivity, and appearance retrievals remain supplementary material.

Three locally selected natural rock boundaries in the same image provide secondary context.''')
replace('This demonstrates anomalous local image morphology; the three contextual rocks are not an exhaustive statistical representation of all Martian geological structures.', 'This describes the three selected local boundaries; the completed comparison above supplies the broader measured context.')
section('\\section{Geological and Manufactured-Origin Interpretations}', '\\section{Reproducibility and Data Availability}', r'''\section{Geometric Implications and Scope}
\label{sec:discussion}

The evidence is cumulative. The front rim constrains the section; the exposed rear curve tests transferred curvature; and the measured dorsal boundary constrains orientation and exterior tangency. The six-parameter model imposes these relations jointly. Sparse registration and guarded holdouts add evidence beyond a fitted overlay: untrained rear stations continue to follow the frozen shape with approximately $0.2$--$0.24\px$ RMS. A straight sedimentary edge alone is not the identifying result.

Constant-section engineered elements possess the geometric relations tested here. The measured configuration therefore exhibits manufacturing-like geometric regularity, with predictive support rather than visual resemblance alone. The completed geological comparison has not demonstrated a natural analogue reproducing the measured conjunction. Neither naming abrasion, fracture, concretion, or sediment fluidization nor pointing to a straight edge supplies a quantitative explanation of this configuration. Those processes remain documented geological context \cite{bridges2014,loope2011,rubin2017,chan2004,wiens2017}; this study does not require eliminating every conceivable natural process. Manufacture is a morphologically motivated hypothesis, while determining origin is beyond the present scope.

\subsection{Measurement and interpretation limits}
\label{sec:limits}

The validation is retrospective and uses selected coordinates from one acquisition. Neighboring samples share optical and interpolation information, even with coordinate-level guard bands. The nominal reduced chi-square of 33.59 signals an inadequate error/model description; correlation, underestimated localization errors, and model discrepancy are possible contributors, not separately measured explanations. No calibrated origin odds, coverage-calibrated joint confidence interval, or model ranking follows from those nominal weights. Model-specific Birge rescaling is not a common likelihood or a fitted spatial covariance.

The partial terminal arcs constrain visible boundaries rather than both complete hidden end faces. The shared cylindrical model is a constrained image-plane representation, not a unique three-dimensional reconstruction. Focus-based range and receiving-plane assumptions are conditional. Pixel-to-micrometer conversions quantify projected residual distances at an assumed range, not independently measured machining tolerance or surface roughness. The present photometry ($z=0.95$) does not independently establish curved shading.

The comparison study measures photometric features, not a population frequency of the full geometry. Its appearance and straightness rankings cannot be converted into probabilities of natural or manufactured origin. Composition, provenance, and a unique concealed shape remain undetermined. Additional observations could address them, but they are not prerequisites for reporting the measured predictive consistency.
''')
section('The complete source archive and machine-readable numerical outputs', '\\section{Conclusion}', r'''The source images, analysis scripts, and numerical outputs are retained in \repo. The original reconstruction base is commit \texttt{90fbf8f89ac2634a9dbd2b27f81fc80d68b9943c} (11 November 2026). The present 13 November revision additionally incorporates the predictive validation, completed comparison, and audit corrections. The old base commit alone does not contain this complete revision.

\begin{lstlisting}[language=bash,caption={Reproduction from the repository root; no additional image acquisition is required.}]
python -m pip install -r audit/comparative-study/requirements.txt
python audit/predictive-validation/run_validation.py
python -m unittest discover -s audit/comparative-study/scripts -p test_analysis.py -v
python papers/build_paper_evidence.py
cd papers
xelatex -interaction=nonstopmode -halt-on-error martian-cylinder-technical-paper.tex
xelatex -interaction=nonstopmode -halt-on-error martian-cylinder-technical-paper.tex
\end{lstlisting}

The original reconstruction can separately be reproduced with \sourcepath{independent-reconstruction/run_all.py}. Primary outputs include \sourcepath{step3_features.json} (stations), \sourcepath{step8_pebble_and_rear_terminus.json} (front/rear definitions), and \sourcepath{step9_joint_model.json} (joint fits and scale profiles). Predictive folds, fitted parameters, residuals, convergence diagnostics, and input hashes are in \sourcepath{audit/predictive-validation/results.json}. The fixed comparison corpus and its summaries are under \sourcepath{audit/comparative-study/}; no new geological sampling accompanies this revision.

The accompanying \sourcepath{papers/paper-evidence-manifest.json} identifies exact SHA-256 hashes of the manuscript, scripts, numerical inputs, protocols, and comparison records used for the added results. \Cref{app:revision} reproduces the principal hashes. This manifest identifies the working revision without inventing a new committed snapshot or backdating later tests. The figure/data build checks these records and generates the predictive table values directly from JSON.
''')
section('Physically directed subpixel measurements of the sol-3556', '\\section*{Acknowledgment and provenance note}', r'''Physically directed subpixel measurements yield three mutually constraining features: a 35-point near rim, a 24-point exposed far termination, and a 26-point dorsal boundary. Their strict common-axis, common-section, tangent-boundary model fits all 85 observations at $0.3788\px$ RMS. More decisively, the frozen front/dorsal-derived shape predicts eighteen rear stations after six-anchor registration at $\SparseRearRMS\px$ RMS, and guarded rear holdouts at $\BlockedRearRMS\px$. Guarded spatial prediction across all three feature families yields $\BlockedJointRMS\px$. The tested M4 formulation fails its own physical tangency condition.

The measured configuration exhibits manufacturing-like geometric regularity, supported by frozen-shape transfer and heldout prediction. The completed geological comparison has not demonstrated a natural analogue reproducing the measured conjunction. These findings establish a quantitative morphological anomaly and motivate manufacture as a hypothesis; they do not determine composition or provenance.
''')
replace('\\end{thebibliography}', r'''\bibitem{ward2025} Ward, J. (2025). Cylindrical Object in Colour (Sol 3556), 23 October. \url{https://megalithicmars.com/2025/10/23/rover-curiosity-cylindrical-object-in-colour-sol-3556/}.
\bibitem{miltoid2025} MILTOID (2025). VFX Artist Reacts -- Ancient Artefact on Mars, 23 October. Video; image decoding and visual cylinder overlay. \url{https://www.youtube.com/watch?v=xpr8cWDRTO8}.
\bibitem{bogner2026deposit} Bogner, J. (2026). Morphological and Photometric Analysis of an Unidentified Cylindrical Feature in Curiosity Sol 3556 Mastcam Imagery. Zenodo v1.0.0, published 30 October. \url{https://doi.org/10.5281/zenodo.23789092}.
\bibitem{comparison2026} Bogner, J. (2026). Curiosity geological comparison study, 13 November. Supplementary report, image manifest, and numerical exports, \sourcepath{audit/comparative-study/report.md}, accompanying this paper's evidence manifest.
\bibitem{wiens2017} Wiens, R. C., et al. (2017). Centimeter to decimeter hollow concretions and voids in Gale Crater sediments, Mars. \emph{Icarus}. \url{https://doi.org/10.1016/j.icarus.2017.02.003}.
\end{thebibliography}''')
replace("The paper's cited commit freezes the interpretation and the accompanying JSON values used here. Updated repository commits should be treated as new versions of the research record, not silently substituted for this snapshot in reproducing numerical tables.", "The original base revision and this paper's evidence manifest serve different roles: the base identifies the reconstruction history; the manifest identifies the exact files used in the current synthesis. Later replacements should be recorded as new revisions.")
replace('\\end{document}',r'''\section{Evidence Manifest for the 13 November Revision}
\label{app:revision}
\input{paper-evidence-hashes.tex}
\end{document}''')
p.write_text(t,encoding='utf-8')
print('Updated manuscript and relocation-dependent comparison paths.')
