/** Phase D: data-driven motion authoring, built on the existing player/schema. */
const RAD = 180 / Math.PI;
const FINGERS = ['thumb', 'index', 'middle', 'ring', 'pinky'];
const ARM_BONES = side => [`Bip001_${side}_Clavicle`, `Bip001_${side}_UpperArm`, `Bip001_${side}_Forearm`, `Bip001_${side}_Hand`];

export class SignAuthoringController {
  constructor({ bonesMap, handRig, player, library, onState }) {
    this.bonesMap = bonesMap; this.handRig = handRig; this.player = player; this.library = library; this.onState = onState;
    this.rest = new Map([...bonesMap].map(([name, b]) => [name, { r: b.rotation.clone(), p: b.position.clone() }]));
    this.frames = []; this.selected = -1; this.duration = 1500; this.signId = 'authoring_test'; this.snapshots = new Map();
  }
  begin(id = this.signId) { this.signId = String(id).trim().toLowerCase(); this.frames = []; this.selected = -1; this.reset(); this.emit(); }
  reset() { this.player.stop(); this.rest.forEach((v, n) => { const b = this.bonesMap.get(n); if (b) { b.rotation.copy(v.r); b.position.copy(v.p); } }); }
  controlledNames() { return [...new Set(['L', 'R'].flatMap(side => [...ARM_BONES(side), ...FINGERS.flatMap(f => (this.handRig[side === 'L' ? 'left' : 'right'][f] || []).map(b => b.name))]))].filter(n => this.bonesMap.has(n)); }
  pose() { const rotations = {}; const positions = {};
    this.controlledNames().forEach(n => { const b = this.bonesMap.get(n), r = this.rest.get(n); const d = { x: (b.rotation.x-r.r.x)*RAD, y:(b.rotation.y-r.r.y)*RAD, z:(b.rotation.z-r.r.z)*RAD };
      if (Math.abs(d.x)+Math.abs(d.y)+Math.abs(d.z) > .001) rotations[n] = d;
      const p = { x:b.position.x-r.p.x, y:b.position.y-r.p.y, z:b.position.z-r.p.z }; if (Math.abs(p.x)+Math.abs(p.y)+Math.abs(p.z) > .00001) positions[n]=p;
    }); return { rotations, ...(Object.keys(positions).length ? { positions } : {}) };
  }
  applyPose(pose) { this.reset(); Object.entries(pose.rotations || {}).forEach(([n, d]) => { const b=this.bonesMap.get(n), r=this.rest.get(n); if(b&&r) b.rotation.set(r.r.x+d.x/RAD,r.r.y+d.y/RAD,r.r.z+d.z/RAD); }); Object.entries(pose.positions || {}).forEach(([n,d])=>{const b=this.bonesMap.get(n),r=this.rest.get(n);if(b&&r)b.position.set(r.p.x+d.x,r.p.y+d.y,r.p.z+d.z);}); }
  addFrame(time, label = 'Pose', easing = 'easeInOutQuad') { const frame={ time_ms:Number(time), label, easing, ...this.pose() }; const same=this.frames.findIndex(f=>f.time_ms===frame.time_ms); if(same>=0)this.frames[same]=frame; else this.frames.push(frame); this.frames.sort((a,b)=>a.time_ms-b.time_ms); this.selected=this.frames.indexOf(frame); this.emit(); }
  select(i) { this.selected=i; if(this.frames[i]) this.applyPose(this.frames[i]); this.emit(); }
  moveSelected(time) { if(this.selected<0)return; this.frames[this.selected].time_ms=Number(time); this.frames.sort((a,b)=>a.time_ms-b.time_ms); this.selected=this.frames.indexOf(this.frames.find(f=>f.time_ms===Number(time))); this.emit(); }
  deleteSelected() { if(this.selected>=0)this.frames.splice(this.selected,1); this.selected=-1; this.emit(); }
  preset(kind, side='right') { const curl=kind==='fist'?80:kind==='point'?80:0; const target=side==='both'?['left','right']:[side]; target.forEach(s=>FINGERS.forEach(f=>(this.handRig[s][f]||[]).forEach((b,i)=>{const r=this.rest.get(b.name); const value=(kind==='point'&&f==='index')?0:curl; b.rotation.z=r.r.z+(value/RAD)*(i===0?.75:1); }))); this.emit(); }
  saveSnapshot(name) { this.snapshots.set(name, this.pose()); this.emit(); }
  applySnapshot(name) { const p=this.snapshots.get(name); if(p)this.applyPose(p); this.emit(); }
  motion() { const involved=[...new Set(this.frames.flatMap(f=>[...Object.keys(f.rotations||{}),...Object.keys(f.positions||{})]))]; return { status:'playable', duration_ms:Number(this.duration), dominant_hand:'right', return_to_neutral:true, transition_hints:{safe_transition:'neutral',direct_blend_supported:false}, involved_bones:involved, keyframes:this.frames.map(f=>structuredClone(f)) }; }
  definition() { return { schema_version:'2.0.0', sign_id:this.signId, metadata:{display_name:this.signId.replace(/(^|_)(\w)/g,(_,a,b)=>`${a}${b.toUpperCase()}`), gloss:this.signId.toUpperCase(), language:'ISL', lexical_type:'Technical motion authoring asset', validation_status:'MOTION_TECHNICALLY_COMPLETE', source:{organization:'Local Phase D authoring tool'}, notes:'Technical completion only; linguistic correctness is not asserted.'}, motion:this.motion() }; }
  validate() { const errors=[], warnings=[], m=this.motion(), id=this.signId; if(!/^[a-z0-9_]+$/.test(id))errors.push('Sign ID must use lowercase letters, digits, or underscores.'); if(!(m.duration_ms>0))errors.push('Duration must be greater than zero.'); if(m.keyframes.length<2)errors.push('At least two keyframes are required.'); const times=new Set(); m.keyframes.forEach((f,i)=>{if(!Number.isFinite(f.time_ms)||f.time_ms<0||f.time_ms>m.duration_ms)errors.push(`Frame ${i+1} time is outside duration.`);if(times.has(f.time_ms))errors.push(`Duplicate timestamp: ${f.time_ms} ms.`);times.add(f.time_ms);Object.entries({...f.rotations,...f.positions}).forEach(([n,r])=>{if(!this.bonesMap.has(n))errors.push(`Missing bone: ${n}`);['x','y','z'].forEach(a=>{if(!Number.isFinite(r[a]))errors.push(`Invalid pose value ${n}.${a}`);if(f.rotations?.[n]&&Math.abs(r[a])>180)warnings.push(`Large rotation at ${n}.`);});});}); if(m.keyframes[0]?.time_ms!==0)warnings.push('No neutral pose at 0 ms.'); if(m.keyframes.at(-1)?.time_ms!==m.duration_ms)warnings.push('No final reset state at duration.'); return {errors:[...new Set(errors)],warnings:[...new Set(warnings)]}; }
  preview() { const v=this.validate(); if(v.errors.length) return v; this.player.loadSign({...this.motion(),sign_id:this.signId,gloss:this.signId.toUpperCase()}); this.player.replay(); return v; }
  async load(id) { const def=await this.library.loadSign(id); if(!def.motion?.keyframes)throw new Error('This sign has no editable keyframes.'); this.signId=def.sign_id; this.duration=def.motion.duration_ms; this.frames=structuredClone(def.motion.keyframes); this.selected=-1; this.player.loadSign({...def.motion,sign_id:def.sign_id,gloss:def.metadata.gloss}); this.emit(); }
  emit(){this.onState?.(this);}
}
