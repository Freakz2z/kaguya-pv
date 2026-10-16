# Modified for this archive; adapted HyperFrames registry techniques. See NOTICE.md and LICENSES/.
# Final narrative sequence, appended without changing accepted scenes01–14.
D=1866/30
ENDING_FADE=.65
ending_copy='き（）・君の声ここに届いてるよまた会える。星降る海月見ヤチヨ早見沙織作詞作曲編曲手書二次創作BGMVocalAqu3ra(cv.)｜： / ！超かぐや姫'
endcss="@font-face{font-family:EndHeavy;src:local('Arial')}@font-face{font-family:EndMincho;src:local('Arial')}"
def endscene(sid,a,b,bg,title):
 s=scene('append-finale-'+sid,a,b,bg,title);s['css'].append(endcss);s['filename']=title.replace('｜','-')+'.html';return s

def endtype(s,name,txt,x,y,size,color,frame,align='left',width=1400,font='EndMincho'):
 t=node(s,name,html.escape(txt),f'left:{x}px;top:{y}px;width:{width}px;font:{size}px/1.2 {font};color:{color};text-align:{align};white-space:nowrap;opacity:0;','text','type','data-layout-allow-overlap')
 ft(s,t,{'opacity':0,'y':12},{'opacity':1,'y':0},frame,10,'power3.out');return t

for prior in scenes:
 if prior['id']=='append-together':
  prior['description']='08｜また会えた・踮脚碰指'
  prior['filename']='08-また会えた・踮脚碰指.html'

# Fourteen pose drawings: two extra folding bridges join the twelve-key sheet.
s=endscene('answer',1487,1647,PAPER,'18｜指先の約束・碰指与回应')
node(s,'warm-ground','','inset:0;background:#fff3da;','background')
for i,(x,y,r,c) in enumerate([(-190,240,390,'#dfb5bf'),(1630,600,380,'#d1c1d9')]):
 node(s,'edge-disc-'+str(i),'',f'left:{x}px;top:{y}px;width:{r}px;height:{r}px;border-radius:50%;background:{c};','background','shape','data-layout-ignore')
papergrain(s,INK,.035)
key_frames=[1487,1496,1502,1508,1514,1524,1530,1536,1542,1548,1554,1560,1568,1578,1589]
keys=[('hand-sequence-12.png',4,3,i) for i in range(6)]+[('hand-bridges.png',2,2,i) for i in range(2)]+[('hand-sequence-12.png',4,3,i) for i in range(6,12)]
hand_cels=[]
for i,(file,cols,rows,cell) in enumerate(keys):
 start,stop=key_frames[i:i+2]
 h=node(s,'hand-'+str(i),'',f'left:0;top:0;width:1010px;height:1010px;opacity:0;background-image:url(assets/art/ending-v28/{file});background-size:{1010*cols}px {1010*rows}px;background-position:{-1010*(cell%cols)}px {-1010*(cell//cols)}px;','character','shape','data-layout-allow-overlap data-layout-allow-occlusion')
 # Registered opaque cels replace each other at one exact frame boundary.
 # No alpha blend: it creates translucent duplicate fingers even at full coverage.
 hand_cels.append(s['layers']['character'].pop())
 st(s,h,{'opacity':1},start)
 st(s,h,{'opacity':0},stop if i<13 else 1598)
# One stationary feather applied after cel compositing, never fourteen masks.
node(s,'hand-cel-window',''.join(hand_cels),'left:455px;top:70px;width:1010px;height:1010px;overflow:hidden;isolation:isolate;mask-image:linear-gradient(to right,transparent,#000 5%,#000 95%,transparent);','character','shape','data-layout-allow-overlap data-layout-allow-occlusion')
# Small graphic cues flank the hands, never cover the crossing anatomy.
a=endtype(s,'voice-key','君の声',110,400,105,INK,1488,width=350)
outlined(s,a,'#fff3da',3)
b=endtype(s,'here-key','ここに',1465,575,105,PINK,1520,width=350)
for x in [a,b]:to(s,x,{'opacity':0},1583,5)
# Contact glint opens into a paper-cut flower, then the answer lands on top.
glint=node(s,'contact-glint','<svg viewBox="0 0 100 100"><path d="M50 0L59 40 100 50 59 60 50 100 41 60 0 50 41 40Z" fill="#fff9d6"/></svg>','left:915px;top:510px;width:90px;height:90px;opacity:0;','foreground','shape','data-layout-ignore')
ft(s,glint,{'opacity':0,'scale':.15,'rotation':-12},{'opacity':1,'scale':1.15,'rotation':0},1583,5)
to(s,glint,{'opacity':0,'scale':2.2},1588,5)
petals=[]
for i in range(12):
 angle=math.pi*2*i/12
 r=150 if i%2 else 500
 petals.append(f'{960+math.cos(angle)*r:.1f},{560+math.sin(angle)*r:.1f}')
burst=plate(s,'answer-flower','<path d="M0 0H1920V1080H0Z" fill="#e5adbb"/><path d="M-200 890Q1000 130 2100 720V1080H-200Z" fill="#d8c6dd"/><path d="M144 451L167 408 230 374 222 348 348 291 540 245 571 254 733 223 1012 231 1034 217 1273 245 1320 240 1508 306 1559 301 1679 393 1734 474 1727 548 1761 572 1713 709 1641 748 1654 769 1482 861 1337 892 1293 916 1088 926 1011 949 758 938 711 948 480 894 429 899 254 799 268 772 170 696 151 594 126 566Z" fill="#fff3da"/><polygon points="'+' '.join(petals)+'" fill="#edd69c" opacity=".5"/>','foreground','inset:0;clip-path:circle(0% at 50% 52%);')
ft(s,burst,{'clipPath':'circle(0% at 50% 52%)'},{'clipPath':'circle(85% at 50% 52%)'},1588,9,'power3.out')
# A larger first kanji and offset following glyphs make the impact asymmetric.
for i,(ch,x,y,size) in enumerate([('届',210,240,430),('い',665,410,230),('て',895,385,230),('る',1125,410,230),('よ',1355,385,230)]):
 t=node(s,'answer-glyph-'+str(i),ch,f'left:{x}px;top:{y}px;font:{size}px/1.15 EndHeavy;color:{INK};opacity:0;transform-origin:50% 65%;text-shadow:7px 9px 0 #d9a0af;','text','type','data-layout-allow-overlap data-layout-allow-occlusion')
 outlined(s,t,'#fff9e8',7)
 f=1589+i*2
 ft(s,t,{'opacity':0,'y':-95 if i%2==0 else 95,'scale':1.46,'rotation':-10 if i%2==0 else 9},{'opacity':1,'y':0,'scale':.97,'rotation':-3 if i==0 else 0},f,5,'power4.out')
 to(s,t,{'scale':1},f+5,4,'sine.out')
# Hand-printed particles radiate away from the word, with unequal paths/holds.
for i in range(24):
 ang=i*2.399963;radius=510+(i%4)*70
 x=960+math.cos(ang)*radius;y=540+math.sin(ang)*radius*.62
 color=[PINK,GOLD,'#7e637e','#fef6d9'][i%4]
 dot=node(s,'petal-'+str(i),f'<svg viewBox="0 0 32 52" width="100%" height="100%"><path d="M16 2Q37 20 20 49Q-8 30 16 2Z" fill="{color}" stroke="{INK}" stroke-width="1.5"/></svg>',f'left:{x}px;top:{y}px;width:{12+i%5*4}px;height:{20+i%5*5}px;opacity:0;','foreground','shape','data-layout-ignore')
 f=1592+i%6
 ft(s,dot,{'opacity':0,'x':-math.cos(ang)*130,'y':-math.sin(ang)*80,'rotation':i*31},{'opacity':.85,'x':0,'y':0,'rotation':i*31+40},f,9,'power3.out')
 to(s,dot,{'x':math.cos(ang)*30,'y':math.sin(ang)*20+35,'rotation':i*31+95,'opacity':.25},f+9,29,'sine.inOut')
for i,(x,y,z) in enumerate([(145,760,90),(1620,240,110),(1495,765,62),(700,200,56)]):star(s,'answer-star-'+str(i),x,y,z,1594+i*3,GOLD)
# Three angled paper shutters carry the final word directly into the trio reveal.
for i,c in enumerate(['#d8c8df','#c6ddd8','#e9b9bd']):
 a=node(s,'exit-shutter-'+str(i),'',f'left:{i*640}px;top:0;width:640px;height:1080px;background:{c};transform:translateY(1080px);','transition','shape','data-layout-ignore')
 ft(s,a,{'y':1080},{'y':0},1635+i*2,8,'power3.inOut')
mark(s,1487,'两指相点，新绘十四张手势关键帧','gesture key')
mark(s,1502,'指尖释放与手腕内转中间姿态','gesture bridge')
mark(s,1514,'交叉停留，明确手指前后遮挡','gesture key')
mark(s,1530,'松开交叉，折指中间姿态','gesture bridge')
mark(s,1560,'小狐狸接近，留出短暂停顿','gesture bridge')
mark(s,1568,'小狐狸相碰，停留后文字接力','gesture key')
mark(s,1589,'届字与纸花落定，余字错时回弹','typographic impact')

# Concert trio: three local reveals uncover one coherent fixed-size illustration.
s=endscene('reunion',1647,1734,'#f3e4cf','19｜また会える・三人舞台')
node(s,'stage-paper','','inset:0;background:radial-gradient(ellipse at 50% 40%,#fff6df 20%,#f0d8d0 100%);','background')
for i,(x,c) in enumerate([(0,'#d8c8df'),(640,'#c6ddd8'),(1280,'#e9b9bd')]):
 field=node(s,'field-'+str(i),'',f'left:{x}px;top:0;width:640px;height:1080px;background:{c};opacity:.5;','background','shape','data-layout-ignore')
 to(s,field,{'opacity':.15},1656+i*3,25,'sine.out')
for i,(x,y,r) in enumerate([(140,190,170),(1530,200,230),(820,620,360)]):
 node(s,'soft-light-'+str(i),'',f'left:{x}px;top:{y}px;width:{r}px;height:{r}px;border-radius:50%;background:#fff6d2;opacity:.55;','background','shape','data-layout-ignore')
papergrain(s,INK,.035)
# A single image is revealed by three nonoverlapping SVG clip rectangles.
windows=[(0,790),(790,1110),(1110,1920)]
rects=''.join(f'<rect id="concert-reveal-{i}" x="{a}" y="{1080 if i!=1 else 0}" width="{b-a}" height="0"/>' for i,(a,b) in enumerate(windows))
node(s,'reveal-defs','<svg width="0" height="0"><defs><clipPath id="concert-reveal-mask" clipPathUnits="userSpaceOnUse">'+rects+'</clipPath></defs></svg>','inset:0;','background','shape','data-layout-ignore')
art=node(s,'concert-art','<img src="assets/art/ending-v24/concert-trio.png" style="position:absolute;left:240px;top:120px;width:1440px;height:960px"/>','inset:0;clip-path:url(#concert-reveal-mask);','character','shape','data-layout-allow-overlap data-layout-allow-occlusion')
for i,(a,b) in enumerate(windows):
 ft(s,'#concert-reveal-'+str(i),{'attr':{'y':1080 if i!=1 else 0,'height':0}},{'attr':{'y':0,'height':1080}},1647+i*4,11,'power4.out')
 cover=node(s,'entry-paper-'+str(i),'',f'left:{i*640}px;top:0;width:640px;height:1080px;background:{["#d8c8df","#c6ddd8","#e9b9bd"][i]};','foreground','shape','data-layout-ignore')
 to(s,cover,{'y':-1080 if i!=1 else 1080},1647+i*4,11,'power4.inOut')
# Perimeter foil and print stars remain away from the three faces.
for i,(x,y,z) in enumerate([(120,330,95),(1700,230,105),(1660,840,70),(90,870,48)]):
 a=star(s,'concert-star-'+str(i),x,y,z,1658+i*4,[GOLD,PINK,GOLD,'#9db9b4'][i])
for i in range(18):
 x=75+(i*139)%1790;y=150+(i*97)%820
 # Keep the facial region clean; the paper specks live at the edges/lower frame.
 if 350<x<1520 and y<650:continue
 a=node(s,'foil-'+str(i),'',f'left:{x}px;top:{y}px;width:{7+i%4}px;height:{16+i%5*3}px;border-radius:60% 0;background:{[GOLD,"#a06781","#fff9dc"][i%3]};opacity:0;','foreground','shape','data-layout-ignore')
 f=1658+i%6*3
 ft(s,a,{'opacity':0,'y':-35,'rotation':-20},{'opacity':.7,'y':0,'rotation':30},f,14,'sine.out')
 to(s,a,{'opacity':0,'y':55,'rotation':100,'x':18 if i%2 else -18},f+14,32,'sine.inOut')
t=endtype(s,'promise','また、会える。',250,900,114,INK,1678,'center',1420)
outlined(s,t,PAPER,9)
s['layers']['text']=[m.replace('id="append-finale-reunion-promise"','id="append-finale-reunion-promise" data-layout-allow-occlusion') for m in s['layers']['text']]
wash=node(s,'title-wash','','inset:0;background:#f5e6a7;opacity:0;','transition','shape','data-layout-ignore')
ft(s,wash,{'opacity':0},{'opacity':1},1720,14,'sine.inOut')
mark(s,1647,'三色纸幕与分区遮罩错时打开，三人图缓慢放大','concert entrance')
mark(s,1666,'三人演出服画面完整落定，随后停留','key visual hold')
mark(s,1720,'暖纸色覆盖接入原有片名与音乐署名','ending wash')

# Reference clip: warm sketch title -> same-centred clean logo on white.
s=endscene('title',1734,1866,'#f5e6a7','20｜超かぐや姫！・片名与音乐署名')
node(s,'gold-paper','','inset:0;background:radial-gradient(ellipse at 68% 25%,#fffed7 0%,#f4e6a8 55%,#d8bb75 100%);','background')
white=node(s,'white-paper','','inset:0;background:#fff;opacity:0;','background')
ft(s,white,{'opacity':0},{'opacity':1},1770,30,'sine.inOut')
# Independent illustrations, no frame from the reference recording is reused.
sketch=node(s,'sketch-logo','<img src="assets/art/ending-v23/sketch-logo.png" style="width:100%;height:100%;object-fit:contain"/>','left:210px;top:290px;width:1500px;height:430px;opacity:0;','character')
ft(s,sketch,{'opacity':0},{'opacity':1},1734,9,'sine.out')
to(s,sketch,{'opacity':0},1770,28,'sine.inOut')
logo=img(s,'clean-logo','ending-v23/official-logo.png',285,350,1350,'character',extra='opacity:0;')
ft(s,logo,{'opacity':0},{'opacity':1},1774,28,'sine.inOut')
# Credits are intentionally still, legible and independent from narrative lyrics.
endtype(s,'bgm','BGM｜星降る海',460,745,50,INK,1793,'center',1000)
endtype(s,'vocal','Vocal｜月見ヤチヨ（cv.早見沙織）',360,820,34,INK,1799,'center',1200)
endtype(s,'music','作詞・作曲・編曲｜Aqu3ra',460,878,32,INK,1804,'center',1000)
endtype(s,'fancredit','手書き二次創作',610,975,25,'#706978',1808,'center',700)
mark(s,1734,'暖黄手绘标题停留，参考用户提供的7.338秒录屏','reference title staging')
mark(s,1802,'白底清晰片名与BGM署名落定，保持到结束','credits hold')
