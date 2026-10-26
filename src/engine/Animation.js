export const ease = t => t*t*(3-2*t);
export function track(keys,t){
 if(t<=keys[0][0])return keys[0][1];
 for(let i=1;i<keys.length;i++)if(t<=keys[i][0]){const [a,x]=keys[i-1],[b,y]=keys[i];return x+(y-x)*ease((t-a)/(b-a));}
 return keys.at(-1)[1];
}
export function solveIK(x,y,a,b,bend=1){
 const d=Math.max(.01,Math.min(Math.hypot(x,y),a+b-.001));
 const knee=Math.acos(Math.max(-1,Math.min(1,(d*d-a*a-b*b)/(2*a*b))))*bend;
 const hip=Math.atan2(-x,y)-Math.atan2(b*Math.sin(knee),a+b*Math.cos(knee));
 return [hip*180/Math.PI,knee*180/Math.PI];
}
export const durations={idle:4,walk:1.15,run:.68,wave:3.2,jump:1.9,sit:2,tilt:3};
const cyc=(t,offset=0)=>(t+offset)%1;
export function poseAt(character,clip,time){
 const duration=durations[clip]||4, t=(time/duration)%1, s=Math.sin(t*Math.PI*2), p={};
 const set=(name,r=0,x=0,y=0,sx=1,sy=1)=>p[name]={r,x,y,sx,sy};
 set('root',0,0,-1.3*(1-Math.cos(t*Math.PI*2))); set('head',1.2*s);
 if(character==='boy'){
  set('torso',.5*s,0,0,1,1+.008*s);
  set('shoulderL',8+.7*s);set('shoulderR',-8-.7*s);set('elbowL',-3);set('elbowR',3);set('fringe',1.8*Math.sin(t*(2*Math.PI)-.5));
  if(clip==='walk'||clip==='run'){
   const run=clip==='run', stride=run?43:25, lift=run?39:18;
   const bounce=track([[0,0],[.15,run?-8:-2],[.3,run?-14:-4],[.5,0],[.65,run?-8:-2],[.8,run?-14:-4],[1,0]],t);
   set('root',0,0,bounce);set('torso',run?-9:-2);set('head',run?5:1);
   ['L','R'].forEach((side,i)=>{
    const q=cyc(t,i*.5);
    // Stance has linear ground travel; swing uses authored lift and clearance.
    const fx=q<.6?stride*(1-2*q/.6):track([[.6,-stride],[.8,0],[1,stride]],q);
    const fy=q<.6?0:track([[.6,0],[.72,-lift],[.84,-lift*.85],[1,0]],q);
    const [hip,knee]=solveIK(fx,119+fy-bounce,60,64,-1);
    set('hip'+side,hip);set('knee'+side,knee);set('ankle'+side,-hip-knee+track([[0,-3],[.45,0],[.6,-12],[.8,8],[1,-3]],q));
    set('shoulder'+side,track([[0,-(run?35:19)],[.5,run?35:19],[1,-(run?35:19)]],q));
    set('elbow'+side,run?-65:-12);
   });
  }
  if(clip==='wave'){
   const raise=track([[0,0],[.2,1],[.77,1],[1,0]],t);
   set('shoulderR',-100*raise);set('elbowR',-35*raise+track([[0,0],[.25,0],[.33,-22],[.41,16],[.49,-22],[.57,16],[.65,-22],[.76,0],[1,0]],t));set('wristR',12*raise);set('head',-4*raise);
  }
  if(clip==='jump'){
   const y=track([[0,0],[.18,18],[.25,15],[.42,-65],[.53,-78],[.67,-50],[.77,14],[.85,19],[1,0]],t);
   const crouch=track([[0,0],[.18,1],[.3,0],[.6,.25],[.75,0],[.83,1],[1,0]],t);
   set('root',0,0,y);set('torso',-8*crouch,0,0,1+.025*crouch,1-.035*crouch);
   for(const side of ['L','R']){set('hip'+side,24*crouch);set('knee'+side,-48*crouch);set('ankle'+side,24*crouch);set('shoulder'+side,track([[0,0],[.18,25],[.4,-125],[.6,-110],[.8,20],[1,0]],t));set('elbow'+side,-15*crouch);}
  }
 }else{
  set('body',.8*s,0,0,1,1+.015*s);set('tail',track([[0,-15],[.25,18],[.5,-15],[.75,18],[1,-15]],t));set('tailTip',10*Math.sin(t*(4*Math.PI)-.6));set('earL',3*s);set('earR',-3*s);
  if(clip==='walk'){
   ['rearFar','frontFar','rearNear','frontNear'].forEach((leg,i)=>{const q=cyc(t,[0,.5,.5,0][i]);const x=track([[0,17],[.6,-17],[.8,0],[1,17]],q),y=track([[0,0],[.6,0],[.8,-15],[1,0]],q);const [a,b]=solveIK(x,52+y,28,28,-1);set(leg,a);set(leg+'Knee',b);});set('root',0,0,track([[0,0],[.25,-3],[.5,0],[.75,-3],[1,0]],t));
  }
  if(clip==='sit'){
   const a=track([[0,0],[.35,1],[.85,1],[1,0]],t);set('root',0,0,13*a);set('body',-9*a);set('rearNear',-65*a);set('rearFar',-65*a);set('rearNearKnee',110*a);set('rearFarKnee',110*a);set('head',9*a,0,-2*a);
  }
  if(clip==='tilt'){set('head',track([[0,0],[.25,-15],[.5,-15],[.75,12],[1,0]],t));set('earL',track([[0,0],[.3,14],[.55,8],[1,0]],t));}
 }
 return p;
}
export function blend(a,b,t){const p={};for(const name of new Set([...Object.keys(a),...Object.keys(b)])){p[name]={};for(const k of ['r','x','y','sx','sy']){const fallback=k[0]==='s'?1:0;const x=a[name]?.[k]??fallback,y=b[name]?.[k]??fallback;p[name][k]=x+(y-x)*ease(Math.min(1,t));}}return p;}
