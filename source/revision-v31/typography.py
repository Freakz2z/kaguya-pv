# Entrances alter only the outer type node; beat impulses stay on an inner wrapper.
# Keep first-visible timestamps, copy and resting layout; tighten long arrivals.
type_entry_evidence=[]
def strong_type_entry(s,sel,a,b,frame,dur,ease):
 is_glyph=isinstance(sel,str) and ' .glyph-' in sel
 if not isinstance(sel,str) or (sel not in s.get('typeTargets',[]) and not is_glyph):return False
 if b.get('opacity')!=1 or a.get('opacity') not in (0,1):return False
 if not (a.get('opacity')==0 or any(k in a for k in ('scale','scaleX','scaleY','x','y','clipPath'))):return False
 a=dict(a);b=dict(b);duration=max(3,min(dur,8));name=sel.rsplit('-',1)[-1]
 if s['id']=='append-finale-title':
  profile='credit-lift';a.update(y=30);b.update(y=0);duration=8
 elif 'clipPath' in a:
  profile='shutter-pull';a.pop('scale',None);b.pop('scale',None)
  # The reveal itself provides the acceleration; no simultaneous surface scaling.
 elif 'scaleY' in a:
  profile='fold-open';a['scaleY']=.06;a['rotation']=b.get('rotation',0)-16
 elif a.get('scale',1)>1:
  profile='weight-slam';a['scale']=max(1.42,a['scale']);a['y']=a.get('y',0)-22;b.setdefault('y',0)
 elif is_glyph or 'scaleX' in a:
  profile='glyph-snap';a['scaleX']=.42 if a.get('scaleX',1)<1 else 1.42;a['y']=54 if a.get('y',0)>=0 else -54
 elif abs(a.get('x',0))>0:
  profile='side-strike';a['x']=max(110,abs(a['x']))*(1 if a['x']>0 else -1)
 elif a.get('y',0)<0:
  profile='drop-lock';a['y']=min(-110,a['y'])
 elif a.get('y',0)>0:
  profile='rise-lock';a['y']=max(76,a['y']);b.setdefault('rotation',0);a['rotation']=b['rotation']-7
 else:
  profile='stamp';a['scale']=1.34;b.setdefault('scale',1)
 for k in ('x','y','rotation','scale','scaleX','scaleY'):
  if k in a and k not in b:b[k]=1 if k.startswith('scale') else 0
 # Six distinct entry shapes. Sharp attack, finite two-frame settle; no loops.
 impact=dict(b)
 settle=2 if duration>=5 and profile not in ('shutter-pull','credit-lift') else 0
 if settle:
  if profile in ('weight-slam','stamp'):impact['scale']=b.get('scale',1)*.965
  elif profile=='fold-open':impact['scaleY']=b.get('scaleY',1)*1.035
  elif profile=='glyph-snap':impact['scaleX']=b.get('scaleX',1)*1.045
  elif profile=='side-strike':impact['x']=b.get('x',0)+(-5 if a['x']>0 else 5)
  else:impact['y']=b.get('y',0)+(4 if a.get('y',0)<0 else -4)
  for k in impact:
   if k not in b and k not in ('opacity','clipPath'):b[k]=0
 start=(frame-s['startFrame'])/30
 s['js'].append(f"tl.fromTo({J(sel)},{J(a)},{J(dict(impact,duration=(duration-settle)/30,ease='expo.out' if profile!='credit-lift' else 'power3.out',immediateRender=False))},{start});")
 if settle:s['js'].append(f"tl.to({J(sel)},{J(dict(b,duration=settle/30,ease='sine.out'))},{start+(duration-settle)/30});")
 type_entry_evidence.append(dict(scene=s['id'],target=sel,profile=profile,frame=frame,settledFrame=frame+duration))
 return True
