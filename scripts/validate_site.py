"""Offline integrity and scientific transcription checks; Python standard library."""
import hashlib, json, re, sys
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
errors=[]
def check(ok, message):
    if not ok: errors.append(message)
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]; self.refs=[]; self.images=[]; self.meta=[]; self.headings=[]; self.lang=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.append(a['id'])
        for key in ['href','src']:
            if a.get(key): self.refs.append(a[key])
        if tag=='img': self.images.append(a)
        if tag=='meta': self.meta.append(a)
        if tag=='html': self.lang=a.get('lang')
        if re.fullmatch('h[1-6]',tag): self.headings.append(tag)
html=(ROOT/'index.html').read_text(encoding='utf-8')
page=Page(); page.feed(html)
check(page.lang=='en','Missing language')
check(len(page.ids)==len(set(page.ids)),'Duplicate IDs')
check(page.headings.count('h1')==1,'Expected one h1')
check('\ufffd' not in html,'Invalid text encoding')
check(not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',html),'Unexpected control character')
check('class="skip"' in html and 'role="status"' in html,'Missing accessibility affordances')
for img in page.images:
    check(bool(img.get('alt','').strip()),f'Missing image alt: {img.get("src")}')
    check('width' in img and 'height' in img,f'Missing image dimensions: {img.get("src")}')
def reference(ref, origin):
    u=urlsplit(ref)
    if u.scheme or u.netloc: return
    check(not u.path.startswith('/'),f'Root-relative URL: {ref}')
    if not u.path:
        if u.fragment: check(unquote(u.fragment) in page.ids,f'Broken anchor: {ref}')
        return
    p=(origin.parent/unquote(u.path)).resolve()
    check(p.is_relative_to(ROOT) and p.is_file(),f'Missing local dependency: {ref}')
for ref in page.refs: reference(ref,ROOT/'index.html')
for p in [ROOT/'template.css',ROOT/'style.css',*list((ROOT/'assets').rglob('*.css'))]:
    for ref in re.findall(r'url\(\s*[\"\']?([^\)\"\']+)',p.read_text(encoding='utf-8')): reference(ref.strip(),p)
authors=['Xingjian Li','Kelvin Kan','Deepanshu Verma','Krishna Kumar','Stanley Osher','Ján Drgoňa']
check([m['content'] for m in page.meta if m.get('name')=='citation_author']==authors,'Citation authors mismatch')
ld=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S).group(1))
check([a['name'] for a in ld['author']]==authors,'JSON-LD author mismatch')
bib=re.search(r'<code id="bibtex">(.*?)</code>',html,re.S).group(1).strip()
check(unescape(bib)==(ROOT/'citation.bib').read_text(encoding='utf-8').strip(),'BibTeX mismatch')
data=json.loads((ROOT/'data/results.json').read_text(encoding='utf-8'))
for key in ['table1','table2','table3']:
    table=re.search(r'<table class="results" id="'+key+r'".*?</table>',html,re.S).group(0)
    rows=[[unescape(re.sub('<[^>]+>','',c).strip()) for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>',r,re.S)] for r in re.findall(r'<tr>(.*?)</tr>',table,re.S)[1:]]
    check(rows==data[key],key+' transcription mismatch')
check('No demonstrations from the new task' in html and 'New task data are required' in html,'Missing transfer-route qualifications')
check('no end-to-end timing table' in html,'Missing timing qualification')
check('squared control norms' in html,'Missing paper-code discrepancy')
check(not re.search(r'__[A-Z_]+__|TODO|lorem ipsum',html),'Unresolved placeholder')
manifest=json.loads((ROOT/'assets/manifest.json').read_text(encoding='utf-8'))
for name,digest in manifest.items():
    p=ROOT/name
    check(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,f'Asset changed: {name}')
graphic=(ROOT/'assets/figures/graphical-abstract.svg').read_bytes()
check(hashlib.sha1(b'blob '+str(len(graphic)).encode()+b'\0'+graphic).hexdigest()=='a5d6c72b02d5b6f9756fc7ec97e15efe62d893fb','Original SOLARIS graphic changed')
for p in (ROOT/'assets').rglob('*.svg'):
    for e in ET.parse(p).iter():
        check(e.tag.rsplit('}',1)[-1] not in {'script','foreignObject'},f'Active SVG content: {p.name}')
        for k,v in e.attrib.items():
            check(not k.lower().startswith('on'),f'SVG event handler: {p.name}')
            if k.rsplit('}',1)[-1]=='href': check(not v.startswith(('http:','https:','//')),f'External SVG asset: {p.name}')
if errors:
    print('\n'.join('ERROR: '+e for e in errors)); sys.exit(1)
print(f'PASS: {len(page.images)} images, {len(page.refs)} references, {len(manifest)} asset checksums, all three tables, citations, SVG integrity.')
