import { readFile } from 'node:fs/promises';
import { SignAuthoringController } from './avatar_viewer/SignAuthoringController.js';

class Euler { constructor(x=0,y=0,z=0){this.x=x;this.y=y;this.z=z;} clone(){return new Euler(this.x,this.y,this.z);} copy(v){this.x=v.x;this.y=v.y;this.z=v.z;return this;} set(x,y,z){this.x=x;this.y=y;this.z=z;return this;} }
class Vec { constructor(x=0,y=0,z=0){this.x=x;this.y=y;this.z=z;} clone(){return new Vec(this.x,this.y,this.z);} copy(v){this.x=v.x;this.y=v.y;this.z=v.z;return this;} set(x,y,z){this.x=x;this.y=y;this.z=z;return this;} }
const bone = name => ({name, rotation:new Euler(), position:new Vec()});
const bones = new Map(); const handRig={left:{},right:{}};
for (const side of ['L','R']) { for(const part of ['Clavicle','UpperArm','Forearm','Hand']) bones.set(`Bip001_${side}_${part}`,bone(`Bip001_${side}_${part}`)); const h=side==='L'?'left':'right'; for(let i=0;i<5;i++){const b=bone(`Bip001_${side}_Finger${i}`);bones.set(b.name,b);handRig[h][['thumb','index','middle','ring','pinky'][i]]=[b];} }
const player={stop(){},loadSign(s){this.sign=s;},replay(){this.replays=(this.replays||0)+1;}};
const library={async loadSign(){return JSON.parse(await readFile(new URL('../signs/hello.json',import.meta.url)));}};
const author=new SignAuthoringController({bonesMap:bones,handRig,player,library});
author.begin('authoring_test'); author.addFrame(0,'Neutral'); bones.get('Bip001_R_Finger1').rotation.set(.1,.2,.4); bones.get('Bip001_R_Hand').rotation.y=.2; author.addFrame(500,'Move');
const fingerRotation=author.frames.find(frame=>frame.time_ms===500)?.rotations?.Bip001_R_Finger1;
if(!fingerRotation||Math.abs(fingerRotation.x-5.7296)>.001||Math.abs(fingerRotation.y-11.4592)>.001||Math.abs(fingerRotation.z-22.9183)>.001)throw new Error('Finger base XYZ articulation did not serialize as schema-2.0.0 degree deltas.');
author.reset(); author.addFrame(1500,'Neutral');
const report=author.validate(); if(report.errors.length) throw new Error(report.errors.join('; '));
for(let i=0;i<5;i++){author.preview();author.reset();for(const b of bones.values())if(b.rotation.x||b.rotation.y||b.rotation.z)throw new Error(`Reset drift after preview ${i+1}: ${b.name}`);}
const original=await readFile(new URL('../signs/hello.json',import.meta.url),'utf8'); await author.load('hello'); const after=await readFile(new URL('../signs/hello.json',import.meta.url),'utf8'); if(original!==after)throw new Error('HELLO source was modified by authoring load.');
console.log('PASS: sparse schema-2.0.0 keyframes validate and use verified bones');
console.log('PASS: five preview/reset cycles restore the captured neutral pose without drift');
console.log('PASS: HELLO loads for authoring review without changing its baseline file');
