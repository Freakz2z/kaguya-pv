# Chinese translation of the supplied audio, separate from narrative typography.
# Timing: local whisper large-v3 phrase estimates; the first post-pause vocal
# entry is overridden by the user's confirmed original preview cue 20.750.
lyrics=[
 (0,5.02,'示例字幕 · 01'),
 (5.02,9.82,'示例字幕 · 02'),
 (9.82,14.56,'示例字幕 · 03'),
 (14.56,19.72,'示例字幕 · 04'),
 (20.75,24.36,'示例字幕 · 05'),
 (24.36,27.12,'示例字幕 · 06'),
 (27.12,31.22,'示例字幕 · 07'),
 (31.22,37.36,'示例字幕 · 08'),
 (37.36,40.84,'示例字幕 · 09'),
 (40.84,46.966667,'示例字幕 · 10'),
 (46.966667,50.9,'示例字幕 · 11'),
 (50.9,54.9,'示例字幕 · 12'),
 (54.9,59.6,'示例字幕 · 13'),
]
translate_time=lambda t:t+(PAUSE_LENGTH if t>=PAUSE_AT else 0)
rows=[{'start':round(translate_time(a),6),'end':min(D,round(translate_time(b),6)),'text':txt,'sourceStart':START+a,'sourceEnd':START+b} for a,b,txt in lyrics]
chars=''.join(q['text'] for q in rows)
# Shot-specific safe corners. V31: user now requests gentle lyric beat pulses.
# Phrase anchors survive scene cuts. Only the first phrase relocates once to
# clear the incoming portrait; color alone follows the underlying shot.
corner_plan=[
 (0,107,'br','dark'),(107,196,'tl','dark'),(196,268,'tr','light'),
 (268,296,'tr','dark'),(296,412,'bl','light'),(412,590,'tr','dark'),
 (590,732,'br','light'),(732,856,'br','dark'),(856,915,'bl','dark'),
 (915,1028,'tr','dark'),(1028,1093,'tr','dark'),(1093,1173,'tl','light'),
 (1173,1389,'tr','light'),(1389,1487,'tl','dark'),(1487,1866,'tl','dark')]
submarkup=[];subjs=[];placed=[];lyric_pulses=[]
lyric_beats=json.loads((P/'source/revision-v31/lyric-beats.json').read_text())['beats']
colors={'dark':'#322438','light':'#fff0d8'}
strokes={'dark':'#f5efe7','light':'#322438'}
def layout(corner,tone,txt):
 width=550 if corner=='tl' else 760
 size=min(42,(width-8)/max(1,len(txt))-2)
 return dict(left=56 if corner.endswith('l') else 1920-56-width,
  top=30 if corner.startswith('t') else 996,width=width,height=60,
  fontSize=round(size,2),textAlign='left' if corner.endswith('l') else 'right',
  color=colors[tone],webkitTextStrokeColor=strokes[tone])
cue_corners=['br','tl','bl','tr','tr','tl','tl','tr','tr','tl','tl','tl','tl']
for cue,q in enumerate(rows):
 segments=[]
 for shot,(fa,fb,corner,tone) in enumerate(corner_plan):
  start=max(q['start'],fa/30);end=min(q['end'],fb/30)
  if end>start:
   stable_corner=cue_corners[cue]
   if cue==0 and fa>=107:stable_corner='tl' # sole within-phrase move, to avoid the new portrait
   segments.append(dict(start=start,end=end,corner=stable_corner,tone=tone))
 sel=f'cn-lyric-{cue}'
 first=segments[0];initial=layout(first['corner'],first['tone'],q['text'])
 submarkup.append(f'<div id="{sel}" class="cn-lyric clip" data-start="{q["start"]}" data-duration="{q["end"]-q["start"]}" data-track-index="0" data-label="{q["text"]}" data-layout-allow-caption-zone data-layout-allow-overflow><span id="{sel}-beat" style="display:inline-block;white-space:nowrap">{q["text"]}</span></div>')
 subjs.append(f"tl.set('#{sel}',{J(initial)},{q['start']});")
 last=None
 for seg in segments:
  corner,tone=seg['corner'],seg['tone'];start=seg['start'];style=layout(corner,tone,q['text'])
  moved=last is None or corner!=last['corner']
  if moved:
   subjs.append(f"tl.set('#{sel}-beat',{{transformOrigin:'{'0%' if corner.endswith('l') else '100%'} 50%'}},{start});")
   if last:
    subjs.append(f"tl.to('#{sel}',{{opacity:0,y:{-8 if last['corner'].startswith('t') else 8},duration:.1,ease:'power2.in'}},{start-.1});")
   subjs.append(f"tl.set('#{sel}',{J(style)},{start});")
   origin=dict(opacity=0,x=-20 if corner.endswith('l') else 20,y=-6 if corner.startswith('t') else 6)
   dest=dict(opacity=1,x=0,y=0,duration=.20,ease='power3.out',immediateRender=False)
   subjs.append(f"tl.fromTo('#{sel}',{J(origin)},{J(dest)},{start});")
  elif tone!=last['tone']:
   subjs.append(f"tl.to('#{sel}',{J(dict(color=colors[tone],webkitTextStrokeColor=strokes[tone],duration=.18,ease='sine.inOut'))},{start});")
  placed.append(dict(start=start,end=seg['end'],text=q['text'],corner=corner,tone=tone,fontSize=style['fontSize'],singleLine=True))
  last=seg
 for beat in lyric_beats:
  t=beat['frame']/30
  if not q['start']+.24<t<q['end']-.32:continue
  # Inner wrapper leaves corner, line length and color transitions independent.
  peak=round(1.035+.025*min(1,beat['strength']/3),4)
  subjs.append(f"tl.fromTo('#{sel}-beat',{{scale:1}},{{scale:{peak},duration:{1/30},ease:'power2.out',immediateRender:false}},{t-1/30});")
  subjs.append(f"tl.to('#{sel}-beat',{{scale:1,duration:{7/30},ease:'power3.out'}},{t});")
  lyric_pulses.append(dict(cue=cue,frame=beat['frame'],peakScale=peak))
 subjs.append(f"tl.to('#{sel}',{{opacity:0,duration:.10,ease:'power2.in'}},{q['end']-.10});")
(P/'source/revision-v31/lyric-pulses.json').write_text(json.dumps(lyric_pulses,ensure_ascii=False,indent=2))
subtitle_file=P/'compositions/17-中文歌词字幕.html'
subtitle_file.write_text(f'''<!doctype html><html lang="zh-CN"><body><template><style>@font-face{{font-family:LyricsCN;src:url('assets/fonts/LyricsCN.woff2')}}#chinese-lyrics-root{{position:absolute;inset:0;pointer-events:none}}#chinese-lyrics-root .cn-lyric{{position:absolute;inset:auto;width:760px;height:60px;opacity:0;overflow:visible;font:42px/1.2 LyricsCN;letter-spacing:2px;white-space:nowrap;background:none;paint-order:stroke fill;-webkit-text-stroke:.8px #f5efe7;}}</style><div id="chinese-lyrics-root" data-composition-id="chinese-lyrics" data-width="1920" data-height="1080" data-duration="{D}">{''.join(submarkup)}</div><script>(()=>{{const tl=gsap.timeline({{paused:true}});{''.join(subjs)}window.__timelines=window.__timelines||{{}};window.__timelines['chinese-lyrics']=tl;}})();</script></template></body></html>''')
main=(P/'index.html').read_text().replace('</main>',f'<div class="clip" id="slot-chinese-lyrics" data-composition-id="chinese-lyrics" data-composition-src="compositions/17-中文歌词字幕.html" data-start="0" data-duration="{D}" data-track-index="5" data-width="1920" data-height="1080" data-label="17｜中文歌词・四角书法字" style="z-index:110;pointer-events:none"></div></main>')
(P/'index.html').write_text(main)
(P/'source/revision-v22/chinese-lyrics.json').write_text(json.dumps({'basis':'User-provided song; local large-v3 phrase estimates, translated into Chinese. Post-pause onset uses user-confirmed cue. Not official Chinese subtitles.','font':'Ma Shan Zheng, OFL, Google Fonts','cues':rows,'placements':placed},ensure_ascii=False,indent=2))
