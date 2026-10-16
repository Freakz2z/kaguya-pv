# A nested wrapper isolates pulse from typography entrance/placement transforms.
# Small finite impulses on selected existing detected beat/onset anchors only.
pulse_specs={
 'distance':[('far',53,5),('star',89,4)],
 'voice':[('voice',125,5),('notgone',178,4)],
 'promise':[('one',268,7),('ja',268,5),('na',268,5),('i',268,5)],
 'night':[('again',339,4),('n1',375,4)],
 'append-voice':[('voiceword',770,6),('toyou',822,5)],
 'append-answer':[('heard',890,5)],
 'append-relay-distance':[('reach-0',1075,4)],
 'append-relay-panels':[('glyph-0',1129,6),('glyph-1',1129,5),('glyph-2',1129,6)],
 'append-relay-journey':[('far-phrase',1233,4),('toward-you',1299,4),('arrived',1374,4),('arrival-star-0',1374,7)],
}
# Retain prior exact bass anchors for original shots. Continuation targets use
# nearest measured spectral-onset candidates (<=0.16 s) from the source track.
onsets=json.loads((P/'source/revision-v20/music-onsets.json').read_text())['onsets']
pulse_evidence=[]
import re
for s in scenes:
 for name,f,amount in pulse_specs.get(s['id'],[]):
  anchor='existing detected musical accent'
  if f>590:
   near=min(onsets,key=lambda q:abs(q['frame']-f))
   if abs(near['frame']-f)<=5:f=near['frame'];anchor='source spectral onset candidate'
  key=s['id']+'-'+name;inner=key+'-impulse'
  found=False
  for layer,items in s['layers'].items():
   for idx,markup in enumerate(items):
    if f'id="{key}"' in markup:
     parts=markup.split('>',1)
     items[idx]=parts[0]+'><span id="'+inner+'" data-layout-allow-overflow data-layout-allow-occlusion style="display:block;width:100%;height:100%;transform-origin:50% 60%">'+parts[1][:-6]+'</span></div>'
     found=True
  if not found:raise ValueError('Missing pulse target '+key)
  # Isotropic 4-7% expansion at the accent, then a smooth 8-frame release.
  # All entrance position/rotation remain exclusively on the outer wrapper.
  peak=1+(amount+3)/100
  ft(s,'#'+inner,{'scale':1},{'scale':peak},f-1,1,'power2.out')
  to(s,'#'+inner,{'scale':1},f,8,'power3.out')
  mark(s,f,'鼓点缩放 '+name,anchor,'只缩放内层，位置与旋转不变，中文歌词排除')
  pulse_evidence.append(dict(scene=s['id'],element=key,frame=f,time=f/30,peakScale=peak,releaseFrames=8,anchor=anchor))
(P/'source/revision-v22/beat-scale-pulses.json').write_text(json.dumps(pulse_evidence,ensure_ascii=False,indent=2))
