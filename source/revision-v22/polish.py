# Deterministic particles follow the registry particle-image-reveal principle:
# fixed per-particle table at author time; explicit visible GSAP tracks; no clock/random.
SCENE_NAMES={
'distance':'01｜远く・离别的约定','voice':'02｜君の声・彩叶的声音','promise':'03｜ひとりじゃない・文字接力',
'night':'04｜夜を越えて・八千代等待','return':'05｜また会える・双人回忆',
'append-fireworks':'06A｜烟花升空・余辉呼唤','append-voice':'06B｜彩叶歌唱・この声が','append-answer':'07｜聞こえた・辉夜回应','append-together':'08｜また会えた・再次相遇',
'append-relay-distance':'09｜声音接力①・彩叶低声唱歌','append-relay-panels':'10｜声音接力②・文字化为音符',
'append-relay-journey':'11–14｜声音远行・地球到月球一镜到底','append-relay-waiting':'11｜声音远行①・离开地球','append-relay-spirit':'12｜声音远行②・精神世界',
'append-relay-flat':'13｜声音远行③・二维画境','append-relay-moon':'14｜声音远行④・月球收信',
'append-relay-reply':'15｜声音回应・辉夜听见了'}
for s in scenes:
 s['description']=SCENE_NAMES[s['id']]
 s['filename']=SCENE_NAMES[s['id']].replace('｜','-')+'.html'
 # Quiet editorial dust at the edges; omit the existing firework and pure-text shots.
 if s['id'] in ('append-fireworks','append-voice','promise','append-relay-panels','append-relay-journey'):continue
 travel=s['id'] in ('append-relay-waiting','append-relay-spirit','append-relay-flat','append-relay-moon')
 count=22 if travel else 7
 duration=s['endFrame']-s['startFrame']
 color=PAPER if travel or s['id']=='night' else '#ac7791'
 for i in range(count):
  x=45+(i*293)%1810;y=160+(i*167)%760
  if not travel:x=45+(i%2)*1750+(i%3)*12
  radius=3+(i%4)*2
  p=node(s,'dust-'+str(i),'',f'left:{x}px;top:{y}px;width:{radius}px;height:{radius}px;border-radius:50%;background:{color};opacity:0;','foreground','shape','data-layout-ignore')
  start=s['startFrame']+(i*7)%max(1,int(duration-25));life=min(35,duration-(start-s['startFrame']))
  ft(s,p,{'opacity':0,'y':15},{'opacity':.55 if travel else .3,'y':0},start,life*.3,'sine.out')
  to(s,p,{'opacity':0,'y':-55 if travel else -25,'x':18 if i%2 else -18},start+life*.3,life*.7,'sine.in')
 if s['id']=='append-relay-moon':
  for i in range(16):
   theta=i*math.pi*2/16;x=1390+math.cos(theta)*30;y=520+math.sin(theta)*30
   a=node(s,'receive-spark-'+str(i),'',f'left:{x}px;top:{y}px;width:7px;height:7px;background:{GOLD};opacity:0;','foreground','shape','data-layout-ignore')
   ft(s,a,{'opacity':0,'scale':.2},{'opacity':1,'scale':1.5},1350+i%3,4)
   to(s,a,{'x':math.cos(theta)*145,'y':math.sin(theta)*145,'opacity':0,'scale':.15},1354+i%3,22,'power2.out')

exec(compile((P/'source/revision-v22/pulse.py').read_text(),'revision-v20/trails-and-type.py','exec'),globals())

exec(compile((P/'source/revision-v22/motifs.py').read_text(),'revision-v22/motifs.py','exec'),globals())
