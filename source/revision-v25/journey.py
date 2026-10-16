# 11–14 share a single world, camera and three note identities for 216 frames.
s=relay_scene('journey',1173,1389,NAVY,'声音远行：地球—精神世界—二维画境—月球，一镜到底')
grades=json.loads((P/'source/revision-v20/scene-grades.json').read_text())
# Full-frame painted planes overlap for 30 frames; no hard spatial seams.
# Each retains a fixed image size and translates gently through the same direction.
def ease01(v):
 v=max(0,min(1,v));return v*v*(3-2*v)
def camera(f):return 6*f
for i,(asset,start,end) in enumerate([('launch',0,74),('spirit',38,126),('flat',96,178),('moon',148,216)]):
 grading=html.escape(J(grades[asset]),quote=True)
 width=1920 if i==0 else 2120
 a=node(s,'world-'+asset,f'<img src="assets/art/relay-v17/{asset}-oil.png" data-color-grading="{grading}" style="width:100%;height:100%;object-fit:cover"/>',f'left:0;top:0;width:{width}px;height:1080px;opacity:{1 if i==0 else 0};','background','shape','data-layout-ignore')
 if i:
  ft(s,a,{'opacity':0},{'opacity':1},1173+start,30,'sine.inOut')
  ft(s,a,{'x':0},{'x':-180},1173+start,end-start,'none')
# Three identities remain separated in a staggered flying formation.
tracks=[]
for i,(x0,y0) in enumerate([(430,520),(800,345),(1180,555)]):
 def pose(f):
  # One continuous Hermite approach, not a late 22-frame sprint.
  end=195+i*6;q=max(0,min(1,f/end))
  h00=2*q**3-3*q*q+1;h10=q**3-2*q*q+q;h01=-2*q**3+3*q*q
  x=h00*x0+h10*(1.2*end)+h01*(1390+i*12)
  y=h00*y0+h01*(475+i*18)-52*math.sin(math.pi*q)**2
  z=1-.82*ease01((q-.48)/.52)
  alpha=1-ease01((q-.86)/.14)
  return {'x':x-x0,'y':y-y0,'scale':z,'opacity':alpha,'rotation':[-12,10,-4][i]+8*math.sin(f/216*math.pi*2)}
 color=[GOLD,'#efb5b0','#b3e5df'][i]
 a=note(s,'continuous-note-'+str(i),x0,y0,120,color,'character',variant=i)
 s['css'].append(a+' svg{stroke:#443247;stroke-width:1.5px;paint-order:stroke fill;}')
 samples=[]
 for f in range(217):
  v=pose(f);samples.append([x0+v['x']+40,y0+v['y']+127,v['scale'],v['opacity'],camera(f)])
 for f in range(0,216,2):ft(s,a,pose(f),pose(f+2),1173+f,2,'none')
 tracks.append({'samples':samples,'color':color})
canvas_id=s['id']+'-trails-canvas'
node(s,'trails',f'<canvas id="{canvas_id}" width="1920" height="1080" style="width:100%;height:100%"></canvas>','inset:0;','foreground','shape','data-layout-ignore')
s['js'].append((P/'source/revision-v25/journey-trails.js').read_text().replace('__ID__',canvas_id).replace('__TRACKS__',J(tracks)))
# Stable foreground framing; no wipes, circles or note resets between worlds.
eclipse_bars(s,60,138,1173,12)
t=rtext(s,'far-phrase','どこまでも',185,190,180,PAPER,'PaintMincho');outlined(s,t,INK,6)
ft(s,t,{'opacity':0,'y':18},{'opacity':1,'y':0},1210,10);to(s,t,{'opacity':0,'y':-15},1254,12)
t=rtext(s,'toward-you','君へ',200,670,210,PAPER,'PaintMincho');outlined(s,t,INK,6)
ft(s,t,{'opacity':0,'clipPath':'inset(0 100% 0 0)'},{'opacity':1,'clipPath':'inset(0 0% 0 0)'},1277,12);to(s,t,{'opacity':0},1320,12)
shine=node(s,'received-light','','left:1198px;top:173px;width:724px;height:724px;border-radius:50%;background:#fff0c4;mix-blend-mode:screen;opacity:0;','foreground')
ft(s,shine,{'opacity':0},{'opacity':.20},1360,12);to(s,shine,{'opacity':.05},1372,17)
t=rtext(s,'arrived','届いた',215,615,175,PAPER,'PaintMincho');outlined(s,t,INK,7)
ft(s,t,{'opacity':0,'y':16},{'opacity':1,'y':0},1368,12)
for i,(x,y,z) in enumerate([(1060,260,56),(1120,765,36),(1770,820,48)]):star(s,'arrival-star-'+str(i),x,y,z,1370+i*4,GOLD)
mark(s,1173,'分离队形与前镜等速接续；四幅油画重叠过渡','single continuous journey')
mark(s,1368,'音符抵达月球；亮起并保留回应','arrival hold')
# Only the exit into the distinct Kaguya shot remains a cut.
paper_cut(s,1383,6,PAPER)
