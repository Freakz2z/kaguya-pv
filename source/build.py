import sys
if sys.version_info < (3, 11):
 raise SystemExit('Python 3.11+ is required to rebuild this project. Preview with npm run dev needs only Node.js.')
from pathlib import Path
import json,math,html,csv,unicodedata,hashlib,argparse
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools import subset
P=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description='Rebuild V07; refuse to overwrite unincorporated Studio edits.')
parser.add_argument('--adopt-existing',action='store_true',help='First build only: adopt existing HTML after saving it in Git.')
parser.add_argument('--overwrite-edited',action='store_true',help='Only after incorporating saved Studio edits into this source.')
parser.add_argument('--refresh-fonts',action='store_true',help='Regenerate bundled font subsets from local macOS fonts.')
args=parser.parse_args()
state=P/'source/generated-files.json'
digest=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
if state.exists():
 changed=[n for n,h in json.loads(state.read_text()).items() if not (P/n).exists() or digest(P/n)!=h]
 if changed and not args.overwrite_edited:raise SystemExit('Generated files changed outside build.py; save and incorporate these edits before rebuilding: '+', '.join(changed))
elif (P/'index.html').exists() and not args.adopt_existing:
 raise SystemExit('Save current HTML in Git, then run once with --adopt-existing.')
FPS=30;D=590/30;START=169.1
for d in ['assets/art','assets/audio','assets/fonts','assets/vendor','compositions','qa','renders','boards']:(P/d).mkdir(exist_ok=True,parents=True)
for n in ['art/kaguya-away-reference-v3.png','art/iroha-away.png','art/yachiyo-wait-reference-v3.png','art/reunion-corrected.png','audio/demo-silence.wav','vendor/gsap.min.js']:
 if not (P/'assets'/n).is_file():raise SystemExit('Required versioned asset missing: assets/'+n)
copy='遠く離れても君の声は消えないひとりじゃ何度でも夜を越また会える。あの日約束'
J=lambda a:json.dumps(a,ensure_ascii=False,separators=(',',':'))
INK='#322438';PAPER='#f5efe7';PINK='#ac2d53';LILAC='#cbb8d4';GOLD='#d5ad69'
cssbase="""@font-face{font-family:Heavy;src:local('Arial')}@font-face{font-family:Mincho;src:local('Arial')}@font-face{font-family:Hand;src:local('Arial')}*{box-sizing:border-box}.layer{position:absolute;inset:0;width:100%;height:100%}.type{position:absolute;display:block;white-space:nowrap;line-height:1.16;font-family:Heavy;color:#322438;transform-origin:center;opacity:0}.art{position:absolute;display:block;height:auto}.shape{position:absolute;display:block}.dotfield{background-image:radial-gradient(#9d668b 2px,transparent 2.5px);background-size:16px 16px;opacity:.2}.stroke-text{-webkit-text-stroke:3px #ac2d53;color:transparent}.sticker{paint-order:stroke fill;-webkit-text-stroke:12px #f5efe7;text-shadow:5px 7px 0 #322438}.paperframe{border:7px solid #322438;background:#f5efe7}.frameinner{position:absolute;inset:15px;border:2px solid #322438;pointer-events:none}"""
layer_names=dict(background='背景',backtext='后景文字',character='人物',foreground='前景特效',text='主文字',transition='转场')
scenes=[];events=[]
def scene(sid,a,b,bg,description):
 s={'id':sid,'startFrame':a,'endFrame':b,'bg':bg,'description':description,'layers':{k:[] for k in ['background','backtext','character','foreground','text','transition']},'css':[],'js':[],'states':[]};scenes.append(s);return s

def node(s,name,markup,style,layer='foreground',cls='shape',attrs=''):
 id=s['id']+'-'+name
 if cls=='type':s.setdefault('typeTargets',[]).append('#'+id)
 s['layers'][layer].append(f'<div id="{id}" class="{cls}" {attrs}>{markup}</div>');s['css'].append(f'#{id}'+'{'+style+'}');return '#'+id

def img(s,name,file,x,y,w,layer='character',extra=''):
 return node(s,name,f'<img class="art" src="assets/art/{file}" alt="" style="width:100%;left:0;top:0"/>',f'left:{x}px;top:{y}px;width:{w}px;height:{w*Image.open(P/"assets/art"/file).height/Image.open(P/"assets/art"/file).width}px;'+extra,layer)

exec(compile((P/'source/revision-v31/typography.py').read_text(),'revision-v31/typography.py','exec'),globals())
def ft(s,sel,a,b,frame,dur=6,ease='power3.out'):
 if strong_type_entry(s,sel,a,b,frame,dur,ease):return
 s['js'].append(f"tl.fromTo({J(sel)},{J(a)},{J(dict(b,duration=dur/30,ease=ease,immediateRender=False))},{(frame-s['startFrame'])/30});")
def to(s,sel,b,frame,dur=6,ease='power3.out'):s['js'].append(f"tl.to({J(sel)},{J(dict(b,duration=dur/30,ease=ease))},{(frame-s['startFrame'])/30});")
def st(s,sel,b,frame):s['js'].append(f"tl.set({J(sel)},{J(b)},{(frame-s['startFrame'])/30});")
def mark(s,f,what,anchor='drum onset',note=''):
 events.append({'frame':f,'time':round(f/30,4),'sourceTime':round(START+f/30-max(0,min(globals().get('PAUSE_LENGTH',0),f/30-globals().get('PAUSE_AT',999))),4),'scene':s['id'],'event':what,'anchor':anchor,'note':note});s['states'].append({'frame':f,'event':what})
def word(s,name,text,x,y,size,frame,mode='wipe',angle=0,color=INK,font='Heavy',layer='text',extra='',anticipate=0,anchor='drum onset'):
 sel=node(s,name,html.escape(text),f'left:{x}px;top:{y}px;font-size:{size}px;font-family:{font};color:{color};'+extra,layer,'type','data-layout-allow-overlap data-layout-allow-occlusion')
 initial={'opacity':0,'rotation':angle};end={'opacity':1,'rotation':angle}
 if mode=='wipe':initial.update(clipPath='inset(0 100% 0 0)',x=-22);end.update(clipPath='inset(0 0% 0 0)',x=0)
 elif mode=='rise':initial.update(y=160,rotation=angle-12);end.update(y=0)
 elif mode=='slam':initial.update(scale=1.4);end.update(scale=1)
 elif mode=='flip':initial.update(scaleY=.15,rotation=angle+16);end.update(scaleY=1)
 elif mode=='slide':initial.update(x=240);end.update(x=0)
 elif mode=='drop':initial.update(y=-100);end.update(y=0)
 dur=anticipate if anticipate else (5 if mode=='slam' else 7)
 if anticipate:initial['opacity']=1
 ft(s,sel,initial,end,frame-anticipate,dur);mark(s,frame,'文字 '+text, anchor=anchor,note='落定' if anticipate else '显现');return sel

def block(s,name,x,y,w,h,col,layer='background',extra=''):
 return node(s,name,'',f'left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{col};'+extra,layer)
def star(s,name,x,y,size,frame,color=GOLD):
 svg=f'<svg width="100%" height="100%" viewBox="0 0 100 100"><path d="M49 3L61 35 95 48 64 62 52 96 37 66 4 53 35 38Z" fill="{color}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/></svg>'
 sel=node(s,name,svg,f'left:{x}px;top:{y}px;width:{size}px;height:{size}px;opacity:0;','foreground')
 ft(s,sel,{'opacity':1,'scale':.25,'rotation':-25},{'opacity':1,'scale':1,'rotation':5},frame,5)
 to(s,sel,{'rotation':25,'scale':.85},frame+7,12);mark(s,frame,'星形强调 '+name);return sel

def band(s,name,y,h,col,frame,layer='foreground',angle=0):
 sel=block(s,name,-100,y,2120,h,col,layer,extra='opacity:0;')
 s['layers'][layer][-1]=s['layers'][layer][-1].replace('class="shape"','class="shape" data-layout-allow-overflow')
 ft(s,sel,{'x':-2200,'rotation':angle,'opacity':1},{'x':0,'rotation':angle,'opacity':1},frame-6,6,'power3.in');mark(s,frame,'横条接管 '+name);return sel

# 01 / distance: a narrow portrait slit becomes an open silhouette; reading then passes to type.
s=scene('distance',0,107,PAPER,'辉夜窄画格揭示，远近字组换位，再由倾斜纸面遮挡接走')
block(s,'field',970,0,950,1080,LILAC,extra='clip-path:polygon(18% 0,100% 0,100% 100%,0 100%);')
node(s,'dots','', 'left:1330px;top:640px;width:590px;height:440px;','background','dotfield')
word(s,'far','遠く',700,20,430,0,'slam',-7,PINK,layer='backtext',extra='opacity:1;')
a=img(s,'kaguya','revision-v19/kaguya-black-top.png',-70,20,1130)
ft(s,a,{'clipPath':'inset(0 70% 0 8%)','x':-80},{'clipPath':'inset(0 0% 0 0%)','x':0},0,18)
s['css'].append('#distance-character-layer{clip-path:polygon(0 0,1000px 0,890px 1080px,0 1080px)}')
mark(s,0,'窄画格展开辉夜','phrase onset (ASR estimate)')
word(s,'apart','離れて',1100,465,150,36,'rise',-8,anticipate=5)
word(s,'even','も',1540,525,170,53,'flip',9,PINK)
star(s,'star',1640,180,105,73)
label=block(s,'remember-label',1020,825,790,155,PAPER,'foreground',extra=f'opacity:0;border:5px solid {INK};')
ft(s,label,{'scaleX':.05,'rotation':-3,'opacity':1},{'scaleX':1,'rotation':-3,'opacity':1},83,6)
word(s,'memory','あの日の約束',1090,838,95,89,'wipe',-3,INK,'Mincho',anticipate=5)
mark(s,89,'右下纸签落定，不遮挡人物')
# 02 / voice: diagonal portrait frame, two rear words then foreground band captures centre.
s=scene('voice',107,196,LILAC,'彩叶漫画画框；字先在左侧形成词组，随后前景横条重写视觉重点')
block(s,'paper',780,-40,1050,1180,PAPER,extra='clip-path:polygon(16% 0,100% 0,86% 100%,0 100%);')
node(s,'dots','', 'left:0;top:0;width:650px;height:1080px;','background','dotfield')
a=img(s,'iroha','iroha-away.png',930,-35,900,extra='clip-path:polygon(16% 0,100% 0,100% 100%,0 100%);')
ft(s,a,{'x':160,'clipPath':'inset(0 0 100% 0)'},{'x':0,'clipPath':'inset(0 0 0% 0)'},107,10)
word(s,'you','君の',145,110,195,107,'drop',-8)
word(s,'voice','声',245,350,360,125,'slam',5,PINK,anticipate=4)
word(s,'topic','は',640,610,115,142,'flip',-4,font='Mincho')
band(s,'deny-strip',700,275,INK,160,'foreground',-4)
word(s,'notgone','消えない',260,710,230,160,'wipe',-4,PAPER,anticipate=6)
# Portrait remains fixed. Foreground text makes the occlusion swap; no character jolt.
to(s,['#voice-you','#voice-voice','#voice-topic'],{'opacity':.16},154,6)
star(s,'accent',1650,815,105,178,PAPER)
# 03 / promise: typographic interlude, letter relay and ink-to-paper inversion, then moon opening.
s=scene('promise',196,296,INK,'纯文字段：逐字出现、前后层交换、黑白反转，以圆形遮挡揭示八千代')
word(s,'one','ひとり',310,135,340,196,'wipe',-4,PAPER)
for name,c,x,y,f,mode in [('ja','じゃ',260,580,214,'rise'),('na','な',850,600,232,'flip'),('i','い',1200,525,250,'slam')]:word(s,name,c,x,y,245,f,mode,4,PAPER)
# 268 is an observed stronger bass attack: invert the full typographic state.
st(s,'#promise-bg',{'backgroundColor':PAPER},268)
st(s,['#promise-one','#promise-ja','#promise-na','#promise-i'],{'color':INK},268)
to(s,'#promise-one',{'scale':.68,'y':-45,'x':-165,'rotation':-9},268,8)
to(s,'#promise-ja',{'x':80,'y':-80,'rotation':-3},268,8)
to(s,'#promise-na',{'x':-20,'y':-80,'rotation':-3},268,8)
to(s,'#promise-i',{'x':-60,'y':-5,'rotation':-3},268,8)
mark(s,268,'黑白反转与字组重新排布','stronger bass onset')
star(s,'promise-star',1450,185,180,268,PINK)
# 04 / wait: circle window, calligraphic vertical words; foreground band passes behind the hair.
s=scene('night',296,412,INK,'八千代由月形窗口揭示；大字在人物身后，竖向小字接力，短暂留白')
block(s,'disc',670,-165,1300,1300,LILAC,extra='border-radius:50%;')
s['layers']['background'][-1]=s['layers']['background'][-1].replace('class="shape"','class="shape" data-layout-allow-overflow')
a=img(s,'yachiyo','yachiyo-wait-reference-v3.png',780,-10,1160)
ft(s,a,{'clipPath':'circle(0% at 55% 45%)'},{'clipPath':'circle(78% at 55% 45%)'},296,10)
word(s,'again','何度でも',100,65,255,303,'slam',-3,PAPER,layer='backtext',extra='paint-order:stroke fill;-webkit-text-stroke:9px #322438;',anticipate=5)
st(s,'#night-backtext-layer',{'zIndex':8},296)
st(s,'#night-backtext-layer',{'zIndex':2},321)
mark(s,321,'大字由前景切到人物身后，夜字接力')
word(s,'nightword','夜を',145,465,195,321,'wipe',-5,PAPER,'Mincho')
word(s,'cross','越えて',155,730,140,357,'rise',3,PAPER,'Mincho',anticipate=6)
# A restrained three-star progression follows an arc without connecting-line decoration.
star(s,'n1',620,650,50,339)
star(s,'n2',710,810,70,375)
star(s,'n3',540,910,38,391)
mark(s,391,'字组完整，保持八千代表情，下一镜前留出停顿','phrase articulation')
# 05 / reunion: one stationary drawing, two SVG windows opening into one frame.
s=scene('return',412,590,PAPER,'同一双人画稿经两个窗口依次揭示；遮罩展开成完整画面，人物位置保持连续')
block(s,'pinkzone',0,700,1920,380,'#e8c8d3',extra='clip-path:polygon(0 22%,100% 0,100% 100%,0 100%);')
node(s,'dots','', 'left:0;top:730px;width:1920px;height:350px;','background','dotfield')
# The clip rectangles use artwork-local coordinates. No image swap or crop remapping.
art_h=1470*Image.open(P/'assets/art/revision-v19/duo-black-top.png').height/Image.open(P/'assets/art/revision-v19/duo-black-top.png').width
defs='<svg width="0" height="0" aria-hidden="true"><defs><clipPath id="return-windows" clipPathUnits="userSpaceOnUse"><rect id="return-window-left" x="135" y="890" width="655" height="0"/><rect id="return-window-right" x="820" y="890" width="570" height="0"/></clipPath></defs></svg>'
a=img(s,'together','revision-v19/duo-black-top.png',225,10,1470,extra='clip-path:url(#return-windows);')
s['layers']['character'].insert(0,defs)
for side,x,w,f in [('left',360,655,428),('right',1045,570,445)]:
 sel=node(s,side,'',f'left:{x-8}px;top:112px;width:{w+16}px;height:796px;border:7px solid {INK};opacity:0;','foreground','shape')
 ft(s,sel,{'y':65,'scale':.94,'opacity':0},{'y':0,'scale':1,'opacity':1},412,10)
 ft(s,f'#return-window-{side}',{'attr':{'y':890,'height':0}},{'attr':{'y':110,'height':780}},f,7)
 to(s,f'#return-window-{side}',{'attr':{'x':0 if side=='left' else 735,'y':0,'width':735,'height':art_h}},475,12,'power2.inOut')
 to(s,sel,{'scale':1.08,'opacity':0},475,12,'power2.inOut')
 mark(s,f,'固定画稿窗口揭示'+('辉夜' if side=='left' else '彩叶'))
word(s,'mata','また',70,45,220,412,'slide',-8,PINK)
word(s,'meet','会える',1080,750,185,463,'rise',-5,PINK,extra='paint-order:stroke fill;-webkit-text-stroke:11px #f5efe7;',anticipate=6)
mark(s,481,'双窗口展开；同一画稿保持固定位置，不切换图片','accent onset')
st(s,['#return-mata','#return-meet'],{'opacity':0},481)
word(s,'backpromise','また会える',35,55,310,481,'wipe',0,PINK,layer='backtext',extra='letter-spacing:8px;')
# Retire the background promise before the foreground letter relay; no repeated full-width band.
to(s,'#return-backpromise',{'opacity':.16},529,6)
for i,c in enumerate('また会える。'):
 word(s,f'final-{i}',c,480+i*155,835,150,530+i,'rise' if i%2==0 else 'flip',-2,INK,'Mincho',extra=f'paint-order:stroke fill;-webkit-text-stroke:16px {PAPER};',anticipate=4,anchor='letter relay into frame 535 accent')
mark(s,535,'结尾逐字接力完成，完整短句落在强调点','accent onset','落定')
star(s,'close-a',160,720,110,535,PINK)
star(s,'close-b',1660,150,75,551)
mark(s,570,'结尾完整短句与双人构图保持，不再添加新信息','final accent / hold')

# Append the approved reference-matched sequence within this same project.
exec(compile((P/"source/revision-v24/append.py").read_text(),"revision-v19/append.py","exec"),globals())

exec(compile((P/"source/revision-v25/relay.py").read_text(),"revision-v19/relay.py","exec"),globals())

exec(compile((P/'source/revision-v22/polish.py').read_text(),'revision-v19/polish.py','exec'),globals())
exec(compile((P/'source/revision-v25/ending.py').read_text(),'revision-v24/ending.py','exec'),globals())
exec(compile((P/'source/revision-v26/backgrounds.py').read_text(),'revision-v26/backgrounds.py','exec'),globals())
exec(compile((P/'source/revision-v27/transitions.py').read_text(),'revision-v27/transitions.py','exec'),globals())
exec(compile((P/'source/revision-v31/pulses.py').read_text(),'revision-v31/pulses.py','exec'),globals())
# Build independently editable layers; each scene uses one scoped paused timeline.
for s in scenes:
 sid=s['id'];duration=(s['endFrame']-s['startFrame'])/30
 rootcss=f'#{sid}-root'+'{position:absolute;inset:0;width:100%;height:100%;overflow:hidden;}'
 layers=f'<div id="{sid}-bg" class="layer" style="background:{s["bg"]}"></div>'
 for n,(layer,items) in enumerate(s['layers'].items()):
  layers+=f'<div id="{sid}-{layer}-layer" class="clip layer" data-start="0" data-duration="{duration}" data-track-index="{n}" data-label="{layer_names[layer]}" style="z-index:{n+1}"><div class="layer">'+''.join(items)+'</div></div>'
 if s.get('stage'): layers=f'<div id="{sid}-stage" class="layer">{layers}</div>'
 script_open="(async()=>{await document.fonts.load('310px AppendMincho');" if s.get('awaitFonts') else "(()=>{"
 page=f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"></head><body><template><style>{cssbase}{appendcss if sid.startswith("append-") else ""}{rootcss}{''.join(s['css'])}</style><div id="{sid}-root" data-composition-id="{sid}" data-width="1920" data-height="1080" data-duration="{duration}">{layers}</div><script>{script_open}const tl=gsap.timeline({{paused:true}});{''.join(s['js'])}window.__timelines=window.__timelines||{{}};window.__timelines['{sid}']=tl;}})();</script></template></body></html>'''
 (P/'compositions'/s['filename']).write_text(page)
# Each shot owns a stacking context. Otherwise an outgoing z-index:4 canvas
# paints above an incoming opacity<1 stage until its fade ends (a false hard cut).
slots=''.join(f'<div id="slot-{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["filename"]}" data-start="{s["startFrame"]/30}" data-duration="{(s["endFrame"]-s["startFrame"])/30}" data-width="1920" data-height="1080" data-track-index="1" data-label="{s["description"]}" style="z-index:{i+1};isolation:isolate"></div>' for i,s in enumerate(scenes))
# Root-level coverage spans cuts, rather than fading to blank before a new scene.
trans=[];tjs=[]
for n,(frame,color,mode) in enumerate([(107,PAPER,'diagonal'),(196,INK,'band'),(296,INK,'circle'),(412,PAPER,'split'),(590,'#201d35','organic')]):
 id=f'cover{n}';base=f'position:absolute;inset:-100px;width:2120px;height:1280px;background:{color};'
 if mode=='organic':
  # Directional-wipe primitive, adapted with a curved leading edge.
  trans.append(f'<svg id="{id}" data-layout-allow-overflow width="2400" height="1200" viewBox="0 0 2400 1200" style="position:absolute;left:-50px;top:-60px;opacity:0;"><path fill="{color}" d="M280 0H2400V1200H200C310 1080 105 980 240 840S90 610 250 470S130 220 280 0Z"/></svg>')
  tjs.append(f"tl.fromTo('#{id}',{{x:2200,opacity:1}},{{x:-300,opacity:1,duration:0.2,ease:'power3.in',immediateRender:false}},{(frame-6)/30});tl.to('#{id}',{{x:-2600,duration:0.2333333333,ease:'power3.out'}},{frame/30});")
 elif mode=='diagonal':
  trans.append(f'<div id="{id}" style="{base}clip-path:polygon(9% 0,100% 0,91% 100%,0 100%);transform-origin:center"></div>')
  tjs.append(f"tl.fromTo('#{id}',{{x:-2400}},{{x:0,duration:{6/30},ease:'power3.in'}},{(frame-6)/30});tl.to('#{id}',{{x:2400,duration:{7/30},ease:'power3.out'}},{frame/30});")
 elif mode=='band':
  trans.append(f'<div id="{id}" style="{base}"></div>');tjs.append(f"tl.fromTo('#{id}',{{scaleY:0}},{{scaleY:1,duration:{5/30},ease:'power3.in'}},{(frame-5)/30});tl.set('#{id}',{{opacity:0}},{frame/30});")
 elif mode=='circle':
  trans.append(f'<div id="{id}" style="{base}clip-path:circle(0% at 68% 50%);"></div>');tjs.append(f"tl.fromTo('#{id}',{{clipPath:'circle(0% at 68% 50%)'}},{{clipPath:'circle(120% at 68% 50%)',duration:{7/30},ease:'power3.in'}},{(frame-7)/30});tl.set('#{id}',{{opacity:0}},{frame/30});")
 else:
  for side,sign in [('l',-1),('r',1)]:
   trans.append(f'<div id="{id}-{side}" data-layout-allow-overflow style="position:absolute;top:-100px;left:{0 if side=="l" else 960}px;width:960px;height:1280px;background:{color};"></div>');tjs.append(f"tl.fromTo('#{id}-{side}',{{x:{sign*1100}}},{{x:0,duration:{5/30},ease:'power3.in'}},{(frame-5)/30});tl.to('#{id}-{side}',{{x:{sign*1100},duration:{7/30},ease:'power3.out'}},{frame/30});")
# Music source is split without skipping samples; PAUSE_LENGTH controls the editorial gap.
resume=PAUSE_AT+PAUSE_LENGTH
rest=D-resume
au_before=J({'version':1,'lanes':[{'target':'volume','points':[{'t':0,'v':1},{'t':PAUSE_AT-.035,'v':1},{'t':PAUSE_AT,'v':0}]}]})
au_after=J({'version':1,'lanes':[{'target':'volume','points':[{'t':0,'v':0},{'t':.025,'v':1},{'t':rest-globals().get('ENDING_FADE',.1),'v':1},{'t':rest,'v':0}]}]})
audio_tags=f'''<audio data-label="音乐①｜星降る海・烟花前" id="song-before" src="assets/audio/demo-silence.wav" data-start="0" data-duration="{PAUSE_AT}" data-media-start="{START}" data-volume="1" data-track-index="0" data-automation='{au_before}'></audio><audio data-label="音乐②｜星降る海・烟花后" id="song-after" src="assets/audio/demo-silence.wav" data-start="{resume}" data-duration="{rest}" data-media-start="{START+PAUSE_AT}" data-volume="1" data-track-index="0" data-automation='{au_after}'></audio>'''
(P/'index.html').write_text(f'''<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>星降る海 — また会える / V07 续段</title><script src="assets/vendor/gsap.min.js"></script><style>html,body{{margin:0;overflow:hidden;background:{PAPER}}}#main,.clip{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}}{cssbase}</style></head><body><main id="main" data-composition-id="main" data-width="1920" data-height="1080" data-duration="{D}" data-fps="30">{slots}<div id="covers" class="clip" data-start="0" data-duration="{D}" data-track-index="4" style="z-index:100;pointer-events:none">{''.join(trans)}</div>{audio_tags}</main><script>const tl=gsap.timeline({{paused:true}});{''.join(tjs)}window.__timelines=window.__timelines||{{}};window.__timelines.main=tl;</script></body></html>''')
(P/'meta.json').write_text(J({'id':P.name,'name':'星降る海 · 画稿与动画源码（无原曲）'}))
(P/'source/cues.json').write_text(json.dumps({'sourceStart':START,'duration':D,'fps':30,'musicPause':{'originalVocalEntry':20.75,'oldTimelineCut':PAUSE_AT,'newResumeTime':resume,'seconds':PAUSE_LENGTH,'sourceResumeTime':START+PAUSE_AT},'auditoryReview':'pending','scenes':[{k:v for k,v in s.items() if k not in ['layers','css','js','noteFlights']} for s in scenes],'events':sorted(events,key=lambda e:e['frame'])},ensure_ascii=False,indent=2))
with (P/'boards/music-cues.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['frame','time','sourceTime','scene','event','anchor','note'],lineterminator='\n');w.writeheader();w.writerows(sorted(events,key=lambda e:e['frame']))
print(f'Built {len(scenes)} scenes, {len(events)} events, {round(D*30)} frames, music {START}–{START+D-PAUSE_LENGTH:.3f}, pause {PAUSE_AT}–{resume}')

main=(P/'index.html').read_text()
oldcover=f'<div id="covers" class="clip" data-start="0" data-duration="{D}" data-track-index="4" style="z-index:100;pointer-events:none">'+''.join(trans)+'</div>'
newcover=f'<div id="slot-transitions" class="clip" data-start="0" data-duration="{D}" data-track-index="4" data-label="16｜全片转场" data-composition-id="transitions" data-composition-src="compositions/16-全片转场.html" data-width="1920" data-height="1080" style="z-index:100;pointer-events:none"></div>'
main=main.replace(oldcover,newcover).replace(''.join(tjs),'')
(P/'index.html').write_text(main)
(P/'compositions/16-全片转场.html').write_text(f'''<!doctype html><html><body><template><style>#transitions-root{{position:absolute;inset:0;width:100%;height:100%;overflow:hidden}}</style><div id="transitions-root" data-composition-id="transitions" data-duration="{D}" data-width="1920" data-height="1080">{''.join(trans)}</div><script>(()=>{{const tl=gsap.timeline({{paused:true}});{''.join(tjs)}window.__timelines=window.__timelines||{{}};window.__timelines.transitions=tl;}})();</script></template></body></html>''')
exec(compile((P/'source/revision-v22/subtitles.py').read_text(),'revision-v21/subtitles.py','exec'),globals())
generated=[subtitle_file,P/'index.html',*[P/'compositions'/s['filename'] for s in scenes],P/'compositions/16-全片转场.html']
# Remove only obsolete generated filenames after writing renamed replacements.
for old in json.loads(state.read_text()) if state.exists() else []:
 if old.startswith('compositions/') and (P/old) not in generated and (P/old).exists():(P/old).unlink()
state.write_text(json.dumps({str(f.relative_to(P)):digest(f) for f in generated},indent=2)+'\n')
