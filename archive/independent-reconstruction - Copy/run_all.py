"""
Master Reproducible Execution Pipeline (`run_all.py`)
Independent Geometric Investigation: Curiosity Sol 3556 (3556MR1025170721700585C00)

Executes all 6 analytical steps in sequence from the primary NASA PDS3 imagery and labels:
  - step1_image_inspection.py: Provenance, SHA-256 verification, radiometric calibration, target localization
  - step2_camera_geometry.py: CAHVOR/CAHV camera intrinsics, SITE_FRAME extrinsics, solar geometry, scale bounds
  - step3_feature_extraction.py: Subpixel edge localization (Erf ODR & Parabolic Gradient), PSF & noise model
  - step4_endface_and_conic_models.py: Conic & polygonal ODR fits, AICc/BIC selection, partial-arc degeneracy
  - step5_competing_3d_interpretations.py: Projective foreshortening theorem, 3D model comparison, clinometry, shadow rays
  - step7_pebble_and_rear_terminus_inspection.py: Zoomed radiometric inspection of adjacent pebble & rear terminus
  - step8_pebble_correction_and_rear_terminus.py: Single pebble outlier exclusion & rear-vs-front curvature comparison
  - step6_robustness_and_sensitivity.py: Perturbation analyses & compilation of `measurements.json`
"""

import step1_image_inspection
import step2_camera_geometry
import step3_feature_extraction
import step4_endface_and_conic_models
import step5_competing_3d_interpretations
import step7_pebble_and_rear_terminus_inspection
import step8_pebble_correction_and_rear_terminus
import step6_robustness_and_sensitivity

def main():
    print("=== [1/8] Running Step 1: Image Provenance & Target Localization ===")
    step1_image_inspection.main()
    print("=== [2/8] Running Step 2: Camera & Illumination Geometry ===")
    step2_camera_geometry.main()
    print("=== [3/8] Running Step 3: Subpixel Feature Extraction ===")
    step3_feature_extraction.main()
    print("=== [4/8] Running Step 4: End-Face Conic & Alternative Models ===")
    step4_endface_and_conic_models.main()
    print("=== [5/8] Running Step 5: Competing 3D Interpretations & Photometry ===")
    step5_competing_3d_interpretations.main()
    print("=== [6/8] Running Step 7: Pebble & Rear Terminus Radiometric Inspection ===")
    step7_pebble_and_rear_terminus_inspection.main()
    print("=== [7/8] Running Step 8: Pebble Outlier Correction & Rear Terminus Analysis ===")
    step8_pebble_correction_and_rear_terminus.main()
    print("=== [8/8] Running Step 6: Robustness Testing & Master Compilation ===")
    step6_robustness_and_sensitivity.main()
    print("=== All steps completed successfully. Outputs saved in independent-reconstruction/ ===")

if __name__ == "__main__":
    main()

