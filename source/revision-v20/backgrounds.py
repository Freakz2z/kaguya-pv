# Scene-specific print-paper graphics. No buildings; clear fields around faces.
def print_field(s,mode):
 s['css'].append('#'+s['id']+'-root{isolation:isolate;}')
 sid=s['id']
 if mode=='voice':
  shapes='<path d="M0 0H710Q900 390 610 1080H0Z" fill="#c8cbdc"/><path d="M0 890Q500 700 910 940T1920 950V1080H0Z" fill="#dfc8d1"/><path data-layout-allow-overflow d="M-50 929Q490 755 950 972T1980 985" fill="none" stroke="#f5efe7" stroke-width="7"/>'
  dots=''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="#82778c"/>' for x in range(40,620,22) for y in range(80,1040,22))
  shapes+=f'<g opacity=".19">{dots}</g>'
 elif mode=='answer':
  shapes='<path d="M0 0H1920V1080H0Z" fill="#eee7f0"/><circle cx="1490" cy="400" r="635" fill="#f7f0dd"/><circle cx="1470" cy="410" r="602" fill="none" stroke="#cebad8" stroke-width="3"/><path d="M0 970Q610 850 1040 1010T1920 990V1080H0Z" fill="#d7c9df"/>'
  shapes+='<g fill="#d2ae74" opacity=".8"><path d="M980 160l8 25 25 8-25 8-8 25-8-25-25-8 25-8Z"/><path d="M1700 120l5 16 16 5-16 5-5 16-5-16-16-5 16-5Z"/><circle cx="900" cy="750" r="4"/></g>'
 else:
  shapes='<rect width="1920" height="1080" fill="#f4e4da"/><path d="M0 0H1920V165Q1230 80 720 165T0 160Z" fill="#ead5d5"/><ellipse data-layout-allow-overflow cx="710" cy="650" rx="835" ry="650" fill="#fbf1df"/><path d="M0 1000Q740 825 1920 930V1080H0Z" fill="#e5bdc7"/><path d="M1260 95Q1490 75 1800 120L1820 815Q1570 850 1380 810" fill="none" stroke="#cba1b3" stroke-width="3"/>'
  petals=[(1430,85,14),(1720,885,-22),(1250,920,28),(1850,270,10)]
  shapes+=''.join(f'<path d="M-12 0Q-4-27 12-18Q30 3-12 0Z" transform="translate({x} {y}) rotate({a})" fill="#c77c9b" opacity=".44"/>' for x,y,a in petals)
 sel=node(s,'scene-paper',f'<svg width="100%" height="100%" viewBox="0 0 1920 1080">{shapes}</svg>','inset:0;width:100%;height:100%;transform-origin:50% 50%;','background')
 return sel
