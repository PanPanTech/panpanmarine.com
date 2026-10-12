from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote
from urllib.request import urlopen
import json
import re
import xml.etree.ElementTree as ET
from marine_blog import load_posts, CATEGORIES, article_path

ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'
routes=json.loads((DIST/'page-manifest.json').read_text(encoding='utf-8'))
posts=load_posts(ROOT)
expected=43+1+len(CATEGORIES)+len(posts)
assert len(routes)==expected, f'Expected {expected} routes, got {len(routes)}'
assert len({p['title'] for p in routes})==len(routes), 'Duplicate page titles'
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
 html=file.read_text(encoding='utf-8')
 p=Page();p.feed(html)
 if '/blog/' not in p.refs:errors.append(f'{path}: missing blog navigation')
 for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S):json.loads(block)
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
origin=json.loads((ROOT/'config.json').read_text(encoding='utf-8'))['site_origin']
sitemap=ET.parse(DIST/'sitemap.xml')
indexed={e.text for e in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')}
for r in routes:
 if (origin+r['path'] in indexed)==r.get('noindex',False):errors.append(f"{r['path']}: sitemap/indexing mismatch")
feed=ET.parse(DIST/'blog/feed.xml')
assert len(feed.findall('./channel/item'))==len(posts), 'RSS article count mismatch'
for post in posts:
 html=(DIST/article_path(post).strip('/')/'index.html').read_text(encoding='utf-8')
 blocks=[json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)]
 article=next(s for s in blocks if s.get('@type')=='BlogPosting')
 faq=next(s for s in blocks if s.get('@type')=='FAQPage')
 assert article['url']==origin+article_path(post)
 assert len(faq['mainEntity'])==len(post['faq'])
 assert all(f'id="{section["id"]}"' in html and f'href="#{section["id"]}"' in html for section in post['sections'])
assert not errors, '\n'.join(errors)
print(f'PASS: {len(routes)} HTTP routes, local links/assets, metadata, blog navigation, article schema, TOC, RSS and sitemap indexing.')
