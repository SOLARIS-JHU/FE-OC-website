"""Create a social preview with the paper title and an explanatory policy diagram."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
R=Path(__file__).resolve().parents[1]
im=Image.new('RGB',(1200,630),'#fbfbfd'); d=ImageDraw.Draw(im)
font=lambda n,s:ImageFont.truetype(str(R/'assets/fonts'/n),s)
d.rectangle((0,0,1200,12),fill='#002d72')
d.text((48,39),'SOLARIS  /  FUNCTION ENCODER POLICIES',font=font('font-4.ttf',22),fill='#002d72')
for i,line in enumerate(['Zero-Shot Transferable Solution Method','for Parametric Optimal Control Problems']):
    d.text((48,92+i*57),line,font=font('font-1.ttf',43),fill='#1a1f2b')
d.text((48,226),'Reusable policy bases. New objectives. No basis retraining.',font=font('font-2.ttf',23),fill='#5b6470')
for x,label,sub in [(48,'Learn bases','offline imitation'),(430,'Infer coefficients','LS or operator'),(812,'Evaluate policy','state feedback')]:
    d.rounded_rectangle((x,326,x+335,510),radius=18,fill='#eef4fa',outline='#bdcde0',width=2)
    d.text((x+24,365),label,font=font('font-4.ttf',27),fill='#002d72')
    d.text((x+24,419),sub,font=font('font-2.ttf',22),fill='#5b6470')
for x in [390,772]:
    d.line((x,418,x+28,418),fill='#002d72',width=3)
    d.polygon([(x+28,418),(x+19,412),(x+19,424)],fill='#002d72')
d.text((48,564),'Li · Kan · Verma · Kumar · Osher · Drgoňa  |  ACC 2026',font=font('font-2.ttf',22),fill='#5b6470')
im.save(R/'assets/social-preview.png',optimize=True)
print('Created 1200 × 630 social preview.')
