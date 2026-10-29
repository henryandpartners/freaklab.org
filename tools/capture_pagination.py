from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlsplit,unquote,quote
from concurrent.futures import ThreadPoolExecutor
import subprocess
ROOT=Path(__file__).resolve().parents[1];CACHE=ROOT/'audit/original'
for turn in range(4):
 missing=set()
 for p in CACHE.rglob('index.html'):
  for a in BeautifulSoup(p.read_text(),'lxml').select('a[href]'):
   u=urlsplit(urljoin('https://freaklab.org/'+p.relative_to(CACHE).as_posix().removesuffix('index.html'),a['href']))
   if u.hostname!='freaklab.org':continue
   path=unquote(u.path).strip('/')
   if ('/page/' in path or path=='tag/คนรับใช้') and not (CACHE/path/'index.html').exists():missing.add(path)
 if not missing:break
 def get(path):
  p=CACHE/path/'index.html';p.parent.mkdir(parents=True,exist_ok=True)
  r=subprocess.run(['curl','-L','--max-time','25','-sS','-w','%{http_code}','https://freaklab.org/'+quote(path,safe='/')+'/','-o',str(p)],capture_output=True,text=True)
  if r.stdout!='200':p.unlink(missing_ok=True)
  return (path,r.stdout)
 with ThreadPoolExecutor(max_workers=8) as pool:print(list(pool.map(get,sorted(missing))),flush=True)
