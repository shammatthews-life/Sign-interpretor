const VIEWS = Object.freeze({
  half: Object.freeze({
    position: [-0.3, 1.43, 0.92],
    target: [-0.15, 1.3, 0.05]
  }),
  full: Object.freeze({
    position: [0, 1.2, 2.5],
    target: [0, 0.9, 0]
  })
});

export function setAvatarCameraView(camera, controls, mode) {
  const view = VIEWS[mode];
  if (!view) throw new RangeError(`Unsupported avatar camera view: ${mode}`);
  if (!camera?.position?.set || !controls?.target?.set || typeof controls.update !== 'function') {
    throw new TypeError('Avatar camera and orbit controls are required.');
  }

  let posX = view.position[0];
  let posY = view.position[1];
  let posZ = view.position[2];

  // Top 0.001% Accessible Framing: In portrait/narrow viewports (e.g. aspect < 0.85),
  // dynamically scale camera distance so two-handed signs and wide gestures
  // are never clipped at the viewport edges.
  if (mode === 'half' && typeof camera.aspect === 'number' && camera.aspect < 0.85 && camera.aspect > 0) {
    const scale = Math.min(1.4, 0.85 / camera.aspect);
    posX = Number((view.target[0] + (view.position[0] - view.target[0]) * scale).toFixed(4));
    posY = Number((view.target[1] + (view.position[1] - view.target[1]) * scale).toFixed(4));
    posZ = Number((view.target[2] + (view.position[2] - view.target[2]) * scale).toFixed(4));
  }

  camera.position.set(posX, posY, posZ);
  controls.target.set(...view.target);
  controls.update();
  return mode;
}
