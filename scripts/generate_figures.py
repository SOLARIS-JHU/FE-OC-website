"""Generate exact SVG explanations and a chart from paper table entries.

No simulation, invented benchmark curves, or inferred uncertainty.
Uses Python's standard library; results.json retains original decimal strings.
"""
from pathlib import Path
from decimal import Decimal
import json
import html

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/figures'
D=json.loads((ROOT/'data/results.json').read_text(encoding='utf-8'))

def text(x,y,s,size=20,color='#1a1f2b',anchor='start',weight='400'):
    return f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}">{html.escape(s)}</text>'

def frame(w,h,title,desc):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(desc)}</desc><rect width="{w}" height="{h}" rx="14" fill="white"/>']

svg=frame(1000,480,'Objective comparison on new tasks','Relative increases in the published mean objective, computed from Tables I and II. Lower is closer to the numerical reference. No uncertainty was reported.')
svg += [text(38,42,'Transfer to new objectives',27,'#002d72',weight='600'),text(38,73,'Relative increase in mean objective versus the numerical reference',17,'#5b6470')]
for x,c,label in [(614,'#002d72','FE–LS'),(759,'#0b847b','FE–operator')]:
    svg += [f'<circle cx="{x}" cy="110" r="6" fill="{c}"/>',text(x+14,116,label,18)]
left,right,top,bottom=335,925,151,381
for tick in range(0,11,2):
    x=left+tick/10*(right-left)
    svg += [f'<path d="M{x} {top} V{bottom}" stroke="#dfe3ea"/>',text(x,410,f'{tick}%',17,'#5b6470','middle')]
items=[('2D · interpolation',D['table1'][1]),('2D · extrapolation',D['table1'][2]),('Quadcopter · new targets',D['table2'][1])]
for row,(label,values) in enumerate(items):
    y=185+row*82
    svg += [text(38,y+6,label,19)]
    ref=Decimal(values[1])
    for offset,col,color in [(-12,2,'#002d72'),(12,3,'#0b847b')]:
        val=100*(Decimal(values[col])/ref-1)
        x=left+float(val)/10*(right-left)
        svg += [f'<path d="M{left} {y+offset} H{x}" stroke="{color}" stroke-opacity=".3" stroke-width="3"/>',f'<circle cx="{x}" cy="{y+offset}" r="6" fill="{color}"/>',text(x+13,y+offset+6,f'{val:.2f}%',17,color)]
svg += [text(38,454,'Source: arXiv:2509.18404v2, Tables I–II · ratio of rounded means · no error bars available',15,'#5b6470'),'</svg>']
(OUT/'objective-comparison.svg').write_text(''.join(svg),encoding='utf-8')

svg=frame(1000,310,'Feedback deployment with fixed policy bases','Current state and time enter fixed bases. Task coefficients combine their outputs into a control action. The dynamics evolve and return the next state to the policy. Coefficient inference is performed for the task before this feedback loop.')
svg += ['<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="#002d72"/></marker></defs>']
svg += [text(35,37,'ONLINE FEEDBACK  ·  basis parameters remain fixed',18,'#002d72',weight='600')]
for x,w,title,line in [(180,240,'Evaluate fixed bases','φ₁(x,t), …, φₚ(x,t)'),(500,195,'Combine','u = Σⱼ cⱼ φⱼ'),(780,185,'Dynamics','ẋ = f(x,u,t)')]:
    svg += [f'<rect x="{x}" y="125" width="{w}" height="90" rx="12" fill="#f1f6fc" stroke="#bdcde0"/>',text(x+w/2,159,title,21,'#002d72','middle','600'),text(x+w/2,192,line,20,'#1a1f2b','middle')]
svg += [text(35,163,'State + time',18),text(35,191,'x(t), t',20),text(599,79,'Task coefficients c(η)',19,'#0b847b','middle')]
for path in ['M126 170 H180','M420 170 H500','M695 170 H780','M599 90 V125','M872 215 V269 H105 V215 H180']:
    svg += [f'<path d="{path}" fill="none" stroke="#002d72" stroke-width="2.2" marker-end="url(#arrow)"/>']
svg += [text(457,157,'φⱼ',18,'#5b6470','middle'),text(737,157,'u(t)',18,'#5b6470','middle'),text(489,296,'Updated state feeds the next policy evaluation',17,'#5b6470','middle'),'</svg>']
(OUT/'feedback.svg').write_text(''.join(svg),encoding='utf-8')
print('Generated exact table chart and static feedback diagram.')
