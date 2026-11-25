import assert from 'node:assert/strict';
import test from 'node:test';
import { correctNonFiniteHelperBoneRotations } from './NonFiniteHelperBoneCorrection.mjs';

function makeVector(x, y, z, w) {
  return {
    x, y, z, ...(w === undefined ? {} : { w }),
    toArray() { return w === undefined ? [this.x, this.y, this.z] : [this.x, this.y, this.z, this.w]; }
  };
}

function makeNode(name, {
  isBone = true,
  scaleX = 0,
  rotationX = Number.NaN,
  rotationY = Number.NaN,
  children = [],
  skeletonBones = []
} = {}) {
  const node = {
    name,
    isBone,
    position: makeVector(1, 2, 3),
    scale: makeVector(scaleX, 2, 3),
    rotation: {
      x: rotationX,
      y: rotationY,
      z: 0,
      order: 'XYZ',
      toArray() { return [this.x, this.y, this.z]; },
      set(x, y, z, order) {
        Object.assign(this, { x, y, z, order });
        this.onChangeCallback?.();
      }
    },
    quaternion: makeVector(Number.NaN, Number.NaN, Number.NaN, Number.NaN),
    matrix: { elements: Array(16).fill(Number.NaN) },
    matrixWorld: { elements: Array(16).fill(Number.NaN) },
    children,
    parent: null
  };
  node.rotation.onChangeCallback = () => {
    node.quaternion.x = 0;
    node.quaternion.y = 0;
    node.quaternion.z = 0;
    node.quaternion.w = 1;
    node.matrix.elements = Array(16).fill(0);
    node.matrixWorld.elements = Array(16).fill(0);
  };
  for (const child of children) child.parent = node;
  if (skeletonBones.length) {
    node.isSkinnedMesh = true;
    node.skeleton = { bones: skeletonBones };
  }
  return node;
}

function makeModel(nodes) {
  const model = {
    updates: 0,
    traverse(callback) {
      const visit = node => {
        callback(node);
        for (const child of node.children || []) visit(child);
      };
      for (const node of nodes) visit(node);
    },
    updateMatrixWorld() { this.updates += 1; }
  };
  return model;
}

test('corrects only the whitelisted eligible helper while preserving position and scale', () => {
  const point = makeNode('PRIVATE_Grenade_Point');
  const lower = makeNode('PRIVATE_Grenade_Point_Low');
  const model = makeModel([point, lower]);

  const result = correctNonFiniteHelperBoneRotations({ model, protectedBones: [] });

  assert.equal(result.status, 'PASS');
  assert.deepEqual(result.corrected.map(item => item.name), [
    'PRIVATE_Grenade_Point',
    'PRIVATE_Grenade_Point_Low'
  ]);
  assert.ok(result.corrected.every(item =>
    item.positionPreserved && item.scalePreserved && item.transformFinite
  ));
  assert.equal(result.skeletonReferencesPreserved, true);
  assert.equal(result.protectedHierarchyPreserved, true);
  assert.deepEqual(result.issues, []);
  assert.deepEqual(point.position.toArray(), [1, 2, 3]);
  assert.deepEqual(point.scale.toArray(), [0, 2, 3]);
  assert.deepEqual(point.rotation.toArray(), [0, 0, 0]);
  assert.deepEqual(point.quaternion.toArray(), [0, 0, 0, 1]);
  assert.ok(model.updates >= 3);
});

test('does not correct nodes that fail any safety condition and reports REVIEW REQUIRED', () => {
  const referenced = makeNode('PRIVATE_Grenade_Point');
  const skinnedMesh = makeNode('Body_Mesh', {
    isBone: false,
    skeletonBones: [referenced]
  });
  const child = makeNode('PRIVATE_Grenade_Point_Low', { children: [makeNode('child')] });
  const model = makeModel([referenced, skinnedMesh, child]);

  const result = correctNonFiniteHelperBoneRotations({ model, protectedBones: [] });

  assert.equal(result.status, 'REVIEW REQUIRED');
  assert.equal(result.corrected.length, 0);
  assert.equal(result.issues.length, 2);
  assert.match(result.issues[0].reason, /referenced by a loaded skinned-mesh skeleton/);
  assert.match(result.issues[1].reason, /Node has children/);
  assert.ok(Number.isNaN(referenced.rotation.x));
  assert.ok(Number.isNaN(child.rotation.x));

  const protectedBone = makeNode('Bip001_R_Hand', { rotationX: 0, rotationY: 0 });
  const ancestor = makeNode('PRIVATE_Grenade_Point', { children: [protectedBone] });
  const ancestorResult = correctNonFiniteHelperBoneRotations({
    model: makeModel([ancestor]),
    protectedBones: [protectedBone]
  });

  assert.equal(ancestorResult.status, 'REVIEW REQUIRED');
  assert.ok(ancestorResult.issues.some(issue => /ancestor/.test(issue.reason)));
  assert.ok(Number.isNaN(ancestor.rotation.x));
});

test('does not normalize a non-zero-scale candidate or modify unlisted nodes', () => {
  const wrongScale = makeNode('PRIVATE_Grenade_Point', { scaleX: 0.01 });
  const unlisted = makeNode('Unrelated_Bone');
  const result = correctNonFiniteHelperBoneRotations({
    model: makeModel([wrongScale, unlisted]),
    protectedBones: []
  });

  assert.equal(result.status, 'REVIEW REQUIRED');
  assert.match(result.issues[0].reason, /not effectively zero/);
  assert.ok(Number.isNaN(wrongScale.rotation.x));
  assert.ok(Number.isNaN(unlisted.rotation.x));
});

test('rejects non-bones and candidates without a non-finite rotation', () => {
  const notBone = makeNode('PRIVATE_Grenade_Point', { isBone: false });
  const finiteRotation = makeNode('PRIVATE_Grenade_Point_Low', {
    rotationX: 0,
    rotationY: 0
  });
  finiteRotation.quaternion.x = 0;
  finiteRotation.quaternion.y = 0;
  finiteRotation.quaternion.z = 0;
  finiteRotation.quaternion.w = 1;
  const result = correctNonFiniteHelperBoneRotations({
    model: makeModel([notBone, finiteRotation]),
    protectedBones: []
  });

  assert.equal(result.status, 'REVIEW REQUIRED');
  assert.match(result.issues[0].reason, /Node is not a bone/);
  assert.match(result.issues[1].reason, /already finite/);
  assert.deepEqual(notBone.rotation.toArray(), [Number.NaN, Number.NaN, 0]);
  assert.deepEqual(finiteRotation.rotation.toArray(), [0, 0, 0]);
});

test('reports missing expected candidate names', () => {
  const result = correctNonFiniteHelperBoneRotations({
    model: makeModel([]),
    protectedBones: []
  });

  assert.equal(result.status, 'REVIEW REQUIRED');
  assert.deepEqual(result.issues.map(issue => issue.name), [
    'PRIVATE_Grenade_Point',
    'PRIVATE_Grenade_Point_Low'
  ]);
});
