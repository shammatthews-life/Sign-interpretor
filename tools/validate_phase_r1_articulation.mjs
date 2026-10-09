/**
 * Static source guardrails for the R1 articulation runtime.
 *
 * This validates that the required code paths and checks are present.
 * It does not replace running the articulation suite against the rendered Aether rig.
 */
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = path => readFile(resolve(root, path), 'utf8');

const [controller, player, authoring, viewer] = await Promise.all([
  read('tools/avatar_viewer/ArticulationTestController.js'),
  read('tools/avatar_viewer/SignAnimationPlayer.js'),
  read('tools/avatar_viewer/SignAuthoringController.js'),
  read('tools/avatar_viewer/index.html')
]);

assert(controller.includes("for (const axis of ['x', 'y', 'z'])"),
  'R1 must test X/Y/Z independently for each finger segment.');
assert(controller.includes('world_rotation_change_radians'),
  'Axis checks must verify the bone world orientation so a twist axis is not failed solely because child origins do not translate.');
assert(controller.includes("axis: 'z', degrees: 30"),
  'R1 must retain a positive Z-axis test.');
assert(controller.includes('joint_id: `${side}-${finger}-${segment}`'),
  'Axis tests must retain their parent anatomical joint identity.');
assert(controller.includes('testCurlFallbackPrecedence()'),
  'R1 must run the explicit-keyframe versus legacy-curl regression.');
assert(controller.includes('explicit_rotation_preserved: explicitPassed'),
  'Curl-precedence test must report whether authored rotation was preserved.');
assert(controller.includes('unkeyframed_legacy_curl_preserved: fallbackPassed'),
  'Curl-precedence test must ensure legacy curl still affects unkeyframed joints.');
assert(controller.includes('listNonFiniteRestComponents()'),
  'R1 must list non-finite captured rest-pose components.');
assert(controller.includes('preexisting_non_finite_rest_component_details: nonFiniteRestDetails'),
  'R1 test result must include exact component details.');
assert(player.includes('if (explicitlyKeyframed) return;'),
  'Legacy curl fallback must not overwrite explicitly keyframed finger joints.');
assert(player.includes('Object.prototype.hasOwnProperty.call(k1.rotations, b.name)'),
  'The guard must consider explicitly authored rotations at the next keyframe.');
assert(authoring.includes("['x','y','z']"),
  'Authoring controller must serialize all three rotation axes.');
assert(viewer.includes("names.map(name=>['x','y','z']"),
  'The authoring UI must expose X/Y/Z sliders for all controlled bones.');
assert(viewer.includes('data-author-axis'),
  'The authoring UI must bind each slider to its specific rotation axis.');
assert(viewer.includes('non-finite rest components'),
  'The R1 UI must show unresolved non-finite rest components.');

console.log('PASS: R1 source guardrails confirm wrist/finger XYZ coverage, curl precedence, and non-finite reporting.');
console.log('NOTE: This is a static source check. Run window.AetherRig.articulationTest.runAutomatedSuite() and visually inspect the rendered avatar to establish runtime results.');
