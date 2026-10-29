"""Vendor presentation assets and verify public R2 media without bucket credentials."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlsplit,unquote
from concurrent.futures import ThreadPoolExecutor,as_completed
import subprocess,re,hashlib,json
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'assets/vendor';OUT.mkdir(parents=True,exist_ok=True)
R2='https://pub-6509346c2fdc47328b748c024f30f006.r2.dev'
URL_RE=re.compile(r'url\(\s*[\"\']?([^\)\"\']+)[\"\']?\s*\)')
def fetch(url,path):
 path.parent.mkdir(parents=True,exist_ok=True)
 r=subprocess.run(['curl','-L','--max-time','35','--retry','1','-sS','-w','%{http_code}',url,'-o',str(path)],capture_output=True,text=True)
 return r.stdout=='200'
def absurl(u,base='https://freaklab.org/'):
 return urljoin(base,u)
manifest=json.loads((ROOT/'audit/vendor-map.json').read_text()) if (ROOT/'audit/vendor-map.json').exists() else {}; failed=[]
def vendor(url):
 url=absurl(url)
 if url in manifest:return manifest[url]
 ext=Path(urlsplit(url).path).suffix or '.bin'; rel='assets/vendor/'+hashlib.sha256(url.encode()).hexdigest()[:16]+ext
 p=ROOT/rel
 if not p.exists() and not fetch(url,p):failed.append(url);p.unlink(missing_ok=True);return url
 manifest[url]='/'+rel
 if ext=='.css':
  text=p.read_text(errors='replace')
  def sub(m):
   u=m[1].strip()
   if u.startswith('data:'):return m[0]
   return 'url("'+vendor(absurl(u,url))+'")'
  text=URL_RE.sub(sub,text);p.write_text(text)
 return manifest[url]
css=set();media=set()
for p in (ROOT/'audit/original').rglob('*.html'):
 s=BeautifulSoup(p.read_text(),'html.parser')
 for t in s.select('link[rel=stylesheet]'):
  u=absurl(t.get('href',''))
  if urlsplit(u).hostname=='freaklab.org':css.add(u)
 for t in s.find_all(True):
  for attr in ['src','href','data-src','data-lazy-src','data-lazysrc','poster','content']:
   u=t.get(attr,'')
   if 'wp-content/uploads/' in u and re.search(r'\.(?:jpe?g|png|gif|webp|svg|ico)(?:[?#]|$)',u,re.I):media.add(absurl(u))
  for item in t.get('srcset','').split(','):
   bits=item.split()
   if bits and 'wp-content/uploads/' in bits[0]:media.add(absurl(bits[0]))
 for m in URL_RE.finditer(p.read_text()):
  if 'wp-content/uploads/' in m[1]:media.add(absurl(m[1]))
content_file=ROOT/'audit/published-content.json'
if content_file.exists():
 data=json.loads(content_file.read_text())
 for attachment in data.get('media',[]):
  u=attachment.get('url','')
  if re.search(r'\.(?:jpe?g|png|webp|gif|svg)(?:[?#]|$)',u,re.I):media.add(u)
for u in sorted(css):vendor(u)
# Inline icon fonts are relative to the original page but served from known theme paths.
for ext in ['woff2','woff','ttf','eot']:
 vendor('https://freaklab.org/wp-content/themes/flatsome/assets/css/icons/fl-icons.'+ext+'?v=3.18.2')
(ROOT/'audit/vendor-map.json').write_text(json.dumps(manifest,indent=2))
print('Vendored',len(manifest),'assets; failures',failed,flush=True)
existing=json.loads((ROOT/'audit/media-map.json').read_text()) if (ROOT/'audit/media-map.json').exists() else {}
def check(u):
 key=u.split('/wp-content/uploads/',1)[1].split('?')[0]
 target=R2+'/images/'+key
 if u in existing:return u,existing[u]
 r=subprocess.run(['curl','-I','-L','--max-time','15','-sS','-w','%{http_code}',target,'-o','/dev/null'],capture_output=True,text=True)
 if r.stdout=='200':return u,{'url':target,'status':200}
 # Preserve missing images locally from the original site, avoiding a runtime WordPress dependency.
 rel='assets/media/'+key
 if fetch(u,ROOT/rel):return u,{'url':'/'+rel,'status':200,'fallback':'original public file'}
 (ROOT/rel).unlink(missing_ok=True)
 return u,{'url':target,'status':int(r.stdout) if r.stdout.isdigit() else 0,'missing':True}
with ThreadPoolExecutor(max_workers=12) as pool:
 for i,t in enumerate(as_completed([pool.submit(check,u) for u in media]),1):
  u,result=t.result();existing[u]=result
  if i%100==0:print('Media checked',i,'/',len(media),flush=True)
(ROOT/'audit/media-map.json').write_text(json.dumps(existing,indent=2))
print('Media complete',len(existing),'missing',sum(v.get('missing',False) for v in existing.values()),flush=True)
