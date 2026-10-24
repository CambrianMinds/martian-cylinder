/**
 * Martian Cylinder Photogrammetry Model & Renderer
 * Features:
 * - Accurate 3D optical central perspective projection physics model
 * - Pure straight cylinder in 3D (no taper): back circle is naturally smaller due to perspective foreshortening!
 * - Full 360° perspective tilt (pitch) and 360° planar rotation (yaw/roll)
 * - Exact outer tangent lines connecting the two perspective ellipses
 * - Uniform resize while strictly maintaining aspect ratio
 * - Direct length adjustment via on-screen handle or slider
 * - Depth-sorted Z-order rendering (far cap behind barrel, near cap on top)
 * - Multiple scientific render modes (wireframe, translucent, diagnostic, solid)
 */

class MartianCylinder {
  constructor(options = {}) {
    // Position on canvas/image (in image coordinate space)
    this.x = options.x || 300;
    this.y = options.y || 250;

    // Base dimensions (defines the fixed aspect ratio)
    this.baseLength = options.baseLength || 180;    // Nominal length
    this.baseDiameter = options.baseDiameter || 108; // Nominal diameter
    this.aspectRatio = this.baseLength / this.baseDiameter; // Default ~1.67

    // Scale multiplier (dragging corners changes this uniformly!)
    this.scale = options.scale || 1.0;

    // Angles
    this.rotation = options.rotation !== undefined ? options.rotation : (-42 * Math.PI / 180); // 360° planar angle (radians)
    this.tilt = options.tilt !== undefined ? options.tilt : (48 * Math.PI / 180); // 360° perspective tilt (radians)

    // Perspective Camera Distance Ratio (Z0 = L * camRatio)
    // Controls how pronounced the perspective scaling is (back circle smaller than front circle)
    this.camRatio = options.camRatio !== undefined ? options.camRatio : 2.8;

    // Visual styles
    this.color = options.color || '#00f0ff';
    this.opacity = options.opacity !== undefined ? options.opacity : 0.75;
    this.lineWidth = options.lineWidth !== undefined ? options.lineWidth : 1.5; // Wireframe & silhouette line thickness
    this.renderMode = options.renderMode || 'semi-transparent'; // 'semi-transparent', 'wireframe', 'solid', 'diagnostic'
    this.showAxis = options.showAxis !== undefined ? options.showAxis : true;
    this.showEllipseAxes = options.showEllipseAxes !== undefined ? options.showEllipseAxes : true;
    this.showShadow = options.showShadow !== undefined ? options.showShadow : false;
    this.sunAzimuth = options.sunAzimuth || 295; // degrees
    this.sunElevation = options.sunElevation || 69.7; // degrees (Curiosity Sol 3556 metadata)
    
    // Interactive State & Handles Visibility
    this.showHandles = options.showHandles !== undefined ? options.showHandles : true;
    this.isSelected = true;
    this.isHovered = false;
    this.hoverHandle = null;

    // Handle styling constants (in screen pixels, adjusted for zoom)
    this.handleSize = 9;
    this.rotHandleOffset = 38;
    this.lenHandleOffset = 28;
  }

  // --- Getters for current scaled dimensions ---
  get length() {
    return this.baseLength * this.scale;
  }

  get diameter() {
    return this.baseDiameter * this.scale;
  }

  get radius() {
    return this.diameter / 2;
  }

  // Set aspect ratio while keeping current diameter (anchoring front face)
  setAspectRatio(ratio, anchorFront = true) {
    if (ratio <= 0) return;
    if (anchorFront) {
      const oldGeo = this.getGeometry();
      const targetNearX = oldGeo.nearX;
      const targetNearY = oldGeo.nearY;

      this.aspectRatio = ratio;
      this.baseLength = this.baseDiameter * ratio;

      const newGeo = this.getGeometry();
      this.x += (targetNearX - newGeo.nearX);
      this.y += (targetNearY - newGeo.nearY);
    } else {
      this.aspectRatio = ratio;
      this.baseLength = this.baseDiameter * ratio;
    }
  }

  // Set diameter directly and update base dimension (anchoring front face)
  setDiameter(d, anchorFront = true) {
    if (d <= 0) return;
    if (anchorFront) {
      const oldGeo = this.getGeometry();
      const targetNearX = oldGeo.nearX;
      const targetNearY = oldGeo.nearY;

      this.baseDiameter = d / this.scale;
      this.aspectRatio = this.baseLength / this.baseDiameter;

      const newGeo = this.getGeometry();
      this.x += (targetNearX - newGeo.nearX);
      this.y += (targetNearY - newGeo.nearY);
    } else {
      this.baseDiameter = d / this.scale;
      this.aspectRatio = this.baseLength / this.baseDiameter;
    }
  }

  // Set length directly (strictly anchors the front face so ONLY the back moves)
  setLength(l, anchorFront = true) {
    if (l <= 0) return;
    if (anchorFront) {
      const oldGeo = this.getGeometry();
      const targetNearX = oldGeo.nearX;
      const targetNearY = oldGeo.nearY;

      this.baseLength = l / this.scale;
      this.aspectRatio = this.baseLength / this.baseDiameter;

      const newGeo = this.getGeometry();
      this.x += (targetNearX - newGeo.nearX);
      this.y += (targetNearY - newGeo.nearY);
    } else {
      this.baseLength = l / this.scale;
      this.aspectRatio = this.baseLength / this.baseDiameter;
    }
  }

  /**
   * Solve exact outer tangent contact points between two perspective ellipses
   * In local coordinates (U, V) where line of centers is along U (X-axis):
   * Ellipse 1: center (0, 0), semi-axes (b1 along U, a1 along V)
   * Ellipse 2: center (D, 0), semi-axes (b2 along U, a2 along V)
   */
  solveTangents(x1, a1, b1, x2, a2, b2) {
    const dx = x1 - x2; // -D (negative)
    if (Math.abs(dx) < 1e-4) {
      return {
        p1Top: { x: x1, y: a1 },
        p2Top: { x: x2, y: a2 },
        p1Bot: { x: x1, y: -a1 },
        p2Bot: { x: x2, y: -a2 }
      };
    }

    // Tangent slope m in (U, V) frame
    let m = (a2 - a1) / (-dx);
    for (let i = 0; i < 20; i++) {
      const h1 = Math.hypot(a1, m * b1);
      const h2 = Math.hypot(a2, m * b2);
      const fVal = m * dx - (h1 - h2);
      const dfVal = dx - (m * b1 * b1 / Math.max(1e-4, h1) - m * b2 * b2 / Math.max(1e-4, h2));
      if (Math.abs(dfVal) < 1e-7) break;
      const step = fVal / dfVal;
      m -= step;
      if (Math.abs(step) < 1e-7) break;
    }

    const h1 = Math.max(1e-4, Math.hypot(a1, m * b1));
    const h2 = Math.max(1e-4, Math.hypot(a2, m * b2));

    return {
      p1Top: { x: x1 - (m * b1 * b1) / h1, y: (a1 * a1) / h1 },
      p2Top: { x: x2 - (m * b2 * b2) / h2, y: (a2 * a2) / h2 },
      p1Bot: { x: x1 + (m * b1 * b1) / h1, y: -(a1 * a1) / h1 },
      p2Bot: { x: x2 + (m * b2 * b2) / h2, y: -(a2 * a2) / h2 }
    };
  }

  /**
   * Compute geometric projection parameters in image coordinate space
   * Using Central Perspective Projection Physics:
   */
  getGeometry() {
    const L = this.length;
    const R = this.radius;
    const rot = this.rotation;
    const tilt = this.tilt; // 0 to 2*PI (360 degrees)

    // Camera reference distance
    const Z0 = Math.max(L * 1.2, L * this.camRatio);

    // 3D Depths:
    const cosTilt = Math.cos(tilt);
    const sinTilt = Math.sin(tilt);

    const Z1 = Math.max(10, Z0 - (L / 2) * cosTilt);
    const Z2 = Math.max(10, Z0 + (L / 2) * cosTilt);

    // Unit direction vectors in 2D screen plane
    const ux = Math.cos(rot);
    const uy = Math.sin(rot);
    const vx = -Math.sin(rot);
    const vy = Math.cos(rot);

    // Screen projected centers of Cap 1 and Cap 2
    // Scaled by respective depth perspective multipliers: (Z0 / Z)
    const fX = this.x + (L / 2) * sinTilt * ux * (Z0 / Z1);
    const fY = this.y + (L / 2) * sinTilt * uy * (Z0 / Z1);

    const rX = this.x - (L / 2) * sinTilt * ux * (Z0 / Z2);
    const rY = this.y - (L / 2) * sinTilt * uy * (Z0 / Z2);

    // Perspective apparent radii on screen:
    // r = R * (Z0 / Z). Farther cap is naturally smaller!
    const r1 = R * (Z0 / Z1);
    const r2 = R * (Z0 / Z2);

    // Ellipse semi-axes:
    // Major axis perpendicular to cylinder axis
    const a1 = r1;
    const a2 = r2;
    // Minor axis along cylinder axis (squashed by |cos(tilt)|)
    const b1 = Math.max(0.5, r1 * Math.abs(cosTilt));
    const b2 = Math.max(0.5, r2 * Math.abs(cosTilt));

    // Determine depth ordering (Z-order)
    const isCap1Near = (Z1 <= Z2);
    const nearCap = isCap1Near ? 1 : 2;
    const nearZ = Math.min(Z1, Z2);
    const farZ = Math.max(Z1, Z2);
    const nearR = isCap1Near ? a1 : a2;
    const farR = isCap1Near ? a2 : a1;
    const perspRatio = farR / nearR; // < 1.0 (back circle smaller than front circle!)

    // Calculate line of centers and tangent lines connecting the two ellipses:
    const cdx = rX - fX;
    const cdy = rY - fY;
    const centerDist = Math.hypot(cdx, cdy);

    let Ux = ux;
    let Uy = uy;
    let Vx = vx;
    let Vy = vy;
    if (centerDist > 1e-4) {
      Ux = cdx / centerDist;
      Uy = cdy / centerDist;
      Vx = -Uy;
      Vy = Ux;
    }

    // Solve tangents in (Ux, Uy) & (Vx, Vy) frame:
    // Ellipse 1 at 0, Ellipse 2 at centerDist
    const tang = this.solveTangents(0, a1, b1, centerDist, a2, b2);

    // Screen contact points:
    // p1 = Cap 1 top, p2 = Cap 1 bot, p4 = Cap 2 top, p3 = Cap 2 bot
    const p1 = {
      x: fX + tang.p1Top.x * Ux + tang.p1Top.y * Vx,
      y: fY + tang.p1Top.x * Uy + tang.p1Top.y * Vy
    };
    const p2 = {
      x: fX + tang.p1Bot.x * Ux + tang.p1Bot.y * Vx,
      y: fY + tang.p1Bot.x * Uy + tang.p1Bot.y * Vy
    };
    const p3 = {
      x: fX + tang.p2Bot.x * Ux + tang.p2Bot.y * Vx,
      y: fY + tang.p2Bot.x * Uy + tang.p2Bot.y * Vy
    };
    const p4 = {
      x: fX + tang.p2Top.x * Ux + tang.p2Top.y * Vx,
      y: fY + tang.p2Top.x * Uy + tang.p2Top.y * Vy
    };

    // Identify Far vs Near Cap centers and parameters
    const nearX = isCap1Near ? fX : rX;
    const nearY = isCap1Near ? fY : rY;
    const nearA = isCap1Near ? a1 : a2;
    const nearB = isCap1Near ? b1 : b2;

    const farX = isCap1Near ? rX : fX;
    const farY = isCap1Near ? rY : fY;
    const farA = isCap1Near ? a2 : a1;
    const farB = isCap1Near ? b2 : b1;

    // Tilt Handle on Near Ellipse apex (pointing forward)
    const tiltApexSign = isCap1Near ? -1 : 1;
    const frontApex = {
      x: nearX + nearB * tiltApexSign * Ux,
      y: nearY + nearB * tiltApexSign * Uy
    };

    // Rear length handle (extending behind the far cap)
    const lenHandleSign = isCap1Near ? 1 : -1;
    const lengthHandle = {
      x: farX + this.lenHandleOffset * lenHandleSign * Ux,
      y: farY + this.lenHandleOffset * lenHandleSign * Uy
    };

    // Bounding box half-extents in local frame
    const halfL = (centerDist + Math.max(b1, b2) * 2) / 2 + 12;
    const halfW = Math.max(a1, a2) + 12;

    // 4 Corner handles in world coordinates:
    const corners = {
      nw: { x: this.x - halfL * ux - halfW * vx, y: this.y - halfL * uy - halfW * vy },
      ne: { x: this.x + halfL * ux - halfW * vx, y: this.y + halfL * uy - halfW * vy },
      se: { x: this.x + halfL * ux + halfW * vx, y: this.y + halfL * uy + halfW * vy },
      sw: { x: this.x - halfL * ux + halfW * vx, y: this.y - halfL * uy + halfW * vy }
    };

    // Rotation handle (extending along -v on top)
    const rotHandle = {
      x: this.x - (halfW + this.rotHandleOffset) * vx,
      y: this.y - (halfW + this.rotHandleOffset) * vy
    };

    const rotStalkBase = {
      x: this.x - halfW * vx,
      y: this.y - halfW * vy
    };

    return {
      ux, uy, vx, vy,
      Ux, Uy, Vx, Vy,
      L, R,
      fX, fY, rX, rY,
      a1, b1, a2, b2,
      r1, r2,
      Z1, Z2, nearZ, farZ,
      nearCap, isCap1Near,
      nearX, nearY, nearA, nearB,
      farX, farY, farA, farB,
      nearR, farR, perspRatio,
      p1, p2, p3, p4,
      tang,
      centerDist,
      frontApex,
      lengthHandle,
      halfL, halfW,
      corners,
      rotHandle,
      rotStalkBase,
      cosTilt
    };
  }

  /**
   * Render the cylinder on the HTML5 Canvas
   */
  render(ctx, zoom = 1.0) {
    const geo = this.getGeometry();

    ctx.save();

    // 1. Draw optional Sun Cast Shadow
    if (this.showShadow) {
      this.drawCastShadow(ctx, geo);
    }

    // 2. Draw Cylinder Body & Caps according to Render Mode (Depth-Sorted!)
    this.drawCylinderBody(ctx, geo);

    // 3. Draw Scientific Diagnostic Annotations
    if (this.renderMode === 'diagnostic' || this.showAxis || this.showEllipseAxes) {
      this.drawDiagnostics(ctx, geo, zoom);
    }

    // 4. Draw Interactive Transform Handles (if selected and handles visible)
    if (this.isSelected && this.showHandles) {
      this.drawHandles(ctx, geo, zoom);
    }

    ctx.restore();
  }

  /**
   * Draw the 3D-shaded or wireframe cylinder barrel and caps with physics depth-sorting
   */
  drawCylinderBody(ctx, geo) {
    const {
      Ux, Uy, Vx, Vy,
      fX, fY, rX, rY,
      a1, b1, a2, b2,
      p1, p2, p3, p4,
      tang, centerDist,
      isCap1Near, farX, farY, nearX, nearY,
      farA, farB, nearA, nearB
    } = geo;

    const isWireframe = this.renderMode === 'wireframe';
    const isSolid = this.renderMode === 'solid';
    const isSemiTrans = this.renderMode === 'semi-transparent' || this.renderMode === 'diagnostic';

    const baseColor = this.color;
    const alpha = isSolid ? 1.0 : this.opacity;
    const lw = this.lineWidth || 1.5;

    // Angle of the ellipse semi-major axis (perpendicular to line of centers)
    const ellipseAngle = Math.atan2(Vy, Vx);

    // If centerDist is nearly 0 (concentric head-on view):
    if (centerDist < 0.5) {
      if (!isWireframe) {
        ctx.save();
        ctx.beginPath();
        ctx.ellipse(nearX, nearY, Math.max(1, nearA), Math.max(0.5, nearB), ellipseAngle, 0, Math.PI * 2);
        ctx.fillStyle = isSolid ? '#1e293b' : this.hexToRgba(baseColor, alpha * 0.7);
        ctx.fill();
        ctx.lineWidth = lw;
        ctx.strokeStyle = baseColor;
        ctx.stroke();
        ctx.restore();
      } else {
        ctx.save();
        ctx.lineWidth = lw;
        ctx.strokeStyle = baseColor;
        ctx.beginPath();
        ctx.ellipse(nearX, nearY, Math.max(1, nearA), Math.max(0.5, nearB), ellipseAngle, 0, Math.PI * 2);
        ctx.stroke();
        ctx.beginPath();
        ctx.ellipse(farX, farY, Math.max(1, farA), Math.max(0.5, farB), ellipseAngle, 0, Math.PI * 2);
        ctx.setLineDash([3, 3]);
        ctx.stroke();
        ctx.restore();
      }
      return;
    }

    // --- STEP 1: Far Cap (Behind barrel) ---
    // In wireframe, draw full far ellipse
    // In translucent, draw full far ellipse with dashed line so viewer sees rear cylinder base
    if (isWireframe || isSemiTrans) {
      ctx.save();
      ctx.beginPath();
      ctx.ellipse(farX, farY, Math.max(1, farA), Math.max(0.5, farB), ellipseAngle, 0, Math.PI * 2);
      if (isSemiTrans) {
        ctx.fillStyle = `rgba(15, 23, 42, ${alpha * 0.75})`;
        ctx.fill();
        ctx.setLineDash([3, 3]);
        ctx.lineWidth = lw;
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.45)';
      } else {
        // Wireframe
        ctx.lineWidth = lw;
        ctx.strokeStyle = baseColor;
      }
      ctx.stroke();
      ctx.restore();
    }

    // --- STEP 2: Cylinder Body Barrel (Solid & Translucent) ---
    if (!isWireframe) {
      ctx.save();
      ctx.beginPath();

      // Closed convex silhouette polygon (zero self-intersection across all 360° tilts)
      const th1 = Math.atan2(tang.p1Top.y / a1, tang.p1Top.x / b1);
      const th2 = Math.atan2(tang.p2Top.y / a2, (tang.p2Top.x - centerDist) / b2);

      const N = 18;
      // Start at top tangent of Cap 1:
      ctx.moveTo(p1.x, p1.y);
      // Line to top tangent of Cap 2:
      ctx.lineTo(p4.x, p4.y);

      // Arc around Cap 2 (th2 -> 0 -> -th2):
      for (let i = 1; i <= N; i++) {
        const t = th2 - 2 * th2 * (i / N);
        const px = rX + b2 * Math.cos(t) * Ux + a2 * Math.sin(t) * Vx;
        const py = rY + b2 * Math.cos(t) * Uy + a2 * Math.sin(t) * Vy;
        ctx.lineTo(px, py);
      }

      // Line to bottom tangent of Cap 1:
      ctx.lineTo(p2.x, p2.y);

      // Arc around Cap 1 (-th1 -> -pi -> th1):
      for (let i = 1; i <= N; i++) {
        const t = -th1 - (2 * Math.PI - 2 * th1) * (i / N);
        const px = fX + b1 * Math.cos(t) * Ux + a1 * Math.sin(t) * Vx;
        const py = fY + b1 * Math.cos(t) * Uy + a1 * Math.sin(t) * Vy;
        ctx.lineTo(px, py);
      }

      ctx.closePath();

      // Lighting gradient perpendicular to cylinder axis (along Vx, Vy)
      const grad = ctx.createLinearGradient(
        this.x - nearA * Vx, this.y - nearA * Vy,
        this.x + nearA * Vx, this.y + nearA * Vy
      );

      if (isSolid) {
        grad.addColorStop(0.0, '#334155');
        grad.addColorStop(0.3, '#cbd5e1');
        grad.addColorStop(0.65, '#64748b');
        grad.addColorStop(1.0, '#1e293b');
      } else {
        grad.addColorStop(0.0, this.hexToRgba(baseColor, alpha * 0.35));
        grad.addColorStop(0.35, this.hexToRgba('#ffffff', alpha * 0.85));
        grad.addColorStop(0.65, this.hexToRgba(baseColor, alpha * 0.55));
        grad.addColorStop(1.0, this.hexToRgba(baseColor, alpha * 0.25));
      }

      ctx.fillStyle = grad;
      ctx.fill();
      ctx.restore();
    }

    // --- STEP 3: Silhouette Outline Strokes (Top & Bottom Tangent Lines) ---
    ctx.save();
    ctx.lineWidth = lw;
    ctx.strokeStyle = baseColor;
    ctx.beginPath();
    // Top silhouette line (p1 to p4)
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p4.x, p4.y);
    // Bottom silhouette line (p2 to p3)
    ctx.moveTo(p2.x, p2.y);
    ctx.lineTo(p3.x, p3.y);
    ctx.stroke();
    ctx.restore();

    // --- STEP 4: Near Cap (In front of barrel) ---
    ctx.save();
    ctx.beginPath();
    ctx.ellipse(nearX, nearY, Math.max(1, nearA), Math.max(0.5, nearB), ellipseAngle, 0, Math.PI * 2);

    if (!isWireframe) {
      const faceGrad = ctx.createRadialGradient(
        nearX, nearY, nearA * 0.1,
        nearX, nearY, nearA
      );
      if (isSolid) {
        faceGrad.addColorStop(0, '#0f172a');
        faceGrad.addColorStop(0.85, '#1e293b');
        faceGrad.addColorStop(1.0, '#475569');
      } else {
        faceGrad.addColorStop(0, this.hexToRgba('#050b14', alpha * 0.92));
        faceGrad.addColorStop(0.7, this.hexToRgba(baseColor, alpha * 0.45));
        faceGrad.addColorStop(1.0, this.hexToRgba(baseColor, alpha * 0.85));
      }
      ctx.fillStyle = faceGrad;
      ctx.fill();
    }

    // Near cap rim stroke
    ctx.lineWidth = lw;
    ctx.strokeStyle = baseColor;
    ctx.stroke();

    // Inner concentric ring for depth cue (non-wireframe)
    if (!isWireframe && nearA > 15) {
      ctx.beginPath();
      ctx.ellipse(nearX, nearY, nearA * 0.88, Math.max(0.5, nearB * 0.88), ellipseAngle, 0, Math.PI * 2);
      ctx.lineWidth = Math.max(0.5, lw * 0.6);
      ctx.strokeStyle = this.hexToRgba(baseColor, 0.45);
      ctx.stroke();
    }
    ctx.restore();
  }

  /**
   * Draw scientific diagnostics:
   * - Central 3D axis arrow line
   * - Major and Minor axes of near face ellipse
   * - Cap centers and perspective labels
   */
  drawDiagnostics(ctx, geo, zoom) {
    const { ux, uy, vx, vy, Ux, Uy, Vx, Vy, fX, fY, rX, rY, a1, b1, a2, b2, isCap1Near } = geo;
    const invZoom = 1 / zoom;

    const nearX = isCap1Near ? fX : rX;
    const nearY = isCap1Near ? fY : rY;
    const nearA = isCap1Near ? a1 : a2;
    const nearB = isCap1Near ? b1 : b2;

    const farX = isCap1Near ? rX : fX;
    const farY = isCap1Near ? rY : fY;

    ctx.save();
    const lw = this.lineWidth || 1.5;

    // 1. Central Axis Arrow Line (Orange -> Cyan -> Yellow)
    if (this.showAxis) {
      const startX = farX - 30 * Ux;
      const startY = farY - 30 * Uy;
      const endX = nearX + 45 * Ux;
      const endY = nearY + 45 * Uy;

      ctx.beginPath();
      ctx.moveTo(startX, startY);
      ctx.lineTo(farX, farY);
      ctx.lineWidth = Math.max(1.0, lw * 1.2) * invZoom;
      ctx.strokeStyle = '#ff9800'; // Orange rear
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(farX, farY);
      ctx.lineTo(nearX, nearY);
      ctx.lineWidth = Math.max(1.0, lw * 1.5) * invZoom;
      ctx.strokeStyle = '#00f0ff'; // Cyan cylinder core
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(nearX, nearY);
      ctx.lineTo(endX, endY);
      ctx.lineWidth = Math.max(1.0, lw * 1.2) * invZoom;
      ctx.strokeStyle = '#ffd600'; // Yellow arrow extension
      ctx.stroke();

      this.drawArrowHead(ctx, endX, endY, Ux, Uy, 9 * invZoom, '#ffd600');
    }

    // 2. Near Ellipse Major and Minor Axes
    if (this.showEllipseAxes) {
      // Major Axis (Transverse vector Vx, Vy)
      const majorLen = nearA * 1.25;
      ctx.beginPath();
      ctx.moveTo(nearX - majorLen * Vx, nearY - majorLen * Vy);
      ctx.lineTo(nearX + majorLen * Vx, nearY + majorLen * Vy);
      ctx.lineWidth = Math.max(1.0, lw * 1.2) * invZoom;
      ctx.strokeStyle = '#ff2a5f'; // Hot red major axis
      ctx.stroke();

      // Minor Axis (Along line of centers Ux, Uy)
      const minorLen = Math.max(8 * invZoom, nearB * 1.35);
      ctx.beginPath();
      ctx.moveTo(nearX - minorLen * Ux, nearY - minorLen * Uy);
      ctx.lineTo(nearX + minorLen * Ux, nearY + minorLen * Uy);
      ctx.lineWidth = Math.max(1.0, lw * 1.2) * invZoom;
      ctx.strokeStyle = '#00e5ff'; // Cyan minor axis
      ctx.stroke();

      // Near Face Center Reticle
      ctx.beginPath();
      ctx.arc(nearX, nearY, 3.5 * invZoom, 0, Math.PI * 2);
      ctx.fillStyle = '#ffffff';
      ctx.fill();
      ctx.lineWidth = 1.0 * invZoom;
      ctx.strokeStyle = '#ff2a5f';
      ctx.stroke();
    }

    ctx.restore();
  }

  /**
   * Draw interactive manipulation box and handles:
   * - Bounding box
   * - 4 Corner resize handles (NW, NE, SE, SW)
   * - Rotation stalk and knob
   * - 360° Tilt apex handle
   * - Length handle at rear
   */
  drawHandles(ctx, geo, zoom) {
    const { corners, rotHandle, rotStalkBase, frontApex, lengthHandle, farX, farY, rX, rY } = geo;
    const invZoom = 1 / zoom;
    const handleR = this.handleSize * invZoom;

    ctx.save();

    // 1. Oriented Bounding Box
    ctx.beginPath();
    ctx.moveTo(corners.nw.x, corners.nw.y);
    ctx.lineTo(corners.ne.x, corners.ne.y);
    ctx.lineTo(corners.se.x, corners.se.y);
    ctx.lineTo(corners.sw.x, corners.sw.y);
    ctx.closePath();
    ctx.lineWidth = 1.2 * invZoom;
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.45)';
    ctx.setLineDash([4 * invZoom, 4 * invZoom]);
    ctx.stroke();
    ctx.setLineDash([]);

    // 2. Rotation Stalk Line
    ctx.beginPath();
    ctx.moveTo(rotStalkBase.x, rotStalkBase.y);
    ctx.lineTo(rotHandle.x, rotHandle.y);
    ctx.lineWidth = 1.5 * invZoom;
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.7)';
    ctx.stroke();

    // 3. Rotation Handle Knob
    ctx.beginPath();
    ctx.arc(rotHandle.x, rotHandle.y, handleR * 1.15, 0, Math.PI * 2);
    ctx.fillStyle = (this.hoverHandle === 'rotation') ? '#ffffff' : '#00f0ff';
    ctx.fill();
    ctx.lineWidth = 2 * invZoom;
    ctx.strokeStyle = '#080c14';
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(rotHandle.x, rotHandle.y, 3 * invZoom, 0, Math.PI * 2);
    ctx.fillStyle = '#080c14';
    ctx.fill();

    // 4. 4 Corner Resize Handles
    const cornerKeys = ['nw', 'ne', 'se', 'sw'];
    cornerKeys.forEach(key => {
      const pt = corners[key];
      const isHov = this.hoverHandle === `corner-${key}`;

      ctx.save();
      ctx.translate(pt.x, pt.y);
      ctx.rotate(this.rotation);

      ctx.beginPath();
      ctx.rect(-handleR / 2, -handleR / 2, handleR, handleR);
      ctx.fillStyle = isHov ? '#ffffff' : '#0f172a';
      ctx.fill();
      ctx.lineWidth = 1.8 * invZoom;
      ctx.strokeStyle = isHov ? '#00f0ff' : '#38bdf8';
      ctx.stroke();

      ctx.restore();
    });

    // 5. 360° Tilt Handle on Near Ellipse Apex (Diamond shape)
    const isTiltHov = this.hoverHandle === 'tilt';
    ctx.save();
    ctx.translate(frontApex.x, frontApex.y);
    ctx.rotate(this.rotation);
    ctx.beginPath();
    ctx.moveTo(0, -handleR * 0.85);
    ctx.lineTo(handleR * 0.85, 0);
    ctx.lineTo(0, handleR * 0.85);
    ctx.lineTo(-handleR * 0.85, 0);
    ctx.closePath();
    ctx.fillStyle = isTiltHov ? '#ffffff' : '#ffb800';
    ctx.fill();
    ctx.lineWidth = 1.5 * invZoom;
    ctx.strokeStyle = '#080c14';
    ctx.stroke();
    ctx.restore();

    // 6. Length Adjustment Handle at the rear base (along cylinder axis)
    const isLenHov = this.hoverHandle === 'length';
    ctx.save();
    ctx.beginPath();
    ctx.moveTo(farX, farY);
    ctx.lineTo(lengthHandle.x, lengthHandle.y);
    ctx.lineWidth = 1.6 * invZoom;
    ctx.strokeStyle = isLenHov ? '#ffffff' : 'rgba(255, 152, 0, 0.85)';
    ctx.setLineDash([3 * invZoom, 3 * invZoom]);
    ctx.stroke();
    ctx.setLineDash([]);

    ctx.translate(lengthHandle.x, lengthHandle.y);
    ctx.rotate(this.rotation);
    ctx.beginPath();
    ctx.rect(-handleR * 1.1, -handleR * 0.7, handleR * 2.2, handleR * 1.4);
    ctx.fillStyle = isLenHov ? '#ffffff' : '#ff9800';
    ctx.fill();
    ctx.lineWidth = 1.5 * invZoom;
    ctx.strokeStyle = '#080c14';
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(-handleR * 0.55, 0);
    ctx.lineTo(-handleR * 0.2, -handleR * 0.35);
    ctx.moveTo(-handleR * 0.55, 0);
    ctx.lineTo(-handleR * 0.2, handleR * 0.35);
    ctx.moveTo(handleR * 0.55, 0);
    ctx.lineTo(handleR * 0.2, -handleR * 0.35);
    ctx.moveTo(handleR * 0.55, 0);
    ctx.lineTo(handleR * 0.2, handleR * 0.35);
    ctx.lineWidth = 1.3 * invZoom;
    ctx.strokeStyle = isLenHov ? '#ff9800' : '#080c14';
    ctx.stroke();
    ctx.restore();

    // 7. Center Anchor Reticle
    ctx.beginPath();
    ctx.arc(this.x, this.y, 4 * invZoom, 0, Math.PI * 2);
    ctx.fillStyle = '#00f0ff';
    ctx.fill();
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 1.2 * invZoom;
    ctx.stroke();

    ctx.restore();
  }

  /**
   * Draw predicted Martian solar cast shadow
   */
  drawCastShadow(ctx, geo) {
    const { radius } = this;
    const { fX, fY, rX, rY } = geo;

    const sunAzRad = (this.sunAzimuth * Math.PI) / 180;
    const sunElRad = (this.sunElevation * Math.PI) / 180;

    const shadowRatio = 1 / Math.tan(Math.max(0.1, sunElRad));
    const shadowDist = radius * 2 * shadowRatio;

    const sx = Math.cos(sunAzRad + Math.PI) * shadowDist;
    const sy = Math.sin(sunAzRad + Math.PI) * shadowDist;

    ctx.save();
    ctx.beginPath();
    ctx.moveTo(fX, fY);
    ctx.lineTo(fX + sx, fY + sy);
    ctx.lineTo(rX + sx, rY + sy);
    ctx.lineTo(rX, rY);
    ctx.closePath();
    ctx.fillStyle = 'rgba(10, 10, 15, 0.45)';
    ctx.filter = 'blur(3px)';
    ctx.fill();
    ctx.restore();
  }

  drawArrowHead(ctx, x, y, dirX, dirY, size, color) {
    const angle = Math.atan2(dirY, dirX);
    ctx.save();
    ctx.translate(x, y);
    ctx.rotate(angle);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(-size, -size * 0.5);
    ctx.lineTo(-size * 0.7, 0);
    ctx.lineTo(-size, size * 0.5);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
    ctx.restore();
  }

  /**
   * Hit test against handles or cylinder body:
   */
  hitTest(worldX, worldY, zoom = 1.0) {
    const geo = this.getGeometry();
    const invZoom = 1 / zoom;
    const tol = Math.max(12 * invZoom, this.handleSize * 1.5 * invZoom);

    // Check handles only if handles are currently enabled
    if (this.showHandles) {
      // 1. Rotation Handle
      if (this.dist(worldX, worldY, geo.rotHandle.x, geo.rotHandle.y) <= tol * 1.3) {
        return 'rotation';
      }

      // 2. Length Handle (Rear base)
      if (this.dist(worldX, worldY, geo.lengthHandle.x, geo.lengthHandle.y) <= tol * 1.3) {
        return 'length';
      }

      // 3. Corner Handles
      const corners = geo.corners;
      for (const key of ['nw', 'ne', 'se', 'sw']) {
        if (this.dist(worldX, worldY, corners[key].x, corners[key].y) <= tol) {
          return `corner-${key}`;
        }
      }

      // 4. 360° Tilt Apex Handle
      if (this.dist(worldX, worldY, geo.frontApex.x, geo.frontApex.y) <= tol) {
        return 'tilt';
      }
    }

    // 5. Body / Bounding Area
    const dx = worldX - this.x;
    const dy = worldY - this.y;
    const localX = dx * geo.ux + dy * geo.uy;
    const localY = dx * geo.vx + dy * geo.vy;

    if (Math.abs(localX) <= geo.halfL && Math.abs(localY) <= geo.halfW) {
      return 'body';
    }

    return null;
  }

  dist(x1, y1, x2, y2) {
    return Math.hypot(x1 - x2, y1 - y2);
  }

  hexToRgba(hex, alpha) {
    let c = hex.replace('#', '');
    if (c.length === 3) {
      c = c[0] + c[0] + c[1] + c[1] + c[2] + c[2];
    }
    const num = parseInt(c, 16);
    const r = (num >> 16) & 255;
    const g = (num >> 8) & 255;
    const b = num & 255;
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }
}

window.MartianCylinder = MartianCylinder;
