from pathlib import Path
from bs4 import BeautifulSoup as Soup
from urllib.parse import urlsplit,unquote,urljoin
from collections import Counter
import json,re,copy
ROOT=Path(__file__).resolve().parents[1]
MEDIA=json.loads((ROOT/'audit/media-map.json').read_text())
INLINE=json.loads((ROOT/'audit/inline-map.json').read_text())
EXTERNAL=json.loads((ROOT/'audit/external-image-map.json').read_text())
R2='https://pub-6509346c2fdc47328b748c024f30f006.r2.dev'
# Prefer the verified original for a resized background or thumbnail of the same file.
def best_image(url):
 if '/thumbs/' in url:url=url.replace('/thumbs/','/')
 match=re.sub(r'-\d+x\d+(?=\.[a-zA-Z]+(?:[?#]|$))','',url)
 if match==url:return url
 original='https://freaklab.org/wp-content/uploads/'+match.split('/images/',1)[1] if '/images/' in match else ''
 result=MEDIA.get(original,{})
 if result.get('status')==200 and not result.get('missing'):return result['url']
 return url
pages=[p for p in ROOT.rglob('index.html') if not any(x in p.relative_to(ROOT).parts for x in ['audit','public','dist','.git','wp-content','wp-includes'])]
for p in pages:
 text=p.read_text();s=Soup(text,'lxml')
 if s.body and not s.body.get('id'):s.body['id']='top'
 for style in s.select('style'):
  if style.string:
   style.string=re.sub(r'url\(([\"\']?)([^)\"\']+)\1\)',lambda m:'url("'+INLINE.get(m[2],m[2])+'")',style.string)
 for link in list(s.select('link[rel=alternate]')):
  if 'rss' in link.get('type',''):
   if 'comment' in link.get('title','').lower():link.decompose()
   else:link['href']='/feed.xml'
 for a in list(s.select('a[href]')):
  if a.get_text(' ',strip=True).lower()=='login':
   parent=a.find_parent('li');(parent if parent else a).decompose()
 main=s.select_one('main')
 if main and not main.select_one('h1'):
  heading=s.new_tag('h1',attrs={'class':'screen-reader-text'});heading.string=s.title.get_text().split(' – FREAK')[0] if s.title else 'FREAK lab';main.insert(0,heading)

 for img in s.select('img[src]'):
  replacement=EXTERNAL.get(img['src'])
  if replacement:
   if replacement.get('unavailable'):
    old=img['src'];basename=urlsplit(old).path.rsplit('/',1)[-1]
    label=re.sub(r'-\d+x\d+(?=\.[^.]+$)','',basename).rsplit('.',1)[0].replace('_',' ').replace('-',' ').strip()
    if label.startswith('grid '):label='Biomimicry award coverage'
    if label=='heatshot Wares':label='Wares Chancharoen'
    placeholder=s.new_tag('span',attrs={'class':'unavailable-image','role':'img','aria-label':label+' — image unavailable'})
    placeholder.string=label+' — image unavailable'
    img.replace_with(placeholder)
    parent=placeholder.parent
    if parent.name=='a' and parent.get('href') in EXTERNAL and EXTERNAL[parent['href']].get('unavailable'):parent.unwrap()
    continue
   img['src']=replacement['url']
   if img.get('srcset'):
    img['srcset']=', '.join(EXTERNAL.get(x.split()[0],{}).get('url',x.split()[0])+' '+' '.join(x.split()[1:]) for x in img['srcset'].split(',') if x.split() and not EXTERNAL.get(x.split()[0],{}).get('unavailable'))
  u=img['src'];img['src']=best_image(u)
  # Use actual original image dimensions where available; preserve existing responsive variants.
  if img.get('srcset') and 'thumbs/' in img['srcset']:del img['srcset']
 for t in s.select('style'):
  if t.string:t.string=re.sub(r'url\(([\"\']?)([^)\"\']+)\1\)',lambda m:'url("'+best_image(m[2])+'")',t.string)
 for a in s.select('a[href]'):
  u=a['href']
  if u=='/featured_item/space-food/':a['href']='/projects/space-food/'
  if u in ['xxx','yyy','Portfolio'] or u.endswith(('/xxx','/yyy','/Portfolio')):a['href']='#';a['aria-disabled']='true'
  if u.startswith('/wp-content/uploads/'):
   source='https://freaklab.org'+u;a['href']=MEDIA.get(source,{}).get('url',R2+'/images/'+u.split('/uploads/',1)[1])
 for t in s.select('script[src],link[href]'):
  attr='src' if t.name=='script' else 'href'
  if t.get(attr,'').startswith('/wp-') and t.get('rel')!=['canonical']:
   # No copied WordPress scripts/styles remain required in the runtime.
   if t.name=='script' or t.get('rel')==['stylesheet']:raise RuntimeError(f'Legacy runtime dependency in {p}: {t[attr]}')
 p.write_text('\n'.join(line.rstrip(' \t') for line in ('<!DOCTYPE html>\n'+str(s.html)).splitlines())+'\n')
# Eliminate URLs for optional theme demo decoration that never existed on the original server.
for p in (ROOT/'assets/vendor').glob('*.css'):
 t=p.read_text();t=re.sub(r'url\([\"\']?https?://(?:www\.)?freaklab\.org/[^)\"\']+[\"\']?\)', 'url("data:image/gif;base64,R0lGODlhAQABAAAAACw=")',t);p.write_text(t)
base=Soup((ROOT/'index.html').read_text(),'lxml')
for name,title,markup in [
 ('search','Search','<section class="static-search"><h1>Search FREAK lab</h1><form id="static-search" action="/search/" role="search"><label for="query">Name, project, or research topic</label><input id="query" name="s" type="search"><button type="submit">Search</button></form><div id="search-results" aria-live="polite"></div></section>'),
 ('404','Page not found','<section class="static-search"><h1>Page not found</h1><p>The page may have moved. Browse our research or search the archive.</p><p><a href="/research/">Research</a> · <a href="/people/">People</a> · <a href="/search/">Search</a></p></section>')]:
 s=copy.deepcopy(base);s.body['class']=s.body.get('class',[])+['static-utility'];main=s.select_one('main');main.clear();main.append(Soup(markup,'html.parser'));s.title.string=title+' – FREAK lab'
 header=s.select_one('#header');header['class']=[c for c in header.get('class',[]) if c!='has-transparent']
 for t in s.select('link[rel=canonical]'):t['href']='https://freaklab.org/'+name+'/'
 for t in s.select('style'):
  # Homepage banner-specific styles are harmless but not needed on utility pages.
  if t.string and re.match(r'\s*#banner-',t.string):t.decompose()
 if name=='404':(ROOT/'404.html').write_text('<!DOCTYPE html>\n'+str(s.html))
 else:(ROOT/name).mkdir(exist_ok=True);(ROOT/name/'index.html').write_text('<!DOCTYPE html>\n'+str(s.html))
index=[];routes=[]
for p in ROOT.rglob('index.html'):
 if any(x in p.relative_to(ROOT).parts for x in ['audit','public','dist','.git','wp-content','wp-includes']):continue
 s=Soup(p.read_text(),'lxml');m=s.select_one('main') or (s.body if p.parent.name=='symposium' else None)
 if not m:continue
 for t in m.select('script,style,.blog-share'):t.decompose()
 title=s.title.get_text().split(' – FREAK')[0] if s.title else p.parent.name
 text=re.sub(r'\s+',' ',m.get_text(' ',strip=True));url='/'+p.relative_to(ROOT).as_posix().removesuffix('index.html')
 index.append({'url':url,'title':title,'text':text});routes.append(url)
(ROOT/'assets/search-index.json').write_text(json.dumps(index,ensure_ascii=False))
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>https://freaklab.org'+url+'</loc></url>' for url in sorted(routes))+'</urlset>\n')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://freaklab.org/sitemap.xml\n')
feed=ROOT/'feed.xml'
if feed.exists():
 text=feed.read_text()
 for original,result in sorted(MEDIA.items(),key=lambda item:len(item[0]),reverse=True):
  if result.get('status')!=200 or result.get('missing'):continue
  target=result['url'];target='https://freaklab.org'+target if target.startswith('/') else target
  text=text.replace(original,target)
 feed.write_text('\n'.join(line.rstrip(' \t') for line in text.splitlines())+'\n')
print('Finalized',len(routes),'routes and static search records.')
