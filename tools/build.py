"""Create the clean Hostatom document root. Python standard library only."""
from pathlib import Path
import shutil,json,re
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'public'
# Only generated output is replaced, never editorial content or WordPress files.
if OUT.exists():shutil.rmtree(OUT)
OUT.mkdir()
skip={'.git','.vercel','audit','content','public','dist','tools','wp-content','wp-includes','images'}
count=0
for p in ROOT.rglob('*.html'):
 rel=p.relative_to(ROOT)
 if any(x in skip for x in rel.parts):continue
 target=OUT/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);count+=1
needed={'assets/site.js','assets/site.css','assets/search-index.json'}
def remember(url):
 z=urlsplit(url.strip())
 if z.scheme or z.netloc:return
 path=unquote(z.path).lstrip('/')
 if path.startswith('assets/'):needed.add(path)
def css(text):
 for match in re.finditer(r'url\(\s*([\"\']?)(.*?)\1\s*\)',text):remember(match[2])
class References(HTMLParser):
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  for key in ['src','href','poster']:remember(attrs.get(key,''))
  if 'srcset' in attrs:
   for candidate in attrs['srcset'].split(','):remember(re.sub(r'\s+\d+(?:w|x)$','',candidate.strip()))
  css(attrs.get('style',''))
  self.in_style=tag=='style'
 def handle_endtag(self,tag):
  if tag=='style':self.in_style=False
 def handle_data(self,text):
  if getattr(self,'in_style',False):css(text)
for page in OUT.rglob('*.html'):References().feed(page.read_text())
processed=set()
while needed-processed:
 for rel in list(needed-processed):
  path=ROOT/rel
  if not path.exists():raise FileNotFoundError(rel)
  if path.suffix=='.css':css(path.read_text())
  target=OUT/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target);processed.add(rel)
(ROOT/'audit/build.json').write_text(json.dumps({'html_documents':count,'assets':len(processed),'media_assets':sum('/media/' in p for p in processed),'bytes':sum((OUT/p).stat().st_size for p in processed)},indent=2))
for name in ['.htaccess','robots.txt','sitemap.xml','feed.xml']:
 if (ROOT/name).exists():shutil.copy2(ROOT/name,OUT/name)
print('Built',count,'HTML documents in public/; no WordPress, PHP, or server-side dependencies.')
