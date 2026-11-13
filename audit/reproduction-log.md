# Argon Audit: Reproduction Log

**Date:** 2026-11-12 17:25:37
**Python:** 3.12.7
**Platform:** Windows AMD64
**Command:** `run_all.py`
**Working Directory:** `independent-reconstruction/`
**Exit Code:** 0
**Runtime:** 136.91 seconds

## 1. Reproduction Status

| Output Artifact | Pre-Run SHA256 | Post-Run SHA256 | Bit-for-Bit Deterministic? | Numerical Equivalence |
| :--- | :--- | :--- | :---: | :---: |
| `step1_provenance.json` | `53335febd758` | `53335febd758` | Yes | Identical |
| `step2_camera_geometry.json` | `32becdb5200f` | `32becdb5200f` | Yes | Identical |
| `step3_features.json` | `9c18d18e9eb1` | `9c18d18e9eb1` | Yes | Identical |
| `step4_endface_models.json` | `fbc2a8d080b6` | `fbc2a8d080b6` | Yes | Identical |
| `step5_3d_interpretations.json` | `8d78344e3b93` | `8d78344e3b93` | Yes | Identical |
| `step8_pebble_and_rear_terminus.json` | `38a1845a6989` | `38a1845a6989` | Yes | Identical |
| `step9_joint_model.json` | `791bcbf5a632` | `791bcbf5a632` | Yes | Identical |
| `measurements.json` | `3587bbed4ede` | `3587bbed4ede` | Yes | Identical |

## 2. Numerical Differences / Drift Detail

All outputs are bit-for-bit identical.

## 3. Standard Output Log

```text
=== [1/9] Running Step 1: Image Provenance & Target Localization ===
Loaded DRXX: shape=(1184, 1328, 3), min=[0, 0, 0], max=[1847, 1391, 981], unique_b0=1711
Loaded DRLX: shape=(1180, 1323, 3), min=[0, 0, 0], max=[4096, 4096, 4096], unique_b0=1749
Loaded DRCX: shape=(1184, 1328, 3), min=[0, 0, 0], max=[255, 209, 197], unique_b0=238
Loaded DRCL: shape=(1180, 1323, 3), min=[0, 0, 0], max=[255, 255, 255], unique_b0=252
DRLX vs DRXX shift at target: dx=-3, dy=-3, corr=0.997762
=== [2/9] Running Step 2: Camera & Illumination Geometry ===
Camera Geometry Summary:
{
  "intrinsics_drxx_cahvor": {
    "hc_px": 699.4411557163015,
    "vc_px": 518.2928025339925,
    "hs_px": 13376.270297745015,
    "vs_px": 13370.534941022059,
    "aspect_ratio_vs_over_hs": 0.9995712290051493,
    "skew_deg": -0.000560393955396421,
    "computed_hfov_deg": 5.683676228470687,
    "computed_vfov_deg": 5.0703973468960815,
    "ifov_h_urad_per_px": 74.7592548401613,
    "ifov_v_urad_per_px": 74.79132319021178
  },
  "intrinsics_drlx_cahv": {
    "hc_px": 673.4326400448685,
    "vc_px": 590.1942945380215,
    "hs_px": 13593.659913478772,
    "vs_px": 13593.664393295123,
    "aspect_ratio_vs_over_hs": 1.0000003295518924,
    "skew_deg": 1.253066699291594e-07,
    "computed_hfov_deg": 5.571903934364932,
    "computed_vfov_deg": 4.970448895156711,
    "ifov_h_urad_per_px": 73.56370590148806,
    "ifov_v_urad_per_px": 73.56368165843755
  },
  "extrinsics_verification": {
    "pds_fixed_instrument_azimuth_deg": 227.7412,
    "computed_drxx_axis_azimuth_deg": 227.9046,
    "computed_drlx_axis_azimuth_deg": 227.7412,
    "pds_fixed_instrument_elevation_deg": -22.0047,
    "computed_drxx_axis_elevation_deg": -21.6775,
    "computed_drlx_axis_elevation_deg": -22.0047,
    "rover_tilt_deg_in_site_frame": 14.8444,
    "camera_center_rover_nav_m": [
      0.6840714,
      0.6478303,
      -1.926771
    ],
    "camera_center_site_m": [
      -135.4634797462946,
      86.02133077555936,
      -22.610372316488032
    ],
    "camera_height_above_rover_origin_site_m": 2.101385316488031
  },
  "target_viewing_geometry": {
    "target_pixel_drxx": [
      1061.0,
      980.0
    ],
    "target_ray_rover_nav": [
      -0.0292234582072538,
      0.8397685559590904,
      0.5421575065539469
    ],
    "target_ray_site": [
      -0.5990075964568599,
      -0.6902091275157964,
      0.40595721410126184
    ],
    "target_azimuth_site_deg": 229.0465,
    "target_elevation_site_deg": -23.9511,
    "grazing_angle_wrt_horizontal_deg": 23.9511,
    "off_axis_angle_from_A_deg": 2.5054,
    "off_axis_angle_from_O_deg": 2.3907,
    "local_jacobian_singular_values_px_per_rad": [
      13498.242607935814,
      13418.427913239595
    ],
    "local_anisotropy_ratio_s1_over_s2": 1.005948,
    "local_anisotropy_percent": 0.5948,
    "mean_local_scale_px_per_rad": 13458.276,
    "mean_local_ifov_urad_per_px": 74.304
  },
  "solar_illumination_geometry": {
    "solar_azimuth_site_deg": 186.8169,
    "solar_elevation_site_deg": 69.8224,
    "sun_direction_site": [
      -0.3424927876065054,
      -0.040942254271253406,
      -0.9386279466608232
    ],
    "sun_direction_rover_nav": [
      0.43816568091540953,
      0.36871309605821934,
      -0.8197935647851217
    ],
    "sun_direction_camera_xyz": [
      -0.44484,
      -0.88943,
      -0.10512
    ],
    "sun_direction_image_plane_angle_deg": -116.571,
    "shadow_cast_image_plane_angle_deg": 63.429,
    "solar_phase_angle_at_target_deg": 81.51
  },
  "distance_and_spatial_scale_bounds": {
    "min_focus_3.600m": {
      "distance_m": 3.6,
      "mm_per_pixel_at_target": 0.26749,
      "mm_per_pixel_paraxial": 0.26913
    },
    "best_focus_3.957m": {
      "distance_m": 3.957,
      "mm_per_pixel_at_target": 0.29402,
      "mm_per_pixel_paraxial": 0.29582
    },
    "max_focus_4.400m": {
      "distance_m": 4.4,
      "mm_per_pixel_at_target": 0.32694,
      "mm_per_pixel_paraxial": 0.32894
    },
    "horiz_plane_zsite_rover_origin": {
      "distance_m": 5.1764,
      "mm_per_pixel_at_target": 0.38462,
      "mm_per_pixel_paraxial": 0.38698
    },
    "rover_nav_plane_z0": {
      "distance_m": 3.5539,
      "mm_per_pixel_at_target": 0.26407,
      "mm_per_pixel_paraxial": 0.26569
    }
  }
}
=== [3/9] Running Step 3: Subpixel Feature Extraction ===
Step 3 Refined Summary:
{
  "dorsal_theta_deg": 28.894753769405032,
  "dorsal_theta_unc_deg": 0.34804368148200576,
  "dorsal_rms_px": 0.2422363875153055,
  "dorsal_max_res_px": 0.618430638944079,
  "dorsal_curvature_z": 1.920706368787201,
  "dorsal_sagitta_px": 0.28014981795372956,
  "ventral_full_theta_deg": 63.90552281497027,
  "ventral_full_theta_unc_deg": 0.16812240502277198,
  "ventral_full_rms_px": 0.1872560322184402,
  "ventral_clean_theta_deg": 63.82457121364896,
  "ventral_clean_rms_px": 0.19588567223468736,
  "convergence_angle_full_deg": 35.01076904556524,
  "convergence_angle_clean_deg": 34.92981744424392,
  "convergence_angle_grad_deg": 35.12919160502254,
  "bisector_angle_full_deg": 46.40013829218765,
  "apex_xy_full": [
    1022.9658048520596,
    937.5093041342793
  ],
  "apex_xy_clean": [
    1022.899076281815,
    937.4724759559351
  ],
  "drlx_convergence_angle_deg": 35.32224137966545,
  "drlx_dorsal_rms_px": 0.23992858826652413,
  "drlx_ventral_rms_px": 0.14764232672037372
}
=== [4/9] Running Step 4: End-Face Conic & Alternative Models ===
Step 4 Model Comparison Summary:
{
  "S1_Strict_Proximal_Arch_140deg": {
    "M1_Circle_3DOF": {
      "n_points": 29,
      "k_params": 3,
      "dof": 26,
      "rms_residual_px": 0.2193,
      "max_residual_px": 0.6157,
      "chi2": 72.32,
      "reduced_chi2": 2.7815,
      "AIC": 78.32,
      "AICc": 79.28,
      "BIC": 82.422,
      "params": {
        "xc": 1072.861653969438,
        "yc": 988.547423364079,
        "R": 21.285017329105855,
        "a": 21.285017329105855,
        "b": 21.285017329105855,
        "b_over_a": 1.0,
        "tilt_deg": 0.0
      }
    },
    "M2_Ellipse_Bisector_Constrained_4DOF": {
      "n_points": 29,
      "k_params": 4,
      "dof": 25,
      "rms_residual_px": 0.1591,
      "max_residual_px": 0.3048,
      "chi2": 39.287,
      "reduced_chi2": 1.5715,
      "AIC": 47.287,
      "AICc": 48.954,
      "BIC": 52.756,
      "params": {
        "xc": 1067.3332729669496,
        "yc": 982.7454648043273,
        "a_perp_axis": 17.924044615204497,
        "b_along_axis": 13.143007854753082,
        "semi_major": 17.924044615204497,
        "semi_minor": 13.143007854753082,
        "b_along_over_a_perp": 0.7332612776250408,
        "b_over_a": 0.7332612776250408,
        "fixed_axis_deg": 46.40013829218765,
        "effective_minor_axis_deg": 46.40013829218765,
        "implied_circular_tilt_deg": 42.83950019231044
      }
    },
    "M3_Ellipse_Dorsal_Constrained_4DOF": {
      "n_points": 29,
      "k_params": 4,
      "dof": 25,
      "rms_residual_px": 0.1213,
      "max_residual_px": 0.2466,
      "chi2": 23.126,
      "reduced_chi2": 0.925,
      "AIC": 31.126,
      "AICc": 32.792,
      "BIC": 36.595,
      "params": {
        "xc": 1068.7481072297037,
        "yc": 986.3324763951753,
        "a_perp_axis": 19.8555045239652,
        "b_along_axis": 16.460151226100947,
        "semi_major": 19.8555045239652,
        "semi_minor": 16.460151226100947,
        "b_along_over_a_perp": 0.8289968762180719,
        "b_over_a": 0.8289968762180719,
        "fixed_axis_deg": 28.894753769405032,
        "effective_minor_axis_deg": 28.894753769405032,
        "implied_circular_tilt_deg": 34.00416958541288
      }
    },
    "M4_Ellipse_Free_5DOF": {
      "n_points": 29,
      "k_params": 5,
      "dof": 24,
      "rms_residual_px": 0.1053,
      "max_residual_px": 0.1892,
      "chi2": 17.156,
      "reduced_chi2": 0.7148,
      "AIC": 27.156,
      "AICc": 29.765,
      "BIC": 33.993,
      "params": {
        "xc": 1067.1630275105188,
        "yc": 983.7667292253556,
        "semi_major": 18.309510171866094,
        "semi_minor": 13.697974259828612,
        "b_over_a": 0.748134391977157,
        "minor_axis_deg": 39.119342982041424,
        "major_axis_deg": 129.11934298204142,
        "implied_circular_tilt_deg": 41.570969430676186
      }
    },
    "M5_Parabolic_Arch_4DOF": {
      "n_points": 29,
      "k_params": 4,
      "dof": 25,
      "rms_residual_px": 0.2956,
      "max_residual_px": 0.6927,
      "chi2": 133.782,
      "reduced_chi2": 5.3513,
      "AIC": 141.782,
      "AICc": 143.448,
      "BIC": 147.251,
      "params": {
        "vertex_x": 1060.5510615820126,
        "vertex_y": 970.942490497874,
        "curvature_c2_px_inv": 0.028939569890140456,
        "vertex_radius_of_curvature_px": 17.277381864971915,
        "axis_angle_deg": 54.616576606276475
      }
    },
    "M6a_Angular_2Facet_Rim_4DOF": {
      "n_points": 29,
      "k_params": 4,
      "dof": 25,
      "rms_residual_px": 0.8873,
      "max_residual_px": 2.3649,
      "chi2": 1194.096,
      "reduced_chi2": 47.7638,
      "AIC": 1202.096,
      "AICc": 1203.762,
      "BIC": 1207.565,
      "params": {
        "vertices_xy": [
          [
            1049.8657627415955,
            991.6533137775017
          ],
          [
            1057.3103678274365,
            971.734202377557
          ],
          [
            1076.60862488323,
            966.0107107648244
          ]
        ],
        "n_segments": 2
      }
    },
    "M6b_Angular_3Facet_Rim_6DOF": {
      "n_points": 29,
      "k_params": 6,
      "dof": 23,
      "rms_residual_px": 0.3991,
      "max_residual_px": 0.9445,
      "chi2": 243.843,
      "reduced_chi2": 10.6019,
      "AIC": 255.843,
      "AICc": 259.661,
      "BIC": 264.046,
      "params": {
        "vertices_xy": [
          [
            1051.075796603779,
            990.7466028336987
          ],
          [
            1053.5951688740493,
            978.0528247940489
          ],
          [
            1064.1767588485511,
            968.0354992468634
          ],
          [
            1080.948877022874,
            967.1834344486641
          ]
        ],
        "n_segments": 3
      }
    }
  },
  "S2_Full_Proximal_Rim_160deg": {
    "M1_Circle_3DOF": {
      "n_points": 33,
      "k_params": 3,
      "dof": 30,
      "rms_residual_px": 0.2685,
      "max_residual_px": 0.7099,
      "chi2": 109.462,
      "reduced_chi2": 3.6487,
      "AIC": 115.462,
      "AICc": 116.29,
      "BIC": 119.952,
      "params": {
        "xc": 1072.5686019533682,
        "yc": 988.4290263390867,
        "R": 21.02175651094437,
        "a": 21.02175651094437,
        "b": 21.02175651094437,
        "b_over_a": 1.0,
        "tilt_deg": 0.0
      }
    },
    "M2_Ellipse_Bisector_Constrained_4DOF": {
      "n_points": 33,
      "k_params": 4,
      "dof": 29,
      "rms_residual_px": 0.2592,
      "max_residual_px": 1.0609,
      "chi2": 92.926,
      "reduced_chi2": 3.2044,
      "AIC": 100.926,
      "AICc": 102.355,
      "BIC": 106.912,
      "params": {
        "xc": 1068.7365155106008,
        "yc": 984.3709196304956,
        "a_perp_axis": 18.945722246506644,
        "b_along_axis": 15.315885663742124,
        "semi_major": 18.945722246506644,
        "semi_minor": 15.315885663742124,
        "b_along_over_a_perp": 0.808408645733534,
        "b_over_a": 0.808408645733534,
        "fixed_axis_deg": 46.40013829218765,
        "effective_minor_axis_deg": 46.40013829218765,
        "implied_circular_tilt_deg": 36.05925807827502
      }
    },
    "M3_Ellipse_Dorsal_Constrained_4DOF": {
      "n_points": 33,
      "k_params": 4,
      "dof": 29,
      "rms_residual_px": 0.1596,
      "max_residual_px": 0.4218,
      "chi2": 35.24,
      "reduced_chi2": 1.2152,
      "AIC": 43.24,
      "AICc": 44.668,
      "BIC": 49.226,
      "params": {
        "xc": 1069.2788263836183,
        "yc": 986.6428324439906,
        "a_perp_axis": 20.098240056376042,
        "b_along_axis": 17.089229849841562,
        "semi_major": 20.098240056376042,
        "semi_minor": 17.089229849841562,
        "b_along_over_a_perp": 0.8502848907121153,
        "b_over_a": 0.8502848907121153,
        "fixed_axis_deg": 28.894753769405032,
        "effective_minor_axis_deg": 28.894753769405032,
        "implied_circular_tilt_deg": 31.757330804641217
      }
    },
    "M4_Ellipse_Free_5DOF": {
      "n_points": 33,
      "k_params": 5,
      "dof": 28,
      "rms_residual_px": 0.1682,
      "max_residual_px": 0.5002,
      "chi2": 36.983,
      "reduced_chi2": 1.3208,
      "AIC": 46.983,
      "AICc": 49.205,
      "BIC": 54.466,
      "params": {
        "xc": 1068.9083466465436,
        "yc": 986.0314137610835,
        "semi_major": 19.735625213854178,
        "semi_minor": 16.462387982194613,
        "b_over_a": 0.8341457543811791,
        "minor_axis_deg": 32.54489012415719,
        "major_axis_deg": 122.54489012415719,
        "implied_circular_tilt_deg": 33.47300719534175
      }
    },
    "M5_Parabolic_Arch_4DOF": {
      "n_points": 33,
      "k_params": 4,
      "dof": 29,
      "rms_residual_px": 0.3697,
      "max_residual_px": 0.7882,
      "chi2": 216.34,
      "reduced_chi2": 7.46,
      "AIC": 224.34,
      "AICc": 225.769,
      "BIC": 230.326,
      "params": {
        "vertex_x": 1060.7758329082503,
        "vertex_y": 970.6679304400061,
        "curvature_c2_px_inv": 0.030921189687117545,
        "vertex_radius_of_curvature_px": 16.170141092867173,
        "axis_angle_deg": 55.90919445909291
      }
    },
    "M6a_Angular_2Facet_Rim_4DOF": {
      "n_points": 33,
      "k_params": 4,
      "dof": 29,
      "rms_residual_px": 1.1221,
      "max_residual_px": 2.7103,
      "chi2": 1923.312,
      "reduced_chi2": 66.3211,
      "AIC": 1931.312,
      "AICc": 1932.741,
      "BIC": 1937.298,
      "params": {
        "vertices_xy": [
          [
            1049.4412426562512,
            994.0644728409982
          ],
          [
            1057.9480439054755,
            970.3573229478142
          ],
          [
            1084.0050932224242,
            966.1919668860078
          ]
        ],
        "n_segments": 2
      }
    },
    "M6b_Angular_3Facet_Rim_6DOF": {
      "n_points": 33,
      "k_params": 6,
      "dof": 27,
      "rms_residual_px": 0.4426,
      "max_residual_px": 0.974,
      "chi2": 309.186,
      "reduced_chi2": 11.4513,
      "AIC": 321.186,
      "AICc": 324.417,
      "BIC": 330.165,
      "params": {
        "vertices_xy": [
          [
            1051.011482771462,
            994.104637415694
          ],
          [
            1053.140900355085,
            978.4726012426754
          ],
          [
            1065.4221700866335,
            967.2254066201849
          ],
          [
            1086.5127389749111,
            969.0321117310831
          ]
        ],
        "n_segments": 3
      }
    }
  },
  "S3_Lobe_Excluded_250deg": {
    "M1_Circle_3DOF": {
      "n_points": 50,
      "k_params": 3,
      "dof": 47,
      "rms_residual_px": 1.5598,
      "max_residual_px": 6.3412,
      "chi2": 4045.108,
      "reduced_chi2": 86.0661,
      "AIC": 4051.108,
      "AICc": 4051.63,
      "BIC": 4056.845,
      "params": {
        "xc": 1070.7173492988024,
        "yc": 986.8185095176437,
        "R": 19.152842043486764,
        "a": 19.152842043486764,
        "b": 19.152842043486764,
        "b_over_a": 1.0,
        "tilt_deg": 0.0
      }
    },
    "M2_Ellipse_Bisector_Constrained_4DOF": {
      "n_points": 50,
      "k_params": 4,
      "dof": 46,
      "rms_residual_px": 0.9307,
      "max_residual_px": 4.5371,
      "chi2": 1242.081,
      "reduced_chi2": 27.0018,
      "AIC": 1250.081,
      "AICc": 1250.97,
      "BIC": 1257.729,
      "params": {
        "xc": 1069.0540070004788,
        "yc": 985.6578819931378,
        "a_perp_axis": 20.317411610695107,
        "b_along_axis": 16.227484361190264,
        "semi_major": 20.317411610695107,
        "semi_minor": 16.227484361190264,
        "b_along_over_a_perp": 0.7986984106109313,
        "b_over_a": 0.7986984106109313,
        "fixed_axis_deg": 46.40013829218765,
        "effective_minor_axis_deg": 46.40013829218765,
        "implied_circular_tilt_deg": 36.99401113853685
      }
    },
    "M3_Ellipse_Dorsal_Constrained_4DOF": {
      "n_points": 50,
      "k_params": 4,
      "dof": 46,
      "rms_residual_px": 0.9927,
      "max_residual_px": 4.8089,
      "chi2": 1399.752,
      "reduced_chi2": 30.4294,
      "AIC": 1407.752,
      "AICc": 1408.641,
      "BIC": 1415.401,
      "params": {
        "xc": 1067.941348280296,
        "yc": 985.5507970487046,
        "a_perp_axis": 20.084363890438823,
        "b_along_axis": 15.20075092822421,
        "semi_major": 20.084363890438823,
        "semi_minor": 15.20075092822421,
        "b_along_over_a_perp": 0.7568450268649305,
        "b_over_a": 0.7568450268649305,
        "fixed_axis_deg": 28.894753769405032,
        "effective_minor_axis_deg": 28.894753769405032,
        "implied_circular_tilt_deg": 40.81315366143416
      }
    },
    "M4_Ellipse_Free_5DOF": {
      "n_points": 50,
      "k_params": 5,
      "dof": 45,
      "rms_residual_px": 0.8223,
      "max_residual_px": 4.3147,
      "chi2": 832.201,
      "reduced_chi2": 18.4934,
      "AIC": 842.201,
      "AICc": 843.565,
      "BIC": 851.761,
      "params": {
        "xc": 1068.162346210361,
        "yc": 985.4567590855645,
        "semi_major": 20.30991683454377,
        "semi_minor": 15.303848810056406,
        "b_over_a": 0.7535160746708288,
        "minor_axis_deg": 37.02277024323413,
        "major_axis_deg": 127.02277024323413,
        "implied_circular_tilt_deg": 41.104123959218015
      }
    }
  },
  "S4_Full_360deg_Dark_Patch": {
    "M1_Circle_3DOF": {
      "n_points": 72,
      "k_params": 3,
      "dof": 69,
      "rms_residual_px": 1.7826,
      "max_residual_px": 6.4795,
      "chi2": 6875.231,
      "reduced_chi2": 99.641,
      "AIC": 6881.231,
      "AICc": 6881.583,
      "BIC": 6888.061,
      "params": {
        "xc": 1069.9159609722622,
        "yc": 986.4545746644314,
        "R": 18.54112440769722,
        "a": 18.54112440769722,
        "b": 18.54112440769722,
        "b_over_a": 1.0,
        "tilt_deg": 0.0
      }
    },
    "M2_Ellipse_Bisector_Constrained_4DOF": {
      "n_points": 72,
      "k_params": 4,
      "dof": 68,
      "rms_residual_px": 1.721,
      "max_residual_px": 5.3033,
      "chi2": 5243.55,
      "reduced_chi2": 77.111,
      "AIC": 5251.55,
      "AICc": 5252.147,
      "BIC": 5260.657,
      "params": {
        "xc": 1069.6254677905872,
        "yc": 986.3375177340865,
        "a_perp_axis": 19.601735423875006,
        "b_along_axis": 17.50924616458199,
        "semi_major": 19.601735423875006,
        "semi_minor": 17.50924616458199,
        "b_along_over_a_perp": 0.893249795793879,
        "b_over_a": 0.893249795793879,
        "fixed_axis_deg": 46.40013829218765,
        "effective_minor_axis_deg": 46.40013829218765,
        "implied_circular_tilt_deg": 26.71550093780634
      }
    },
    "M3_Ellipse_Dorsal_Constrained_4DOF": {
      "n_points": 72,
      "k_params": 4,
      "dof": 68,
      "rms_residual_px": 1.8245,
      "max_residual_px": 5.7488,
      "chi2": 5603.941,
      "reduced_chi2": 82.4109,
      "AIC": 5611.941,
      "AICc": 5612.538,
      "BIC": 5621.047,
      "params": {
        "xc": 1069.5999950286355,
        "yc": 986.319569551989,
        "a_perp_axis": 19.530513256329424,
        "b_along_axis": 17.498053130445673,
        "semi_major": 19.530513256329424,
        "semi_minor": 17.498053130445673,
        "b_along_over_a_perp": 0.8959341160568284,
        "b_over_a": 0.8959341160568284,
        "fixed_axis_deg": 28.894753769405032,
        "effective_minor_axis_deg": 28.894753769405032,
        "implied_circular_tilt_deg": 26.37133273578131
      }
    },
    "M4_Ellipse_Free_5DOF": {
      "n_points": 72,
      "k_params": 5,
      "dof": 67,
      "rms_residual_px": 1.7595,
      "max_residual_px": 5.3562,
      "chi2": 5215.686,
      "reduced_chi2": 77.8461,
      "AIC": 5225.686,
      "AICc": 5226.595,
      "BIC": 5237.069,
      "params": {
        "xc": 1069.5840900623787,
        "yc": 986.3171104827188,
        "semi_major": 19.640924306003303,
        "semi_minor": 17.44144125400836,
        "b_over_a": 0.8880152981739936,
        "minor_axis_deg": 40.04892905670792,
        "major_axis_deg": 130.04892905670792,
        "implied_circular_tilt_deg": 27.375099994205996
      }
    }
  }
}
Bootstrap Uncertainties:
{
  "S2_Full_Proximal_Rim_160deg": {
    "b_over_a_mean": 0.822552241648604,
    "b_over_a_std": 0.03748351075922594,
    "b_over_a_ci95": [
      0.7301334768766655,
      0.8839807333664622
    ],
    "tilt_deg_mean": 34.478762921783336,
    "tilt_deg_std": 3.7745875099068655,
    "tilt_deg_ci95": [
      27.873637874934445,
      43.10241466827519
    ],
    "minor_axis_deg_mean": 32.17152573857693,
    "minor_axis_deg_std": 6.3731141501124045,
    "semi_major_px_mean": 19.687189295016285,
    "semi_major_px_std": 0.7528598644132223,
    "semi_minor_px_mean": 16.217639806215026,
    "semi_minor_px_std": 1.299414681885553
  },
  "S3_Lobe_Excluded_250deg": {
    "b_over_a_mean": 0.7521626322352064,
    "b_over_a_std": 0.019439547525205356,
    "b_over_a_ci95": [
      0.7208400715419147,
      0.795724428222889
    ],
    "tilt_deg_mean": 41.192436428330566,
    "tilt_deg_std": 1.7147482597477413,
    "tilt_deg_ci95": [
      37.27622458830588,
      43.876118079496045
    ],
    "minor_axis_deg_mean": 36.56401904219261,
    "minor_axis_deg_std": 2.438594275574697,
    "semi_major_px_mean": 20.283030552497113,
    "semi_major_px_std": 0.2803346527542645,
    "semi_minor_px_mean": 15.253755238392003,
    "semi_minor_px_std": 0.3541328134086828
  },
  "S4_Full_360deg_Dark_Patch": {
    "b_over_a_mean": 0.8857469944906902,
    "b_over_a_std": 0.026053894832004106,
    "b_over_a_ci95": [
      0.8335797820975605,
      0.940335785098283
    ],
    "tilt_deg_mean": 27.474937361340718,
    "tilt_deg_std": 3.2895993484009933,
    "tilt_deg_ci95": [
      19.891949865257214,
      33.531752402740445
    ],
    "minor_axis_deg_mean": 40.72974274164583,
    "minor_axis_deg_std": 5.769142462946337,
    "semi_major_px_mean": 19.672150378568915,
    "semi_major_px_std": 0.2904533733114324,
    "semi_minor_px_mean": 17.41851625859746,
    "semi_minor_px_std": 0.3447097838789884
  }
}
=== [5/9] Running Step 5: Competing 3D Interpretations & Photometry ===
Step 5 Summary:
{
  "perspective_foreshortening_proof": {
    "observed_convergence_deg": 35.011,
    "observed_convergence_unc_deg": 0.387,
    "table_by_tilt_gamma": [
      {
        "axis_tilt_gamma_deg": 0.184,
        "vanishing_point_dist_px": 43.2,
        "predicted_limb_convergence_2alpha_deg": 38.2797,
        "predicted_endface_b_over_a": 0.999995,
        "required_3D_length_to_diameter_ratio": 435.95
      },
      {
        "axis_tilt_gamma_deg": 1.0,
        "vanishing_point_dist_px": 234.9,
        "predicted_limb_convergence_2alpha_deg": 7.3071,
        "predicted_endface_b_over_a": 0.999848,
        "required_3D_length_to_diameter_ratio": 80.22
      },
      {
        "axis_tilt_gamma_deg": 5.0,
        "vanishing_point_dist_px": 1177.4,
        "predicted_limb_convergence_2alpha_deg": 1.4598,
        "predicted_endface_b_over_a": 0.996195,
        "required_3D_length_to_diameter_ratio": 16.06
      },
      {
        "axis_tilt_gamma_deg": 15.0,
        "vanishing_point_dist_px": 3606.1,
        "predicted_limb_convergence_2alpha_deg": 0.4766,
        "predicted_endface_b_over_a": 0.965926,
        "required_3D_length_to_diameter_ratio": 5.41
      },
      {
        "axis_tilt_gamma_deg": 30.0,
        "vanishing_point_dist_px": 7770.1,
        "predicted_limb_convergence_2alpha_deg": 0.2212,
        "predicted_endface_b_over_a": 0.866025,
        "required_3D_length_to_diameter_ratio": 2.8
      },
      {
        "axis_tilt_gamma_deg": 45.0,
        "vanishing_point_dist_px": 13458.3,
        "predicted_limb_convergence_2alpha_deg": 0.1277,
        "predicted_endface_b_over_a": 0.707107,
        "required_3D_length_to_diameter_ratio": 1.98
      },
      {
        "axis_tilt_gamma_deg": 60.0,
        "vanishing_point_dist_px": 23310.4,
        "predicted_limb_convergence_2alpha_deg": 0.0737,
        "predicted_endface_b_over_a": 0.5,
        "required_3D_length_to_diameter_ratio": 1.62
      },
      {
        "axis_tilt_gamma_deg": 75.0,
        "vanishing_point_dist_px": 50227.0,
        "predicted_limb_convergence_2alpha_deg": 0.0342,
        "predicted_endface_b_over_a": 0.258819,
        "required_3D_length_to_diameter_ratio": 1.45
      }
    ],
    "conclusion": "An unburied right circular cylinder at D~4m in Mastcam-100 (f=13458 px) has perspective limb convergence of only 0.08 to 0.35 deg for plausible tilt angles (20-75 deg), ruling out pure perspective foreshortening of parallel cylinder edges at >50 sigma. Convergence of 35.35 deg requires either physical tapering (cone/wedge) or oblique progressive burial in regolith."
  },
  "transverse_photometry_clinometry": {
    "n_total_samples": 145,
    "flat_planar_facet_rms_rel": 0.02682,
    "full_180deg_cylinder_cone_rms_rel": 0.02674,
    "convex_partial_arc_quadratic_rms_rel": 0.02673,
    "quadratic_curvature_coeff_c2": -0.01285,
    "quadratic_curvature_err": 0.01357,
    "convexity_significance_z_sigma": 0.95,
    "peak_brightness_transverse_coord_v_frac": -2.0779,
    "solar_vector_in_object_frame": {
      "s_axial_along_bisector": -0.9509,
      "s_transverse_towards_dorsal": 0.2912,
      "s_outward_towards_camera": 0.1051
    }
  },
  "cast_shadow_verification": {
    "solar_shadow_2d_angle_deg": 63.429,
    "mean_shadow_chord_length_px": 32.3,
    "std_shadow_chord_length_px": 4.71,
    "chords": [
      {
        "arch_x": 1056.1535034790113,
        "arch_y": 975.479158954084,
        "distal_x": 1070.6674514270064,
        "distal_y": 1002.9635096925031,
        "shadow_length_px": 31.073656977538327
      },
      {
        "arch_x": 1057.121671468951,
        "arch_y": 974.6216714689511,
        "distal_x": 1070.6674514270064,
        "distal_y": 1002.9635096925031,
        "shadow_length_px": 31.40750948594631
      },
      {
        "arch_x": 1057.839843242504,
        "arch_y": 973.487473479231,
        "distal_x": 1072.1462803028237,
        "distal_y": 1002.3401541563444,
        "shadow_length_px": 32.20464397895296
      },
      {
        "arch_x": 1058.9204129393656,
        "arch_y": 972.7470798406845,
        "distal_x": 1075.5260740989079,
        "distal_y": 1007.0514573536191,
        "shadow_length_px": 38.108994491859086
      },
      {
        "arch_x": 1059.8451593899076,
        "arch_y": 971.7414271394783,
        "distal_x": 1075.3650614029414,
        "distal_y": 1001.8666786088403,
        "shadow_length_px": 33.88559751341353
      },
      {
        "arch_x": 1061.0150371767434,
        "arch_y": 971.0929523462789,
        "distal_x": 1077.0490158005268,
        "distal_y": 1001.5393805287904,
        "shadow_length_px": 34.40280157222661
      },
      {
        "arch_x": 1062.0657524716116,
        "arch_y": 970.0695276240259,
        "distal_x": 1077.0490158005268,
        "distal_y": 1001.5393805287904,
        "shadow_length_px": 34.84814120919372
      },
      {
        "arch_x": 1063.3322302847857,
        "arch_y": 969.4456716685735,
        "distal_x": 1078.737597313006,
        "distal_y": 1001.0489522031403,
        "shadow_length_px": 35.156286024082306
      },
      {
        "arch_x": 1064.6539476928554,
        "arch_y": 968.85923529281,
        "distal_x": 1083.3675502808796,
        "distal_y": 1003.9102100529077,
        "shadow_length_px": 39.71963251520243
      },
      {
        "arch_x": 1066.02140968154,
        "arch_y": 968.099635325647,
        "distal_x": 1082.0063096496376,
        "distal_y": 999.5063096496376,
        "shadow_length_px": 35.23967404016593
      },
      {
        "arch_x": 1067.5,
        "arch_y": 967.5460943617628,
        "distal_x": 1084.1601329032505,
        "distal_y": 998.9795113744821,
        "shadow_length_px": 35.56562823906455
      },
      {
        "arch_x": 1069.060288273693,
        "arch_y": 967.1658234243048,
        "distal_x": 1084.1601329032505,
        "distal_y": 998.9795113744821,
        "shadow_length_px": 35.2078082249052
      },
      {
        "arch_x": 1070.6469366886947,
        "arch_y": 967.1528351699174,
        "distal_x": 1085.4869922540747,
        "distal_y": 997.5946275660228,
        "shadow_length_px": 33.86460591926
      },
      {
        "arch_x": 1072.2420069190196,
        "arch_y": 967.302589248376,
        "distal_x": 1087.6374712007275,
        "distal_y": 996.6263744185383,
        "shadow_length_px": 33.11311967991411
      },
      {
        "arch_x": 1073.8536544767096,
        "arch_y": 967.5434777942233,
        "distal_x": 1087.6374712007275,
        "distal_y": 996.6263744185383,
        "shadow_length_px": 32.176773239580704
      },
      {
        "arch_x": 1075.495111735735,
        "arch_y": 967.8544275524689,
        "distal_x": 1089.7826211643376,
        "distal_y": 995.3905568926973,
        "shadow_length_px": 31.018679350292278
      },
      {
        "arch_x": 1077.1283213276658,
        "arch_y": 968.3232582688839,
        "distal_x": 1089.7826211643376,
        "distal_y": 995.3905568926973,
        "shadow_length_px": 29.868820982512368
      },
      {
        "arch_x": 1078.7871032711141,
        "arch_y": 968.8803459614661,
        "distal_x": 1091.1377822678987,
        "distal_y": 993.6034491495806,
        "shadow_length_px": 27.636406139717717
      },
      {
        "arch_x": 1080.5098662728478,
        "arch_y": 969.4954451301634,
        "distal_x": 1089.4493306158056,
        "distal_y": 986.9203176008655,
        "shadow_length_px": 19.58315070563726
      },
      {
        "arch_x": 1083.3375713016394,
        "arch_y": 969.1624286983606,
        "distal_x": 1091.9383339866386,
        "distal_y": 989.309137645409,
        "shadow_length_px": 21.866005425285753
      }
    ]
  }
}
=== [6/9] Running Step 7: Pebble & Rear Terminus Radiometric Inspection ===
Saved diag07_pebble_and_rear_terminus_zoom.png
=== [7/9] Running Step 8: Pebble Outlier Correction & Rear Terminus Analysis ===
Step 8 completed successfully.
Front Face (36 pts, incl. theta=-45°): Free Ellipse a=19.52, b/a=0.8194, phi=40.37°, RMS=0.4167 px
Front Face (35 pts, excl. ONLY theta=-45°): Free Ellipse a=19.72, b/a=0.8330, phi=32.70°, RMS=0.1639 px
Front Face (35 pts, Dorsal-Constrained 29.88°): a=20.03, b/a=0.8411, RMS=0.1618 px
Exposed Rear Cap Arc (24 pts, theta=-170°..-55°): 1:1 Unscaled Front-Face Copy RMS=0.1854 px (max=0.3179 px); Scaled Coaxial s=0.9379 RMS=0.1841 px
=== [8/9] Running Step 9: Joint Geometric Model & Collinear Resolution ===
================================================================================
STEP 9: JOINT GEOMETRIC MODELING & COLLINEAR AXIS RESOLUTION
================================================================================
Loaded: Front Rim N = 35, Exposed Rear Arc N = 24, Dorsal Edge N = 26 (Total N = 85)

--- Independent Baseline Measurements ---
Front Free Ellipse Minor Axis: 32.70° (RMS = 0.1639 px)
Measured Dorsal Edge Line:     28.89° (RMS = 0.2422 px)
Center-to-Center Bearing:      33.18° (Baseline L = 39.32 px, Rear RMS = 0.1863 px)
Observed Angular Discrepancy:  +4.29° (Bearing vs Dorsal)
                               +3.81° (Front Minor Axis vs Dorsal)

--- Model 1: Strict Right Circular Cylinder (6 DOF, Tangent Dorsal) ---
Axis Angle: 30.32° | L_proj: 40.86 px | a: 19.99 px, b: 15.74 px (b/a = 0.787)
Front Center: (1068.30, 985.95) | Rear Center: (1033.03, 965.32)
Residuals: Front RMS = 0.2376 px | Rear RMS = 0.4830 px | Dorsal RMS = 0.4217 px | Total RMS = 0.3788 px

--- Model 2: Right Circular Cylinder with Free Dorsal Offset (7 DOF) ---
Axis Angle: 31.10° | L_proj: 40.29 px | a: 20.12 px, b: 16.00 px (b/a = 0.795)
Front Center: (1068.58, 985.98) | Rear Center: (1034.08, 965.17)
Dorsal Crest Offset: 19.25 px (delta_r wrt front semi-major = +0.87 px)
Residuals: Front RMS = 0.2314 px | Rear RMS = 0.3049 px | Dorsal RMS = 0.4851 px | Total RMS = 0.3468 px

--- Model 3: Cylinder-compatible fit with free dorsal offset (7 effective DOF, unweighted) ---
Optimal Axis Angle: 30.60° | L_proj: 40.61 px | a: 20.28 px, b: 16.06 px (b/a = 0.792)
Front Center: (1068.58, 986.12) | Rear Center: (1033.63, 965.45)
Residuals: Front RMS = 0.2422 px | Rear RMS = 0.3784 px | Dorsal RMS = 0.4054 px | Total RMS = 0.3389 px

--- Model 4: Tapered Conical Frustum with Coupled Dorsal Silhouette (8 DOF) ---
Body Axis Angle: 39.33° | Scale Ratio s: 0.619 | Half-Taper Angle alpha: 9.46°
Coupled Dorsal Angle: 29.86° (Observed: 28.89°) | L_proj: 44.14 px
Residuals: Front RMS = 0.1930 px | Rear RMS = 0.2684 px | Dorsal RMS = 0.3096 px | Total RMS = 0.2549 px

--- Scale Ratio Profile Likelihoods ---
Standalone Rear Arc: Best s = 0.930 | 95% CI = [0.870, 0.990]
  Rear RMS at s=1.000: 0.1863 px (Delta wrt min 0.1843 px: 0.0020 px)
  Flatness Delta_RMS across [0.85, 1.15]: 0.0102 px
Joint Coupled Frustum (M4): Best s = 0.619 | 95% CI = [0.610, 0.630]
  Total Joint RMS = 0.2549 px (chi2 = 1044.1, BIC = 1079.6)

Saved machine-readable results to D:\projects\martian-cylinder\independent-reconstruction\step9_joint_model.json
Generated diagnostic figure: D:\projects\martian-cylinder\independent-reconstruction\figures\diag09_joint_geometric_model.png

Step 9 completed successfully.
=== [9/9] Running Step 6: Robustness Testing & Master Compilation ===
Step 6 Robustness & Master Measurements Saved Successfully.
{
  "pixel_dimensions_drxx": {
    "rim_chord_width_px": 35.54,
    "ellipse_major_diameter_S1_px": 36.62,
    "ellipse_major_diameter_S2_px": 39.47,
    "sunlit_axial_length_to_arch_vertex_px": 50.21,
    "dorsal_limb_length_px": 60.66,
    "ventral_limb_length_px": 63.49,
    "apparent_length_to_chord_width_ratio": 1.707,
    "axial_length_to_arch_over_chord_width_ratio": 1.413
  },
  "best_focus_3.957m_mm": {
    "distance_m": 3.957,
    "scale_mm_per_px": 0.29402,
    "rim_chord_width_mm": 10.45,
    "ellipse_major_diameter_S1_mm": 10.77,
    "ellipse_major_diameter_S2_mm": 11.61,
    "sunlit_axial_length_to_arch_mm": 14.76,
    "dorsal_limb_length_mm": 17.84,
    "ventral_limb_length_mm": 18.67
  },
  "product_tests": {
    "DRXX_16bit_Raw_CAHVOR": {
      "dorsal_theta_deg": 29.905,
      "dorsal_rms_px": 0.2603,
      "ventral_theta_deg": 65.356,
      "ventral_rms_px": 0.665,
      "convergence_angle_deg": 35.451,
      "proximal_arch_free_ellipse_b_over_a": 0.8341,
      "proximal_arch_free_ellipse_minor_deg": 32.54,
      "proximal_arch_rms_px": 0.1682
    },
    "DRCX_8bit_Color_CAHVOR": {
      "dorsal_theta_deg": 30.026,
      "dorsal_rms_px": 0.2855,
      "ventral_theta_deg": 65.098,
      "ventral_rms_px": 0.6383,
      "convergence_angle_deg": 35.072,
      "proximal_arch_free_ellipse_b_over_a": 0.8456,
      "proximal_arch_free_ellipse_minor_deg": 29.2,
      "proximal_arch_rms_px": 0.1155
    },
    "DRLX_16bit_Linearized_CAHV": {
      "dorsal_theta_deg": 29.753,
      "dorsal_rms_px": 0.2542,
      "ventral_theta_deg": 65.666,
      "ventral_rms_px": 0.6543,
      "convergence_angle_deg": 35.914,
      "proximal_arch_free_ellipse_b_over_a": 0.8211,
      "proximal_arch_free_ellipse_minor_deg": 34.07,
      "proximal_arch_rms_px": 0.2046
    },
    "DRCL_8bit_Linearized_CAHV": {
      "dorsal_theta_deg": 29.949,
      "dorsal_rms_px": 0.2681,
      "ventral_theta_deg": 65.433,
      "ventral_rms_px": 0.6374,
      "convergence_angle_deg": 35.484,
      "proximal_arch_free_ellipse_b_over_a": 0.8368,
      "proximal_arch_free_ellipse_minor_deg": 29.49,
      "proximal_arch_rms_px": 0.1297
    }
  },
  "mc_noise_results": {
    "Noise_1x_Correlated": {
      "convergence_mean_deg": 34.162,
      "convergence_std_deg": 1.079,
      "dorsal_rms_mean_px": 0.4993,
      "dorsal_constrained_ba_mean": 0.8432,
      "dorsal_constrained_ba_std": 0.0407
    },
    "Noise_2x_Correlated": {
      "convergence_mean_deg": 34.653,
      "convergence_std_deg": 1.89,
      "dorsal_rms_mean_px": 0.773,
      "dorsal_constrained_ba_mean": 0.8505,
      "dorsal_constrained_ba_std": 0.0762
    },
    "Noise_3x_Correlated": {
      "convergence_mean_deg": 34.938,
      "convergence_std_deg": 2.452,
      "dorsal_rms_mean_px": 1.0083,
      "dorsal_constrained_ba_mean": 0.8149,
      "dorsal_constrained_ba_std": 0.1296
    }
  }
}
=== All steps completed successfully. Outputs saved in independent-reconstruction/ ===

```

