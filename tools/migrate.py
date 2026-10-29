"""Convert captured public pages into self-contained static HTML.
Run capture_original.py and prepare_assets.py first. Runtime requires no Python or PHP.
"""
from pathlib import Path
from bs4 import BeautifulSoup as Soup, Comment
from urllib.parse import urljoin,urlsplit,urlunsplit,unquote,quote,parse_qs,urlencode
import json,re,copy,hashlib
ROOT=Path(__file__).resolve().parents[1]; SOURCE=ROOT/'audit/original'
R2='https://pub-6509346c2fdc47328b748c024f30f006.r2.dev'
vendors=json.loads((ROOT/'audit/vendor-map.json').read_text());media=json.loads((ROOT/'audit/media-map.json').read_text())
URL_RE=re.compile(r'url\(\s*[\"\']?([^\)\"\']+)[\"\']?\s*\)')
features={}; titles={}; issues=[]; records=[]
for p in ROOT.rglob('index.html'):
 if any(x in p.parts for x in ['audit','.git','dist']):continue
 s=Soup(p.read_text(),'lxml');im=s.select_one('.entry-featured-img img')
 if im:features[p.relative_to(ROOT).as_posix()]=im.get('src')
for p in SOURCE.rglob('index.html'):
 s=Soup(p.read_text(),'lxml'); rel=p.relative_to(SOURCE).as_posix()
 title=s.find('meta',property='og:title');titles[rel]=title.get('content','') if title else s.title.get_text().split(' – FREAK')[0] if s.title else rel

def local(u,base):
 if u in ['xxx','yyy','Portfolio']:return '#'
 if not u or u.startswith(('data:','#','mailto:','tel:','whatsapp:')):return u
 absolute=urljoin(base,u); z=urlsplit(absolute)
 if absolute in vendors:return vendors[absolute]
 if absolute in media:return media[absolute]['url']
 if '/wp-content/uploads/' in absolute and z.hostname in ['freaklab.org','www.freaklab.org']:
  return R2+'/images/'+absolute.split('/wp-content/uploads/',1)[1]
 if z.hostname in ['freaklab.org','www.freaklab.org']:
  path=re.sub('/+','/',unquote(z.path))
  if path=='/wp-login.php' or path.startswith('/wp-admin'):return '/'
  if path=='/wp-content' or path.startswith('/wp-json') or path=='/xmlrpc.php':return '/'
  if path in ['/your@email','/yyy','/xxx','/Portfolio']:return '#'
  if '@' in path and not path.startswith('/assets/'):return 'mailto:'+path.lstrip('/')
  return quote(path,safe='/:@-._~')+('?' +z.query if z.query else '')+('#'+z.fragment if z.fragment else '')
 return absolute

def normalize(s,rel):
 base='https://freaklab.org/'+rel.removesuffix('index.html')
 # Remove server/plugin execution and stale authentication/API metadata.
 for t in list(s.find_all('script')):
  if t.get('type')!='application/ld+json':t.decompose()
 for t in list(s.find_all('link')):
  if t.attrs is None:continue
  if set(t.get('rel',[])) & {'pingback','profile','EditURI','https://api.w.org/','shortlink','prefetch'} or 'oembed' in t.get('type',''):t.decompose()
 for t in list(s.find_all('meta',attrs={'name':'generator'})):t.decompose()
 for t in list(s.find_all(string=lambda v:isinstance(v,Comment))):t.extract()
 for t in s.find_all(True):
  for attr in list(t.attrs):
   if attr.startswith('on'):del t[attr]
  if t.name=='img':
   lazy=t.get('data-lazysrc') or t.get('data-src') or t.get('data-lazy-src')
   if lazy:t['src']=lazy
   for a in ['data-lazysrc','data-src','data-lazy-src','data-srcset']:t.attrs.pop(a,None)
   t['decoding']='async'
   if not t.get('fetchpriority'):t['loading']='lazy'
  for attr in ['href','src','poster','data-src','data-flickity-lazyload']:
   if t.get(attr):t[attr]=local(t[attr],base)
  if t.get('srcset'):
   t['srcset']=', '.join(local(x.split()[0],base)+' '+ ' '.join(x.split()[1:]) for x in t['srcset'].split(',') if x.split())
  if t.get('content') and 'freaklab.org/wp-content/uploads/' in t['content']:t['content']=local(t['content'],base)
  if t.get('style'):t['style']=URL_RE.sub(lambda m:'url("'+local(m[1],base)+'")',t['style'])
  if t.name=='style' and t.string:t.string=URL_RE.sub(lambda m:'url("'+local(m[1],base)+'")',t.string)
  if t.name=='a' and t.get('target')=='_blank':t['rel']='noopener noreferrer'
  if t.name=='a' and t.get('href')=='#' and not t.get('data-open'):
   # Original placeholder links should not navigate to nonexistent pages.
   t['aria-disabled']='true'
 for im in s.select('.esg-entry-media img'):
  card=im.find_parent('li');a=card.select_one('.esg-entry-content a') if card else None
  if not im.get('alt') and a:im['alt']=a.get_text(' ',strip=True)
  if card and not im.find_parent('a'):
   target=card.select_one('a[href]')
   if target:
    a=s.new_tag('a',href=target['href']);a['tabindex']='-1';a['aria-hidden']='true';im.wrap(a)
 for el in s.select('.bg,.parallax-active'):
  classes=el.get('class',[])
  if 'bg' in classes and 'bg-loaded' not in classes:el['class']=classes+['bg-loaded']
 for el in s.select('[data-animate]'):el.attrs.pop('data-animate',None)
 for el in s.select('html'):
  el['class']=[x for x in el.get('class',[]) if x not in ['loading-site','no-js']]+['static-site']
 for a in s.select('a[href]'):
  u=a['href']
  if 'sharer.php?' in u or 'twitter.com/share?' in u or 'shareArticle?' in u or 'pinterest.com/pin/create/' in u:
   z=urlsplit(u);q=parse_qs(z.query)
   for k in ['url','u']:
    if k in q:q[k]=[base]
   a['href']=urlunsplit((z.scheme,z.netloc,z.path,urlencode(q,doseq=True),''))
 for form in s.select('form.searchform'):
  form['action']='/search/';form['method']='get'
 for form in s.select('form'):
  if 'searchform' not in form.get('class',[]):
   issues.append({'page':rel,'issue':'Original dynamic form requires a replacement service','action':form.get('action')})
 # Add the static behavior and override styles last, so legacy animation layout cannot hide content.
 for tag,attrs in [('link',{'rel':'stylesheet','href':'/assets/site.css'}),('script',{'src':'/assets/site.js','defer':''})]:
  s.head.append(s.new_tag(tag,**attrs))
 for t in list(s.select('link[rel=canonical]')):t.decompose()
 s.head.append(s.new_tag('link',rel='canonical',href=base))
 return s

homepage=Soup((SOURCE/'index.html').read_text(),'lxml')
empty=[]
for p in sorted(SOURCE.rglob('index.html')):
 rel=p.relative_to(SOURCE).as_posix(); dest=ROOT/rel
 old=Soup(dest.read_text(),'lxml') if dest.exists() else None
 source_text=p.read_text(); start=source_text.lower().find('<!doctype'); raw=Soup(source_text[start:] if start>=0 else source_text,'lxml')
 # The existing symposium is a standalone static presentation with its own controls.
 if rel=='symposium/index.html':
  s=old
  for t in list(s.select('script')):
   if t.get('src'):t.decompose()
  for t in s.find_all(True):
   for a in ['src','href','poster']:
    if t.get(a):t[a]=local(t[a],'https://freaklab.org/symposium/')
  dest.write_text(str(s));records.append({'page':rel,'source':'existing standalone symposium','title':s.title.get_text()});continue
 s=normalize(raw,rel)
 if not s.html or not s.head or not s.body:
  issues.append({'page':rel,'issue':'Invalid source HTML'});continue
 # Discard PHP notices outside the actual document.
 output=s.html
 entry=s.select_one('.entry-content.single-page')
 if entry and not entry.select_one('h1') and rel.split('/')[0] in ['projects','peoples','update','event','talk']:
  title=titles[rel];h=s.new_tag('h1');h.string=title;entry.insert(0,h)
  if rel in features:
   figure=s.new_tag('figure',attrs={'class':'entry-featured-img'})
   figure.append(s.new_tag('img',src=features[rel].replace('/thumbs/','/'),alt=title,decoding='async'))
   entry.insert(1,figure)
  # Missing body content is a source limitation, not text to fabricate.
  body=[x for x in entry.select('p,h2,h3,h4,ul,ol,table,iframe') if not x.find_parent(class_='blog-share')]
  if not body:empty.append(rel)
 if rel=='projects/index.html':
  main=s.select_one('main');main.clear()
  section=s.new_tag('section',attrs={'class':'section static-projects'});h=s.new_tag('h1');h.string='Projects';section.append(h)
  section.append(copy.deepcopy(homepage.select_one('.esg-grid')));main.append(section)
  # The copied grid comes from the original and needs the same media/URL normalization.
  normalize_grid=section
  for t in section.find_all(True):
   for a in ['src','href']:
    if t.get(a):t[a]=local(t[a],'https://freaklab.org/')
   if t.name=='img' and t.get('data-lazysrc'):t['src']=local(t['data-lazysrc'],'https://freaklab.org/');del t['data-lazysrc']
 # Capture text inventory for content auditing and static search.
 main=s.select_one('main')
 text=main.get_text(' ',strip=True) if main else ''
 records.append({'page':rel,'source':'public WordPress snapshot','title':titles[rel],'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'text_length':len(text)})
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text('<!DOCTYPE html>\n'+str(s.html)+'\n')
(ROOT/'audit/migration.json').write_text(json.dumps({'pages':records,'missing_original_body':empty,'issues':issues},indent=2,ensure_ascii=False))
# Search data has a safe text-only schema; no executable HTML enters the search UI.
index=[]
for r in records:
 p=ROOT/r['page'];s=Soup(p.read_text(),'lxml');m=s.select_one('main')
 if not m:continue
 for t in m.select('script,style,.blog-share'):t.decompose()
 text=re.sub(r'\s+',' ',m.get_text(' ',strip=True))
 index.append({'url':'/'+r['page'].removesuffix('index.html'),'title':r['title'],'text':text[:12000]})
(ROOT/'assets/search-index.json').write_text(json.dumps(index,ensure_ascii=False))
print('Migrated',len(records),'pages;',len(empty),'detail pages have no public original body.')
