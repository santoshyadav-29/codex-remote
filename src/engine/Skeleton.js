const NS='http://www.w3.org/2000/svg';
export const element=(name,attrs={})=>{const e=document.createElementNS(NS,name);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,v);return e;};
export class Skeleton{
 constructor(parts,container){this.parts=parts;this.bones=new Map();this.pose={};
  for(const part of parts){const g=element('g',{'data-bone':part.name});const art=element('g',{class:'part-art'});art.innerHTML=part.art;g.append(art);this.bones.set(part.name,{...part,g,art});(this.bones.get(part.parent)?.g||container).append(g);}
  for(const bone of this.bones.values()){
   const debug=element('g',{class:'bone-debug'});
   for(const child of parts.filter(p=>p.parent===bone.name))debug.append(element('line',{x1:0,y1:0,x2:child.x,y2:child.y,'data-child':child.name}));
   debug.append(element('circle',{r:2.3}));bone.g.append(debug);
  }
 }
 apply(pose){this.pose=pose;for(const [name,b]of this.bones){const p=pose[name]||{};b.g.setAttribute('transform',`translate(${b.x+(p.x||0)} ${b.y+(p.y||0)}) rotate(${p.r||0}) scale(${(p.sx??1)*(b.scale||1)} ${(p.sy??1)*(b.scale||1)})`);}}
 exportConfig(character){return {version:1,character,bones:this.parts.map(({name,parent,x,y})=>({name,parent,x,y})),pose:this.pose};}
 loadConfig(data,character){if(data.version!==1||data.character!==character||!Array.isArray(data.bones)||!data.pose)throw Error('Choose a version 1 rig for the selected character.');
  if(data.bones.length!==this.parts.length)throw Error('Bone count does not match this rig.');
  for(const b of data.bones){const known=this.bones.get(b.name);if(!known||b.parent!==known.parent||![b.x,b.y].every(v=>Number.isFinite(v)&&Math.abs(v)<500))throw Error('Invalid bone structure or pivot.');}
  for(const [name,p]of Object.entries(data.pose)){if(!this.bones.has(name)||Object.entries(p).some(([k,v])=>!['x','y','r','sx','sy'].includes(k)||!Number.isFinite(v)||Math.abs(v)>1000))throw Error('Invalid pose.');}
  for(const b of data.bones){Object.assign(this.bones.get(b.name),{x:b.x,y:b.y});Object.assign(this.parts.find(p=>p.name===b.name),{x:b.x,y:b.y});}for(const bone of this.bones.values())for(const line of bone.g.querySelectorAll(':scope > .bone-debug > line')){const child=this.bones.get(line.getAttribute('data-child'));line.setAttribute('x2',child.x);line.setAttribute('y2',child.y);}this.apply(data.pose);
 }
}
