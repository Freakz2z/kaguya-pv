# Four edited shots. Absolute 30fps frames, after the existing 1028-frame cut.
# Iris primitive adapted from compositions/components/iris-reveal.html:
# explicit circle endpoints, no runtime randomness, then a still hold.
D=1487/30
NAVY='#302e49'; PALE='#ded4e4'
relaycss="@font-face{font-family:PaintHeavy;src:local('Arial')}@font-face{font-family:PaintMincho;src:local('Arial')}"
def relay_scene(sid,a,b,bg,desc):
 s=scene('append-relay-'+sid,a,b,bg,desc);s['css'].append(relaycss);return s

def rtext(s,name,copy,x,y,size,color=PINK,font='PaintHeavy'):
 return node(s,name,html.escape(copy),f'left:{x}px;top:{y}px;font:{size}px/1.1 {font};color:{color};white-space:nowrap;opacity:0;','text','type','data-layout-allow-overlap data-layout-allow-occlusion')

def paint(s,name,asset,layer='background'):
 grading=html.escape(J(json.loads((P/'source/revision-v20/scene-grades.json').read_text())[asset]),quote=True)
 return node(s,name,f'<img data-color-grading="{grading}" src="assets/art/relay-v17/{asset}-oil.png" style="width:100%;height:100%;object-fit:cover;display:block"/>','inset:0;width:1920px;height:1080px;',layer,'shape','data-layout-ignore')

def outlined(s,sel,color=PAPER,width=8):
 s['css'].append(sel+f'{{paint-order:stroke fill;-webkit-text-stroke:{width}px {color};}}')

def papergrain(s,color=INK,opacity=.06):
 # A fine print screen is a surface, not another animated subject.
 node(s,'grain','',f'inset:0;opacity:{opacity};background-image:radial-gradient({color} .8px,transparent 1px);background-size:5px 5px;','transition','shape','data-layout-ignore')

def crescent(s,name,x,y,w,color,layer='foreground'):
 svg=f'<svg width="100%" height="100%" viewBox="0 0 420 480"><path d="M318 20C144 17 22 128 28 274C34 425 195 497 337 429C196 430 117 319 145 196C163 119 224 59 318 20Z" fill="{color}"/></svg>'
 return node(s,name,svg,f'left:{x}px;top:{y}px;width:{w}px;height:{w*480/420}px;transform-origin:50% 50%;',layer)

# Musical-note contours share a head pivot, allowing the squeezed glyph to
# become a note at the same location rather than crossfading unrelated layouts.
def note(s,name,x,y,size,color=PAPER,layer='foreground',hidden=False,variant=0):
 paths=['M61 123V17C66 42 104 34 99 66C96 80 85 86 79 87','M61 123V17','M61 123V17C66 38 104 32 99 58C96 70 85 76 79 77 M61 43C66 64 102 58 98 83C95 95 85 101 79 102']
 path=paths[variant%3]
 svg=f'''<svg width="100%" height="100%" viewBox="0 0 120 160"><path d="{path}" fill="none" stroke="#443247" stroke-width="17" stroke-linecap="round" stroke-linejoin="round"/><ellipse class="note-head" cx="40" cy="127" rx="26" ry="18" transform="rotate(-22 40 127)" fill="{color}" stroke="#443247" stroke-width="3"/><path class="note-stem" d="{path}" fill="none" stroke="{color}" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/><path d="M24 124Q34 113 46 115" fill="none" stroke="#fff8df" stroke-opacity=".8" stroke-width="3" stroke-linecap="round"/></svg>'''
 return node(s,name,svg,f'left:{x}px;top:{y}px;width:{size}px;height:{size*4/3}px;transform-origin:33.333% 79.375%;'+('opacity:0;' if hidden else ''),layer,'shape','data-layout-allow-overflow')

def note_draw(s,sel,start):
 s['js'].append(f"document.querySelectorAll('{sel} .note-stem').forEach(p=>{{const l=p.getTotalLength();p.style.strokeDasharray=l;p.style.strokeDashoffset=l;}});")
 ft(s,sel+' .note-head',{'scale':.05,'opacity':0,'svgOrigin':'40 127'},{'scale':1,'opacity':1},start,6)
 to(s,sel+' .note-stem',{'strokeDashoffset':0},start+3,9,'power2.out')

def eclipse_bars(s,start_height,end_height,frame,dur):
 for edge in ('top','bottom'):
  b=node(s,'cinema-'+edge,'',f'left:0;{edge}:0;width:1920px;height:{start_height}px;background:#171522;','transition','shape','data-layout-ignore')
  ft(s,b,{'height':start_height},{'height':end_height},frame,dur,'sine.inOut')

def lunar_disc(s,x,y,size):
 # Hand-cut lunar paper, with restrained craters. No architectural environment.
 markup=f'''<svg width="100%" height="100%" viewBox="0 0 400 400"><circle cx="200" cy="200" r="188" fill="#eadcba" stroke="#f8f0d9" stroke-width="7"/><path d="M234 17C365 45 411 207 325 326C275 389 159 413 82 346C221 362 317 265 305 168C301 99 276 52 234 17Z" fill="#d6c8ae" opacity=".75"/><g fill="none" stroke="#b5a38a" stroke-width="3" opacity=".45"><ellipse cx="132" cy="121" rx="31" ry="24" transform="rotate(-20 132 121)"/><path d="M113 125Q126 104 153 114"/><ellipse cx="238" cy="263" rx="46" ry="31" transform="rotate(25 238 263)"/><ellipse cx="107" cy="258" rx="17" ry="22"/><path d="M258 123Q296 132 288 167M216 315Q249 333 275 317"/></g></svg>'''
 return node(s,'moon',markup,f'left:{x}px;top:{y}px;width:{size}px;height:{size}px;','foreground')

# ① 34.267–36.433. New pajama sticker, registered mouth-only cel animation.
s=relay_scene('distance',1028,1093,PAPER,'声音接力①：睡衣彩叶握三环手环，沉闷唱歌，嘴型开合')
node(s,'night-paper','<svg viewBox="0 0 1920 1080" width="100%" height="100%"><path d="M0 0H740L1030 1080H0Z" fill="#91a9b2"/><path d="M0 0H190L400 1080H0Z" fill="#39465e"/><path d="M790 115L1830 60 1890 1010 1060 1000Z" fill="#ead8df"/><path d="M1230 75L1810 45 1850 260 1260 290Z" fill="#f5efe7"/><path d="M1870 0Q1650 110 1860 350" fill="none" stroke="#ad879d" stroke-width="15"/></svg>','inset:0;','background')
# The two images stay in one local coordinate system. Only mouth patch toggles.
height=1030*Image.open(P/'assets/art/relay-v15/iroha-pajama-closed.png').height/Image.open(P/'assets/art/relay-v15/iroha-pajama-closed.png').width
actor=node(s,'iroha',f'<img src="assets/art/relay-v15/iroha-pajama-closed.png" style="width:100%;display:block"/><img id="iroha-singing-mouth" src="assets/art/relay-v15/iroha-pajama-open.png" style="position:absolute;inset:0;width:100%;clip-path:ellipse(4% 3.5% at 48.4% 53.6%);opacity:0"/>',f'left:30px;top:-85px;width:1030px;height:{height}px;transform-origin:50% 85%;','character')
# Mild continuous singing sway, not random position jumps.
ft(s,actor,{'rotation':-1.1,'y':2},{'rotation':1.1,'y':-2},1028,17,'sine.inOut')
for f,r,y in [(1045,-1.1,2),(1062,1.1,-2),(1079,0,0)]:to(s,actor,{'rotation':r,'y':y},f,14 if f==1079 else 17,'sine.inOut')
for f,op in [(1028,0),(1032,1),(1040,0),(1043,1),(1053,0),(1056,1),(1067,0),(1071,1),(1080,0),(1083,1)]:st(s,'#iroha-singing-mouth',{'opacity':op},f)
t=rtext(s,'voice','この声を',1040,160,125,INK,'PaintMincho')
outlined(s,t)
ft(s,t,{'opacity':0,'y':15},{'opacity':1,'y':0},1028,10)
for i,(c,x,y,z,r) in enumerate([('届',880,365,390,-7),('い',1235,520,280,8),('て',1495,665,310,-5)]):
 t=rtext(s,'reach-'+str(i),c,x,y,z,PINK)
 outlined(s,t,PAPER,13)
 a={'opacity':0,'rotation':r};b={'opacity':1,'rotation':r}
 if i==0:a['clipPath']='inset(0 100% 0 0)';b['clipPath']='inset(0 0% 0 0)'
 elif i==1:a['scaleY']=.3;b['scaleY']=1
 else:a['y']=55;b['y']=0
 ft(s,t,a,b,1038+i*6,9,'power3.out')
n=note(s,'sing-note',1635,350,90,INK,hidden=True)
ft(s,n,{'opacity':0,'y':25,'rotation':-13},{'opacity':.8,'y':0,'rotation':9},1058,10)
star(s,'small-star',1785,570,60,1065,GOLD)
mark(s,1032,'睡衣彩叶低落唱歌；闭眼、泪痣、双手握三环','mouth cel timing','开闭口为演出时序，非音素级唇同步')
mark(s,1042,'大字届いて和声音装饰进入','phrase choreography')

# ② Preserve the approved three-letter entrance; enrich the panels and morph.
s=relay_scene('panels',1093,1173,NAVY,'声音接力②：三格文字保留，字形压成音符，画面开始收束')
launch=paint(s,'flight-prelap','launch')
ft(s,launch,{'opacity':0},{'opacity':1},1152,21,'sine.inOut')
for i,(x,y,w,h,col) in enumerate([(45,100,580,820,PAPER),(665,45,580,820,PALE),(1280,155,580,820,'#e8c8d3')]):
 sheet=f'<svg width="100%" height="100%" viewBox="0 0 535 680"><path d="M9 8L520 3 530 666 12 678 4 355Z" fill="{col}" stroke="{PAPER}" stroke-width="4"/><path d="M25 638L100 620M25 646L127 620M25 654L153 620M25 662L178 620" fill="none" stroke="{INK}" stroke-opacity=".18" stroke-width="2"/><circle cx="445" cy="78" r="40" fill="none" stroke="{INK}" stroke-opacity=".13" stroke-width="6"/><path d="M25 40H125M25 54H80" stroke="{INK}" stroke-opacity=".14" stroke-width="4"/></svg>'
 p=node(s,f'panel-{i}',sheet,f'left:{x}px;top:{y}px;width:{w}px;height:{h}px;opacity:0;','background')
 ft(s,p,{'opacity':1,'clipPath':'inset(100% 0 0 0)'},{'opacity':1,'clipPath':'inset(0% 0 0 0)'},1093+i*5,10)
 label=rtext(s,f'glyph-{i}','届いて'[i],x+0,y+100,550,PINK if i!=1 else NAVY)
 s['css'].append(label+'{width:550px;height:605px;transform-origin:50% 50%;}')
 if i==0:ft(s,label,{'opacity':1,'x':-85,'clipPath':'inset(0 100% 0 0)'},{'opacity':1,'x':0,'clipPath':'inset(0 0% 0 0)'},1093,12)
 elif i==1:ft(s,label,{'opacity':1,'scaleY':.15,'rotation':-13},{'opacity':1,'scaleY':1,'rotation':4},1101,12,'back.out(1.1)')
 else:ft(s,label,{'opacity':1,'y':-95,'rotation':9},{'opacity':1,'y':0,'rotation':-4},1109,12)
 for sel in (p,label):to(s,sel,{'y':[-24,35,-18][i]},1129,9,'power2.inOut')
 # Decorative notes are nested into each printed panel and disappear with it.
 dec=note(s,'margin-note-'+str(i),x+405,y+470,55,INK,hidden=True)
 ft(s,dec,{'opacity':0,'rotation':-12},{'opacity':.22,'rotation':6},1115+i*5,9)
 # Each character compresses into the same notehead position, then a stem draws out.
 pivotx=x+275; pivoty=y+100+302.5+[-24,35,-18][i]
 destx,desty=[(430,520),(800,345),(1180,555)][i]
 transform_at=1142+i*3
 to(s,label,{'scaleX':.16,'scaleY':.095,'rotation':-22,'color':GOLD},transform_at,10,'power2.in')
 to(s,label,{'opacity':0},transform_at+8,3)
 n=note(s,'travel-note-'+str(i),pivotx-40,pivoty-127,120,[GOLD,'#efb5b0','#b3e5df'][i],hidden=True,variant=i)
 ft(s,n,{'opacity':0},{'opacity':1},transform_at+7,3)
 note_draw(s,n,transform_at+7)
 # Continuous endpoint velocity; separate lanes instead of a single gathered knot.
 start=1153+i*2;duration=1173-start
 x0=pivotx-40;y0=pivoty-127
 for step in range(duration):
  def key(k):
   q=k/duration; h=q*q*(3-2*q); tangent=q*q*(q-1)
   return {'x':(destx-x0)*h+tangent*duration*1.2,'y':(desty-y0)*h,'rotation':[-12,10,-4][i]*h}
  ft(s,n,key(step),key(step+1),start+step,1,'none')
 to(s,[p,dec],{'scaleY':.78,'opacity':0},1155+i*2,13,'power2.in')
star(s,'relay-a',575,820,65,1112,GOLD)
star(s,'relay-b',1170,140,45,1129,PAPER)
for sel in ['#append-relay-panels-relay-a','#append-relay-panels-relay-b']:to(s,sel,{'opacity':0},1155,9)
# The print fields leave at different depths, exposing a common flight corridor.
for i in range(3):
 to(s,f'#append-relay-panels-panel-{i}',{'rotation':[-7,5,-5][i],'x':[-90,0,90][i]},1142+i*3,20,'power2.in')
# Matte starts closing here; next shot continues from precisely 60px.
eclipse_bars(s,0,60,1155,18)
papergrain(s,PAPER,.04)
mark(s,1093,'保留届・い・て三格字入场','onset candidate 36.434')
mark(s,1142,'三个字依次压成符头、长出符干','text to music-note transformation')
mark(s,1155,'纸格退场；上下黑边开始收束','continuous framing handoff')


# ③ A 216-frame journey, cut into distinct spaces. No one-take camera.
# Each cut matches the dominant note direction; foreground paper motivates the cut.
def plate(s,name,markup,layer='background',style='inset:0;'):
 return node(s,name,'<svg width="100%" height="100%" viewBox="0 0 1920 1080">'+markup+'</svg>',style,layer,'shape','data-layout-ignore')

def flight(s,name,points,size,color,frame,dur,scale=(1,1),rot=(-15,15),layer='foreground',fade=False):
 # Sample the quadratic every <=2 frames into visible GSAP properties.
 # No helper-state callbacks: forward, reverse and exact-cut seeks share poses.
 (x0,y0),(cx,cy),(x1,y1)=points
 s.setdefault('noteFlights',[]).append(dict(name=name,points=points,size=size,color=color,frame=frame,dur=dur,scale=scale,fade=fade))
 sel=note(s,name,x0,y0,size,color,layer)
 def pose(t):
  p=(1-math.cos(math.pi*t))/2; q=1-p
  return {'x':q*q*x0+2*q*p*cx+p*p*x1-x0,'y':q*q*y0+2*q*p*cy+p*p*y1-y0,
          'scale':scale[0]+p*(scale[1]-scale[0]),'rotation':rot[0]+p*(rot[1]-rot[0]),
          'opacity':1-max(0,(p-.9)/.1) if fade else 1}
 s['js'].append(f"gsap.set({J(sel)},{J(pose(0))});")
 count=math.ceil(dur/2)
 for step in range(count):
  ft(s,sel,pose(step/count),pose((step+1)/count),frame+dur*step/count,dur/count,'none')
 return sel

def paper_cut(s,frame,duration,color,incoming=False):
 # Directional paper edge, not speed lines. Covers the cut on both sides.
 d='M150 -30L2020 -30V1110H150L205 970 110 850 194 710 125 570 195 420 108 260 176 110Z'
 cover=node(s,'paper-cut-'+str(frame),f'<svg width="100%" height="100%" viewBox="0 0 2400 1080"><path d="{d.replace("2020","2500")}" fill="{color}"/></svg>','left:0;top:0;width:2400px;height:1080px;','foreground','shape','data-layout-ignore')
 if incoming:ft(s,cover,{'x':-220},{'x':-2500},frame,duration,'power3.out')
 else:
  st(s,cover,{'x':1940},s['startFrame'])
  ft(s,cover,{'x':1940},{'x':-220},frame,duration,'power3.in')

def print_starfield(s,count,color=PAPER):
 # Fixed layout, no ambient random particles.
 for i in range(count):
  x=(i*337+195)%1850; y=170+(i*193)%730
  size=[4,7,5,10,3][i%5]
  node(s,'sky-'+str(i),'',f'left:{x}px;top:{y}px;width:{size}px;height:{size}px;border-radius:50%;background:{color};opacity:{.18+(i%4)*.09};','background')

exec(compile((P/'source/revision-v25/journey.py').read_text(),'revision-v21/journey.py','exec'),globals())

# ④ Working → hears a voice → starry joy. Keep verified art, change staging.
s=relay_scene('reply',1389,1487,PAPER,'声音接力④：辉夜写字处理事务，听见歌声后切到放下手的星星眼上半身')
node(s,'reply-paper','<svg viewBox="0 0 1920 1080" width="100%" height="100%"><path d="M0 0H1920V1080H0Z" fill="#e0d0df"/><path data-layout-allow-overflow d="M-40 80L520 20 650 1080H0Z" fill="#f5efe7"/><path data-layout-allow-overflow d="M660 0Q1730 -110 1830 650T700 1130Q450 690 660 0Z" fill="#d9adbb"/><path d="M640 980Q1550 880 1920 1020V1080H650Z" fill="#65516d"/></svg>','inset:0;','background')
a=img(s,'working','relay-v15/kaguya-robe-working.png',625,30,1000,extra='transform-origin:50% 65%;')
b=img(s,'starry','revision-v30/kaguya-desk-joy.png',625,30,1000,extra='opacity:0;transform-origin:50% 65%;')
# Registered transparent cels use isolated additive compositing during the fade.
# Their complementary alpha sums to one rather than flashing the background.
pose_markup=''.join(s['layers']['character'][-2:]);del s['layers']['character'][-2:]
node(s,'pose-pair',pose_markup,'inset:0;isolation:isolate;','character','shape','data-layout-allow-overlap data-layout-allow-occlusion')
s['css'].append(a+','+b+'{mix-blend-mode:plus-lighter;}')
paper_cut(s,1389,7,PAPER,True)
# Recognition is conveyed by the expression cut and type, with no flying note.
ft(s,a,{'opacity':1},{'opacity':0},1422,6,'sine.inOut')
ft(s,b,{'opacity':0},{'opacity':1},1422,6,'sine.inOut')
# One damped sticker tremble AFTER the pose resolves; no scale pulse or loop.
previous=1428
for frame,x,y,r in [(1430,-9,2,-.9),(1433,7,-2,.7),(1436,-5,1,-.45),(1439,3,0,.25),(1442,-1.5,0,-.12),(1446,0,0,0)]:
 to(s,b,{'x':x,'y':y,'rotation':r},previous,frame-previous,'sine.inOut');previous=frame
mark(s,1428,'新姿态落定后短促衰减抖动，随后静止','sticker tremble')
# Vertical type anchors the empty left field; the oversized final kana answers the pose.
for i,(c,x,y,z) in enumerate([('聞',150,145,250),('こ',255,410,155),('え',230,580,180),('る',270,775,160)]):
 t=rtext(s,'reply-'+str(i),c,x,y,z,INK,'PaintMincho')
 outlined(s,t,PAPER,7)
 ft(s,t,{'opacity':0,'x':-35 if i%2 else 35,'rotation':-8 if i==0 else 4},{'opacity':1,'x':0,'rotation':-4 if i==0 else 0},1390+i*3,9)
t=rtext(s,'reply-yo','よ',1460,690,300,PINK)
outlined(s,t,PAPER,12)
ft(s,t,{'opacity':0,'scale':.65,'rotation':12},{'opacity':1,'scale':1,'rotation':-7},1402,10,'back.out(1.1)')
for i,(x,y,z) in enumerate([(655,300,65),(1580,215,95),(1690,690,55)]):star(s,'joy-'+str(i),x,y,z,1422+i*5,GOLD)
eclipse_bars(s,138,0,1389,12)
mark(s,1389,'辉夜伏案写字，收到歌声后切换为放下手的上半身','working hold')
mark(s,1390,'转场同时开始回应文字，不再等待已删除的音符飞行','immediate response')
mark(s,1422,'同位伏案星星眼换稿，六帧柔和切换','recognition')
mark(s,1441,'完整回应保持1.53秒','final hold')
