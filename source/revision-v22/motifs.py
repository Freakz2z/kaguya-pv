# Sparse iridescent soap bubbles, with a clear centre and uneven bright rim.
def soap(s,name,x,y,r,f,life,depth):
 uid=s['id']+'-'+name
 svg=f'''<svg width="100%" height="100%" viewBox="0 0 200 200"><defs><radialGradient id="{uid}-film" cx="35%" cy="27%" r="72%"><stop offset="0" stop-color="#fffdf3" stop-opacity=".04"/><stop offset=".70" stop-color="#d9d9ee" stop-opacity=".02"/><stop offset=".92" stop-color="#9acbd3" stop-opacity=".16"/><stop offset="1" stop-color="#d8a2c8" stop-opacity=".20"/></radialGradient><linearGradient id="{uid}-rim" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fff7e7"/><stop offset=".24" stop-color="#9ab5cd"/><stop offset=".49" stop-color="#dda7c5" stop-opacity=".25"/><stop offset=".74" stop-color="#bd92b7"/><stop offset="1" stop-color="#f5d999"/></linearGradient></defs><circle cx="100" cy="100" r="91" fill="url(#{uid}-film)" stroke="url(#{uid}-rim)" stroke-width="3"/><path d="M30 82C35 52 51 35 76 28" fill="none" stroke="#fffaf0" stroke-width="6" stroke-linecap="round" opacity=".85"/><path d="M127 173Q162 160 173 124" fill="none" stroke="#e9b5d7" stroke-width="3.2" stroke-linecap="round" opacity=".8"/><ellipse cx="47" cy="54" rx="7" ry="4" fill="#fffdf4" opacity=".85" transform="rotate(-45 47 54)"/></svg>'''
 a=node(s,name,svg,f'left:{x}px;top:{y}px;width:{r*2}px;height:{r*2}px;opacity:0;',depth,'shape','data-layout-ignore')
 ft(s,a,{'opacity':0,'y':32,'x':0},{'opacity':.72 if depth=='foreground' else .48,'y':8,'x':8},f,10,'sine.out')
 to(s,a,{'y':-55-r*.25,'x':-18 if r%2 else 23,'rotation':9},f+10,life-10,'sine.inOut')
 to(s,a,{'opacity':0},f+life-8,8,'sine.in')
for s in scenes:
 if s['id']=='append-voice':
  for i,(x,y,r) in enumerate([(1710,335,86),(1550,840,43),(775,915,32),(1130,390,54),(1790,735,31)]):soap(s,'bubble-'+str(i),x,y,r,735+i*7,95-i*7,'backtext' if i%2 else 'foreground')
 if s['id']=='append-answer':
  for i,(x,y,r) in enumerate([(725,365,65),(80,780,37),(835,845,48),(1720,60,31)]):soap(s,'bubble-'+str(i),x,y,r,858+i*4,65-i*5,'backtext' if i%2==0 else 'foreground')
 if s['id']=='append-together':
  for i,(x,y,r) in enumerate([(1700,320,75),(1020,55,33),(1765,635,36)]):soap(s,'bubble-'+str(i),x,y,r,923+i*7,90-i*7,'backtext')
  # Empty upper-left field, below the lyrics and outside the portrait silhouette.
  # Inherit the scene's single dissolve; no delayed local tween or second entrance.
  img(s,'pancake-memory','revision-v22/pancake-memory.png',50,135,260,'backtext')
  mark(s,s['startFrame'],'松饼位于左上留白，随场景统一入场后保持静止','memory motif')
