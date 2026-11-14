# Target-only predictive geometry checks

This is a retrospective validation of the existing feature coordinates, not a new blind image selection or geological survey. Use the existing clean front rim (35 stations), exposed rear arc (24 stations), and dorsal boundary (26 stations), with no new exclusions or station tuning.

Before running, define these checks:

1. Reproduce the established unchanged-front-ellipse rear registration. Freeze ellipse size and orientation from the front/dorsal analysis. Fit only two rear translation parameters.
2. Register that same frozen ellipse using six rear stations, spaced at indices 0, 4, 8, 12, 16, 20. Predict the other eighteen stations without further fitting.
3. Five spatially contiguous rear-arc holdouts. Omit each block in turn, plus two neighboring stations at each boundary from training. Freeze the front-derived ellipse. Fit rear translation to remaining rear stations and predict the omitted block. Guard stations are neither trained nor scored in that fold.
4. Five strict-cylinder holdouts. Divide each feature family into five contiguous blocks. In each fold withhold one block from all three families, and exclude two guard stations around each block from training. Fit the same six-parameter M1 model to remaining points and predict withheld coordinates. Score every point exactly once across folds.
5. Withhold the entire dorsal family. Fit M1 to front and rear points only, then evaluate its prescribed tangent silhouette against all 26 dorsal stations. Report this distinct, stronger cross-feature test whether it succeeds or fails.

For M1 use the existing station weights and parameter bounds, with three fixed starting angles (28, 31.2, 35 degrees). Pick the smallest training objective, never the heldout score. Check convergence and boundary hits. Report raw pixel residuals and parameter stability, not nominal significance under an uncalibrated independent-noise assumption. Retain all outcomes.

The two translation parameters are registration, not a prediction of the rear's absolute position. Predictions concern heldout curve locations after registration and the transfer of fixed size/orientation. A cylinder's unknown length cannot be inferred from an isolated front ellipse and an indefinitely extended dorsal line.
