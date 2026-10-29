"""Recover image files from their original public URLs; reject HTML error responses."""
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,unquote
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import json,subprocess,hashlib,re,tempfile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/external';OUT.mkdir(exist_ok=True)
report=json.loads((ROOT/'audit/image-verification.json').read_text())
urls=[x['url'] for x in report['additional_checks'] if x['status']!=200]
R2='https://pub-6509346c2fdc47328b748c024f30f006.r2.dev'
def recover(u):
 z=urlsplit(u);candidates=[]
 if z.hostname and z.hostname.startswith('pub-') and z.path.startswith('/images/'):
  candidates=['https://freaklab.org/wp-content/uploads/'+z.path.split('/images/',1)[1]]
 elif z.hostname=='pat.design':
  path=z.path
  candidates=['https://pat.design'+path,R2+'/images/'+path.split('/uploads/',1)[1]]
 elif z.hostname=='www.iafastro.org':candidates=['https://www.iafastro.org'+z.path,'https://iafastro.org'+z.path]
 else:candidates=[u]
 ext=Path(unquote(z.path)).suffix
 if ext.lower() not in ['.jpg','.jpeg','.png','.gif','.webp','.svg']:ext='.jpg'
 rel='assets/external/'+hashlib.sha256(u.encode()).hexdigest()[:16]+ext;out=ROOT/rel
 for candidate in candidates:
  r=subprocess.run(['curl','-L','--max-time','10','-sS','-w','%{http_code}',candidate,'-o',str(out)],capture_output=True,text=True)
  if r.stdout!='200':continue
  try:
   with Image.open(out) as image:width,height=image.size;image.verify()
  except Exception:continue
  return u,{'url':'/'+rel,'recovered_from':candidate,'width':width,'height':height,'status':200}
 out.unlink(missing_ok=True);return u,{'url':u,'unavailable':True}
with ThreadPoolExecutor(max_workers=8) as pool:results=dict(pool.map(recover,urls))
(ROOT/'audit/external-image-map.json').write_text(json.dumps(results,indent=2));print('Recovered',sum(not v.get('unavailable') for v in results.values()),'of',len(results),'external image URLs',flush=True)
print('Remaining',[u for u,v in results.items() if v.get('unavailable')],flush=True)
