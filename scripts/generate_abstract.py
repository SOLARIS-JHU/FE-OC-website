"""Generate the function-encoder workflow, with operation-based SVG animation.

Scientific structure: arXiv:2509.18404v2, Algorithms 1-2 and Section III.
The animation shows computational stages; it contains no benchmark trajectories.
Embed the animated SVG inline. Set data-paused="true" on its root to pause.
CSS prefers-reduced-motion produces the same legible structure without motion.
"""
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'figures'

def text(x, y, value, size=17, color='#002d72', weight=500, anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{color}" font-weight="{weight}">{escape(value)}</text>'

def rect(x, y, w, h, kind='fa-node'):
    fill,stroke=('#edf8f5','#9fcfc5') if kind=='fa-operator' else (('#eaf2fc','#8faecf') if kind=='fa-policy' else ('#fff','#b9cada'))
    return f'<rect class="{kind}" x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>'

def arrow(path, kind='fa-wire', marker='fa-arrow'):
    stroke={'fa-wire':'#7b95b1','fa-repeat':'#85719b','fa-frozen':'#002d72','fa-operator-transfer':'#4f8e87'}[kind]
    dash=' stroke-dasharray="6 5"' if kind=='fa-operator-transfer' else ''
    return f'<path class="{kind}" d="{path}" fill="none" stroke="{stroke}" stroke-width="2.1" stroke-linejoin="round"{dash} marker-end="url(#{marker})"/>'

def flow(path, kind):
    return f'<path class="fa-flow {kind}" d="{path}" fill="none" stroke="#007e79" stroke-width="4" stroke-linecap="round" stroke-dasharray="2 22" opacity="0"/>'

BASE_CSS = '''
.feoc-abstract { display:block; width:100%; height:auto; font-family:Arial,Helvetica,sans-serif; }
.feoc-abstract .fa-panel { fill:#f7f9fc; stroke:#d8e2ed; stroke-width:1.2; }
.feoc-abstract .fa-online-panel { fill:#f6faf9; }
.feoc-abstract .fa-node { fill:#fff; stroke:#b9cada; stroke-width:1.4; }
.feoc-abstract .fa-operator { fill:#edf8f5; stroke:#9fcfc5; stroke-width:1.4; }
.feoc-abstract .fa-policy { fill:#eaf2fc; stroke:#8faecf; stroke-width:1.4; }
.feoc-abstract .fa-wire { fill:none; stroke:#7b95b1; stroke-width:2.1; stroke-linejoin:round; }
.feoc-abstract .fa-repeat { fill:none; stroke:#85719b; stroke-width:2.1; stroke-linejoin:round; }
.feoc-abstract .fa-frozen { fill:none; stroke:#002d72; stroke-width:2.1; stroke-linejoin:round; }
.feoc-abstract .fa-operator-transfer { fill:none; stroke:#4f8e87; stroke-width:2.1; stroke-linejoin:round; stroke-dasharray:6 5; }
.feoc-abstract .fa-flow { fill:none; stroke:#007e79; stroke-width:4; stroke-linecap:round; stroke-linejoin:round; stroke-dasharray:2 22; opacity:0; }
.feoc-abstract .fa-learning { stroke:#6c4a8c; }
.feoc-abstract .fa-feedback { stroke:#002d72; }
.feoc-abstract .fa-stage-label { letter-spacing:1.1px; }
'''

ANIMATION_CSS = '''
@keyframes fa-travel { to { stroke-dashoffset:-48; } }
@keyframes fa-training { 0%,42% { opacity:1; } 47%,100% { opacity:0; } }
@keyframes fa-operator-fit { 0%,34% { opacity:0; } 38%,46% { opacity:1; } 49%,100% { opacity:0; } }
@keyframes fa-data-inference { 0%,48% { opacity:0; } 51%,59% { opacity:1; } 63%,100% { opacity:0; } }
@keyframes fa-parameter-inference { 0%,72% { opacity:0; } 75%,83% { opacity:1; } 87%,100% { opacity:0; } }
@keyframes fa-feedback-steps { 0%,55% { opacity:0; } 58%,98% { opacity:1; } 100% { opacity:0; } }
@keyframes fa-gradient-step { 0%,8%,20%,32%,44%,100% { fill:#fff; stroke:#b9cada; } 12%,24%,36% { fill:#e5d7f0; stroke:#6c4a8c; } }
.feoc-abstract .fa-training-flow { animation:fa-travel 1.1s linear infinite,fa-training 12s linear infinite; }
.feoc-abstract .fa-learning { animation:fa-travel 1.1s linear infinite,fa-training 12s linear infinite; }
.feoc-abstract .fa-operator-fit { animation:fa-travel 1.1s linear infinite,fa-operator-fit 12s linear infinite; }
.feoc-abstract .fa-data-inference { animation:fa-travel 1.1s linear infinite,fa-data-inference 12s linear infinite; }
.feoc-abstract .fa-parameter-inference { animation:fa-travel 1.1s linear infinite,fa-parameter-inference 12s linear infinite; }
.feoc-abstract .fa-feedback { animation:fa-travel 1.1s linear infinite,fa-feedback-steps 12s linear infinite; }
.feoc-abstract .fa-update { animation:fa-gradient-step 12s linear infinite; }
.feoc-abstract[data-paused="true"] *, .feoc-abstract[data-paused="true"] { animation-play-state:paused!important; }
@media(prefers-reduced-motion:reduce) {
  .feoc-abstract *, .feoc-abstract { animation:none!important; }
  .feoc-abstract .fa-flow { opacity:0!important; }
}
'''

def generate(animated):
    parts = [
      '<svg xmlns="http://www.w3.org/2000/svg" id="feoc-abstract" class="feoc-abstract" viewBox="0 0 1080 650" font-family="Arial,Helvetica,sans-serif" role="img" aria-labelledby="fa-title fa-description" data-paused="false">',
      '<title id="fa-title">Function encoder policies: offline learning and online transfer</title>',
      '<desc id="fa-description">Training demonstrations support alternating least-squares coefficient solves and gradient updates of shared neural bases, using reconstruction loss and a basis-norm penalty. An optional operator is trained on task specifications and coefficient targets after freezing the bases. The frozen bases transfer to both the online least-squares solve and the feedback policy; the trained operator transfers to online coefficient inference. For a new task, either demonstrations and least squares or a task specification and the trained operator produce coefficients. The coefficients combine fixed bases into a feedback policy; applied controls evolve the system and its next state and time return to the policy.</desc>',
      '<style>'+BASE_CSS+(ANIMATION_CSS if animated else '')+'</style>',
      '<defs><marker id="fa-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#7b95b1"/></marker><marker id="fa-purple-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#85719b"/></marker><marker id="fa-blue-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#002d72"/></marker><marker id="fa-teal-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#4f8e87"/></marker></defs>',
      '<rect width="1080" height="650" rx="16" fill="#fff"/>',
      '<rect class="fa-panel" x="18" y="18" width="1044" height="268" rx="16" fill="#f7f9fc" stroke="#d8e2ed" stroke-width="1.2"/>',
      '<rect class="fa-panel fa-online-panel" x="18" y="306" width="1044" height="326" rx="16" fill="#f6faf9" stroke="#d8e2ed" stroke-width="1.2"/>',
      text(40,48,'OFFLINE  ·  LEARN A REUSABLE CONTROL BASIS',17,weight=700,anchor='start'),
      text(40,337,'ONLINE  ·  ADAPT TO A NEW OBJECTIVE',17,weight=700,anchor='start'),
      # Offline nodes. The loss and gradient update are one computational stage.
      rect(40,106,180,84),rect(265,106,190,84),
      rect(510,106,225,84,'fa-node fa-update'),rect(815,106,220,84,'fa-operator'),
      text(130,133,'Training',18,weight=700),text(130,155,'demonstrations',18,weight=700),
      text(130,177,'state · time · control',14,color='#53677e'),
      text(360,137,'Least-squares solve',18,weight=700),text(360,164,'Task coefficients',15,color='#53677e'),
      text(622.5,129,'Update neural bases',18,weight=700),
      text(622.5,150,'Reconstruction loss',14,color='#53677e'),text(622.5,168,'+ basis-norm penalty',14,color='#53677e'),
      text(925,133,'Optional operator',18,weight=700),text(925,155,'Fit task parameters to',14,color='#53677e'),text(925,174,'coefficient targets',14,color='#53677e'),
      arrow('M220 148H265'),arrow('M455 148H510'),
      arrow('M622.5 190V229H360V190','fa-repeat','fa-purple-arrow'),
      text(490,252,'Recompute coefficients after each gradient step',14,color='#6c4a8c'),
      arrow('M360 106V80H925V106'),text(686,72,'Coefficient targets; bases frozen',14,color='#53677e'),
      text(925,215,'Train separately after',14,color='#53677e'),text(925,235,'the shared bases are learned',14,color='#53677e'),
      # A fixed transfer, deliberately not animated: learned bases are copied/frozen.
      arrow('M735 148H774V365H360V391','fa-frozen','fa-blue-arrow'),
      arrow('M645 365V426','fa-frozen','fa-blue-arrow'),
      text(659,355,'Frozen bases',15,weight=700,anchor='start'),
      arrow('M1035 148H1047V620H360V566','fa-operator-transfer','fa-teal-arrow'),
      text(450,610,'Frozen operator',14,color='#397a73',weight=700,anchor='start'),
      # Online adaptation routes.
      rect(40,391,185,64),rect(265,391,190,64),rect(40,502,185,64),rect(265,502,190,64,'fa-operator'),
      text(132.5,416,'New-task',17,weight=700),text(132.5,438,'demonstrations',17,weight=700),
      text(360,417,'Least-squares solve',18,weight=700),text(360,440,'Task coefficients',14,color='#53677e'),
      text(132.5,540,'Task specification',17,weight=700),text(360,528,'Trained operator',18,weight=700),text(360,551,'Task coefficients',14,color='#53677e'),
      text(248,595,'Choose either inference route',14,color='#53677e'),
      rect(535,426,220,108,'fa-policy'),rect(825,439,210,81),
      text(645,452,'Feedback policy',19,weight=700),text(645,479,'Combine fixed bases',15,color='#53677e'),text(645,502,'with task coefficients',15,color='#53677e'),
      text(930,468,'System dynamics',19,weight=700),text(930,497,'Apply control',15,color='#53677e'),
      arrow('M225 423H265'),arrow('M225 534H265'),
      arrow('M455 423H492V479H535'),arrow('M455 534H492V479H535'),
      arrow('M755 479H825'),text(790,466,'control',13,color='#53677e'),
      arrow('M930 520V588H645V534','fa-frozen','fa-blue-arrow'),
      text(794,612,'Next state + time',15,color='#002d72'),
      # Moving markers encode execution/order, never measured state trajectories.
      flow('M220 148H265','fa-training-flow'),flow('M455 148H510','fa-learning'),
      flow('M622.5 190V229H360V190','fa-learning'),
      flow('M360 106V80H925V106','fa-operator-fit'),
      flow('M225 423H265','fa-data-inference'),flow('M455 423H492V479H535','fa-data-inference'),
      flow('M225 534H265','fa-parameter-inference'),flow('M455 534H492V479H535','fa-parameter-inference'),
      flow('M755 479H825','fa-feedback'),flow('M930 520V588H645V534','fa-feedback'),
      '</svg>'
    ]
    result='\n'.join(parts)+'\n'
    ET.fromstring(result)
    return result

OUT.mkdir(exist_ok=True,parents=True)
(OUT/'graphical-abstract-animated.svg').write_text(generate(True),encoding='utf-8')
(OUT/'graphical-abstract-static.svg').write_text(generate(False),encoding='utf-8')
print('Generated animated and static function-encoder abstracts.')
