"""Blue Sky study: moving layouts, nested frames, dispersed paper tiles.

All movement is confined to authored background graphics. No portrait scale,
music edit, subtitle relocation, external asset or wall-clock animation.
"""
bg_scenes={s['id']:s for s in scenes}

def bg_span(s): return s['endFrame']-s['startFrame']

def bg_drift(s,sel,x,y=0,rotation=0):
 ft(s,sel,{'x':0,'y':0,'rotation':0},{'x':x,'y':y,'rotation':rotation},s['startFrame'],bg_span(s),'none')

def bg_svg(s,name,markup,opacity=1):
 return node(s,'motion-'+name,f'<svg width="100%" height="100%" viewBox="0 0 1920 1080">{markup}</svg>',f'inset:0;width:1920px;height:1080px;opacity:{opacity};pointer-events:none;','background','shape','data-layout-ignore')

def bg_frames(s,cx,cy,w,h,color,opacity=.3,start=None,end=None):
 # Like the reference's nested windows, but open hand-ink frames, never copies
 # of the hero artwork. Opposing corner offsets give parallax at fixed scale.
 start=s['startFrame'] if start is None else start
 end=s['endFrame'] if end is None else end
 for i in range(3):
  x=cx-w/2-i*54;y=cy-h/2-i*34
  ww=w+i*108;hh=h+i*68
  d=f'M{x+8} {y}L{x+ww} {y+6} {x+ww-5} {y+hh} {x} {y+hh-4}Z'
  sel=bg_svg(s,'frame-'+str(i),f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{5-i}"/>',0)
  f=start+i*4
  ft(s,sel,{'opacity':0,'x':(i-1)*48,'y':30+i*15},{'opacity':opacity*(1-i*.2),'x':0,'y':0},f,16,'power2.out')
  to(s,sel,{'x':(i-1)*34,'y':-32-i*12},f+16,max(1,end-f-16),'sine.inOut')
  if end<s['endFrame']:to(s,sel,{'opacity':0},end-9,9,'sine.inOut')

def bg_tiles(s,side,color,start=None,end=None):
 # A small margin constellation expands, drifts, then regroups. Not a full
 # screen particle field; keep face/typography zones visually quiet.
 start=s['startFrame'] if start is None else start
 end=s['endFrame'] if end is None else end
 for i in range(7):
  x=(85 if side=='left' else 1720)+(i%2)*65
  y=115+i*127;size=[35,19,52,28,42,23,32][i]
  sel=node(s,'motion-tile-'+str(i),'',f'left:{x}px;top:{y}px;width:{size}px;height:{size}px;background:{color};opacity:0;border:2px solid {color};transform-origin:50% 50%;','background','shape','data-layout-ignore')
  f=start+(i%3)*3
  ft(s,sel,{'opacity':0,'x':-40 if side=='left' else 40,'y':(3-i)*35,'rotation':-15},{'opacity':.2+(i%3)*.06,'x':0,'y':0,'rotation':8},f,15,'power2.out')
  mid=start+int((end-start)*.58)
  to(s,sel,{'x':(-1 if i%2 else 1)*(24+i*4),'y':-25-i*3,'rotation':30 if i%2 else -20},f+15,max(1,mid-f-15),'sine.inOut')
  to(s,sel,{'x':0,'y':-45,'rotation':0,'opacity':.12},mid,max(1,end-mid),'sine.inOut')

def bg_orbit(s,cx,cy,rx,ry,color,opacity=.35):
 # Elliptical paper orbits, not neon bars. Broken rings stay behind the actor.
 markup=f'<g fill="none" stroke="{color}" stroke-width="3"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" stroke-dasharray="220 85 30 110"/><ellipse cx="{cx}" cy="{cy}" rx="{rx+32}" ry="{ry+22}" stroke-dasharray="80 200 14 130"/></g>'
 sel=bg_svg(s,'orbit',markup,opacity)
 ft(s,sel+' g',{'rotation':-12,'svgOrigin':f'{cx} {cy}'},{'rotation':26,'svgOrigin':f'{cx} {cy}'},s['startFrame'],bg_span(s),'none')
 for i in range(4):
  a=i*1.63;xx=cx+math.cos(a)*rx;yy=cy+math.sin(a)*ry
  p=node(s,'motion-orbit-chip-'+str(i),f'<svg viewBox="0 0 32 32"><path d="M16 1L20 12 31 16 20 20 16 31 12 20 1 16 12 12Z" fill="{color}"/></svg>',f'left:{xx-12}px;top:{yy-12}px;width:24px;height:24px;opacity:{opacity};','background','shape','data-layout-ignore')
  n=16
  for k in range(n):
   def pose(q):
    theta=a+q*.56
    return {'x':cx+math.cos(theta)*rx-xx,'y':cy+math.sin(theta)*ry-yy,'rotation':q*65}
   ft(s,p,pose(k/n),pose((k+1)/n),s['startFrame']+k*bg_span(s)/n,bg_span(s)/n,'none')

# Opening: animate the existing screens instead of piling on decoration.
for sid,offset in [('distance','64px -48px'),('voice','-64px 64px'),('return','80px -32px')]:
 s=bg_scenes[sid]
 ft(s,'#'+sid+'-dots',{'backgroundPosition':'0px 0px'},{'backgroundPosition':offset},s['startFrame'],bg_span(s),'none')
bg_drift(bg_scenes['distance'],'#distance-field',-110)
bg_drift(bg_scenes['voice'],'#voice-paper',-85)
bg_drift(bg_scenes['return'],'#return-pinkzone',0,-65)

s=bg_scenes['promise']
bg_frames(s,960,540,1540,820,'#a987a4',.24)
bg_tiles(s,'right','#d9b7d7')
s=bg_scenes['night']
bg_drift(s,'#night-disc',-65,24)
bg_orbit(s,1310,490,620,650,'#eee0c0',.3)

# Existing SVG scenery is decomposed by element: wave, halftone and moon travel
# at different rates; the SVG viewport remains fixed and never reveals seams.
s=bg_scenes['append-voice']; a=s['startFrame']; d=bg_span(s)
ft(s,'#append-voice-scene-paper svg > path:nth-child(1)',{'attr':{'d':'M0 0H710Q900 390 610 1080H0Z'}},{'attr':{'d':'M0 0H640Q1050 460 690 1080H0Z'}},a,d,'sine.inOut')
ft(s,'#append-voice-scene-paper svg > path:nth-child(2)',{'attr':{'d':'M0 890Q500 700 910 940T1920 950V1080H0Z'}},{'attr':{'d':'M0 950Q500 810 910 860T1920 920V1080H0Z'}},a,d,'sine.inOut')
bg_drift(s,'#append-voice-scene-paper svg > g',0,-70)
bg_tiles(s,'right','#a56e91')
s=bg_scenes['append-answer']
bg_drift(s,'#append-answer-scene-paper svg > circle',-65,26)
bg_orbit(s,1470,410,650,620,'#98729f',.3)
s=bg_scenes['append-together']
bg_drift(s,'#append-together-scene-paper svg > ellipse',70,-24)
# Keep the original SVG placement transform on the petal; animate its wrapper.
import re
s['layers']['background']=[re.sub(r'(<path d="M-12 0[^>]+/>)',r'<g class="motion-petal">\1</g>',m) for m in s['layers']['background']]
bg_drift(s,'#append-together-scene-paper .motion-petal',-42,55)
bg_frames(s,780,535,1260,870,'#bf8ba1',.28)

s=bg_scenes['append-relay-distance']
bg_drift(s,'#append-relay-distance-night-paper svg > path:nth-child(3)',-45,25,-2)
bg_drift(s,'#append-relay-distance-night-paper svg > path:nth-child(4)',65,-20,3)
bg_tiles(s,'left','#e7ecdd')
s=bg_scenes['append-relay-reply']
bg_drift(s,'#append-relay-reply-reply-paper svg > path:nth-child(3)',70,-45,3)
bg_orbit(s,1200,530,645,500,'#ab7c97',.38)
bg_tiles(s,'left','#c38da8')

# Flight already has four moving oil-paper planes and matched note trajectories.
# Keep that deliberate continuous journey; no new overlay on its painted vistas.

s=bg_scenes['append-finale-answer']
bg_drift(s,'#append-finale-answer-edge-disc-0',70,-80)
bg_drift(s,'#append-finale-answer-edge-disc-1',-100,-45)
bg_frames(s,960,545,1200,830,'#b98da0',.46,end=1589)
# The impact graphic covers these frames at 1589; use its own flat wave motion.
bg_drift(s,'#append-finale-answer-answer-flower svg > path:nth-child(2)',0,-60)
s=bg_scenes['append-finale-reunion']
for i in range(3):
 bg_drift(s,f'#append-finale-reunion-field-{i}',[-90,25,90][i],0,[-3,2,3][i])
for i in range(3):
 bg_drift(s,f'#append-finale-reunion-soft-light-{i}',[60,-90,30][i],[-55,70,-50][i])
bg_frames(s,960,540,1710,850,'#b99ba9',.36)

for s in scenes:
 if any('motion-' in x for x in s['layers']['background']) or s['id'] in ['distance','voice','return']:
  mark(s,s['startFrame'],'V26 背景分层运动：纸面、画框与图案独立于人物','reference-led background choreography','不改人物尺寸、歌词位置及音乐时间')
