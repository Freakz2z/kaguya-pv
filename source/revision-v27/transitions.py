"""Late-cut handoffs: explicit overlap + isolated shot stacking.

Reference mechanisms: installed iris-reveal and animation/css-dissolve.md.
The directional-wipe registry download timed out; the soft paper reveal below
uses authored CSS mask endpoints instead, without a new runtime dependency.
"""
handoff_scenes={s['id']:s for s in scenes}
handoff_map=[]
# The moon circles and bottom paper wave intentionally bleed past the fixed SVG
# viewport. Mark only these background shapes; clipping is part of the artwork.
s=handoff_scenes['append-answer']
s['layers']['background']=[m.replace('<circle ', '<circle data-layout-allow-overflow ')
 .replace('<path d="M0 970', '<path data-layout-allow-overflow d="M0 970')
 if 'append-answer-scene-paper' in m else m for m in s['layers']['background']]

def remove_local(s,token):
 # Remove an obsolete cover together with all its CSS and timeline tracks.
 for k in s['layers']:
  s['layers'][k]=[m for m in s['layers'][k] if token not in m]
 s['css']=[m for m in s['css'] if token not in m]
 s['js']=[m for m in s['js'] if token not in m]

def handoff(old_id,new_id,duration,mode='dissolve',delay=0):
 old=handoff_scenes[old_id];new=handoff_scenes[new_id]
 start=new['startFrame'];finish=start+delay+duration
 old['endFrame']=max(old['endFrame'],finish+1)
 # A single envelope owns the incoming stage, not a second competing fade.
 sel='#'+new_id+'-stage'
 new['stage']=True
 new['css']=[c for c in new['css'] if sel not in c]
 new['js']=[j for j in new['js'] if sel not in j]
 if mode=='dissolve':
  new['css'].append(sel+'{opacity:0;}')
  ft(new,sel,{'opacity':0},{'opacity':1},start+delay,duration,'sine.inOut')
 elif mode in ('iris','curtain','diagonal'):
  bounds={
   'iris':('circle(0% at 50% 25%)','circle(110% at 50% 25%)'),
   'curtain':('inset(0 50% 0 50%)','inset(0 0% 0 0%)'),
   'diagonal':('polygon(0% 0%,0% 0%,0% 0%,0% 0%)','polygon(0% 0%,200% 0%,0% 200%,0% 100%)')}
  before,after=bounds[mode]
  new['css'].append(sel+'{clip-path:'+before+';}')
  ft(new,sel,{'clipPath':before},{'clipPath':after},start+delay,duration,'power2.inOut')
 else:
  # 10%-wide feather, complete transparent/opaque endpoints. No image scale,
  # no off-screen slide of the scene, no extra opaque rectangle or white flash.
  angle=105 if mode=='paper-left' else 255
  mask=f'linear-gradient({angle}deg,#000 calc(var(--paper-edge) - 5%),rgba(0,0,0,0) calc(var(--paper-edge) + 5%))'
  new['css'].append(sel+'{--paper-edge:-12%;mask-image:'+mask+';-webkit-mask-image:'+mask+';}')
  ft(new,sel,{'--paper-edge':'-12%'},{'--paper-edge':'112%'},start+delay,duration,'sine.inOut')
 mark(new,start,'V27 场景交接 '+mode,'continuous scene handoff',f'{duration}帧交接，前镜延续至{finish+1}帧，不缩放人物')
 handoff_map.append(dict(outgoing=old_id,incoming=new_id,startFrame=start,finishFrame=finish,mode=mode))

# 06A -> 06B: let the final fireworks pulse land at frame720, then night merges
# into the singing paper field. The old replay must remain valid during overlap.
handoff('append-fireworks','append-voice',26,'dissolve',delay=4)
fire=handoff_scenes['append-fireworks']
fire['js']=[j.replace('END=142/30',f'END={fire["endFrame"]-590}/30') for j in fire['js']]

# Related call/response shots: one directional paper family, then a gentler hold.
handoff('append-voice','append-answer',22,'paper-right')
handoff('append-answer','append-together',22,'iris')
# Preserve uninterrupted fixed-size portrait drift at 45% of former speed.
for sid,name,initial,finish,original_duration in [
 ('append-voice','iroha',(-60,8),(80,-8),152),
 ('append-answer','kaguya',(-52,10),(34,-8),71)]:
 s=handoff_scenes[sid];sel='#'+sid+'-'+name
 s['js']=[j for j in s['js'] if J(sel) not in j]
 d=s['endFrame']-s['startFrame']
 ft(s,sel,{'x':initial[0],'y':initial[1]},
    {'x':initial[0]+(finish[0]-initial[0])*d/original_duration*.45,
     'y':initial[1]+(finish[1]-initial[1])*d/original_duration*.45},s['startFrame'],d,'none')

# Reality -> remembered song -> typography: no one-frame background replacement.
handoff('append-together','append-relay-distance',20,'curtain')
handoff('append-relay-distance','append-relay-panels',16,'dissolve')
handoff_scenes['append-relay-panels']['css'].append('#append-relay-panels-flight-prelap{opacity:0;}')
# 10 -> 11 already shares note coordinates/velocities and the launch background.
# Keep this match intact; do not cover it with an unrelated preset.

# Moon arrival -> response. Remove the white page that previously filled the
# entire shot. Keep reply typography's original1390 onset fully independent.
journey=handoff_scenes['append-relay-journey'];reply=handoff_scenes['append-relay-reply']
remove_local(journey,'paper-cut-1383');remove_local(reply,'paper-cut-1389')
journey['endFrame']=1416
targets=['#append-relay-reply-bg']+['#append-relay-reply-'+n+'-layer > .layer' for n in ['background','backtext','character','foreground']]
reply['css'].append(','.join(targets)+'{opacity:0;}')
ft(reply,targets,{'opacity':0},{'opacity':1},1389,26,'sine.inOut')
# The matte expands smoothly while the received moon remains visible below.
for edge in ['top','bottom']:
 sel='#append-relay-reply-cinema-'+edge
 reply['js']=[j for j in reply['js'] if J(sel) not in j]
 reply['css'].append(sel+'{transform-origin:50% '+('0%' if edge=='top' else '100%')+';}')
 ft(reply,sel,{'scaleY':1},{'scaleY':0},1389,26,'sine.inOut')
mark(reply,1389,'V27 月球余光叠入辉夜；回应文字保持原起点','continuous scene handoff','26帧；删除白纸整屏遮挡')
handoff_map.append(dict(outgoing=journey['id'],incoming=reply['id'],startFrame=1389,finishFrame=1415,mode='moon-response-layered-dissolve'))

# Joy -> promise closeup. Feathered paper reveals hands while Kaguya remains
# underneath; the hand keys retain their authored placement and original timing.
handoff('append-relay-reply','append-finale-answer',22,'diagonal')

# Restore requested three-colour paper transition and the local trio windows.
answer=handoff_scenes['append-finale-answer'];reunion=handoff_scenes['append-finale-reunion']
# User explicitly restored the original three-colour shutters. Both sides
# meet with the same full-screen colour blocks at frame1647, then open locally.
mark(reunion,1647,'三色块接续原位后交错打开','three-colour shutters','恢复原三色块过渡')
handoff_map.append(dict(outgoing=answer['id'],incoming=reunion['id'],startFrame=1635,finishFrame=1666,mode='three-colour-shutters'))

# Close on the existing warm title, with a soft full-scene blend rather than an
# empty yellow frame. White logo/credit transformation stays exactly where it was.
remove_local(reunion,'title-wash')
handoff('append-finale-reunion','append-finale-title',24,'dissolve')

# Explicit new request permits a subtle portrait enlargement in scene19 only.
ft(reunion,'#append-finale-reunion-concert-art img',{'scale':1,'transformOrigin':'50% 65%'},{'scale':1.055},1647,reunion['endFrame']-1647,'none')

(P/'source/revision-v27/handoffs.json').write_text(json.dumps(handoff_map,ensure_ascii=False,indent=2)+'\n')
