# Additional finite, non-position-jitter beat impulses. Do not pulse the Chinese
# subtitle composition (handled separately), characters, pancake, or credits.
import re
extra_specs={
 'distance':[('even',73,1.10),('memory',98,1.045),('remember-label',98,1.025)],
 'voice':[('accent',185,1.12)],
 'promise':[('one',285,1.07)],
 'night':[('n2',391,1.07)],
 'return':[('backpromise',511,1.055),('close-a',551,1.15),('close-b',570,1.13)],
 'append-voice':[('this',755,1.075),('voiceword',790,1.09),('reach',843,1.09),('bubble-0',772,1.12),('bubble-3',799,1.10)],
 'append-answer':[('truly',902,1.065),('bubble-0',888,1.12),('bubble-2',902,1.10)],
 'append-together':[('again',950,1.065),('met',959,1.11),('ending',986,1.085),('ending-tab',986,1.04),('bubble-0',977,1.12),('bubble-1',994,1.1)],
 'append-relay-distance':[('voice',1048,1.045),('reach-1',1057,1.08),('reach-2',1075,1.10),('small-star',1084,1.15)],
 'append-relay-panels':[('relay-a',1128,1.13),('relay-b',1142,1.13)],
 'append-relay-journey':[('far-phrase',1244,1.055)],
 'append-relay-reply':[('reply-0',1414,1.08),('reply-2',1432,1.07),('reply-yo',1450,1.10),('joy-0',1441,1.16),('joy-1',1450,1.13),('joy-2',1467,1.13)],
 'append-finale-answer':[('voice-key',1503,1.045),('here-key',1540,1.055),('answer-glyph-0',1610,1.10),('answer-glyph-2',1610,1.07),('answer-glyph-4',1627,1.075),('answer-star-0',1610,1.15),('answer-star-1',1627,1.14)],
 'append-finale-reunion':[('concert-star-0',1684,1.12),('concert-star-1',1702,1.14),('promise',1702,1.06)],
}
new_pulses=[]
onsets=json.loads((P/'source/revision-v20/music-onsets.json').read_text())['onsets']
for s in scenes:
 for name,f,peak in extra_specs.get(s['id'],[]):
  if f>700:
   q=min(onsets,key=lambda q:abs(q['frame']-f))
   if abs(q['frame']-f)<=5:f=q['frame']
  key=s['id']+'-'+name;inner=key+'-impulse';exists=False
  for layer,items in s['layers'].items():
   for i,m in enumerate(items):
    if f'id="{key}"' not in m:continue
    exists=True
    if f'id="{inner}"' not in m:
     head,body=m.split('>',1)
     items[i]=head+'><span id="'+inner+'" data-layout-allow-overflow data-layout-allow-occlusion style="display:block;width:100%;height:100%;transform-origin:50% 55%">'+body[:-6]+'</span></div>'
  if not exists:raise ValueError('Missing pulse '+key)
  ft(s,'#'+inner,{'scale':1},{'scale':peak},f-2,2,'power3.in')
  to(s,'#'+inner,{'scale':1},f,7,'power3.out')
  new_pulses.append(dict(scene=s['id'],target=key,frame=f,peakScale=peak,releaseFrames=7))
  mark(s,f,'补充鼓点脉冲 '+name,'selected existing onset','独立内层缩放；中文歌词和人物排除')
(P/'source/revision-v31/entrance-map.json').write_text(json.dumps(type_entry_evidence,ensure_ascii=False,indent=2))
(P/'source/revision-v31/extra-pulses.json').write_text(json.dumps(new_pulses,ensure_ascii=False,indent=2))
