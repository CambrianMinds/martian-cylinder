/**
 * Martian Cylinder Photogrammetry Application Controller
 * Handles viewport management, interaction gestures, image pipeline,
 * telemetry updates, presets, and export utilities.
 */

(function () {
  'use strict';

  // --- State Variables ---
  const state = {
    // Canvas & Viewport
    viewport: {
      panX: 0,
      panY: 0,
      zoom: 1.0,
      minZoom: 0.1,
      maxZoom: 15.0
    },

    // Background Image
    image: null,
    imageWidth: 800,
    imageHeight: 600,
    imageFilters: {
      brightness: 100,
      contrast: 100,
      invert: false,
      grayscale: false,
      sobel: false
    },
    sobelCacheCanvas: null,

    // Interaction Gestures
    dragMode: null, // 'move', 'resize', 'rotate', 'tilt', 'pan'
    dragStart: {
      screenX: 0,
      screenY: 0,
      worldX: 0,
      worldY: 0,
      cylX: 0,
      cylY: 0,
      cylScale: 1.0,
      cylRot: 0,
      cylTilt: 0,
      initDist: 1,
      initAngle: 0,
      handleKey: null
    },

    // Spacebar Panning
    isSpacePressed: false,

    // Measurement Calibration
    calibration: {
      mmPerPixel: 0.317 // Sol 3556 Mastcam-100 ground-projected scale (3.96m distance, -22° elevation)
    }
  };

  // Instantiate the Martian Cylinder (Pre-calibrated to Sol 3556 Figure 4 Fit: 110×34 px, θ=218°, Tilt=156°, AR=3.24:1)
  const cylinder = new MartianCylinder({
    x: 246.8,
    y: 268.7,
    baseLength: 110,
    baseDiameter: 34,
    scale: 1.0,
    rotation: 218 * Math.PI / 180,
    tilt: 156 * Math.PI / 180,
    camRatio: 3.96,
    color: '#38bdf8',
    renderMode: 'semi-transparent'
  });

  // DOM Elements
  const elements = {
    canvas: document.getElementById('viewportCanvas'),
    viewportContainer: document.getElementById('canvasViewport'),
    fileInput: document.getElementById('imageFileInput'),
    btnOpen: document.getElementById('btnOpenImage'),
    btnPaste: document.getElementById('btnPasteImage'),
    btnExport: document.getElementById('btnExportImage'),
    btnResetView: document.getElementById('btnResetView'),
    btnFitImage: document.getElementById('btnFitImage'),
    btnFocusCylinder: document.getElementById('btnFocusCylinder'),
    btnCenterCylinder: document.getElementById('btnCenterCylinder'),
    dropOverlay: document.getElementById('dropZoneOverlay'),
    gestureTooltip: document.getElementById('gestureTooltip'),

    // HUD Telemetry
    teleAngle: document.getElementById('teleAngle'),
    teleTilt: document.getElementById('teleTilt'),
    teleFrontCap: document.getElementById('teleFrontCap'),
    teleBackCap: document.getElementById('teleBackCap'),
    telePerspRatio: document.getElementById('telePerspRatio'),
    teleDimensions: document.getElementById('teleDimensions'),
    teleRatio: document.getElementById('teleRatio'),
    telePhysical: document.getElementById('telePhysical'),
    zoomIndicator: document.getElementById('zoomIndicator'),

    // Control Inputs (Sliders & Numeric Digits)
    scaleSlider: document.getElementById('scaleSlider'),
    scaleInput: document.getElementById('scaleInput'),
    rotSlider: document.getElementById('rotSlider'),
    rotInput: document.getElementById('rotInput'),
    tiltSlider: document.getElementById('tiltSlider'),
    tiltInput: document.getElementById('tiltInput'),
    camRatioSlider: document.getElementById('camRatioSlider'),
    camRatioInput: document.getElementById('camRatioInput'),
    aspectSlider: document.getElementById('aspectSlider'),
    aspectInput: document.getElementById('aspectInput'),
    lengthSlider: document.getElementById('lengthSlider'),
    lengthInput: document.getElementById('lengthInput'),
    diaSlider: document.getElementById('diaSlider'),
    diaInput: document.getElementById('diaInput'),
    lineWidthSlider: document.getElementById('lineWidthSlider'),
    lineWidthInput: document.getElementById('lineWidthInput'),
    linePresets: document.querySelectorAll('.line-preset'),
    opacitySlider: document.getElementById('opacitySlider'),
    opacityInput: document.getElementById('opacityInput'),
    btnNasaCalib: document.getElementById('btnNasaCalib'),
    colorPicker: document.getElementById('colorPicker'),
    colorDots: document.querySelectorAll('.color-dot'),

    // Toggles
    toggleHandles: document.getElementById('toggleHandles'),
    btnToggleHandles: document.getElementById('btnToggleHandles'),
    btnToggleHandlesText: document.getElementById('btnToggleHandlesText'),
    iconHandlesOn: document.getElementById('iconHandlesOn'),
    iconHandlesOff: document.getElementById('iconHandlesOff'),
    toggleAxis: document.getElementById('toggleAxis'),
    toggleEllipseAxes: document.getElementById('toggleEllipseAxes'),
    toggleShadow: document.getElementById('toggleShadow'),
    toggleLockAspect: document.getElementById('toggleLockAspect'),
    filterSobel: document.getElementById('filterSobel'),
    filterInvert: document.getElementById('filterInvert'),
    filterGrayscale: document.getElementById('filterGrayscale'),
    brightnessSlider: document.getElementById('brightnessSlider'),
    contrastSlider: document.getElementById('contrastSlider'),
    calibInput: document.getElementById('calibMmPerPx'),

    // Quick angle buttons
    angleBtns: document.querySelectorAll('.angle-btn'),
    renderModeBtns: document.querySelectorAll('.render-mode-btn'),
    presetChips: document.querySelectorAll('.preset-chip'),

    // Toast & Modals
    toastContainer: document.getElementById('toastContainer'),
    btnHelp: document.getElementById('btnHelp'),
    modalHelp: document.getElementById('modalHelp'),
    modalClose: document.getElementById('modalClose')
  };

  const ctx = elements.canvas.getContext('2d');

  // --- Initialization ---
  function init() {
    setupCanvasDPI();
    bindEvents();
    syncControlsFromCylinder();

    // Load initial default image
    loadDefaultImage();

    // Start render loop
    requestAnimationFrame(renderLoop);
  }

  // Handle HiDPI Screen Rendering
  function setupCanvasDPI() {
    const rect = elements.viewportContainer.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;

    elements.canvas.width = Math.round(rect.width * dpr);
    elements.canvas.height = Math.round(rect.height * dpr);
    elements.canvas.style.width = `${rect.width}px`;
    elements.canvas.style.height = `${rect.height}px`;

    ctx.scale(dpr, dpr);
  }

  // --- Image Loading Pipeline ---
  function loadDefaultImage() {
    if (window.DEFAULT_IMAGE) {
      loadImageSource(window.DEFAULT_IMAGE);
    } else {
      loadImageSource('../data/crop_bottom_right.png');
    }
  }

  function loadImageSource(src, presetKey = null) {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      state.image = img;
      state.imageWidth = img.naturalWidth || img.width;
      state.imageHeight = img.naturalHeight || img.height;
      state.sobelCacheCanvas = null; // Invalidate Sobel cache

      // Center the cylinder on the Sol 3556 anomaly if loading the default 500x450 crop, otherwise image center
      if (state.imageWidth === 500 && state.imageHeight === 450) {
        cylinder.x = 246.8;
        cylinder.y = 268.7;
      } else {
        cylinder.x = state.imageWidth / 2;
        cylinder.y = state.imageHeight / 2;
      }

      // Fit image inside viewport so cylinder on Mars is centered on user's screen
      fitImageToViewport();

      showToast(`Loaded image: ${state.imageWidth}×${state.imageHeight} px`);
      triggerRedraw();
    };
    img.onerror = () => {
      // Create a simulated Mars surface placeholder canvas if file not found
      createFallbackMarsCanvas();
    };
    img.src = src;
  }

  function createFallbackMarsCanvas() {
    const fallback = document.createElement('canvas');
    fallback.width = 720;
    fallback.height = 540;
    const fctx = fallback.getContext('2d');

    // Martian terrain gradient
    const grad = fctx.createLinearGradient(0, 0, 720, 540);
    grad.addColorStop(0, '#8c4b2d');
    grad.addColorStop(0.5, '#b45f3c');
    grad.addColorStop(1, '#66321b');
    fctx.fillStyle = grad;
    fctx.fillRect(0, 0, 720, 540);

    // Dust & regolith texture
    for (let i = 0; i < 3000; i++) {
      const rx = Math.random() * 720;
      const ry = Math.random() * 540;
      const r = Math.random() * 2.5;
      fctx.fillStyle = Math.random() > 0.5 ? 'rgba(255,200,160,0.15)' : 'rgba(40,20,10,0.2)';
      fctx.beginPath();
      fctx.arc(rx, ry, r, 0, Math.PI * 2);
      fctx.fill();
    }

    state.image = fallback;
    state.imageWidth = 720;
    state.imageHeight = 540;
    fitImageToViewport();
    triggerRedraw();
  }

  // --- Real-Time Sobel Edge Detection ---
  function computeSobel(sourceImg) {
    const w = state.imageWidth;
    const h = state.imageHeight;
    const offCanvas = document.createElement('canvas');
    offCanvas.width = w;
    offCanvas.height = h;
    const offCtx = offCanvas.getContext('2d');
    offCtx.drawImage(sourceImg, 0, 0, w, h);

    const srcData = offCtx.getImageData(0, 0, w, h);
    const data = srcData.data;
    const outData = offCtx.createImageData(w, h);
    const out = outData.data;

    // Convert to grayscale intensity buffer
    const gray = new Float32Array(w * h);
    for (let i = 0, j = 0; i < data.length; i += 4, j++) {
      gray[j] = 0.299 * data[i] + 0.587 * data[i + 1] + 0.114 * data[i + 2];
    }

    // Sobel 3x3 kernels
    for (let y = 1; y < h - 1; y++) {
      for (let x = 1; x < w - 1; x++) {
        const idx = y * w + x;

        const gx =
          -gray[idx - w - 1] + gray[idx - w + 1]
          - 2 * gray[idx - 1] + 2 * gray[idx + 1]
          - gray[idx + w - 1] + gray[idx + w + 1];

        const gy =
          -gray[idx - w - 1] - 2 * gray[idx - w] - gray[idx - w + 1]
          + gray[idx + w - 1] + 2 * gray[idx + w] + gray[idx + w + 1];

        const mag = Math.min(255, Math.hypot(gx, gy) * 1.5);
        const outIdx = idx * 4;

        // Invert or high contrast neon green edges on dark background
        out[outIdx] = 0;          // R
        out[outIdx + 1] = mag;    // G (Green edges!)
        out[outIdx + 2] = mag * 0.8; // B (Cyan tint)
        out[outIdx + 3] = 255;
      }
    }

    offCtx.putImageData(outData, 0, 0);
    return offCanvas;
  }

  // --- Coordinate Transformations ---
  function screenToWorld(sx, sy) {
    const { panX, panY, zoom } = state.viewport;
    return {
      x: (sx - panX) / zoom,
      y: (sy - panY) / zoom
    };
  }

  function worldToScreen(wx, wy) {
    const { panX, panY, zoom } = state.viewport;
    return {
      x: wx * zoom + panX,
      y: wy * zoom + panY
    };
  }

  // --- Viewport Navigation (Pan & Zoom) ---
  function zoomAt(factor, clientX, clientY) {
    const rect = elements.canvas.getBoundingClientRect();
    const sx = clientX - rect.left;
    const sy = clientY - rect.top;

    const newZoom = Math.min(state.viewport.maxZoom, Math.max(state.viewport.minZoom, state.viewport.zoom * factor));
    const zoomRatio = newZoom / state.viewport.zoom;

    state.viewport.panX = sx - (sx - state.viewport.panX) * zoomRatio;
    state.viewport.panY = sy - (sy - state.viewport.panY) * zoomRatio;
    state.viewport.zoom = newZoom;

    updateZoomDisplay();
    triggerRedraw();
  }

  function fitImageToViewport() {
    if (!state.image) return;
    const rect = elements.viewportContainer.getBoundingClientRect();
    const sidebarOffset = window.innerWidth > 768 ? 320 : 0;
    const availW = Math.max(200, rect.width - sidebarOffset - 40);
    const availH = Math.max(200, rect.height - 80);

    const scale = Math.min(availW / state.imageWidth, availH / state.imageHeight, 1.8);
    state.viewport.zoom = Math.max(0.2, scale);
    state.viewport.panX = sidebarOffset + (rect.width - sidebarOffset - state.imageWidth * state.viewport.zoom) / 2;
    state.viewport.panY = (rect.height - state.imageHeight * state.viewport.zoom) / 2;

    updateZoomDisplay();
    triggerRedraw();
  }

  function focusOnCylinder(targetZoom = null) {
    if (!state.image) return;
    const rect = elements.viewportContainer.getBoundingClientRect();
    const sidebarOffset = window.innerWidth > 768 ? 320 : 0;
    const screenCenterX = sidebarOffset + (rect.width - sidebarOffset) / 2;
    const screenCenterY = rect.height / 2;

    if (targetZoom) {
      state.viewport.zoom = Math.min(state.viewport.maxZoom, Math.max(state.viewport.minZoom, targetZoom));
    }
    state.viewport.panX = screenCenterX - cylinder.x * state.viewport.zoom;
    state.viewport.panY = screenCenterY - cylinder.y * state.viewport.zoom;

    updateZoomDisplay();
    triggerRedraw();
  }

  function resetView100() {
    const rect = elements.viewportContainer.getBoundingClientRect();
    const sidebarOffset = window.innerWidth > 768 ? 320 : 0;
    state.viewport.zoom = 1.0;
    state.viewport.panX = sidebarOffset + (rect.width - sidebarOffset - state.imageWidth) / 2;
    state.viewport.panY = (rect.height - state.imageHeight) / 2;
    updateZoomDisplay();
    triggerRedraw();
  }

  function updateZoomDisplay() {
    elements.zoomIndicator.textContent = `${Math.round(state.viewport.zoom * 100)}%`;
  }

  // --- Rendering Pipeline ---
  let needsRedraw = true;

  function triggerRedraw() {
    needsRedraw = true;
  }

  function renderLoop() {
    if (needsRedraw) {
      renderScene();
      updateTelemetry();
      needsRedraw = false;
    }
    requestAnimationFrame(renderLoop);
  }

  function renderScene() {
    const rect = elements.viewportContainer.getBoundingClientRect();
    const dpr = window.devicePixelRatio || 1;

    // Clear canvas
    ctx.save();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, elements.canvas.width, elements.canvas.height);
    ctx.restore();

    ctx.save();
    // Apply viewport camera transform
    ctx.translate(state.viewport.panX, state.viewport.panY);
    ctx.scale(state.viewport.zoom, state.viewport.zoom);

    // 1. Draw Background Image
    if (state.image) {
      drawBackgroundImage();
    }

    // 2. Draw Cylinder Model & Interactive Handles
    cylinder.render(ctx, state.viewport.zoom);

    ctx.restore();
  }

  function drawBackgroundImage() {
    const { imageWidth, imageHeight, imageFilters } = state;
    ctx.save();

    // Check if Sobel edge filter is active
    if (imageFilters.sobel) {
      if (!state.sobelCacheCanvas) {
        state.sobelCacheCanvas = computeSobel(state.image);
      }
      ctx.drawImage(state.sobelCacheCanvas, 0, 0, imageWidth, imageHeight);
    } else {
      // Build CSS Filter string
      const filters = [];
      if (imageFilters.brightness !== 100) filters.push(`brightness(${imageFilters.brightness}%)`);
      if (imageFilters.contrast !== 100) filters.push(`contrast(${imageFilters.contrast}%)`);
      if (imageFilters.invert) filters.push('invert(100%)');
      if (imageFilters.grayscale) filters.push('grayscale(100%)');

      ctx.filter = filters.length > 0 ? filters.join(' ') : 'none';
      ctx.drawImage(state.image, 0, 0, imageWidth, imageHeight);
    }

    // Subtle image border
    ctx.filter = 'none';
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.2)';
    ctx.lineWidth = 1 / state.viewport.zoom;
    ctx.strokeRect(0, 0, imageWidth, imageHeight);

    ctx.restore();
  }

  // --- Telemetry & Measurements Display ---
  function updateTelemetry() {
    const geo = cylinder.getGeometry();
    const deg = ((cylinder.rotation * 180 / Math.PI) % 360 + 360) % 360;
    const tiltDeg = ((cylinder.tilt * 180 / Math.PI) % 360 + 360) % 360;
    const lenPx = cylinder.length;
    const diaPx = cylinder.diameter;
    const ratio = cylinder.aspectRatio;

    elements.teleAngle.textContent = `${deg.toFixed(1)}°`;
    elements.teleTilt.textContent = `${tiltDeg.toFixed(1)}°`;

    if (elements.teleFrontCap) elements.teleFrontCap.textContent = `${Math.round(geo.nearR * 2)} px`;
    if (elements.teleBackCap) elements.teleBackCap.textContent = `${Math.round(geo.farR * 2)} px`;
    if (elements.telePerspRatio) elements.telePerspRatio.textContent = `${(geo.perspRatio * 100).toFixed(1)}%`;

    elements.teleDimensions.textContent = `${Math.round(lenPx)} × ${Math.round(diaPx)} px`;
    elements.teleRatio.textContent = `${ratio.toFixed(2)} : 1`;

    // Physical calibration calculation
    const mmPerPx = state.calibration.mmPerPixel;
    const lenMm = lenPx * mmPerPx;
    const diaMm = diaPx * mmPerPx;
    elements.telePhysical.textContent = `${lenMm.toFixed(1)} × ${diaMm.toFixed(1)} mm`;
  }

  // Toggle handles visibility across all UI controls
  function updateHandlesUI(visible) {
    cylinder.showHandles = visible;
    if (elements.toggleHandles) elements.toggleHandles.checked = visible;
    if (elements.btnToggleHandlesText) {
      elements.btnToggleHandlesText.textContent = visible ? 'Handles: ON' : 'Handles: OFF';
    }
    if (elements.iconHandlesOn && elements.iconHandlesOff) {
      elements.iconHandlesOn.style.display = visible ? 'inline-block' : 'none';
      elements.iconHandlesOff.style.display = visible ? 'none' : 'inline-block';
    }
    if (elements.btnToggleHandles) {
      if (visible) {
        elements.btnToggleHandles.style.borderColor = 'rgba(0, 240, 255, 0.4)';
        elements.btnToggleHandles.style.color = 'var(--accent-cyan)';
      } else {
        elements.btnToggleHandles.style.borderColor = 'rgba(255, 255, 255, 0.15)';
        elements.btnToggleHandles.style.color = 'var(--text-muted)';
      }
    }
    triggerRedraw();
  }

  // Synchronize input fields with cylinder model
  function syncControlsFromCylinder() {
    const deg = Math.round(((cylinder.rotation * 180 / Math.PI) % 360 + 360) % 360);
    const tiltDeg = Math.round(((cylinder.tilt * 180 / Math.PI) % 360 + 360) % 360);
    const scalePct = Math.round(cylinder.scale * 100);
    const lenPx = Math.round(cylinder.length);
    const diaPx = Math.round(cylinder.diameter);
    const aspect = cylinder.aspectRatio;
    const camRatio = cylinder.camRatio;
    const opacityPct = Math.round(cylinder.opacity * 100);
    const lw = cylinder.lineWidth || 1.5;

    if (elements.scaleSlider) elements.scaleSlider.value = scalePct;
    if (elements.scaleInput && document.activeElement !== elements.scaleInput) {
      elements.scaleInput.value = scalePct;
    }

    if (elements.rotSlider) elements.rotSlider.value = deg;
    if (elements.rotInput && document.activeElement !== elements.rotInput) {
      elements.rotInput.value = deg;
    }

    if (elements.tiltSlider) elements.tiltSlider.value = tiltDeg;
    if (elements.tiltInput && document.activeElement !== elements.tiltInput) {
      elements.tiltInput.value = tiltDeg;
    }

    if (elements.camRatioSlider) elements.camRatioSlider.value = camRatio;
    if (elements.camRatioInput && document.activeElement !== elements.camRatioInput) {
      elements.camRatioInput.value = camRatio.toFixed(1);
    }

    if (elements.aspectSlider) elements.aspectSlider.value = aspect.toFixed(2);
    if (elements.aspectInput && document.activeElement !== elements.aspectInput) {
      elements.aspectInput.value = aspect.toFixed(2);
    }

    if (elements.lengthSlider) elements.lengthSlider.value = lenPx;
    if (elements.lengthInput && document.activeElement !== elements.lengthInput) {
      elements.lengthInput.value = lenPx;
    }

    if (elements.diaSlider) elements.diaSlider.value = diaPx;
    if (elements.diaInput && document.activeElement !== elements.diaInput) {
      elements.diaInput.value = diaPx;
    }

    if (elements.lineWidthSlider) elements.lineWidthSlider.value = lw;
    if (elements.lineWidthInput && document.activeElement !== elements.lineWidthInput) {
      elements.lineWidthInput.value = lw;
    }

    if (elements.opacitySlider) elements.opacitySlider.value = opacityPct;
    if (elements.opacityInput && document.activeElement !== elements.opacityInput) {
      elements.opacityInput.value = opacityPct;
    }

    if (elements.toggleAxis) elements.toggleAxis.checked = cylinder.showAxis;
    if (elements.toggleEllipseAxes) elements.toggleEllipseAxes.checked = cylinder.showEllipseAxes;
    if (elements.toggleShadow) elements.toggleShadow.checked = cylinder.showShadow;

    if (elements.colorPicker) elements.colorPicker.value = cylinder.color;
  }

  // --- Mouse & Gesture Interaction Engine ---
  function bindEvents() {
    const cvs = elements.canvas;

    // Window Resize
    window.addEventListener('resize', () => {
      setupCanvasDPI();
      triggerRedraw();
    });

    // Keyboard (Spacebar for Pan, Arrow keys for Nudge)
    window.addEventListener('keydown', onKeyDown);
    window.addEventListener('keyup', onKeyUp);

    // Mouse Interactions on Canvas
    cvs.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    cvs.addEventListener('wheel', onWheel, { passive: false });

    // Drag & Drop Files
    window.addEventListener('dragover', onDragOver);
    window.addEventListener('dragleave', onDragLeave);
    window.addEventListener('drop', onDrop);

    // Clipboard Paste (Ctrl+V)
    window.addEventListener('paste', onPaste);

    // File Input
    elements.fileInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) loadFile(file);
    });

    elements.btnOpen.addEventListener('click', () => elements.fileInput.click());
    elements.btnPaste.addEventListener('click', () => {
      navigator.clipboard?.read().then(items => {
        for (const item of items) {
          const type = item.types.find(t => t.startsWith('image/'));
          if (type) {
            item.getType(type).then(blob => loadFile(blob));
            return;
          }
        }
        showToast('No image in clipboard. Try copying an image first!');
      }).catch(() => {
        showToast('Press Ctrl+V to paste an image!');
      });
    });

    // Preset chips
    elements.presetChips.forEach(chip => {
      chip.addEventListener('click', () => {
        const key = chip.dataset.preset;
        if (window.IMAGE_PRESETS && window.IMAGE_PRESETS[key]) {
          loadImageSource(window.IMAGE_PRESETS[key], key);
        } else if (key === 'crop_bottom_right') {
          loadImageSource('data/crop_bottom_right.png', key);
        } else if (key === 'user_visual') {
          loadImageSource('user-visual-interpretation.png', key);
        }
      });
    });

    // Control Sliders and Direct Digit Inputs
    elements.scaleSlider?.addEventListener('input', (e) => {
      cylinder.scale = parseFloat(e.target.value) / 100;
      if (elements.scaleInput) elements.scaleInput.value = e.target.value;
      triggerRedraw();
    });
    elements.scaleInput?.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      if (!isNaN(val) && val > 0) {
        cylinder.scale = val / 100;
        if (elements.scaleSlider) elements.scaleSlider.value = Math.min(600, Math.max(10, val));
        triggerRedraw();
      }
    });

    elements.rotSlider?.addEventListener('input', (e) => {
      const deg = parseFloat(e.target.value);
      cylinder.rotation = (deg * Math.PI) / 180;
      if (elements.rotInput) elements.rotInput.value = Math.round(deg);
      triggerRedraw();
    });
    elements.rotInput?.addEventListener('input', (e) => {
      const deg = parseFloat(e.target.value);
      if (!isNaN(deg)) {
        cylinder.rotation = (deg * Math.PI) / 180;
        if (elements.rotSlider) elements.rotSlider.value = ((Math.round(deg) % 360) + 360) % 360;
        triggerRedraw();
      }
    });

    elements.tiltSlider?.addEventListener('input', (e) => {
      const deg = parseFloat(e.target.value);
      cylinder.tilt = (deg * Math.PI) / 180;
      if (elements.tiltInput) elements.tiltInput.value = Math.round(deg);
      triggerRedraw();
    });
    elements.tiltInput?.addEventListener('input', (e) => {
      const deg = parseFloat(e.target.value);
      if (!isNaN(deg)) {
        cylinder.tilt = (deg * Math.PI) / 180;
        if (elements.tiltSlider) elements.tiltSlider.value = ((Math.round(deg) % 360) + 360) % 360;
        triggerRedraw();
      }
    });

    elements.aspectSlider?.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      cylinder.setAspectRatio(val);
      if (elements.aspectInput) elements.aspectInput.value = val.toFixed(2);
      if (elements.lengthSlider) elements.lengthSlider.value = Math.round(cylinder.length);
      if (elements.lengthInput) elements.lengthInput.value = Math.round(cylinder.length);
      triggerRedraw();
    });
    elements.aspectInput?.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      if (!isNaN(val) && val > 0) {
        cylinder.setAspectRatio(val);
        if (elements.aspectSlider) elements.aspectSlider.value = Math.min(6, Math.max(0.2, val));
        if (elements.lengthSlider) elements.lengthSlider.value = Math.round(cylinder.length);
        if (elements.lengthInput) elements.lengthInput.value = Math.round(cylinder.length);
        triggerRedraw();
      }
    });

    elements.lengthSlider?.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      cylinder.setLength(val);
      if (elements.lengthInput) elements.lengthInput.value = Math.round(val);
      if (elements.aspectSlider) elements.aspectSlider.value = cylinder.aspectRatio.toFixed(2);
      if (elements.aspectInput) elements.aspectInput.value = cylinder.aspectRatio.toFixed(2);
      triggerRedraw();
    });
    elements.lengthInput?.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      if (!isNaN(val) && val > 0) {
        cylinder.setLength(val);
        if (elements.lengthSlider) elements.lengthSlider.value = Math.min(800, Math.max(20, val));
        if (elements.aspectSlider) elements.aspectSlider.value = cylinder.aspectRatio.toFixed(2);
        if (elements.aspectInput) elements.aspectInput.value = cylinder.aspectRatio.toFixed(2);
        triggerRedraw();
      }
    });

    elements.diaSlider?.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      cylinder.setDiameter(val);
      if (elements.diaInput) elements.diaInput.value = Math.round(val);
      if (elements.aspectSlider) elements.aspectSlider.value = cylinder.aspectRatio.toFixed(2);
      if (elements.aspectInput) elements.aspectInput.value = cylinder.aspectRatio.toFixed(2);
      triggerRedraw();
    });
    elements.diaInput?.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      if (!isNaN(val) && val > 0) {
        cylinder.setDiameter(val);
        if (elements.diaSlider) elements.diaSlider.value = Math.min(500, Math.max(10, val));
        if (elements.aspectSlider) elements.aspectSlider.value = cylinder.aspectRatio.toFixed(2);
        if (elements.aspectInput) elements.aspectInput.value = cylinder.aspectRatio.toFixed(2);
        triggerRedraw();
      }
    });

    // Wireframe Line Width Slider and Direct Input
    elements.lineWidthSlider?.addEventListener('input', (e) => {
      const lw = parseFloat(e.target.value);
      cylinder.lineWidth = lw;
      if (elements.lineWidthInput) elements.lineWidthInput.value = lw;
      triggerRedraw();
    });
    elements.lineWidthInput?.addEventListener('input', (e) => {
      const lw = parseFloat(e.target.value);
      if (!isNaN(lw) && lw > 0) {
        cylinder.lineWidth = lw;
        if (elements.lineWidthSlider) elements.lineWidthSlider.value = Math.min(8, Math.max(0.5, lw));
        triggerRedraw();
      }
    });

    elements.linePresets?.forEach(btn => {
      btn.addEventListener('click', () => {
        const lw = parseFloat(btn.dataset.width);
        cylinder.lineWidth = lw;
        if (elements.lineWidthSlider) elements.lineWidthSlider.value = lw;
        if (elements.lineWidthInput) elements.lineWidthInput.value = lw;
        triggerRedraw();
        showToast(`Line thickness set to ${lw}px`);
      });
    });

    elements.opacitySlider?.addEventListener('input', (e) => {
      cylinder.opacity = parseFloat(e.target.value) / 100;
      if (elements.opacityInput) elements.opacityInput.value = e.target.value;
      triggerRedraw();
    });
    elements.opacityInput?.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      if (!isNaN(val) && val >= 0) {
        cylinder.opacity = Math.min(1.0, Math.max(0.05, val / 100));
        if (elements.opacitySlider) elements.opacitySlider.value = Math.min(100, Math.max(5, val));
        triggerRedraw();
      }
    });

    // Color selection
    elements.colorPicker.addEventListener('input', (e) => {
      cylinder.color = e.target.value;
      elements.colorDots.forEach(d => d.classList.remove('active'));
      triggerRedraw();
    });

    elements.colorDots.forEach(dot => {
      dot.addEventListener('click', () => {
        const col = dot.dataset.color;
        cylinder.color = col;
        elements.colorPicker.value = col;
        elements.colorDots.forEach(d => d.classList.remove('active'));
        dot.classList.add('active');
        triggerRedraw();
      });
    });

    // Quick rotation preset buttons
    document.querySelectorAll('.rot-preset').forEach(btn => {
      btn.addEventListener('click', () => {
        const deg = parseFloat(btn.dataset.angle);
        cylinder.rotation = (deg * Math.PI) / 180;
        syncControlsFromCylinder();
        triggerRedraw();
      });
    });

    // Quick 360° tilt preset buttons
    document.querySelectorAll('.tilt-preset').forEach(btn => {
      btn.addEventListener('click', () => {
        const deg = parseFloat(btn.dataset.tilt);
        cylinder.tilt = (deg * Math.PI) / 180;
        syncControlsFromCylinder();
        triggerRedraw();
      });
    });

    // Perspective depth / camera distance slider & numeric input
    if (elements.camRatioSlider) {
      elements.camRatioSlider.addEventListener('input', (e) => {
        cylinder.camRatio = parseFloat(e.target.value);
        if (elements.camRatioInput) elements.camRatioInput.value = cylinder.camRatio.toFixed(1);
        triggerRedraw();
      });
    }
    if (elements.camRatioInput) {
      elements.camRatioInput.addEventListener('input', (e) => {
        const val = parseFloat(e.target.value);
        if (!isNaN(val) && val >= 1.0) {
          cylinder.camRatio = val;
          if (elements.camRatioSlider) elements.camRatioSlider.value = Math.min(10, Math.max(1.0, val));
          triggerRedraw();
        }
      });
    }

    // NASA Sol 3556 Mastcam-100 Calibration Preset Button
    if (elements.btnNasaCalib) {
      elements.btnNasaCalib.addEventListener('click', () => {
        // Verified Mastcam-100 optical geometry & photogrammetric fit from Sol 3556 paper (Section 4.3, Figure 4):
        // Sequence: mcam02517, Focal length: 100mm, Focus distance: 3.957m (2705 counts)
        // Cylinder fit: 110x34 px (AR 3.24:1), Planar angle: 218°, Perspective tilt: 156° (alpha=24.0°)
        cylinder.scale = 1.0;
        cylinder.baseDiameter = 34;
        cylinder.baseLength = 110;
        cylinder.aspectRatio = 110 / 34;
        cylinder.rotation = (218 * Math.PI) / 180;
        cylinder.tilt = (156 * Math.PI) / 180;
        cylinder.camRatio = 3.96;
        if (state.imageWidth === 500 && state.imageHeight === 450) {
          cylinder.x = 246.8;
          cylinder.y = 268.7;
        }
        syncControlsFromCylinder();
        triggerRedraw();
        showToast('NASA Sol 3556 Fit Applied: 110×34 px (AR 3.24:1), θ=218°, Tilt=156°, R=3.96m');
      });
    }

    // Render mode buttons
    elements.renderModeBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        elements.renderModeBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        cylinder.renderMode = btn.dataset.mode;
        triggerRedraw();
      });
    });

    // Toggles
    elements.toggleHandles?.addEventListener('change', (e) => {
      updateHandlesUI(e.target.checked);
    });

    elements.btnToggleHandles?.addEventListener('click', () => {
      updateHandlesUI(!cylinder.showHandles);
      showToast(cylinder.showHandles ? 'Handles Shown' : 'Handles Hidden (Clean View)');
    });

    elements.toggleAxis.addEventListener('change', (e) => {
      cylinder.showAxis = e.target.checked;
      triggerRedraw();
    });

    elements.toggleEllipseAxes.addEventListener('change', (e) => {
      cylinder.showEllipseAxes = e.target.checked;
      triggerRedraw();
    });

    elements.toggleShadow.addEventListener('change', (e) => {
      cylinder.showShadow = e.target.checked;
      triggerRedraw();
    });

    // Image Adjustments
    elements.filterSobel.addEventListener('change', (e) => {
      state.imageFilters.sobel = e.target.checked;
      triggerRedraw();
    });

    elements.filterInvert.addEventListener('change', (e) => {
      state.imageFilters.invert = e.target.checked;
      triggerRedraw();
    });

    elements.filterGrayscale.addEventListener('change', (e) => {
      state.imageFilters.grayscale = e.target.checked;
      triggerRedraw();
    });

    elements.brightnessSlider.addEventListener('input', (e) => {
      state.imageFilters.brightness = parseInt(e.target.value, 10);
      triggerRedraw();
    });

    elements.contrastSlider.addEventListener('input', (e) => {
      state.imageFilters.contrast = parseInt(e.target.value, 10);
      triggerRedraw();
    });

    // Calibration input
    elements.calibInput.addEventListener('input', (e) => {
      const val = parseFloat(e.target.value);
      if (val > 0) {
        state.calibration.mmPerPixel = val;
        updateTelemetry();
      }
    });

    document.querySelectorAll('.calib-preset-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const val = parseFloat(btn.dataset.scale);
        if (val > 0) {
          state.calibration.mmPerPixel = val;
          if (elements.calibInput) elements.calibInput.value = val.toFixed(3);
          updateTelemetry();
          showToast(`Scale calibrated: ${val.toFixed(3)} mm/px`);
        }
      });
    });

    // Buttons
    elements.btnFitImage.addEventListener('click', fitImageToViewport);
    elements.btnResetView.addEventListener('click', resetView100);
    elements.btnFocusCylinder?.addEventListener('click', () => {
      focusOnCylinder(1.5);
      showToast('Centered on Cylinder Anomaly');
    });
    elements.btnCenterCylinder.addEventListener('click', () => {
      if (state.image) {
        cylinder.x = state.imageWidth / 2;
        cylinder.y = state.imageHeight / 2;
      }
      triggerRedraw();
      showToast('Cylinder centered');
    });

    elements.btnExport.addEventListener('click', exportCompositeImage);

    // Help Modal
    elements.btnHelp.addEventListener('click', () => elements.modalHelp.classList.add('open'));
    elements.modalClose.addEventListener('click', () => elements.modalHelp.classList.remove('open'));
    elements.modalHelp.addEventListener('click', (e) => {
      if (e.target === elements.modalHelp) elements.modalHelp.classList.remove('open');
    });
  }

  // --- Mouse Event Handlers ---
  function onMouseDown(e) {
    const rect = elements.canvas.getBoundingClientRect();
    const sx = e.clientX - rect.left;
    const sy = e.clientY - rect.top;
    const world = screenToWorld(sx, sy);

    // Middle click OR Spacebar held = Pan
    if (e.button === 1 || state.isSpacePressed) {
      state.dragMode = 'pan';
      state.dragStart = { screenX: e.clientX, screenY: e.clientY };
      elements.viewportContainer.classList.add('panning');
      e.preventDefault();
      return;
    }

    if (e.button === 0) {
      // Hit test cylinder handles
      const hit = cylinder.hitTest(world.x, world.y, state.viewport.zoom);

      if (hit) {
        if (hit === 'rotation') {
          state.dragMode = 'rotate';
          const angle = Math.atan2(world.y - cylinder.y, world.x - cylinder.x);
          state.dragStart = {
            cylRot: cylinder.rotation,
            initAngle: angle
          };
        } else if (hit === 'length') {
          // Adjust Cylinder Length directly by dragging rear handle (anchors front cap!)
          state.dragMode = 'length';
          const geo = cylinder.getGeometry();
          const dx = geo.farX - geo.nearX;
          const dy = geo.farY - geo.nearY;
          const dist = Math.hypot(dx, dy);
          const dirX = dist > 1e-4 ? dx / dist : -geo.ux;
          const dirY = dist > 1e-4 ? dy / dist : -geo.uy;

          state.dragStart = {
            nearX: geo.nearX,
            nearY: geo.nearY,
            dirX: dirX,
            dirY: dirY,
            initLength: cylinder.length,
            initWorldX: world.x,
            initWorldY: world.y
          };
        } else if (hit.startsWith('corner-')) {
          // RESIZE WHILE STRICTLY MAINTAINING ASPECT RATIO
          state.dragMode = 'resize';
          const dist = Math.hypot(world.x - cylinder.x, world.y - cylinder.y);
          state.dragStart = {
            handleKey: hit,
            cylScale: cylinder.scale,
            initDist: Math.max(1, dist)
          };
        } else if (hit === 'tilt') {
          // Adjust 3D Perspective Tilt directly
          state.dragMode = 'tilt';
          state.dragStart = {
            screenY: e.clientY,
            cylTilt: cylinder.tilt
          };
        } else if (hit === 'body') {
          // Move cylinder
          state.dragMode = 'move';
          state.dragStart = {
            worldX: world.x,
            worldY: world.y,
            cylX: cylinder.x,
            cylY: cylinder.y
          };
        }
        cylinder.isSelected = true;
        triggerRedraw();
        e.preventDefault();
      } else {
        // Clicked empty area
        // Deselect or do nothing
      }
    }
  }

  function onMouseMove(e) {
    const rect = elements.canvas.getBoundingClientRect();
    const sx = e.clientX - rect.left;
    const sy = e.clientY - rect.top;
    const world = screenToWorld(sx, sy);

    if (state.dragMode) {
      handleDragGesture(e, world);
      return;
    }

    // Hover Cursor Management
    if (state.isSpacePressed) {
      elements.canvas.style.cursor = 'grab';
      return;
    }

    const hit = cylinder.hitTest(world.x, world.y, state.viewport.zoom);
    cylinder.hoverHandle = hit;

    if (!hit) {
      elements.canvas.style.cursor = 'default';
      hideTooltip();
    } else if (hit === 'rotation') {
      elements.canvas.style.cursor = 'crosshair';
      showTooltip(e.clientX, e.clientY, `Rotate: ${Math.round(((cylinder.rotation * 180 / Math.PI) % 360 + 360) % 360)}°`);
    } else if (hit === 'length') {
      elements.canvas.style.cursor = 'ew-resize';
      showTooltip(e.clientX, e.clientY, `Drag to Change Length: ${Math.round(cylinder.length)} px`);
    } else if (hit.startsWith('corner-')) {
      elements.canvas.style.cursor = 'nwse-resize';
      showTooltip(e.clientX, e.clientY, `Resize (${Math.round(cylinder.scale * 100)}%) [Ratio Locked]`);
    } else if (hit === 'tilt') {
      elements.canvas.style.cursor = 'ns-resize';
      showTooltip(e.clientX, e.clientY, `Perspective Tilt: ${Math.round(cylinder.tilt * 180 / Math.PI)}°`);
    } else if (hit === 'body') {
      elements.canvas.style.cursor = 'move';
      showTooltip(e.clientX, e.clientY, 'Drag to Position');
    }

    triggerRedraw();
  }

  function handleDragGesture(e, world) {
    const { dragMode, dragStart } = state;

    if (dragMode === 'pan') {
      const dx = e.clientX - dragStart.screenX;
      const dy = e.clientY - dragStart.screenY;
      state.viewport.panX += dx;
      state.viewport.panY += dy;
      dragStart.screenX = e.clientX;
      dragStart.screenY = e.clientY;
      triggerRedraw();
    } else if (dragMode === 'move') {
      // Move cylinder
      const dx = world.x - dragStart.worldX;
      const dy = world.y - dragStart.worldY;
      cylinder.x = dragStart.cylX + dx;
      cylinder.y = dragStart.cylY + dy;
      showTooltip(e.clientX, e.clientY, `X: ${Math.round(cylinder.x)} | Y: ${Math.round(cylinder.y)}`);
      triggerRedraw();
    } else if (dragMode === 'length') {
      // DRAG TO CHANGE LENGTH (only the back moves, front face strictly anchored!)
      const { dirX, dirY, initLength, initWorldX, initWorldY } = dragStart;
      const deltaX = world.x - initWorldX;
      const deltaY = world.y - initWorldY;
      const deltaProj = deltaX * dirX + deltaY * dirY;

      const newLength = Math.max(20, initLength + deltaProj);
      cylinder.setLength(newLength, true);

      syncControlsFromCylinder();
      showTooltip(
        e.clientX,
        e.clientY,
        `Length: ${Math.round(cylinder.length)} px [Front Fixed]`
      );
      triggerRedraw();
    } else if (dragMode === 'resize') {
      // UNIFORM RESIZE WHILE STRICTLY MAINTAINING ASPECT RATIO
      const currentDist = Math.hypot(world.x - cylinder.x, world.y - cylinder.y);
      const ratio = currentDist / dragStart.initDist;
      const newScale = Math.max(0.05, Math.min(20.0, dragStart.cylScale * ratio));

      cylinder.scale = newScale;
      syncControlsFromCylinder();

      showTooltip(
        e.clientX,
        e.clientY,
        `Size: ${Math.round(cylinder.length)}×${Math.round(cylinder.diameter)} px (${Math.round(newScale * 100)}%)`
      );
      triggerRedraw();
    } else if (dragMode === 'rotate') {
      // 360° PLANAR ROTATION
      const currentAngle = Math.atan2(world.y - cylinder.y, world.x - cylinder.x);
      let deltaAngle = currentAngle - dragStart.initAngle;
      let newRot = dragStart.cylRot + deltaAngle;

      // Snap to 15° if Shift key is pressed
      if (e.shiftKey) {
        const snap = 15 * Math.PI / 180;
        newRot = Math.round(newRot / snap) * snap;
      }

      cylinder.rotation = newRot;
      syncControlsFromCylinder();

      const deg = Math.round(((newRot * 180 / Math.PI) % 360 + 360) % 360);
      showTooltip(e.clientX, e.clientY, `Angle: ${deg}°${e.shiftKey ? ' (Snap 15°)' : ''}`);
      triggerRedraw();
    } else if (dragMode === 'tilt') {
      // 360° PERSPECTIVE TILT
      const dy = (e.clientY - dragStart.screenY) * 0.012;
      let newTilt = (dragStart.cylTilt - dy) % (Math.PI * 2);
      if (newTilt < 0) newTilt += Math.PI * 2;
      cylinder.tilt = newTilt;
      syncControlsFromCylinder();

      const tiltDeg = Math.round(((newTilt * 180 / Math.PI) % 360 + 360) % 360);
      showTooltip(e.clientX, e.clientY, `Perspective Tilt: ${tiltDeg}°`);
      triggerRedraw();
    }
  }

  function onMouseUp() {
    if (state.dragMode) {
      state.dragMode = null;
      elements.viewportContainer.classList.remove('panning');
      hideTooltip();
      triggerRedraw();
    }
  }

  function onWheel(e) {
    e.preventDefault();

    // If hovering over cylinder with Alt/Shift, resize cylinder; otherwise zoom viewport
    if (e.altKey && cylinder.hoverHandle) {
      const scaleDelta = e.deltaY < 0 ? 1.05 : 0.95;
      cylinder.scale = Math.max(0.05, Math.min(20.0, cylinder.scale * scaleDelta));
      syncControlsFromCylinder();
      triggerRedraw();
    } else {
      const zoomFactor = e.deltaY < 0 ? 1.12 : 0.89;
      zoomAt(zoomFactor, e.clientX, e.clientY);
    }
  }

  // --- Keyboard Shortcuts ---
  function onKeyDown(e) {
    if (e.code === 'Space' && !state.isSpacePressed && document.activeElement.tagName !== 'INPUT') {
      state.isSpacePressed = true;
      elements.viewportContainer.classList.add('panning');
      e.preventDefault();
    }

    // Micro-nudges with Arrow Keys
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.code) && document.activeElement.tagName !== 'INPUT') {
      const step = e.shiftKey ? 10 : 1;
      if (e.code === 'ArrowUp') cylinder.y -= step;
      if (e.code === 'ArrowDown') cylinder.y += step;
      if (e.code === 'ArrowLeft') cylinder.x -= step;
      if (e.code === 'ArrowRight') cylinder.x += step;
      triggerRedraw();
      e.preventDefault();
    }

    // Bracket keys [ and ] for 1-degree rotation nudge
    if (e.key === '[' || e.key === ']') {
      const rotStep = (e.shiftKey ? 5 : 1) * Math.PI / 180;
      cylinder.rotation += (e.key === ']' ? rotStep : -rotStep);
      syncControlsFromCylinder();
      triggerRedraw();
    }

    // Plus and Minus for scale
    if ((e.key === '+' || e.key === '=') && document.activeElement.tagName !== 'INPUT') {
      cylinder.scale = Math.min(20.0, cylinder.scale * 1.05);
      syncControlsFromCylinder();
      triggerRedraw();
    }
    if ((e.key === '-' || e.key === '_') && document.activeElement.tagName !== 'INPUT') {
      cylinder.scale = Math.max(0.05, cylinder.scale * 0.95);
      syncControlsFromCylinder();
      triggerRedraw();
    }

    // Toggle handles on/off with H key
    if ((e.key === 'h' || e.key === 'H') && document.activeElement.tagName !== 'INPUT') {
      updateHandlesUI(!cylinder.showHandles);
      showToast(cylinder.showHandles ? 'Handles Shown (H)' : 'Handles Hidden (Clean View)');
      e.preventDefault();
    }
  }

  function onKeyUp(e) {
    if (e.code === 'Space') {
      state.isSpacePressed = false;
      elements.viewportContainer.classList.remove('panning');
      triggerRedraw();
    }
  }

  // --- File Upload / Drag & Drop / Clipboard ---
  function loadFile(file) {
    if (!file || !file.type.startsWith('image/')) {
      showToast('Please select a valid image file');
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      loadImageSource(e.target.result, null);
    };
    reader.readAsDataURL(file);
  }

  function onDragOver(e) {
    e.preventDefault();
    elements.dropOverlay.classList.add('drag-over');
  }

  function onDragLeave(e) {
    if (e.clientX <= 0 || e.clientY <= 0 || e.clientX >= window.innerWidth || e.clientY >= window.innerHeight) {
      elements.dropOverlay.classList.remove('drag-over');
    }
  }

  function onDrop(e) {
    e.preventDefault();
    elements.dropOverlay.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file) loadFile(file);
  }

  function onPaste(e) {
    const items = (e.clipboardData || e.originalEvent.clipboardData).items;
    for (const item of items) {
      if (item.type.indexOf('image') !== -1) {
        const file = item.getAsFile();
        loadFile(file);
        showToast('Image pasted from clipboard!');
        break;
      }
    }
  }

  // --- Tooltip & Toast Notifications ---
  function showTooltip(x, y, text) {
    elements.gestureTooltip.style.left = `${x}px`;
    elements.gestureTooltip.style.top = `${y}px`;
    elements.gestureTooltip.textContent = text;
    elements.gestureTooltip.style.display = 'block';
  }

  function hideTooltip() {
    elements.gestureTooltip.style.display = 'none';
  }

  function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="16" x2="12" y2="12"></line>
        <line x1="12" y1="8" x2="12.01" y2="8"></line>
      </svg>
      <span>${message}</span>
    `;
    elements.toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3200);
  }

  // --- Composite Export ---
  function exportCompositeImage() {
    if (!state.image) {
      showToast('No image loaded to export');
      return;
    }

    // Render full-resolution composite canvas matching background image natural size
    const expCanvas = document.createElement('canvas');
    expCanvas.width = state.imageWidth;
    expCanvas.height = state.imageHeight;
    const expCtx = expCanvas.getContext('2d');

    // 1. Draw image with filters
    const { imageFilters } = state;
    if (imageFilters.sobel && state.sobelCacheCanvas) {
      expCtx.drawImage(state.sobelCacheCanvas, 0, 0);
    } else {
      const filters = [];
      if (imageFilters.brightness !== 100) filters.push(`brightness(${imageFilters.brightness}%)`);
      if (imageFilters.contrast !== 100) filters.push(`contrast(${imageFilters.contrast}%)`);
      if (imageFilters.invert) filters.push('invert(100%)');
      if (imageFilters.grayscale) filters.push('grayscale(100%)');

      expCtx.filter = filters.length > 0 ? filters.join(' ') : 'none';
      expCtx.drawImage(state.image, 0, 0);
    }

    // 2. Draw Cylinder overlay (temporarily hide handles for export)
    const prevSelected = cylinder.isSelected;
    cylinder.isSelected = false;
    cylinder.render(expCtx, 1.0);
    cylinder.isSelected = prevSelected;

    // 3. Draw Watermark & Telemetry Banner in lower left
    expCtx.save();
    expCtx.fillStyle = 'rgba(15, 23, 42, 0.75)';
    expCtx.fillRect(10, state.imageHeight - 34, 460, 26);
    expCtx.font = '11px monospace';
    expCtx.fillStyle = '#00f0ff';
    const deg = Math.round(((cylinder.rotation * 180 / Math.PI) % 360 + 360) % 360);
    const tiltDeg = Math.round(cylinder.tilt * 180 / Math.PI);
    expCtx.fillText(
      `CYLINDER: ${Math.round(cylinder.length)}×${Math.round(cylinder.diameter)}px | θ=${deg}° | Tilt=${tiltDeg}° | AR=${cylinder.aspectRatio.toFixed(2)}`,
      18,
      state.imageHeight - 17
    );
    expCtx.restore();

    // Trigger download
    const link = document.createElement('a');
    link.download = `martian-cylinder-overlay-${Date.now()}.png`;
    link.href = expCanvas.toDataURL('image/png');
    link.click();

    showToast('Composite PNG exported successfully!');
  }

  // Boot on DOMContentLoaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  // Expose to window for external integration / testing
  window.cylinder = cylinder;
  window.appState = state;
  window.syncControlsFromCylinder = syncControlsFromCylinder;
  window.triggerRedraw = triggerRedraw;

})();
