import assert from 'node:assert/strict';
import { test } from 'node:test';
import { setAvatarCameraView } from './AvatarCameraView.mjs';

function createCamera() {
  const camera = { position: { value: null, set(...value) { this.value = value; } } };
  const controls = {
    target: { value: null, set(...value) { this.value = value; } },
    updates: 0,
    update() { this.updates += 1; }
  };
  return { camera, controls };
}

test('half-body view frames the upper body and hands', () => {
  const { camera, controls } = createCamera();
  assert.equal(setAvatarCameraView(camera, controls, 'half'), 'half');
  assert.deepEqual(camera.position.value, [-0.3, 1.43, 0.92]);
  assert.deepEqual(controls.target.value, [-0.15, 1.3, 0.05]);
  assert.equal(controls.updates, 1);
});

test('full-body view frames the complete avatar', () => {
  const { camera, controls } = createCamera();
  assert.equal(setAvatarCameraView(camera, controls, 'full'), 'full');
  assert.deepEqual(camera.position.value, [0, 1.2, 2.5]);
  assert.deepEqual(controls.target.value, [0, 0.9, 0]);
  assert.equal(controls.updates, 1);
});

test('rejects unsupported views rather than leaving ambiguous framing', () => {
  const { camera, controls } = createCamera();
  assert.throws(() => setAvatarCameraView(camera, controls, 'zoomed'), RangeError);
});
test('half-body view dynamically adapts distance in portrait viewports to prevent hand clipping', () => {
  const { camera, controls } = createCamera();
  camera.aspect = 0.64; // Portrait aspect ratio (320px x 500px)
  assert.equal(setAvatarCameraView(camera, controls, 'half'), 'half');
  assert.ok(camera.position.value[2] > 0.92); // Camera pulls back to preserve handspan
  assert.equal(controls.updates, 1);
});
