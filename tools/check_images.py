"""Check public image URLs referenced by the deployment. No storage credentials used."""
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,re,subprocess
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'public';manifest=json.loads((ROOT/'audit/media-map.json').read_text())
verified={v['url'] for v in manifest.values() if v.get('status')==200 and not v.get('missing')}
previous_file=ROOT/'audit/image-verification.json'
if previous_file.exists():
 for result in json.loads(previous_file.read_text()).get('additional_checks',[]):
  if result.get('status')==200:verified.add(result['url'])
urls=set()
for p in SITE.rglob('*.html'):
 s=BeautifulSoup(p.read_text(),'lxml')
 for im in s.select('img[src]'):urls.add(im['src'])
 for im in s.select('img[srcset]'):
  for candidate in im['srcset'].split(','):
   if candidate.split():urls.add(candidate.split()[0])
 for t in s.select('style,[style]'):
  text=t.get_text() if t.name=='style' else t['style']
  for u in re.findall(r'url\([\"\']?([^\)\"\']+)',text):
   if re.search(r'\.(?:jpe?g|png|webp|gif|svg)(?:[?#]|$)',u,re.I):urls.add(u)
remote={u for u in urls if urlsplit(u).scheme in ['http','https']}
unchecked=remote-verified
results=[]
def check(u):
 r=subprocess.run(['curl','-I','-L','--max-time','20','-sS','-w','%{http_code}',u,'-o','/dev/null'],capture_output=True,text=True)
 return {'url':u,'status':int(r.stdout) if r.stdout.isdigit() else 0}
with ThreadPoolExecutor(max_workers=8) as pool:
 for result in pool.map(check,sorted(unchecked)):results.append(result)
report={'remote_image_urls':len(remote),'previously_verified_in_media_audit':len(remote&verified),'additional_checks':results,'local_originals':sum(p.is_file() for p in (SITE/'assets/media').rglob('*')),'missing_unused_original_attachment':[u for u,v in manifest.items() if v.get('missing')]}
(ROOT/'audit/image-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='additional_checks'},indent=2));print('Additional image checks',len(results),'failed',sum(x['status']!=200 for x in results))
