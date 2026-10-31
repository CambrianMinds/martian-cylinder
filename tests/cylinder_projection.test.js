// Regression tests for the interactive projection engine (audit finding 3).
// Expected values are derived independently from pinhole-camera geometry, not
// from previously published numbers.  Run: node tests/cylinder_projection.test.js
const assert = require('assert');
const MartianCylinder = require('../cylinder-tool/cylinder.js');

const IFOV = 7.4e-5;
let failures = 0;
function check(name, fn) {
  try { fn(); console.log('  ok   ' + name); }
  catch (e) { failures++; console.log('  FAIL ' + name + '\n       ' + e.message); }
}
const near = (a, b, tol, msg) => assert.ok(Math.abs(a - b) <= tol, `${msg || ''} got ${a}, expected ${b} +/- ${tol}`);

// Independent pinhole reference: cap centres on the optical axis separated by
// dZ = L_mm*|cos(tilt)| along depth; radius ratio = Z_front / Z_rear.
function referenceRatio(Lmm, Zmm, tiltDeg) {
  const dZ = Lmm * Math.abs(Math.cos(tiltDeg * Math.PI / 180));
  return (Zmm - dZ / 2) / (Zmm + dZ / 2);
}

console.log('cylinder projection');

check('35 mm cylinder at 3957 mm, tilt 156 deg: rear/front ~= 0.992 (audit acceptance case)', () => {
  const Zmm = 3957, Lmm = 35;
  const s = Zmm * IFOV;                    // mm/px normal scale
  const c = new MartianCylinder({ baseLength: Lmm / s, baseDiameter: 11 / s, tilt: 156 * Math.PI / 180 });
  c.setCameraDistanceMm(Zmm);
  const g = c.getGeometry();
  near(g.perspRatio, referenceRatio(Lmm, Zmm, 156), 1e-4, 'perspRatio');
  near(g.perspRatio, 0.992, 1e-3, 'perspRatio vs audit 0.992');
});

check('physical mode agrees with reference over ranges and tilts', () => {
  for (const Zmm of [1000, 3630, 3957, 4300, 8000]) {
    for (const tilt of [100, 130, 156, 170]) {
      const Lmm = 35, s = Zmm * IFOV;
      const c = new MartianCylinder({ baseLength: Lmm / s, baseDiameter: 11 / s, tilt: tilt * Math.PI / 180 });
      c.setCameraDistanceMm(Zmm);
      near(c.getGeometry().perspRatio, referenceRatio(Lmm, Zmm, tilt), 2e-4, `Z=${Zmm} tilt=${tilt}`);
    }
  }
});

check('contraction is independent of the overlay pixel length at fixed physical size', () => {
  const Zmm = 3957, s = Zmm * IFOV;
  const a = new MartianCylinder({ baseLength: 110, baseDiameter: 34, tilt: 156 * Math.PI / 180 });
  a.setCameraDistanceMm(Zmm);
  near(a.getGeometry().perspRatio, referenceRatio(110 * s, Zmm, 156), 2e-4);
  a.scale = 2.0; // 2x pixels => 2x physical length; contraction must follow physics, not stay fixed
  near(a.getGeometry().perspRatio, referenceRatio(220 * s, Zmm, 156), 2e-4);
});

check('old preset (camRatio 3.96 treated as ratio) is NOT ~0.99: documents the audited defect', () => {
  const c = new MartianCylinder({ baseLength: 110, baseDiameter: 34, tilt: 156 * Math.PI / 180, camRatio: 3.96 });
  assert.ok(c.getGeometry().perspRatio < 0.85, 'legacy mode retains strong contraction');
});

console.log(failures ? `${failures} FAILED` : 'all passed');
process.exit(failures ? 1 : 0);

