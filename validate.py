from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
from urllib.request import urlopen
import json

ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'
routes=json.loads((DIST/'page-manifest.json').read_text(encoding='utf-8'))
assert len(routes)==24, f'Expected 24 planned routes, got {len(routes)}'
assert len({p['title'] for p in routes})==24, 'Duplicate page titles'
errors=[]
class Page(HTMLParser):
 def __init__(self): super().__init__();self.h1=0;self.refs=[];self.images=[];self.meta={};self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if a.get('id'):self.ids.add(a['id'])
  if tag in ['a','link'] and a.get('href'):self.refs.append(a['href'])
  if tag in ['img','script'] and a.get('src'):self.refs.append(a['src'])
  if tag=='img':self.images.append(a)
  if tag=='meta':self.meta[a.get('name','')]=a.get('content','')

for r in routes:
 path=r['path'];file=DIST/path.strip('/')/'index.html' if path!='/' else DIST/'index.html'
 p=Page();p.feed(file.read_text(encoding='utf-8'))
 if p.h1!=1:errors.append(f'{path}: h1 count {p.h1}')
 if not p.meta.get('description'):errors.append(f'{path}: missing description')
 for im in p.images:
  if not im.get('alt'):errors.append(f'{path}: missing image alt')
 for ref in p.refs:
  u=urlparse(ref)
  if u.scheme or u.netloc:continue
  target=DIST/unquote(u.path).lstrip('/') if u.path else file
  if u.path.endswith('/'):target=target/'index.html'
  if not target.exists():errors.append(f'{path}: missing {ref}')
 with urlopen('http://127.0.0.1:4173'+path,timeout=10) as res:
  if res.status!=200:errors.append(f'{path}: HTTP {res.status}')
 if path=='/thank-you/' and 'noindex' not in p.meta.get('robots',''):errors.append('Confirmation must be noindex')
assert not errors, '\n'.join(errors)
print('PASS: all 24 routes return HTTP 200; local links and assets resolve; unique titles, descriptions, H1 and image alt text present.')
