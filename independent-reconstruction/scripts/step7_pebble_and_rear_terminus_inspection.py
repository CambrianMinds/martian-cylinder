"""
Step 7: High-Resolution Pixel-Level Inspection of the Adjacent Upper-Right Pebble
and the Rear Terminus Curvature vs Front Face
Independent Geometric Investigation - Curiosity Sol 3556 (3556MR1025170721700585C00)
"""

import os
import numpy as np
from scipy.ndimage import gaussian_filter, sobel
import matplotlib.pyplot as plt

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(OUT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

from step1_image_inspection import PRODUCTS, load_pds_image
from step3_feature_extraction import load_drxx, load_drlx

def main():
    drxx_dn, drxx_rad, drxx_lum = load_drxx()
    drlx_dn, drlx_rad, drlx_lum = load_drlx()
    drcx = load_pds_image(PRODUCTS["DRCX"])

    # Zoom 1: Full target and immediate surroundings [x: 1022..1095, y: 942..1006] with 2-px grid
    x0, x1 = 1022, 1095
    y0, y1 = 942, 1006

    crop_lum = drxx_lum[y0:y1, x0:x1]
    crop_drcx = drcx[y0:y1, x0:x1]

    # Compute Sobel gradient magnitude on unsmoothed and lightly smoothed (sigma=0.6) DRXX luminance
    gx = sobel(gaussian_filter(drxx_lum, 0.5), axis=1)[y0:y1, x0:x1]
    gy = sobel(gaussian_filter(drxx_lum, 0.5), axis=0)[y0:y1, x0:x1]
    gmag = np.hypot(gx, gy)

    fig, axes = plt.subplots(2, 2, figsize=(18, 16), dpi=160)

    # Panel A: DRCX with 2-px coordinate grid
    axes[0, 0].imshow(crop_drcx, extent=[x0 - 0.5, x1 - 0.5, y1 - 0.5, y0 - 0.5], interpolation="nearest")
    axes[0, 0].set_xticks(np.arange(x0, x1 + 1, 2))
    axes[0, 0].set_yticks(np.arange(y0, y1 + 1, 2))
    axes[0, 0].tick_params(axis="x", rotation=90, labelsize=7)
    axes[0, 0].tick_params(axis="y", labelsize=7)
    axes[0, 0].grid(True, color="cyan", alpha=0.35, linewidth=0.4)
    axes[0, 0].set_title("DRCX Color with 2-px Coordinate Grid [x: 1022..1095, y: 942..1006]")

    # Panel B: DRXX Luminance with Iso-Radiance Contours
    im1 = axes[0, 1].imshow(crop_lum, extent=[x0 - 0.5, x1 - 0.5, y1 - 0.5, y0 - 0.5], cmap="magma", interpolation="nearest")
    levels = np.linspace(0.02, 0.105, 18)
    X_grid, Y_grid = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1))
    axes[0, 1].contour(X_grid, Y_grid, crop_lum, levels=levels, colors="cyan", linewidths=0.6, alpha=0.7)
    axes[0, 1].set_xticks(np.arange(x0, x1 + 1, 2))
    axes[0, 1].set_yticks(np.arange(y0, y1 + 1, 2))
    axes[0, 1].tick_params(axis="x", rotation=90, labelsize=7)
    axes[0, 1].tick_params(axis="y", labelsize=7)
    axes[0, 1].grid(True, color="white", alpha=0.3, linewidth=0.4)
    axes[0, 1].set_title("DRXX Spectral Radiance + Iso-Radiance Contours")

    # Panel C: Ultra-Zoom on Rear Terminus & Upper-Right Flank [x: 1024..1072, y: 943..975]
    rx0, rx1, ry0, ry1 = 1024, 1072, 943, 975
    axes[1, 0].imshow(drxx_lum[ry0:ry1, rx0:rx1], extent=[rx0 - 0.5, rx1 - 0.5, ry1 - 0.5, ry0 - 0.5], cmap="viridis", interpolation="nearest")
    Xg_r, Yg_r = np.meshgrid(np.arange(rx0, rx1), np.arange(ry0, ry1))
    axes[1, 0].contour(Xg_r, Yg_r, drxx_lum[ry0:ry1, rx0:rx1], levels=np.linspace(0.04, 0.105, 14), colors="white", linewidths=0.7)
    axes[1, 0].set_xticks(np.arange(rx0, rx1 + 1, 1))
    axes[1, 0].set_yticks(np.arange(ry0, ry1 + 1, 1))
    axes[1, 0].tick_params(axis="x", rotation=90, labelsize=6.5)
    axes[1, 0].tick_params(axis="y", labelsize=6.5)
    axes[1, 0].grid(True, color="yellow", alpha=0.4, linewidth=0.4)
    axes[1, 0].set_title("Ultra-Zoom (1-px Grid): Rear Terminus & Upper-Right Region [x: 1024..1072, y: 943..975]")

    # Panel D: Sobel Gradient Magnitude [x: 1022..1095, y: 942..1006]
    axes[1, 1].imshow(gmag, extent=[x0 - 0.5, x1 - 0.5, y1 - 0.5, y0 - 0.5], cmap="inferno", interpolation="nearest")
    axes[1, 1].set_xticks(np.arange(x0, x1 + 1, 2))
    axes[1, 1].set_yticks(np.arange(y0, y1 + 1, 2))
    axes[1, 1].tick_params(axis="x", rotation=90, labelsize=7)
    axes[1, 1].tick_params(axis="y", labelsize=7)
    axes[1, 1].grid(True, color="cyan", alpha=0.35, linewidth=0.4)
    axes[1, 1].set_title("Sobel Edge Gradient Magnitude (Highlighting Object vs Adjacent Pebble Boundaries)")

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "diag07_pebble_and_rear_terminus_zoom.png"))
    plt.close()
    print("Saved diag07_pebble_and_rear_terminus_zoom.png")

if __name__ == "__main__":
    main()

