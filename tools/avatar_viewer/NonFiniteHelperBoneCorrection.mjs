export const NON_FINITE_HELPER_BONE_NAMES = Object.freeze([
  'PRIVATE_Grenade_Point',
  'PRIVATE_Grenade_Point_Low'
]);

const DEFAULT_ZERO_SCALE_TOLERANCE = 1e-8;

function rotationIsNonFinite(node) {
  return ![node.rotation.x, node.rotation.y, node.rotation.z].every(Number.isFinite)
    || ![node.quaternion.x, node.quaternion.y, node.quaternion.z, node.quaternion.w].every(Number.isFinite);
}

function matrixIsFinite(matrix) {
  return !matrix || matrix.elements.every(Number.isFinite);
}

function transformIsFinite(node) {
  return !rotationIsNonFinite(node)
    && node.position.toArray().every(Number.isFinite)
    && node.scale.toArray().every(Number.isFinite)
    && matrixIsFinite(node.matrix)
    && matrixIsFinite(node.matrixWorld);
}

function isAncestorOfAny(node, protectedBones) {
  return protectedBones.some(bone => {
    for (let current = bone; current; current = current.parent) {
      if (current === node) return true;
    }
    return false;
  });
}

function collectNodes(model) {
  const nodes = [];
  model.traverse(node => nodes.push(node));
  return nodes;
}

function collectSkeletonBones(nodes) {
  const bones = new Set();
  for (const node of nodes) {
    if (node.isSkinnedMesh && node.skeleton?.bones) {
      for (const bone of node.skeleton.bones) bones.add(bone);
    }
  }
  return bones;
}

function readTransformVector(vector) {
  return vector.toArray();
}

export function correctNonFiniteHelperBoneRotations({
  model,
  protectedBones,
  zeroScaleTolerance = DEFAULT_ZERO_SCALE_TOLERANCE
}) {
  if (!model || typeof model.traverse !== 'function' || typeof model.updateMatrixWorld !== 'function') {
    throw new TypeError('A loaded 3D model with traverse and updateMatrixWorld is required.');
  }
  if (!Array.isArray(protectedBones)) {
    throw new TypeError('protectedBones must list the articulated wrist, hand, and finger bones.');
  }

  model.updateMatrixWorld(true);
  const nodes = collectNodes(model);
  const skeletonBones = collectSkeletonBones(nodes);
  const skeletonReferences = nodes
    .filter(node => node.isSkinnedMesh && node.skeleton?.bones)
    .map(node => ({ node, bones: [...node.skeleton.bones] }));
  const protectedParents = protectedBones.map(bone => ({ bone, parent: bone.parent }));
  const corrected = [];
  const issues = [];

  for (const name of NON_FINITE_HELPER_BONE_NAMES) {
    const node = nodes.find(candidate => candidate.name === name);
    if (!node) {
      issues.push({ name, reason: 'Expected imported helper bone is missing.' });
      continue;
    }

    const reasons = [];
    if (!node.isBone) reasons.push('Node is not a bone.');
    if (!Number.isFinite(node.scale?.x) || Math.abs(node.scale.x) > zeroScaleTolerance) {
      reasons.push(`X scale is not effectively zero (expected |x| <= ${zeroScaleTolerance}).`);
    }
    if (!rotationIsNonFinite(node)) reasons.push('Imported rotation and quaternion are already finite.');
    if (!Array.isArray(node.children) || node.children.length !== 0) reasons.push('Node has children.');
    if (skeletonBones.has(node)) reasons.push('Node is referenced by a loaded skinned-mesh skeleton.');
    if (isAncestorOfAny(node, protectedBones)) reasons.push('Node is an ancestor of an articulated wrist, hand, or finger bone.');

    if (reasons.length) {
      issues.push({ name, reason: reasons.join(' ') });
      continue;
    }

    const originalPosition = readTransformVector(node.position);
    const originalScale = readTransformVector(node.scale);
    node.rotation.set(0, 0, 0, node.rotation.order);
    model.updateMatrixWorld(true);

    const positionPreserved = originalPosition.every((value, index) => value === node.position.toArray()[index]);
    const scalePreserved = originalScale.every((value, index) => value === node.scale.toArray()[index]);
    if (!positionPreserved || !scalePreserved || !transformIsFinite(node)) {
      issues.push({
        name,
        reason: `Correction verification failed (position preserved: ${positionPreserved}; scale preserved: ${scalePreserved}; transform finite: ${transformIsFinite(node)}).`
      });
      continue;
    }

    corrected.push({
      name,
      reason: 'Reset non-finite imported rotation to identity on a zero-X-scale, childless helper bone unused by skeletons and articulated chains.',
      positionPreserved,
      scalePreserved,
      transformFinite: true
    });
  }

  const skeletonReferencesPreserved = skeletonReferences.every(({ node, bones }) =>
    node.skeleton.bones.length === bones.length
      && bones.every((bone, index) => node.skeleton.bones[index] === bone)
  );
  const protectedHierarchyPreserved = protectedParents.every(({ bone, parent }) => bone.parent === parent);
  if (!skeletonReferencesPreserved) {
    issues.push({ name: 'loaded skeletons', reason: 'Correction changed a loaded skeleton bone array.' });
  }
  if (!protectedHierarchyPreserved) {
    issues.push({ name: 'articulated chains', reason: 'Correction changed an articulated bone parent link.' });
  }

  return {
    status: issues.length ? 'REVIEW REQUIRED' : 'PASS',
    corrected,
    issues,
    skeletonReferencesPreserved,
    protectedHierarchyPreserved
  };
}
