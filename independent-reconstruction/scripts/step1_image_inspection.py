"""
Step 1: Primary Image Provenance, Radiometric Verification, and Target Localization
Independent Geometric Investigation - Curiosity Sol 3556 (3556MR1025170721700585C00)
"""

import os
import json
import hashlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure output directory exists
OUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(OUT_DIR, "figures")
os.makedirs(FIG_DIR, exist_ok=True)

DATA_DIR = os.path.abspath(os.path.join(OUT_DIR, "..", "data"))

PRODUCTS = {
    "DRXX": {
        "img": os.path.join(DATA_DIR, "3556MR1025170721700585C00_DRXX.IMG"),
        "lbl": os.path.join(DATA_DIR, "3556MR1025170721700585C00_DRXX.LBL"),
        "lines": 1184,
        "samples": 1328,
        "bands": 3,
        "dtype": ">u2",  # MSB_UNSIGNED_INTEGER 16-bit
        "invalid": 4096,
        "radiance_scale": [1.201e-04, 1.112e-04, 1.037e-04],
        "first_line": 17,
        "first_sample": 161,
        "model_type": "CAHVOR"
    },
    "DRLX": {
        "img": os.path.join(DATA_DIR, "3556MR1025170721700585C00_DRLX.IMG"),
        "lbl": os.path.join(DATA_DIR, "3556MR1025170721700585C00_DRLX.LBL"),
        "lines": 1180,
        "samples": 1323,
        "bands": 3,
        "dtype": ">u2",
        "invalid": 4096,
        "radiance_scale": [1.201e-04, 1.112e-04, 1.037e-04],
        "first_line": 17,
        "first_sample": 161,
        "model_type": "CAHV"
    },
    "DRCX": {
        "img": os.path.join(DATA_DIR, "3556MR1025170721700585C00_DRCX.IMG"),
        "lbl": os.path.join(DATA_DIR, "3556MR1025170721700585C00_DRCX.LBL"),
        "lines": 1184,
        "samples": 1328,
        "bands": 3,
        "dtype": "u1",  # 8-bit unsigned integer
        "invalid": 255,
        "radiance_scale": None,
        "first_line": 17,
        "first_sample": 161,
        "model_type": "CAHVOR"
    },
    "DRCL": {
        "img": os.path.join(DATA_DIR, "3556MR1025170721700585C00_DRCL.IMG"),
        "lbl": os.path.join(DATA_DIR, "3556MR1025170721700585C00_DRCL.LBL"),
        "lines": 1180,
        "samples": 1323,
        "bands": 3,
        "dtype": "u1",
        "invalid": 255,
        "radiance_scale": None,
        "first_line": 17,
        "first_sample": 161,
        "model_type": "CAHV"
    }
}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def load_pds_image(prod_info):
    raw = np.fromfile(prod_info["img"], dtype=prod_info["dtype"])
    arr = raw.reshape((prod_info["bands"], prod_info["lines"], prod_info["samples"]))
    # Transpose to (lines, samples, bands) -> (y, x, c)
    return np.transpose(arr, (1, 2, 0))

def main():
    provenance = {}
    images = {}
    for name, info in PRODUCTS.items():
        arr = load_pds_image(info)
        images[name] = arr
        unique_vals_b0 = np.unique(arr[:, :, 0])
        provenance[name] = {
            "file": os.path.basename(info["img"]),
            "sha256": sha256_file(info["img"]),
            "lbl_sha256": sha256_file(info["lbl"]),
            "shape_yxc": list(arr.shape),
            "dtype": str(arr.dtype),
            "min_per_band": [int(arr[:, :, b].min()) for b in range(3)],
            "max_per_band": [int(arr[:, :, b].max()) for b in range(3)],
            "mean_per_band": [float(arr[:, :, b].mean()) for b in range(3)],
            "unique_dn_count_band0": int(len(unique_vals_b0)),
            "model_type": info["model_type"]
        }
        print(f"Loaded {name}: shape={arr.shape}, min={provenance[name]['min_per_band']}, max={provenance[name]['max_per_band']}, unique_b0={len(unique_vals_b0)}")

    # Search for the target object in the lower-right quadrant
    # From visual inspection of full frame (1328 x 1184), the object is near x ~ 1000-1120, y ~ 930-1030
    drxx = images["DRXX"].astype(np.float64)
    drcx = images["DRCX"]
    drlx = images["DRLX"].astype(np.float64)
    drcl = images["DRCL"]

    # Create a broad overview plot of the lower-right region with coordinate grid to pinpoint exact pixel bounds
    fig, axes = plt.subplots(1, 2, figsize=(16, 8), dpi=150)
    # Broad region: x in [950, 1150], y in [900, 1060]
    x0, x1 = 980, 1120
    y0, y1 = 920, 1040

    axes[0].imshow(drcx[y0:y1, x0:x1], extent=[x0 - 0.5, x1 - 0.5, y1 - 0.5, y0 - 0.5])
    axes[0].set_title("DRCX (8-bit Color, Raw CAHVOR Geometry)\nBroad Region [x: 980..1120, y: 920..1040]")
    axes[0].set_xlabel("Sample x (0-based image col)")
    axes[0].set_ylabel("Line y (0-based image row)")
    axes[0].grid(True, color="white", alpha=0.3, linestyle="--")

    # Tight region around the object: let's inspect [1020, 1105], [945, 1015]
    tx0, tx1 = 1020, 1105
    ty0, ty1 = 945, 1015
    axes[1].imshow(drcx[ty0:ty1, tx0:tx1], extent=[tx0 - 0.5, tx1 - 0.5, ty1 - 0.5, ty0 - 0.5], interpolation="nearest")
    axes[1].set_title("DRCX Zoomed Object [x: 1020..1105, y: 945..1015]")
    axes[1].set_xlabel("Sample x (0-based image col)")
    axes[1].set_ylabel("Line y (0-based image row)")
    axes[1].set_xticks(np.arange(tx0, tx1 + 1, 5))
    axes[1].set_yticks(np.arange(ty0, ty1 + 1, 5))
    axes[1].grid(True, color="cyan", alpha=0.4, linewidth=0.5)

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "diag01_localization_drcx.png"))
    plt.close()

    # Also plot DRXX (16-bit linear radiometric) vs DRLX (16-bit linearized CAHV)
    fig, axes = plt.subplots(2, 2, figsize=(16, 14), dpi=150)

    # Normalize DRXX locally for display
    crop_drxx = drxx[ty0:ty1, tx0:tx1]
    crop_drxx_norm = (crop_drxx - crop_drxx.min()) / (crop_drxx.max() - crop_drxx.min())
    axes[0, 0].imshow(crop_drxx_norm, extent=[tx0 - 0.5, tx1 - 0.5, ty1 - 0.5, ty0 - 0.5], interpolation="nearest")
    axes[0, 0].set_title("DRXX (16-bit Linear Radiometric, Locally Normalized)")
    axes[0, 0].set_xticks(np.arange(tx0, tx1 + 1, 5))
    axes[0, 0].set_yticks(np.arange(ty0, ty1 + 1, 5))
    axes[0, 0].grid(True, color="yellow", alpha=0.35, linewidth=0.5)

    # Luminance (radiance-weighted or green band) of DRXX
    rad_scale = np.array(PRODUCTS["DRXX"]["radiance_scale"])
    crop_rad = crop_drxx * rad_scale[None, None, :]
    lum_rad = crop_rad.mean(axis=2)
    im1 = axes[0, 1].imshow(lum_rad, extent=[tx0 - 0.5, tx1 - 0.5, ty1 - 0.5, ty0 - 0.5], cmap="viridis", interpolation="nearest")
    axes[0, 1].set_title("DRXX Mean Spectral Radiance (W / m^2 / sr / nm)")
    axes[0, 1].set_xticks(np.arange(tx0, tx1 + 1, 5))
    axes[0, 1].set_yticks(np.arange(ty0, ty1 + 1, 5))
    axes[0, 1].grid(True, color="white", alpha=0.35, linewidth=0.5)
    plt.colorbar(im1, ax=axes[0, 1], fraction=0.046, pad=0.04)

    # DRLX at same approximate coordinates (let's check offset between DRXX and DRLX)
    # Find the shift between DRXX and DRLX around the target via cross-correlation
    patch_ref = drxx[ty0:ty1, tx0:tx1, 1] - drxx[ty0:ty1, tx0:tx1, 1].mean()
    best_corr = -1e9
    best_dx, best_dy = 0, 0
    for dy in range(-15, 16):
        for dx in range(-15, 16):
            sub = drlx[ty0 + dy:ty1 + dy, tx0 + dx:tx1 + dx, 1]
            sub = sub - sub.mean()
            corr = np.sum(patch_ref * sub) / (np.linalg.norm(patch_ref) * np.linalg.norm(sub) + 1e-12)
            if corr > best_corr:
                best_corr = corr
                best_dx, best_dy = dx, dy

    print(f"DRLX vs DRXX shift at target: dx={best_dx}, dy={best_dy}, corr={best_corr:.6f}")
    provenance["drlx_shift_at_target"] = {"dx": int(best_dx), "dy": int(best_dy), "corr": float(best_corr)}

    lx0, lx1 = tx0 + best_dx, tx1 + best_dx
    ly0, ly1 = ty0 + best_dy, ty1 + best_dy
    crop_drlx = drlx[ly0:ly1, lx0:lx1]
    crop_drlx_norm = (crop_drlx - crop_drlx.min()) / (crop_drlx.max() - crop_drlx.min())
    axes[1, 0].imshow(crop_drlx_norm, extent=[lx0 - 0.5, lx1 - 0.5, ly1 - 0.5, ly0 - 0.5], interpolation="nearest")
    axes[1, 0].set_title(f"DRLX (16-bit Linearized CAHV) [x: {lx0}..{lx1}, y: {ly0}..{ly1}]")
    axes[1, 0].set_xticks(np.arange(lx0, lx1 + 1, 5))
    axes[1, 0].set_yticks(np.arange(ly0, ly1 + 1, 5))
    axes[1, 0].grid(True, color="yellow", alpha=0.35, linewidth=0.5)

    # Band difference (R - B normalized) to check for Bayer demosaicing / chromatic artifacts
    r_norm = (crop_drxx[:, :, 0] - crop_drxx[:, :, 0].mean()) / crop_drxx[:, :, 0].std()
    b_norm = (crop_drxx[:, :, 2] - crop_drxx[:, :, 2].mean()) / crop_drxx[:, :, 2].std()
    rb_diff = r_norm - b_norm
    im3 = axes[1, 1].imshow(rb_diff, extent=[tx0 - 0.5, tx1 - 0.5, ty1 - 0.5, ty0 - 0.5], cmap="RdBu_r", vmin=-1.5, vmax=1.5, interpolation="nearest")
    axes[1, 1].set_title("DRXX Standardized (R - B) Color Difference\n(Inspecting Bayer Demosaicing / Spectral Variation)")
    axes[1, 1].set_xticks(np.arange(tx0, tx1 + 1, 5))
    axes[1, 1].set_yticks(np.arange(ty0, ty1 + 1, 5))
    axes[1, 1].grid(True, color="black", alpha=0.3, linewidth=0.5)
    plt.colorbar(im3, ax=axes[1, 1], fraction=0.046, pad=0.04)

    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "diag02_radiometric_comparison.png"))
    plt.close()

    with open(os.path.join(OUT_DIR, "step1_provenance.json"), "w") as f:
        json.dump(provenance, f, indent=2)

if __name__ == "__main__":
    main()

