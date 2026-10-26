"""Original layered artwork -> 3x PNG masks -> genuine Potrace -> colored SVG parts."""
import os,json,subprocess,io,xml.etree.ElementTree as ET
from pathlib import Path
import cairosvg
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'assets'; OUT.mkdir(exist_ok=True)
POTRACE=os.environ.get('POTRACE','potrace')
ink='#252b3d'; skin='#edbfa5'; navy='#344557'; light='#52667b'; cream='#f1eee4'
def shape(d,c,stroke=ink,w=1.5): return dict(d=d,fill=c,stroke=stroke,width=w)
def part(name,parent,x,y,shapes): return dict(name=name,parent=parent,x=x,y=y,shapes=shapes)
b=[]
b.append(part('root',None,0,0,[]))
# Rear limbs are painted before the coat. Each segment includes hidden overlap.
for side,x in [('R',15),('L',-15)]:
 b.append(part('hip'+side,'root',x,0,[shape('M-12 -9 Q0 -15 12 -7 L10 62 Q2 69 -9 62 L-13 17Z','#303747'),shape('M4 8 L6 56 L2 61 L0 12Z','#424b5d',None)]))
 b.append(part('knee'+side,'hip'+side,0,60,[shape('M-9 -8 Q0 -13 10 -6 L7 65 Q0 70 -8 65 L-10 12Z','#303747'),shape('M3 5 L5 58 L1 60 L0 12Z','#454f61',None)]))
 b.append(part('ankle'+side,'knee'+side,0,64,[shape('M-8 -5 L7 -5 Q10 3 18 7 Q25 10 22 16 Q8 20 -11 16 L-12 8Z','#252a36'),shape('M-11 14 Q6 18 23 13 L23 17 Q7 22 -12 18Z','#75818a'),shape('M3 3 L11 7 M1 6 L9 10','none','#a3a6ab',1)]))
b.append(part('torso','root',0,-78,[shape('M-24 -4 Q-37 1 -33 24 L-26 79 Q-7 87 0 78 Q10 87 28 78 L33 20 Q35 3 22 -4Z',navy),shape('M-14 -7 L14 -7 L12 43 L0 60 L-13 42Z',cream),shape('M-10 -7 L0 3 L-8 14 L-16 0 M10 -7 L0 3 L8 14 L16 0',cream),shape('M-3 9 L3 9 L5 36 L0 44 L-5 36Z','#8a5860'),shape('M-22 0 L-11 -6 L-14 15 L-7 21 L-21 51 L-23 12Z',light),shape('M22 0 L11 -6 L14 15 L7 21 L21 51 L23 12Z',light),shape('M1 43 L1 78 M-21 59 L-9 58 M10 58 L23 59','none','#202c3b',1.2),shape('M5 57 L7 57 M5 70 L7 70','none','#c6aa7e',2)]))
for side,x,sgn in [('L',-29,-1),('R',29,1)]:
 b.append(part('shoulder'+side,'torso',x,5,[shape('M-8 -6 Q0 -13 9 -5 Q13 10 9 38 Q0 44 -9 37 L-11 10Z',navy),shape('M5 4 Q8 19 4 34','none',light,2)]))
 b.append(part('elbow'+side,'shoulder'+side,0,36,[shape('M-9 -7 Q0 -12 9 -5 L7 35 Q0 41 -8 35 L-10 8Z',navy),shape('M-8 30 L7 30 L7 36 L-8 36Z',light),shape('M-6 36 L6 36 L6 42 L-6 42Z',cream)]))
 b.append(part('wrist'+side,'elbow'+side,0,40,[shape('M-5 -3 Q0 -6 5 -2 L6 7 Q11 14 7 17 L4 12 L4 23 Q2 27 0 23 Q-3 27 -5 22 L-7 9Z',skin),shape('M-2 12 L-2 21 M1 13 L1 22','none','#bc8b7b',.7)]))
b.append(part('head','torso',0,-17,[shape('M-8 1 L-8 20 Q0 26 8 20 L8 0Z',skin),shape('M-24 -27 Q-32 -8 -22 6 L-14 14 Q0 24 14 14 L24 2 Q32 -15 21 -33Z',skin),shape('M-24 -9 Q-33 -14 -29 -3 L-23 3 M24 -9 Q33 -14 29 -3 L23 3',skin),shape('M-20 -11 Q-12 -16 -5 -10 M5 -10 Q12 -16 20 -11','none',ink,1.8),shape('M-20 -7 Q-12 -11 -5 -6 Q-11 1 -18 -3Z','#fff9ee'),shape('M5 -6 Q12 -11 20 -7 L18 -3 Q11 1 5 -6Z','#fff9ee'),shape('M-14 -8 Q-9 -9 -10 -2 Q-16 0 -14 -8 M10 -8 Q15 -9 14 -2 Q8 0 10 -8','#866344'),shape('M-12 -7 L-12 -3 M12 -7 L12 -3','none',ink,2),shape('M0 -3 L-2 5 L1 6 M-5 12 Q0 14 5 11','none','#a66f64',1),shape('M-27 -10 Q-35 -30 -21 -43 Q-8 -53 8 -46 Q25 -48 30 -29 L26 -7 L20 -23 L15 -14 L12 -28 L4 -14 L1 -25 L-9 -13 L-10 -27 L-21 -14 L-20 -25Z','#292c37'),shape('M-24 -32 Q-8 -47 12 -39 M-17 -27 Q-7 -38 3 -37 M16 -36 Q24 -27 23 -19','none','#484956',1.5)]))
b.append(part('fringe','head',0,-26,[shape('M-5 -13 Q8 -21 18 -9 L12 3 L10 -7 L2 6 L2 -6 L-7 4Z','#292c37')]))
d=[part('root',None,0,0,[])]
for side,x,y in [('rearFar',29,-35),('frontFar',-30,-35),('rearNear',43,-30),('frontNear',-43,-30)]:
 d.append(part(side,'root',x,y,[shape('M-10 -5 Q3 -12 12 0 L8 30 Q0 38 -9 29Z','#b9794e')]))
 d.append(part(side+'Knee',side,0,28,[shape('M-8 -6 Q0 -10 8 -4 L6 26 Q-1 32 -13 28 Q-18 22 -9 20Z','#d49a65')]))
d.append(part('tail','root',57,-58,[shape('M-6 9 Q17 0 16 -26 Q30 -17 23 1 Q16 18 0 20Z','#b9794e')]))
d.append(part('tailTip','tail',18,-15,[shape('M-4 6 Q2 -4 -3 -15 Q11 -13 10 -2 L6 12Z',cream)]))
d.append(part('body','root',0,-49,[shape('M-53 -17 Q-29 -36 29 -25 Q57 -25 61 -3 Q64 19 39 26 L-30 25 Q-61 18 -53 -17Z','#d49a65'),shape('M-40 4 Q-24 18 15 14 L38 25 L-30 25 Q-48 22 -48 10Z','#edbf87',None)]))
d.append(part('head','body',-48,-16,[shape('M-23 -25 Q0 -44 24 -21 L28 6 Q23 31 -4 29 Q-33 25 -32 2Z','#d49a65'),shape('M-23 4 Q-10 -5 0 6 Q12 -3 22 9 Q25 28 -2 30 Q-29 26 -23 4Z',cream),shape('M-21 -9 Q-13 -22 -5 -9 L-5 1 Q-18 8 -21 -9 M6 -10 Q14 -23 20 -9 L19 1 Q6 7 6 -10','#fff9ee'),shape('M-15 -11 Q-8 -14 -9 -2 Q-17 4 -15 -11 M10 -11 Q17 -14 16 -2 Q8 4 10 -11',ink),shape('M-8 8 Q0 4 8 8 Q7 17 0 17 Q-7 16 -8 8Z',ink),shape('M0 16 Q-1 25 -10 21 M0 17 Q4 25 12 20','none',ink,1.3),shape('M-16 -23 L-8 -25 M8 -25 L16 -23','none',ink,2)]))
for side,x in [('L',-24),('R',23)]:
 d.append(part('ear'+side,'head',x,-19,[shape('M-7 -5 Q-20 -9 -19 9 Q-21 35 -10 35 Q0 33 5 6Z','#754b3c'),shape('M-9 3 Q-14 14 -10 26','none','#9d6b50',3)]))
next(p for p in b if p['name']=='head')['scale']=.82
characters={'boy':b,'dog':d}
ET.register_namespace('', 'http://www.w3.org/2000/svg')
ns='{http://www.w3.org/2000/svg}'
def svg(content,box='-120 -100 240 320'):return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{box}">{content}</svg>'
def markup(s):return f'<path d="{s["d"]}" fill="{s["fill"]}" stroke="{s["stroke"] or "none"}" stroke-width="{s["width"]}" stroke-linejoin="round" stroke-linecap="round"/>'
for char,parts in characters.items():
 folder=OUT/char; folder.mkdir(exist_ok=True); assembled=[]; positions={}; scales={}
 for p in parts:
  parent=positions.get(p['parent'],(0,0)); inherited=scales.get(p['parent'],1); positions[p['name']]=(parent[0]+p['x']*inherited,parent[1]+p['y']*inherited); scales[p['name']]=inherited*p.get('scale',1)
  raw=''.join(map(markup,p['shapes'])); (folder/(p['name']+'.source.svg')).write_text(svg(raw))
  traced=[]
  for i,s in enumerate(p['shapes']):
   # Trace outline and interior separately, preserving the illustrated line weight.
   for label,color,stroke in [('outline',s['stroke'],True),('fill',s['fill'],False)]:
    if not color or color=='none':continue
    mask=dict(s,fill='#000',stroke='#000' if stroke else None)
    if s['fill']=='none':
     if not stroke:continue
     mask['fill']='none'
    png=cairosvg.svg2png(bytestring=svg(markup(mask)).encode(),output_width=720,output_height=960)
    image=Image.open(io.BytesIO(png)); bg=Image.new('RGB',image.size,'white'); bg.paste(image,mask=image.getchannel('A'))
    stem=folder/f'{p["name"]}-{i}-{label}'; bg.save(str(stem)+'.png'); bg.convert('L').point(lambda x:0 if x<160 else 255,'1').save(str(stem)+'.pbm')
    subprocess.run([POTRACE,str(stem)+'.pbm','-s','--flat','-t','2','-a','1','-o',str(stem)+'.svg'],check=True)
    tree=ET.parse(str(stem)+'.svg'); groups=[ET.tostring(e,encoding='unicode').replace('#000000',color) for e in tree.getroot() if e.tag!=ns+'metadata']
    traced.append(f'<g transform="translate(-120 -100) scale(0.3333333333)">{"".join(groups)}</g>')
  p['art']=''.join(traced);
  if (char=='boy' and p['name']=='ankleL') or (char=='dog' and p['name']=='earR'):
   p['art']='<g transform="scale(-1 1)">'+p['art']+'</g>'; raw='<g transform="scale(-1 1)">'+raw+'</g>'
  (folder/(p['name']+'.svg')).write_text(svg(p['art']))
  x,y=positions[p['name']]; assembled.append(f'<g transform="translate({x} {y}) scale({scales[p['name']]})">{raw}</g>')
 content=''.join(assembled); source=svg(content,'-130 -170 260 340'); (folder/'complete.source.svg').write_text(source)
 png=cairosvg.svg2png(bytestring=source.encode(),output_width=780,output_height=1020); (folder/'complete.png').write_bytes(png)
 im=Image.open(io.BytesIO(png)); bg=Image.new('RGB',im.size,'white'); bg.paste(im,mask=im.getchannel('A')); bg.convert('L').point(lambda x:0 if x<230 else 255,'1').save(folder/'complete.pbm')
 subprocess.run([POTRACE,str(folder/'complete.pbm'),'-s','-o',str(folder/'complete.trace.svg')],check=True)
(OUT/'characters.json').write_text(json.dumps(characters))
print('Built both characters with genuine Potrace masks, part vectors and complete traces.')
