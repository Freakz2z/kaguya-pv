# Modified for this archive; adapted HyperFrames registry techniques. See NOTICE.md and LICENSES/.
# Executed by source/build.py after the original five scenes. Frames are absolute.
# The pause ends when the five fireworks fall; the 0.25s pickup remains on the resumed clip.
APPEND_START=590
D=1028/30
PAUSE_AT=20.5; PAUSE_LENGTH=2.6
def af(f): return f+PAUSE_LENGTH*30 if f>=615 else f
def aft(s,sel,a,b,frame,dur=6,ease="power3.out"): return ft(s,sel,a,b,af(frame),dur,ease)
def ato(s,sel,b,frame,dur=6,ease="power3.out"): return to(s,sel,b,af(frame),dur,ease)
def ast(s,sel,b,frame): return st(s,sel,b,af(frame))
def amark(s,f,what,anchor="drum onset",note=""): return mark(s,af(f),what,anchor,note)
def ascene(sid,a,b,bg,description): return scene(sid,af(a),af(b),bg,description)
APAPER=PAPER; APINK=PINK; APURPLE='#74449a'
appendcopy='ねえこの声が君に届くなら声を、もとへ。聞こえたちゃんまた会'
appendcss="@font-face{font-family:AppendHeavy;src:local('Arial')}@font-face{font-family:AppendMincho;src:local('Arial')}"

exec(compile((P/'source/revision-v20/backgrounds.py').read_text(),'style-v11/backgrounds.py','exec'),globals())

def ew(s,name,text,x,y,size,frame,mode='rise',angle=-4,color=APINK,layer='text',anticipate=0,font='AppendHeavy'):
 # Append-only restrained entrances: keep variety without throwing the eye across the frame.
 sel=node(s,name,html.escape(text),f'left:{x}px;top:{y}px;font-size:{size}px;font-family:{font};color:{color};paint-order:stroke fill;-webkit-text-stroke:10px {APAPER};text-shadow:3px 5px 0 #e6c9d8;',layer,'type','data-layout-allow-overlap data-layout-allow-occlusion')
 initial={'opacity':0,'rotation':angle};end={'opacity':1,'rotation':angle}
 if mode=='wipe': initial.update(clipPath='inset(0 100% 0 0)');end.update(clipPath='inset(0 0% 0 0)')
 elif mode=='rise': initial.update(y=44);end.update(y=0)
 elif mode=='slam': initial.update(scale=1.14);end.update(scale=1)
 elif mode=='flip': initial.update(y=20,rotation=angle-4);end.update(y=0)
 elif mode=='drop': initial.update(y=-24);end.update(y=0)
 dur=8 if mode!='wipe' else 10
 aft(s,sel,initial,end,frame,dur,'power2.out')
 amark(s,frame,'文字 '+text,'phrase entrance',f'{dur} 帧入场，随后保持')
 return sel

def letter_run(s,name,text,x,y,size,frame,color=APINK,angle=0):
 # One designed word group, with different internal entry poses; not a beat per glyph.
 sel=node(s,name,''.join(f'<span class="glyph glyph-{i}">{html.escape(c)}</span>' for i,c in enumerate(text)),f'left:{x}px;top:{y}px;font-size:{size}px;line-height:1.16;font-family:AppendHeavy;color:{color};white-space:nowrap;paint-order:stroke fill;-webkit-text-stroke:7px {APAPER};','text','shape','data-layout-allow-overlap data-layout-allow-occlusion')
 s['css'].append(sel+' .glyph{display:inline-block;opacity:0;transform-origin:50% 75%;}')
 for i,c in enumerate(text):
  a={'opacity':0,'y':26 if i%2==0 else -18,'scaleX':.72 if i%2==0 else 1.16,'rotation':angle+(-3 if i%2 else 3)}
  aft(s,sel+' .glyph-'+str(i),a,{'opacity':1,'y':0,'scaleX':1,'rotation':angle},frame+i*3,6,'power4.out')
 amark(s,frame,'字组内部错开进入 '+text,'group choreography','每字相隔 3 帧，不逐字绑定鼓点')
 return sel

def dissolve_in(s,frames=12,delay=0):
 # Fade a single untimed inner stage, including its background. Outgoing scene stays
 # alive underneath until this fade completes; never fade both scenes into blank.
 s['stage']=True
 s['css'].append('#'+s['id']+'-stage{opacity:0;}')
 ft(s,'#'+s['id']+'-stage',{'opacity':0},{'opacity':1},s['startFrame']+delay,frames,'sine.inOut')

s=scene('append-fireworks',590,732,APAPER,'烟花升空・余辉中呼唤')
s['awaitFonts']=True
fire=node(s,'fireworks','<canvas id="append-fireworks-canvas" width="1920" height="1080" style="width:100%;height:100%" aria-hidden="true"></canvas>','inset:0;width:100%;height:100%;','foreground','shape','data-layout-ignore')
s['js'].append((P/'source/revision-v22/fireworks.js').read_text().replace('append-voice-fireworks-canvas','append-fireworks-canvas'))
mark(s,590,'多枚烟花先后升空','instrumental opening')
mark(s,615,'音乐截断点20.500秒','user supplied music anchor')
mark(s,650.6,'主烟花爆开；五枚烟花错开','adapted user cinematic shell')
mark(s,693,'余辉中「ねえ」落定；音乐恢复','falling embers; music resumes at 23.100')
s=scene('append-voice',716,868,APAPER,'彩叶歌唱・这个声音传向你')
voicebg=print_field(s,'voice')
dissolve_in(s,9,7)
hero=img(s,'iroha','style-v10/iroha-virtual-print.png',-250,60,960)
# Constant-size continuous translation starts under the dissolve and lasts until
# the outgoing composition is fully covered. Never ease to a stop or reset x.
ft(s,hero,{'x':-60,'y':8},{'x':80,'y':-8},716,152,'none')
ew(s,'this','この',790,135,255,650,'wipe',-7,APINK)
letter_run(s,'voiceword','声が',890,460,380,666,APINK,5)
amark(s,644,'固定尺寸连续平移，入场和转场期间保持速度','continuous translation')
# Typography cross-reveals in place; no full-screen middle transition.
ato(s,['#append-voice-this','#append-voice-voiceword'],{'opacity':0},718,9,'sine.inOut')
ew(s,'toyou','君に',850,125,330,725,'wipe',-5,APINK)
ew(s,'reach','届くなら',880,620,210,744,'rise',3,APURPLE)
amark(s,729,'字组直接接力，人物沿原轨迹继续平移','covered typography cut')
amark(s,759,'字组落定，人物继续平移直到下一场覆盖完成','continuous translation')

s=ascene('append-answer',778,849,APAPER,'续段：完整纸面从右侧揭示辉夜；字组错开变形进入')
print_field(s,'answer')
s['stage']=True
s['css'].append('#append-answer-stage{clip-path:inset(0 0 0 100%);}')
aft(s,'#append-answer-stage',{'clipPath':'inset(0 0 0 100%)'},{'clipPath':'inset(0 0 0 0%)'},778,12,'power2.inOut')
answerhero=img(s,'kaguya','style-v10/kaguya-response-print.png',970,35,950,extra='transform-origin:50% 25%;')
ft(s,answerhero,{'x':-52,'y':10},{'x':34,'y':-8},856,71,'none')
letter_run(s,'heard','聞こえた',65,190,235,786,APINK,-6)
ew(s,'truly','ちゃんと。',135,625,185,807,'wipe',3,APURPLE,font='AppendMincho')
amark(s,778,'完整纸面从右向左揭示辉夜，旧镜头保留到 790 帧','12-frame directional reveal')
amark(s,822,'回应短句落定；画稿持续平移至转场结束','continuous translation')
ato(s,['#append-answer-heard','#append-answer-truly'],{'opacity':0},832,9,'sine.inOut')

s=ascene('append-together',837,950,APAPER,'续段：12 帧叠化至虚拟服双人踮脚碰指画稿，短句落定后完整停留')
print_field(s,'together');dissolve_in(s)
duohero=img(s,'virtual-duo-tiptoe','ending-v24/virtual-duo-tiptoe-v4.png',-100,100,1440)
# Touching fingers form a stable emotional hold, revealed by the existing stage and typography.
ew(s,'again','また、',1300,120,180,845,'drop',7,APURPLE,font='AppendMincho')
# The kanji is a foreground graphic mass. The smaller ending sits on a paper tab.
ew(s,'met','会',1130,335,410,847,'slam',-7,APINK)
label=block(s,'ending-tab',1435,775,445,210,'#e8c8d3','foreground',extra=f'opacity:0;border:4px solid {INK};transform-origin:0% 50%;')
aft(s,label,{'opacity':1,'scaleX':.05,'rotation':3},{'opacity':1,'scaleX':1,'rotation':3},852,10,'power2.out')
ew(s,'ending','えた。',1460,790,145,858,'wipe',3,INK)
amark(s,873,'大小字与纸签落定，图文允许前后交叠','visual lockup')
amark(s,837,'虚拟服双人踮脚碰指画稿开始叠化，旧镜头保留到 849 帧','12-frame dissolve')
amark(s,849,'全身双人碰指镜头保持静止，字组接力展开','stable relationship frame')
amark(s,873,'图文完整后保持77帧，不再持续推近','final hold')
