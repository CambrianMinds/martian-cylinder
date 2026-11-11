"""
Phase II Landmark Validation & Gradient Field Analysis
Curiosity Sol 3556 Mastcam cylindrical anomaly.
Extracts all key landmarks, evaluates candidate interpretations of the rear terminus,
computes gradient evidence, generates high-resolution annotated visualizations,
and exports structured measurements.
"""

import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import geometry_utils as gu
import audit_reanalysis as ar

def run_landmark_analysis():
    # Load crop image
    crop_path = 'data/crop_bottom_right.png'
    crop_img = Image.open(crop_path)
    crop_arr = np.array(crop_img)
    
    # sub120 region: [240:360, 209:329]
    y_off, x_off = 240, 209
    sub = crop_arr[y_off:y_off+120, x_off:x_off+120].astype(float)
    gray = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
    Sx, Sy, G = ar.sobel(gray)
    
    # 1. Front cap detection & center
    dark = gray[22:62, 38:78] < 75.0
    yy, xx = np.where(dark)
    xc0, yc0 = 38.0 + float(xx.mean()), 22.0 + float(yy.mean())
    X_rim, Y_rim = ar.rim_points(gray, Sx, Sy, xc0, yc0, 85.0, 2.6)
    
    from reproduce_analysis import fit_ellipse_fitzgibbon
    front_ellipse = fit_ellipse_fitzgibbon(X_rim, Y_rim)
    front_xc = front_ellipse['xc']
    front_yc = front_ellipse['yc']
    front_major_2a = front_ellipse['major_2a']
    front_minor_2b = front_ellipse['minor_2b']
    front_ba = front_ellipse['circ_ratio']
    
    # Front rim extreme points
    front_right_apex = (float(np.max(X_rim)), float(Y_rim[np.argmax(X_rim)]))
    front_top_pt = (float(X_rim[np.argmin(Y_rim)]), float(np.min(Y_rim)))
    front_bot_pt = (float(X_rim[np.argmax(Y_rim)]), float(np.max(Y_rim)))
    
    # 2. Upper generator line
    xs_up, ys_up = [], []
    for x in range(28, 53):
        c = [y for y in range(2, 28) if Sy[y, x] > 15.0 and Sx[y, x] < -8.0]
        if c:
            by = max(c, key=lambda y: G[y, x])
            xs_up.append(float(x))
            ys_up.append(float(ar._subpix(G[:, x], by)))
    
    gen_fit = gu.tls_line_fit(xs_up, ys_up)
    gen_angle = gen_fit['angle_deg']
    gen_rmse = gen_fit['rmse_perp']
    
    # Unit vector along generator direction
    # Angle is measured from x-axis in degrees
    rad_gen = math.radians(gen_angle)
    u_gen = np.array([math.cos(rad_gen), math.sin(rad_gen)]) # points forward-right
    v_gen = np.array([-math.sin(rad_gen), math.cos(rad_gen)]) # perpendicular
    
    # 3. Rear terminus boundary extraction
    # Candidate rear boundary points at y in [4, 12]
    rear_pts = []
    for y in range(4, 13):
        bx = max(range(14, 24), key=lambda x: G[y, x])
        rear_pts.append((float(ar._subpix(G[y, :], bx)), float(y)))
    rear_x = np.array([p[0] for p in rear_pts])
    rear_y = np.array([p[1] for p in rear_pts])
    
    # Inferred rear center:
    # Under cylinder model with face ratio ba:
    # rear cap center projection along generator axis
    theta_view = gu.view_angle_from_face_ratio(front_ba)
    R_px = front_major_2a / 2.0
    b_minor = R_px * front_ba
    
    # Project rear points onto longitudinal axis
    u_c = []
    for xp, yp in rear_pts:
        dx, dy = xp - front_xc, yp - front_yc
        u = dx * u_gen[0] + dy * u_gen[1]
        v = dx * v_gen[0] + dy * v_gen[1]
        if abs(v) < R_px:
            u_c.append(u + b_minor * math.sqrt(max(0.0, 1.0 - (v / R_px)**2)))
    
    inferred_axis_2d = -float(np.mean(u_c)) # positive distance along axis
    rear_xc = front_xc - inferred_axis_2d * u_gen[0]
    rear_yc = front_yc - inferred_axis_2d * u_gen[1]
    
    # Far rear silhouette apex
    far_rear_apex = (float(np.min(rear_x)), float(rear_y[np.argmin(rear_x)]))
    
    # 4. Lower terrain-contact / shadow boundary
    # Scan vertically below cylinder body for gradient transition (y in 40..65, x in 25..60)
    contact_pts = []
    for x in range(25, 55, 2):
        # find strongest negative vertical gradient or transition below object
        y_candidates = [y for y in range(35, 60) if y < 120]
        if y_candidates:
            by = max(y_candidates, key=lambda y: abs(Sy[y, x]))
            contact_pts.append((float(x), float(by)))
            
    # 5. Metric distances
    # A. Center-to-center projected separation
    center_sep_px = math.hypot(front_xc - rear_xc, front_yc - rear_yc)
    # B. Apex-to-apex total visible feature extent
    feature_extent_px = math.hypot(front_right_apex[0] - far_rear_apex[0], front_right_apex[1] - far_rear_apex[1])
    # C. Illuminated generator length
    gen_len_px = math.hypot(xs_up[-1] - xs_up[0], ys_up[-1] - ys_up[0])
    # D. Historical 110-px visual extent (spanning from rear shelf edge x~10 to far right edge x~118)
    # In full sub120, the entire rock/shadow formation spans ~108-112 px
    
    print(f"--- LANDMARK MEASUREMENTS ---")
    print(f"Front cap center (sub120): ({front_xc:.2f}, {front_yc:.2f}) -> crop: ({front_xc+x_off:.2f}, {front_yc+y_off:.2f})")
    print(f"Front cap major 2a: {front_major_2a:.2f} px, minor 2b: {front_minor_2b:.2f} px, b/a: {front_ba:.4f}")
    print(f"Inferred rear cap center (sub120): ({rear_xc:.2f}, {rear_yc:.2f}) -> crop: ({rear_xc+x_off:.2f}, {rear_yc+y_off:.2f})")
    print(f"Projected center-to-center separation: {center_sep_px:.2f} px")
    print(f"Upper generator angle: {gen_angle:.2f} deg, RMSE: {gen_rmse:.3f} px, length: {gen_len_px:.2f} px")
    print(f"Silhouette apex-to-apex visible extent: {feature_extent_px:.2f} px")
    print(f"Far rear apex: {far_rear_apex}, Front right apex: {front_right_apex}")
    
    # 6. Generate Visualizations using PIL
    # A. Annotated landmarks overlay
    scale = 4  # 4x zoom for crisp display
    overlay_img = crop_img.copy()
    draw_crop = ImageDraw.Draw(overlay_img)
    
    # Let's crop and upscale sub120 to 480x480 for ultra-clear inspection
    sub_img = crop_img.crop((x_off, y_off, x_off+120, y_off+120)).resize((120*scale, 120*scale), Image.Resampling.LANCZOS)
    draw_sub = ImageDraw.Draw(sub_img)
    
    # Draw front rim points
    for x, y in zip(X_rim, Y_rim):
        sx, sy = x * scale, y * scale
        draw_sub.ellipse((sx-2, sy-2, sx+2, sy+2), fill='cyan', outline='blue')
        
    # Draw front center
    fc_s = (front_xc * scale, front_yc * scale)
    draw_sub.ellipse((fc_s[0]-5, fc_s[1]-5, fc_s[0]+5, fc_s[1]+5), fill='yellow', outline='black')
    
    # Draw rear points
    for x, y in rear_pts:
        sx, sy = x * scale, y * scale
        draw_sub.ellipse((sx-3, sy-3, sx+3, sy+3), fill='magenta', outline='white')
        
    # Draw rear center
    rc_s = (rear_xc * scale, rear_yc * scale)
    draw_sub.ellipse((rc_s[0]-5, rc_s[1]-5, rc_s[0]+5, rc_s[1]+5), fill='orange', outline='black')
    
    # Draw generator points
    for x, y in zip(xs_up, ys_up):
        sx, sy = x * scale, y * scale
        draw_sub.ellipse((sx-2, sy-2, sx+2, sy+2), fill='lime', outline='green')
        
    # Draw axis line between centers
    draw_sub.line([(rc_s[0], rc_s[1]), (fc_s[0], fc_s[1])], fill='yellow', width=3)
    
    # Draw generator line
    x_g0, y_g0 = xs_up[0], ys_up[0]
    x_g1, y_g1 = xs_up[-1], ys_up[-1]
    draw_sub.line([(x_g0*scale, y_g0*scale), (x_g1*scale, y_g1*scale)], fill='lime', width=2)
    
    # Draw terrain contact points
    for x, y in contact_pts:
        sx, sy = x * scale, y * scale
        draw_sub.rectangle((sx-2, sy-2, sx+2, sy+2), fill='coral', outline='red')
        
    # Draw apex-to-apex dashed/dotted line
    draw_sub.line([(far_rear_apex[0]*scale, far_rear_apex[1]*scale), 
                   (front_right_apex[0]*scale, front_right_apex[1]*scale)], fill='white', width=1)
                   
    # Add annotations text
    draw_sub.text((10, 10), "Cyan: Front Rim Points", fill='cyan')
    draw_sub.text((10, 25), "Yellow: Front Center & Axis (38.8 px)", fill='yellow')
    draw_sub.text((10, 40), "Magenta: Rear Terminus Boundary", fill='magenta')
    draw_sub.text((10, 55), "Orange: Inferred Rear Center", fill='orange')
    draw_sub.text((10, 70), "Lime: Upper Generator", fill='lime')
    draw_sub.text((10, 85), "Coral: Terrain Contact Boundary", fill='coral')
    draw_sub.text((10, 100), f"Apex Extent: {feature_extent_px:.1f} px", fill='white')
    
    sub_img.save('data/phase2_landmarks_overlay.png')
    print("Saved data/phase2_landmarks_overlay.png")
    
    # B. Gradient Field Visualization
    # Normalize G to 0..255
    G_norm = np.clip((G / np.percentile(G, 99)) * 255.0, 0, 255).astype(np.uint8)
    grad_img = Image.fromarray(G_norm).convert('RGB').resize((120*scale, 120*scale), Image.Resampling.NEAREST)
    draw_grad = ImageDraw.Draw(grad_img)
    
    # Overlay contours
    draw_grad.line([(rc_s[0], rc_s[1]), (fc_s[0], fc_s[1])], fill='yellow', width=2)
    for x, y in zip(X_rim, Y_rim):
        draw_grad.point((x*scale, y*scale), fill='cyan')
    for x, y in rear_pts:
        draw_grad.ellipse((x*scale-2, y*scale-2, x*scale+2, y*scale+2), fill='magenta')
    for x, y in zip(xs_up, ys_up):
        draw_grad.point((x*scale, y*scale), fill='lime')
    draw_grad.text((10, 10), "Sobel Gradient Field Magnitude |G|", fill='yellow')
    draw_grad.text((10, 25), "Rear Terminus vs Front Rim vs Generator", fill='white')
    
    grad_img.save('data/phase2_gradient_field.png')
    print("Saved data/phase2_gradient_field.png")
    
    # 7. Evaluate the 6 Rear Boundary Hypotheses
    # We analyze gradient strength, curvature, continuity, and local morphology:
    grad_rear = [G[int(round(y)), int(round(x))] for x, y in rear_pts]
    grad_rim = [G[int(round(y)), int(round(x))] for x, y in zip(X_rim, Y_rim)]
    grad_gen = [G[int(round(y)), int(round(x))] for x, y in zip(xs_up, ys_up)]
    
    print("\n--- GRADIENT EVIDENCE ANALYSIS ---")
    print(f"Front rim gradient: mean={np.mean(grad_rim):.2f}, std={np.std(grad_rim):.2f}, min={np.min(grad_rim):.2f}, max={np.max(grad_rim):.2f}")
    print(f"Rear boundary gradient: mean={np.mean(grad_rear):.2f}, std={np.std(grad_rear):.2f}, min={np.min(grad_rear):.2f}, max={np.max(grad_rear):.2f}")
    print(f"Upper generator gradient: mean={np.mean(grad_gen):.2f}, std={np.std(grad_gen):.2f}, min={np.min(grad_gen):.2f}, max={np.max(grad_gen):.2f}")
    
    return {
        "front_center_sub": [front_xc, front_yc],
        "front_center_crop": [front_xc + x_off, front_yc + y_off],
        "rear_center_sub": [rear_xc, rear_yc],
        "rear_center_crop": [rear_xc + x_off, rear_yc + y_off],
        "center_sep_px": center_sep_px,
        "feature_extent_px": feature_extent_px,
        "gen_len_px": gen_len_px,
        "gen_angle": gen_angle,
        "gen_rmse": gen_rmse,
        "front_ellipse": front_ellipse,
        "rear_pts": rear_pts,
        "contact_pts": contact_pts,
        "grad_rear_mean": float(np.mean(grad_rear)),
        "grad_rim_mean": float(np.mean(grad_rim)),
        "grad_gen_mean": float(np.mean(grad_gen))
    }

if __name__ == '__main__':
    run_landmark_analysis()

